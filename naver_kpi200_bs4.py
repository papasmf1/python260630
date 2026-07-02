import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import parse_qs, urlparse
import sys

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


def _parse_entry_table(table):
    if table is None:
        return []

    rows = []
    for tr in table.select("tr"):
        tds = tr.find_all("td")
        if len(tds) != 7:
            continue

        # Skip blank/divider rows.
        classes = set(tr.get("class", []))
        if classes.intersection({"blank_07", "blank_09", "division_line"}):
            continue

        name_link = tds[0].select_one("a[href*='item/main.naver?code=']")
        if not name_link:
            continue

        cols = [td.get_text(" ", strip=True) for td in tds]
        query = parse_qs(urlparse(name_link.get("href", "")).query)
        item_code = query.get("code", [None])[0]

        row = {
            "name": cols[0],
            "code": item_code,
            "price": cols[1],
            "change": cols[2],
            "rate": cols[3],
            "volume": cols[4],
            "amount_million": cols[5],
            "market_cap_100m": cols[6],
        }
        rows.append(row)

    return rows


def crawl_top_components(code="KPI200", total_pages=20):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        )
    }

    all_items = []
    seen_codes = set()

    for page in range(1, total_pages + 1):
        page_url = f"https://finance.naver.com/sise/entryJongmok.naver?type={code}&page={page}"
        res = requests.get(page_url, headers=headers, timeout=10)
        res.raise_for_status()
        res.encoding = res.apparent_encoding

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table.type_1")
        page_items = _parse_entry_table(table)

        for item in page_items:
            item_code = item.get("code")
            if item_code and item_code in seen_codes:
                continue
            if item_code:
                seen_codes.add(item_code)
            all_items.append(item)

    return all_items


def save_to_excel(items, file_path="kospi200.xlsx"):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "KOSPI200"

    headers = [
        "종목명",
        "종목코드",
        "현재가",
        "전일비",
        "등락률",
        "거래량",
        "거래대금(백만)",
        "시가총액(억)",
    ]
    sheet.append(headers)

    for item in items:
        sheet.append(
            [
                item.get("name"),
                item.get("code"),
                item.get("price"),
                item.get("change"),
                item.get("rate"),
                item.get("volume"),
                item.get("amount_million"),
                item.get("market_cap_100m"),
            ]
        )

    workbook.save(file_path)


class CrawlWorker(QThread):
    success = pyqtSignal(list)
    failed = pyqtSignal(str)

    def __init__(self, code, total_pages, parent=None):
        super().__init__(parent)
        self.code = code
        self.total_pages = total_pages

    def run(self):
        try:
            items = crawl_top_components(self.code, self.total_pages)
            self.success.emit(items)
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setWindowTitle("네이버 지수 구성종목 수집기")
        self.resize(980, 680)
        self._build_ui()

    def _build_ui(self):
        root = QWidget(self)
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("지수코드(type):"))
        self.code_input = QLineEdit("KPI200")
        self.code_input.setPlaceholderText("예: KPI200")
        row1.addWidget(self.code_input)

        row1.addWidget(QLabel("페이지 수:"))
        self.pages_input = QSpinBox()
        self.pages_input.setRange(1, 200)
        self.pages_input.setValue(20)
        row1.addWidget(self.pages_input)
        main_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("저장 파일:"))
        self.file_input = QLineEdit("kospi200.xlsx")
        row2.addWidget(self.file_input)

        browse_button = QPushButton("찾아보기")
        browse_button.clicked.connect(self.select_file)
        row2.addWidget(browse_button)
        main_layout.addLayout(row2)

        row3 = QHBoxLayout()
        self.run_button = QPushButton("수집 후 엑셀 저장")
        self.run_button.clicked.connect(self.run_crawl)
        row3.addWidget(self.run_button)

        self.status_label = QLabel("대기 중")
        row3.addWidget(self.status_label)
        main_layout.addLayout(row3)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "종목명",
                "종목코드",
                "현재가",
                "전일비",
                "등락률",
                "거래량",
                "거래대금(백만)",
                "시가총액(억)",
            ]
        )
        main_layout.addWidget(self.table)

    def select_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "저장할 엑셀 파일 선택",
            self.file_input.text().strip() or "kospi200.xlsx",
            "Excel Files (*.xlsx)",
        )
        if path:
            self.file_input.setText(path)

    def run_crawl(self):
        code = self.code_input.text().strip() or "KPI200"
        total_pages = self.pages_input.value()

        self.run_button.setEnabled(False)
        self.status_label.setText("수집 중...")

        self.worker = CrawlWorker(code, total_pages, self)
        self.worker.success.connect(self.on_crawl_success)
        self.worker.failed.connect(self.on_crawl_failed)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_crawl_success(self, items):
        self._populate_table(items)

        output_file = self.file_input.text().strip() or "kospi200.xlsx"
        try:
            save_to_excel(items, output_file)
            self.status_label.setText(f"완료: {len(items)}건 저장")
            QMessageBox.information(
                self,
                "완료",
                f"총 {len(items)}건 수집 후 저장했습니다.\n파일: {output_file}",
            )
        except Exception as exc:
            self.status_label.setText("엑셀 저장 실패")
            QMessageBox.critical(self, "저장 오류", str(exc))

    def on_crawl_failed(self, message):
        self.status_label.setText("수집 실패")
        QMessageBox.critical(self, "수집 오류", message)

    def on_worker_finished(self):
        self.run_button.setEnabled(True)

    def _populate_table(self, items):
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            values = [
                item.get("name", ""),
                item.get("code", ""),
                item.get("price", ""),
                item.get("change", ""),
                item.get("rate", ""),
                item.get("volume", ""),
                item.get("amount_million", ""),
                item.get("market_cap_100m", ""),
            ]
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
