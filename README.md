
below is the code, all paths are corrected, and file is also there, 
cell 1
paths = {
    ### Paths for master database and final modeling dataset
    'db_path' : f"{db_path}\\02. Data\\01. Master Database",
    # Main
    'main' : f"{db_path}\\02. Data\\02. Model Development\\",
    
    # INPUT DATASET FILE PATHS
    'ratio_cleaning' : {
        'folder' : '01. Ratio Cleaning\\',
        # Modify this text to the desired input folder
        'subfolder' : '20260601\\',
        # Modify this text to the desired input dataset
        'dataset' : '20260622_imp_df_seg_20260618 1349 Final Modeling Dataset V1.parquet'
    },
    
    # RESULTS EXPORT FILE PATHS
    'sfa' : {
        'folder' : '02. SFA\\',
        # Modify this subfolder to the desired export folder
        'subfolder' : f"{timestamp}\\",
        'file' : f"{timestamp}_SFA_results.xlsx",
        'plots_folder' : f"{timestamp}"
    },

    'mapping' : {
        # SOURCE OF TRUTH MAPPING DOCUMENTS WILL REMAIN IN THE MAIN "MFA" FOLDER
        'folder' : '00. Support\\02. MFA Preprocessing\\',
        # ONLY POPULATE THIS FILE PATH IF ADHOC TESTING IS DONE AND LEVERAGES EXTERNAL MAPPING DOCUMENTS
        # Follow this naming convention, replacing subfolder_name with the name of the actual folder
        # Example: "subfolder_name\\""
        'subfolder' : '',
        # NAMES OF EXTERNAL EXCEL FILES FOR MFA 
        'variable_selection' : '20250813 Var Cats re-run vars_prioritized.xlsx',
        'alt_treatments' : 'vars_prioritized_alt_treatment.xlsx', 
        'alt_selections' : 'vars_prioritized_selection_helper.xlsx'
    },
}

import_file = rf"{paths['main']}{paths['ratio_cleaning']['folder']}{paths['ratio_cleaning']['subfolder']}{paths['ratio_cleaning']['dataset']}"

export_folder = rf"{paths['main']}{paths['sfa']['folder']}{paths['sfa']['subfolder']}"
export_file = os.path.join(export_folder, paths['sfa']['file'])

cell 2
# load master db modeling dataset
mydata = pd.read_parquet(import_file)

### DP TO ADD COLUMN FOR ALL SEGMENT

print(mydata.columns)
print(len(mydata))

ERROR 
---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
Cell In[14], line 2
      1 # load master db modeling dataset
----> 2 mydata = pd.read_parquet(import_file)
      4 ### DP TO ADD COLUMN FOR ALL SEGMENT
      6 print(mydata.columns)

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
--> 267 path_or_handle, handles, filesystem = _get_path_or_handle(
    268     path,
    269     filesystem,
    270     storage_options=storage_options,
    271     mode="rb",
    272 )
    273 try:
    274     pa_table = self.api.parquet.read_table(
    275         path_or_handle,
    276         columns=columns,
   (...)
    279         **kwargs,
    280     )

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\parquet.py:140, in _get_path_or_handle(path, fs, storage_options, mode, is_dir)
    130 handles = None
    131 if (
    132     not fs
    133     and not is_dir
   (...)
    138     # fsspec resources can also point to directories
    139     # this branch is used for example when reading from non-fsspec URLs
--> 140     handles = get_handle(
    141         path_or_handle, mode, is_text=False, storage_options=storage_options
    142     )
    143     fs = None
    144     path_or_handle = handles.handle

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\common.py:882, in get_handle(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)
    873         handle = open(
    874             handle,
    875             ioargs.mode,
   (...)
    878             newline="",
    879         )
    880     else:
    881         # Binary mode
--> 882         handle = open(handle, ioargs.mode)
    883     handles.append(handle)
    885 # Convert BytesIO or file objects passed with an encoding

FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Vivek Ambastha\\Swati- Model Validation\\...MODEL DEVELOPMENT\\Old Download\\05 05 26 ID_BSD Code Updates20260505094251\\02. Data\\02. Model Development\\01. Ratio Cleaning\\20260601\\20260622_imp_df_seg_20260618 1349 Final Modeling Dataset V1.parquet'
