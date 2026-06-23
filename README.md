main piece of code, 


    # apply forwardfill from last observed
    #mixed_uw = mixed_uw.sort_values(by=['cif', 'cust_line_nbr', 'period'], ascending=[True, True, True])
    sort_cols = ['cif', 'cust_line_nbr', 'period']
    available_sort_cols = [col for col in sort_cols if col in mixed_uw.columns]

    mixed_uw = mixed_uw.sort_values(
        by=available_sort_cols, 
    ascending=[True, True, True])\
        .groupby(['cif', 'cust_line_nbr'])\
            .apply(forwardfill_last_method)\
                .reset_index(drop=True)

error:

File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 79, in <module>
    run()
    ~~~^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\run.py", line 37, in run
    treat_legacy_bank_data(fcb_data_dict, cit_data_dict, svb_data_dict, citp2012_data_dict, config, support)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing.py", line 36, in treat_legacy_bank_data
    (treat_svb(**svb_data_dict, config=config, support=support) if config["svb_do_preprocessing"]
     ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py", line 1445, in treat_svb
    svb_data = add_underwriting_exceptions(svb_data, uw_cf_other)
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\01. Code\src\preprocessing\preprocessing_svb.py", line 526, in add_underwriting_exceptions
    mixed_uw = mixed_uw.sort_values(
               ~~~~~~~~~~~~~~~~~~~~^
        by=available_sort_cols,
        ^^^^^^^^^^^^^^^^^^^^^^^
    ascending=[True, True, True])\
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\06112026 PD Portfolio Data Pipeline Code Updates\.venv\Lib\site-packages\pandas\core\frame.py", line 8335, in sort_values
    raise ValueError(
    ...<2 lines>...
    )
ValueError: Length of ascending (3) != length of by (1)
