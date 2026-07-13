so, this is the code i have that generates the charts, i want to add some code here to save all charts generated here in excel sheet, in seperate tabs with its respective chart name

lifestage_plot_datasets = {}

for var in var_list2:
    lifestage_plot_datasets[var] = plot_predicted_actual2(
        df_id_bsd,
        var,
        'valid_def_ind_1yr',
        num_buckets=10,
        segment_var='lifestage_map2',
        variable=var,
        folder_name='Images',
        plot_axis='log',
        plot_ranges=False)
