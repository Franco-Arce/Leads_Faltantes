import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import OperationalError

# Page Configuration
st.set_page_config(
    page_title="Dashboard Leads Faltantes",
    page_icon="📊",
    layout="wide"
)

# --- Helper Functions ---

def get_db_connection(config):
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            database=config["dbname"],
            user=config["user"],
            password=config["password"],
            connect_timeout=5  # Fail fast if connection is bad
        )
        return conn
    except OperationalError as e:
        raise e

def fetch_data_from_uni(uni_name, config):
    """Fetches data from a specific university's database."""
    conn = None
    try:
        conn = get_db_connection(config)
        # Filtrar solo leads de la semana actual (desde el lunes hasta hoy)
        query = """
            SELECT * FROM faltantes_neotel
        """
        df = pd.read_sql_query(query, conn)
        
        # Robust fix for Pyarrow date conversion issues
        # Converting to string is the safest way to ensure rendering
        if 'fecha' in df.columns:
            df['fecha'] = df['fecha'].astype(str)
            
        df['origen_universidad'] = uni_name
        return df, None # Success
    except Exception as e:
        return None, str(e) # Failure
    finally:
        if conn:
            conn.close()

def load_all_data():
    """Iterates through all configured universities and aggregates data."""
    all_dfs = []
    errors = []
    
    # Check if secrets are configured
    if "connections" not in st.secrets:
        st.error("No database connections found in secrets.toml")
        return pd.DataFrame()

    # Iterate over each university in secrets
    # Assuming structure: [connections.ues], [connections.cesa], etc.
    # st.secrets["connections"] returns a dictionary-like object
    
    for uni_key, config in st.secrets["connections"].items():
        # Convert key to readable name (e.g., "ues" -> "UES")
        uni_name = uni_key.upper()
        
        with st.spinner(f"Conectando a {uni_name}..."):
            df, error = fetch_data_from_uni(uni_name, config)
            
            if error:
                errors.append(f"⚠️ Error conectando a **{uni_name}**: {error}")
            elif df is not None and not df.empty:
                all_dfs.append(df)
            elif df is not None and df.empty:
                 # Handle empty table case if needed, or just ignore
                 pass

    # Display errors if any
    if errors:
        for err in errors:
            st.warning(err)

    if not all_dfs:
        return pd.DataFrame()
    
    return pd.concat(all_dfs, ignore_index=True)

# --- Main App ---

def main():
    st.title("📊 Dashboard Centralizado: Leads Faltantes")
    
    # Refresh Button
    if st.button("🔄 Refrescar Datos"):
        if 'data' in st.session_state:
            del st.session_state['data']
        st.cache_data.clear()
        st.rerun()

    # Load Data
    # We use a simple caching mechanism or just load directly since the user asked for a refresh button
    # that re-runs queries. Streamlit re-runs the script on interaction, so we just call load_all_data.
    # To make "Refrescar Datos" work effectively with caching, we would use @st.cache_data
    # But the requirement says "simply re-execute SQL queries", so we can skip cache or clear it.
    
    # Let's use session state to store data so it doesn't reload on every interaction (like changing tabs)
    # unless the user hits Refresh.
    
    if 'data' not in st.session_state:
        st.session_state.data = load_all_data()

    df_master = st.session_state.data

    # Check if we have data
    if df_master.empty:
        st.info("No hay datos disponibles o no se pudo conectar a ninguna base de datos.")
        return

    # --- KPIs Globales ---
    total_faltantes = len(df_master)
    
    if 'origen_universidad' in df_master.columns:
        top_uni = df_master['origen_universidad'].value_counts().idxmax()
        top_uni_count = df_master['origen_universidad'].value_counts().max()
    else:
        top_uni = "N/A"
        top_uni_count = 0

    col1, col2 = st.columns(2)
    col1.metric("Total Leads Faltantes", total_faltantes)
    col2.metric("Universidad con más faltantes", f"{top_uni} ({top_uni_count})")

    st.divider()

    # --- Tabs ---
    tab1, tab2 = st.tabs(["🌎 Vista Global", "📈 Desglose por Universidad"])

    with tab1:
        st.subheader("Listado Completo de Leads")
        
        # Sidebar Filters
        st.sidebar.header("Filtros")
        unis_available = df_master['origen_universidad'].unique()
        selected_unis = st.sidebar.multiselect(
            "Filtrar por Universidad", 
            options=unis_available,
            default=unis_available
        )
        
        # Filter Logic
        if selected_unis:
            df_filtered = df_master[df_master['origen_universidad'].isin(selected_unis)]
        else:
            df_filtered = df_master

        st.dataframe(df_filtered, use_container_width=True)

    with tab2:
        st.subheader("Comparativa por Universidad")
        
        if not df_master.empty:
            counts = df_master['origen_universidad'].value_counts().reset_index()
            counts.columns = ['Universidad', 'Cantidad']
            
            st.bar_chart(counts, x='Universidad', y='Cantidad', color='Universidad')
        else:
            st.write("No hay datos para graficar.")

if __name__ == "__main__":
    # Logic to handle the "Refresh" button clearing state
    # The button inside main() sets a flag, but since we check session_state at the start,
    # we need to ensure the button press triggers a reload.
    # Actually, the button returns True once. We can handle it inside main or here.
    # Simplified: The button in main() clears cache/state and reruns.
    main()
