import sqlite3
from typing import List, Optional, Tuple


class ProductDB:
    def __init__(self, db_name: str = "MyProduct.db") -> None:
        self.db_name = db_name

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY,
            productName TEXT NOT NULL,
            productPrice INTEGER NOT NULL
        )
        """
        with self._connect() as conn:
            conn.execute(query)
            conn.commit()

    def insert_product(self, product_id: int, product_name: str, product_price: int) -> None:
        query = """
        INSERT INTO Products (productID, productName, productPrice)
        VALUES (?, ?, ?)
        ON CONFLICT(productID) DO UPDATE SET
            productName = excluded.productName,
            productPrice = excluded.productPrice
        """
        with self._connect() as conn:
            conn.execute(query, (product_id, product_name, product_price))
            conn.commit()

    def insert_many_products(self, products: List[Tuple[int, str, int]]) -> None:
        query = """
        INSERT INTO Products (productID, productName, productPrice)
        VALUES (?, ?, ?)
        ON CONFLICT(productID) DO UPDATE SET
            productName = excluded.productName,
            productPrice = excluded.productPrice
        """
        with self._connect() as conn:
            conn.executemany(query, products)
            conn.commit()

    def update_product(self, product_id: int, new_name: str, new_price: int) -> int:
        query = """
        UPDATE Products
        SET productName = ?, productPrice = ?
        WHERE productID = ?
        """
        with self._connect() as conn:
            cursor = conn.execute(query, (new_name, new_price, product_id))
            conn.commit()
            return cursor.rowcount

    def delete_product(self, product_id: int) -> int:
        query = "DELETE FROM Products WHERE productID = ?"
        with self._connect() as conn:
            cursor = conn.execute(query, (product_id,))
            conn.commit()
            return cursor.rowcount

    def select_product_by_id(self, product_id: int) -> Optional[Tuple[int, str, int]]:
        query = "SELECT productID, productName, productPrice FROM Products WHERE productID = ?"
        with self._connect() as conn:
            cursor = conn.execute(query, (product_id,))
            return cursor.fetchone()

    def select_all_products(self) -> List[Tuple[int, str, int]]:
        query = "SELECT productID, productName, productPrice FROM Products ORDER BY productID"
        with self._connect() as conn:
            cursor = conn.execute(query)
            return cursor.fetchall()

    def count_products(self) -> int:
        query = "SELECT COUNT(*) FROM Products"
        with self._connect() as conn:
            cursor = conn.execute(query)
            return cursor.fetchone()[0]

    def prepare_sample_products(self, count: int = 1000) -> List[Tuple[int, str, int]]:
        products = []
        for i in range(1, count + 1):
            name = f"Electronics-{i:04d}"
            price = 10000 + (i * 137)
            products.append((i, name, price))
        return products


if __name__ == "__main__":
    db = ProductDB("MyProduct.db")
    db.create_table()

    if db.count_products() == 0:
        sample_data = db.prepare_sample_products(1000)
        db.insert_many_products(sample_data)
        print("Inserted 1000 sample products.")
    else:
        print("Products table already has data. Skip sample insert.")

    # CRUD examples
    db.insert_product(2001, "Electronics-2001", 555000)
    updated_rows = db.update_product(1, "Electronics-0001-Updated", 99999)
    deleted_rows = db.delete_product(2)
    selected_one = db.select_product_by_id(1)
    selected_all_count = db.count_products()

    print("Updated rows:", updated_rows)
    print("Deleted rows:", deleted_rows)
    print("Selected product (ID=1):", selected_one)
    print("Total products:", selected_all_count)
