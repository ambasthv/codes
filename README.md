PS C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code> python src\run.py
db_path is C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251
08:32:08.7 - NOTE: Running PD risk rating module
08:32:08.7 - NOTE: Loading support sheet
DEBUG: Path length = 163
DEBUG: Path exists = True
DEBUG: Full path = C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251/02. Data/01. Master Database/Support_v2.xlsx
08:32:10.7 - NOTE: Loading legacy bank datasets: SVB: raw
08:32:10.7 - NOTE: Loading SVB data
08:32:10.7 - NOTE: Loading SVB total portfolio dataset
08:32:12.5 - NOTE: Loading SVB commitment dataset
08:32:14.2 - NOTE: Loading SVB deposits dataset
08:32:17.5 - NOTE: Loading SVB defaults dataset
08:32:17.9 - NOTE: Loading SVB chargeoffs dataset
08:32:17.9 - NOTE: Loading SVB total statement dataset
08:32:19.7 - NOTE: Loading SVB grade events dataset
08:32:20.6 - NOTE: Loading SVB LECE clients dataset
08:32:26.9 - NOTE: Finished loading SVB data
08:32:26.9 - NOTE: Finished loading all legacy bank data
08:32:26.9 - NOTE: Merging SVB raw data with OOT data
08:32:28.6 - NOTE: In Time Period: 2007-07-31 00:00:00.000 to 2024-03-31 00:00:00.000
08:32:28.6 - NOTE: OOT Period: 2024-05-31 00:00:00.000 to 2025-09-30 00:00:00.000
08:32:30.6 - NOTE: Size before merge: (3901190, 19), Size after merge: (3603247, 21)
08:32:30.6 - NOTE: Completed merge of SVB portfolio OOT data
08:32:31.3 - NOTE: In Time Period: 2006-01-31 to 2023-12-31
08:32:31.4 - NOTE: OOT Period: 2024-01-31 to 2025-07-31
08:32:31.7 - NOTE: Completed merge of SVB commitment OOT data
08:32:44.0 - NOTE: In Time Period: 2021-10-31 to 2023-12-31
08:32:44.4 - NOTE: OOT Period: 2024-01-31 to 2025-07-31
08:32:46.3 - NOTE: Completed merge of SVB deposits OOT data
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader_svb.py:342: FutureWarning: errors='ignore' is deprecated and will raise in a future version. Use to_numeric without passing `errors` and catch exceptions explicitly instead
  svb_defaults_oot['cif'] = pd.to_numeric(svb_defaults_oot['cif'], errors = 'ignore')
08:32:47.6 - NOTE: In Time Period: 2007-07-31 to 2023-12-31
08:32:47.6 - NOTE: OOT Period: 2024-01-31 to 2025-07-31
08:32:47.7 - NOTE: Completed merge of SVB defaults OOT data
08:32:47.7 - NOTE: In Time Period: 2006-03-31 to 2023-12-31
08:32:47.7 - NOTE: OOT Period: 2024-03-31 to 2025-09-30
08:32:47.7 - NOTE: Completed merge of SVB chargeoffs OOT data
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader_svb.py:389: DtypeWarning: Columns (2) have mixed types. Specify dtype option on import or set low_memory=False.
  svb_statement_oot = pd.read_csv(f"{db_path}/{svb_oot_path}/{svb_statement_path}")
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader_svb.py:394: FutureWarning: errors='ignore' is deprecated and will raise in a future version. Use to_numeric without passing `errors` and catch exceptions explicitly instead
  svb_statement_oot['CIF'] = pd.to_numeric(svb_statement_oot['CIF'], errors='ignore')
