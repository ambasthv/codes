import pyarrow.parquet as pq

parquet_path = "your_file.parquet"  # Change to your file path

# Get row count without loading full data
row_count = pq.read_table(parquet_path).num_rows

print(f"Total rows in parquet file: {row_count:,}")