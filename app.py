import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="AI Asisten SPJ Fisik - Dinas Arpus",
    page_icon="📄",
    layout="centered"
)

# Judul Aplikasi
st.title("📄 AI Asisten Kelengkapan SPJ Fisik 2026")
st.caption("Dinas Kearsipan dan Perpustakaan Kabupaten Semarang")

# Ambil API Key Gemini dari Streamlit Secrets atau Input User
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    api_key_input = st.sidebar.text_input("Masukkan Google Gemini API Key Anda:", type="password")
    if api_key_input:
        genai.configure(api_key=api_key_input)
    else:
        st.info("Silakan masukkan Gemini API Key di sidebar atau konfigurasi Secrets untuk memulai.")
        st.stop()

# KNOWLEDGE BASE: Diambil langsung dari Bagian "Kelengkapan SPJ Fisik" dokumen Rule Penatausahaan 2026
DATA_SPJ_RULES = """
Berikut adalah aturan resmi Kelengkapan SPJ Fisik Tahun 2026 pada Dinas Kearsipan dan Perpustakaan Kabupaten Semarang:

1. Belanja Perjalanan Dinas Dalam daerah dan Luar Daerah:
   - Surat Tugas, ttd Kepala PD
   - Surat Perintah Perjalanan Dinas (SPPD), ttd Kepala PD
   - Bukti Transfer Uang Harian Perjadin
   - Tanda Terima Uang Harian Perjadin
   - Laporan Perjadin ber-TTD yang melaksanakan Perjadin
   - Foto Perjadin (Minimal 4 Foto, Berwarna dan Jelas, WAJIB menerangkan Lokasi, Titik Koordinat, dan Waktu Pelaksanaan Perjadin memanfaatkan aplikasi GPS Map Camera).

2. Bahan Bakar Minyak (BBM):
   - Surat Tugas, ttd Kepala PD
   - Tanda Terima Uang BBM
   - Struk/Nota Pembelian BBM (Pembelian BBM searah dengan lokasi yang dituju)
   - Screenshoot jarak dari kantor ke lokasi dari aplikasi maps
   - Perhitungan Kebutuhan BBM sesuai rute dan jarak (bisa melalui Menu Calculator Perjadin pada linktree).

3. Belanja Uang Saku Peserta Workshop/Bimtek/Sosialisasi:
   - Surat Undangan Workshop/Bimtek/Sosialisasi
   - Tanda Terima Uang Harian
   - Bukti Pembayaran Billing Pajak
   - Cetak Id Billing Pajak dari Coretax
   - Cetak E-Bupot dari Coretax
   - Foto Kegiatan (Minimal 4 Foto, Berwarna dan Jelas, WAJIB menerangkan Lokasi, Titik Koordinat, dan Waktu Pelaksanaan menggunakan GPS Map Camera).

4. Belanja Tol:
   - Surat Tugas, ttd Kepala PD
   - Struk/Nota Pembayaran Tol.

5. Belanja ATK, Kertas Cover, Bahan Komputer Rutin/Persediaan:
   - Invoice
   - Bukti Pembayaran Invoice
   - Jika di atas 2 juta, lampirkan Foto Barang Diterima.

6. Belanja ATK Keperluan Rapat:
   - Invoice
   - Bukti Pembayaran Invoice
   - Foto Barang Diterima
   - Tanda Terima ATK kepada Peserta
   - Foto Kegiatan (Minimal 4 Foto, Berwarna, Jelas, pakai GPS Map Camera dengan info Lokasi, Koordinat, Waktu).

7. Belanja Makan Minum Rapat/Jamuan Tamu:
   - Melalui KKPD (Kartu Kredit Pemerintah Daerah). Dokumen data dukung yang disetorkan ke Bendahara Pengeluaran meliputi: QRIS KODE BAYAR dari aplikasi TISERA, Invoice dari Aplikasi TISERA, Surat Undangan (Makan Minum Rapat) / Surat Permohonan Kunjungan (Jamuan Tamu) / Surat Tugas (Aktivitas Lapangan), Foto Makan Minum yang diterima, Dokumen Daftar Hadir yang ditandatangani PPTK (daftar hadir rapat menyertakan Jenis Kelamin), Foto Kegiatan ber-GPS & waktu, serta Notulen untuk Makan Minum Rapat.

8. Belanja Uang Harian Lembur Pegawai:
   - Surat Tugas Lembur, ttd Kepala PD
   - Bukti Transfer
   - Tanda Terima UH Lembur
   - Jika Over Time: Lampirkan Daftar Presensi Online sesuai Jam Lembur.
   - Jika Selain Hari Kerja: Lampirkan Daftar Presensi Online selama hari kerja, Daftar Hadir Lembur (Jam Kehadiran & Pulang), Laporan Lembur, dan Foto Kegiatan ber-GPS (Min 4 foto).

9. Belanja Jasa Lain-Lain:
   - Menggunakan Penyedia Jasa yang sudah ber-PKP (Pengusaha Kena Pajak) yang dapat mengeluarkan Faktur PPN.

10. Belanja Honor Narasumber:
    - Surat Tugas/Surat Permohonan Narasumber, ttd Kepala PD
    - Bukti Transfer Honor
    - Bukti Pembayaran Billing Pajak
    - Cetak Id Billing Pajak dari Coretax
    - Cetak E-Bupot dari Coretax
    - Tanda Terima Honor Materi Narsum
    - Daftar Hadir Kegiatan (tambahkan jenis kelamin)
    - Foto Kegiatan ber-GPS (Minimal 4 Foto).

11. Belanja Penginapan (Rekening SPPD maupun Rekening Penginapan Sendiri):
    - Surat Tugas, ttd Kepala PD
    - Bill Hotel/Penginapan
    - Bukti Pembayaran Penginapan.

12. Belanja Hadiah Perlombaan (Anak di bawah Usia Kerja):
    - Laporan Kegiatan Lomba, Tanda Terima Hadiah, Foto Kegiatan & Penerimaan Hadiah ber-GPS (Min 4 foto).

13. Belanja Hadiah Perlombaan (Masyarakat Umum Usia Kerja / Perangkat Daerah / Lembaga Pendidikan):
    - Laporan Kegiatan Lomba, Tanda Terima Hadiah, Potong Pajak Hadiah (apabila uang), Bukti Pembayaran Billing Pajak, Cetak Id Billing dari Coretax, Cetak E-Bupot dari Coretax, Foto Kegiatan & Penerimaan Hadiah ber-GPS (Min 4 foto).

CATATAN PENTING TAMBAHAN:
- SPJ diurutkan berdasarkan tanggal kegiatan, BUKAN tanggal pembayaran atau per kode rekening.
- Pengumpulan SPJ Fisik maksimal setiap tanggal 05 bulan berikutnya ke Bendahara Pengeluaran. Harus diketahui Kasubbag/Ketua Tim, diparaf PPTK, dilengkapi Cover SPJ, Pengumpul, dan Kendali 1 Lembar.
- SPJ Fisik yang sudah turun asman dikumpulkan maksimal tanggal 10 bulan berikutnya.
"""

