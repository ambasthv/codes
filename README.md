import numpy as np

def construct_ratio_safe(df):
    df = df.copy()

    while True:
        try:
            return construct_ratio(df)

        except KeyError as e:
            missing_col = e.args[0]

            print(f"⚠️ Missing column: '{missing_col}'")
            print(f"   -> Creating '{missing_col}' with NaN and retrying...")

            df[missing_col] = np.nan





master_db = construct_ratio_safe(master_db)