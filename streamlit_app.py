import streamlit as st
from quakefeeds import QuakeFeed
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone
import numpy as np

PR_BBOX = {"lat_min": 17.6, "lat_max": 19.0, "lon_min": -67.9, "lon_max": -65.0}

SEVERITY_OPTIONS = {
    "todos": "all",
    "significativo": "significant",
    "4.5": "4.5",
    "2.5": "2.5",
    "1.0": "1.0",
}

PERIOD_OPTIONS = {"mes": "month", "semana": "week", "día": "day"}

PR_SIZE_FACTOR = 0.04
WORLD_SIZE_FACTOR = 0.04

MESES_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

def formato_fecha_dia(dt):
    if pd.isna(dt) or dt is None:
        return ""
    if isinstance(dt, str):
        try:
            dt = pd.to_datetime(dt)
        except Exception:
            return dt
    try:
        return f"{int(dt.day)} de {MESES_ES[int(dt.month) - 1]} de {int(dt.year)}"
    except Exception:
        return str(dt)

def clasificacion_mag(mag):
    if pd.isna(mag):
        return "desconocido"
    try:
        m = float(mag)
    except Exception:
        return "desconocido"

    if m < 2:
        return "micro"
    if 2 <= m <= 3.9:
        return "menor"
    if 4 <= m <= 4.9:
        return "ligero"
    if 5 <= m <= 5.9:
        return "moderado"
    if 6 <= m <= 6.9:
        return "fuerte"
    if 7 <= m <= 7.9:
        return "mayor"
    if 8 <= m <= 9.9:
        return "épico"
    if m >= 10:
        return "legendario"
    return "desconocido"

@st.cache_data(ttl=300)
def obtener_feed(severity_feed_key: str, period_feed_key: str):
    feed = QuakeFeed(severity_feed_key, period_feed_key)
    rows = []
    for i in range(len(feed)):
        event = feed[i]
        props = event.get("properties", {})
        coords = event.get("geometry", {}).get("coordinates", [None, None, None])
        lon = coords[0] if len(coords) > 0 else None
        lat = coords[1] if len(coords) > 1 else None
        depth = coords[2] if len(coords) > 2 else None

        t_ms = props.get("time")
        try:
            time_dt = datetime.fromtimestamp(int(t_ms) / 1000.0, tz=timezone.utc) if t_ms is not None else None
        except Exception:
            time_dt = None

        rows.append({
            "time": time_dt,
            "place": props.get("place", props.get("title", "")),
            "latitude": lat,
            "longitude": lon,
            "depth_km": depth,
            "magnitude": props.get("mag"),
            "url": props.get("url", ""),
        })

    df = pd.DataFrame(rows)
    df["clasificacion"] = df["magnitude"].apply(clasificacion_mag)
    if "time" in df.columns:
        df = df.sort_values("time", ascending=False).reset_index(drop=True)
    return df, feed

st.set_page_config(layout="wide", page_title="Terremotos - Puerto Rico y Mundo")

with st.sidebar:
    st.header("Severidad")
    sev_label = st.selectbox("Selecciona severidad", list(SEVERITY_OPTIONS.keys()), index=0)
    severity = SEVERITY_OPTIONS[sev_label]

    st.markdown("---")
    st.header("Periodo")
    per_label = st.selectbox("Selecciona periodo", list(PERIOD_OPTIONS.keys()), index=0)
    period = PERIOD_OPTIONS[per_label]

    st.markdown("---")
    st.header("Zona Geográfica")
    zone = st.selectbox("Selecciona zona", ["Puerto Rico", "Mundo"], index=0)

    st.markdown("---")
    show_map = st.checkbox("Mostrar mapa", value=True)

    st.write("")
    st.markdown("---")
    show_table_checkbox = st.checkbox("Mostrar tabla con 5 eventos", value=False)
    num_events_for_table = st.slider("Cantidad de eventos", 5, 20, 5) if show_table_checkbox else None

    st.markdown("---")
    st.markdown("Aplicación desarrollada por:")
    st.markdown("David Santana")
    st.markdown("INGE3016")
    st.markdown("Universidad de Puerto Rico, Recinto de Humacao")

with st.spinner("Obteniendo datos del feed..."):
    try:
        df, feed = obtener_feed(severity, period)
        request_time = getattr(feed, "time", None)
    except Exception as e:
        st.error(f"No se pudo obtener el feed: {e}")
        st.stop()

if zone == "Puerto Rico":
    df_zone = df[
        (df["latitude"].notna()) &
        (df["longitude"].notna()) &
        (df["latitude"] >= PR_BBOX["lat_min"]) &
        (df["latitude"] <= PR_BBOX["lat_max"]) &
        (df["longitude"] >= PR_BBOX["lon_min"]) &
        (df["longitude"] <= PR_BBOX["lon_max"])
    ].reset_index(drop=True)
