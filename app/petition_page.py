import streamlit as st
from utils.gemini_handler import generate_answer

# Dilekçe hazırlama sayfasını gösterir
def show_petition_page(go_home_callback):
    st.header("📝 Dilekçe Hazırlama Asistanı")

    # Kullanıcıdan alınan bilgiler
    full_name = st.text_input("Ad Soyad *")
    address = st.text_area("Adres")
    court_name = st.text_input("Mahkeme Adı * (örn. İstanbul Anadolu 5. Aile Mahkemesi)")
    case_type = st.selectbox("Dava Türü *", ["Seçiniz", "Boşanma", "İcra", "İş Davası", "Tüketici", "Diğer"])
    opponent_name = st.text_input("Davalı/Davacı Adı *")
    petition_details = st.text_area("Olayın Özeti / Gerekçe *")

    # Zorunlu alanları kontrol etmek için alanlar listesi
    required_fields = {
        "Ad Soyad": full_name,
        "Mahkeme Adı": court_name,
        "Dava Türü": case_type if case_type != "Seçiniz" else "",
        "Karşı Taraf": opponent_name,
        "Olay Özeti": petition_details
    }

    # Kullanıcı "Dilekçeyi Oluştur" butonuna bastığında
    if st.button("📄 Dilekçeyi Oluştur"):
        
        # Eksik alanları kontrol et
        missing_fields = [label for label, value in required_fields.items() if not value.strip()]
        if missing_fields:
            st.error(f"Lütfen aşağıdaki zorunlu alanları doldurunuz: {', '.join(missing_fields)}")
            return
        
        # Yapay zekâya gönderilecek dilekçe oluşturma komutu
        prompt = f"""
Sen bir hukuk asistanısın. Aşağıdaki bilgileri kullanarak resmi ve düzgün bir dilekçe hazırla. 
Metin sade ve anlaşılır bir Türkçe ile yazılsın. Giriş, olay açıklaması ve sonuç (talep) bölümleri olsun.

Bilgiler:
- Ad Soyad: {full_name}
- Adres: {address}
- Mahkeme: {court_name}
- Dava Türü: {case_type}
- Karşı Taraf: {opponent_name}
- Olay Özeti / Gerekçe: {petition_details}

Resmi ve geçerli bir dilekçe yapısı kullan. En sonunda “Gereğini arz ederim.” ile bitir.
"""

        # Yapay zekâdan dilekçeyi al
        response = generate_answer(prompt)
        st.write(response.candidates[0].content.parts[0].text)
        
    # Anasayfaya dönüş butonu
    st.button("🔙 Anasayfaya Dön", on_click=go_home_callback)
