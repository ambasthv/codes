---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
Cell In[10], line 5
      2 master_db = pd.read_parquet(master_db_path)   # Use full path directly
      4 # load variable cleaning excels
----> 5 cleaning_excels = read_cleaning_xlsx(support_path)  # Use full path
      7 print(f"Loaded master data shape: {master_db.shape}")
      8 print("✅ Data and cleaning rules loaded successfully!")

File c:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\MODELLING WORK\segmentation_analysis- Nick code 29 June\code\segmentation_analysis_utils.py:179, in read_cleaning_xlsx(file_path, sheet_key)
    175 if not sheet_name:
    176     raise ValueError(f"No sheet configured for key: {sheet_key}")
    178 cleaning_excels = {
--> 179     sheet_key: pd.read_excel(
    180         io=file_path,
    181         sheet_name=sheet_name
    182     )
    183 }
    185 return cleaning_excels

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\excel\_base.py:495, in read_excel(io, sheet_name, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skiprows, nrows, na_values, keep_default_na, na_filter, verbose, parse_dates, date_parser, date_format, thousands, decimal, comment, skipfooter, storage_options, dtype_backend, engine_kwargs)
    493 if not isinstance(io, ExcelFile):
    494     should_close = True
--> 495     io = ExcelFile(
    496         io,
...
--> 882         handle = open(handle, ioargs.mode)
    883     handles.append(handle)
    885 # Convert BytesIO or file objects passed with an encoding

FileNotFoundError: [Errno 2] No such file or directory: 'C:/Users/YWA95/OneDrive - First-Citizens Bank & Trust Co/MODELLING WORK/segmentation_analysis- Nick code 29 June/data/Support/006222026_variable transformations python.xlsx'
