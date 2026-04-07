import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ====================== APP SETUP ======================
st.set_page_config(page_title="Model Monitoring Report", layout="wide")
st.title("Model Monitoring Report")

# ====================== FILE UPLOAD (EXCEL) ======================
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Load entire Excel file
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
    except ImportError:
        st.error("❌ Missing required package: **openpyxl**\n\n"
                 "Please run this command in your terminal and restart the app:\n\n"
                 "`pip install openpyxl`")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {e}")
        st.stop()

    # Create one tab per Excel sheet
    tabs = st.tabs(sheet_names)

    # ====================== PROCESS EACH SHEET ======================
    for idx, tab_name in enumerate(sheet_names):
        with tabs[idx]:
            st.subheader(f"**{tab_name}**")

            # Read current sheet
            df = pd.read_excel(uploaded_file, sheet_name=tab_name, engine="openpyxl")

            # ====================== AUTO-DETECT QUARTER ======================
            # Detect quarter name from any column header (e.g., 2025Q3)
            original_quarter_name = "2025Q3"
            for col in df.columns:
                if "2025" in str(col).upper() and "Q3" in str(col).upper():
                    original_quarter_name = str(col).strip().upper().replace("_", "")
                    break

            # Collapsible raw data preview (hidden by default for clean PDF export)
            with st.expander("Uploaded Data Preview", expanded=False):
                st.dataframe(df, use_container_width=True, hide_index=True)

            # ====================== DATA CLEANING ======================
            # Clean column names: remove spaces, make lowercase
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

            # Find the cleaned quarter column (e.g., 2025q3)
            quarter_col = next((col for col in df.columns if "2025" in col and "q3" in col), None)
            if quarter_col is None:
                st.error(f"Could not detect 2025Q3 column in sheet '{tab_name}'")
                st.stop()

            # Identify metric column (first column or 'metric')
            metric_col = 'metric' if 'metric' in df.columns else df.columns[0]
            df[metric_col] = df[metric_col].astype(str).str.strip().str.lower()

            # Create raw dictionary: metric → value
            raw_dict = dict(zip(df[metric_col], df[quarter_col]))

            # ====================== STANDARDIZE METRICS ======================
            # Map raw metric names to standard keys used in tables
            data_dict = {}
            for k, v in raw_dict.items():
                k_clean = str(k).lower().strip()
                if "gini" in k_clean:           data_dict["gini"] = float(v) if pd.notna(v) else 0.0
                elif "ks" in k_clean:           data_dict["ks"] = float(v) if pd.notna(v) else 0.0
                elif "accuracy" in k_clean:     data_dict["accuracy"] = float(v) if pd.notna(v) else 0.0
                elif k_clean == "psi" or "population stability" in k_clean: 
                    data_dict["psi"] = float(v) if pd.notna(v) else 0.0
                elif "input psi" in k_clean or "input stability" in k_clean: 
                    data_dict["input psi"] = float(v) if pd.notna(v) else 0.0
                elif "override" in k_clean:     data_dict["overrides"] = float(v) if pd.notna(v) else 0.0
                elif "balance" in k_clean or "exposure" in k_clean:
                    data_dict["balance/exposure"] = str(v).strip()   # Keep exact text from Excel

            # ====================== TABLE 1: MODEL ATTRIBUTE ======================
            st.subheader("Model Attribute")
            table1 = pd.DataFrame({
                "Model Type": ["Dual Risk Rating"],
                "Model ID": ["M-2022"],
                "Model Component": ["PD"],
                "Balance/Exposure": [data_dict.get("balance/exposure", "N/A")],
                "Tier": ["Tier 3"],
                "Model Owner": ["Vivek Ambastha"],
                "Business Segment/Coverage": ["GFB"],
                "Purpose": ["Model used for rating"]
            })
            st.table(table1)   # Plain table - no styling, no green tint

            # ====================== TABLE 2: PERFORMANCE MONITORING ======================
            st.subheader(f"Ongoing Performance Monitoring - {original_quarter_name}")
            
            table2 = pd.DataFrame({
                "Metric Name": ["Accuracy", "GINI", "KS", "PSI", "OVERRIDES", "Input PSI"],
                "Soft Threshold": [0.06, 0.40, 0.40, 0.10, None, None],
                "Hard Threshold": [0.08, 0.20, 0.20, 0.25, 0.05, 0.00],
                original_quarter_name: [data_dict.get("accuracy", 0.0), data_dict.get("gini", 0.0),
                                        data_dict.get("ks", 0.0), data_dict.get("psi", 0.0),
                                        data_dict.get("overrides", 0.0), data_dict.get("input psi", 0.0)]
            })

            # Calculate breach status for each metric
            status_list = []
            breach_count = {"No Breach": 0, "Soft Breach": 0, "Hard Breach": 0}
            for _, row in table2.iterrows():
                val = row[original_quarter_name]
                soft = row["Soft Threshold"]
                hard = row["Hard Threshold"]
                status = "Hard Breach" if pd.notnull(hard) and val > hard else \
                         "Soft Breach" if pd.notnull(soft) and val > soft else "No Breach"
                status_list.append(status)
                breach_count[status] += 1

            table2["Status"] = status_list

            # Color coding for Status column
            def highlight_status(row):
                if row["Status"] == "Hard Breach":    return ["background-color: #ffcccc; color: red; font-weight: bold"] * len(row)
                elif row["Status"] == "Soft Breach":  return ["background-color: #ffe6cc; color: orange; font-weight: bold"] * len(row)
                else:                                 return ["background-color: #ccffcc; color: green; font-weight: bold"] * len(row)

            styled_table2 = table2.style.apply(highlight_status, axis=1).set_table_styles([
                {'selector': 'thead th', 'props': [('font-weight','bold'),('background-color','#f0f2f6'),('border','1px solid #999'),('text-align','center'),('padding','10px')]},
                {'selector': 'tbody td', 'props': [('border','1px solid #999'),('text-align','center'),('padding','10px')]},
                {'selector': 'table', 'props': [('border-collapse','collapse'),('width','100%')]}
            ])
            st.table(styled_table2)

            # ====================== RESULT SUMMARY + CHART ======================
            st.subheader("Result Summary")

            fig, ax = plt.subplots(figsize=(3.8, 2.0))
            colors = ["#4CAF50", '#FF9800', '#F44336']
            ax.bar(breach_count.keys(), breach_count.values(), color=colors)
            ax.set_title(f"Breach Summary - {original_quarter_name}", fontsize=11, pad=10)
            ax.set_ylabel("Number of Metrics", fontsize=9)
            ax.tick_params(axis='both', labelsize=9)
            ax.set_ylim(0, max(breach_count.values()) + 1)
            
            for i, v in enumerate(breach_count.values()):
                ax.text(i, v + 0.08, str(v), ha='center', fontsize=10)

            st.pyplot(fig, use_container_width=False)

            # ====================== KEY OBSERVATIONS ======================
            soft_text = ", ".join(table2[table2["Status"] == "Soft Breach"]["Metric Name"].tolist()) or "None"
            hard_text = ", ".join(table2[table2["Status"] == "Hard Breach"]["Metric Name"].tolist()) or "None"
            no_text   = ", ".join(table2[table2["Status"] == "No Breach"]["Metric Name"].tolist()) or "None"

            st.markdown("#### Key Observations")
            summary_text = f"""
For the **GFB** portfolio we observed **Soft Breach** for **{soft_text}** and **Hard Breach** for **{hard_text}**.  
The **{no_text}** metrics do not show any breaches.  

The CCLOC risk rating template was originally developed as a qualitative scorecard with categorical data. 
Also, this portfolio segment has a very low rate of actual default that comes in significantly lower than the predicted default embedded in the risk ratings.
"""
            st.markdown(summary_text)
