get me the sql codes from below. i need just sql codes in word document, dont hallucinate the result, read the data carefully 

# %% [markdown]
# #### Importing libraries 

# %%
# ### Importing libraries to be used for importing data and calculations and model dev and validation


import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.3f}'.format
pd.set_option('display.max_columns',None)

import pyodbc

import os
#print(os.getcwd())

import warnings
warnings.filterwarnings('ignore')

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

lowess = sm.nonparametric.lowess

filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')
start = datetime.now()
#print(start)



# %% [markdown]
# #### Function to convert month to quarter

# %%
def month_to_quarter (month):
    if month in [1,2,3]:
        return 'Q1'
    elif month in [4,5,6]:
        return 'Q2'
    elif month in [7,8,9]:
        return 'Q3'
    else: return 'Q4'

# %% [markdown]
# #### Create dates to be used for generating performance monitoring KPIs

# %%


current_date = date.today()
month_end = current_date + relativedelta(day=31)
last_month_end = month_end - relativedelta(months = 1)
last_month_end = last_month_end + pd.offsets.MonthEnd(n=0)
last_month_end1 = last_month_end.strftime("%Y-%m-%d")



month_end_24m_prior = month_end - relativedelta(months=25)

month_end_24m_prior = month_end_24m_prior + pd.offsets.MonthEnd(n=0)
month_end_24m_prior = month_end_24m_prior.strftime("%Y-%m-%d")

last_month = last_month_end.month
kpi_quarter = month_to_quarter(last_month)

large_corp_date = '08-31-2023'

mid_date = '04-30-2024'

early_date = '04-30-2024'

CCLOC_date = '01-31-2022'

NAV_date = '01-31-2022'

firm_date = '08-31-2023'

lc_model = ['Innovation > $75MM & Sponsor – CF', 'Innovation > $75MM & Sponsor – ID/BS' ]
mid_model = ['Innovation > $15MM up to $75MM']
early_model = ['Innovation up to $15MM']
ccloc_model = ['CCLOC']
nav_model  = ['NAV']
firm_model = ['GFB Firm']

large_corp_lgd_kpi = []
mid_lgd_kpi = []
early_lgd_kpi = []
ccloc_lgd_kpi = []
nav_lgd_kpi = []
firm_lgd_kpi = []



model_name = ['GFB CCLOC', 'GFB NAV', 'GFB Firm','Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage']
model_name = ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage']

# %%
print(last_month_end1, month_end_24m_prior)

# %%
grade_map = {'BGC' : 'F',
'BSL' : 'D',
'CFD' : 'C',
'CHT' : 'D',
'FOL' : 'D',
'FOT' : 'E',
'GCT' : 'F',
'GUD' : 'D',
'IRR' : 'E',
'MEZ' : 'F',
'MRR' : 'C',
'NFL' : 'E',
'NFT' : 'F',
'SFD' : 'D',
'SFR' : 'E',
'UNL' : 'G',
'PCC' : 'C',
'NAV' : 'D',
'SFT' : 'A',
'REL' : 'B',
'RET' : 'B',
'SSL' : 'B',
'PAW' : 'C',
'EOF' : 'D',
'LFL' : 'D',
'BAC' : 'D',
'WHL' : 'D',
'NVS' : 'D', 
'APP' : 'E',
'CMR' : 'E',
'BGC' : 'F',
'BRL' : 'F',
'PSL' : 'E',
'BRT' : 'F',
'ICC' : 'E',
'GCC' : 'F',
'CFR' : 'F',
'CFT' : 'G',
'UNL' : 'G',
'UNT' : 'G'


}

# %% [markdown]
# #### Establish connection to SQL server

# %%
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQLAG-CRDMPRD-L.CORP.SVBANK.COM,1433;'
                      'Database=CRDADMANALYSIS;'
                      'Schema=dbo'
                      'Trusted_Connection=yes;')


conn2 = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQLAG-CRDMPRD-L.CORP.SVBANK.COM,1433;'
                      'Database=CRDADMPRD;'
                      'Schema=dbo'
                      'Trusted_Connection=yes;')

#Step 1
# Connection to sql server
#password = cyberArk_automation_v1.main()
#conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                      #'Server=10.108.24.101,1436;'
                      #'Server=10.108.24.61,1435;'
                      #'Database=CRDADMANALYSIS;'
                      #'UID=svc.cdmdrr;'
                      #'PWD='+password+';'
                      #'Schema=dbo;'
                      #'TrustServerCertificate=yes;')



# %% [markdown]
# #### Section 1: LGD Models Rank Order Assessment and Accuracy

# %%

# DRR All Models



sql_override = """
    
    select distinct  a.CIF, a.RISK_GRADE_TEMPLATE	
                				
                

                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 'Innovation > $75MM & Sponsor – ID/BS', 'GFB Firm'
     , 'Innovation > $15MM up to $75MM', 'Innovation up to $15MM', 'CCLOC', 'NAV' )	

     		
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null

                
                
               
    """

DRR_CIFS = pd.DataFrame(pd.read_sql_query(sql_override, conn))
DRR_CIFS = DRR_CIFS.drop_duplicates()



cif_list_large_lgd = DRR_CIFS.loc[DRR_CIFS.RISK_GRADE_TEMPLATE.isin(lc_model)].CIF.unique()
cif_list_mid_lgd = DRR_CIFS.loc[DRR_CIFS.RISK_GRADE_TEMPLATE.isin(mid_model)].CIF.unique()
cif_list_early_lgd = DRR_CIFS.loc[DRR_CIFS.RISK_GRADE_TEMPLATE.isin(early_model)].CIF.unique()
cif_list_CCLOC_lgd = DRR_CIFS.loc[DRR_CIFS.RISK_GRADE_TEMPLATE.isin(ccloc_model)].CIF.unique()
cif_list_NAV_lgd = DRR_CIFS.loc[DRR_CIFS.RISK_GRADE_TEMPLATE.isin(nav_model)].CIF.unique()
cif_list_firm_lgd = DRR_CIFS.loc[DRR_CIFS.RISK_GRADE_TEMPLATE.isin(firm_model)].CIF.unique()



