Great chart! Here’s everything you need to confidently present this.

What this chart is showing

This is a histogram of Balance values, coloured by Lifestage. Every bar represents a range of balance amounts, and the height tells you how many companies (records) fall in that range.

Reading the X axis
The X axis goes from 0B to 0.025B — so these are relatively small balance values (under $25 million). Most of the portfolio sits between 0 and 0.005B ($5 million or less). That tall spike on the left tells you the majority of companies have small outstanding balances.

Reading the Y axis
Y axis = count of records. The tallest bar reaches nearly 60,000 records — meaning roughly 60,000 facilities have a balance in that lowest range.

What the colours tell you
Each colour is a lifestage. From the chart you can see Early Stage (red) and Late Stage (blue) dominate the left side — meaning most small-balance facilities belong to these two segments. As you move right (larger balances), the bars get smaller and thinner — fewer companies have large balances.

The key story for management

Tell them three things:

First, the portfolio is heavily concentrated in small balances — the distribution is extremely right-skewed, meaning most borrowers have modest exposures but a small number have very large ones.

Second, Early Stage and Late Stage drive the volume — they have the most facilities and mostly at lower balance levels, which is expected for their risk profile.

Third, that lone pink bar at 0.025B on the far right — that is Large Corporate. Very few records but sitting at the highest balance range, meaning Large Corporates carry significantly bigger individual exposures even though they are fewer in number.

One line summary for management

“Most of our portfolio consists of small-balance Early and Late Stage facilities. However, our largest individual exposures belong to Large Corporates — fewer in count but significantly higher in balance size.”

The code that generates this

plot_df = df[["lifestage_mapped", "balance"]].dropna().copy()
plot_df["balance"] = clip_outliers(plot_df["balance"])        # removes extreme outliers
plot_df["bal_B"]   = plot_df["balance"] / 1e9                 # convert to billions

fig = px.histogram(plot_df, x="bal_B", color="lifestage_mapped",
                   nbins=30, barmode="overlay", opacity=0.6,
                   title="Balance — Histogram by Lifestage",
                   labels={"bal_B":"Balance (Billions $)",
                           "lifestage_mapped":"Lifestage"},
                   template="plotly_white", height=430)
fig.show()


clip_outliers removes the top and bottom 1% so extreme values don’t squash the chart. barmode="overlay" stacks all lifestages on the same axis so you can compare shapes. opacity=0.6 makes overlapping colours visible.