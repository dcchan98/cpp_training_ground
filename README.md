# cpp_training_ground

# TODO cpp is cool and all, and using it makes you feel like a bad ass. These tools make you feel more bad ass, and remove some clunky parts by having a cooler print which python does better (the only thing it does better lel) 


# cp qol (code forces and leetcode)

# Python generation

Generate full file, run and copy to clipboard
```bash
python3 run_generate_and_copy.py  --run --copy 
```

leetcode mode
```bash
python3 run_generate_and_copy.py  --run  
python3 run_generate_and_copy.py --remove_prints --single_class Solution --copy
```

Generate full file and removing print statements ( Modify )
To modify exclusion lines , change `REMOVE_PREFIXES` variable inside file `run_generate_and_copy.py` 
```bash
python3 run_generate_and_copy.py --remove_prints --run 
```
- commands for python script 
  - Generate single file and copy all
  - optional flag to remove print and pprint and cout
  - optional flag to run 
  - optional flag to copy to clipboard


  - single_class python parameter, follow by the class name to copy , for leetcode as leetcode submissions just require the Solution class

# TODO Clion being free for practice , and good ui, and me being a fan of jetbrains, and setting up run configs to use std=c++23 , as well as run config for python

# 

# Run commands

## Compile and run

main
```bash
# Compile
g++ -std=c++23 main.cpp -o bin/main

# Run
./bin/main      # for mac and linux
# bin\main.exe  # for windows
```

notes
```bash
# Compile
g++ -std=c++23 dc_notes.cpp -o bin/dc_notes

# Run
./bin/dc_notes      # for mac and linux
# bin\dc_notes.exe  # for windows
```

# Todo

- Experiment if i can add run configurations to github
  - If yes > create read me section
- Make python script better and more maintanable 
- Make read me nice
