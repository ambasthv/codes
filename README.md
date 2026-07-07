import numpy as np
import pandas as pd

def export_bucket_counts(
    df,
    variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts.xlsx'
):

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

        for var in variables:

            temp = df[[var, segment_var]].dropna().copy()

            # Same bucketing logic as graph
            temp['rank'] = temp[var].rank(method='first')

            temp['x_bin'] = pd.qcut(
                temp['rank'],
                q=num_buckets,
                labels=False
            )

            # Same bin edges used in graph
            bin_edges = np.quantile(
                temp[var],
                np.linspace(0, 1, num_buckets + 1)
            )

            bin_edges = np.unique(bin_edges)

            labels = [
                f"{bin_edges[i]:.4f} - {bin_edges[i+1]:.4f}"
                for i in range(len(bin_edges)-1)
            ]

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

            # Put Bin as first column
            cols = ['Bin'] + [c for c in count_df.columns if c != 'Bin']
            count_df = count_df[cols]

            # Excel sheet names cannot exceed 31 characters
            sheet_name = var[:31]

            count_df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    print(f"\nWorkbook saved as: {output_file}")

-------
variables = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

export_bucket_counts(
    df=df,
    variables=variables,
    segment_var='niche_mapped',
    num_buckets=10,
    output_file='Bucket_Counts_By_Niche.xlsx'
)
--------
export_bucket_counts(
    df=df_id_bsd,
    variables=variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts_By_Lifestage.xlsx'
)n