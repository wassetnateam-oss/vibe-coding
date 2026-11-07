"""
Scientific / Expression-based CLI Calculator using only Python's standard library.
Features:
- Math expression evaluation (e.g., 2 + 3 * (4 - 1))
- Built-in math constants (pi, e)
- Standard math functions (sqrt, sin, cos, tan, log, exp, abs, round)
- Calculation history tracking
- Interactive REPL interface
"""

import math

# Available math functions and constants safely mapped
SAFE_ENV = {
    # Functions
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "factorial": math.factorial,
    # Constants
    "pi": math.pi,
    "e": math.e,
}

HELP_TEXT = """
Available Features:
  Basic Operators: +, -, *, /, // (floor div), % (modulo), ** or ^ (power)
  Grouping:        ( ... )
  Constants:       pi, e
  Functions:       sqrt(x), sin(x), cos(x), tan(x), log(x), log10(x)
                   exp(x), abs(x), round(x, n), floor(x), ceil(x), factorial(n)
  
Special Commands:
  ans              Reuse the result from the previous calculation
  history          View past calculations
  help             Show this help screen
  clear            Reset calculation history
  exit / quit      Exit the calculator
"""

def evaluate_expression(expr: str, last_ans: float | None) -> float:
    # Normalize power operator
    processed = expr.replace("^", "**")

    local_vars = dict(SAFE_ENV)
    if last_ans is not None:
        local_vars["ans"] = last_ans

    # Safe evaluation without Python built-ins
    return eval(processed, {"__builtins__": None}, local_vars)

def main():
    print("=" * 55)
    print("      Python Expression Calculator (Standard Library)")
    print("=" * 55)
    print("Type 'help' for instructions or 'quit' to exit.")
    
    history: list[str] = []
    last_ans: float | None = None

    while True:
        try:
            user_input = input("\ncalc > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting calculator.")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        if cmd == "help":
            print(HELP_TEXT)
            continue

        if cmd == "history":
            if not history:
                print("No calculations in history yet.")
            else:
                print("\n--- Calculation History ---")
                for idx, item in enumerate(history[-10:], start=1):
                    print(f"  {idx}. {item}")
            continue

        if cmd == "clear":
            history.clear()
            last_ans = None
            print("History cleared and 'ans' reset.")
            continue

        try:
            result = evaluate_expression(user_input, last_ans)
            
            # Format clean integer display if whole number
            if isinstance(result, float) and result.is_integer():
                formatted_result = int(result)
            elif isinstance(result, float):
                formatted_result = round(result, 8)
            else:
                formatted_result = result

            last_ans = result
            record = f"{user_input} = {formatted_result}"
            history.append(record)
            print(f"=> {formatted_result}")

        except ZeroDivisionError:
            print("Math Error: Division by zero is not allowed.")
        except ValueError as e:
            print(f"Math Error: {e}")
        except NameError as e:
            print(f"Syntax Error: Unrecognized name or function ({e}). Type 'help' for valid names.")
        except TypeError as e:
            print(f"Type Error: {e}")
        except SyntaxError:
            print("Syntax Error: Invalid mathematical expression.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