08:32:53.9 - NOTE: In Time Period: 2006-01-01 00:00:00.000 to 2023-12-31 00:00:00.000
08:32:53.9 - NOTE: OOT Period: 2024-01-01 00:00:00.000 to 2025-07-31 00:00:00.000
08:32:55.5 - NOTE: Completed merge of SVB statements OOT data
08:32:57.4 - NOTE: In Time Period: nan to nan
08:32:57.5 - NOTE: OOT Period: 2024-03-07 to 2025-08-05
08:32:57.6 - NOTE: Completed merge of SVB grade event OOT data
08:32:59.2 - NOTE: In Time Period: 2022-06-30 00:00:00 to 2023-12-31 00:00:00
08:32:59.2 - NOTE: OOT Period: 2024-01-31 to 2025-08-05
08:33:00.1 - NOTE: Completed merge of SVB LECE clients OOT data
08:33:04.9 - NOTE: In Time Period: 2007-09-30 00:00:00 to 2023-12-31 00:00:00
08:33:04.9 - NOTE: OOT Period: 2024-01-31 00:00:00 to 2025-12-31 00:00:00
08:33:04.9 - NOTE: Completed merge of SVB underwriting CF other OOT data
08:33:05.9 - NOTE: In Time Period: 2007-07-31 00:00:00.000 to 2024-05-31 00:00:00.000
08:33:05.9 - NOTE: OOT Period: 2024-06-30 00:00:00.000 to 2025-09-30 00:00:00.000
08:33:06.1 - NOTE: Completed merge of SVB EMEA OOT data
08:33:07.4 - NOTE: Finished merging SVB raw data with OOT data
08:33:07.4 - NOTE: Preparing each legacy bank dataset with settings: 
FCB preprocessing: unpacking interim
CIT preprocessing: unpacking interim
SVB preprocessing: processing
Pre-2012 CIT preprocessing: unpacking interim
08:33:07.4 - NOTE: Processing SVB data
08:33:07.4 - NOTE: Executing initial cleaning for SVB
08:33:22.1 - NOTE: Merging SVB-specific fields for aggregation
08:33:22.5 - NOTE: Filtering valid NAICS and SIC codes
08:33:22.6 - NOTE: Constructing derived industry field
08:33:23.0 - NOTE: Merging model routing fields
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\utils.py:199: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  data["cre_industry"] = data[industry_code_col].map(cre_flag_map).fillna(0)
08:33:24.0 - NOTE: Creating model routing flags
08:33:27.2 - NOTE: Mapping loan_age_max_bal
08:33:31.0 - NOTE: Mapping loan_term_max_bal
08:33:32.7 - NOTE: Mapping loan_age_to_term_max_bal
08:33:34.3 - NOTE: Mapping pct_amortization_max_bal
08:33:36.0 - NOTE: Mapping revolving_credit_ind_max_bal
08:33:37.6 - NOTE: Mapping loan_age_max_exp
08:33:39.0 - NOTE: Mapping loan_term_max_exp
08:33:40.5 - NOTE: Mapping loan_age_to_term_max_exp
08:33:42.1 - NOTE: Mapping pct_amortization_max_exp
08:33:43.8 - NOTE: Mapping revolving_credit_ind_max_exp
08:33:45.5 - NOTE: Executing plurality balance mapping
08:33:45.5 - NOTE: Mapping facility_model_routing
08:33:47.1 - NOTE: Mapping naics_med_flag
08:33:48.8 - NOTE: Mapping naics_code
08:33:50.4 - NOTE: Mapping call_code
08:33:52.2 - NOTE: Mapping industry_group
08:33:53.9 - NOTE: Mapping lifestage
08:33:55.6 - NOTE: Mapping facility_type
08:33:57.3 - NOTE: Mapping 1205_niche_desc
08:33:59.0 - NOTE: Mapping 1205ncd
08:34:00.8 - NOTE: Aggregating total portfolio dataset
08:34:08.5 - NOTE: Aggregation of total portfolio data complete
08:34:08.7 - NOTE: Merging commitment data
08:34:13.7 - WARNING: Merge of commitment data results in 89.34% match rate.
08:34:14.0 - NOTE: Adding growth flag
08:34:17.3 - NOTE: Adding underwriting method
Traceback (most recent call last):
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\run.py", line 79, in <module>
    run()
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\run.py", line 37, in run
    treat_legacy_bank_data(fcb_data_dict, cit_data_dict, svb_data_dict, citp2012_data_dict, config, support)
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\preprocessing\preprocessing.py", line 36, in treat_legacy_bank_data
    (treat_svb(**svb_data_dict, config=config, support=support) if config["svb_do_preprocessing"]
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\preprocessing\preprocessing_svb.py", line 1436, in treat_svb
    svb_data = add_underwriting_exceptions(svb_data, uw_cf_other)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\preprocessing\preprocessing_svb.py", line 431, in add_underwriting_exceptions
    uw_df['imputed_method'] = np.where(uw_df['imputed_uw']=='blank',np.nan,'known')
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numpy.exceptions.DTypePromotionError: The DType <class 'numpy.dtypes._PyFloatDType'> could not be promoted by <class 'numpy.dtypes.StrDType'>. This means that no common DType exists for the given inputs. For example they cannot be stored in a single array unless the dtype is `object`. The full list of DTypes is: (<class 'numpy.dtypes._PyFloatDType'>, <class 'numpy.dtypes.StrDType'>)
PS C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code> 
