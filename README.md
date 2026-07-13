Quick_Ratio in dataframe: False

Columns containing Quick:
['Quick_Ratio_null_flag']

Rows in cleaning sheet containing Quick:
          variable  floor_pct  floor_val  cap_pct  cap_val  \
7      Quick_Ratio       0.01        NaN     0.99      NaN   
8  Adj Quick Ratio       0.01        NaN     0.99      NaN   

  Potential Negative Location  Bad Zero Denom  Bad Zero Num negative_handling  \
7                     neither               0             0        set to min   
8                     neither               0             0        set to min   

   zero_handling negative_infinite_handling positive_infinite_handling  \
7            NaN                 set to min                 set to max   
8            NaN                 set to min                 set to max   

   special_cap_floor_treatment  Negative Value Notes  Infinite Value Notes  
7                          NaN                   NaN                   NaN  
8                          NaN                   NaN                   NaN  
