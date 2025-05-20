import streamlit as st
from utils.gemini_handler import generate_answer, generate_answer_from_docs
from utils.pdf_handler import process_uploaded_pdf, process_decisions_text
from utils.vektor_store import initialize_vector_store, add_to_vector_store, query_vector_store
from utils.keyword_extractor import extract_keywords
from utils.web_searcher import fetch_decision_texts

# Genel hukuki sorular için basit bir yanıt üretir.
def handle_general_query(query: str):
    prompt = f"""
Sen profesyonel bir hukuk danışmanısın. Aşağıda kullanıcıdan gelen bir hukuki soru var.
Amacın bu soruya kısa, açık, teknik terimlere dayanan ve resmi bir dille yanıt vermektir.
Yanıtın yaklaşık 4-5 cümleyi geçmemelidir.

Soru: "{query}"

Cevap:
"""
    response = generate_answer(prompt)
    return response.candidates[0].content.parts[0].text

# Yüklenen PDF dosyasındaki metinlerden sorguya en uygun bilgiyi çıkarır ve yanıt üretir.
def handle_pdf_query(query: str, pdf_path: str):
    COLLECTION_NAME = "research_pdf"
    
    st.info("PDF işleniyor...")
    docs = process_uploaded_pdf(pdf_path)
    
    client, embeddings = initialize_vector_store(COLLECTION_NAME)

    st.info("Vektör veritabanına kaydediliyor...")
    add_to_vector_store(client, embeddings, docs, COLLECTION_NAME)

    st.info("Sorunuza en uygun içerik aranıyor...")
    relevant_docs = query_vector_store(client, embeddings, query, COLLECTION_NAME)
                    
    st.info("Yanıt oluşturuluyor...")
    answer = generate_answer_from_docs(query, relevant_docs)

    return answer.candidates[0].content.parts[0].text

# Yargıtay kararlarından, sorguya uygun karar metinlerini indirir, işler ve yanıt üretir.
def handle_internet_query(query: str):
    COLLECTION_NAME = "research_pdfs"

    keywords = extract_keywords(query)
    st.success(f"Çıkarılan Anahtar Kelimeler: {keywords}")

    st.info("Yargitay.gov.tr'de ilgili Kararlar aranıyor...")
    decisions_text  = fetch_decision_texts(keywords) 

    if not decisions_text:
        st.error("İlgili Kararlar bulunamadı. Lütfen sorunuzu değiştirip tekrar deneyin.")
    else:
        st.info("Kararlar indiriliyor ve işleniyor...")
        docs = process_decisions_text(decisions_text) 
        if not docs:
            st.error("Kararlar işlenirken bir hata oluştu.")
        else:
            st.info("Vektör veritabanına kaydediliyor...") 
            client, embeddings = initialize_vector_store(COLLECTION_NAME)
            add_to_vector_store(client, embeddings, docs, COLLECTION_NAME)

            st.info("Sorunuza en uygun içerik aranıyor...")
            relevant_docs = query_vector_store(client, embeddings, query, COLLECTION_NAME)

            st.info("Yanıt oluşturuluyor...")
            answer = generate_answer_from_docs(query, relevant_docs)

            return answer.candidates[0].content.parts[0].text