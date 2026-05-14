# Fixed for newer numpy/pandas
uw_df['imputed_uw'] = uw_df['imputed_uw'].astype(str)
uw_df['imputed_method'] = np.where(
    uw_df['imputed_uw'] == 'blank', 
    np.nan, 
    'known'
)