# %% [markdown]
# ### DRR Models Input PSI Calculator

# %% [markdown]
# #### This code calculates Input PSI  portfolio for DRR Models (GFB CCLOC, GFB NAV, GFB Firm, Large Corp, Mid Size, Early Stage, GFB Firm) 

# %%
#import libraries required

import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.3f}'.format
pd.set_option('display.max_columns',None)

import pyodbc

import gc

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator, ScalarFormatter)
import matplotlib.backends.backend_pdf as pdf_backend

from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta 
import timeit

import statsmodels.api as sm
import statsmodels.formula.api as smf

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score, recall_score, precision_score
from sklearn.metrics import average_precision_score, f1_score, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import RocCurveDisplay
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.datasets import make_classification
from sklearn.metrics import roc_curve
from warnings import filterwarnings
from sklearn.utils import resample
from scipy import stats

import warnings
#from pandas.errors import SettingWithCopyWarning 
#warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')

start = datetime.now()
#print(start)

# %%
#download Model Rating Data
ccloc_raw_ncino = pd.read_csv('gfb_ccloc_rating_data.csv')
nav_raw_ncino = pd.read_csv('gfb_nav_rating_data.csv')
large_corp_raw_ncino = pd.read_csv('large_corp_rating_data.csv')
mid_size_raw_ncino = pd.read_csv('mid_size_rating_data.csv')
early_stage_raw_ncino = pd.read_csv('early_stage_rating_data.csv')
gfb_firm_raw_ncino = pd.read_csv('gfb_firm_rating_data.csv')


# %%
column_list_gfb = ['LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.LLC_BI__Status__c', 
               'LLC_BI__Risk_Grade_Factor_Name__c', 'LLC_BI__Qualitative_Value__c',
                 'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.Calculated_ORR__c',
       'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.Final_ORR__c',
           'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.LLC_BI__Account__r.CIF__c',
           'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.Credit_Package__r.Credit_Package_Number__c',
           'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.CreatedDate']


column_list_iv = ['LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.LLC_BI__Status__c', 
               'LLC_BI__Risk_Grade_Factor_Name__c', 'LLC_BI__Qualitative_Value__c', 'LLC_BI__Quantitative_Value__c',
                 'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.Calculated_ORR__c',
       'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.Final_ORR__c',
           'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.LLC_BI__Account__r.CIF__c',
           'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.LLC_BI__Risk_Rating_Review__r.Credit_Package__r.Credit_Package_Number__c',
           'LLC_BI__Risk_Grade_Factor__r.LLC_BI__Risk_Grade_Template__r.CreatedDate']

new_name_gfb = ['Status','Factor_Name','Factor_Value','Calc_ORR','Final_ORR','CIF',	'CPNumber',	'Date']

new_name_iv = ['Status','Factor_Name','Factor_Value_Qual','Factor_Value_Quant','Calc_ORR','Final_ORR','CIF','CPNumber','Date']

# %%
ccloc_raw = ccloc_raw_ncino[column_list_gfb]
nav_raw = nav_raw_ncino[column_list_gfb]
gfb_firm_raw = gfb_firm_raw_ncino[column_list_iv]
large_corp_raw = large_corp_raw_ncino[column_list_iv]
mid_size_raw = mid_size_raw_ncino[column_list_iv]
early_stage_raw = early_stage_raw_ncino[column_list_iv]


ccloc_raw.columns = new_name_gfb
nav_raw.columns = new_name_gfb
gfb_firm_raw.columns = new_name_iv
large_corp_raw.columns = new_name_iv
early_stage_raw.columns = new_name_iv
mid_size_raw.columns = new_name_iv

# %%
#download Model Rating Data



ccloc_all = ccloc_raw.loc[ccloc_raw.Status == 'Approved']

ccloc_all = ccloc_all.loc[:, ~ccloc_all.columns.str.contains('^Unnamed')]
ccloc_all = ccloc_all.drop_duplicates()



nav_all = nav_raw.loc[nav_raw.Status == 'Approved']


nav_all = nav_all.loc[:, ~nav_all.columns.str.contains('^Unnamed')]
nav_all = nav_all.drop_duplicates()




large_corp_all_approved = large_corp_raw.loc[large_corp_raw.Status == 'Approved']


large_corp_all = large_corp_all_approved.loc[:, ~large_corp_all_approved.columns.str.contains('^Unnamed')]
large_corp_all = large_corp_all.drop_duplicates()



mid_size_all_approved = mid_size_raw.loc[mid_size_raw.Status == 'Approved']


mid_size_all = mid_size_all_approved.loc[:, ~mid_size_all_approved.columns.str.contains('^Unnamed')]
mid_size_all = mid_size_all.drop_duplicates()



early_stage_all_approved = early_stage_raw.loc[early_stage_raw.Status == 'Approved']


early_stage_all = early_stage_all_approved.loc[:, ~early_stage_all_approved.columns.str.contains('^Unnamed')]
early_stage_all = early_stage_all.drop_duplicates()



gfb_firm_all_approved = gfb_firm_raw.loc[gfb_firm_raw.Status == 'Approved']


gfb_firm_all = gfb_firm_all_approved.loc[:, ~gfb_firm_all_approved.columns.str.contains('^Unnamed')]
gfb_firm_all = gfb_firm_all.drop_duplicates()


# %%
#download Model Benchmark Data


benchmark_ccloc_raw = pd.read_csv('gfb_ccloc_rating_data_benchmark.csv')
ccloc_all_benchmark = benchmark_ccloc_raw.loc[benchmark_ccloc_raw.Status == 'Approved']

ccloc_all_benchmark = ccloc_all_benchmark.loc[:, ~ccloc_all_benchmark.columns.str.contains('^Unnamed')]
ccloc_all_benchmark = ccloc_all_benchmark.drop_duplicates()


df1_PSI = pd.read_csv('gfb_nav_rating_data_benchmark.csv')
nav_benchmark_all = df1_PSI.loc[df1_PSI.Status == 'Approved']

nav_benchmark_all = nav_benchmark_all.loc[:, ~nav_benchmark_all.columns.str.contains('^Unnamed')]
nav_benchmark_all = nav_benchmark_all.drop_duplicates()

large_corp_raw = pd.read_csv('large_corp_rating_data_benchmark.csv')

large_corp_all_benchmark_approved = large_corp_raw.loc[large_corp_raw.Status == 'Approved']


large_corp_all_benchmark = large_corp_all_benchmark_approved.loc[:, ~large_corp_all_benchmark_approved.columns.str.contains('^Unnamed')]
large_corp_all_benchmark = large_corp_all_benchmark.drop_duplicates()

mid_size_raw = pd.read_csv('mid_size_rating_data_benchmark.csv')

mid_size_all_benchmark_approved = mid_size_raw.loc[mid_size_raw.Status == 'Approved']


mid_size_all_benchmark = mid_size_all_benchmark_approved.loc[:, ~mid_size_all_benchmark_approved.columns.str.contains('^Unnamed')]
mid_size_all_benchmark = mid_size_all_benchmark.drop_duplicates()

early_stage_raw = pd.read_csv('early_stage_rating_data_benchmark.csv')

early_stage_all_benchmark_approved = early_stage_raw.loc[early_stage_raw.Status == 'Approved']


early_stage_all_benchmark = early_stage_all_benchmark_approved.loc[:, ~early_stage_all_benchmark_approved.columns.str.contains('^Unnamed')]
early_stage_all_benchmark = early_stage_all_benchmark.drop_duplicates()



gfb_firm_all_benchmark_approved = gfb_firm_raw.loc[gfb_firm_raw.Status == 'Approved']


gfb_firm_all_benchmark = gfb_firm_all_benchmark_approved.loc[:, ~gfb_firm_all_benchmark_approved.columns.str.contains('^Unnamed')]
gfb_firm_all_benchmark = gfb_firm_all_benchmark.drop_duplicates()

# %%


# %%

#GFB CCLOC Rating data

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

ccloc_factor1 = ccloc_all.loc[ccloc_all.Factor_Name == 'Fund Performance']
ccloc_factor2 = ccloc_all.loc[ccloc_all.Factor_Name == 'LP Capacity']
ccloc_factor3 = ccloc_all.loc[ccloc_all.Factor_Name == 'LP Diversification']
ccloc_factor4 = ccloc_all.loc[ccloc_all.Factor_Name == 'Management Experience']

ccloc_factor1['Factor_Value1']  = pd.factorize(ccloc_factor1['Factor_Value'])[0]
ccloc_factor2['Factor_Value1']  = pd.factorize(ccloc_factor2['Factor_Value'])[0]
ccloc_factor3['Factor_Value1']  = pd.factorize(ccloc_factor3['Factor_Value'])[0]
ccloc_factor4['Factor_Value1']  = pd.factorize(ccloc_factor4['Factor_Value'])[0]



