Traceback (most recent call last):
  File "C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\1.OW\ID_BSD Modelling\01. Code\src\run.py", line 79, in <module>
    run()
  File "C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\1.OW\ID_BSD Modelling\01. Code\src\run.py", line 60, in run
    modeling_dataset = refine_model_pop(combined_entity_data, macro_data, support, config)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\1.OW\ID_BSD Modelling\01. Code\src\preprocessing\preprocessing.py", line 895, in refine_model_pop
    df['arr_software_ind'] = np.select(
                             ^^^^^^^^^^
  File "C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\1.OW\ID_BSD Modelling\.venv\Lib\site-packages\numpy\lib\_function_base_impl.py", line 898, in select
    raise TypeError(msg) from None
TypeError: Choicelist and default value do not have a common dtype: The DType <class 'numpy.dtypes.StrDType'> could not be promoted by <class 'numpy.dtypes._PyLongDType'>. This means that no common DType exists for the given inputs. For example they cannot be stored in a single array unless the dtype is `object`. The full list of DTypes is: (<class 'numpy.dtypes.StrDType'>, <class 'numpy.dtypes._PyLongDType'>, <class 'numpy.dtypes._PyLongDType'>)
