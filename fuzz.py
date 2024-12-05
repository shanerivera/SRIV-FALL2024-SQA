# Shane Rivera
# Fuzzing 5 Python Methods

import random
import string

# Example of fuzzing the `len()` function
def fuzz_len():
    test_cases = [None, 123, 45.6, {}, [], object(), "valid string", " " * random.randint(1, 100)]
    for case in test_cases:
        try:
            print(f"Testing len({case})")
            print(len(case))
        except Exception as e:
            print(f"Error when calling len() with {case}: {e}")

# Example of fuzzing the `int()` function
def fuzz_int():
    test_cases = ["123", "invalid", "0", "1.2", None, "", object()]
    for case in test_cases:
        try:
            print(f"Testing int({case})")
            print(int(case))
        except Exception as e:
            print(f"Error when calling int() with {case}: {e}")

# Example of fuzzing the `str()` function
def fuzz_str():
    test_cases = [None, 123, 45.6, {}, [], object()]
    for case in test_cases:
        try:
            print(f"Testing str({case})")
            print(str(case))
        except Exception as e:
            print(f"Error when calling str() with {case}: {e}")

# Example of fuzzing the `open()` function
def fuzz_open():
    test_cases = ["testfile.txt", None, 123, "invalid/file/path", object()]
    for case in test_cases:
        try:
            print(f"Testing open({case})")
            with open(case, 'w') as f:
                f.write("Testing")
        except Exception as e:
            print(f"Error when calling open() with {case}: {e}")

# Example of fuzzing the `append()` method for lists
def fuzz_append():
    test_cases = [None, 123, 45.6, {}, [], object(), "random string"]
    for case in test_cases:
        try:
            print(f"Testing append({case}) to empty list")
            lst = []
            lst.append(case)
            print(lst)
        except Exception as e:
            print(f"Error when calling append() with {case}: {e}")

if __name__ == "__main__":
    fuzz_len()
    fuzz_int()
    fuzz_str()
    fuzz_open()
    fuzz_append()
