# 🌿 PasarSemaka — Pasar Digital Produk Lokal Kabupaten Tanggamus

> **Platform E-Commerce & Sistem Monitoring UMKM Terpadu Kabupaten Tanggamus, Provinsi Lampung**  
> *Dimensi Smart City: Smart Economy*  
> **Inisiatif Kolaboratif**: Pemerintah Kabupaten Tanggamus & Universitas Teknokrat Indonesia (UTI) Lampung  
> **Penyusun**: **Athi Cahyani R** (NPM: 24311007) & **Dr. Erliyan Redy Susanto, M.Kom.**  
> **Copyright © 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom.**

---

## 📌 Ringkasan Eksekutif & Identitas Proyek

**PasarSemaka** adalah platform pasar digital terpadu yang dirancang khusus untuk memfasilitasi pemasaran, pemesanan, dan distribusi komoditas lokal unggulan dari **20 kecamatan se-Kabupaten Tanggamus**, sekaligus menyediakan dashboard analitik dan kurasi legalitas bagi Pemerintah Daerah (Dinas Koperasi, UKM, Perindustrian, dan Perdagangan Kabupaten Tanggamus).

Nama **PasarSemaka** menggabungkan filosofi pasar digital kerakyatan dengan ikon geografis kebanggaan daerah, yaitu **Teluk Semaka** dan **Kecamatan Semaka**.

---

## 🎨 Desain & Identitas Visual Resmi

Sesuai ketentuan dokumen *Product Requirements Document (PRD)* dan perancangan *Stitch AI*:
- **Warna Utama (*Primary*)**: `#003820` / `#0F5132` (Hijau Hutan Pegunungan Tanggamus & Semaka)
- **Warna Aksen (*Secondary / Gold*)**: `#7D5700` / `#FDC254` (Emas Kehormatan & Pesisir Teluk Semaka)
- **Warna Latar (*Surface Canvas*)**: `#F8F9FF` & `#EFF4FF` (Bersih, modern, dan sejuk)
- **Tipografi**: **Plus Jakarta Sans** (Google Fonts)
- **Ikonografi**: **Material Symbols Outlined**
- **Identitas Institusi Terpadu**:
  - Badge & Lambang Resmi **Pemerintah Kabupaten Tanggamus**
  - Badge & Lambang Resmi **Universitas Teknokrat Indonesia** (Kampus Juara)
  - Logo Resmi **PasarSemaka: Produk Lokal Tanggamus**

---

## 👥 3 Peran Pengguna (*Multi-Role Persona Architecture*)

PasarSemaka mengintegrasikan tiga pemangku kepentingan utama dalam satu ekosistem terpadu:

### 1. 🛍️ Portal Pembeli (*Consumer Portal*)
- **Beranda Interaktif (`beranda.html` / `index.html`)**:
  - *Hero visual area* bernuansa perkebunan kopi lereng Gunung Tanggamus dan pesisir teluk.
  - Form pencarian cepat dengan rekomendasi pencarian populer (*Kopi Ulubelu, Keripik Pisang Muli, Madu Odeng Gisting*).
  - 6 Kategori Unggulan Komoditas Daerah dengan jumlah produk aktif.
  - Kartu produk kurasi terbaik (*Bestseller, Binaan Pemkab, Organik*).
  - *Pojok UMKM Berdaya*: Profil gerai UMKM mitra binaan terverifikasi.
  - Ajakan kolaborasi & pendaftaran pelaku UMKM desa.
- **Katalog Lengkap (`katalog.html`)**:
  - Penyaringan multi-kategori: *Kopi & Minuman, Makanan Ringan, Hasil Bumi & Madu, Olahan Ikan, Kerajinan Tapis, Herbal & Rempah*.
  - Filter wilayah berdasarkan **20 Kecamatan di Kabupaten Tanggamus**.
  - *Price Range Slider* interaktif hingga Rp 200.000+.
  - *Checkbox* khusus jaminan: "Terverifikasi Dinas" & "Hanya Stok Ready".
  - *Grid / List View Switcher*.
  - Modal detail komoditas dengan ketersediaan stok riil dan tombol beli instan.
- **Keranjang & Checkout MVP (`keranjang.html`)**:
  - Sistem pesanan *single-merchant* untuk efisiensi rantai pasok lokal antar-pekon.
  - Pengaturan kuantitas barang dengan perhitungan otomatis subtotal, estimasi ongkir kurir lokal (Rp 10.000), dan total pembayaran.
  - Form data pembeli (Nama, WhatsApp aktif, Alamat, Pilihan Kecamatan dari 20 Wilayah, Catatan Khusus).
  - Modal penyelesaian pesanan dilengkapi kode transaksi resmi (contoh: `#PSM-2026-0891`), notifikasi pengiriman ke WhatsApp seller, dan opsi bayar di tempat (COD).
