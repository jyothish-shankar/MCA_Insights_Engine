#!/usr/bin/env python
# coding: utf-8

# In[39]:


import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="MCA Insights Engine",
    page_icon="📊",
    layout="wide",
)

# --- Data Loading and Cleaning ---
@st.cache_data
def load_data():
    """Loads and cleans all datasets properly."""
    try:
        # ✅ Load CSV files
        master_df = pd.read_csv(
            r"C:\Users\jyoth\Downloads\Master_data\mca_master.csv",
            encoding='latin1',
            low_memory=False
        )
        change_log_df = pd.read_csv(
            r"C:\Users\jyoth\Downloads\Master_data\log.csv",
            encoding='latin1'
        )
        enriched_df = pd.read_csv(
            r"C:\Users\jyoth\Downloads\Master_data\Enriched.csv",
            encoding='latin1',
            header=0  # ✅ actual headers in first row
        )

        # ✅ Clean column names
        for df in [master_df, change_log_df, enriched_df]:
            df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()

        # ✅ Parse registration date
        if 'registration_date' in master_df.columns:
            master_df['registration_date'] = pd.to_datetime(
                master_df['registration_date'], format='%d-%b-%Y', errors='coerce'
            )

        return master_df, change_log_df, enriched_df

    except FileNotFoundError as e:
        st.error(f"❌ File not found: {e}")
        return None, None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None, None, None


# --- Main App Execution ---
master_df, change_log_df, enriched_df = load_data()

if master_df is not None:
    st.title("📊 MCA Insights Engine Dashboard")
    st.markdown("An interactive interface to search, filter, and visualize corporate data.")

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filter Companies")
    search_term = st.sidebar.text_input("Search by CIN or Company Name")

    # --- Ensure consistent CIN column ---
    for df in [master_df, change_log_df, enriched_df]:
        if 'cin' not in df.columns:
            possible_cols = [c for c in df.columns if 'cin' in c.lower()]
            if possible_cols:
                df.rename(columns={possible_cols[0]: 'cin'}, inplace=True)
            else:
                df['cin'] = None

    # --- Sidebar filters ---
    state_col = 'state_code' if 'state_code' in master_df.columns else None
    status_col = 'status' if 'status' in master_df.columns else None

    states = sorted(master_df[state_col].dropna().unique()) if state_col else []
    statuses = sorted(master_df[status_col].dropna().unique()) if status_col else []

    selected_state = st.sidebar.selectbox("State", ["All"] + states) if states else "All"
    selected_status = st.sidebar.selectbox("Company Status", ["All"] + statuses) if statuses else "All"

    # --- Filtering Logic ---
    filtered_df = master_df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df['cin'].astype(str).str.contains(search_term, case=False, na=False) |
            filtered_df['company_name'].astype(str).str.contains(search_term, case=False, na=False)
        ]
    if selected_state != "All" and state_col:
        filtered_df = filtered_df[filtered_df[state_col] == selected_state]
    if selected_status != "All" and status_col:
        filtered_df = filtered_df[filtered_df[status_col] == selected_status]

    # --- Display Filtered Companies ---
    st.header("🏢 Company Directory")
    st.write(f"Displaying **{len(filtered_df)}** of **{len(master_df)}** companies.")
    st.dataframe(filtered_df, use_container_width=True)
    # --- Display Filtered Data (Paginated & Limited) ---
    st.header("🏢 Company Directory")

    if filtered_df.empty:
        st.warning("No companies match your filters.")
    else:
        st.write(f"Displaying {len(filtered_df)} of {len(master_df)} total companies.")

    rows_per_page = 500
    total_pages = max(1, (len(filtered_df) // rows_per_page) + 1)
    page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)

    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    st.dataframe(filtered_df.iloc[start:end], use_container_width=True)   

    # --- Detailed Company Info ---
    if not filtered_df.empty:
        st.header("📄 Detailed Company Information")
        selected_cin = st.selectbox("Select a CIN to view details", filtered_df['cin'].unique())
 
        if selected_cin:
            col1, col2 = st.columns(2)

            # --- Left Column: Enriched Data ---
            with col1:
                st.subheader("🏢 Enriched Data")
                enriched_info = enriched_df[enriched_df['cin'] == selected_cin]

                if not enriched_info.empty:
                    directors = enriched_info[enriched_info['field'].str.lower() == 'director_name']['value'].tolist() \
                        if 'field' in enriched_info.columns and 'value' in enriched_info.columns else []

                    address_row = enriched_info[
                        enriched_info['field'].str.lower().str.contains('registered_address', na=False)
                    ] if 'field' in enriched_info.columns else pd.DataFrame()

                    address = address_row['value'].iloc[0] if not address_row.empty and 'value' in address_row.columns else "Not available"

                    st.markdown(f"**Registered Address:** {address}")
                    st.markdown("**Directors:**")
                    if directors:
                        for director in directors:
                            st.markdown(f"- {director}")
                    else:
                        st.info("No director data available.")
                else:
                    st.info("No enriched data found for this company.")

            # --- Right Column: Change History ---
            with col2:
                st.subheader("📅 Change History")
                if 'cin' in change_log_df.columns:
                    change_history = change_log_df[change_log_df['cin'] == selected_cin]
                    if not change_history.empty:
                        st.dataframe(change_history)
                        if 'change_type' not in change_history.columns:
                            change_history['change_type'] = 'Data Logged'
                        if 'date' not in change_history.columns:
                            change_history['date'] = pd.Timestamp.now()

                        # --- Timeline Visualization ---
                        fig = px.timeline(
                            change_history,
                            x_start="date",
                            x_end="date",
                            y="change_type",
                            color="change_type",
                            title=f"Timeline of Changes for {selected_cin}"
                        )
                        fig.update_yaxes(categoryorder="total ascending")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No change history found for this company.")
                else:
                    st.warning("Change log has no 'cin' column.")
    else:
        st.warning("No companies match the selected filters.")
else:
    st.error("❌ Could not load data. Please check your file paths and formats.")


# In[ ]:


get_ipython().system('jupyter nbconvert --to script Streamlitd2.ipynb')


# In[ ]:





# In[ ]:




