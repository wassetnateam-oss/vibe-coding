"""
Simple CLI Calculator in Python (Standard Library only).
Supports basic operations, power, modulo, and chained calculations with error handling.
"""

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def power(a: float, b: float) -> float:
    return a ** b

def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot calculate modulo by zero.")
    return a % b

OPERATIONS = {
    "+": ("Add", add),
    "-": ("Subtract", subtract),
    "*": ("Multiply", multiply),
    "/": ("Divide", divide),
    "^": ("Power", power),
    "%": ("Modulo", modulo),
}

def get_number(prompt: str) -> float:
    while True:
        user_input = input(prompt).strip()
        try:
            return float(user_input)
        except ValueError:
            print("Invalid number. Please enter a valid numerical value.")

def display_menu():
    print("\n--- Available Operations ---")
    for symbol, (name, _) in OPERATIONS.items():
        print(f"  {symbol} : {name}")
    print("  c : Clear current result")
    print("  q : Quit")
    print("----------------------------")

def main():
    print("=" * 40)
    print("       Welcome to Simple Calculator       ")
    print("=" * 40)
    
    current_value = None

    while True:
        if current_value is None:
            current_value = get_number("Enter the first number: ")

        print(f"\nCurrent value: {current_value}")
        display_menu()
        
        choice = input("Choose an operator or action (+, -, *, /, ^, %, c, q): ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == 'c':
            current_value = None
            print("Calculator reset.")
            continue
        elif choice not in OPERATIONS:
            print("Invalid option. Please choose a valid operator.")
            continue

        op_name, op_func = OPERATIONS[choice]
        next_number = get_number(f"Enter the next number to {op_name.lower()}: ")

        try:
            result = op_func(current_value, next_number)
            # Format integer outputs cleanly (e.g. 4.0 -> 4)
            formatted_result = int(result) if result.is_integer() else result
            print(f"\nResult: {current_value} {choice} {next_number} = {formatted_result}")
            current_value = formatted_result
        except ZeroDivisionError as err:
            print(f"Error: {err}")
        except OverflowError:
            print("Error: Calculation resulted in an overflow (number too large).")

if __name__ == "__main__":
    main()

