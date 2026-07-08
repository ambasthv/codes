actually this is the code thre in 895 rows

    # Software ID
    df['arr_software_ind'] = np.select(
        [
            ~(df['lb'] == 'svb'),
            df['1205_niche_desc'] == 'SOFTWARE'
        ],
        [
            'N/A', 
            1
        ],
        0
    )

  now tell me what to correct, give me complete one 
