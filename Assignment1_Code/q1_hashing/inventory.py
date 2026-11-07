"""
inventory.py
Command-line Pharmacy Inventory System (Question 1).

Run:  python inventory.py
Features: insert, search (with hash-vs-array timing), edit, delete, list.
"""
import time
from hash_table import HashTable
from product import Product
from sample_data import SAMPLE_PRODUCTS

TABLE_SIZE = 53          # prime number > number of records -> fewer collisions


class PharmacyInventory:
    """Stores products in a HashTable and, for comparison, in a plain list."""

    def __init__(self, capacity=TABLE_SIZE):
        self.table = HashTable(capacity)
        self.array = []                       # one-dimensional array (list)

    def add(self, product):
        """Insert into both structures. Returns the hash-table slot index."""
        if self.table.search(product.product_id) is not None:
            raise ValueError(f"Product ID {product.product_id} already exists")
        slot = self.table.insert(product.product_id, product)
        self.array.append(product)
        return slot

    def search_hash(self, product_id):
        return self.table.search(product_id)

    def search_array(self, product_id):
        """Linear search through the array."""
        for p in self.array:
            if p.product_id == product_id:
                return p
        return None

    def update(self, product_id, name=None, category=None, price=None, stock=None):
        p = self.table.search(product_id)    # same object is shared by the array
        if p is None:
            return False
        if name:
            p.name = name
        if category:
            p.category = category
        if price is not None:
            p.price = float(price)
        if stock is not None:
            p.stock = int(stock)
        return True

    def remove(self, product_id):
        p = self.table.search(product_id)
        if p is None:
            return False
        self.table.delete(product_id)
        self.array.remove(p)
        return True


# ------------------------------------------------------------------ input helpers
def read_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"  Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


def read_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("  Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("  Invalid input. Please enter a number.")


# ------------------------------------------------------------------ menu actions
def insert_product(inv):
    pid = read_int("Enter Product ID: ", 1)
    if inv.search_hash(pid) is not None:
        print(f"Product ID {pid} already exists.")
        return
    name = input("Enter Product Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    category = input("Enter Category: ").strip() or "General"
    price = read_float("Enter Price: ")
    stock = read_int("Enter Stock Quantity: ", 0)
    try:
        slot = inv.add(Product(pid, name, category, price, stock))
        print(f"Product inserted successfully into slot [{slot}]")
    except OverflowError:
        print("Inventory is full - cannot insert more products.")


def search_product(inv):
    pid = read_int("Enter Product ID to search: ", 1)

    t0 = time.perf_counter_ns()
    found = inv.search_hash(pid)
    t_hash = time.perf_counter_ns() - t0

    t0 = time.perf_counter_ns()
    inv.search_array(pid)
    t_arr = time.perf_counter_ns() - t0

    if found is None:
        print("Product Not Found.")
    else:
        print("Product Found!")
        print(found)
    print(f"Search completed in {t_hash / 1e9:.6f} seconds (Hash Table)")
    print(f"Search completed in {t_arr / 1e9:.6f} seconds (Array - same record)")


def edit_product(inv):
    pid = read_int("Enter Product ID to edit: ", 1)
    p = inv.search_hash(pid)
    if p is None:
        print("Product Not Found.")
        return
    print("Current record:", p)
    print("(Press Enter to keep the current value)")
    name = input("New name: ").strip() or None
    category = input("New category: ").strip() or None
    price_s = input("New price: ").strip()
    stock_s = input("New stock: ").strip()
    try:
        price = float(price_s) if price_s else None
        stock = int(stock_s) if stock_s else None
        if (price is not None and price < 0) or (stock is not None and stock < 0):
            print("Price and stock cannot be negative. No changes made.")
            return
    except ValueError:
        print("Invalid number entered. No changes made.")
        return
    inv.update(pid, name, category, price, stock)
    print("Product updated:", inv.search_hash(pid))


def delete_product(inv):
    pid = read_int("Enter Product ID to delete: ", 1)
    print("Product deleted." if inv.remove(pid) else "Product Not Found.")


def list_products(inv):
    print(f"{'Slot':<5}| ID    | Name")
    for idx, slot in enumerate(inv.table.slots):
        if slot.state == 1:
            print(f"[{idx:>2}] | {slot.key:<5} | {slot.value.name}")
    print(f"Items: {len(inv.table)}/{inv.table.capacity} "
          f"(load factor {inv.table.load_factor():.2f})")


def main():
    inv = PharmacyInventory()
    for p in SAMPLE_PRODUCTS:
        inv.add(p)

    actions = {"1": insert_product, "2": search_product, "3": edit_product,
               "4": delete_product, "5": list_products}
    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. List All Products")
        print("6. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "6":
            print("Exiting Inventory System. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(inv)
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
