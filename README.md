new error in same code

---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
File ~\AppData\Roaming\Python\Python312\site-packages\matplotlib\style\__init__.py:130, in use(style)
    129 try:
--> 130     style = rc_params_from_file(style, use_default_template=False)
    131 except OSError as err:

File ~\AppData\Roaming\Python\Python312\site-packages\matplotlib\__init__.py:968, in rc_params_from_file(fname, fail_on_error, use_default_template)
    954 """
    955 Construct a `RcParams` from file *fname*.
    956 
   (...)
    966     parameters specified in the file. (Useful for updating dicts.)
    967 """
--> 968 config_from_file = _rc_params_in_file(fname, fail_on_error=fail_on_error)
    970 if not use_default_template:

File ~\AppData\Roaming\Python\Python312\site-packages\matplotlib\__init__.py:900, in _rc_params_in_file(fname, transform, fail_on_error)
    899 rc_temp = {}
--> 900 with _open_file_or_url(fname) as fd:
    901     try:

File c:\Program Files\Anaconda3_2024_10_1\Lib\contextlib.py:137, in _GeneratorContextManager.__enter__(self)
    136 try:
--> 137     return next(self.gen)
...
    135             f"styles are listed in `style.available`)") from err
    136 filtered = {}
    137 for k in style:  # don't trigger RcParams.__getitem__('backend')

OSError: 'C:/Users/ZRR28/Dev/dev-id-bsd-model/01. Code/model_development/utils/resources/ow_style.mplstyle' is not a valid package style, path of style file, URL of style file, or library style name (library styles are listed in `style.available`)
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
