# 📊 Dashboard Visualisasi Bencana Alam Indonesia (2023–2024)

## Deskripsi Proyek
Proyek ini merupakan bagian dari **Ujian Akhir Semester (UAS)** mata kuliah **Visualisasi Data dan Informasi**.  
Aplikasi ini menyajikan **dashboard interaktif** untuk menganalisis data **bencana alam di Indonesia** berdasarkan **provinsi** dan **tahun (2023–2024)**.

Dashboard dibangun menggunakan **Python** dengan framework **Streamlit** dan visualisasi berbasis **Plotly**, sehingga pengguna dapat melakukan eksplorasi data secara dinamis melalui filter dan grafik interaktif.

---

## Tujuan
- Menyajikan rekapitulasi kejadian bencana alam per provinsi  
- Membandingkan data bencana antar tahun (2023 dan 2024)  
- Menyediakan visualisasi data yang informatif dan interaktif  
- Mendukung analisis data berbasis dashboard web  

---

## Fitur Utama
- Filter tahun (2023, 2024, atau gabungan)  
- Filter provinsi  
- KPI ringkas (jumlah provinsi, total kejadian, korban, dan terdampak)  
- Grafik Top N provinsi berdasarkan indikator bencana  
- Grafik perbandingan data tahun 2023 dan 2024  
- Preview data hasil pembersihan (data cleaning)  

---

## Teknologi yang Digunakan
- Python  
- Streamlit  
- Pandas  
- Plotly Express  
- OpenPyXL  

---

## Struktur Folder
```
bencana-dashboard/
├── app.py
├── README.md
├── requirements.txt
└── data/
    ├── Data_2023.xlsx
    └── Data_2024.xlsx
```

---

## Cara Menjalankan Aplikasi

### Install Dependensi
```bash
pip install -r requirements.txt
```

### Jalankan Aplikasi
```bash
streamlit run app.py
```

---

## Identitas Kelompok

**Kelompok 4 – Visualisasi Data dan Informasi**

| NIM | Nama |
|----|------|
| 220660121083 | Amanda Listiana Puspanagara |
| 220660121019 | Rifki Septiana Rizki |
| 220660121024 | Anjelina Mentari Rustandi |
| 220660121125 | Wildan Hidayatulloh |

---

## Catatan
Dashboard ini dikembangkan untuk keperluan akademik dan dapat dikembangkan lebih lanjut sesuai kebutuhan analisis data.
