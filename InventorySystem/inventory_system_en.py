# Inventory Management System
# A simple script to manage product inventory
# Version: 1.0
# Date: May 2025

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def update_quantity(self, new_quantity):
        if new_quantity >= 0:
            self.quantity = new_quantity
            return True
        else:
            print("Error: Quantity cannot be negative.")
            return False
    
    def update_price(self, new_price):
        if new_price > 0:
            self.price = new_price
            return True
        return False      

    def get_value(self):
        return self.price * self.quantity


class Inventory:
    def __init__(self):
        self.products = {}
        self.log = []
    
    def add_product(self, product):
        if product.product_id in self.products:
            print(f"Product with ID {product.product_id} already exists.")
            return False
        
        self.products[product.product_id] = product
        self.log.append(f"Added product: {product.name}")
        return True
    
    def remove_product(self, product_id):
        if product_id in self.products:
            product = self.products.pop(product_id)
            self.log.append(f"Removed product: {product.name}")
            return True
        else:
            print(f"Error: Product with ID {product_id} not found.")
            return False
    
    def get_product(self, product_id):
        if product_id in self.products:
            return self.products[product_id]
        else:
            print(f"Error: Product with ID {product_id} not found.")
            return None
    
    def list_products(self):
        for product_id, product in self.products.items():
            print(f"ID: {product_id}, Name: {product.name}, Price: {product.price}, Quantity: {product.quantity}")
    
    def total_inventory_value(self):
        total = 0
        for product in self.products.values():
            total += product.get_value()
        return total
    
    def search_products(self, keyword):
        results = []
        for product in self.products.values():
            if keyword.lower() in product.name.lower():
                results.append(product)
        return results
    
    def low_stock_alert(self, threshold=5):
        low_stock = []
        for product in self.products:
            if product.quantity <= threshold:
                low_stock.append(product)
        return low_stock


# Example usage
def main():
    inventory = Inventory()
    
    # Add some products
    p1 = Product(1, "Laptop", 999.99, 10)
    p2 = Product(2, "Mouse", 24.99, 50)
    p3 = Product(3, "Keyboard", 59.99, 30)
    
    inventory.add_product(p1)
    inventory.add_product(p2)
    inventory.add_product(p3)
    
    # Update product quantity
    p1.update_quantity(5)
   

    # Search for products
    search_results = inventory.search_products("key")
    for product in search_results:
        print(f"Found: {product.name}")
    
    # Calculate total value
    total_value = inventory.total_inventory_value()
    print(f"Total inventory value: ${total_value}")
    
    # Get low stock products
    low_stock = inventory.low_stock_alert()
    if low_stock:
        for product in low_stock:
            print(f"Low stock alert: {product.name} - only {product.quantity} left.")
    
   

if __name__ == "__main__":
    main()
