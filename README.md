this supposed to generate all the charts in the list, but get only two and others are not appearing with error, 
basically i want chart for 
 'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100'
    Net Sales/Total Assets',
    ===
code is 

for var in valid_vars2:
    plot_predicted_actual2(
    df_id_bsd,
    var,
    'valid_def_ind_1yr',
    num_buckets=10,
    segment_var='lifestage_map2',
    variable=var,
    folder_name='Images',
    plot_axis='log',
    plot_ranges=False)


error is 
---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
Cell In[48], line 2
      1 for var in valid_vars2:
----> 2     plot_predicted_actual2(
      3     df_id_bsd,
      4     var,
      5     'valid_def_ind_1yr',
      6     num_buckets=10,
      7     segment_var='lifestage_map2',
      8     variable=var,
      9     folder_name='Images',
     10     plot_axis='log',
     11     plot_ranges=False)

Cell In[4], line 145
    138 safe_variable = variable.replace('/', '_')
    140 file_path = os.path.join(
    141     folder_name,
    142     f'{safe_variable}_{segment_var}_bucketed_plot.png'
    143 )
--> 145 plt.savefig(file_path, bbox_inches='tight')
    146 plt.show()
    147 plt.close()
...
-> 2563         fp = builtins.open(filename, "w+b")
   2564 else:
   2565     fp = cast(IO[bytes], fp)

FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\YWA95\\OneDrive - First-Citizens Bank & Trust Co\\Old Download----NEW WORK\\05 05 26 ID_BSD Code Updates20260505094251\\01. Code\\model_development\\segmentation_analysis\\code\\Images\\(EBITDA-Capex)_(Interest Expense+CPLTD)_winsor_lifestage_map2_bucketed_plot.png'
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
