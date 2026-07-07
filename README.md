import numpy as np
import pandas as pd
import re

def export_bucket_counts(
    df,
    variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts.xlsx'
):

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

        for var in variables:

            print(f"Processing: {var}")

            temp = df[[var, segment_var]].dropna().copy()

            # Same bucketing logic as plot_predicted_actual2()
            temp['rank'] = temp[var].rank(method='first')

            temp['x_bin'] = pd.qcut(
                temp['rank'],
                q=num_buckets,
                labels=False
            )

            # Same bin edges used in the graph
            bin_edges = np.quantile(
                temp[var],
                np.linspace(0, 1, num_buckets + 1)
            )

            bin_edges = np.unique(bin_edges)

            labels = []

            for i in range(len(bin_edges)-1):
                labels.append(
                    f"{bin_edges[i]:,.4f} to {bin_edges[i+1]:,.4f}"
                )

            bucket_map = {
                i: labels[i]
                for i in range(len(labels))
            }

            temp['Bin'] = temp['x_bin'].map(bucket_map)

            count_df = (
                temp.groupby(['Bin', segment_var], observed=True)
                    .size()
                    .unstack(fill_value=0)
                    .reset_index()
            )

            # Preserve bucket order
            count_df['Bin'] = pd.Categorical(
                count_df['Bin'],
                categories=labels,
                ordered=True
            )

            count_df = count_df.sort_values('Bin')

            # Safe Excel sheet name
            sheet_name = re.sub(r'[\\/*?:\[\]]', '_', var)[:31]

            count_df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    print(f"\nWorkbook saved successfully:\n{output_file}")

------
 variables = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

export_bucket_counts(
    df=df_id_bsd,
    variables=variables,
    segment_var='niche_mapped',
    num_buckets=10,
    output_file='Bucket_Counts_By_Niche.xlsx'
)
-----
export_bucket_counts(
    df=df_id_bsd,
    variables=variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts_By_Lifestage.xlsx'
)