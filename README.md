df_id_bsd['niche_mapped'] = (
    df_id_bsd['1205_niche_desc']
        .map(niche_mapping)
        .fillna("OTHER")
)

print(df_id_bsd['niche_mapped'].value_counts()) 


export_bucket_counts(
    df=df_id_bsd,
    variables=variables,
    segment_var='niche_mapped',
    num_buckets=10,
    output_file='Bucket_Counts_By_Niche.xlsx'
) 