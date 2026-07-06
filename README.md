this gve error, 
#create a separate mapped lifestage column with simplified lifestage 
mapping = pd.read_csv('Lifestage_Mapping.csv')
mapping_dict = dict(zip(mapping['Original Lifestage'], mapping['Mapped Lifestage']))
df_id_bsd['lifestage_map'] = df_id_bsd['lifestage'].map(mapping_dict)




error is 
---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
Cell In[31], line 2
      1 #create a separate mapped lifestage column with simplified lifestage 
----> 2 mapping = pd.read_csv('Lifestage_Mapping.csv')
      3 mapping_dict = dict(zip(mapping['Original Lifestage'], mapping['Mapped Lifestage']))
      4 df_id_bsd['lifestage_map'] = df_id_bsd['lifestage'].map(mapping_dict)

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\parsers\readers.py:1026, in read_csv(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)
   1013 kwds_defaults = _refine_defaults_read(
   1014     dialect,
   1015     delimiter,
   (...)
   1022     dtype_backend=dtype_backend,
   1023 )
   1024 kwds.update(kwds_defaults)
-> 1026 return _read(filepath_or_buffer, kwds)

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\io\parsers\readers.py:620, in _read(filepath_or_buffer, kwds)
    617 _validate_names(kwds.get("names", None))
    619 # Create the parser.
--> 620 parser = TextFileReader(filepath_or_buffer, **kwds)
    622 if chunksize or iterator:
    623     return parser
...
    880     else:
    881         # Binary mode
    882         handle = open(handle, ioargs.mode)

FileNotFoundError: [Errno 2] No such file or directory: 'Lifestage_Mapping.csv'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
