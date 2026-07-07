GETTING ERROR HERE WITH GRAPHS, ONLY ONE GRPAH IS BEING SHOWN

for var in var_list2:
    plot_predicted_actual2(
    df_id_bsd,
    var,
    'valid_def_ind_1yr',
    num_buckets=4,
    segment_var='lifestage_map2',
    variable=var,
    folder_name='Images',
    plot_axis='log',
    plot_ranges=False)


    ERROR IS 
    ---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
Cell In[35], line 2
      1 for var in var_list2:
----> 2     plot_predicted_actual2(
      3     df_id_bsd,
      4     var,
      5     'valid_def_ind_1yr',
      6     num_buckets=4,
      7     segment_var='lifestage_map2',
      8     variable=var,
      9     folder_name='Images',
     10     plot_axis='log',
     11     plot_ranges=False)

Cell In[4], line 151
    144 safe_variable = variable.replace('/', '_')
    146 file_path = os.path.join(
    147     folder_name,
    148     f'{safe_variable}_{segment_var}_bucketed_plot.png'
    149 )
--> 151 plt.savefig(file_path, bbox_inches='tight')
    152 plt.show()
    153 plt.close()
...
-> 2563         fp = builtins.open(filename, "w+b")
   2564 else:
   2565     fp = cast(IO[bytes], fp)

FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\YWA95\\OneDrive - First-Citizens Bank & Trust Co\\Old Download----NEW WORK\\05 05 26 ID_BSD Code Updates20260505094251\\01. Code\\model_development\\segmentation_analysis\\code\\Images\\(EBITDA-Capex)_(Interest Expense+CPLTD)_winsor_lifestage_map2_bucketed_plot.png'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
