---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)
Cell In[19], line 34
     32     filename = f"Mean_Default_by_{bin_col}.xlsx"
     33     output_path = os.path.join(output_dir, filename)
---> 34     mean_default.to_excel(output_path, index=False)
     36     print(f"✅ Saved: {output_path}")
     38 print("\n✅ All files saved successfully!")

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\util\_decorators.py:333, in deprecate_nonkeyword_arguments.<locals>.decorate.<locals>.wrapper(*args, **kwargs)
    327 if len(args) > num_allow_args:
    328     warnings.warn(
    329         msg.format(arguments=_format_argument_list(allow_args)),
    330         FutureWarning,
    331         stacklevel=find_stack_level(),
    332     )
--> 333 return func(*args, **kwargs)

File c:\Program Files\Anaconda3_2024_10_1\Lib\site-packages\pandas\core\generic.py:2417, in NDFrame.to_excel(self, excel_writer, sheet_name, na_rep, float_format, columns, header, index, index_label, startrow, startcol, engine, merge_cells, inf_rep, freeze_panes, storage_options, engine_kwargs)
   2404 from pandas.io.formats.excel import ExcelFormatter
   2406 formatter = ExcelFormatter(
   2407     df,
   2408     na_rep=na_rep,
   (...)
   2415     inf_rep=inf_rep,
...
    614 parent = Path(path).parent
    615 if not parent.is_dir():
--> 616     raise OSError(rf"Cannot save file into a non-existent directory: '{parent}'")

OSError: Cannot save file into a non-existent directory: 'C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\Old Download----NEW WORK\05 05 26 ID_BSD Code Updates20260505094251\Analysis-Vivek\Mean_Default_by_Gross Profit'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