else:
    df_zone = df.copy()

st.markdown("<h2 style='text-align: center; white-space: nowrap;'>Datos en Tiempo Real de los Terremotos en Puerto Rico y el Mundo</h2>", unsafe_allow_html=True)
st.markdown("---")

fecha_text = formato_fecha_dia(request_time)
cantidad_eventos = len(df_zone)

mag_series = pd.to_numeric(df_zone["magnitude"], errors="coerce").dropna()
depth_series = pd.to_numeric(df_zone["depth_km"], errors="coerce").dropna()

avg_mag = mag_series.mean() if not mag_series.empty else np.nan
avg_depth = depth_series.mean() if not depth_series.empty else np.nan

avg_mag_str = f"{avg_mag:.2f}" if not np.isnan(avg_mag) else "N/A"
avg_depth_str = f"{avg_depth:.2f} km" if not np.isnan(avg_depth) else "N/A"

stacked_style = (
    "display:flex;flex-direction:column;align-items:center;justify-content:center;"
    "gap:6px;text-align:center;font-size:14px;color:#DDDDDD;padding:6px;"
)
stacked_html = (
    f"<div style='{stacked_style}'>"
    f"<div><strong>Fecha de petición</strong><br>{fecha_text}</div>"
    f"<div><strong>Cantidad de eventos</strong><br>{cantidad_eventos}</div>"
    f"<div><strong>Promedios</strong><br>Magnitud: {avg_mag_str} — Profundidad: {avg_depth_str}</div>"
    f"</div>"
)
st.markdown(stacked_html, unsafe_allow_html=True)

st.markdown("---")
st.subheader("Tabla de Eventos")

df_display = df_zone.copy()
df_display["time"] = df_display["time"].apply(lambda x: formato_fecha_dia(x) if pd.notnull(x) else "")

cols = [c for c in ["time", "place", "magnitude", "clasificacion"] if c in df_display.columns]
rename_map = {"time": "Fecha", "place": "Localización", "magnitude": "Magnitud", "clasificacion": "Clasificación"}

table_to_show = df_display[cols].rename(columns=rename_map).reset_index(drop=True)

if show_table_checkbox and num_events_for_table is not None:
    st.table(table_to_show.head(num_events_for_table))
else:
    st.dataframe(table_to_show.head(2000), height=300)

if show_map:
    map_df = df_zone.copy()
    map_df["time_str"] = map_df["time"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if pd.notnull(x) else "")
    map_df["magnitude"] = pd.to_numeric(map_df["magnitude"], errors="coerce")

    size_base = map_df["magnitude"].fillna(0.0).clip(lower=0.0)
    base_factor = 2.0

    if zone == "Mundo":
        size_factor = base_factor * float(WORLD_SIZE_FACTOR)
        default_zoom, size_max, sizemin_value = 1, 6, 0.5
    else:
        size_factor = base_factor * float(PR_SIZE_FACTOR)
        default_zoom, size_max, sizemin_value = 7, 10, 1

    map_df["size_plot"] = ((size_base + 0.1) * size_factor).clip(lower=0.5, upper=size_max)
    common_height = 520

    fig_mag = px.histogram(map_df, x="magnitude", nbins=30, color_discrete_sequence=["crimson"],
                           title="Histograma de Magnitudes")
    fig_mag.update_layout(yaxis_title="conteo", xaxis_title="magnitud", height=common_height,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

    fig_depth = px.histogram(map_df, x="depth_km", nbins=30, color_discrete_sequence=["darkred"],
                             title="Histograma de Profundidades")
    fig_depth.update_layout(yaxis_title="conteo", xaxis_title="profundidad (km)", height=common_height,
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

    fig_map = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        color="magnitude",
        size="size_plot",
        color_continuous_scale="Turbo",
        size_max=size_max,
        zoom=default_zoom,
        hover_name="place",
        hover_data={"magnitude": True, "depth_km": True, "clasificacion": True, "time_str": True},
        height=common_height,
    )
    fig_map.update_traces(marker=dict(sizemode="area", sizemin=sizemin_value))
    fig_map.update_layout(
        mapbox_style="carto-darkmatter",
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(title="magnitud"),
        title=dict(text="Mapa de Terremotos", x=0.5),
    )

    col_a, col_b, col_c = st.columns([1, 1, 1.6], gap="large")
    with col_a:
        st.plotly_chart(fig_mag, use_container_width=True)
    with col_b:
        st.plotly_chart(fig_depth, use_container_width=True)
    with col_c:
        st.plotly_chart(fig_map, use_container_width=True)