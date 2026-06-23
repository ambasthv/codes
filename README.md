import pandas as pd
import numpy as np

def construct_ratio(df):
    
    df['capex'] = 0
    df['(EBITDA-Capex)/(Interest Expense+CPLTD)'] = (df['ebitda'] - df['capex']) / (df['interest_expense'] + df['cpltd'])
    #df['Total Debt/Equity'] = df['total_debt'] --confirm how this is calculated with Swati
    #df["(Cash+Marketable Securities+Net Accts Receivable Trade+Acct Receivable Other)/Current Liabilities"] = (df['cash'] + df['market_securities'] + df['acctsrecother'] + df['net_accounts_receivable']) / df['current_liabilities']
    #df["Quick Ratio*(Current Liabilities/(Current Liabilities-Deferred Revenue))"] = df["Quick Ratio"] * (df['current_liabilities']/(df['current_liabilities'] - df['deferred_revenue']))
    df['Net Profit/Net Sales_x_100'] = (df['net_profit'] / df['net_sales']) * 100

    return df


def apply_cleaning(df, variable_cleaning, null_treatment=False):
    """
    Apply various cleaning operations to specified variables based on defined rules.
    :param df: DataFrame containing the data to be cleaned.
    :param variable_cleaning: DataFrame containing the cleaning rules and configurations for each variable.
    :param grp_var: The name of the grouping variable/column used for aggregation in certain operations.
    :param special_value_dict: Dictionary containing special values for specific segments and variables.
    :param null_treatment: Boolean indicating whether to treat null values by filling them with calculated medians.
    :param special_null_treatment: Boolean indicating whether to apply special treatment for null values based on the provided dictionary.
    :param set_flags_to_0: Boolean indicating whether to reset all flags to 0 after processing.
    :param seg_list: List of segments for which special null treatment may be applied.
    :return: DataFrame with the cleaned variables and additional flag columns indicating the treatment applied.
    """
    for _, row in variable_cleaning.iterrows():
        variable = row['variable']
        floor_pct = row['floor_pct']
        floor_val = row['floor_val']
        cap_pct = row['cap_pct']
        cap_val = row['cap_val']
        negative_handling = row['negative_handling']
        zero_handling = row['zero_handling']
        positive_infinite_handling = row['positive_infinite_handling']
        negative_infinite_handling = row['negative_infinite_handling']
        special_cap_floor_treatment = row['special_cap_floor_treatment']

        # Nulls >>

        # Flag
        # Create a new column to flag values
        flag_col = f'{variable}_null_flag'
        df[flag_col] = 0
        # Flag the values
        df[flag_col] = np.where(df[variable].isna(), 1, 0)
        
        # Negatives >>

        # Flag
        # Create a new column to flag values
        flag_col = f'{variable}_negative_flag'
        df[flag_col] = 0       

        # Treat
        if negative_handling=='set to null':
            df.loc[lambda x: (x[variable]<0), flag_col] = 1
            df.loc[lambda x: (x[variable]<0), variable] = None
        elif negative_handling=='impute to median':
            df.loc[lambda x: (x[variable]<0), flag_col] = 1
            df.loc[lambda x: (x[variable]<0), variable] = median_by_group(df, variable)
        elif negative_handling=='set to max':
            df.loc[lambda x: (x[variable]<0), flag_col] = 1
            df.loc[lambda x: (x[variable]<0), variable] = 999999
        elif negative_handling=='set to min':
            df.loc[lambda x: (x[variable]<0), flag_col] = 1
            df.loc[lambda x: (x[variable]<0), variable] = -999999
               
        # Zeros >>

        # Flag
        # Create a new column to flag values
        flag_col = f'{variable}_zero_flag'
        df[flag_col] = 0

        # Treat
        if zero_handling=='set to null':
            df.loc[lambda x: (x[variable]==0), flag_col] = 1
            df.loc[lambda x: (x[variable]==0), variable] = None

        # Infinites >>

        # Flag
        # Create a new column to flag values
        flag_col = f'{variable}_inf_flag'
        df[flag_col] = 0

        # Treat
        if positive_infinite_handling =='set to max':
            df.loc[lambda x: (x[variable]== np.inf), flag_col] = 1
            df.loc[lambda x: (x[variable]== np.inf), variable] = 999999
        elif positive_infinite_handling =='set to null':
            df.loc[lambda x: (x[variable]== np.inf), flag_col] = 1
            df.loc[lambda x: (x[variable]== np.inf), variable] = None
        if negative_infinite_handling =='set to min':
            df.loc[lambda x: (x[variable]==-np.inf), flag_col] = 1
            df.loc[lambda x: (x[variable]==-np.inf), variable] = -999999
        elif negative_infinite_handling =='set to null':
            df.loc[lambda x: (x[variable]==-np.inf), flag_col] = 1
            df.loc[lambda x: (x[variable]==-np.inf), variable] = None

        # Cap and floor >>

        # Select variable column
        var_col = df[lambda x: (x[variable]!=-np.inf) & (x[variable]!=np.inf) & (x[variable]!=-999999) & (x[variable]!=999999)][variable]
     
        # Determine floor value
        if pd.notna(floor_pct) and pd.notna(floor_val):
            floor_value = max(var_col.quantile(floor_pct), floor_val)
        elif pd.notna(floor_pct):
            floor_value = var_col.quantile(floor_pct)
        else:
            floor_value = floor_val
        
        # Determine cap value
        if pd.notna(cap_pct) and pd.notna(cap_val):
            cap_value = min(var_col.quantile(cap_pct), cap_val)
        elif pd.notna(cap_pct):
            cap_value = var_col.quantile(cap_pct)
        else:
            cap_value = cap_val

        # Flag
        # Create a new column to flag values
        flag_col = f'{variable}_cap_floor_flag'
        df[flag_col] = 0
        # Flag the values
        df[flag_col] = np.where( (df[variable] < floor_value) | (df[variable] > cap_value) , 1, 0)

        # Cap & floor
        if special_cap_floor_treatment=='set to null':
            df.loc[df[variable] < floor_value, variable] = None
            df.loc[df[variable] > cap_value, variable] = None
        else:
            df[variable] = df[variable].clip(lower=floor_value, upper=cap_value)

        # Create invalid flag
        df[f'{variable}_invalid_flag'] = np.where( (df[f'{variable}_negative_flag']==1) | (df[f'{variable}_zero_flag']==1) | (df[f'{variable}_inf_flag']==1) , 1, 0)

        # Treat
        if null_treatment:
            df[variable] = df[variable].fillna(median_by_group(df, variable))

    return df


