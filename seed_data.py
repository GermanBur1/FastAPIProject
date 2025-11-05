from app.models.schemas import CarSale, CarSaleCreate
from app.models.binary_tree import BinarySearchTree
from datetime import datetime, timedelta
import random

def generate_sample_cars():
    """Genera 10 autos de ejemplo para la venta"""
    # Lista de marcas y colores disponibles
    brands = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", 
              "Volkswagen", "Hyundai", "Kia", "Mazda", "Subaru"]
    
    colors = ["red", "blue", "green", "black", "white", "silver", "gray"]
    
    # Generar 10 autos de ejemplo
    sample_cars = []
    for i in range(1, 11):
        # Generar placa aleatoria (ejemplo: ABC123, XYZ789)
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        numbers = ''.join(random.choices('0123456789', k=3))
        license_plate = f"{letters}{numbers}"
        
        # Crear datos del auto
        car_data = {
            "license_plate": license_plate,
            "brand": random.choice(brands),
            "color": random.choice(colors),
            "price": round(random.uniform(10000, 50000), 2),
            "sale_date": datetime.now() - timedelta(days=random.randint(0, 365))
        }
        
        # Crear instancia de CarSaleCreate (sin ID)
        car = CarSaleCreate(**car_data)
        sample_cars.append(car)
    
    return sample_cars

def seed_database():
    """Agrega los autos de ejemplo al árbol"""
    tree = BinarySearchTree()
    sample_cars = generate_sample_cars()
    
    print("Agregando autos de ejemplo...")
    for i, car in enumerate(sample_cars, 1):
        # Insertar el auto en el árbol
        result = tree.insert(car)
        print(f"{i}. {result.brand} {result.license_plate} - ${result.price:,.2f} - {result.color}")
    
    # Guardar los cambios en el CSV
    tree.save_tree()
    print("\n¡Datos de ejemplo agregados exitosamente!")
    print(f"Total de autos en el árbol: {tree.get_tree_stats().total_nodes}")

if __name__ == "__main__":
    seed_database()
