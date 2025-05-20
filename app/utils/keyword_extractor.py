from utils.gemini_handler import generate_answer

#Verilen hukuk sorusundan, belirtilen sayıda (default 5) anahtar kelime çıkarır.
def extract_keywords(question, max_keywords=5):
    prompt = f"""Aşağıdaki hukuk sorusundan en uygun {max_keywords} anahtar kelimeyi çıkar.
Anahtar kelimeleri aralarında birer boşluk bırakarak yaz.

Örnek Çıktı: ehliyeysiz kaza motosiklet  

Soru: {question}

Anahtar Kelimeler:"""

    response = generate_answer(prompt)

    return response.candidates[0].content.parts[0].text
