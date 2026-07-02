import sqlite3
import sys
from typing import Iterable, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ProductManager(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Bike Product Manager (PyQt6 + SQLite3)")
        self.resize(820, 540)

        self.conn = sqlite3.connect("myproduct.db")
        self._create_table()

        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setPlaceholderText("auto-generated")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Helmet, Gloves, Light")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("e.g. 39000")

        self.add_button = QPushButton("Input")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.search_button = QPushButton("Search")

        self.table = QTableWidget()
        self._build_ui()
        self._apply_styles()
        self._connect_signals()
        self.load_products()

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS MyProduct (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)

        hero_panel = QFrame()
        hero_panel.setObjectName("heroPanel")
        hero_layout = QVBoxLayout(hero_panel)
        hero_layout.setContentsMargins(20, 16, 20, 16)
        hero_title = QLabel("Bike Gear Inventory")
        hero_title.setObjectName("heroTitle")
        hero_subtitle = QLabel("PyQt6 + SQLite3 / Fast input, update, delete, search")
        hero_subtitle.setObjectName("heroSubtitle")
        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_subtitle)

        form_card = QFrame()
        form_card.setObjectName("formCard")

        form_layout = QFormLayout()
        form_layout.setContentsMargins(18, 16, 18, 6)
        form_layout.setVerticalSpacing(10)
        form_layout.addRow(QLabel("id"), self.id_input)
        form_layout.addRow(QLabel("name"), self.name_input)
        form_layout.addRow(QLabel("price"), self.price_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)
        button_layout.setContentsMargins(18, 0, 18, 14)
        button_layout.setSpacing(10)

        form_card_layout = QVBoxLayout(form_card)
        form_card_layout.setContentsMargins(0, 0, 0, 0)
        form_card_layout.addLayout(form_layout)
        form_card_layout.addLayout(button_layout)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["id", "name", "price"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)
        layout.addWidget(hero_panel)
        layout.addWidget(form_card)
        layout.addWidget(self.table)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0b132b,
                    stop: 0.45 #1c2541,
                    stop: 1 #3a506b
                );
            }
            QWidget {
                color: #f4f7fb;
                font-family: "Segoe UI";
                font-size: 13px;
            }
            QFrame#heroPanel {
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #5bc0be,
                    stop: 1 #4ea8de
                );
            }
            QLabel#heroTitle {
                color: #072031;
                font-size: 26px;
                font-weight: 800;
            }
            QLabel#heroSubtitle {
                color: #133547;
                font-size: 12px;
                font-weight: 600;
            }
            QFrame#formCard {
                background: rgba(11, 19, 43, 0.55);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 14px;
            }
            QLabel {
                font-weight: 600;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.96);
                color: #17223b;
                border: 2px solid transparent;
                border-radius: 10px;
                padding: 8px 10px;
                selection-background-color: #4ea8de;
            }
            QLineEdit:focus {
                border: 2px solid #5bc0be;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ffd166,
                    stop: 1 #f77f00
                );
                color: #2d1b00;
                border: none;
                border-radius: 11px;
                padding: 9px 16px;
                font-size: 12px;
                font-weight: 800;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ffe08a,
                    stop: 1 #ff9e1f
                );
            }
            QPushButton:pressed {
                padding-top: 10px;
                padding-bottom: 8px;
            }
            QTableWidget {
                background: rgba(255, 255, 255, 0.95);
                color: #17223b;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                gridline-color: #d6deeb;
                alternate-background-color: #eaf1fb;
                selection-background-color: #5bc0be;
                selection-color: #0e2a3a;
            }
            QHeaderView::section {
                background: #1c2541;
                color: #f8fbff;
                border: none;
                border-right: 1px solid #2f3f68;
                padding: 8px;
                font-size: 12px;
                font-weight: 700;
            }
            QTableCornerButton::section {
                background: #1c2541;
                border: none;
            }
            """
        )
        self.table.setAlternatingRowColors(True)

    def _connect_signals(self) -> None:
        self.add_button.clicked.connect(self.add_product)
        self.update_button.clicked.connect(self.update_product)
        self.delete_button.clicked.connect(self.delete_product)
        self.search_button.clicked.connect(self.search_products)
        self.table.cellClicked.connect(self._sync_form_with_selected_row)

    def _validate_inputs(self, require_id: bool = False) -> Tuple[bool, str, int, int]:
        id_text = self.id_input.text().strip()
        name = self.name_input.text().strip()
        price_text = self.price_input.text().strip()

        if require_id and not id_text:
            self._show_warning("Select a row first.")
            return False, "", 0, 0

        if not name:
            self._show_warning("name is required.")
            return False, "", 0, 0

        try:
            price = int(price_text)
        except ValueError:
            self._show_warning("price must be an integer.")
            return False, "", 0, 0

        if price < 0:
            self._show_warning("price must be >= 0.")
            return False, "", 0, 0

        row_id = int(id_text) if id_text else 0
        return True, name, price, row_id

    def add_product(self) -> None:
        ok, name, price, _ = self._validate_inputs(require_id=False)
        if not ok:
            return

        self.conn.execute(
            "INSERT INTO MyProduct (name, price) VALUES (?, ?)",
            (name, price),
        )
        self.conn.commit()
        self._clear_form(keep_search_text=False)
        self.load_products()

    def update_product(self) -> None:
        ok, name, price, row_id = self._validate_inputs(require_id=True)
        if not ok:
            return

        cur = self.conn.execute(
            "UPDATE MyProduct SET name = ?, price = ? WHERE id = ?",
            (name, price, row_id),
        )
        self.conn.commit()

        if cur.rowcount == 0:
            self._show_warning("No matching row found.")
            return

        self.load_products()

    def delete_product(self) -> None:
        id_text = self.id_input.text().strip()
        if not id_text:
            self._show_warning("Select a row first.")
            return

        row_id = int(id_text)
        cur = self.conn.execute("DELETE FROM MyProduct WHERE id = ?", (row_id,))
        self.conn.commit()

        if cur.rowcount == 0:
            self._show_warning("No matching row found.")
            return

        self._clear_form(keep_search_text=False)
        self.load_products()

    def search_products(self) -> None:
        name = self.name_input.text().strip()
        id_text = self.id_input.text().strip()

        if id_text:
            rows = self.conn.execute(
                "SELECT id, name, price FROM MyProduct WHERE id = ? ORDER BY id",
                (int(id_text),),
            ).fetchall()
        elif name:
            rows = self.conn.execute(
                "SELECT id, name, price FROM MyProduct WHERE name LIKE ? ORDER BY id",
                (f"%{name}%",),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id, name, price FROM MyProduct ORDER BY id"
            ).fetchall()

        self._render_rows(rows)

    def load_products(self) -> None:
        rows = self.conn.execute(
            "SELECT id, name, price FROM MyProduct ORDER BY id"
        ).fetchall()
        self._render_rows(rows)

    def _render_rows(self, rows: Iterable[Tuple[int, str, int]]) -> None:
        rows = list(rows)
        self.table.setRowCount(len(rows))

        for row_idx, (row_id, name, price) in enumerate(rows):
            id_item = QTableWidgetItem(str(row_id))
            name_item = QTableWidgetItem(name)
            price_item = QTableWidgetItem(str(price))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 0, id_item)
            self.table.setItem(row_idx, 1, name_item)
            self.table.setItem(row_idx, 2, price_item)

        self.table.resizeColumnsToContents()

    def _sync_form_with_selected_row(self, row: int, _: int) -> None:
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.price_input.setText(self.table.item(row, 2).text())

    def _clear_form(self, keep_search_text: bool) -> None:
        self.id_input.clear()
        if not keep_search_text:
            self.name_input.clear()
            self.price_input.clear()

    def _show_warning(self, message: str) -> None:
        QMessageBox.warning(self, "Warning", message)

    def closeEvent(self, event) -> None:  # noqa: N802
        self.conn.close()
        event.accept()


def main() -> None:
    app = QApplication(sys.argv)
    win = ProductManager()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
