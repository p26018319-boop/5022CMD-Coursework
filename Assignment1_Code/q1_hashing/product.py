"""
product.py
Entity class for one product sold in the pharmacy.
"""


class Product:
    """A pharmacy product (medicine, supplement, medical supply...)."""

    def __init__(self, product_id, name, category, price, stock):
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Product ID must be a positive whole number")
        if not name.strip():
            raise ValueError("Product name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")
        self.product_id = product_id        # int   : unique key, fast to hash
        self.name = name.strip()            # str   : e.g. "Paracetamol 500mg"
        self.category = category.strip()    # str   : e.g. "Pain Relief"
        self.price = float(price)           # float : price in RM
        self.stock = int(stock)             # int   : whole units in stock

    def __str__(self):
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Category: {self.category} | Price: RM{self.price:.2f} | "
                f"Stock: {self.stock}")