# %% [markdown]
# #### Section 2: Default Data Download 

# %%
#Total Only Chargeoff Data import

sql_chargeoff = """SET NOCOUNT ON

select cif, final_lgd, max(loaddt) as max_date, facility_type into #temp1 
  from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW] 
  where line_status = 'ACTIVE' and loaddt > '01-01-2022' and final_lgd is not null
  group by cif, FINAL_LGD, facility_type

  select c.* into #temp2 from #temp1 c
  inner join [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW] d on c.cif = d.cif and max_date = d.loaddt

  select distinct a.*,b.FINAL_LGD from [CRDADMPRD].[dbo].[CDM_CHARGEOFF_RECOVERY_TOPSIDED] a left outer join #temp2 b

  on a.cif = b.cif and a.FACILITY_TYP = b.facility_type
  where EFF_DT > '2021-12-31'  

  and TRNS_TYP in ('CHARGEOFF', 'RECOVERY')

  
drop table #temp1, #temp2
"""

all_default = pd.read_sql_query(sql_chargeoff, conn)
chargeoff = all_default.loc[all_default.TRNS_TYP == 'CHARGEOFF']
recovery =  all_default.loc[all_default.TRNS_TYP == 'RECOVERY']

# %%
#Total only Default Flag data import


sql_default = """

SELECT a.LOADDT, a.CIF, a.RISK_CD, a.DEFAULT_FLAG
  FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW] a

  inner join 

  (select CIF, min(loaddt) as min_date

from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]

where default_flag = 1
group by cif ) b 

on a.cif = b.cif and a.loaddt = b.min_date




"""


default_flag_data = pd.read_sql_query(sql_default, conn)




# %%
masterscale = pd.read_csv('LGD_MASTERSCALE.csv')

# %% [markdown]
# #### Create a dummy dataframe to hold rating default data 

# %%
FINAL_ORR = list(range(18))
FINAL_ORR.pop(0)
Predict_Default = [0]*17
dummy_df = list(zip(FINAL_ORR, Predict_Default))
dummy_df1 = pd.DataFrame(dummy_df, columns=['FINAL_ORR', 'Predict_Default'])


# %%
# DRR Large Corp 

large_corp_choff = chargeoff.loc[chargeoff.CIF.isin(cif_list_large_lgd)]
large_corp_choff.EFF_DT = pd.to_datetime(large_corp_choff.EFF_DT)
large_corp_choff_v2 = large_corp_choff.loc[large_corp_choff.EFF_DT > large_corp_date]
#large_corp_choff_v2 = large_corp_choff.loc[large_corp_choff.EFF_DT < month_end_24m_prior]

choff_large_corp_cif = large_corp_choff_v2.CIF.unique()

recovery_large_corp = recovery.loc[recovery.CIF.isin(choff_large_corp_cif)]

large_corp_net_choff = pd.concat([large_corp_choff_v2, recovery_large_corp])

large_corp_net_choff_v2 = large_corp_net_choff.groupby(['CIF', 'FINAL_LGD','FACILITY_TYP'])['TRNSCTN_AMT'].sum().reset_index()



# sense checking the chargeoff data with default flag data


large_corp_default = default_flag_data.loc[default_flag_data.CIF.isin(cif_list_large_lgd)]
large_corp_default.LOADDT = pd.to_datetime(large_corp_default.LOADDT)
large_corp_default_v2 = large_corp_default.loc[large_corp_default.LOADDT > large_corp_date]
#large_corp_default_v2 = large_corp_default.loc[large_corp_default.LOADDT < month_end_24m_prior]


# %%
large_corp_choff.to_csv('large_corp_choff.csv')

# %%
# DRR Mid Size 
mid_choff = chargeoff.loc[chargeoff.CIF.isin(cif_list_mid_lgd)]
mid_choff.EFF_DT = pd.to_datetime(mid_choff.EFF_DT)
mid_choff_v2 = mid_choff.loc[mid_choff.EFF_DT > mid_date]
#mid_choff_v2 = mid_choff.loc[mid_choff.EFF_DT < month_end_24m_prior]

choff_mid_cif = mid_choff_v2.CIF.unique()

recovery_mid = recovery.loc[recovery.CIF.isin(choff_mid_cif)]

mid_net_choff = pd.concat([mid_choff_v2, recovery_mid])

mid_net_choff_v2 = mid_net_choff.groupby(['CIF', 'FINAL_LGD','FACILITY_TYP'])['TRNSCTN_AMT'].sum().reset_index()

mid_default = default_flag_data.loc[default_flag_data.CIF.isin(cif_list_mid_lgd)]
mid_default.LOADDT = pd.to_datetime(mid_default.LOADDT)
mid_default_v2 = mid_default.loc[mid_default.LOADDT > mid_date]
#mid_default_v2 = mid_default.loc[mid_default.LOADDT < month_end_24m_prior]

# %%
mid_choff.to_csv('mid_size_choff.csv')

# %%
# DRR CCLOC

CCLOC_choff = chargeoff.loc[chargeoff.CIF.isin(cif_list_CCLOC_lgd)]
CCLOC_choff.EFF_DT = pd.to_datetime(CCLOC_choff.EFF_DT)
CCLOC_choff_v2 = CCLOC_choff.loc[CCLOC_choff.EFF_DT > CCLOC_date]
#CCLOC_choff_v2 = CCLOC_choff.loc[CCLOC_choff.EFF_DT < month_end_24m_prior]

