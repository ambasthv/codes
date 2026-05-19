Python code to create below, 
First filter the data by column model_routing= “ID/BSD”
Display chart and table in each steps. (make clear charts), 
1.	Stacked column chart using obligor_id (it is the id of a customer: object) for count, use riksunitnames (ID - Early Stage,ID - Mid Stage,Balance Sheet Dependent). Count against each risk unit name. (display table and chart)
2.	Stacked column chart using obligor_id (it is the id of a customer) for count, use riksunitnames (ID - Early Stage,ID - Mid Stage,Balance Sheet Dependent) use year starting till end and create time series). Name of chart: observation count by riskunitname and Grade date by Year, don’t use months. (display table and chart)
3.	Stacked column chart using obligor_id (is the id of a customer) for count and create time series using grade_date (datetime64[ns]: use year starting till end and create time series). Name of chart: observation count by riskunitname and Grade date by Year. (display table and chart)
4.	Stacked column chart using obligor_id (is the id of a customer) for count and create time series using grade_date (datetime64[ns]: use year and month (no date, just year and month) starting till end and create time series). Name of chart: observation count by riskunitname and Grade date by year/month. (display table and chart)
5.	Total “exposure” (float64 column, you can sum). Using riksunitnames (ID - Early Stage,ID - Mid Stage,Balance Sheet Dependent). Find total exposure in Y axis, for all dates. (don’t show dates here) (display table and chart)
6.	Total “balance” (float64 column, you can sum and count). Using riksunitnames (ID - Early Stage,ID - Mid Stage,Balance Sheet Dependent). Find total exposure in Y axis, for all dates. (don’t show dates here) (display table and chart)
7.	Balance vs exposure analysis. Create some chart to show comparison.(preferred stacked colm) by grade year (use year only not month) (display table and chart)
8.	Use “final_default_ind” (it has 0 and 1) count them against each riskunitname. Create column chart, (display table and chart) for all dates. Title: number of observation with default by riskunitname.
9.	Do distribution analysis of financial columns (count, mean median, mode, and any other statistical info), 
10.	Do Null analysis of each column, get total rows count, non null count, Null count, percentage of non null count. Display in chart for null count columns (like total col vs non null vs null)
11.	Use “final_default_ind” column (int32, it has value in 1 and 0), use sum, Default Rate by riskunitname, Default Rate by Grade Year, Default Rate by model_routing. Create table and chart and display them. 

Save all charts and table in excel (don’t save chart separately)

