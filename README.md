i am trying to save excel after running the b elow code, but getting error, fix it

import os

print("=== Count per Bin per Niche ===\n")

bin_cols = ['Gross Profit/Net Sales_x_100_bin', 
               'Net Profit/Net Sales_x_100_bin', 
               'Net Sales/Total Assets_bin']

for bin_col in bin_cols:
    if bin_col not in df.columns:
        continue
    
    count_df = df.groupby([bin_col, 'niche_mapped']).size().unstack(fill_value=0)
    count_df = count_df.reset_index()
    count_df = count_df.rename(columns={bin_col: 'Bin'})
    
    ratio_name = bin_col.replace('_winsor_bin', '')
    count_df.insert(0, 'Ratio', ratio_name)
    
    print(f"\n{ratio_name} - Counts per Bin:")
    print(count_df)
    
    # Create directory if it doesn't exist
    output_dir = os.path.dirname(df_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save
    output_path = os.path.join(output_dir, f"Bin_Counts_{ratio_name}.xlsx")
    count_df.to_excel(output_path, index=False)
    print(f"✅ Saved: {output_path}")

print("\n✅ All bin count tables saved successfully!")


this is the error i am getting, fix it
---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)
Cell In[14], line 29
     27     # Save
     28     output_path = os.path.join(output_dir, f"Bin_Counts_{ratio_name}.xlsx")
---> 29     count_df.to_excel(output_path, index=False)
     30     print(f"✅ Saved: {output_path}")
     32 print("\n✅ All bin count tables saved successfully!")

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

OSError: Cannot save file into a non-existent directory: 'C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\Old Download----NEW WORK\05 05 26 ID_BSD Code Updates20260505094251\Analysis-Vivek\Bin_Counts_Gross Profit'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