def median_by_group(df, variable):
    """
    Calculate the population-level median for a specified variable.
    :param df: DataFrame containing the data.
    :param variable: The name of the variable/column for which the median is to be computed.
    :return: The median value for the variable.
    """
    return df[variable].median()

def read_cleaning_xlsx(file_path, sheet_key='ratio_sheet'):
    """
    Read a single cleaning Excel sheet and return it in a dictionary.
    :param file_path: Path to the Excel file.
    :param sheet_key: Key from cfg['cleaning_sheets'] that identifies which tab to read.
    :return: Dictionary containing only the requested sheet.
    """
    sheet_name = 'ratio_variables'
    if not sheet_name:
        raise ValueError(f"No sheet configured for key: {sheet_key}")

    cleaning_excels = {
        sheet_key: pd.read_excel(
            io=file_path,
            sheet_name=sheet_name
        )
    }

    return cleaning_excels

def get_ratio_flag_counts(modeling_dataset, cleaning_excels, sheet_key='ratio_sheet'):
    """
    Build per-variable flag counts and percentages as a summary table.

    For each variable listed in cleaning_excels[sheet_key]['variable'] this computes:
    - total_obs
    - negative/inf/zero/null flag counts
    - negative/inf/zero/null flag percentages
    """
    ratio_variables = (
        cleaning_excels[sheet_key]['variable']
        .dropna()
        .astype(str)
        .tolist()
    )

    total_rows = len(modeling_dataset)
    rows = []

    for variable in ratio_variables:
        negative_col = f'{variable}_negative_flag'
        # Fallback for occasional misspelling in naming
        negative_col_alt = f'{variable}_negatve_flag'
        inf_col = f'{variable}_inf_flag'
        zero_col = f'{variable}_zero_flag'
        null_col = f'{variable}_null_flag'

        negative_count = 0
        if negative_col in modeling_dataset.columns:
            negative_count = int((modeling_dataset[negative_col] == 1).sum())
        elif negative_col_alt in modeling_dataset.columns:
            negative_count = int((modeling_dataset[negative_col_alt] == 1).sum())

        inf_count = int((modeling_dataset[inf_col] == 1).sum()) if inf_col in modeling_dataset.columns else 0
        zero_count = int((modeling_dataset[zero_col] == 1).sum()) if zero_col in modeling_dataset.columns else 0
        null_count = int((modeling_dataset[null_col] == 1).sum()) if null_col in modeling_dataset.columns else 0

        if total_rows > 0:
            negative_pct = (negative_count / total_rows) * 100
            inf_pct = (inf_count / total_rows) * 100
            zero_pct = (zero_count / total_rows) * 100
            null_pct = (null_count / total_rows) * 100
        else:
            negative_pct = 0.0
            inf_pct = 0.0
            zero_pct = 0.0
            null_pct = 0.0

        rows.append({
            'variable': variable,
            'total_obs': total_rows,
            'negative_flag_count': negative_count,
            'inf_flag_count': inf_count,
            'zero_flag_count': zero_count,
            'null_flag_count': null_count,
            'negative_flag_pct': round(negative_pct, 4),
            'inf_flag_pct': round(inf_pct, 4),
            'zero_flag_pct': round(zero_pct, 4),
            'null_flag_pct': round(null_pct, 4),
        })

    summary_df = pd.DataFrame(rows)
    return summary_df
