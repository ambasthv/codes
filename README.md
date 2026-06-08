print(df["adjquick"].apply(lambda x: "negative" if x < 0 else ("zero" if x == 0 else "positive")).value_counts())
