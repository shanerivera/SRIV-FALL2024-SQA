from myLogger import giveMeLoggingObject

# Get the logger object from myLogger.py
logObj = giveMeLoggingObject()

# Method 1: Using a simple conditional with warning logging
def check_even_or_odd(number):
    if number % 2 != 0:
        logObj.warning(f"{number} is odd")  # Warning log for odd number
        return "odd"
    return "even"

# Method 2: Attempting to access an invalid index with warning logging
def get_string_from_list(strings, index):
    try:
        result = strings[index]
        return result
    except IndexError as e:
        logObj.warning(f"IndexError: {e} - Invalid index {index}")  # Warning log for IndexError
        return None

# Method 3: Dividing by zero and logging warning
def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError as e:
        logObj.warning(f"ZeroDivisionError: {e} - Cannot divide {a} by zero")  # Warning log for division by zero
        return None

# Method 4: Logging if a number is too large (e.g., exceeding a threshold)
def check_large_number(number, threshold=100):
    if number > threshold:
        logObj.warning(f"Warning: {number} exceeds the threshold of {threshold}")  # Warning log for large number
    return number

# Method 5: Attempting to use an unsupported operation
def unsupported_operation():
    try:
        result = "string" + 10  # Trying to add a string and integer
    except TypeError as e:
        logObj.warning(f"TypeError: {e} - Unsupported operation between types")  # Warning log for TypeError
        return None
    return result

# Demonstrating the methods
if __name__ == "__main__":
    # Method 1: Check if number is odd or even
    check_even_or_odd(7)

    # Method 2: Get string from list
    strings = ["apple", "banana", "cherry"]
    get_string_from_list(strings, 5)

    # Method 3: Divide numbers
    divide_numbers(10, 0)

    # Method 4: Check for large number
    check_large_number(150)

    # Method 5: Unsupported operation
    unsupported_operation()
