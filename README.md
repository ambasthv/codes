import os
import re

print("=== Count per Bin per Niche ===\n")

bin_cols = [
    'Gross Profit/Net Sales_x_100_bin',
    'Net Profit/Net Sales_x_100_bin',
    'Net Sales/Total Assets_bin'
]

for bin_col in bin_cols:

    if bin_col not in df.columns:
        continue

    count_df = (
        df.groupby([bin_col, 'niche_mapped'])
          .size()
          .unstack(fill_value=0)
          .reset_index()
    )

    count_df.rename(columns={bin_col: 'Bin'}, inplace=True)

    ratio_name = bin_col.replace('_winsor_bin', '')

    count_df.insert(0, 'Ratio', ratio_name)

    print(f"\n{ratio_name} - Counts per Bin:")
    print(count_df)

    output_dir = os.path.dirname(df_path)
    os.makedirs(output_dir, exist_ok=True)

    # Make filename Windows-safe
    safe_ratio_name = re.sub(r'[<>:"/\\|?*]', '_', ratio_name)

    output_path = os.path.join(
        output_dir,
        f"Bin_Counts_{safe_ratio_name}.xlsx"
    )

    count_df.to_excel(output_path, index=False)

    print(f"✅ Saved: {output_path}")

print("\n✅ All bin count tables saved successfully!")