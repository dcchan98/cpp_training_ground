#!/usr/bin/env python3
import os
import re
from pathlib import Path
import argparse
import subprocess
import platform

# --- CONFIG ---
ROOT = Path(__file__).parent
REMOVE_PREFIXES = ["print", "pprint"]  # Lines to remove if starts with these
SRC_DIRS = [ROOT / "cp_util", ROOT / "include"]  # Modify files to include more hpp directory if needed
MAIN_FILE = ROOT / "main.cpp"  # Script entry point
OUTPUT_FILE = ROOT / "bin" / "combined.cpp"  # Generated Script Output
BINARY_FILE = ROOT / "bin" / "combined"  # compiled executable


def clean_code(code: str, remove_prints=False) -> str:
    """
    Clean C++ source code by removing redundant or unwanted lines.

    This function:
      - Removes all `#include` statements except `#include <bits/stdc++.h>`
      - Removes `#pragma once`
      - Optionally removes lines that start with prefixes like `print` or `pprint`

    Args:
        code (str): The C++ source code to clean.
        remove_prints (bool, optional): If True, remove lines starting with debug print prefixes.

    Returns:
        str: The cleaned C++ source code.
    """
    cleaned_lines = []
    for line in code.splitlines():
        stripped = line.strip()

        # Remove pragma once
        if stripped.startswith("#pragma once"):
            continue

        # Remove all #include except bits/stdc++.h
        if stripped.startswith("#include") and "<bits/stdc++.h>" not in stripped:
            continue

        # Optional removal of print/pprint
        if remove_prints and any(stripped.startswith(prefix) for prefix in REMOVE_PREFIXES):
            continue

        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def gather_headers(dirs, remove_prints=False):
    """
     Collect and clean all `.hpp` header files from the given directories.

     This function recursively searches through each directory in `dirs` for `.hpp` files,
     cleans them using `clean_code()`, and returns a list of formatted header contents
     ready to be concatenated into a single C++ file.

     Args:
         dirs (list[Path]): A list of directories to search for `.hpp` files.
         remove_prints (bool, optional): If True, remove lines starting with debug print
             prefixes such as `print` or `pprint`.

     Returns:
         list[str]: A list of cleaned and formatted header file contents.
     """
    headers = []
    for d in dirs:
        for path in sorted(d.glob("**/*.hpp")):
            with open(path, "r", encoding="utf-8") as f:
                content = clean_code(f.read(), remove_prints=remove_prints)
                headers.append(f"\n// ===== {path.relative_to(ROOT)} =====\n{content}\n")
    return headers


def extract_class(code: str, class_name: str) -> str:
    """
    Extract a single C++ class definition by name.
    Assumes well-formed code and braces match correctly.
    """
    if not class_name:
        return code

    pattern = re.compile(rf'class\s+{class_name}\b.*?{{', re.DOTALL)
    match = pattern.search(code)
    if not match:
        print(f"⚠️ Class '{class_name}' not found in code.")
        return ""

    brace_count = 0
    inside_class = False
    extracted_lines = []

    for line in code[match.start():].splitlines():
        if '{' in line:
            brace_count += line.count('{')
            inside_class = True
        if '}' in line:
            brace_count -= line.count('}')
        if inside_class:
            extracted_lines.append(line)
        if inside_class and brace_count == 0:
            break

    return "\n".join(extracted_lines)


def copy_to_clipboard(file_path: Path):
    """Copy the content of file_path to the system clipboard (cross-platform, no external deps)"""
    system = platform.system()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if system == "Darwin":  # macOS
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            p.communicate(input=content.encode())
        elif system == "Windows":
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            p.communicate(input=content.encode())
        elif system == "Linux":
            # Requires xclip or xsel installed
            p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            p.communicate(input=content.encode())
        else:
            print(f"⚠️ Unsupported OS: {system}")
            return
        print(f"📋 Copied {file_path} to clipboard!")
    except Exception as e:
        print(f"❌ Failed to copy to clipboard: {e}")


def compile_cpp(source: Path, output: Path):
    os.makedirs(output.parent, exist_ok=True)
    compile_cmd = ["g++", "-std=c++23", str(source), "-o", str(output)]
    print(f"🛠️ Compiling: {' '.join(compile_cmd)}")
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Compilation failed:")
        print(result.stderr)
        return False
    print(f"✅ Compiled successfully: {output}")
    return True

def run_binary(binary: Path):
    """Run the compiled binary and clearly sandwich its output in the terminal."""
    print(f"▶️ Running: {binary}\n")

    if platform.system() == "Windows":
        run_cmd = [str(binary) + ".exe"]
    else:
        run_cmd = [str(binary)]

    # Print start sandwich
    print("\n" + "="*80)
    print("🔥 Binary Output Start 🔥")
    print("="*80 + "\n")

    # Run the binary
    result = subprocess.run(run_cmd, text=True)

    # Print end sandwich
    print("\n" + "="*80)
    print("🔥 Binary Output End 🔥")
    print("="*80 + "\n")

    if result.returncode != 0:
        print(f"⚠️ Program exited with code {result.returncode}")

def main():
    parser = argparse.ArgumentParser(description="Generate single-file C++ source.")
    parser.add_argument("--remove_prints", action="store_true",
                        help="Remove lines starting with print or pprint")
    parser.add_argument("--run", action="store_true",
                        help="Compile and run the generated C++ file")
    parser.add_argument("--copy", action="store_true",
                        help="Copy generated C++ file to clipboard")
    parser.add_argument("--single_class", type=str, default="",
                        help="Only include the specified class in the generated file (Such as for LeetCode which only needs Solution)")
    args = parser.parse_args()

    os.makedirs(ROOT / "bin", exist_ok=True)

    headers = gather_headers(SRC_DIRS, remove_prints=args.remove_prints)
    with open(MAIN_FILE, "r", encoding="utf-8") as f:
        main_code = clean_code(f.read(), remove_prints=args.remove_prints)

    # --- Prepare combined content ---
    if args.single_class:
        all_code = "\n".join(headers) + "\n" + main_code
        extracted = extract_class(all_code, args.single_class)
        combined = [
            "// ==============================================",
            "// Auto-generated single-file C++ source - Single class",
            "// Generated by forge.py",
            "// Source: https://github.com/dcchan98/cpp_training_ground",
            "// ==============================================\n",
            "#include <bits/stdc++.h>",
            "using namespace std;\n",
            extracted,
        ]
    else:
        combined = [
            "// ==============================================",
            "// Auto-generated single-file C++ source",
            "// Generated by forge.py",
            "// Source: https://github.com/dcchan98/cpp_training_ground",
            "// ==============================================\n",
            *headers,
            "#include <bits/stdc++.h>",
            "using namespace std;\n",
            "\n// ===== main.cpp =====\n",
            main_code,
            "\n// ==============================================\n"
        ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(combined))

    print(f"✅ Generated {OUTPUT_FILE.relative_to(ROOT)}")

    if args.run:
        if compile_cpp(OUTPUT_FILE, BINARY_FILE):
            run_binary(BINARY_FILE)
    if args.copy:
        copy_to_clipboard(OUTPUT_FILE)


if __name__ == "__main__":
    main()
