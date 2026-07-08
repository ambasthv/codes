# Software ID
df['arr_software_ind'] = np.select(
    [
        ~(df['lb'] == 'svb'),
        df['1205_niche_desc'] == 'SOFTWARE'
    ],
    [
        'N/A',
        '1'
    ],
    default='0'
)