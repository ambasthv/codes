this is the path configuration, and it lodaed the data correctly.
# Cell 2: Define paths and load data

db_path = r"C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Outputs"
master_db_path = "C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Outputs/20260622_imp_df_seg_20260618 1349 Final Modeling Dataset V1.parquet"
support_path = "C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Support/006222026_variable transformations python.xlsx"
export_path = "C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Outputs"

# Load main data
df = pd.read_parquet(os.path.join(db_path, master_db_path))
print(f"Loaded data shape: {df.shape}")

print("Paths and data loaded successfully!")
below that in next cell i have read the data code but it is giving error, 

# load master db modeling dataset
master_db = pd.read_parquet(rf"{db_path}/{master_db_path}")
# load variable cleaning excels
cleaning_excels = read_cleaning_xlsx(f"{support_path}")

error is 
FileNotFoundError                         Traceback (most recent call last)
Cell In[6], line 2
      1 # load master db modeling dataset
----> 2 master_db = pd.read_parquet(rf"{db_path}/{master_db_path}")
      3 # load variable cleaning excels
      4 cleaning_excels = read_cleaning_xlsx(f"{support_path}")

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\parquet.py:667, in read_parquet(path, engine, columns, storage_options, use_nullable_dtypes, dtype_backend, filesystem, filters, **kwargs)
    664     use_nullable_dtypes = False
    665 check_dtype_backend(dtype_backend)
--> 667 return impl.read(
    668     path,
    669     columns=columns,
    670     filters=filters,
    671     storage_options=storage_options,
    672     use_nullable_dtypes=use_nullable_dtypes,
    673     dtype_backend=dtype_backend,
    674     filesystem=filesystem,
    675     **kwargs,
    676 )

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\parquet.py:267, in PyArrowImpl.read(self, path, columns, filters, use_nullable_dtypes, dtype_backend, storage_options, filesystem, **kwargs)
    264 if manager == "array":
    265     to_pandas_kwargs["split_blocks"] = True  # type: ignore[assignment]
...
--> 882         handle = open(handle, ioargs.mode)
    883     handles.append(handle)
    885 # Convert BytesIO or file objects passed with an encoding

FileNotFoundError: [Errno 2] No such file or directory: 'C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Outputs/C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Outputs/20260622_imp_df_seg_20260618 1349 Final Modeling Dataset V1.parquet'
