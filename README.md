Absolutely. Here is a short, natural, stakeholder-speaking version for each one. You should be able to read these almost as-is without sounding like you’re reading a technical document.

1. EBITDA / (Interest Expense + CPLTD + Short Term Debt)

Floor = 0 | Cap = 1.25

“Here, we can see that as the ratio increases, the default rate generally comes down, so the relationship is quite intuitive. At the lower end, particularly below zero, the default rate is much higher, so we treat values below zero as the highest-risk group and set the floor at 0. At the higher end, the default rate has already come down substantially, and beyond around 1.25 the relationship becomes less meaningful and more noisy. So we cap the variable at 1.25. Essentially, we’re retaining the meaningful relationship in the middle and avoiding too much differentiation at the extremes.”

⸻

2. (Operating Profits + Selling Expense) / Total Assets

Floor = -0.60 | Cap = 0.35

“This variable also shows a clear inverse relationship with default — as the ratio improves, default rates generally come down. At the lower end, we see significantly higher default rates, so we set the floor at -0.60. We didn’t choose -0.47 because there is still meaningful risk differentiation between -0.60 and -0.47. At the higher end, once we get to around 0.35, default rates are already quite low and the remaining movement is more noise than a clear trend. So we set the cap at 0.35.”

⸻

3. Profit Before Taxes / (Total Assets − Total Liabilities)

Floor = -1.34 | Cap = -0.34

“Here again, the overall relationship is that higher values are associated with lower default rates. At the very negative end, default rates are substantially higher, so we set the floor at -1.34 and don’t allow increasingly extreme negative values to create additional differentiation. On the other side, the default rate continues to fall up to around -0.34, so we want to retain that relationship. Beyond -0.34, the default rate is already quite low and becomes more variable, so we set -0.34 as the cap.”

One sentence to remember for all three

If someone asks “What is the overall principle?”, say:

“We’re trying to retain the part of the variable where the data shows meaningful risk differentiation, while capping the extreme ends where the relationship becomes less reliable or increasingly noisy.”

That one sentence captures the whole methodology.