choff_ccloc_cif = CCLOC_choff_v2.CIF.unique()

recovery_ccloc = recovery.loc[recovery.CIF.isin(choff_ccloc_cif)]

CCLOC_net_choff = pd.concat([CCLOC_choff_v2, recovery_ccloc])

CCLOC_net_choff_v2 = CCLOC_net_choff.groupby(['CIF','FINAL_LGD' ,'FACILITY_TYP'])['TRNSCTN_AMT'].sum().reset_index()

CCLOC_default = default_flag_data.loc[default_flag_data.CIF.isin(cif_list_CCLOC_lgd)]
CCLOC_default.LOADDT = pd.to_datetime(CCLOC_default.LOADDT)
CCLOC_default_v2 = CCLOC_default.loc[CCLOC_default.LOADDT > CCLOC_date]
#CCLOC_default_v2 = CCLOC_default.loc[CCLOC_default.LOADDT < month_end_24m_prior]


# %%
# DRR Early Stage

early_choff = chargeoff.loc[chargeoff.CIF.isin(cif_list_early_lgd)]
early_choff.EFF_DT = pd.to_datetime(early_choff.EFF_DT)
early_choff_v2 = early_choff.loc[early_choff.EFF_DT > early_date]
#early_choff_v2 = early_choff.loc[early_choff.EFF_DT < month_end_24m_prior]

choff_early_cif = early_choff_v2.CIF.unique()

recovery_early = recovery.loc[recovery.CIF.isin(choff_early_cif)]

early_net_choff = pd.concat([early_choff_v2, recovery_early])

early_net_choff_v2 = early_net_choff.groupby(['CIF','FINAL_LGD', 'FACILITY_TYP'])['TRNSCTN_AMT'].sum().reset_index()

early_default = default_flag_data.loc[default_flag_data.CIF.isin(cif_list_early_lgd)]
early_default.LOADDT = pd.to_datetime(early_default.LOADDT)
early_default_v2 = early_default.loc[early_default.LOADDT > early_date]
#early_default_v2 = early_default.loc[early_default.LOADDT < month_end_24m_prior]

# %%
early_choff.to_csv('early_stage_choff.csv')

# %%
# DRR NAV

NAV_choff = chargeoff.loc[chargeoff.CIF.isin(cif_list_NAV_lgd)]
NAV_choff.EFF_DT = pd.to_datetime(NAV_choff.EFF_DT)
NAV_choff_v2 = NAV_choff.loc[NAV_choff.EFF_DT > NAV_date]
#NAV_choff_v2 = NAV_choff.loc[NAV_choff.EFF_DT < month_end_24m_prior]

choff_NAV_cif = NAV_choff_v2.CIF.unique()

recovery_NAV = recovery.loc[recovery.CIF.isin(choff_NAV_cif)]

NAV_net_choff = pd.concat([NAV_choff_v2, recovery_NAV])

NAV_net_choff_v2 = NAV_net_choff.groupby(['CIF','FINAL_LGD', 'FACILITY_TYP'])['TRNSCTN_AMT'].sum().reset_index()

NAV_default = default_flag_data.loc[default_flag_data.CIF.isin(cif_list_NAV_lgd)]
NAV_default.LOADDT = pd.to_datetime(NAV_default.LOADDT)
NAV_default_v2 = NAV_default.loc[NAV_default.LOADDT > NAV_date]
#NAV_default_v2 = NAV_default.loc[NAV_default.LOADDT < month_end_24m_prior]

# %%
# DRR firm

firm_choff = chargeoff.loc[chargeoff.CIF.isin(cif_list_firm_lgd)]
firm_choff.EFF_DT = pd.to_datetime(firm_choff.EFF_DT)
firm_choff_v2 = firm_choff.loc[firm_choff.EFF_DT > firm_date]
#firm_choff_v2 = firm_choff.loc[firm_choff.EFF_DT < month_end_24m_prior]

choff_firm_cif = firm_choff_v2.CIF.unique()

recovery_firm = recovery.loc[recovery.CIF.isin(choff_firm_cif)]

firm_net_choff = pd.concat([firm_choff_v2, recovery_firm])

firm_net_choff_v2 = firm_net_choff.groupby(['CIF','FINAL_LGD', 'FACILITY_TYP'])['TRNSCTN_AMT'].sum().reset_index()

firm_default = default_flag_data.loc[default_flag_data.CIF.isin(cif_list_firm_lgd)]
firm_default.LOADDT = pd.to_datetime(firm_default.LOADDT)
firm_default_v2 = firm_default.loc[firm_default.LOADDT > firm_date]
#firm_default_v2 = firm_default.loc[firm_default.LOADDT < month_end_24m_prior]

# %%
all_default_cifs = []

all_default_cifs.append(choff_large_corp_cif)
all_default_cifs.append(choff_mid_cif)
all_default_cifs.append(choff_early_cif)
all_default_cifs.append(choff_ccloc_cif)
all_default_cifs.append(choff_NAV_cif)
all_default_cifs.append(choff_firm_cif)

list0 = [item for sublist in all_default_cifs for item in sublist]
list1 = """' , '""".join([str(item) for item in list0])
list2 = "'" + list1[:] + "'" + list1[0:0]
#print(list2)

# %%
# Pull final balance for the defaulted accounts

