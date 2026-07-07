import streamlit as st
import litellm
import os

# 1. Masukkan API Key Groq kamu di sini
os.environ["GROQ_API_KEY"] = "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"

# --- TAMPILAN WEB APP ---
st.set_page_config(page_title="Klinik Harapan Sehat", page_icon="🏥")
st.title("🏥 Klinik Harapan Sehat - Skrining AI")
st.write("Silakan masukkan keluhan Anda di bawah ini:")

# Input keluhan dari pasien
gejala = st.text_area("Keluhan Anda:", placeholder="Contoh: Pusing sebelah kanan, hidung tersumbat, dan mual...")

# Tombol untuk memicu AI
if st.button("Analisis Gejala"):
    if gejala:
        # Menampilkan efek loading saat AI sedang mikir
        with st.spinner("AI Llama 3.1 sedang menganalisis super cepat..."):
            try:
                # Memanggil API Groq lewat litellm
                respons = litellm.completion(
                    model="groq/llama-3.3-70b-versatile", # <-- Menggunakan model Groq terbaru yang paling cepat
                    messages=[
                        {
                            "role": "system", 
                            "content": "Kamu adalah asisten klinik yang ramah dan profesional. Jawablah menggunakan bahasa Indonesia yang baik. Berikan tips ringan dan penanganan pertama. JANGAN PERNAH memberikan diagnosis pasti atau resep obat keras. Selalu sarankan untuk menemui dokter secara langsung."
                        },
                        {
                            "role": "user", 
                            "content": gejala
                        }
                    ]
                )
                
                # Menampilkan hasil jawaban di web
                st.success("Saran dari AI Klinik:")
                st.write(respons.choices[0].message.content)
            
            except Exception as e:
                # Mencegah web crash jika terjadi error
                st.error(f"Maaf, AI sedang ada kendala: {e}")
                
    else:
        # Peringatan kalau teks kosong tapi tombol keburu dipencet
        st.warning("Mohon tuliskan keluhan Anda terlebih dahulu sebelum menekan tombol.")