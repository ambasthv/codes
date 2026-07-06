for var in valid_vars2:
    try:
        plot_predicted_actual2(
            df_id_bsd,
            var,
            'valid_def_ind_1yr',
            num_buckets=10,
            segment_var='lifestage_map2',
            variable=var,
            folder_name='Images',
            plot_axis='log',
            plot_ranges=False
        )
        print(f"✓ {var}")

    except Exception as e:
        print(f"✗ {var}")
        print(e)