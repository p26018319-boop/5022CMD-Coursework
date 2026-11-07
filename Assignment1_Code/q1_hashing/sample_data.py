"""sample_data.py - pre-defined pharmacy records loaded at start-up."""
from product import Product

SAMPLE_PRODUCTS = [
    Product(1042, "Paracetamol 500mg", "Pain Relief", 5.90, 120),
    Product(1043, "Ibuprofen 400mg", "Pain Relief", 8.50, 80),
    Product(1101, "Amoxicillin 250mg", "Antibiotic", 12.30, 45),
    Product(1102, "Cetirizine 10mg", "Allergy", 7.20, 95),
    Product(1150, "Loratadine 10mg", "Allergy", 9.60, 60),
    Product(1201, "Omeprazole 20mg", "Gastric", 14.80, 70),
    Product(1202, "Antacid Tablets", "Gastric", 4.50, 150),
    Product(1250, "Vitamin C 1000mg", "Supplement", 22.00, 200),
    Product(1251, "Vitamin D3 1000IU", "Supplement", 28.50, 90),
    Product(1300, "Cough Syrup 100ml", "Cough & Cold", 11.40, 55),
    Product(1301, "Throat Lozenges", "Cough & Cold", 6.80, 130),
    Product(1400, "Digital Thermometer", "Medical Supply", 19.90, 35),
    Product(1401, "Adhesive Bandages (50s)", "Medical Supply", 8.90, 110),
    Product(1500, "Hand Sanitiser 250ml", "Hygiene", 9.90, 140),
    Product(1501, "Face Masks (50s)", "Hygiene", 15.00, 180),
]
