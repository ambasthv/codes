PS C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code> python src\run.py
db_path is C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251
08:50:18.2 - NOTE: Running PD risk rating module
08:50:18.2 - NOTE: Loading support sheet
DEBUG: Path length = 163
DEBUG: Path exists = True
DEBUG: Full path = C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251/02. Data/01. Master Database/Support_v2.xlsx
08:50:20.5 - NOTE: Loading legacy bank datasets: SVB: raw
08:50:20.5 - NOTE: Loading SVB data
08:50:20.5 - NOTE: Loading SVB total portfolio dataset
08:50:22.3 - NOTE: Loading SVB commitment dataset
08:50:24.8 - NOTE: Loading SVB deposits dataset
08:50:28.5 - NOTE: Loading SVB defaults dataset
08:50:28.9 - NOTE: Loading SVB chargeoffs dataset
08:50:28.9 - NOTE: Loading SVB total statement dataset
08:50:30.5 - NOTE: Loading SVB grade events dataset
08:50:31.3 - NOTE: Loading SVB LECE clients dataset
08:50:37.2 - NOTE: Finished loading SVB data
08:50:37.2 - NOTE: Finished loading all legacy bank data
08:50:37.2 - NOTE: Merging SVB raw data with OOT data
08:50:39.0 - NOTE: In Time Period: 2007-07-31 00:00:00.000 to 2024-03-31 00:00:00.000
08:50:39.0 - NOTE: OOT Period: 2024-05-31 00:00:00.000 to 2025-09-30 00:00:00.000
08:50:41.2 - NOTE: Size before merge: (3901190, 19), Size after merge: (3603247, 21)
08:50:41.2 - NOTE: Completed merge of SVB portfolio OOT data
08:50:41.9 - NOTE: In Time Period: 2006-01-31 to 2023-12-31
08:50:42.0 - NOTE: OOT Period: 2024-01-31 to 2025-07-31
08:50:42.2 - NOTE: Completed merge of SVB commitment OOT data
08:50:54.3 - NOTE: In Time Period: 2021-10-31 to 2023-12-31
08:50:54.7 - NOTE: OOT Period: 2024-01-31 to 2025-07-31
08:50:55.2 - NOTE: Completed merge of SVB deposits OOT data
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader_svb.py:342: FutureWarning: errors='ignore' is deprecated and will raise in a future version. Use to_numeric without passing `errors` and catch exceptions explicitly instead
  svb_defaults_oot['cif'] = pd.to_numeric(svb_defaults_oot['cif'], errors = 'ignore')
08:50:56.3 - NOTE: In Time Period: 2007-07-31 to 2023-12-31
08:50:56.3 - NOTE: OOT Period: 2024-01-31 to 2025-07-31
08:50:56.3 - NOTE: Completed merge of SVB defaults OOT data
08:50:56.4 - NOTE: In Time Period: 2006-03-31 to 2023-12-31
08:50:56.4 - NOTE: OOT Period: 2024-03-31 to 2025-09-30
08:50:56.4 - NOTE: Completed merge of SVB chargeoffs OOT data
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader_svb.py:389: DtypeWarning: Columns (2) have mixed types. Specify dtype option on import or set low_memory=False.
  svb_statement_oot = pd.read_csv(f"{db_path}/{svb_oot_path}/{svb_statement_path}")
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\loader\loader_svb.py:394: FutureWarning: errors='ignore' is deprecated and will raise in a future version. Use to_numeric without passing `errors` and catch exceptions explicitly instead
  svb_statement_oot['CIF'] = pd.to_numeric(svb_statement_oot['CIF'], errors='ignore')
