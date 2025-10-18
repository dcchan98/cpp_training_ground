#!/usr/bin/env python3
import os
import re
from pathlib import Path
import argparse
import subprocess
import platform

# --- CONFIG ---
ROOT = Path(__file__).parent
SRC_DIRS = [ROOT / "cp_util", ROOT / "include"]
MAIN_FILE = ROOT / "main.cpp"
OUTPUT_FILE = ROOT / "bin" / "combined.cpp"
BINARY_FILE = ROOT / "bin" / "main"  # compiled executable

# Lines to remove if `--remove_prints` is set
REMOVE_PREFIXES = ["print", "pprint"]

# --------------
INCLUDE_PATTERN = re.compile(r'#\s*include\s*[<"].*[>"]')
# --- after reading headers and main_code ---
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

    start_idx = match.start()
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
    """Copy the content of file_path to the system clipboard."""
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
def clean_code(code: str, remove_prints=False) -> str:
    cleaned_lines = []
    for line in code.splitlines():
        stripped = line.strip()

        # Removal of pragma once
        if stripped.startswith("#pragma once"):
            continue

        # Remove all #include lines except '#include <bits/stdc++.h>'
        if stripped.startswith("#include") and "<bits/stdc++.h>" not in stripped:
            continue

        # Optional removal of print/pprint lines
        if remove_prints:
            if any(stripped.startswith(prefix) for prefix in REMOVE_PREFIXES):
                continue

        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def gather_headers(dirs, remove_prints=False):
    headers = []
    for d in dirs:
        for path in sorted(d.glob("**/*.hpp")):
            with open(path, "r", encoding="utf-8") as f:
                content = clean_code(f.read(), remove_prints=remove_prints)
                headers.append(f"\n// ===== {path.relative_to(ROOT)} =====\n{content}\n")
    return headers

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
    print(f"▶️ Running: {binary}")
    if platform.system() == "Windows":
        run_cmd = [str(binary) + ".exe"]
    else:
        run_cmd = [str(binary)]
    result = subprocess.run(run_cmd, text=True)
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

    combined = [
        "// ==============================================",
        "// Auto-generated single-file C++ source",
        "// Generated by run_generate_and_copy.py",
        "// ==============================================\n",
        *headers,
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