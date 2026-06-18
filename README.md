---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[47], line 60
     56 fig.show()
     59 filename = f"Mean_Default_Line_{bin_col}.png"
---> 60 fig.write_image(os.path.join(os.path.dirname(df_path), filename))

File ~\AppData\Roaming\Python\Python312\site-packages\plotly\basedatatypes.py:3895, in BaseFigure.write_image(self, *args, **kwargs)
   3891     if kwargs.get("engine", None):
   3892         warnings.warn(
   3893             ENGINE_PARAM_DEPRECATION_MSG, DeprecationWarning, stacklevel=2
   3894         )
-> 3895 return pio.write_image(self, *args, **kwargs)

File ~\AppData\Roaming\Python\Python312\site-packages\plotly\io\_kaleido.py:528, in write_image(fig, file, format, scale, width, height, validate, engine)
    524 format = infer_format(path, format)
    526 # Request image
    527 # Do this first so we don't create a file if image conversion fails
--> 528 img_data = to_image(
    529     fig,
    530     format=format,
    531     scale=scale,
    532     width=width,
    533     height=height,
    534     validate=validate,
    535     engine=engine,
    536 )
    538 # Open file
    539 if path is None:
    540     # We previously failed to make sense of `file` as a pathlib object.
    541     # Attempt to write to `file` as an open file descriptor.

File ~\AppData\Roaming\Python\Python312\site-packages\plotly\io\_kaleido.py:345, in to_image(fig, format, width, height, scale, validate, engine)
    343     # Raise informative error message if Kaleido is not installed
    344     if not kaleido_available():
--> 345         raise ValueError(
    346             """
    347 Image export using the "kaleido" engine requires the Kaleido package,
    348 which can be installed using pip:
    349 
    350     $ pip install --upgrade kaleido
    351 """
    352         )
    354     # Convert figure to dict (and validate if requested)
    355     fig_dict = validate_coerce_fig_to_dict(fig, validate)

ValueError: 
Image export using the "kaleido" engine requires the Kaleido package,
which can be installed using pip:

    $ pip install --upgrade kaleido
