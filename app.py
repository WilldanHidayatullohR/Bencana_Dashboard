from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Bencana Indonesia 2023–2024", layout="wide")

# =========================
# Config: file paths (OPTION 2)
# =========================
DATA_DIR = Path("data")
FILE_2023 = DATA_DIR / "Data_2023.xlsx"
FILE_2024 = DATA_DIR / "Data_2024.xlsx"

# =========================
# Helpers
# =========================
EXPECTED_COLS = [
    "Kode_Provinsi",
    "Provinsi",
    "Jumlah_Kejadian",
    "Meninggal_Hilang",
    "Luka_Luka",
    "Mengungsi_Terdampak",
    "Rumah_Rusak_Berat",
    "Rumah_Rusak_Sedang",
    "Rumah_Rusak_Ringan",
    "Rumah_Terendam",
    "Fasilitas_Pendidikan",
    "Fasilitas_Peribadatan",
    "Fasilitas_Kesehatan",
]
NUM_COLS = [c for c in EXPECTED_COLS if c not in ["Kode_Provinsi", "Provinsi"]]


def _to_number(x):
    if pd.isna(x):
        return 0
    if isinstance(x, str):
        s = x.strip()
        if s in ["-", "—", "–", ""]:
            return 0
        s = s.replace(",", "")
        try:
            return float(s)
        except ValueError:
            return 0
    try:
        return float(x)
    except Exception:
        return 0


