import streamlit as st
import os
from datetime import datetime
from utils.query_handler import handle_general_query, handle_pdf_query, handle_internet_query

# Uygulamanın özel CSS stilini yükler
def load_css():
    with open("assets/style.css", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Araştırma sayfasını gösterir
def show_research_page(go_home_callback):
    load_css()

    st.title("🔍 Hukuk Araştırma Asistanı")

    # Oturum durumu değişkenlerini başlatır
    if "pdf_mode" not in st.session_state:
        st.session_state.pdf_mode = False
    if "internet_mode" not in st.session_state:
        st.session_state.internet_mode = False
    if "uploaded_pdf_name" not in st.session_state:
        st.session_state.uploaded_pdf_name = None

    # Modlar arasında geçiş yapan fonksiyonlar
    def toggle_pdf():
        st.session_state.pdf_mode = True
        st.session_state.internet_mode = False

    def toggle_internet():
        st.session_state.internet_mode = True
        st.session_state.pdf_mode = False

    def toggle_general():
        st.session_state.internet_mode = False
        st.session_state.pdf_mode = False

    # Modlara göre ipucu metni belirle
    if st.session_state.pdf_mode:
        placeholder = "📄 PDF ile ilgili sormak istediğiniz soruyu yazın..."
    elif st.session_state.internet_mode:
        placeholder = "🌐 İnternetten aramak istediğiniz hukuki sorunuzu yazın..."
    else:
        placeholder = "💬 Genel hukuk sorunuz..."

    # Kullanıcı giriş alanı
    user_input = st.text_input("✏️", placeholder=placeholder, key="user_input")
    
    # Butonlar için kolon düzeni
    col1, col4, col2, col3 = st.columns([1, 2, 2, 2])

    with col1:
        send_disabled = not user_input.strip()
        send_clicked = st.button("⬆️  Gönder", disabled=send_disabled)

    # İnternet modu butonu
    with col2:
        if st.session_state.internet_mode:
            st.markdown('<button class="custom-button active">🌐 İnternet Araması</button>', unsafe_allow_html=True)
        else:
            if st.button("🌐 İnternet Araması", key="web_btn"):
                toggle_internet()

    # PDF modu butonu
    with col3:
        if st.session_state.pdf_mode:
            st.markdown('<button class="custom-button active">📄 PDF Araması</button>', unsafe_allow_html=True)
        else:
            if st.button("📄 PDF Araması", key="pdf_btn"):
                toggle_pdf()

    # Genel arama modu butonu
    with col4:
        if not st.session_state.pdf_mode and not st.session_state.internet_mode:
            st.markdown('<button class="custom-button active">💬 Genel Arama</button>', unsafe_allow_html=True)
        else:
            if st.button("💬 Genel Arama", key="general_btn"):
                toggle_general()

    # PDF Yükleme Alanı
    if st.session_state.pdf_mode:
        uploaded_file = st.file_uploader("📤 PDF Dosyası Yükle", type=["pdf"], key="pdf_uploader")
        if uploaded_file is not None:
            upload_dir = "uploaded_pdfs"
            os.makedirs(upload_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_path = os.path.join(upload_dir, f"{timestamp}_{uploaded_file.name}")
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.uploaded_pdf_name = pdf_path
            st.success(f"✅ {uploaded_file.name} başarıyla yüklendi.")

    # PDF yüklenmişse ve PDF modu pasifse yine de göster
    elif st.session_state.uploaded_pdf_name:
        st.markdown(f"📎 Yüklü: **{st.session_state.uploaded_pdf_name}**")

    # Anasayfaya dönüş butonu
    st.markdown("---")
    st.button("🔙 Anasayfaya Dön", on_click=go_home_callback)

    # Kullanıcı sorguyu gönderdiğinde ilgili işleme yönlendir
    if send_clicked:
        query = user_input.strip()

        if st.session_state.pdf_mode:
            st.info("📄 PDF ile ilgili arama yapılıyor...")
            pdf_path = st.session_state.uploaded_pdf_name
            answer = handle_pdf_query(query, pdf_path)
            st.write(answer)

        elif st.session_state.internet_mode:
            st.info("🌐 İnternet araması yapılıyor...")
            answer = handle_internet_query(query)
            st.write(answer)

        else:
            st.info("💬 Genel bir soru gönderildi, işleniyor...")
            answer = handle_general_query(query)
            st.write(answer)
