getting this error, for almost all the libraries, .venv  is created, and active also, but it is not in green colour, its same as another texts

(.venv) PS C:\Users\YWA95\OneDrive - First-Citizens Bank & Trust Co\1.OW\20July_OW> pip install pandas==2.2.2
Collecting pandas==2.2.2
  Using cached pandas-2.2.2.tar.gz (4.4 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [12 lines of output]
      + meson setup C:\Users\YWA95\AppData\Local\Temp\pip-install-ewh8l_71\pandas_32289be87bf34ee982e404fab4f3d56d C:\Users\YWA95\AppData\Local\Temp\pip-install-ewh8l_71\pandas_32289be87bf34ee982e404fab4f3d56d\.mesonpy-152w93ev\build -Dbuildtype=release -Db_ndebug=if-release -Db_vscrt=md --vsenv --native-file=C:\Users\YWA95\AppData\Local\Temp\pip-install-ewh8l_71\pandas_32289be87bf34ee982e404fab4f3d56d\.mesonpy-152w93ev\build\meson-python-native-file.ini
      The Meson build system
      Version: 1.2.1
      Source dir: C:\Users\YWA95\AppData\Local\Temp\pip-install-ewh8l_71\pandas_32289be87bf34ee982e404fab4f3d56d
      Build dir: C:\Users\YWA95\AppData\Local\Temp\pip-install-ewh8l_71\pandas_32289be87bf34ee982e404fab4f3d56d\.mesonpy-152w93ev\build
      Build type: native build
      Project name: pandas
      Project version: 2.2.2
      
      ..\..\meson.build:2:0: ERROR: Could not parse vswhere.exe output
      
      A full log can be found at C:\Users\YWA95\AppData\Local\Temp\pip-install-ewh8l_71\pandas_32289be87bf34ee982e404fab4f3d56d\.mesonpy-152w93ev\build\meson-logs\meson-log.txt
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> pandas

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
