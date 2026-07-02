import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import parse_qs, urlparse


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


if __name__ == "__main__":
    items = crawl_top_components("KPI200")
    output_file = "kospi200.xlsx"
    save_to_excel(items, output_file)

    print(f"count: {len(items)}")
    print(f"saved: {output_file}")
    for i, item in enumerate(items, 1):
        print(
            f"{i:2d}. {item['name']:<12}({item['code']}) | price: {item['price']:<10} "
            f"| change: {item['change']:<12} | rate: {item['rate']}"
        )