- **Status & Pelacakan Pesanan (`pesanan.html`)**:
  - *Live Tracking Semaka Express*: Peta visual SVG rute distribusi pekon (*Ulubelu -> Hub Talang Padang -> Kota Agung Timur*).
  - Profil kurir lokal pekon (**Budi Santoso**, No. Pol BE 4182 ZG, rating 4.9).
  - Tombol kontak langsung via WhatsApp dan telepon driver.
  - *Milestone timeline* status pengiriman paket.

### 2. 🏪 Dashboard Pelaku UMKM (`umkm-dashboard.html`)
- **Profil Usaha & Akreditasi Legalitas**:
  - Status resmi: **TERVERIFIKASI DINAS** (NIB: `1904230048123`, P-IRT: `2101806010452-26`, Sertifikat Halal).
  - Skor kepatuhan mutu (98/100) dan jangkauan siap antar ke 12-20 kecamatan.
- **4 Metrik Operasional Utama**:
  - Total Produk Unggulan (13 produk aktif di etalase)
  - Pesanan Masuk (7 pesanan menunggu tindakan cepat)
  - Pesanan Diproses (6 pesanan sedang disiapkan/diantar)
  - Pesanan Selesai (142 transaksi sukses, omzet Rp 7.450.000)
- **Manajemen Produk (CRUD Lengkap)**:
  - Tabel produk komoditas UMKM dengan status aktif dan stok terkini.
  - Tombol modal `+ Tambah Produk Baru` (Nama produk, kategori, harga, stok, foto, deskripsi).
  - Fitur hapus dan edit produk yang tersinkronisasi ke basis data SQLite.
- **Kelola Pesanan Masuk**:
  - Rincian item pesanan pembeli (misal: Rian Hidayat, 3 bungkus kopi Robusta).
  - Tombol tindakan: Konfirmasi Pesanan, Siapkan Paket, Cetak Resi Pengiriman, dan Lacak Pengiriman Kurir.

### 3. 🏛️ Admin Dinas Koperasi & UKM (`admin-dinas.html`)
- **Panel Kurasi & Validasi Legalitas UMKM**:
  - Daftar antrean verifikasi UMKM baru dari pekon-pekon di Tanggamus.
  - Modal pemeriksaan berkas digital: legalitas NIB, P-IRT, sertifikat Halal, foto lokasi sentra produksi, dan keaslian bahan baku lokal.
  - Tindakan keputusan resmi: **Setujui & Terbitkan Izin Etalase**, **Minta Revisi Dokumen**, atau **Tolak Pendaftaran**.
- **Monitoring & Statistik Wilayah (Smart Governance)**:
  - Distribusi UMKM terdaftar di **20 Kecamatan** (Kota Agung, Semaka, Ulubelu, Gisting, Wonosobo, Talang Padang, Pulau Panggung, Pugung, dll.).
  - Komposisi komoditas daerah (*Kopi, Keripik Pisang, Hasil Laut, Madu Hutan, Kriya Tapis, Herbal Rempah*).
  - **Ekspor Laporan CSV Resmi (`/api/admin/export`)**: Menghasilkan dokumen spreadsheet `Laporan_UMKM_Tanggamus_2026.csv` siap pakai untuk rapat dinas.
  - Tombol sinkronisasi data daerah secara real-time.

---

## 🛠️ Arsitektur Teknologi & Basis Data

```
                         +-----------------------------------+
                         |   Browser Klien (Desktop / Mobile)|
                         |   Tailwind CSS + JS Controller    |
                         +-----------------+-----------------+
                                           | HTTP / REST API
                         +-----------------v-----------------+
                         |      Tornado / Python Backend     |
                         |      server.py (Port 8080)        |
                         +-----------------+-----------------+
                                           | SQLite Engine
                         +-----------------v-----------------+
                         |    Relational Database: SQLite    |
                         |         pasarsemaka.db            |
                         +-----------------------------------+
```

### Struktur Skema Basis Data Relasional (`pasarsemaka.db`):
1. `users`: Menyimpan akun dan kredensial pengguna (Buyer, UMKM, Admin Dinas).
2. `umkm_profiles`: Menyimpan profil gerai, pemilik, legalitas NIB, P-IRT, status verifikasi dinas, dan alamat pekon.
3. `categories`: 6 kategori resmi komoditas Tanggamus.
4. `products`: Katalog produk, harga, stok, foto resolusi tinggi, rating, dan status aktif.
5. `orders`: Transaksi pemesanan pembeli, total belanja, ongkir lokal, alamat antar, catatan, status pesanan, dan nomor resi.
6. `order_items`: Rincian item produk dalam setiap transaksi pesanan.
7. `reviews`: Ulasan dan rating bintang dari pembeli.
8. `admin_logs`: Rekam jejak audit aktivitas verifikasi dan kurasi petugas dinas.

