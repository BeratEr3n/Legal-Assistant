import streamlit as st
from research_page import show_research_page
from petition_page import show_petition_page

# Sayfa başlığı ve geniş düzen ayarı
st.set_page_config(page_title="⚖️ Hukuk Asistanı", layout="wide")

# Sayfa durumu ilk kez tanımlanıyorsa 'home' olarak ayarlanır
if "page" not in st.session_state:
    st.session_state.page = "home"

# Ana sayfaya dönme işlevi
def go_home():
    st.session_state.page = "home"

# Hukuk araştırma sayfasına geçiş
def go_to_research():
    st.session_state.page = "research"

# Dilekçe oluşturma sayfasına geçiş
def go_to_petition():
    st.session_state.page = "petition"

# Ana sayfa görüntüleniyor
if st.session_state.page == "home":

    st.title("⚖️ Yapay Zeka Tabanlı Hukuk Asistanı")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Hukuk Araştırma Asistanı")
        st.write("""
        Yasal kaynakları, içtihatları ve kanunları araştırmak için bu bölümü kullanabilirsiniz.
        """)
        st.button("Araştırmaya Başla", on_click=go_to_research)

    with col2:
        st.subheader("📝 Dilekçe Hazırlama Asistanı")
        st.write("""
        İhtiyacınıza uygun otomatik dilekçeler oluşturmak için bu bölümü kullanabilirsiniz.
        """)
        st.button("Dilekçe Hazırlamaya Başla", on_click=go_to_petition)

# Hukuk araştırma sayfası çağrılır
elif st.session_state.page == "research":
    show_research_page(go_home)
    
# Dilekçe hazırlama sayfası çağrılır
elif st.session_state.page == "petition":
    show_petition_page(go_home)