from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from ..models.schemas import CarSale, CarSaleCreate, CarSaleUpdate, TreeStats
from ..models.binary_tree import BinarySearchTree

# Initialize the binary search tree
car_sales_tree = BinarySearchTree()

class CarSalesController:
    @staticmethod
    def create_car_sale(car_sale: CarSaleCreate) -> CarSale:
        """Create a new car sale"""
        # Convert CarSaleCreate to CarSale (ID will be assigned in the tree)
        new_sale = CarSale(
            id=0,  # Will be set by the tree
            license_plate=car_sale.license_plate,
            brand=car_sale.brand,
            color=car_sale.color,
            price=car_sale.price,
            sale_date=car_sale.sale_date
        )
        
        # Insert into the tree
        result = car_sales_tree.insert(new_sale)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to create car sale")
            
        return result

    @staticmethod
    def get_car_sale(license_plate: str) -> CarSale:
        """Get a car sale by license plate"""
        sale = car_sales_tree.find(license_plate)
        if not sale:
            raise HTTPException(status_code=404, detail="Car sale not found")
        return sale

    @staticmethod
    def update_car_sale(license_plate: str, update_data: CarSaleUpdate) -> CarSale:
        """Update a car sale"""
        # Get the existing sale to ensure it exists
        existing = car_sales_tree.find(license_plate)
        if not existing:
            raise HTTPException(status_code=404, detail="Car sale not found")
            
        # Convert update data to dict and remove None values
        update_dict = update_data.dict(exclude_unset=True)
        
        # Update the sale
        updated = car_sales_tree.update(license_plate, update_dict)
        if not updated:
            raise HTTPException(status_code=400, detail="Failed to update car sale")
            
        return updated

    @staticmethod
    def delete_car_sale(license_plate: str) -> bool:
        """Delete a car sale"""
        if not car_sales_tree.delete(license_plate):
            raise HTTPException(status_code=404, detail="Car sale not found")
        return True

    @staticmethod
    def get_tree_traversal(order: str) -> List[CarSale]:
        """Get tree traversal in the specified order"""
        if order == "inorder":
            return car_sales_tree.in_order_traversal()
        elif order == "preorder":
            return car_sales_tree.pre_order_traversal()
        elif order == "postorder":
            return car_sales_tree.post_order_traversal()
        else:
            raise HTTPException(status_code=400, detail="Invalid traversal order")

    @staticmethod
    def get_tree_statistics() -> TreeStats:
        """Get tree statistics"""
        return car_sales_tree.get_tree_stats()

    @staticmethod
    def get_path_between_nodes(start_plate: str, end_plate: str) -> List[CarSale]:
        """Get the path between two nodes"""
        path = car_sales_tree.find_path(start_plate, end_plate)
        if not path:
            raise HTTPException(status_code=404, detail="One or both nodes not found")
        return path

    @staticmethod
    def get_longest_path() -> List[CarSale]:
        """Get the longest path in the tree"""
        path = car_sales_tree.find_longest_path()
        if not path:
            raise HTTPException(status_code=404, detail="Tree is empty")
        return path
