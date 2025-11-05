from typing import Optional, List, Dict, Any, Tuple
from ..models.schemas import CarSale, TreeStats
import csv
import os
from datetime import datetime

class TreeNode:
    def __init__(self, data: CarSale):
        self.data = data
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

class BinarySearchTree:
    def __init__(self):
        self.root: Optional[TreeNode] = None
        self._next_id = 1
        self.csv_file = "car_sales.csv"
        self._ensure_csv_headers()
        self._load_from_csv()

    def _ensure_csv_headers(self):
        """Ensure CSV file exists with proper headers"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'id', 'license_plate', 'brand', 'color', 'price', 'sale_date'
                ])
                writer.writeheader()

    def _load_from_csv(self):
        """Load data from CSV into the tree"""
        if not os.path.exists(self.csv_file):
            return
            
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['id']:  # Skip empty rows
                    continue
                    
                car_sale = CarSale(
                    id=int(row['id']),
                    license_plate=row['license_plate'],
                    brand=row['brand'],
                    color=row['color'],
                    price=float(row['price']),
                    sale_date=datetime.fromisoformat(row['sale_date'])
                )
                self.insert(car_sale)
                self._next_id = max(self._next_id, car_sale.id + 1)

    def _save_to_csv(self, node: Optional[TreeNode]):
        """Save tree data to CSV (in-order traversal)"""
        if node is None:
            return []
        
        left_data = self._save_to_csv(node.left)
        current_data = [{
            'id': str(node.data.id),
            'license_plate': node.data.license_plate,
            'brand': node.data.brand,
            'color': node.data.color,
            'price': str(node.data.price),
            'sale_date': node.data.sale_date.isoformat()
        }]
        right_data = self._save_to_csv(node.right)
        
        return left_data + current_data + right_data

    def save_tree(self):
        """Save the entire tree to CSV"""
        if not self.root:
            return
            
        data = self._save_to_csv(self.root)
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'license_plate', 'brand', 'color', 'price', 'sale_date'
            ])
            writer.writeheader()
            writer.writerows(data)

    def insert(self, data) -> CarSale:
        """Insert a new node into the tree"""
        # Convertir a diccionario si es un modelo Pydantic
        if hasattr(data, 'dict'):
            data_dict = data.dict()
            # Si es un CarSaleCreate, asignar un ID
            if not data_dict.get('id'):
                data_dict['id'] = self._next_id
                self._next_id += 1
            # Crear un objeto CarSale con los datos
            from .schemas import CarSale
            data = CarSale(**data_dict)
            
        # Si el árbol está vacío, crear el nodo raíz
        if not self.root:
            self.root = TreeNode(data)
            self.save_tree()
            return data
            
        # Si el árbol no está vacío, buscar la posición correcta
        current = self.root
        while current:
            if data.license_plate < current.data.license_plate:
                if current.left is None:
                    current.left = TreeNode(data)
                    self.save_tree()
                    return data
                current = current.left
            elif data.license_plate > current.data.license_plate:
                if current.right is None:
                    current.right = TreeNode(data)
                    self.save_tree()
                    return data
                current = current.right
            else:
                # Actualizar nodo existente
                current.data = data
                self.save_tree()
                return data

    def find(self, license_plate: str) -> Optional[CarSale]:
        """Find a node by license plate"""
        current = self.root
        while current:
            if license_plate < current.data.license_plate:
                current = current.left
            elif license_plate > current.data.license_plate:
                current = current.right
            else:
                return current.data
        return None

    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find the node with minimum value in a subtree"""
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, license_plate: str) -> bool:
        """Delete a node by license plate"""
        def _delete(node: Optional[TreeNode], key: str) -> Optional[TreeNode]:
            if not node:
                return None
                
            if key < node.data.license_plate:
                node.left = _delete(node.left, key)
            elif key > node.data.license_plate:
                node.right = _delete(node.right, key)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                    
                temp = self._find_min(node.right)
                node.data = temp.data
                node.right = _delete(node.right, temp.data.license_plate)
                
            return node
            
        self.root = _delete(self.root, license_plate)
        self.save_tree()
        return self.root is not None

    def update(self, license_plate: str, update_data: dict) -> Optional[CarSale]:
        """Update a node's data"""
        node = self.root
        while node:
            if license_plate < node.data.license_plate:
                node = node.left
            elif license_plate > node.data.license_plate:
                node = node.right
            else:
                for key, value in update_data.items():
                    if value is not None and hasattr(node.data, key):
                        setattr(node.data, key, value)
                self.save_tree()
                return node.data
        return None

    def in_order_traversal(self) -> List[CarSale]:
        """Return nodes in in-order (left, root, right)"""
        result = []
        def _in_order(node):
            if node:
                _in_order(node.left)
                result.append(node.data)
                _in_order(node.right)
        _in_order(self.root)
        return result

    def pre_order_traversal(self) -> List[CarSale]:
        """Return nodes in pre-order (root, left, right)"""
        result = []
        def _pre_order(node):
            if node:
                result.append(node.data)
                _pre_order(node.left)
                _pre_order(node.right)
        _pre_order(self.root)
        return result

    def post_order_traversal(self) -> List[CarSale]:
        """Return nodes in post-order (left, right, root)"""
        result = []
        def _post_order(node):
            if node:
                _post_order(node.left)
                _post_order(node.right)
                result.append(node.data)
        _post_order(self.root)
        return result

    def get_tree_stats(self) -> TreeStats:
        """Get statistics about the tree"""
        def _height(node):
            if not node:
                return 0
            return 1 + max(_height(node.left), _height(node.right))
            
        def _count_nodes(node):
            if not node:
                return 0
            return 1 + _count_nodes(node.left) + _count_nodes(node.right)
            
        def _count_leaves(node):
            if not node:
                return 0
            if not node.left and not node.right:
                return 1
            return _count_leaves(node.left) + _count_leaves(node.right)
            
        def _nodes_per_level(node, level, level_dict):
            if not node:
                return
                
            if level in level_dict:
                level_dict[level] += 1
            else:
                level_dict[level] = 1
                
            _nodes_per_level(node.left, level + 1, level_dict)
            _nodes_per_level(node.right, level + 1, level_dict)
        
        level_dict = {}
        _nodes_per_level(self.root, 0, level_dict)
        
        return TreeStats(
            height=_height(self.root),
            total_nodes=_count_nodes(self.root),
            leaf_count=_count_leaves(self.root),
            nodes_per_level=level_dict
        )

    def find_path(self, start_plate: str, end_plate: str) -> Optional[List[CarSale]]:
        """Find the path between two nodes"""
        def _find_lca(node, p, q):
            if not node:
                return None
                
            if node.data.license_plate == p or node.data.license_plate == q:
                return node
                
            left = _find_lca(node.left, p, q)
            right = _find_lca(node.right, p, q)
            
            if left and right:
                return node
                
            return left if left else right
            
        def _get_path(root, path, k):
            if not root:
                return False
                
            path.append(root.data)
            
            if root.data.license_plate == k:
                return True
                
            if (_get_path(root.left, path, k) or 
                _get_path(root.right, path, k)):
                return True
                
            path.pop()
            return False
            
        lca = _find_lca(self.root, start_plate, end_plate)
        if not lca:
            return None
            
        path1 = []
        path2 = []
        
        _get_path(lca, path1, start_plate)
        _get_path(lca, path2, end_plate)
        
        path2 = path2[1:]  # Remove the LCA from the second path
        path2.reverse()
        
        return path1 + path2

    def find_longest_path(self) -> List[CarSale]:
        """Find the longest path between any two leaf nodes"""
        def _longest_path(node):
            if not node:
                return 0, []
                
            left_height, left_path = _longest_path(node.left)
            right_height, right_path = _longest_path(node.right)
            
            if left_height > right_height:
                return left_height + 1, [node.data] + left_path
            else:
                return right_height + 1, [node.data] + right_path
                
        if not self.root:
            return []
            
        _, left_path = _longest_path(self.root.left)
        _, right_path = _longest_path(self.root.right)
        
        left_path = left_path[::-1]  # Reverse to get path from leaf to root
        right_path = right_path  # Already from root to leaf
        
        return left_path + [self.root.data] + right_path