def extract_province_section(df_raw: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Extract the 'Kode Wilayah Provinsi' section and normalize columns.
    Works for the BNPB-style recap sheets you showed earlier.
    """
    first_col = df_raw.columns[0]

    marker_idx = df_raw.index[
        df_raw[first_col].astype(str).str.contains("Kode Wilayah Provinsi", na=False)
    ]

    if len(marker_idx) == 0:
        # fallback: search any cell
        marker_idx = df_raw.index[
            df_raw.astype(str).apply(
                lambda r: r.str.contains("Kode Wilayah Provinsi", na=False).any(),
                axis=1,
            )
        ]

    if len(marker_idx) == 0:
        raise ValueError(
            "Tidak menemukan bagian 'Kode Wilayah Provinsi'. Struktur file berbeda dari yang diharapkan."
        )

    marker_idx = int(marker_idx[0])
    df = df_raw.iloc[marker_idx + 1 :].copy()

    # Keep first 13 columns for the section
    df = df.iloc[:, :13].copy()
    df.columns = EXPECTED_COLS

    # Drop rows without province code/name
    df = df.dropna(subset=["Kode_Provinsi", "Provinsi"], how="any").copy()

    # Remove placeholder codes (-1, -2, ...)
    df = df[~df["Kode_Provinsi"].astype(str).str.startswith("-")].copy()

    # Clean text
    df["Kode_Provinsi"] = df["Kode_Provinsi"].apply(
        lambda x: str(int(x)) if str(x).strip().isdigit() else str(x).strip()
    )
    df["Provinsi"] = df["Provinsi"].astype(str).str.strip().str.title()

    # Numeric conversion
    for c in NUM_COLS:
        df[c] = df[c].apply(_to_number).astype(float)

    df["Tahun"] = int(year)

    # Convenience totals (optional)
    df["Total_Dampak_Indikator"] = (
        df["Jumlah_Kejadian"]
        + df["Meninggal_Hilang"]
        + df["Luka_Luka"]
        + df["Mengungsi_Terdampak"]
        + df["Rumah_Rusak_Berat"]
        + df["Rumah_Rusak_Sedang"]
        + df["Rumah_Rusak_Ringan"]
    )

    return df


@st.cache_data(show_spinner=False)
def load_from_excel(path: Path, year: int) -> pd.DataFrame:
    df_raw = pd.read_excel(path)
    return extract_province_section(df_raw, year)


# =========================
# App
# =========================
st.title("Dashboard Rekap Bencana Indonesia (Per Provinsi) — 2023 & 2024")

# Validate files exist
missing = [str(p) for p in [FILE_2023, FILE_2024] if not p.exists()]
if missing:
    st.error(
        "File data tidak ditemukan.\n\n"
        "Pastikan struktur folder seperti ini:\n"
        "bencana-dashboard/\n"
        "├── app.py\n"
        "├── requirements.txt\n"
        "└── data/\n"
        "    ├── Data_2023.xlsx\n"
        "    └── Data_2024.xlsx\n\n"
        f"Yang tidak ditemukan: {', '.join(missing)}"
    )
    st.stop()

# Load data
try:
    df23 = load_from_excel(FILE_2023, 2023)
    df24 = load_from_excel(FILE_2024, 2024)
except Exception as e:
    st.error(f"Gagal membaca/merapikan data: {e}")
    st.stop()

df = pd.concat([df23, df24], ignore_index=True)

# =========================
# Sidebar controls
# =========================
with st.sidebar:
    st.header("Filter")
    years = sorted(df["Tahun"].unique().tolist())
    year_sel = st.multiselect("Tahun", years, default=years)  # default: 2023+2024 (gabungan)

    provs = sorted(df["Provinsi"].unique().tolist())
    prov_sel = st.multiselect("Provinsi", provs, default=[])

    st.divider()
    st.header("Visual Settings")
    metric = st.selectbox(
        "Metric utama",
        options=[
            "Jumlah_Kejadian",
            "Meninggal_Hilang",
            "Luka_Luka",
            "Mengungsi_Terdampak",
            "Rumah_Rusak_Berat",
            "Rumah_Rusak_Sedang",
            "Rumah_Rusak_Ringan",
            "Rumah_Terendam",
            "Fasilitas_Pendidikan",
            "Fasilitas_Peribadatan",
            "Fasilitas_Kesehatan",
        ],
        index=0,
    )
    top_n = st.slider("Top N Provinsi", min_value=5, max_value=38, value=15, step=1)

# Apply filters
df_f = df[df["Tahun"].isin(year_sel)].copy()
if prov_sel:
    df_f = df_f[df_f["Provinsi"].isin(prov_sel)].copy()

# =========================
# KPI row
# =========================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Jumlah Provinsi", f"{df_f['Provinsi'].nunique():,.0f}")
c2.metric("Total Kejadian", f"{df_f['Jumlah_Kejadian'].sum():,.0f}")
c3.metric("Meninggal & Hilang", f"{df_f['Meninggal_Hilang'].sum():,.0f}")
c4.metric("Mengungsi & Terdampak", f"{df_f['Mengungsi_Terdampak'].sum():,.0f}")

st.divider()

# =========================
# Charts
# =========================
left, right = st.columns(2)

# Top N provinces by selected metric (aggregated across selected years)
top_df = (
    df_f.groupby("Provinsi", as_index=False)[metric]
    .sum()
    .sort_values(metric, ascending=False)
    .head(top_n)
)

fig_top = px.bar(
    top_df,
    x=metric,
    y="Provinsi",
    orientation="h",
    title=f"Top {top_n} Provinsi berdasarkan {metric.replace('_', ' ')} (Tahun: {', '.join(map(str, year_sel))})",
)
fig_top.update_layout(yaxis={"categoryorder": "total ascending"})
left.plotly_chart(fig_top, use_container_width=True)

# Year comparison for top provinces
cmp_df = (
    df_f[df_f["Provinsi"].isin(top_df["Provinsi"])]
    .groupby(["Tahun", "Provinsi"], as_index=False)[metric]
    .sum()
)

fig_cmp = px.bar(
    cmp_df,
    x="Provinsi",
    y=metric,
    color="Tahun",
    barmode="group",
    title=f"Perbandingan {metric.replace('_', ' ')} per Provinsi (2023 vs 2024) — Top {top_n}",
)
right.plotly_chart(fig_cmp, use_container_width=True)

st.divider()

# Table preview
with st.expander("Preview data (setelah cleaning)"):
    show_cols = ["Tahun", "Kode_Provinsi", "Provinsi"] + NUM_COLS
    st.dataframe(
        df_f.sort_values(["Tahun", "Provinsi"])[show_cols],
        use_container_width=True,
        height=420,
    )

st.caption(
    "Sumber data: rekap bencana per provinsi. Aplikasi mengekstrak bagian 'Kode Wilayah Provinsi' dari file Excel, "
    "lalu menstandarkan kolom untuk analisis 2023–2024."
)