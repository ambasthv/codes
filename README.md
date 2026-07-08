"C:\Program Files\Anaconda3_2024_10_1\python.exe" -m venv .venv

.\.venv\Scripts\Activate

python -c "import sys; print(sys.executable)"

python -m pip install pandas==2.2.2

python -c "import pandas as pd; print(pd.__version__)"