sql_balance = """

select a.LOADDT, a.CIF, a.FACILITY_TYPE AS FACILITYTYPE, a.NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] a

inner join 

(select cif, facility_type, max(loaddt) as max_date from 

[CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' and NET_LOAN_BAL > 0
group by cif, facility_type) b

on a.cif = b.cif and a.loaddt = b.max_date and a.facility_type = b.facility_type 

where a.cif in ({list2})

""".format(list2=list2)


default_balance = pd.read_sql_query(sql_balance, conn)

# %%
def is_consistent(row):
    grade = row['FACILITYTYPE']
    description = row['FINAL_LGD']
    # Check if the description is in the list of acceptable words for that grade
    if grade in grade_map and description in grade_map[grade]:
        return True
    else:
        return False



# %%
default_balance.shape

# %%
# Join last balance with chargeoff and recovery data 
#large corp

large_corp_all =  pd.merge(large_corp_net_choff_v2, default_balance, left_on=['CIF', 'FACILITY_TYP'], right_on= ['CIF', 'FACILITYTYPE'], how='inner')
mid_all =  pd.merge(mid_net_choff_v2, default_balance, left_on=['CIF', 'FACILITY_TYP'], right_on= ['CIF', 'FACILITYTYPE'], how='inner')
early_all =  pd.merge(early_net_choff_v2, default_balance, left_on=['CIF', 'FACILITY_TYP'], right_on= ['CIF', 'FACILITYTYPE'], how='inner')
ccloc_all =  pd.merge(CCLOC_net_choff_v2, default_balance, left_on=['CIF', 'FACILITY_TYP'], right_on= ['CIF', 'FACILITYTYPE'], how='inner')
nav_all =  pd.merge(NAV_net_choff_v2, default_balance, left_on=['CIF', 'FACILITY_TYP'], right_on= ['CIF', 'FACILITYTYPE'], how='inner')
firm_all =  pd.merge(firm_net_choff_v2, default_balance, left_on=['CIF', 'FACILITY_TYP'], right_on= ['CIF', 'FACILITYTYPE'], how='inner')


large_corp_all['lgd_low'] = 0
mid_all['lgd_low'] = 0
early_all['lgd_low'] = 0
ccloc_all['lgd_low'] = 0
nav_all['lgd_low'] = 0
firm_all['lgd_low'] = 0


large_corp_all['lgd_high'] = 0
mid_all['lgd_high'] = 0
early_all['lgd_high'] = 0
ccloc_all['lgd_high'] = 0
nav_all['lgd_high'] = 0
firm_all['lgd_high'] = 0







large_corp_all['not_modified'] = large_corp_all.apply(is_consistent, axis = 1)
mid_all['not_modified'] = mid_all.apply(is_consistent, axis = 1)
early_all['not_modified'] = early_all.apply(is_consistent, axis = 1)
ccloc_all['not_modified'] = ccloc_all.apply(is_consistent, axis = 1)
nav_all['not_modified'] = nav_all.apply(is_consistent, axis = 1)
firm_all['not_modified'] = firm_all.apply(is_consistent, axis = 1)


large_corp_all['lgd_low'] = large_corp_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_LOW'])
mid_all['lgd_low'] = mid_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_LOW'])
early_all['lgd_low'] = early_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_LOW'])
ccloc_all['lgd_low'] = ccloc_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_LOW'])
nav_all['lgd_low'] = nav_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_LOW'])
firm_all['lgd_low'] = firm_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_LOW'])


large_corp_all['lgd_high'] = large_corp_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_HIGH'])
mid_all['lgd_high'] = mid_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_HIGH'])
early_all['lgd_high'] = early_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_HIGH'])
ccloc_all['lgd_high'] = ccloc_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_HIGH'])
nav_all['lgd_high'] = nav_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_HIGH'])
firm_all['lgd_high'] = firm_all['FACILITYTYPE'].map(masterscale.set_index('FACILITY_TYPE')['LGD_HIGH'])



large_corp_all['lgd_mid'] = (large_corp_all['lgd_high'] + large_corp_all['lgd_low'])/2
mid_all['lgd_mid'] = (mid_all['lgd_high'] + mid_all['lgd_low'])/2
early_all['lgd_mid'] = (early_all['lgd_high'] + early_all['lgd_low'])/2
ccloc_all['lgd_mid'] = (ccloc_all['lgd_high'] + ccloc_all['lgd_low'])/2
nav_all['lgd_mid'] = (nav_all['lgd_high'] + nav_all['lgd_low'])/2
firm_all['lgd_mid'] = (firm_all['lgd_high'] + firm_all['lgd_low'])/2




large_corp_all['lgd_actual'] = large_corp_all['TRNSCTN_AMT']/large_corp_all['NET_LOAN_BAL']
mid_all['lgd_actual'] = mid_all['TRNSCTN_AMT']/mid_all['NET_LOAN_BAL']
early_all['lgd_actual'] = early_all['TRNSCTN_AMT']/early_all['NET_LOAN_BAL']
ccloc_all['lgd_actual'] = ccloc_all['TRNSCTN_AMT']/ccloc_all['NET_LOAN_BAL']
nav_all['lgd_actual'] = nav_all['TRNSCTN_AMT']/nav_all['NET_LOAN_BAL']
firm_all['lgd_actual'] = firm_all['TRNSCTN_AMT']/firm_all['NET_LOAN_BAL']


large_corp_sorted = large_corp_all.sort_values(by='FINAL_LGD', ascending=True)

mid_sorted = mid_all.sort_values(by='FINAL_LGD', ascending=True)

early_sorted = early_all.sort_values(by='FINAL_LGD', ascending=True)

ccloc_sorted = ccloc_all.sort_values(by='FINAL_LGD', ascending=True)

nav_sorted = nav_all.sort_values(by='FINAL_LGD', ascending=True)

firm_sorted = firm_all.sort_values(by='FINAL_LGD', ascending=True)


