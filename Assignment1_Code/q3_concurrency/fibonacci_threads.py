"""
fibonacci_threads.py
Question 3: Fibonacci with and without multithreading.

Usage:
    python fibonacci_threads.py              # 10 rounds, Fib(35), Fib(38), Fib(40)
    python fibonacci_threads.py --rounds 3   # fewer rounds for a quick test
"""
import argparse
import sys
import threading
import time

NUMBERS = (35, 38, 40)
ROUNDS = 10


def fibonacci(n):
    """Return the n-th Fibonacci number (naive recursion).

    fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)
    Time complexity: O(2^n)  (derivation is in the report).
    """
    if n <= 1:                                   # base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)   # two recursive calls


# ------------------------------------------------------------ multithreaded
def _worker(n, results, index, starts, ends):
    """Thread body: compute fib(n) and record this thread's own start/end time."""
    starts[index] = time.perf_counter_ns()
    results[index] = fibonacci(n)
    ends[index] = time.perf_counter_ns()


def run_multithreaded(numbers):
    """One thread per number.

    T = (end time of the thread that finished LAST)
        - (start time of the thread that started FIRST)
    Returns (results, T in ns).
    """
    count = len(numbers)
    results = [None] * count
    starts = [0] * count
    ends = [0] * count
    threads = [threading.Thread(target=_worker,
                                args=(n, results, i, starts, ends))
               for i, n in enumerate(numbers)]
    for t in threads:          # start all three threads
        t.start()
    for t in threads:          # wait for all three to finish
        t.join()
    return results, max(ends) - min(starts)


# ----------------------------------------------------------- single-threaded
def run_sequential(numbers):
    """Same work, one after another in the main thread. Returns (results, T)."""
    start = time.perf_counter_ns()
    results = [fibonacci(n) for n in numbers]
    end = time.perf_counter_ns()
    return results, end - start


# ------------------------------------------------------------------ reporting
def run_experiment(title, runner, rounds):
    print(f"\n=== Fibonacci Computation ({title}) ===")
    times = []
    for r in range(1, rounds + 1):
        results, elapsed = runner(NUMBERS)
        times.append(elapsed)
        values = ", ".join(f"Fib({n})={v}" for n, v in zip(NUMBERS, results))
        print(f"Round {r:>2}: {values} | T = {elapsed:,} ns")
    average = sum(times) // len(times)
    print(f"Average T ({title}): {average:,} ns  ({average / 1e9:.3f} s)")
    return average


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    args = parser.parse_args()

    gil = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {sys.version.split()[0]} | GIL enabled: {gil}")

    avg_mt = run_experiment("With Multithreading", run_multithreaded, args.rounds)
    avg_seq = run_experiment("Without Multithreading", run_sequential, args.rounds)

    change = (avg_seq - avg_mt) / avg_seq * 100
    print()
    if change >= 0:
        print(f"Observation: Multithreading reduced the average completion "
              f"time by approximately {change:.1f}%.")
    else:
        print(f"Observation: Multithreading INCREASED the average completion "
              f"time by approximately {-change:.1f}%.")


if __name__ == "__main__":
    main()
