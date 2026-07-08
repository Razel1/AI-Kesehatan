import streamlit as st
import litellm
import os

# 1. Masukkan API Key Groq kamu di sini
os.environ["GROQ_API_KEY"] = "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"

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Klinik Harapan Sehat", page_icon="🏥", layout="wide")

# --- SIDEBAR (Panel Samping) ---
with st.sidebar:
    st.title("🏥 Harapan Sehat")
    st.markdown("---")
    st.write("**🕒 Jam Operasional:**")
    st.write("• Senin - Jumat: 08.00 - 20.00 WIB")
    st.write("• Sabtu - Minggu: 09.00 - 15.00 WIB")
    st.markdown("---")
    st.info("💡 **Catatan:** AI ini dikonfigurasi untuk skrining awal dan saran penanganan darurat pertama oleh Dokter Senior.")
    
    # Tombol untuk reset obrolan
    if st.button("🔄 Mulai Obrolan Baru"):
        st.session_state.messages = []
        st.rerun()

# --- TAMPILAN UTAMA ---
st.title("Halo! Saya Dr. Anda. Ada yang bisa saya bantu? ✨")
st.write("Silakan ceritakan keluhan kesehatan yang Anda rasakan di bawah ini.")

# --- SESSION STATE (Menyimpan Riwayat Chat) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat di layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT CHAT DARI PASIEN ---
if gejala := st.chat_input("Ketik keluhan Anda di sini... (Contoh: Sudah 2 hari demam dan pusing)"):
    
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(gejala)
    
    st.session_state.messages.append({"role": "user", "content": gejala})
    
    # Proses AI dengan Persona Dokter Senior
    with st.chat_message("assistant"):
        with st.spinner("Dr. Anda sedang menganalisis gejala Anda..."):
            try:
                system_prompt = {
                    "role": "system", 
                    "content": """Kamu adalah Dr. Anda, seorang dokter umum senior dengan pengalaman lebih dari 15 tahun di Klinik Harapan Sehat. Sifatmu empatik, menenangkan, analitis, dan profesional. 

                    Tugas utamamu adalah menganalisis gejala pasien dan memberikan edukasi.
                    PANDUAN MENJAWAB:
                    1. Empati: Mulai dengan sapaan hangat dan tunjukkan empati atas keluhan mereka.
                    2. Analisis & Diagnosis Banding: Sebutkan 2-3 kemungkinan kondisi medis yang paling masuk akal berdasarkan gejala. Gunakan bahasa awam yang mudah dipahami.
                    3. Penanganan Mandiri: Berikan tips pertolongan pertama atau obat bebas yang aman (misal: paracetamol).
                    4. Arahan: Sarankan untuk datang langsung ke Klinik Harapan Sehat untuk pemeriksaan fisik."""
                }
                
                messages_for_api = [system_prompt] + st.session_state.messages
                
                respons = litellm.completion(
                    model="groq/llama-3.3-70b-versatile",
                    messages=messages_for_api
                )
                
                jawaban_ai = respons.choices[0].message.content
                
                st.markdown(jawaban_ai)
                st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})
                
            except Exception as e:
                st.error(f"Maaf, sistem klinik sedang sibuk: {e}")
