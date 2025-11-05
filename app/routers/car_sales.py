from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from ..models.schemas import CarSale, CarSaleCreate, CarSaleUpdate, TreeStats
from ..controllers.car_sales_controller import CarSalesController

router = APIRouter(
    prefix="/api/car-sales",
    tags=["car-sales"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CarSale, status_code=201)
async def create_car_sale(car_sale: CarSaleCreate):
    """Create a new car sale"""
    return CarSalesController.create_car_sale(car_sale)

@router.get("/{license_plate}", response_model=CarSale)
async def get_car_sale(license_plate: str = Path(..., min_length=6, max_length=10)):
    """Get a car sale by license plate"""
    return CarSalesController.get_car_sale(license_plate)

@router.put("/{license_plate}", response_model=CarSale)
async def update_car_sale(
    license_plate: str = Path(..., min_length=6, max_length=10),
    update_data: CarSaleUpdate = ...
):
    """Update a car sale"""
    return CarSalesController.update_car_sale(license_plate, update_data)

@router.delete("/{license_plate}", status_code=204)
async def delete_car_sale(license_plate: str = Path(..., min_length=6, max_length=10)):
    """Delete a car sale"""
    CarSalesController.delete_car_sale(license_plate)
    return None

@router.get("/traversal/{order}", response_model=List[CarSale])
async def get_tree_traversal(
    order: str = Path(..., regex="^(inorder|preorder|postorder)$")
):
    """
    Get tree traversal
    - **order**: Traversal order (inorder, preorder, postorder)
    """
    return CarSalesController.get_tree_traversal(order)

@router.get("/stats/", response_model=TreeStats)
async def get_tree_statistics():
    """Get tree statistics"""
    return CarSalesController.get_tree_statistics()

@router.get("/path/{start_plate}/{end_plate}", response_model=List[CarSale])
async def get_path_between_nodes(
    start_plate: str = Path(..., min_length=6, max_length=10),
    end_plate: str = Path(..., min_length=6, max_length=10)
):
    """
    Get the path between two nodes
    - **start_plate**: Starting node license plate
    - **end_plate**: Ending node license plate
    """
    return CarSalesController.get_path_between_nodes(start_plate, end_plate)

@router.get("/longest-path/", response_model=List[CarSale])
async def get_longest_path():
    """Get the longest path in the tree"""
    return CarSalesController.get_longest_path()