---

## 🚀 Panduan Menjalankan Aplikasi

Aplikasi dibangun mandiri (*zero external dependencies setup*) menggunakan runtime Python yang telah tersedia pada sistem:

### Opsi 1: Klik Ganda Launcher Windows (Paling Praktis)
1. Buka folder `D:\PPSI\UTSPPSI` di File Explorer.
2. Klik ganda pada file **`run.bat`**.
3. Sistem akan secara otomatis mendeteksi runtime Python, menginisialisasi basis data `pasarsemaka.db`, menyalakan server lokal pada port `8080`, dan membuka peramban web (*browser*) Anda secara otomatis ke alamat `http://localhost:8080`.

### Opsi 2: Menggunakan PowerShell
```powershell
cd D:\PPSI\UTSPPSI
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

### Opsi 3: Menjalankan Langsung via Terminal
```cmd
"C:\Users\user\AppData\Local\Programs\Orange\python.exe" server.py 8080
```
Lalu buka peramban di: **`http://localhost:8080`**

### Opsi 4: Membuka File HTML Langsung (Mode Offline Tanpa Server)
Seluruh halaman HTML didesain responsif dan dapat dibuka langsung melalui protokol `file:///` di peramban apa pun:
- `D:\PPSI\UTSPPSI\index.html` atau `beranda.html` (Portal Pembeli)
- `D:\PPSI\UTSPPSI\katalog.html` (Katalog Komoditas)
- `D:\PPSI\UTSPPSI\keranjang.html` (Keranjang & Form Pemesanan)
- `D:\PPSI\UTSPPSI\pesanan.html` (Live Tracking & Status Pengiriman)
- `D:\PPSI\UTSPPSI\umkm-dashboard.html` (Dashboard Operasional UMKM)
- `D:\PPSI\UTSPPSI\admin-dinas.html` (Dashboard Kurasi & Verifikasi Dinas)

---

## 📂 Struktur Berkas Proyek

```
D:\PPSI\UTSPPSI\
├── database.py             # Engine database SQLite3, skema tabel, & data seeding
├── server.py               # REST API server & web router (Python Tornado)
├── pasarsemaka.db          # Basis data persisten SQLite3 lokal
├── run.bat                 # 1-Click Launcher untuk Windows
├── run.ps1                 # 1-Click Launcher untuk PowerShell
├── README.md               # Dokumentasi lengkap proyek PasarSemaka
├── index.html              # Halaman Beranda Utama PasarSemaka
├── beranda.html            # Portal Pembeli (Komoditas & Sentra UMKM)
├── katalog.html            # Katalog Komoditas Lokal & Filter 20 Kecamatan
├── keranjang.html          # Keranjang Belanja & Checkout Single-Merchant
├── pesanan.html            # Status Pesanan & Live Tracking Kurir Semaka Express
├── umkm-dashboard.html     # Dashboard Operasional UMKM & CRUD Produk
├── admin-dinas.html        # Dashboard Admin Dinas (Kurasi NIB & Statistik)
├── static/
│   ├── css/                # Lembar gaya kustom tambahan
│   ├── js/
│   │   └── app.js          # Pengendali logika interaktif klien, keranjang, & router
│   └── img/
│       ├── logo-pasarsemaka.svg  # Logo resmi vektor PasarSemaka
│       ├── logo-tanggamus.svg    # Logo lambang Pemkab Tanggamus
│       └── logo-teknokrat.svg    # Logo lambang Universitas Teknokrat Indonesia
└── templates/              # Salinan templat halaman web yang disajikan oleh server.py
    ├── index.html
    ├── beranda.html
    ├── katalog.html
    ├── keranjang.html
    ├── pesanan.html
    ├── umkm-dashboard.html
    └── admin-dinas.html
```

---

## 📜 Kepatuhan Terhadap Ketentuan Hak Cipta & Akademik

Sesuai instruksi PRD Bagian 14, seluruh tampilan antarmuka dan dokumentasi PasarSemaka memuat teks hak cipta resmi berikut secara konsisten:

```text
PasarSemaka
Pasar Digital Produk Lokal Kabupaten Tanggamus
Copyright © 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom.
Didukung oleh Pemerintah Kabupaten Tanggamus & Universitas Teknokrat Indonesia (Smart City Initiative)
```

