# Dashboard Analisis Data E-Commerce

Dashboard ini dibuat untuk menganalisis pola transaksi pelanggan dalam platform e-commerce. Menggunakan Streamlit dan Python, dashboard ini menyajikan visualisasi interaktif terkait pola pembelian, kategori produk, biaya pengiriman, metode pembayaran, dan loyalitas pelanggan berdasarkan RFM Analysis.

---

## Prasyarat

Sebelum menjalankan dashboard, pastikan Anda telah menginstal **Python 3.8 atau lebih baru**.

---

## Instalasi

1. Buat Virtual Environment:

   ```bash
   python -m venv venv
   ```

2. Aktifkan Virtual Environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - MacOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install Prasyarat:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Dashboard

1. Pastikan Dataset Tersedia:
   - Dataset yang digunakan harus tersedia dalam direktori proyek.
2. Jalankan Dashboard:
   ```bash
   streamlit run dashboard/dashboard.py
   ```
3. Akses Dashboard:
   - Buka browser dan akses http://localhost:8501.
   - Dashboard siap digunakan!

## Fitur Dashboard

1. Pola Pembelian Pelanggan:

   - Menampilkan tren transaksi pelanggan.
   - Memungkinkan filter berdasarkan tahun dan lokasi.
   - Insight: Mayoritas pelanggan hanya melakukan satu kali transaksi.

2. Pola Pembelian Berdasarkan Kategori Produk:

   - Menampilkan kategori produk yang paling sering dibeli.
   - Insight: Produk dengan harga lebih rendah lebih sering dibeli.

3. Pengaruh Biaya Pengiriman terhadap Jumlah Transaksi:

   - Menganalisis hubungan antara biaya pengiriman dan jumlah transaksi.
   - Insight: Ongkir tinggi mengurangi jumlah pembelian.

4. Distribusi Metode Pembayaran:
   - Menampilkan metode pembayaran yang paling sering digunakan pelanggan.
   - Insight: Kartu kredit merupakan metode pembayaran paling dominan.

5. Pola Loyalitas Pelanggan Berdasarkan RFM Analysis:
   - Mengelompokkan pelanggan berdasarkan Recency, Frequency, dan Monetary.
   - Insight: Sebagian besar pelanggan jarang bertransaksi.

Dashboard ini dirancang untuk membantu bisnis dalam memahami pola transaksi pelanggan dan menyusun strategi pemasaran yang lebih efektif. 🚀