large_corp_monotonic = large_corp_sorted['lgd_actual'].is_monotonic_increasing
mid_monotonic = mid_sorted['lgd_actual'].is_monotonic_increasing
early_monotonic = early_sorted['lgd_actual'].is_monotonic_increasing
ccloc_monotonic = ccloc_sorted['lgd_actual'].is_monotonic_increasing
nav_monotonic = nav_sorted['lgd_actual'].is_monotonic_increasing
firm_monotonic = firm_sorted['lgd_actual'].is_monotonic_increasing


lgd_monotonic = []

lgd_monotonic.append(large_corp_monotonic)
lgd_monotonic.append(mid_monotonic)
lgd_monotonic.append(early_monotonic)
lgd_monotonic.append(ccloc_monotonic)
lgd_monotonic.append(nav_monotonic)
lgd_monotonic.append(firm_monotonic)

model_names = ['Large Corp', 'Mid Size', 'Early Stage', 'CCLOC', 'NAV', 'GFB Firm']
lgd_monotonic2 = pd.DataFrame({'Model': model_names, 'Monotonic': lgd_monotonic})
lgd_monotonic2.to_csv('LGD_Rank_Ordering.csv')


large_corp_sorted['Pred_Amount'] = large_corp_sorted['NET_LOAN_BAL']*large_corp_sorted['lgd_mid']
mid_sorted['Pred_Amount'] = mid_sorted['NET_LOAN_BAL']*mid_sorted['lgd_mid']
early_sorted['Pred_Amount'] = early_sorted['NET_LOAN_BAL']*early_sorted['lgd_mid']
ccloc_sorted['Pred_Amount'] = ccloc_sorted['NET_LOAN_BAL']*ccloc_sorted['lgd_mid']
nav_sorted['Pred_Amount'] = nav_sorted['NET_LOAN_BAL']*nav_sorted['lgd_mid']
firm_sorted['Pred_Amount'] = firm_sorted['NET_LOAN_BAL']*firm_sorted['lgd_mid']

large_corp_sorted['Bad_Ind'] = (large_corp_sorted['TRNSCTN_AMT'] > 0).astype(int)
mid_sorted['Bad_Ind'] = (mid_sorted['TRNSCTN_AMT'] >  0).astype(int)
early_sorted['Bad_Ind'] = (early_sorted['TRNSCTN_AMT'] >  0).astype(int)
ccloc_sorted['Bad_Ind'] = (ccloc_sorted['TRNSCTN_AMT'] >  0).astype(int)
nav_sorted['Bad_Ind'] = (nav_sorted['TRNSCTN_AMT'] >  0).astype(int)
firm_sorted['Bad_Ind'] = (firm_sorted['TRNSCTN_AMT'] >  0).astype(int)

lgd_accuracy = []

large_corp_mae = abs(large_corp_sorted['Pred_Amount'].sum() - large_corp_sorted['TRNSCTN_AMT'].sum())/large_corp_sorted['NET_LOAN_BAL'].sum()
mid_mae = abs(mid_sorted['Pred_Amount'].sum() - mid_sorted['TRNSCTN_AMT'].sum())/mid_sorted['NET_LOAN_BAL'].sum()
early_mae = abs(early_sorted['Pred_Amount'].sum() - early_sorted['TRNSCTN_AMT'].sum())/early_sorted['NET_LOAN_BAL'].sum()
ccloc_mae = abs(ccloc_sorted['Pred_Amount'].sum() - ccloc_sorted['TRNSCTN_AMT'].sum())/ccloc_sorted['NET_LOAN_BAL'].sum()
nav_mae = abs(nav_sorted['Pred_Amount'].sum() - nav_sorted['TRNSCTN_AMT'].sum())/nav_sorted['NET_LOAN_BAL'].sum()
firm_mae = abs(firm_sorted['Pred_Amount'].sum() - firm_sorted['TRNSCTN_AMT'].sum())/firm_sorted['NET_LOAN_BAL'].sum()

lgd_accuracy.append(large_corp_mae)
lgd_accuracy.append(mid_mae)
lgd_accuracy.append(early_mae)
lgd_accuracy.append(ccloc_mae)
lgd_accuracy.append(nav_mae)
lgd_accuracy.append(firm_mae)



large_corp_no_override = large_corp_sorted.loc[large_corp_sorted.not_modified == 1]
mid_no_override = mid_sorted.loc[mid_sorted.not_modified == 1]
early_no_override = early_sorted.loc[early_sorted.not_modified == 1]
ccloc_no_override = ccloc_sorted.loc[ccloc_sorted.not_modified == 1]
nav_no_override = nav_sorted.loc[nav_sorted.not_modified == 1]
firm_no_override = firm_sorted.loc[firm_sorted.not_modified == 1]

large_corp_override = large_corp_sorted.loc[large_corp_sorted.not_modified != 1]
mid_override = mid_sorted.loc[mid_sorted.not_modified != 1]
early_override = early_sorted.loc[early_sorted.not_modified != 1]
ccloc_override = ccloc_sorted.loc[ccloc_sorted.not_modified != 1]
nav_override = nav_sorted.loc[nav_sorted.not_modified != 1]
firm_override = firm_sorted.loc[firm_sorted.not_modified != 1]

large_corp_no_or_loss = large_corp_no_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
mid_no_or_loss = mid_no_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
early_no_or_loss = early_no_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
ccloc_no_or_loss = ccloc_no_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
nav_no_or_loss = nav_no_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
firm_no_or_loss = firm_no_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))