# Setup System Instruction untuk AI
system_instruction = f"""
Anda adalah AI Asisten Penatausahaan Keuangan di Dinas Kearsipan dan Perpustakaan Kabupaten Semarang.
Tugas Anda adalah membantu pegawai atau PPTK memeriksa dan menjawab pertanyaan mengenai kelengkapan dokumen SPJ Fisik Tahun 2026.

Gunakan data aturan di bawah ini sebagai satu-satunya kebenaran (Ground Truth):
{DATA_SPJ_RULES}

Jawablah pertanyaan user dengan ramah, jelas, menggunakan poin-poin (bullet points), dan sampaikan secara tegas dokumen apa saja yang wajib ada. Jika pengguna bertanya tentang hal di luar dokumen di atas, jawab bahwa informasi tersebut tidak diatur dalam pedoman penatausahaan fisik saat ini. Gunakan bahasa Indonesia yang formal namun mudah dipahami.
"""

# Inisialisasi Model Gemini
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=system_instruction
)

# Mengelola History Chat menggunakan Session State Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat history sebelumnya
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom Input Chat User
if user_query := st.chat_input("Contoh: Apa saja kelengkapan SPJ untuk Perjalanan Dinas?"):
    # Tampilkan chat user
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Jalankan Generator Jawaban AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Mengirim chat ke Gemini dengan context terpandu
            response = model.generate_content(user_query)
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.error(f"Terjadi kesalahan pada sistem AI: {e}")