08:51:03.1 - NOTE: In Time Period: 2006-01-01 00:00:00.000 to 2023-12-31 00:00:00.000
08:51:03.1 - NOTE: OOT Period: 2024-01-01 00:00:00.000 to 2025-07-31 00:00:00.000
08:51:05.2 - NOTE: Completed merge of SVB statements OOT data
08:51:07.2 - NOTE: In Time Period: nan to nan
08:51:07.2 - NOTE: OOT Period: 2024-03-07 to 2025-08-05
08:51:07.3 - NOTE: Completed merge of SVB grade event OOT data
08:51:08.9 - NOTE: In Time Period: 2022-06-30 00:00:00 to 2023-12-31 00:00:00
08:51:08.9 - NOTE: OOT Period: 2024-01-31 to 2025-08-05
08:51:09.8 - NOTE: Completed merge of SVB LECE clients OOT data
08:51:14.3 - NOTE: In Time Period: 2007-09-30 00:00:00 to 2023-12-31 00:00:00
08:51:14.3 - NOTE: OOT Period: 2024-01-31 00:00:00 to 2025-12-31 00:00:00
08:51:14.3 - NOTE: Completed merge of SVB underwriting CF other OOT data
08:51:15.2 - NOTE: In Time Period: 2007-07-31 00:00:00.000 to 2024-05-31 00:00:00.000
08:51:15.3 - NOTE: OOT Period: 2024-06-30 00:00:00.000 to 2025-09-30 00:00:00.000
08:51:15.4 - NOTE: Completed merge of SVB EMEA OOT data
08:51:16.3 - NOTE: Finished merging SVB raw data with OOT data
08:51:16.3 - NOTE: Preparing each legacy bank dataset with settings: 
FCB preprocessing: unpacking interim
CIT preprocessing: unpacking interim
SVB preprocessing: processing
Pre-2012 CIT preprocessing: unpacking interim
08:51:16.3 - NOTE: Processing SVB data
08:51:16.3 - NOTE: Executing initial cleaning for SVB
08:51:31.0 - NOTE: Merging SVB-specific fields for aggregation
08:51:31.5 - NOTE: Filtering valid NAICS and SIC codes
08:51:31.5 - NOTE: Constructing derived industry field
08:51:31.9 - NOTE: Merging model routing fields
C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\utils.py:199: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
  data["cre_industry"] = data[industry_code_col].map(cre_flag_map).fillna(0)
08:51:33.0 - NOTE: Creating model routing flags
08:51:36.1 - NOTE: Mapping loan_age_max_bal
08:51:39.0 - NOTE: Mapping loan_term_max_bal
08:51:40.6 - NOTE: Mapping loan_age_to_term_max_bal
08:51:42.2 - NOTE: Mapping pct_amortization_max_bal
08:51:43.8 - NOTE: Mapping revolving_credit_ind_max_bal
08:51:45.4 - NOTE: Mapping loan_age_max_exp
08:51:46.8 - NOTE: Mapping loan_term_max_exp
08:51:48.3 - NOTE: Mapping loan_age_to_term_max_exp
08:51:49.9 - NOTE: Mapping pct_amortization_max_exp
08:51:51.5 - NOTE: Mapping revolving_credit_ind_max_exp
08:51:53.2 - NOTE: Executing plurality balance mapping
08:51:53.2 - NOTE: Mapping facility_model_routing
08:51:54.7 - NOTE: Mapping naics_med_flag
08:51:56.4 - NOTE: Mapping naics_code
08:51:57.9 - NOTE: Mapping call_code
08:51:59.6 - NOTE: Mapping industry_group
08:52:01.4 - NOTE: Mapping lifestage
08:52:03.0 - NOTE: Mapping facility_type
08:52:04.9 - NOTE: Mapping 1205_niche_desc
08:52:06.6 - NOTE: Mapping 1205ncd
08:52:08.3 - NOTE: Aggregating total portfolio dataset
08:52:16.7 - NOTE: Aggregation of total portfolio data complete
08:52:16.9 - NOTE: Merging commitment data
08:52:22.2 - WARNING: Merge of commitment data results in 89.34% match rate.
08:52:22.4 - NOTE: Adding growth flag
08:52:26.1 - NOTE: Adding underwriting method
Traceback (most recent call last):
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\run.py", line 79, in <module>
    run()
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\run.py", line 37, in run
    treat_legacy_bank_data(fcb_data_dict, cit_data_dict, svb_data_dict, citp2012_data_dict, config, support)
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\preprocessing\preprocessing.py", line 36, in treat_legacy_bank_data
    (treat_svb(**svb_data_dict, config=config, support=support) if config["svb_do_preprocessing"]
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\preprocessing\preprocessing_svb.py", line 1438, in treat_svb
    svb_data = add_underwriting_exceptions(svb_data, uw_cf_other)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code\src\preprocessing\preprocessing_svb.py", line 433, in add_underwriting_exceptions
    uw_df['imputed_method'] = np.where( uw_df['imputed_uw'] == 'blank', np.nan, 'known' )
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
numpy.exceptions.DTypePromotionError: The DType <class 'numpy.dtypes._PyFloatDType'> could not be promoted by <class 'numpy.dtypes.StrDType'>. This means that no common DType exists for the given inputs. For example they cannot be stored in a single array unless the dtype is `object`. The full list of DTypes is: (<class 'numpy.dtypes._PyFloatDType'>, <class 'numpy.dtypes.StrDType'>)
PS C:\Vivek Ambastha\Swati- Model Validation\...MODEL DEVELOPMENT\Old Download\05 05 26 ID_BSD Code Updates20260505094251\01. Code> 
