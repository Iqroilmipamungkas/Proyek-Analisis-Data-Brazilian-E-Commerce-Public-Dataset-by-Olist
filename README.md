# Submission Dicoding "Belajar Data Analytics dengan Python"
## Proyek Analisis Data
Repository ini berisi proyek analisis data yang saya kerjakan untuk menghasilkan dahsboard  hasil analisis data dengan menggunakan **Streamlit** <img src="https://seeklogo.com/images/S/streamlit-logo-1A3B208AE4-seeklogo.com.png" alt="Streamlit Logo" width="60"></img>

## Deskripsi
Proyek ini bertujuan untuk menganalisis data pada **Brazilian E-Commerce Public Dataset by Olist**. Tujuan akhir proyek ini adalah untuk mendapatkan wawasan dan informasi yang berguna dari hasil analisis data.

## Struktur Direktori
- **/Dashboard**: Direktori ini berisi dashboard.py yang digunakan untuk membuat dashboard hasil analisis data.
- **/Data**: Direktori ini berisi data yang digunakan dalam proyek dengan format .csv 
- **Notebook.ipynb**: File yang digunakan untuk melakukan analisis data.

## Setup environment
```
conda create --name main-ds python=3.11
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
```
## Run steamlit app: Menampilkan dashboard
```
streamlit run dashboard.py                           
```