large_corp_or_loss = large_corp_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
mid_or_loss = mid_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
early_or_loss = early_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
ccloc_or_loss = ccloc_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
nav_or_loss = nav_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))
firm_or_loss = firm_override.groupby('FINAL_LGD').agg(total_pred_amount=('Pred_Amount','sum'),total_loss_amount=('TRNSCTN_AMT','sum'),total_balance= ('NET_LOAN_BAL','sum'),total_obligors=('NET_LOAN_BAL','count'))

large_corp_no_or_loss['mae'] = abs(large_corp_no_or_loss['total_pred_amount'] - large_corp_no_or_loss['total_loss_amount'])/large_corp_no_or_loss['total_balance']
large_corp_or_loss['mae'] = abs(large_corp_or_loss['total_pred_amount'] - large_corp_or_loss['total_loss_amount'])/large_corp_or_loss['total_balance']

mid_no_or_loss['mae'] = abs(mid_no_or_loss['total_pred_amount'] - mid_no_or_loss['total_loss_amount'])/mid_no_or_loss['total_balance']
mid_or_loss['mae'] = abs(mid_or_loss['total_pred_amount'] - mid_or_loss['total_loss_amount'])/mid_or_loss['total_balance']

early_no_or_loss['mae'] = abs(early_no_or_loss['total_pred_amount'] - early_no_or_loss['total_loss_amount'])/early_no_or_loss['total_balance']
early_or_loss['mae'] = abs(early_or_loss['total_pred_amount'] - early_or_loss['total_loss_amount'])/early_or_loss['total_balance']

ccloc_no_or_loss['mae'] = abs(ccloc_no_or_loss['total_pred_amount'] - ccloc_no_or_loss['total_loss_amount'])/ccloc_no_or_loss['total_balance']
ccloc_or_loss['mae'] = abs(ccloc_or_loss['total_pred_amount'] - ccloc_or_loss['total_loss_amount'])/ccloc_or_loss['total_balance']

nav_no_or_loss['mae'] = abs(nav_no_or_loss['total_pred_amount'] - nav_no_or_loss['total_loss_amount'])/nav_no_or_loss['total_balance']
nav_or_loss['mae'] = abs(nav_or_loss['total_pred_amount'] - nav_or_loss['total_loss_amount'])/nav_or_loss['total_balance']

firm_no_or_loss['mae'] = abs(firm_no_or_loss['total_pred_amount'] - firm_no_or_loss['total_loss_amount'])/firm_no_or_loss['total_balance']
firm_or_loss['mae'] = abs(firm_or_loss['total_pred_amount'] - firm_or_loss['total_loss_amount'])/firm_or_loss['total_balance']




# %%
#total counts override

large_corp_bad_or_total = large_corp_override.groupby('FINAL_LGD')['CIF'].count()

mid_bad_or_total = mid_override.groupby('FINAL_LGD')['CIF'].count()

early_bad_or_total = early_override.groupby('FINAL_LGD')['CIF'].count()

ccloc_bad_or_total = ccloc_override.groupby('FINAL_LGD')['CIF'].count()

nav_bad_or_total = nav_override.groupby('FINAL_LGD')['CIF'].count()

firm_bad_or_total = firm_override.groupby('FINAL_LGD')['CIF'].count()


#bad counts override

large_corp_bad_or = large_corp_override.groupby('FINAL_LGD')['Bad_Ind'].count()

mid_bad_or = mid_override.groupby('FINAL_LGD')['Bad_Ind'].count()

early_bad_or = early_override.groupby('FINAL_LGD')['Bad_Ind'].count()

ccloc_bad_or = ccloc_override.groupby('FINAL_LGD')['Bad_Ind'].count()

nav_bad_or = nav_override.groupby('FINAL_LGD')['Bad_Ind'].count()

firm_bad_or = firm_override.groupby('FINAL_LGD')['Bad_Ind'].count()



#total counts no override

large_corp_bad_no_or_total = large_corp_override.groupby('FINAL_LGD')['CIF'].count()

mid_bad_no_or_total = mid_override.groupby('FINAL_LGD')['CIF'].count()

early_bad_no_or_total = early_override.groupby('FINAL_LGD')['CIF'].count()

ccloc_bad_no_or_total = ccloc_override.groupby('FINAL_LGD')['CIF'].count()

nav_bad_no_or_total = nav_override.groupby('FINAL_LGD')['CIF'].count()

firm_bad_no_or_total = firm_override.groupby('FINAL_LGD')['CIF'].count()


#bad counts no override

large_corp_bad_no_or = large_corp_override.groupby('FINAL_LGD')['Bad_Ind'].count()

mid_bad_no_or = mid_override.groupby('FINAL_LGD')['Bad_Ind'].count()

early_bad_no_or = early_override.groupby('FINAL_LGD')['Bad_Ind'].count()

ccloc_bad_no_or = ccloc_override.groupby('FINAL_LGD')['Bad_Ind'].count()

nav_bad_no_or = nav_override.groupby('FINAL_LGD')['Bad_Ind'].count()

firm_bad_no_or = firm_override.groupby('FINAL_LGD')['Bad_Ind'].count()



#lgd_mid

large_corp_mid = large_corp_override.groupby('FINAL_LGD')['lgd_mid'].mean()

mid_mid = mid_override.groupby('FINAL_LGD')['lgd_mid'].mean()

early_mid = early_override.groupby('FINAL_LGD')['lgd_mid'].mean()

ccloc_mid = ccloc_override.groupby('FINAL_LGD')['lgd_mid'].mean()

nav_mid = nav_override.groupby('FINAL_LGD')['lgd_mid'].mean()

firm_mid = firm_override.groupby('FINAL_LGD')['lgd_mid'].mean()


#large_corp_joined = pd.merge( large_corp_mid, large_corp_bad_or, large_corp_bad_or_total,large_corp_bad_no_or, large_corp_bad_no_or_total, on='FINAL_LGD')

