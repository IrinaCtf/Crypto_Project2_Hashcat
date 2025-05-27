# Corruption Localization Tool

NYU Tandon, Applied Cryptograph, 2025 Spring Best Final Project

## Project Structure

├── experiment.py # Automates randomized corruption experiments and computes statistics.  
├── main.py # Core runner: runs inline tests or reads from the testcase/ folder.  
├── localize.py # Implements the corruption localization logic.  
├── tag.py # Generates recursive SHA-256 hash tags from both ends of the message.  
├── TestcaseGen.py # Utility to write formatted testcases into the testcase/ folder.  
├── testcase/ # Folder containing testcase#.txt files.  
  └── testcase0.txt, testcase1.txt, ...



---

## How It Works

### Tagging (`tag.py`)
Messages are recursively divided and hashed from both the start and end. This produces two sequences of hash digests.

### Localization (`localize.py`)
A corrupted message is compared against the tagged original. The function identifies the earliest point where hash mismatches begin (from both ends) and returns the maximum index as the corruption start.

### Main Runner (`main.py`)
- If `READ_FROM_TXT = False`: runs predefined inline test cases.
- If `READ_FROM_TXT = True`: loads test cases from the `testcase/` folder.

### Experimentation (`experiment.py`)
Automatically creates randomized corruptions and measures localization accuracy across many trials. Reports minimum, maximum, average, and standard deviation of localization factors.

### Testcase Generation (`TestcaseGen.py`)
Writes custom test cases to the `testcase/` folder. Automatically finds the smallest unused `testcase#.txt` file name.

---

## Test Case Format (`testcase/testcase#.txt`)

Each test file must contain:
Line 1: The original message
Line 2: The corrupted message (should be strictly longer due to an insertion)


---

## How to Run

### Option 1: Run predefined inline tests
In main.py, ensure:  
READ_FROM_TXT = False

Then run:
```bash
python main.py  
```

### Option 2: Run tests from /testcase folder

In main.py, set:  
READ_FROM_TXT = True

Then run:
```bash
python main.py
```
### Option 3: Run randomized experiments
```bash
python experiment.py
```
### Option 4: Add custom test case
```bash
python TestcaseGen.py
```