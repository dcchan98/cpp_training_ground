# TODO introduction cpp_training_ground
# TODO cp qol (code forces and leetcode)
# TODO cpp is cool and all, and using it makes you feel like a bad ass. These tools make you feel more bad ass, and remove some clunky parts by having a cooler print which python does better (the only thing it does better lel)
# TODO Clion being free for practice , and good ui, and me being a fan of jetbrains, and setting up run configs to use std=c++23 , as well as run config for python

# Python forge

Running **forge** script will always create a generated file. We can then add some flags for further functionality. Here are some examples.
For a fill list of supported arguments, run `python3 forge.py --help`

Regular mode (runs full file) , generate full combined file , copy to clipboard
```bash
python3 forge.py --remove_prints  --run --copy 
```

Leetcode mode (runs full file) , generate single class file , copy to clipboard
```bash
python3 forge.py --run  
python3 forge.py --remove_prints --copy --single_class Solution
```

# Todo
- Experiment if i can add run configurations to github
    - If yes > create read me section
- Make python script better and more maintanable
- Make read me nice


# Vanilla run commands for main.cpp / dc_notes 
main
```bash
# Compile
g++ -std=c++23 main.cpp -o bin/main

# Run
./bin/main      # for mac and linux
# bin\main.exe  # for windows
```

dc_notes
```bash
# Compile
g++ -std=c++23 dc_notes.cpp -o bin/dc_notes

# Run
./bin/dc_notes      # for mac and linux
# bin\dc_notes.exe  # for windows
```

