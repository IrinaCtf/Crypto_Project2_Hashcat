==============================
 Corruption Localization Tool
==============================

This Python project detects the index where a corruption (insertion) has occurred in a string message.
It uses recursive segment hashing and comparison to efficiently localize inserted content in a corrupted message.

------------
File Structure
------------

├── main.py           # Entry point of the program (supports inline or file-based testing)
├── tag.py            # Contains the recursive tag(message) function
├── localize.py       # Contains the localize(corrupted_msg, reference_tags) function
└── testcase/         # Folder with .txt test files (used when READ_FROM_TXT is enabled)
    ├── test1.txt     # Each file must contain:
    ├── test2.txt         Line 1: original message
                          Line 2: corrupted message (with inserted content)

------------
How It Works
------------

1. `tag.py` defines a `tag(message)` function that:
   - Recursively hashes segments of the input message using SHA-256.
   - Returns a list of segment hashes.

2. `localize.py` defines a `localize(corrupted_msg, reference_tags)` function that:
   - Recursively segments the corrupted message using the same logic as `tag()`
   - Compares each segment hash to the original hash list.
   - Returns the starting index of the first mismatched segment.

3. `main.py` allows two modes:
   - Inline test cases embedded directly in the code.
   - File-based test cases stored under the `testcase/` directory.

To switch between modes, change the following line in `main.py`:
```python
READ_FROM_TXT = False   # Set to True to use testcase folder
