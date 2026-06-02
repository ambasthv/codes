def plot_distributions(df_filt, ratio_cols, segment_col='lifestage'):
    for ratio in ratio_cols:
        if ratio not in df_filt.columns:
            continue
            
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Box Plot
        sns.boxplot(data=df_filt, x=segment_col, y=ratio, ax=axes[0])
        axes[0].set_title(f'Box Plot - {ratio} by {segment_col}')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Histogram
        sns.histplot(data=df_filt, x=ratio, hue=segment_col, kde=True, ax=axes[1])
        axes[1].set_title(f'Distribution - {ratio}')
        
        plt.tight_layout()
        plt.savefig(f"{output_folder}/{ratio}_distribution.png", dpi=300, bbox_inches='tight')
        plt.show()   # This will show chart in VS Code / Jupyter

plot_distributions(df_filt, target_ratios)
