import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}


def fetch_search_page(query):
    url = "https://search.naver.com/search.naver"
    params = {
        "where": "nexearch",
        "sm": "tab_hty.top",
        "ssc": "tab.nx.all",
        "query": query,
    }

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text


def extract_first_text(node, selectors):
    for selector in selectors:
        target = node.select_one(selector)
        if target:
            text = target.get_text(" ", strip=True)
            if text:
                return text
    return ""


def get_news_items(query, max_results=5):
    html = fetch_search_page(query)
    soup = BeautifulSoup(html, "html.parser")

    items = []

    for title_link in soup.select('a[data-heatmap-target=".tit"][href]'):
        title = title_link.get_text(" ", strip=True)
        href = title_link.get("href", "")

        if not title or not href:
            continue

        item_root = title_link.find_parent("div")
        if item_root is None:
            continue

        summary = extract_first_text(
            item_root,
            [
                'a[data-heatmap-target=".body"]',
                '.sds-comps-text-ellipsis-3',
            ],
        )
        source = extract_first_text(
            item_root,
            [
                '.sds-comps-profile-info-title-text span',
                '.sds-comps-profile-info-title-text',
            ],
        )
        time_text = extract_first_text(
            item_root,
            [
                '.sds-comps-profile-info-subtext span',
            ],
        )

        item = {
            "title": title,
            "url": href,
            "source": source,
            "time": time_text,
            "summary": summary,
        }

        if item not in items:
            items.append(item)

        if len(items) >= max_results:
            break

    return items


def crawl_news_article(article_url):
    resp = requests.get(article_url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title = ""
    content = ""

    title_tag = soup.select_one("h2#title_area") or soup.select_one("h2.media_end_head_headline")
    if title_tag:
        title = title_tag.get_text(" ", strip=True)

    content_tag = (
        soup.select_one("#dic_area")
        or soup.select_one("div#newsct_article")
        or soup.select_one("div.article_body")
    )

    if content_tag:
        for tag in content_tag.select("script, style, noscript"):
            tag.decompose()
        content = content_tag.get_text("\n", strip=True)

    return title, content


def save_news_to_excel(news_rows, output_path="naver_result.xlsx"):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "naver_news"

    headers_row = ["검색어", "순번", "기사제목", "언론사", "시간", "요약", "링크", "본문"]
    worksheet.append(headers_row)

    for row in news_rows:
        worksheet.append(
            [
                row.get("query", ""),
                row.get("index", ""),
                row.get("title", ""),
                row.get("source", ""),
                row.get("time", ""),
                row.get("summary", ""),
                row.get("url", ""),
                row.get("content", ""),
            ]
        )

    workbook.save(output_path)


if __name__ == "__main__":
    query = "반도체"
    news_list = get_news_items(query, max_results=5)
    saved_rows = []

    for i, item in enumerate(news_list, 1):
        print(f"\n[{i}] 제목: {item['title']}")
        if item["source"]:
            print(f"언론사: {item['source']}")
        if item["time"]:
            print(f"시간: {item['time']}")
        if item["summary"]:
            print(f"요약: {item['summary']}")
        print(f"링크: {item['url']}")

        try:
            title, content = crawl_news_article(item["url"])
            print(f"기사 제목: {title}")
            print(f"본문:\n{content[:1000]}")
            item["article_title"] = title
            item["content"] = content
        except Exception as e:
            print(f"크롤링 실패: {e}")
            item["article_title"] = ""
            item["content"] = ""

        saved_rows.append(
            {
                "query": query,
                "index": i,
                "title": item.get("article_title") or item.get("title", ""),
                "source": item.get("source", ""),
                "time": item.get("time", ""),
                "summary": item.get("summary", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
        )

    save_news_to_excel(saved_rows, "naver_result.xlsx")
    print("\n엑셀 저장 완료: naver_result.xlsx")