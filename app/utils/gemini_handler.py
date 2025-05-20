import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasından ortam değişkenlerini yükle
load_dotenv()

# Google API anahtarını al
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Google Generative AI kütüphanesini API anahtarı ile yapılandır
genai.configure(api_key=GOOGLE_API_KEY)

# Verilen prompt'a göre yanıt oluşturur
def generate_answer(prompt: str):

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response

# Kullanıcı sorusu ve ilgili belgelerden detaylı, öz yanıt oluşturur
def generate_answer_from_docs(query, documents) -> str:

    # Belgelerdeki sayfa içeriklerini birleştir
    context = "\n\n".join([doc.page_content for doc in documents])

    prompt = f"""
Aşağıda, kullanıcıdan gelen bir hukuki soru ve bu soruyla ilgili belgelerden elde edilen metin parçaları verilmiştir.
Belgeleri dikkate alarak, resmi ve anlaşılır bir dille detaylı fakat öz bir yanıt oluştur.

Soru:
\"{query}\"

İlgili Belgeler:
\"\"\"
{context}
\"\"\"

Cevap, yalnızca belgelerdeki bilgilere dayalı olmalı ve tahmine yer verilmemelidir.
Eğer doğrudan bir yanıt üretilemiyorsa, buna dair açıklayıcı bir ifade kullanılmalıdır.

Cevap:
"""
    return generate_answer(prompt)