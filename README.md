below is the explanation of a chart, its sample for you to undersand what exactly i want, read them, refer the attached picture, and ask if you have any questions.
once you have this understanding, i will share the another graphs and you need to wrtie exactly the same way what has been given in sample.
there is two parts, Statis= dont change anything, dynamic= based on the chart, (you have to understand how caps and floor is decided and same logic explain me which need to incorporate in charts i will give, 

Static:
To decide on these caps and floors, a visual assessment based on bivariate plots is conducted. These plots include both the actual default rates as well as predicted default rates post capping and flooring to allow for a visualization of the effect of the cap and floor. 

Imputed values (i.e., missing and invalids) were excluded from this analysis as the intention is to understand the underlying relationship between the factor and default with a high degree of confidence.

Additionally, it is important to note that the plots rely on rough decile bands as the number of defaults is relatively thin and any further granularity results in significant noise. 

Dynamic= based on the chart
As such, the bands where a cap or floor are being selected can be relatively wide, at which point a rounded number within the band is selected for the cap or floor.

The first variable assessed is EBITDA/(Interest Expense+CPLTD+Short Term Debt), as seen in the Figure below:

Figure 147: EBITDA/(Interest Expense+CPLTD+Short Term Debt) Bivariate Plot incl. Cap and Floor
  
As observed in the figure above, there is a relatively consistent decrease in default rate in EBITDA/(Interest Expense+CPLTD+Short Term Debt) from -0.01 to 1.25. 
Any obligor with a value below 0 would be considered at the riskiest level, and the same logic applied to the less risky bucket for obligors above the 0.85 to 1.25 bucket. 
Ultimately within the bucket a cap of 1.25 was selected as the upper bound within the bucket.

As such, the cap and floor for the variable were established at 1.25 and 0. These caps and floors are reflected on the dark blue line in the figure above and we can observe it captures the general trend of the behavior observed in the actuals (light blue line) but removes the noise around the edges.

