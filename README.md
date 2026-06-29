# Cell 2: Define paths and load data

db_path = r"C:/Users/02. Data Prep/04. IDBSD Handover/PD Pipeline Handover"
master_db_path = "02. Data/01. Master Database/outputs/20260618 1349 Final Modeling Dataset V1.parquet"
support_path = "model_development/segmentation_analysis/data/Support/06222026_variable transformations python.xlsx"
export_path = "model_development/segmentation_analysis/data/Outputs"

# Load main data
df = pd.read_parquet(os.path.join(db_path, master_db_path))
print(f"Loaded data shape: {df.shape}")

print("Paths and data loaded successfully!")