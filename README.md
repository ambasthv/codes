for var in var_list2:
    print(f"Processing: {var}")

    try:
        plot_predicted_actual2(
            df_id_bsd,
            var,
            'valid_def_ind_1yr',
            num_buckets=4,
            segment_var='lifestage_map2',
            variable=var,
            folder_name='Images',
            plot_axis='log',
            plot_ranges=False
        )

    except Exception as e:
        print(f"FAILED: {var}")
        print(e)