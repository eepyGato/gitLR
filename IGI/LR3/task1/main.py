"""
Module: main.py
Purpose: Main program with generator-based initialization.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

from series_core import compute_series, math_value, MaxIterError
from input_handlers import manual_sequence, arithmetic_progression_generator, get_epsilon, get_max_iterations

def log_call(func):
    def wrapper(x, eps, max_iter):
        print(f"[LOG] Calling {func.__name__}(x={x}, eps={eps}, max_iter={max_iter})")
        return func(x, eps, max_iter)
    return wrapper

compute_series = log_call(compute_series)

def print_table(results, eps):
    print("\n" + "=" * 90)
    print(f"{'x':>12} {'n':>8} {'F(x) (series)':>25} {'Math F(x)':>25} {'eps':>15}")
    print("-" * 90)
    for x, n, f_series, f_math in results:
        print(f"{x:12.6f} {n:8d} {f_series:25.12f} {f_math:25.12f} {eps:15.2e}")
    print("=" * 90)

def main():
    print("*** Series expansion of ln((x+1)/(x-1)) ***\n")
    while True:
        print("Choose input method:")
        print("1 - Manual entry (list)")
        print("2 - Generator (arithmetic progression, yields one by one)")
        choice = input("Your choice (1/2): ").strip()
        
        if choice == '2':
            gen = arithmetic_progression_generator()
            x_list = list(gen)   # consume generator into list
        else:
            x_list = manual_sequence()
        
        eps = get_epsilon()
        max_iter = get_max_iterations()
        
        results = []
        for x in x_list:
            try:
                f_series, n_used = compute_series(x, eps, max_iter)
                f_math = math_value(x)
                results.append((x, n_used, f_series, f_math))
            except (ValueError, MaxIterError, ZeroDivisionError, OverflowError) as e:
                print(f"Skipping x={x}: {e}")
            except Exception as e:
                print(f"Skipping x={x}: unexpected {e}")
        
        if results:
            print_table(results, eps)
        else:
            print("No valid results.")
        
        again = input("\nRun again? (y/n): ").lower()
        if again != 'y':
            break
    print("Goodbye!")

if __name__ == "__main__":
    main()