ccloc_factor1_1 = ccloc_factor1.rename(columns = {'Factor_Value1': 'Fund_Performance' })
ccloc_factor2_1 = ccloc_factor2.rename(columns = {'Factor_Value1': 'LP_Capacity' })
ccloc_factor3_1 = ccloc_factor3.rename(columns = {'Factor_Value1': 'LP_Diversification' })
ccloc_factor4_1 = ccloc_factor4.rename(columns = {'Factor_Value1': 'Management_Experience' })



ccloc_factor1_2 = ccloc_factor1_1.drop(['Factor_Name', 'Status', 'Factor_Value'], axis = 1)
ccloc_factor2_2 = ccloc_factor2_1.drop(['Factor_Name', 'Status', 'Factor_Value'], axis = 1)
ccloc_factor3_2 = ccloc_factor3_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
ccloc_factor4_2 = ccloc_factor4_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)

ccloc_all2 = pd.merge(ccloc_factor1_2, ccloc_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

ccloc_all3 = pd.merge(ccloc_all2, ccloc_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


ccloc_final = pd.merge(ccloc_all3, ccloc_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

ccloc_final2 = ccloc_final.drop_duplicates().copy()

ccloc_final2['Date'] = pd.to_datetime(ccloc_final2['Date'])

ccloc_final2['loaddt'] = ccloc_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

ccloc_final2 = ccloc_final2.rename(columns = { 'CIF': 'cif'})
ccloc_final3 = ccloc_final2.copy()



# %%
#GFB CCLOC benchmark data

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

ccloc_benchmark_factor1 = ccloc_all_benchmark.loc[ccloc_all_benchmark.Factor_Name == 'Fund Performance']
ccloc_benchmark_factor2 = ccloc_all_benchmark.loc[ccloc_all_benchmark.Factor_Name == 'LP Capacity']
ccloc_benchmark_factor3 = ccloc_all_benchmark.loc[ccloc_all_benchmark.Factor_Name == 'LP Diversification']
ccloc_benchmark_factor4 = ccloc_all_benchmark.loc[ccloc_all_benchmark.Factor_Name == 'Management Experience']

ccloc_benchmark_factor1['Factor_Value1']  = pd.factorize(ccloc_benchmark_factor1['Factor_Value'])[0]
ccloc_benchmark_factor2['Factor_Value1']  = pd.factorize(ccloc_benchmark_factor2['Factor_Value'])[0]
ccloc_benchmark_factor3['Factor_Value1']  = pd.factorize(ccloc_benchmark_factor3['Factor_Value'])[0]
ccloc_benchmark_factor4['Factor_Value1']  = pd.factorize(ccloc_benchmark_factor4['Factor_Value'])[0]




ccloc_benchmark_factor1_1 = ccloc_benchmark_factor1.rename(columns = {'Factor_Value1': 'Fund_Performance' })
ccloc_benchmark_factor2_1 = ccloc_benchmark_factor2.rename(columns = {'Factor_Value1': 'LP_Capacity' })
ccloc_benchmark_factor3_1 = ccloc_benchmark_factor3.rename(columns = {'Factor_Value1': 'LP_Diversification' })
ccloc_benchmark_factor4_1 = ccloc_benchmark_factor4.rename(columns = {'Factor_Value1': 'Management_Experience' })

ccloc_benchmark_factor1_2 = ccloc_benchmark_factor1_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
ccloc_benchmark_factor2_2 = ccloc_benchmark_factor2_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
ccloc_benchmark_factor3_2 = ccloc_benchmark_factor3_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
ccloc_benchmark_factor4_2 = ccloc_benchmark_factor4_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)

ccloc_benchmark_all2 = pd.merge(ccloc_benchmark_factor1_2, ccloc_benchmark_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

ccloc_benchmark_all3 = pd.merge(ccloc_benchmark_all2, ccloc_benchmark_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


ccloc_benchmark_final = pd.merge(ccloc_benchmark_all3, ccloc_benchmark_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

ccloc_benchmark_final2 = ccloc_benchmark_final.drop_duplicates().copy()

ccloc_benchmark_final2['Date'] = pd.to_datetime(ccloc_benchmark_final2['Date'])

ccloc_benchmark_final2['loaddt'] = ccloc_benchmark_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

ccloc_benchmark_final2 = ccloc_benchmark_final2.rename(columns = { 'CIF': 'cif'})








# %%
#GFB NAV Rating data

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

nav_factor1 = nav_all.loc[nav_all.Factor_Name == 'Exit Environment']
nav_factor2 = nav_all.loc[nav_all.Factor_Name == 'Asset Diversification']
nav_factor3 = nav_all.loc[nav_all.Factor_Name == 'Industry Concentration']
nav_factor4 = nav_all.loc[nav_all.Factor_Name == 'Asset Coverage']
nav_factor5 = nav_all.loc[nav_all.Factor_Name == 'Manager Quality']

nav_factor1['Factor_Value1']  = pd.factorize(nav_factor1['Factor_Value'])[0]
nav_factor2['Factor_Value1']  = pd.factorize(nav_factor2['Factor_Value'])[0]
nav_factor3['Factor_Value1']  = pd.factorize(nav_factor3['Factor_Value'])[0]
nav_factor4['Factor_Value1']  = pd.factorize(nav_factor4['Factor_Value'])[0]
nav_factor5['Factor_Value1']  = pd.factorize(nav_factor5['Factor_Value'])[0]

nav_factor1_1 = nav_factor1.rename(columns = {'Factor_Value1': 'Exit_Environment' })
nav_factor2_1 = nav_factor2.rename(columns = {'Factor_Value1': 'Asset_Diversification' })
nav_factor3_1 = nav_factor3.rename(columns = {'Factor_Value1': 'Industry_Concentration' })
nav_factor4_1 = nav_factor4.rename(columns = {'Factor_Value1': 'Asset_Coverage' })
nav_factor5_1 = nav_factor5.rename(columns = {'Factor_Value1': 'Manager_Quality' })

nav_factor1_2 = nav_factor1_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_factor2_2 = nav_factor2_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_factor3_2 = nav_factor3_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_factor4_2 = nav_factor4_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_factor5_2 = nav_factor5_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)

nav_all2 = pd.merge(nav_factor1_2, nav_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

nav_all3 = pd.merge(nav_all2, nav_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


nav_all4 = pd.merge(nav_all3, nav_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

nav_final = pd.merge(nav_all4, nav_factor5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

nav_final2 = nav_final.drop_duplicates().copy()

nav_final2['Date'] = pd.to_datetime(nav_final2['Date'])

nav_final2['loaddt'] = nav_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

nav_final2 = nav_final2.rename(columns = { 'CIF': 'cif'})
nav_final3 = nav_final2.copy()



# %%
#GFB NAV Benchmark data


#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

nav_benchmark_factor1 = nav_benchmark_all.loc[nav_benchmark_all.Factor_Name == 'Exit Environment']
nav_benchmark_factor2 = nav_benchmark_all.loc[nav_benchmark_all.Factor_Name == 'Asset Diversification']
nav_benchmark_factor3 = nav_benchmark_all.loc[nav_benchmark_all.Factor_Name == 'Industry Concentration']
nav_benchmark_factor4 = nav_benchmark_all.loc[nav_benchmark_all.Factor_Name == 'Asset Coverage']
nav_benchmark_factor5 = nav_benchmark_all.loc[nav_benchmark_all.Factor_Name == 'Manager Quality']

nav_benchmark_factor1['Factor_Value1'] = pd.factorize(nav_benchmark_factor1['Factor_Value'])[0]
nav_benchmark_factor2['Factor_Value1'] = pd.factorize(nav_benchmark_factor2['Factor_Value'])[0]
nav_benchmark_factor3['Factor_Value1'] = pd.factorize(nav_benchmark_factor3['Factor_Value'])[0]
nav_benchmark_factor4['Factor_Value1'] = pd.factorize(nav_benchmark_factor4['Factor_Value'])[0]
nav_benchmark_factor5['Factor_Value1'] = pd.factorize(nav_benchmark_factor5['Factor_Value'])[0]





nav_benchmark_factor1_1 = nav_benchmark_factor1.rename(columns = {'Factor_Value1': 'Exit_Environment' })
nav_benchmark_factor2_1 = nav_benchmark_factor2.rename(columns = {'Factor_Value1': 'Asset_Diversification' })
nav_benchmark_factor3_1 = nav_benchmark_factor3.rename(columns = {'Factor_Value1': 'Industry_Concentration' })
nav_benchmark_factor4_1 = nav_benchmark_factor4.rename(columns = {'Factor_Value1': 'Asset_Coverage' })
nav_benchmark_factor5_1 = nav_benchmark_factor5.rename(columns = {'Factor_Value1': 'Manager_Quality' })

nav_benchmark_factor1_2 = nav_benchmark_factor1_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_benchmark_factor2_2 = nav_benchmark_factor2_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_benchmark_factor3_2 = nav_benchmark_factor3_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_benchmark_factor4_2 = nav_benchmark_factor4_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)
nav_benchmark_factor5_2 = nav_benchmark_factor5_1.drop(['Factor_Name', 'Status','Factor_Value'], axis = 1)

nav_benchmark_all2 = pd.merge(nav_benchmark_factor1_2, nav_benchmark_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

nav_benchmark_all3 = pd.merge(nav_benchmark_all2, nav_benchmark_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


nav_benchmark_all4 = pd.merge(nav_benchmark_all3, nav_benchmark_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

nav_benchmark_final = pd.merge(nav_benchmark_all4, nav_benchmark_factor5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

nav_benchmark_final2 = nav_benchmark_final.drop_duplicates().copy()

nav_benchmark_final2['Date'] = pd.to_datetime(nav_benchmark_final2['Date'])

nav_benchmark_final2['loaddt'] = nav_benchmark_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

nav_benchmark_final2 = nav_benchmark_final2.rename(columns = { 'CIF': 'cif'})
nav_benchmark_final3 = nav_benchmark_final2.copy()

# %%
#Large Corp 

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

large_corp_factor1 = large_corp_all.loc[large_corp_all.Factor_Name == 'Profitability - Gross Margin %']
large_corp_factor2 = large_corp_all.loc[large_corp_all.Factor_Name == 'Scale - Revenue (Thousands)']
large_corp_factor3 = large_corp_all.loc[large_corp_all.Factor_Name == 'Leverage - Total Funded Debt to EBITDA']
large_corp_factor4 = large_corp_all.loc[large_corp_all.Factor_Name == 'Liquidity - Current Ratio']
large_corp_factor5 = large_corp_all.loc[large_corp_all.Factor_Name == 'Coverage - FCCR']

large_corp_factor1['Factor_Value_Quant1'] = pd.factorize(large_corp_factor1['Factor_Value_Quant'])[0]
large_corp_factor2['Factor_Value_Quant1'] = pd.factorize(large_corp_factor2['Factor_Value_Quant'])[0]
large_corp_factor3['Factor_Value_Quant1'] = pd.factorize(large_corp_factor3['Factor_Value_Quant'])[0]
large_corp_factor4['Factor_Value_Quant1'] = pd.factorize(large_corp_factor4['Factor_Value_Quant'])[0]
large_corp_factor5['Factor_Value_Quant1'] = pd.factorize(large_corp_factor5['Factor_Value_Quant'])[0]



large_corp_factor1.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor2.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor3.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor4.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor5.drop('Factor_Value_Qual', axis=1, inplace=True)

large_corp_factor1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor3.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor4.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor5.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


large_corp_factor6 = large_corp_all.loc[large_corp_all.Factor_Name == 'Financial Factors / Access to Capital']
large_corp_factor7 = large_corp_all.loc[large_corp_all.Factor_Name == 'Management Evaluation']
large_corp_factor8 = large_corp_all.loc[large_corp_all.Factor_Name == 'Cashflow Stability']
large_corp_factor9 = large_corp_all.loc[large_corp_all.Factor_Name == 'Industry / Competitive Dynamics']


large_corp_factor6['Factor_Value_Qual1'] = pd.factorize(large_corp_factor6['Factor_Value_Qual'])[0]
large_corp_factor7['Factor_Value_Qual1'] = pd.factorize(large_corp_factor7['Factor_Value_Qual'])[0]
large_corp_factor8['Factor_Value_Qual1'] = pd.factorize(large_corp_factor8['Factor_Value_Qual'])[0]
large_corp_factor9['Factor_Value_Qual1'] = pd.factorize(large_corp_factor9['Factor_Value_Qual'])[0]

large_corp_factor6.drop('Factor_Value_Quant', axis=1, inplace=True)
large_corp_factor7.drop('Factor_Value_Quant', axis=1, inplace=True)
large_corp_factor8.drop('Factor_Value_Quant', axis=1, inplace=True)
large_corp_factor9.drop('Factor_Value_Quant', axis=1, inplace=True)

large_corp_factor6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
large_corp_factor7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
large_corp_factor8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
large_corp_factor9.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




large_corp_factor1_1 = large_corp_factor1.rename(columns = {'Factor_Value': 'Gross_Margin' })
large_corp_factor2_1 = large_corp_factor2.rename(columns = {'Factor_Value': 'Scale' })
large_corp_factor3_1 = large_corp_factor3.rename(columns = {'Factor_Value': 'TDEBITDA' })
large_corp_factor4_1 = large_corp_factor4.rename(columns = {'Factor_Value': 'Current_Ratio' })
large_corp_factor5_1 = large_corp_factor5.rename(columns = {'Factor_Value': 'FCCR' })

large_corp_factor6_1 = large_corp_factor6.rename(columns = {'Factor_Value': 'Capital' })
large_corp_factor7_1 = large_corp_factor7.rename(columns = {'Factor_Value': 'Management' })
large_corp_factor8_1 = large_corp_factor8.rename(columns = {'Factor_Value': 'Cashflow' })
large_corp_factor9_1 = large_corp_factor9.rename(columns = {'Factor_Value': 'Industry' })

large_corp_factor1_2 = large_corp_factor1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
large_corp_factor2_2 = large_corp_factor2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
large_corp_factor3_2 = large_corp_factor3_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
large_corp_factor4_2 = large_corp_factor4_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
large_corp_factor5_2 = large_corp_factor5_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)

large_corp_factor6_2 = large_corp_factor6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
large_corp_factor7_2 = large_corp_factor7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
large_corp_factor8_2 = large_corp_factor8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
large_corp_factor9_2 = large_corp_factor9_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)



large_corp_all2 = pd.merge(large_corp_factor1_2, large_corp_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

large_corp_all3 = pd.merge(large_corp_all2, large_corp_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


large_corp_all4 = pd.merge(large_corp_all3, large_corp_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

large_corp_all5 = pd.merge(large_corp_all4, large_corp_factor5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_all6 = pd.merge(large_corp_all5, large_corp_factor6_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_all7 = pd.merge(large_corp_all6, large_corp_factor7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_all8 = pd.merge(large_corp_all7, large_corp_factor8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_final = pd.merge(large_corp_all8, large_corp_factor9_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')









large_corp_final2 = large_corp_final.drop_duplicates().copy()

large_corp_final2['Date'] = pd.to_datetime(large_corp_final2['Date'])

large_corp_final2['loaddt'] = large_corp_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

large_corp_final2 = large_corp_final2.rename(columns = { 'CIF': 'cif'})
large_corp_final3 = large_corp_final2.copy()




# %%
large_corp_factor4_2.columns

# %%
#Large Corp Benchmark

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

large_corp_factor_benchmark1 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Profitability - Gross Margin %']
large_corp_factor_benchmark2 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Scale - Revenue (Thousands)']
large_corp_factor_benchmark3 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Leverage - Total Funded Debt to EBITDA']
large_corp_factor_benchmark4 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Liquidity - Current Ratio']
large_corp_factor_benchmark5 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Coverage - FCCR']


large_corp_factor_benchmark1['Factor_Value_Quant1'] = pd.factorize(large_corp_factor_benchmark1['Factor_Value_Quant'])[0]
large_corp_factor_benchmark2['Factor_Value_Quant1'] = pd.factorize(large_corp_factor_benchmark2['Factor_Value_Quant'])[0]
large_corp_factor_benchmark3['Factor_Value_Quant1'] = pd.factorize(large_corp_factor_benchmark3['Factor_Value_Quant'])[0]
large_corp_factor_benchmark4['Factor_Value_Quant1'] = pd.factorize(large_corp_factor_benchmark4['Factor_Value_Quant'])[0]
large_corp_factor_benchmark5['Factor_Value_Quant1'] = pd.factorize(large_corp_factor_benchmark5['Factor_Value_Quant'])[0]




large_corp_factor_benchmark1.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor_benchmark2.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor_benchmark3.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor_benchmark4.drop('Factor_Value_Qual', axis=1, inplace=True)
large_corp_factor_benchmark5.drop('Factor_Value_Qual', axis=1, inplace=True)


large_corp_factor_benchmark1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark3.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark4.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark5.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


large_corp_factor_benchmark6 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Financial Factors / Access to Capital']
large_corp_factor_benchmark7 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Management Evaluation']
large_corp_factor_benchmark8 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Cashflow Stability']
large_corp_factor_benchmark9 = large_corp_all_benchmark.loc[large_corp_all_benchmark.Factor_Name == 'Industry / Competitive Dynamics']

large_corp_factor_benchmark6['Factor_Value_Qual1'] = pd.factorize(large_corp_factor_benchmark6['Factor_Value_Qual'])[0]
large_corp_factor_benchmark7['Factor_Value_Qual1'] = pd.factorize(large_corp_factor_benchmark7['Factor_Value_Qual'])[0]
large_corp_factor_benchmark8['Factor_Value_Qual1'] = pd.factorize(large_corp_factor_benchmark8['Factor_Value_Qual'])[0]
large_corp_factor_benchmark9['Factor_Value_Qual1'] = pd.factorize(large_corp_factor_benchmark9['Factor_Value_Qual'])[0]






large_corp_factor_benchmark6.drop('Factor_Value_Quant', axis=1, inplace=True)
large_corp_factor_benchmark7.drop('Factor_Value_Quant', axis=1, inplace=True)
large_corp_factor_benchmark8.drop('Factor_Value_Quant', axis=1, inplace=True)
large_corp_factor_benchmark9.drop('Factor_Value_Quant', axis=1, inplace=True)

large_corp_factor_benchmark6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
large_corp_factor_benchmark9.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




large_corp_factor_benchmark1_1 = large_corp_factor_benchmark1.rename(columns = {'Factor_Value': 'Gross_Margin' })
large_corp_factor_benchmark2_1 = large_corp_factor_benchmark2.rename(columns = {'Factor_Value': 'Scale' })
large_corp_factor_benchmark3_1 = large_corp_factor_benchmark3.rename(columns = {'Factor_Value': 'TDEBITDA' })
large_corp_factor_benchmark4_1 = large_corp_factor_benchmark4.rename(columns = {'Factor_Value': 'Current_Ratio' })
large_corp_factor_benchmark5_1 = large_corp_factor_benchmark5.rename(columns = {'Factor_Value': 'FCCR' })

large_corp_factor_benchmark6_1 = large_corp_factor_benchmark6.rename(columns = {'Factor_Value': 'Capital' })
large_corp_factor_benchmark7_1 = large_corp_factor_benchmark7.rename(columns = {'Factor_Value': 'Management' })
large_corp_factor_benchmark8_1 = large_corp_factor_benchmark8.rename(columns = {'Factor_Value': 'Cashflow' })
large_corp_factor_benchmark9_1 = large_corp_factor_benchmark9.rename(columns = {'Factor_Value': 'Industry' })

large_corp_factor_benchmark1_2 = large_corp_factor_benchmark1_1.drop(['Factor_Value_Quant', 'Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark2_2 = large_corp_factor_benchmark2_1.drop(['Factor_Value_Quant', 'Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark3_2 = large_corp_factor_benchmark3_1.drop(['Factor_Value_Quant', 'Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark4_2 = large_corp_factor_benchmark4_1.drop(['Factor_Value_Quant', 'Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark5_2 = large_corp_factor_benchmark5_1.drop(['Factor_Value_Quant', 'Factor_Name', 'Status'], axis = 1)

large_corp_factor_benchmark6_2 = large_corp_factor_benchmark6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark7_2 = large_corp_factor_benchmark7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark8_2 = large_corp_factor_benchmark8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
large_corp_factor_benchmark9_2 = large_corp_factor_benchmark9_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)



large_corp_all_benchmark2 = pd.merge(large_corp_factor_benchmark1_2, large_corp_factor_benchmark2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

large_corp_all_benchmark3 = pd.merge(large_corp_all_benchmark2, large_corp_factor_benchmark3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


large_corp_all_benchmark4 = pd.merge(large_corp_all_benchmark3, large_corp_factor_benchmark4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

large_corp_all_benchmark5 = pd.merge(large_corp_all_benchmark4, large_corp_factor_benchmark5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_all_benchmark6 = pd.merge(large_corp_all_benchmark5, large_corp_factor_benchmark6_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_all_benchmark7 = pd.merge(large_corp_all_benchmark6, large_corp_factor_benchmark7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_all_benchmark8 = pd.merge(large_corp_all_benchmark7, large_corp_factor_benchmark8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
large_corp_final_benchmark = pd.merge(large_corp_all_benchmark8, large_corp_factor_benchmark9_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')









large_corp_final_benchmark2 = large_corp_final_benchmark.drop_duplicates().copy()

large_corp_final_benchmark2['Date'] = pd.to_datetime(large_corp_final_benchmark2['Date'])

large_corp_final_benchmark2['loaddt'] = large_corp_final_benchmark2['Date'] + pd.tseries.offsets.MonthEnd(0)

large_corp_final_benchmark2 = large_corp_final_benchmark2.rename(columns = { 'CIF': 'cif'})
large_corp_final_benchmark3 = large_corp_final_benchmark2.copy()




# %%
#Mid Size 

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

mid_size_factor1 = mid_size_all.loc[mid_size_all.Factor_Name == 'Gross Margin %']
mid_size_factor2 = mid_size_all.loc[mid_size_all.Factor_Name == 'Revenue (Thousands)']
mid_size_factor3 = mid_size_all.loc[mid_size_all.Factor_Name == 'Capital Structure']
mid_size_factor4 = mid_size_all.loc[mid_size_all.Factor_Name == 'Total Funded Debt to EBITDA']

mid_size_factor1['Factor_Value_Quant1'] = pd.factorize(mid_size_factor1['Factor_Value_Quant'])[0]
mid_size_factor2['Factor_Value_Quant1'] = pd.factorize(mid_size_factor2['Factor_Value_Quant'])[0]
mid_size_factor3['Factor_Value_Quant1'] = pd.factorize(mid_size_factor3['Factor_Value_Quant'])[0]
mid_size_factor4['Factor_Value_Quant1'] = pd.factorize(mid_size_factor4['Factor_Value_Quant'])[0]



mid_size_factor1.drop('Factor_Value_Qual', axis=1, inplace=True)
mid_size_factor2.drop('Factor_Value_Qual', axis=1, inplace=True)
mid_size_factor3.drop('Factor_Value_Qual', axis=1, inplace=True)
mid_size_factor4.drop('Factor_Value_Qual', axis=1, inplace=True)


mid_size_factor1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
mid_size_factor2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
mid_size_factor3.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
mid_size_factor4.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


mid_size_factor5 = mid_size_all.loc[mid_size_all.Factor_Name == 'Business & Revenue Model']
mid_size_factor6 = mid_size_all.loc[mid_size_all.Factor_Name == 'Industry / Funding and Regulatory Environment']
mid_size_factor7 = mid_size_all.loc[mid_size_all.Factor_Name == 'Management / Ownership Quality']
mid_size_factor8 = mid_size_all.loc[mid_size_all.Factor_Name == 'Access to Capital & Financial Health']


mid_size_factor5['Factor_Value_Qual1'] = pd.factorize(mid_size_factor5['Factor_Value_Qual'])[0]
mid_size_factor6['Factor_Value_Qual1'] = pd.factorize(mid_size_factor6['Factor_Value_Qual'])[0]
mid_size_factor7['Factor_Value_Qual1'] = pd.factorize(mid_size_factor7['Factor_Value_Qual'])[0]
mid_size_factor8['Factor_Value_Qual1'] = pd.factorize(mid_size_factor8['Factor_Value_Qual'])[0]



mid_size_factor5.drop('Factor_Value_Quant', axis=1, inplace=True)
mid_size_factor6.drop('Factor_Value_Quant', axis=1, inplace=True)
mid_size_factor7.drop('Factor_Value_Quant', axis=1, inplace=True)
mid_size_factor8.drop('Factor_Value_Quant', axis=1, inplace=True)

mid_size_factor5.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
mid_size_factor6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
mid_size_factor7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
mid_size_factor8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




mid_size_factor1_1 = mid_size_factor1.rename(columns = {'Factor_Value': 'Gross_Margin' })
mid_size_factor2_1 = mid_size_factor2.rename(columns = {'Factor_Value': 'Scale' })
mid_size_factor3_1 = mid_size_factor3.rename(columns = {'Factor_Value': 'Cap_Structure' })
mid_size_factor4_1 = mid_size_factor4.rename(columns = {'Factor_Value': 'TDEBITDA' })


mid_size_factor5_1 = mid_size_factor5.rename(columns = {'Factor_Value': 'Business' })
mid_size_factor6_1 = mid_size_factor6.rename(columns = {'Factor_Value': 'Industry' })
mid_size_factor7_1 = mid_size_factor7.rename(columns = {'Factor_Value': 'Management' })
mid_size_factor8_1 = mid_size_factor8.rename(columns = {'Factor_Value': 'Capital' })

mid_size_factor1_2 = mid_size_factor1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
mid_size_factor2_2 = mid_size_factor2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
mid_size_factor3_2 = mid_size_factor3_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
mid_size_factor4_2 = mid_size_factor4_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)

mid_size_factor5_2 = mid_size_factor5_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
mid_size_factor6_2 = mid_size_factor6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
mid_size_factor7_2 = mid_size_factor7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
mid_size_factor8_2 = mid_size_factor8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)




mid_size_all2 = pd.merge(mid_size_factor1_2, mid_size_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

mid_size_all3 = pd.merge(mid_size_all2, mid_size_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


mid_size_all4 = pd.merge(mid_size_all3, mid_size_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

mid_size_all5 = pd.merge(mid_size_all4, mid_size_factor5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
mid_size_all6 = pd.merge(mid_size_all5, mid_size_factor6_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
mid_size_all7 = pd.merge(mid_size_all6, mid_size_factor7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
mid_size_final = pd.merge(mid_size_all7, mid_size_factor8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')









mid_size_final2 = mid_size_final.drop_duplicates().copy()

mid_size_final2['Date'] = pd.to_datetime(mid_size_final2['Date'])

mid_size_final2['loaddt'] = mid_size_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

mid_size_final2 = mid_size_final2.rename(columns = { 'CIF': 'cif'})
mid_size_final3 = mid_size_final2.copy()




# %%
#Mid Size Benchmark

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

mid_size_factor_benchmark1 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Gross Margin %']
mid_size_factor_benchmark2 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Revenue (Thousands)']
mid_size_factor_benchmark3 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Capital Structure']
mid_size_factor_benchmark4 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Total Funded Debt to EBITDA']

mid_size_factor_benchmark1['Factor_Value_Quant1'] = pd.factorize(mid_size_factor_benchmark1['Factor_Value_Quant'])[0]
mid_size_factor_benchmark2['Factor_Value_Quant1'] = pd.factorize(mid_size_factor_benchmark2['Factor_Value_Quant'])[0]
mid_size_factor_benchmark3['Factor_Value_Quant1'] = pd.factorize(mid_size_factor_benchmark3['Factor_Value_Quant'])[0]
mid_size_factor_benchmark4['Factor_Value_Quant1'] = pd.factorize(mid_size_factor_benchmark4['Factor_Value_Quant'])[0]





mid_size_factor_benchmark1.drop('Factor_Value_Qual', axis=1, inplace=True)
mid_size_factor_benchmark2.drop('Factor_Value_Qual', axis=1, inplace=True)
mid_size_factor_benchmark3.drop('Factor_Value_Qual', axis=1, inplace=True)
mid_size_factor_benchmark4.drop('Factor_Value_Qual', axis=1, inplace=True)


mid_size_factor_benchmark1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
mid_size_factor_benchmark2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
mid_size_factor_benchmark3.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
mid_size_factor_benchmark4.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


mid_size_factor_benchmark5 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Business & Revenue Model']
mid_size_factor_benchmark6 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Industry / Funding and Regulatory Environment']
mid_size_factor_benchmark7 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Management / Ownership Quality']
mid_size_factor_benchmark8 = mid_size_all_benchmark.loc[mid_size_all_benchmark.Factor_Name == 'Access to Capital & Financial Health']


mid_size_factor_benchmark5['Factor_Value_Qual1'] = pd.factorize(mid_size_factor_benchmark5['Factor_Value_Qual'])[0]
mid_size_factor_benchmark6['Factor_Value_Qual1'] = pd.factorize(mid_size_factor_benchmark6['Factor_Value_Qual'])[0]
mid_size_factor_benchmark7['Factor_Value_Qual1'] = pd.factorize(mid_size_factor_benchmark7['Factor_Value_Qual'])[0]
mid_size_factor_benchmark8['Factor_Value_Qual1'] = pd.factorize(mid_size_factor_benchmark8['Factor_Value_Qual'])[0]


mid_size_factor_benchmark5.drop('Factor_Value_Quant', axis=1, inplace=True)
mid_size_factor_benchmark6.drop('Factor_Value_Quant', axis=1, inplace=True)
mid_size_factor_benchmark7.drop('Factor_Value_Quant', axis=1, inplace=True)
mid_size_factor_benchmark8.drop('Factor_Value_Quant', axis=1, inplace=True)

mid_size_factor_benchmark5.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
mid_size_factor_benchmark6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
mid_size_factor_benchmark7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
mid_size_factor_benchmark8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




mid_size_factor_benchmark1_1 = mid_size_factor_benchmark1.rename(columns = {'Factor_Value': 'Gross_Margin' })
mid_size_factor_benchmark2_1 = mid_size_factor_benchmark2.rename(columns = {'Factor_Value': 'Scale' })
mid_size_factor_benchmark3_1 = mid_size_factor_benchmark3.rename(columns = {'Factor_Value': 'Cap_Structure' })
mid_size_factor_benchmark4_1 = mid_size_factor_benchmark4.rename(columns = {'Factor_Value': 'TDEBITDA' })


mid_size_factor_benchmark5_1 = mid_size_factor_benchmark5.rename(columns = {'Factor_Value': 'Business' })
mid_size_factor_benchmark6_1 = mid_size_factor_benchmark6.rename(columns = {'Factor_Value': 'Industry' })
mid_size_factor_benchmark7_1 = mid_size_factor_benchmark7.rename(columns = {'Factor_Value': 'Management' })
mid_size_factor_benchmark8_1 = mid_size_factor_benchmark8.rename(columns = {'Factor_Value': 'Capital' })

mid_size_factor_benchmark1_2 = mid_size_factor_benchmark1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
mid_size_factor_benchmark2_2 = mid_size_factor_benchmark2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
mid_size_factor_benchmark3_2 = mid_size_factor_benchmark3_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
mid_size_factor_benchmark4_2 = mid_size_factor_benchmark4_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)

mid_size_factor_benchmark5_2 = mid_size_factor_benchmark5_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
mid_size_factor_benchmark6_2 = mid_size_factor_benchmark6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
mid_size_factor_benchmark7_2 = mid_size_factor_benchmark7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
mid_size_factor_benchmark8_2 = mid_size_factor_benchmark8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)





mid_size_all_benchmark2 = pd.merge(mid_size_factor_benchmark1_2, mid_size_factor_benchmark2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

mid_size_all_benchmark3 = pd.merge(mid_size_all_benchmark2, mid_size_factor_benchmark3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


mid_size_all_benchmark4 = pd.merge(mid_size_all_benchmark3, mid_size_factor_benchmark4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

mid_size_all_benchmark5 = pd.merge(mid_size_all_benchmark4, mid_size_factor_benchmark5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
mid_size_all_benchmark6 = pd.merge(mid_size_all_benchmark5, mid_size_factor_benchmark6_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
mid_size_all_benchmark7 = pd.merge(mid_size_all_benchmark6, mid_size_factor_benchmark7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
mid_size_final_benchmark = pd.merge(mid_size_all_benchmark7, mid_size_factor_benchmark8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')









mid_size_final_benchmark2 = mid_size_final_benchmark.drop_duplicates().copy()

mid_size_final_benchmark2['Date'] = pd.to_datetime(mid_size_final_benchmark2['Date'])

mid_size_final_benchmark2['loaddt'] = mid_size_final_benchmark2['Date'] + pd.tseries.offsets.MonthEnd(0)

mid_size_final_benchmark2 = mid_size_final_benchmark2.rename(columns = { 'CIF': 'cif'})
mid_size_final_benchmark3 = mid_size_final_benchmark2.copy()




# %%
#Early Stage 

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

early_stage_factor1 = early_stage_all.loc[early_stage_all.Factor_Name == 'Net Margin %']
early_stage_factor2 = early_stage_all.loc[early_stage_all.Factor_Name == 'Revenue (Thousands)']
early_stage_factor3 = early_stage_all.loc[early_stage_all.Factor_Name == 'Capital Structure']
early_stage_factor4 = early_stage_all.loc[early_stage_all.Factor_Name == 'Total Funded Debt to EBITDA']


early_stage_factor1['Factor_Value_Quant1'] = pd.factorize(early_stage_factor1['Factor_Value_Quant'])[0]
early_stage_factor2['Factor_Value_Quant1'] = pd.factorize(early_stage_factor2['Factor_Value_Quant'])[0]
early_stage_factor3['Factor_Value_Quant1'] = pd.factorize(early_stage_factor3['Factor_Value_Quant'])[0]
early_stage_factor4['Factor_Value_Quant1'] = pd.factorize(early_stage_factor4['Factor_Value_Quant'])[0]


early_stage_factor1.drop('Factor_Value_Qual', axis=1, inplace=True)
early_stage_factor2.drop('Factor_Value_Qual', axis=1, inplace=True)
early_stage_factor3.drop('Factor_Value_Qual', axis=1, inplace=True)
early_stage_factor4.drop('Factor_Value_Qual', axis=1, inplace=True)


early_stage_factor1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
early_stage_factor2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
early_stage_factor3.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
early_stage_factor4.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


early_stage_factor5 = early_stage_all.loc[early_stage_all.Factor_Name == 'Business and Revenue Model']
early_stage_factor6 = early_stage_all.loc[early_stage_all.Factor_Name == 'Industry / Funding and Regulatory Environment']
early_stage_factor7 = early_stage_all.loc[early_stage_all.Factor_Name == 'Management / Ownership Quality']
early_stage_factor8 = early_stage_all.loc[early_stage_all.Factor_Name == 'Access to Capital & Financial Health']


early_stage_factor5['Factor_Value_Qual1'] = pd.factorize(early_stage_factor5['Factor_Value_Qual'])[0]
early_stage_factor6['Factor_Value_Qual1'] = pd.factorize(early_stage_factor6['Factor_Value_Qual'])[0]
early_stage_factor7['Factor_Value_Qual1'] = pd.factorize(early_stage_factor7['Factor_Value_Qual'])[0]
early_stage_factor8['Factor_Value_Qual1'] = pd.factorize(early_stage_factor8['Factor_Value_Qual'])[0]


early_stage_factor5.drop('Factor_Value_Quant', axis=1, inplace=True)
early_stage_factor6.drop('Factor_Value_Quant', axis=1, inplace=True)
early_stage_factor7.drop('Factor_Value_Quant', axis=1, inplace=True)
early_stage_factor8.drop('Factor_Value_Quant', axis=1, inplace=True)

early_stage_factor5.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
early_stage_factor6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
early_stage_factor7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
early_stage_factor8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




early_stage_factor1_1 = early_stage_factor1.rename(columns = {'Factor_Value': 'Net_Margin' })
early_stage_factor2_1 = early_stage_factor2.rename(columns = {'Factor_Value': 'Scale' })
early_stage_factor3_1 = early_stage_factor3.rename(columns = {'Factor_Value': 'Cap_Structure' })
early_stage_factor4_1 = early_stage_factor4.rename(columns = {'Factor_Value': 'TDEBITDA' })


early_stage_factor5_1 = early_stage_factor5.rename(columns = {'Factor_Value': 'Business' })
early_stage_factor6_1 = early_stage_factor6.rename(columns = {'Factor_Value': 'Industry' })
early_stage_factor7_1 = early_stage_factor7.rename(columns = {'Factor_Value': 'Management' })
early_stage_factor8_1 = early_stage_factor8.rename(columns = {'Factor_Value': 'Capital' })

early_stage_factor1_2 = early_stage_factor1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
early_stage_factor2_2 = early_stage_factor2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
early_stage_factor3_2 = early_stage_factor3_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
early_stage_factor4_2 = early_stage_factor4_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)

early_stage_factor5_2 = early_stage_factor5_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
early_stage_factor6_2 = early_stage_factor6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
early_stage_factor7_2 = early_stage_factor7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
early_stage_factor8_2 = early_stage_factor8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)





early_stage_all2 = pd.merge(early_stage_factor1_2, early_stage_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

early_stage_all3 = pd.merge(early_stage_all2, early_stage_factor3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


early_stage_all4 = pd.merge(early_stage_all3, early_stage_factor4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

early_stage_all5 = pd.merge(early_stage_all4, early_stage_factor5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
early_stage_all6 = pd.merge(early_stage_all5, early_stage_factor6_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
early_stage_all7 = pd.merge(early_stage_all6, early_stage_factor7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
early_stage_final = pd.merge(early_stage_all7, early_stage_factor8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')









early_stage_final2 = early_stage_final.drop_duplicates().copy()

early_stage_final2['Date'] = pd.to_datetime(early_stage_final2['Date'])

early_stage_final2['loaddt'] = early_stage_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

early_stage_final2 = early_stage_final2.rename(columns = { 'CIF': 'cif'})
early_stage_final3 = early_stage_final2.copy()




# %%
#Early Stage Benchmark

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

early_stage_factor_benchmark1 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Net Margin %']
early_stage_factor_benchmark2 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Revenue (Thousands)']
early_stage_factor_benchmark3 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Capital Structure']
early_stage_factor_benchmark4 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Total Funded Debt to EBITDA']

early_stage_factor_benchmark1['Factor_Value_Quant1'] = pd.factorize(early_stage_factor_benchmark1['Factor_Value_Quant'])[0]
early_stage_factor_benchmark2['Factor_Value_Quant1'] = pd.factorize(early_stage_factor_benchmark2['Factor_Value_Quant'])[0]
early_stage_factor_benchmark3['Factor_Value_Quant1'] = pd.factorize(early_stage_factor_benchmark3['Factor_Value_Quant'])[0]
early_stage_factor_benchmark4['Factor_Value_Quant1'] = pd.factorize(early_stage_factor_benchmark4['Factor_Value_Quant'])[0]



early_stage_factor_benchmark1.drop('Factor_Value_Qual', axis=1, inplace=True)
early_stage_factor_benchmark2.drop('Factor_Value_Qual', axis=1, inplace=True)
early_stage_factor_benchmark3.drop('Factor_Value_Qual', axis=1, inplace=True)
early_stage_factor_benchmark4.drop('Factor_Value_Qual', axis=1, inplace=True)


early_stage_factor_benchmark1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
early_stage_factor_benchmark2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
early_stage_factor_benchmark3.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
early_stage_factor_benchmark4.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


early_stage_factor_benchmark5 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Business and Revenue Model']
early_stage_factor_benchmark6 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Industry / Funding and Regulatory Environment']
early_stage_factor_benchmark7 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Management / Ownership Quality']
early_stage_factor_benchmark8 = early_stage_all_benchmark.loc[early_stage_all_benchmark.Factor_Name == 'Access to Capital & Financial Health']

early_stage_factor_benchmark5['Factor_Value_Qual1'] = pd.factorize(early_stage_factor_benchmark5['Factor_Value_Qual'])[0]
early_stage_factor_benchmark6['Factor_Value_Qual1'] = pd.factorize(early_stage_factor_benchmark6['Factor_Value_Qual'])[0]
early_stage_factor_benchmark7['Factor_Value_Qual1'] = pd.factorize(early_stage_factor_benchmark7['Factor_Value_Qual'])[0]
early_stage_factor_benchmark8['Factor_Value_Qual1'] = pd.factorize(early_stage_factor_benchmark8['Factor_Value_Qual'])[0]




early_stage_factor_benchmark5.drop('Factor_Value_Quant', axis=1, inplace=True)
early_stage_factor_benchmark6.drop('Factor_Value_Quant', axis=1, inplace=True)
early_stage_factor_benchmark7.drop('Factor_Value_Quant', axis=1, inplace=True)
early_stage_factor_benchmark8.drop('Factor_Value_Quant', axis=1, inplace=True)

early_stage_factor_benchmark5.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
early_stage_factor_benchmark6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
early_stage_factor_benchmark7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
early_stage_factor_benchmark8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




early_stage_factor_benchmark1_1 = early_stage_factor_benchmark1.rename(columns = {'Factor_Value': 'Net_Margin' })
early_stage_factor_benchmark2_1 = early_stage_factor_benchmark2.rename(columns = {'Factor_Value': 'Scale' })
early_stage_factor_benchmark3_1 = early_stage_factor_benchmark3.rename(columns = {'Factor_Value': 'Cap_Structure' })
early_stage_factor_benchmark4_1 = early_stage_factor_benchmark4.rename(columns = {'Factor_Value': 'TDEBITDA' })


early_stage_factor_benchmark5_1 = early_stage_factor_benchmark5.rename(columns = {'Factor_Value': 'Business' })
early_stage_factor_benchmark6_1 = early_stage_factor_benchmark6.rename(columns = {'Factor_Value': 'Industry' })
early_stage_factor_benchmark7_1 = early_stage_factor_benchmark7.rename(columns = {'Factor_Value': 'Management' })
early_stage_factor_benchmark8_1 = early_stage_factor_benchmark8.rename(columns = {'Factor_Value': 'Capital' })

early_stage_factor_benchmark1_2 = early_stage_factor_benchmark1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
early_stage_factor_benchmark2_2 = early_stage_factor_benchmark2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
early_stage_factor_benchmark3_2 = early_stage_factor_benchmark3_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
early_stage_factor_benchmark4_2 = early_stage_factor_benchmark4_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)

early_stage_factor_benchmark5_2 = early_stage_factor_benchmark5_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
early_stage_factor_benchmark6_2 = early_stage_factor_benchmark6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
early_stage_factor_benchmark7_2 = early_stage_factor_benchmark7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
early_stage_factor_benchmark8_2 = early_stage_factor_benchmark8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)




early_stage_all_benchmark2 = pd.merge(early_stage_factor_benchmark1_2, early_stage_factor_benchmark2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

early_stage_all_benchmark3 = pd.merge(early_stage_all_benchmark2, early_stage_factor_benchmark3_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


early_stage_all_benchmark4 = pd.merge(early_stage_all_benchmark3, early_stage_factor_benchmark4_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

early_stage_all_benchmark5 = pd.merge(early_stage_all_benchmark4, early_stage_factor_benchmark5_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
early_stage_all_benchmark6 = pd.merge(early_stage_all_benchmark5, early_stage_factor_benchmark6_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
early_stage_all_benchmark7 = pd.merge(early_stage_all_benchmark6, early_stage_factor_benchmark7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
early_stage_final_benchmark = pd.merge(early_stage_all_benchmark7, early_stage_factor_benchmark8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')









early_stage_final_benchmark2 = early_stage_final_benchmark.drop_duplicates().copy()

early_stage_final_benchmark2['Date'] = pd.to_datetime(early_stage_final_benchmark2['Date'])

early_stage_final_benchmark2['loaddt'] = early_stage_final_benchmark2['Date'] + pd.tseries.offsets.MonthEnd(0)

early_stage_final_benchmark2 = early_stage_final_benchmark2.rename(columns = { 'CIF': 'cif'})
early_stage_final_benchmark3 = early_stage_final_benchmark2.copy()




# %%
#GFB Firm

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

gfb_firm_factor1 = gfb_firm_all.loc[gfb_firm_all.Factor_Name == 'Leverage - Short Term Obligations to Revenue (%)']
gfb_firm_factor2 = gfb_firm_all.loc[gfb_firm_all.Factor_Name == 'Coverage - 4-year Debt Service Coverage']

gfb_firm_factor1['Factor_Value_Quant1'] = pd.factorize(gfb_firm_factor1['Factor_Value_Quant'])[0]
gfb_firm_factor2['Factor_Value_Quant1'] = pd.factorize(gfb_firm_factor2['Factor_Value_Quant'])[0]


gfb_firm_factor1.drop('Factor_Value_Qual', axis=1, inplace=True)
gfb_firm_factor2.drop('Factor_Value_Qual', axis=1, inplace=True)

gfb_firm_factor1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
gfb_firm_factor2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


gfb_firm_factor6 = gfb_firm_all.loc[gfb_firm_all.Factor_Name == 'Management Evaluation']
gfb_firm_factor7 = gfb_firm_all.loc[gfb_firm_all.Factor_Name == 'Management Fee Stream Quality']
gfb_firm_factor8 = gfb_firm_all.loc[gfb_firm_all.Factor_Name == 'Fund Benchmarking']
gfb_firm_factor9 = gfb_firm_all.loc[gfb_firm_all.Factor_Name == 'Ability to Raise Funds']


gfb_firm_factor6['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor6['Factor_Value_Qual'])[0]
gfb_firm_factor7['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor7['Factor_Value_Qual'])[0]
gfb_firm_factor8['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor8['Factor_Value_Qual'])[0]
gfb_firm_factor9['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor9['Factor_Value_Qual'])[0]


gfb_firm_factor6.drop('Factor_Value_Quant', axis=1, inplace=True)
gfb_firm_factor7.drop('Factor_Value_Quant', axis=1, inplace=True)
gfb_firm_factor8.drop('Factor_Value_Quant', axis=1, inplace=True)
gfb_firm_factor9.drop('Factor_Value_Quant', axis=1, inplace=True)

gfb_firm_factor6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
gfb_firm_factor7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
gfb_firm_factor8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
gfb_firm_factor9.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




gfb_firm_factor1_1 = gfb_firm_factor1.rename(columns = {'Factor_Value': 'Leverage' })
gfb_firm_factor2_1 = gfb_firm_factor2.rename(columns = {'Factor_Value': 'Coverage' })


gfb_firm_factor6_1 = gfb_firm_factor6.rename(columns = {'Factor_Value': 'Management' })
gfb_firm_factor7_1 = gfb_firm_factor7.rename(columns = {'Factor_Value': 'Fee' })
gfb_firm_factor8_1 = gfb_firm_factor8.rename(columns = {'Factor_Value': 'Benchmarking' })
gfb_firm_factor9_1 = gfb_firm_factor9.rename(columns = {'Factor_Value': 'Fundraising' })

gfb_firm_factor1_2 = gfb_firm_factor1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor2_2 = gfb_firm_factor2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)



gfb_firm_factor6_2 = gfb_firm_factor6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor7_2 = gfb_firm_factor7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor8_2 = gfb_firm_factor8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor9_2 = gfb_firm_factor9_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)



gfb_firm_all2 = pd.merge(gfb_firm_factor1_2, gfb_firm_factor2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

gfb_firm_all3 = pd.merge(gfb_firm_all2, gfb_firm_factor6_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


gfb_firm_all4 = pd.merge(gfb_firm_all3, gfb_firm_factor7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

gfb_firm_all5 = pd.merge(gfb_firm_all4, gfb_firm_factor8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
gfb_firm_final = pd.merge(gfb_firm_all5, gfb_firm_factor9_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')








gfb_firm_final2 = gfb_firm_final.drop_duplicates().copy()

gfb_firm_final2['Date'] = pd.to_datetime(gfb_firm_final2['Date'])

gfb_firm_final2['loaddt'] = gfb_firm_final2['Date'] + pd.tseries.offsets.MonthEnd(0)

gfb_firm_final2 = gfb_firm_final2.rename(columns = { 'CIF': 'cif'})
gfb_firm_final3 = gfb_firm_final2.copy()




# %%
#GFB Firm Benchmark

#rename fields, Split single factor value column into 4 separate columns
#rejoin into single table and transform date into month end date
#join with default data 

gfb_firm_factor_benchmark1 = gfb_firm_all_benchmark.loc[gfb_firm_all_benchmark.Factor_Name == 'Leverage - Short Term Obligations to Revenue (%)']
gfb_firm_factor_benchmark2 = gfb_firm_all_benchmark.loc[gfb_firm_all_benchmark.Factor_Name == 'Coverage - 4-year Debt Service Coverage']


gfb_firm_factor_benchmark1['Factor_Value_Quant1'] = pd.factorize(gfb_firm_factor_benchmark1['Factor_Value_Quant'])[0]
gfb_firm_factor_benchmark2['Factor_Value_Quant1'] = pd.factorize(gfb_firm_factor_benchmark2['Factor_Value_Quant'])[0]

gfb_firm_factor_benchmark1.drop('Factor_Value_Qual', axis=1, inplace=True)
gfb_firm_factor_benchmark2.drop('Factor_Value_Qual', axis=1, inplace=True)

gfb_firm_factor_benchmark1.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)
gfb_firm_factor_benchmark2.rename(columns = {'Factor_Value_Quant1': 'Factor_Value' }, inplace = True)


gfb_firm_factor_benchmark6 = gfb_firm_all_benchmark.loc[gfb_firm_all_benchmark.Factor_Name == 'Management Evaluation']
gfb_firm_factor_benchmark7 = gfb_firm_all_benchmark.loc[gfb_firm_all_benchmark.Factor_Name == 'Management Fee Stream Quality']
gfb_firm_factor_benchmark8 = gfb_firm_all_benchmark.loc[gfb_firm_all_benchmark.Factor_Name == 'Fund Benchmarking']
gfb_firm_factor_benchmark9 = gfb_firm_all_benchmark.loc[gfb_firm_all_benchmark.Factor_Name == 'Ability to Raise Funds']


gfb_firm_factor_benchmark6['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor_benchmark6['Factor_Value_Qual'])[0]
gfb_firm_factor_benchmark7['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor_benchmark7['Factor_Value_Qual'])[0]
gfb_firm_factor_benchmark8['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor_benchmark8['Factor_Value_Qual'])[0]
gfb_firm_factor_benchmark9['Factor_Value_Qual1'] = pd.factorize(gfb_firm_factor_benchmark9['Factor_Value_Qual'])[0]



gfb_firm_factor_benchmark6.drop('Factor_Value_Quant', axis=1, inplace=True)
gfb_firm_factor_benchmark7.drop('Factor_Value_Quant', axis=1, inplace=True)
gfb_firm_factor_benchmark8.drop('Factor_Value_Quant', axis=1, inplace=True)
gfb_firm_factor_benchmark9.drop('Factor_Value_Quant', axis=1, inplace=True)

gfb_firm_factor_benchmark6.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
gfb_firm_factor_benchmark7.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
gfb_firm_factor_benchmark8.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)
gfb_firm_factor_benchmark9.rename(columns = {'Factor_Value_Qual1': 'Factor_Value' }, inplace = True)




gfb_firm_factor_benchmark1_1 = gfb_firm_factor_benchmark1.rename(columns = {'Factor_Value': 'Leverage' })
gfb_firm_factor_benchmark2_1 = gfb_firm_factor_benchmark2.rename(columns = {'Factor_Value': 'Coverage' })


gfb_firm_factor_benchmark6_1 = gfb_firm_factor_benchmark6.rename(columns = {'Factor_Value': 'Management' })
gfb_firm_factor_benchmark7_1 = gfb_firm_factor_benchmark7.rename(columns = {'Factor_Value': 'Fee' })
gfb_firm_factor_benchmark8_1 = gfb_firm_factor_benchmark8.rename(columns = {'Factor_Value': 'Benchmarking' })
gfb_firm_factor_benchmark9_1 = gfb_firm_factor_benchmark9.rename(columns = {'Factor_Value': 'Fundraising' })

gfb_firm_factor_benchmark1_2 = gfb_firm_factor_benchmark1_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor_benchmark2_2 = gfb_firm_factor_benchmark2_1.drop(['Factor_Value_Quant','Factor_Name', 'Status'], axis = 1)



gfb_firm_factor_benchmark6_2 = gfb_firm_factor_benchmark6_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor_benchmark7_2 = gfb_firm_factor_benchmark7_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor_benchmark8_2 = gfb_firm_factor_benchmark8_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)
gfb_firm_factor_benchmark9_2 = gfb_firm_factor_benchmark9_1.drop(['Factor_Value_Qual','Factor_Name', 'Status'], axis = 1)



gfb_firm_all_benchmark2 = pd.merge(gfb_firm_factor_benchmark1_2, gfb_firm_factor_benchmark2_2,  on = ['CIF', 'CPNumber', 'Date', 'Calc_ORR', 'Final_ORR'], how = 'inner')

gfb_firm_all_benchmark3 = pd.merge(gfb_firm_all_benchmark2, gfb_firm_factor_benchmark6_2,  on = ['CIF','CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')


gfb_firm_all_benchmark4 = pd.merge(gfb_firm_all_benchmark3, gfb_firm_factor_benchmark7_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')

gfb_firm_all_benchmark5 = pd.merge(gfb_firm_all_benchmark4, gfb_firm_factor_benchmark8_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')
gfb_firm_final_benchmark = pd.merge(gfb_firm_all_benchmark5, gfb_firm_factor_benchmark9_2,  on = ['CIF', 'CPNumber', 'Date','Calc_ORR', 'Final_ORR'], how = 'inner')








gfb_firm_final_benchmark2 = gfb_firm_final_benchmark.drop_duplicates().copy()

gfb_firm_final_benchmark2['Date'] = pd.to_datetime(gfb_firm_final_benchmark2['Date'])

gfb_firm_final_benchmark2['loaddt'] = gfb_firm_final_benchmark2['Date'] + pd.tseries.offsets.MonthEnd(0)

gfb_firm_final_benchmark2 = gfb_firm_final_benchmark2.rename(columns = { 'CIF': 'cif'})
gfb_firm_final_benchmark3 = gfb_firm_final_benchmark2.copy()




# %%
#function for calculating population stability index 


# PSI = Sum((Actual - Expected)*log(%Actual/%Expected))


def calculate_psi(expected_data, actual_data, num_bins=10):
    """
    Calculates the Population Stability Index (PSI) between two datasets.

    Args:
        expected_data (pd.Series or np.ndarray): The reference or "expected" data.
        actual_data (pd.Series or np.ndarray): The current or "actual" data.
        num_bins (int): The number of bins to use for bucketing the data.

    Returns:
        float: The calculated PSI value.
    """

    # Ensure data is in a pandas Series for easier binning
    expected_data = pd.Series(expected_data)
    actual_data = pd.Series(actual_data)

    # Create bins based on the expected data
    bins = pd.cut(expected_data, bins=num_bins, retbins=True, duplicates='drop')[1]

    # Handle cases where bins might not cover all actual data points
    # Extend bins to include min/max of both datasets if necessary
    min_val = min(expected_data.min(), actual_data.min())
    max_val = max(expected_data.max(), actual_data.max())
    bins = np.concatenate(([min_val - 1], bins[1:-1], [max_val + 1]))
    bins = np.sort(np.unique(bins)) # Ensure unique and sorted bins

    # Calculate counts and proportions for each bin
    expected_counts = pd.cut(expected_data, bins=bins, include_lowest=True).value_counts().sort_index()
    actual_counts = pd.cut(actual_data, bins=bins, include_lowest=True).value_counts().sort_index()

    expected_pct = expected_counts / len(expected_data)
    actual_pct = actual_counts / len(actual_data)

    # Handle potential zero percentages for numerical stability
    expected_pct = expected_pct.replace(0, 0.0001)
    actual_pct = actual_pct.replace(0, 0.0001)

    # Calculate PSI for each bin
    psi_per_bin = (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)

    # Sum the PSI for all bins to get the total PSI
    total_psi = psi_per_bin.sum()

    return total_psi




# %%
#calculate psi for gfb ccloc portfolio 
psi_input_gfb_ccloc = []
col_ccloc = ['Fund_Performance',
       'LP_Capacity', 'LP_Diversification', 'Management_Experience']

for features in col_ccloc:
        expected_data = ccloc_benchmark_final2[features].tolist()
        actual_data = ccloc_final3[features].tolist()
        psi_input = calculate_psi(expected_data, actual_data)
        psi_input_gfb_ccloc.append(psi_input)

# %%
#calculate psi for nav portfolio 
psi_input_nav = []


col_nav = ['Exit_Environment',
       'Asset_Diversification', 'Industry_Concentration', 'Asset_Coverage',
       'Manager_Quality', ]

for features in col_nav:
        expected_data = nav_benchmark_final3[features].tolist()
        actual_data = nav_final3[features].tolist()
        psi_input = calculate_psi(expected_data, actual_data)
        psi_input_nav.append(psi_input)

# %%
#calculate psi for gfb firm portfolio 
psi_input_firm = []
col_firm = ['Leverage',
       'Coverage', 'Management', 'Fee', 'Benchmarking', 'Fundraising']

for features in col_firm:
        expected_data = gfb_firm_final_benchmark3[features].tolist()
        actual_data = gfb_firm_final3[features].tolist()
        psi_input = calculate_psi(expected_data, actual_data)
        psi_input_firm.append(psi_input)

# %%
#calculate psi for large_corp portfolio 
psi_input_large_corp = []
col_large = ['Gross_Margin',
       'Scale', 'TDEBITDA', 'Current_Ratio', 'FCCR', 'Capital', 'Management',
       'Cashflow', 'Industry']
for features in col_large:
        expected_data = large_corp_final_benchmark3[features].tolist()
        actual_data = large_corp_final3[features].tolist()
        psi_input = calculate_psi(expected_data, actual_data)
        psi_input_large_corp.append(psi_input)

# %%
#calculate psi for mid size portfolio 
psi_input_mid_size = []
col_mid = ['Gross_Margin',
       'Scale', 'Cap_Structure', 'TDEBITDA', 'Business', 'Industry',
       'Management', 'Capital']

for features in col_mid:
        expected_data = mid_size_final_benchmark3[features].tolist()
        actual_data = mid_size_final3[features].tolist()
        psi_input = calculate_psi(expected_data, actual_data)
        psi_input_mid_size.append(psi_input)

# %%
#calculate psi for early stage portfolio 
psi_input_early = []
col_early = ['Net_Margin',
       'Scale', 'Cap_Structure', 'TDEBITDA', 'Business', 'Industry',
       'Management', 'Capital']

for features in col_early:
        expected_data = early_stage_final_benchmark3[features].tolist()
        actual_data = early_stage_final3[features].tolist()
        psi_input = calculate_psi(expected_data, actual_data)
        psi_input_early.append(psi_input)

# %%
# exporting results

col_name = ['Factor', 'PSI_Value']



ccloc_zipped = list(zip(col_ccloc, psi_input_gfb_ccloc))
nav_zipped = list(zip(col_nav, psi_input_nav))
firm_zipped = list(zip(col_firm, psi_input_firm))
large_zipped = list(zip(col_large, psi_input_large_corp))
mid_zipped = list(zip(col_mid, psi_input_mid_size))
early_zipped = list(zip(col_early, psi_input_early))



df_ccloc = pd.DataFrame(ccloc_zipped, columns=col_name)
df_nav = pd.DataFrame(nav_zipped, columns=col_name)
df_firm = pd.DataFrame(firm_zipped, columns=col_name)
df_large = pd.DataFrame(large_zipped, columns=col_name)
df_mid = pd.DataFrame(mid_zipped, columns=col_name)
df_early = pd.DataFrame(early_zipped, columns=col_name)


df_ccloc.to_csv('ccloc_input_psi.csv')
df_nav.to_csv('nav_input_psi.csv')
df_firm.to_csv('firm_input_psi.csv')
df_large.to_csv('large_input_psi.csv')
df_mid.to_csv('mid_input_psi.csv')
df_early.to_csv('early_input_psi.csv')

# %%
for features in col_nav: 
    expected_data = nav_benchmark_final3[features]
    #actual_data = nav_final3[features].tolist()
    #Calculate quartiles and IQR
    Q1 = expected_data.quantile(0.25)
    Q3 = expected_data.quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    filtered_data = expected_data[(expected_data >= lower_bound) & (expected_data <= upper_bound)]




    #plt.xlabel = 'Variable'
    #plt.ylabel = 'Frequency'
    
    plt.hist(filtered_data,bins = 30,  color = 'orange', edgecolor = 'black' )
    plt.title('GFB NAV_' + features + '_benchmark_data')
    
    plt.savefig('GFB NAV_' + features + '_benchmark_data' + '.jpg')
    plt.show()
    
    plt.close()
    

# %%
for features in col_nav: 
    #expected_data = nav_benchmark_final3[features].tolist()
    actual_data = nav_final3[features]
    #Calculate quartiles and IQR
    Q1 = actual_data.quantile(0.25)
    Q3 = actual_data.quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    filtered_data = actual_data[(actual_data >= lower_bound) & (actual_data <= upper_bound)]




    #plt.xlabel = 'Variable'
    #plt.ylabel = 'Frequency'
    
    plt.hist(filtered_data,bins = 30,  color = 'orange', edgecolor = 'black' )
    plt.title('GFB NAV_' + features + '_predict_data')
    
    plt.savefig('GFB NAV_' + features + '_predict_data' + '.jpg')
    plt.show()
    
    plt.close()