# %%
override_all = []


ccloc_override = ccloc_all['not_modified'].sum()/ccloc_all.shape[0]

override_all.append(ccloc_override) 

nav_override = nav_all['not_modified'].sum()/nav_all.shape[0]

override_all.append(nav_override) 

firm_override = firm_all['not_modified'].sum()/firm_all.shape[0]

override_all.append(firm_override) 

large_corp_override = large_corp_all['not_modified'].sum()/large_corp_all.shape[0]

override_all.append(large_corp_override) 

mid_override = mid_all['not_modified'].sum()/mid_all.shape[0]

override_all.append(mid_override) 

early_override = early_all['not_modified'].sum()/early_all.shape[0]

override_all.append(early_override) 

# %%
model_list = ['Large Corp', 'Mid Size', 'Early Stage', 'CCLOC', 'NAV', 'GFB Firm']

lgd_accuracy2 = pd.DataFrame({'Model': model_list, 'Accuracy': lgd_accuracy})
lgd_accuracy2.to_csv('LGD_Accuracy_All_Models.csv')

# %%
large_corp_or_loss.to_csv('large_corp_or.csv')
large_corp_no_or_loss.to_csv('large_corp_no_or.csv')

mid_or_loss.to_csv('mid_or.csv')
mid_no_or_loss.to_csv('mid_no_or.csv')

early_or_loss.to_csv('early_or.csv')
early_no_or_loss.to_csv('early_no_or.csv')

ccloc_or_loss.to_csv('ccloc_or.csv')
ccloc_no_or_loss.to_csv('ccloc_no_or.csv')

nav_or_loss.to_csv('nav_or.csv')
nav_no_or_loss.to_csv('nav_no_or.csv')

firm_or_loss.to_csv('firm_or.csv')
firm_no_or_loss.to_csv('firm_no_or.csv')

# %%
mid_sorted.to_csv('mid_sorted.csv')

# %%
#LGD PSI Calculation

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

    # Ensure data is in a numpy array
    expected_counts = np.array(expected_data)
    actual_counts = np.array(actual_data)

   
    # Calculate counts and proportions for each bin
    expected_props = expected_counts / expected_counts.sum()
    actual_props = actual_counts / actual_counts.sum()

    expected_props = np.where(expected_props == 0, 0.0001, expected_props)
    actual_props = np.where(actual_props == 0, 0.0001, actual_props)


  

    # Calculate PSI for each bin
    psi_per_bin = (actual_props - expected_props) * np.log(actual_props / expected_props)

    # Sum the PSI for all bins to get the total PSI
    total_psi = np.sum(psi_per_bin)

    return total_psi




# %%
# get benchmark data for all models

list_large1 = """' , '""".join([str(item) for item in cif_list_large_lgd])
list_large2 = "'" + list_large1[:] + "'" + list_large1[0:0]



sql_large = """

select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 

and  cif in ({list_large}) and loaddt in ( '09-30-2025', '03-31-2026') 

""".format(list_large=list_large2)


psi_large = pd.read_sql_query(sql_large, conn)



# %%
# get benchmark data for all models

list_mid1 = """' , '""".join([str(item) for item in cif_list_mid_lgd])
list_mid2 = "'" + list_mid1[:] + "'" + list_mid1[0:0]


sql_mid = """

select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 

and  cif in ({list_large}) and loaddt in ( '09-30-2025', '03-31-2026') 

""".format(list_large=list_mid2)



psi_mid = pd.read_sql_query(sql_mid, conn)



# %%
# get benchmark data for all models

list_early1 = """' , '""".join([str(item) for item in cif_list_early_lgd])
list_early2 = "'" + list_early1[:] + "'" + list_early1[0:0]



sql_early = """

select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 

and  cif in ({list_early}) and loaddt in ( '09-30-2025', '03-31-2026') 

""".format(list_early=list_early2)

psi_early = pd.read_sql_query(sql_early, conn)



# %%
# get benchmark data for all models

list_ccloc1 = """' , '""".join([str(item) for item in cif_list_CCLOC_lgd])
list_ccloc2 = "'" + list_ccloc1[:] + "'" + list_ccloc1[0:0]



sql_ccloc = """

select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 

and  cif in ({list_ccloc}) and loaddt in ( '09-30-2025', '03-31-2026') 

""".format(list_ccloc=list_ccloc2)

psi_ccloc = pd.read_sql_query(sql_ccloc, conn)



# %%
# get benchmark data for all models

list_nav1 = """' , '""".join([str(item) for item in cif_list_NAV_lgd])
list_nav2 = "'" + list_nav1[:] + "'" + list_nav1[0:0]



sql_nav = """

select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 

and  cif in ({list_nav}) and loaddt in ( '09-30-2025', '03-31-2026') 

""".format(list_nav=list_nav2)

psi_nav = pd.read_sql_query(sql_nav, conn)



# %%
# get benchmark data for all models

list_firm1 = """' , '""".join([str(item) for item in cif_list_firm_lgd])
list_firm2 = "'" + list_firm1[:] + "'" + list_firm1[0:0]



sql_firm = """

select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 

and  cif in ({list_firm}) and loaddt in ( '09-30-2025', '03-31-2026') 

""".format(list_firm=list_firm2)

psi_firm = pd.read_sql_query(sql_firm, conn)



# %%
# divide data into benchmark and current data 

psi_large_bench = psi_large.loc[psi_large.LOADDT == '2025-09-30']
psi_large_current = psi_large.loc[psi_large.LOADDT == last_month_end1]

psi_mid_bench = psi_mid.loc[psi_mid.LOADDT == '2025-09-30']
psi_mid_current = psi_mid.loc[psi_mid.LOADDT == last_month_end1]

