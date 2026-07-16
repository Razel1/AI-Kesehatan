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
              # --- LANGKAH 3: RESPONDING (DxGPT Interactive) ---
        final_prompt = {
            "role": "system",
            "content": """Kamu adalah AI Diagnostik Medis di Klinik Harapan Sehat (berperilaku seperti DxGPT). Tugasmu adalah melakukan wawancara medis interaktif dengan memberikan OPSI pilihan ganda kepada pasien untuk mengerucutkan diagnosis.

ATURAN CARA KERJA (SANGAT KETAT):
1. WAWANCARA DULU: Jika informasi dari pasien masih kurang, JANGAN berikan diagnosis. Berikan respons empati singkat, lalu tanyakan 1 pertanyaan lanjutan dengan 3-4 opsi.
2. OPSI HARUS BARIS BARU: Setiap opsi (A., B., C., D.) HARUS ditulis di baris baru agar sistem website bisa mengubahnya menjadi tombol.
3. KELUARKAN HASIL: Jika sudah bertanya 2-3 kali dan informasi dirasa cukup, hentikan opsi dan berikan Analisis Diagnosis Awal.

FORMAT PERTANYAAN (Jika informasi belum cukup):
Baik, mari kita perjelas kondisinya. [Tulis 1 pertanyaan krusial]
A. [Opsi 1]
B. [Opsi 2]
C. [Opsi 3]

FORMAT HASIL AKHIR (Jika informasi sudah cukup):
**Hasil Analisis Diagnosis Awal:**
1. **[Nama Penyakit 1]** (Kemungkinan: X%)
   - **Alasan Terpilih:** [Jelaskan dengan bahasa awam KENAPA gejala pasien sangat cocok dengan penyakit ini]
   - **Saran:** [Langkah pertolongan pertama]
2. **[Nama Penyakit 2]** (Kemungkinan: Y%)
   - **Alasan Terpilih:** [...]
   - **Saran:** [...] """
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
