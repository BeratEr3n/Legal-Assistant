import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Yargıtay karar arama sitesine özel HTTP header'lar
headers = {
    "Host": "karararama.yargitay.gov.tr",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://karararama.yargitay.gov.tr",
    "Referer": "https://karararama.yargitay.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

# Yargıtay karar arama API'sine sorgu gönderir ve sonuçları JSON olarak döner.
def perform_search(query, page=1, page_size=10):
    url = "https://karararama.yargitay.gov.tr/aramalist"
    payload = {
        "data": {
            "aranan": query,
            "arananKelime": query,
            "pageSize": page_size,
            "pageNumber": page
        }
    }
    response = session.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Belirtilen karar ID'sine ait karar detaylarını JSON olarak getirir.
def fetch_decision_by_id(doc_id):
    url = f"https://karararama.yargitay.gov.tr/getDokuman?id={doc_id}"
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# HTML içeriğinden sadece metin kısmını çeker.
def extract_text_from_html(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    body = soup.find("body")
    return body.get_text(separator="\n", strip=True) if body else ""

# Anahtar kelimelerle Yargıtay kararları arar, karar metinlerini getirir ve birleştirerek döner.
def fetch_decision_texts(keywords, limit=7):
    all_results = ""

    try:
        search_results = perform_search(keywords, page=1, page_size=limit)
        decisions = search_results.get("data", {}).get("data", [])[:limit]

        all_results += f"\n### Arama: '{keywords}'\n"

        for decision in decisions:
            decision_id = decision.get("id")
            print(f"İşleniyor: Karar ID {decision_id}")
            if not decision_id:
                continue

            decision_json = fetch_decision_by_id(decision_id)
            html_content = decision_json.get("data", "")
            text = extract_text_from_html(html_content)

            all_results += f"\n--- Karar ID: {decision_id} ---\n{text}\n"

        all_results += "\n" + "=" * 80 + "\n"

    except Exception as e:
        print(f"⚠️ Hata oluştu: {e}")
        all_results += f"\n[HATA: '{keywords}' aranırken sorun yaşandı]\n"

    return all_results