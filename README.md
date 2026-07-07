import numpy as np
import pandas as pd

def export_bucket_counts(
    df,
    variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts_By_Lifestage.xlsx'
):

    final_output = []

    for var in variables:

        # Remove missing values
        temp = df[[var, segment_var]].dropna().copy()

        # Same ranking logic as graph
        temp['rank'] = temp[var].rank(method='first')

        temp['x_bin'] = pd.qcut(
            temp['rank'],
            q=num_buckets,
            labels=False
        )

        # Same bin edges as graph
        bin_edges = np.quantile(
            temp[var],
            np.linspace(0, 1, num_buckets + 1)
        )

        # Remove duplicate edges if any
        bin_edges = np.unique(bin_edges)

        # Create readable labels
        labels = []

        for i in range(len(bin_edges)-1):
            labels.append(
                f"{bin_edges[i]:.4f} - {bin_edges[i+1]:.4f}"
            )

        # Map bucket number to label
        bucket_map = {
            i: labels[i]
            for i in range(len(labels))
        }

        temp['Bin'] = temp['x_bin'].map(bucket_map)

        # Count observations
        counts = (
            temp
            .groupby(['Bin', segment_var], observed=True)
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        # Keep original variable name
        counts.insert(0, 'Ratio', f'{var}_bin')

        final_output.append(counts)

    final_df = pd.concat(final_output, ignore_index=True)

    final_df.to_excel(output_file, index=False)

    print(f"Saved to {output_file}")

    return final_df




  variables = [
    'Gross Profit/Net Sales_x_100',
    'Net Profit/Net Sales_x_100',
    'Net Sales/Total Assets'
]

bucket_counts = export_bucket_counts(
    df_id_bsd,
    variables,
    segment_var='lifestage_map2',
    num_buckets=10,
    output_file='Bucket_Counts_By_Lifestage.xlsx'
)