# apply forwardfill from last observed
sort_cols = ['cif', 'cust_line_nbr', 'period']
available_sort_cols = [col for col in sort_cols if col in mixed_uw.columns]

# Fix: Make ascending match the actual number of columns
ascending_list = [True] * len(available_sort_cols)

mixed_uw = mixed_uw.sort_values(
    by=available_sort_cols, 
    ascending=ascending_list
)\
    .groupby(['cif', 'cust_line_nbr'])\
        .apply(forwardfill_last_method)\
            .reset_index(drop=True)