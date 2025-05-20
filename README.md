
# Hukuki Dilekçe ve Karar Destek Sistemi

## Proje Hakkında

Bu proje, kullanıcıların hukuki dilekçeler hazırlamasına, PDF formatındaki hukuki dokümanlar üzerinde arama yapmasına ve Yargıtay kararları üzerinden ilgili bilgi sorgulamaya imkan sağlayan bir hukuk destek asistanıdır.

### Özellikler
- Kullanıcıdan alınan bilgilerle resmi ve anlaşılır dilekçe oluşturma.
- Yüklenen PDF dosyalarından metin çıkarma, vektörleştirme ve sorgulama.
- Yargıtay kararları üzerinde anahtar kelime tabanlı arama ve ilgili kararların detaylı incelenmesi.
- Google Gemini API kullanarak doğal dil işleme ve embedding işlemleri.
- Vektör tabanlı arama için Qdrant veri deposu entegrasyonu.
- Streamlit ile interaktif ve kullanıcı dostu web arayüzü.

---

## Teknolojiler

- **Python 3.10+**
- **Streamlit:** Hızlı ve kolay web arayüzü geliştirme.
- **Google Gemini API:** Doğal dil işleme ve embedding oluşturma.
- **Qdrant:** Vektör tabanlı arama için yüksek performanslı veritabanı.
- **LangChain:** Doküman yönetimi ve metin parçalama.
- **PyMuPDF (fitz):** PDF dosyalarından metin çıkarma.
- **BeautifulSoup & Requests:** Web scraping ve Yargıtay kararlarının çekilmesi.
- **dotenv:** API anahtarlarını güvenli şekilde yönetme.

---

## Kurulum

1. Depoyu klonlayın:

```bash
git clone https://github.com/kullanici/proje-adi.git
cd proje-adi
```

2. Sanal ortam oluşturup aktif edin:

```bash
python -m venv venv
source venv/bin/activate   # Windows için: venv\Scripts\activate
```

3. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

4. `.env` dosyasını oluşturun ve gerekli API anahtarlarını ekleyin:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key_if_any
```

5. Qdrant sunucusunu kurup başlatın:

- [Qdrant Kurulum Kılavuzu](https://qdrant.tech/documentation/quick_start/)

---

## Kullanım

Projeyi çalıştırmak için:

```bash
streamlit run app.py
```

### Ana Özellikler:

- **Dilekçe Hazırlama:** Formu doldurarak resmi ve anlaşılır dilekçenizi oluşturabilirsiniz.
- **PDF Sorgulama:** Elinizdeki hukuki PDF dokümanlarını yükleyip sorgularınıza göre içerik arayabilirsiniz.
- **Yargıtay Karar Arama:** Sorunuzdan çıkarılan anahtar kelimelerle Yargıtay kararları otomatik aranır ve ilgili kararlar üzerinden yanıt sunulur.

---

## Dosya Yapısı

```
├── app 
│   ├── assets
│   │   └── style.css          
│   ├── utils                
│   │   ├── gemini_handler.py
│   │   ├── keyword_extractor.py
│   │   ├── pdf_handler.py
│   │   ├── query_handler.py
│   │   ├── vektor_store.py
│   │   └── web_searcher.py
│   ├── main.py
│   ├── petition_page.py
│   └── petition_page.py
├── uploaded_pdfs    
├── requirements.txt
├── .env
└── README.md
```

---

## Önemli Notlar

- Google Gemini API ve Qdrant servislerinin doğru çalışması için gerekli API anahtarlarının `.env` dosyasına eklenmesi zorunludur.
- Yargıtay kararları kamuya açık verilerden çekilmektedir; projenin kullanım şekline bağlı olarak yasal sorumluluk kullanıcıya aittir.
- Projenin genişletilmesi ve farklı hukuki kaynaklarla entegrasyonlar yapılabilir.

---

## Lisans

[MIT Lisansı](LICENSE)

---

Herhangi bir sorunuz veya katkınız için çekinmeden iletişime geçebilirsiniz.
