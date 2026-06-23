✅ Clear Instruction:
Go to this file:
C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py
Go to Line 522
Replace this line:
mixed_uw = mixed_uw.sort_values(by=['cif', 'cust_line_nbr', 'period'], ascending=[True, True, True])
With this:
# Safe sorting - only use columns that exist
sort_cols = ['cif', 'cust_line_nbr', 'period']
available_sort_cols = [col for col in sort_cols if col in mixed_uw.columns]

mixed_uw = mixed_uw.sort_values(
    by=available_sort_cols, 
    ascending=[True, True, True]
)

Just make this one replacement and run again.
This should fix the current KeyError: 'cif' error.
Let me know what error comes next (if any).