psi_early_bench = psi_early.loc[psi_early.LOADDT == '2025-09-30']
psi_early_current = psi_early.loc[psi_early.LOADDT == last_month_end1]

psi_ccloc_bench = psi_ccloc.loc[psi_ccloc.LOADDT == '2025-09-30']
psi_ccloc_current = psi_ccloc.loc[psi_ccloc.LOADDT == last_month_end1]

psi_nav_bench = psi_nav.loc[psi_nav.LOADDT == '2025-09-30']
psi_nav_current = psi_nav.loc[psi_nav.LOADDT == last_month_end1]

psi_firm_bench = psi_firm.loc[psi_firm.LOADDT == '2025-09-30']
psi_firm_current = psi_firm.loc[psi_firm.LOADDT == last_month_end1]



# %%
psi_large_bench2 = psi_large_bench.groupby('FINAL_LGD')['CIF'].count().to_frame()
psi_large_current2 = psi_large_current.groupby('FINAL_LGD')['CIF'].count().to_frame()

psi_mid_bench2 = psi_mid_bench.groupby('FINAL_LGD')['CIF'].count().to_frame()
psi_mid_current2 = psi_mid_current.groupby('FINAL_LGD')['CIF'].count().to_frame()

psi_early_bench2 = psi_early_bench.groupby('FINAL_LGD')['CIF'].count().to_frame()
psi_early_current2 = psi_early_current.groupby('FINAL_LGD')['CIF'].count().to_frame()

psi_ccloc_bench2 = psi_ccloc_bench.groupby('FINAL_LGD')['CIF'].count().to_frame()
psi_ccloc_current2 = psi_ccloc_current.groupby('FINAL_LGD')['CIF'].count().to_frame()

psi_nav_bench2 = psi_nav_bench.groupby('FINAL_LGD')['CIF'].count().to_frame()
psi_nav_current2 = psi_nav_current.groupby('FINAL_LGD')['CIF'].count().to_frame()

psi_firm_bench2 = psi_firm_bench.groupby('FINAL_LGD')['CIF'].count().to_frame()
psi_firm_current2 = psi_firm_current.groupby('FINAL_LGD')['CIF'].count().to_frame()

# %%
psi_large2 = pd.merge(psi_large_bench2, psi_large_current2, how='inner', on='FINAL_LGD')

psi_mid2 = pd.merge(psi_mid_bench2, psi_mid_current2, how='inner', on='FINAL_LGD')

psi_early2 = pd.merge(psi_early_bench2, psi_early_current2, how='inner', on='FINAL_LGD')

psi_ccloc2 = pd.merge(psi_ccloc_bench2, psi_ccloc_current2, how='inner', on='FINAL_LGD')

psi_nav2 = pd.merge(psi_nav_bench2, psi_nav_current2, how='inner', on='FINAL_LGD')

psi_firm2 = pd.merge(psi_firm_bench2, psi_firm_current2, how='inner', on='FINAL_LGD')

# %%
#calculate psi for gfb ccloc portfolio 
psi_lgd_output = []

psi_list = [psi_large2, psi_mid2, psi_early2, psi_ccloc2, psi_nav2, psi_firm2]

for b in psi_list:
        expected_data = b['CIF_x'].tolist()
        actual_data = b['CIF_y'].tolist()
        try: 
                psi_input = calculate_psi(expected_data, actual_data)
        except ValueError:
                psi_input = 0
        psi_lgd_output.append(psi_input)

# %%
expected_data = psi_early2['CIF_x'].tolist()
actual_data = psi_early2['CIF_y'].tolist()

test = calculate_psi(expected_data,actual_data)
test

# %%


psi_lgd_output2 = pd.DataFrame({'Model_Name': model_list, 'Output_PSI': psi_lgd_output})
psi_lgd_output2.to_csv('LGD_Output_PSI.csv')

# %%
import math

"""

firm_mae = abs(firm_sorted['Pred_Amount'].sum() - firm_sorted['Amount'].sum())/firm_sorted['NET_LOAN_BAL'].sum()

"""


data_list = [large_corp_sorted, mid_sorted, early_sorted]

accuracy_threshold = []
perc_threshold_hard1 = []
perc_threshold_soft1 = []

for j in range(3):
    for i in range(1000):
        n_1 = math.ceil(data_list[j].shape[0]*0.8)
        df = data_list[j].sample(n=n_1, replace=True)
        df = df.fillna(0)
       
        
        MAE_df =  abs(df['Pred_Amount'].sum() - df['TRNSCTN_AMT'].sum())/df['NET_LOAN_BAL'].sum()
      
        accuracy_threshold.append(MAE_df)
    try: 
        perc_threshold_hard = np.percentile(accuracy_threshold, 98)
    except IndexError: 
        perc_threshold_hard = 0
    try: 
        perc_threshold_soft = np.percentile(accuracy_threshold, 80)
    except IndexError:
        perc_threshold_soft = 0
    perc_threshold_hard1.append(perc_threshold_hard)
    perc_threshold_soft1.append(perc_threshold_soft)




# %%
#Exporting thresholds

perc_threshold_soft2 = pd.DataFrame(list(zip(model_name, perc_threshold_soft1)), columns=['Model_Name', 'Soft_Breach'])
perc_threshold_soft2.to_csv('Soft_Breach_Accuracy_Threshold_LGD.csv')

perc_threshold_hard2 = pd.DataFrame(list(zip(model_name, perc_threshold_hard1)), columns=['Model_Name', 'Hard_Breach'])
perc_threshold_hard2.to_csv('Hard_Breach_Accuracy_Threshold_LGD.csv')


