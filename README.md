                                            variable  floor_pct  floor_val  \
0            (EBITDA-Capex)/(Interest Expense+CPLTD)       0.01        NaN   
1                    EBITDA/(Interest Expense+CPLTD)       0.01        NaN   
2  (Total Assets-Total Liabilities)/Total Liabili...       0.01        NaN   
3                            Total Debt/Total Assets       0.01        NaN   
4                                    Cash/Total Debt       0.01        NaN   
5                 Current Assets/Current Liabilities       0.01        NaN   
6                       Gross Profit/Net Sales_x_100       0.01        NaN   
7                         Net Profit/Net Sales_x_100       0.01        NaN   
8                             Net Sales/Total Assets       0.01        NaN   

   cap_pct  cap_val Potential Negative Location  Bad Zero Denom  Bad Zero Num  \
0     0.99      NaN                   numerator               0             0   
1     0.99      NaN                   numerator               0             0   
2     0.99      NaN                   numerator               0             1   
3     0.99      NaN                 denominator               0             1   
4     0.99      NaN                     neither               0             0   
5     0.99      NaN                     neither               0             0   
6     0.99      NaN                   numerator               0             0   
7     0.99      NaN                   numerator               0             0   
8     0.99      NaN                     neither               0             1   

  negative_handling  zero_handling negative_infinite_handling  \
0               NaN            NaN                 set to min   
1               NaN            NaN                 set to min   
2               NaN            NaN                set to null   
3        set to max            NaN                set to null   
4        set to min            NaN                 set to min   
5        set to min            NaN                 set to min   
6               NaN            NaN                 set to min   
7               NaN            NaN                 set to min   
8        set to min            NaN                set to null   

  positive_infinite_handling  special_cap_floor_treatment  \
0                 set to max                          NaN   
1                 set to max                          NaN   
2                set to null                          NaN   
3                set to null                          NaN   
4                 set to max                          NaN   
5                 set to max                          NaN   
6                set to null                          NaN   
7                set to null                          NaN   
8                set to null                          NaN   

   Negative Value Notes  Infinite Value Notes  
0                   NaN                   NaN  
1                   NaN                   NaN  
2                   NaN                   NaN  
3                   NaN                   NaN  
4                   NaN                   NaN  
5                   NaN                   NaN  
6                   NaN                   NaN  
7                   NaN                   NaN  
8                   NaN                   NaN  

Data types of columns:
variable                        object
floor_pct                      float64
floor_val                      float64
cap_pct                        float64
cap_val                        float64
Potential Negative Location     object
Bad Zero Denom                   int64
Bad Zero Num                     int64
negative_handling               object
zero_handling                  float64
negative_infinite_handling      object
positive_infinite_handling      object
special_cap_floor_treatment    float64
Negative Value Notes           float64
Infinite Value Notes           float64
dtype: object

Variable column values:
['(EBITDA-Capex)/(Interest Expense+CPLTD)', 'EBITDA/(Interest Expense+CPLTD)', '(Total Assets-Total Liabilities)/Total Liabilities', 'Total Debt/Total Assets', 'Cash/Total Debt', 'Current Assets/Current Liabilities', 'Gross Profit/Net Sales_x_100', 'Net Profit/Net Sales_x_100', 'Net Sales/Total Assets']
