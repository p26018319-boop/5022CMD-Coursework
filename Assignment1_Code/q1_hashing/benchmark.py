"""
benchmark.py
Experiment for Question 1 #4: search time in a Hash Table vs a 1-D array.

For each data size n we insert n products with the SAME data in both
structures, then search for the same 1,000 randomly chosen IDs in each.
Every measurement is repeated and the average time per search is reported.
"""
import random
import time
from hash_table import HashTable
from product import Product

SIZES = [100, 1_000, 5_000, 10_000]
SEARCHES = 1_000          # lookups per experiment
REPEATS = 5               # repeat experiment, then average
random.seed(42)           # same data every run -> reproducible results


def build(n):
    ids = random.sample(range(1000, 1000 + n * 5), n)    # unique IDs
    products = [Product(i, f"Item {i}", "Test", 1.0, 10) for i in ids]
    table = HashTable(int(n * 1.5) | 1)                  # ~67% load, odd size
    array = []
    for p in products:
        table.insert(p.product_id, p)
        array.append(p)
    return table, array, ids


def array_search(array, pid):
    for p in array:
        if p.product_id == pid:
            return p
    return None


def time_it(fn):
    t0 = time.perf_counter_ns()
    fn()
    return time.perf_counter_ns() - t0


def main():
    print(f"{'n':>7} | {'Hash avg (ns)':>14} | {'Array avg (ns)':>15} | "
          f"{'Speed-up':>9}")
    print("-" * 56)
    for n in SIZES:
        table, array, ids = build(n)
        targets = random.choices(ids, k=SEARCHES)
        h_total = a_total = 0
        for _ in range(REPEATS):
            h_total += time_it(lambda: [table.search(t) for t in targets])
            a_total += time_it(lambda: [array_search(array, t) for t in targets])
        h_avg = h_total / (REPEATS * SEARCHES)
        a_avg = a_total / (REPEATS * SEARCHES)
        print(f"{n:>7} | {h_avg:>14,.0f} | {a_avg:>15,.0f} | {a_avg / h_avg:>8.1f}x")


if __name__ == "__main__":
    main()
