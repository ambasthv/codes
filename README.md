# %% [markdown]
# ### Importing Libraries and Setting Dates 

# %%

# ### Importing libraries to be used for importing data and calculations and model dev and validation


import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.3f}'.format
pd.set_option('display.max_columns',None)

import pyodbc

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

# %%
kpi_dict2 = {
'KPI 7'	: 'Population Stability Index : Input',
'KPI 8'	: 'Coefficient Stability' }

model_name =  ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage']

# %% [markdown]
# ##### create dates to be used for generating performance monitoring KPIs
# 

# %%

import os
#print(os.getcwd())

current_date = date.today()
month_end = current_date + relativedelta(day=31)
last_month_end = month_end - relativedelta(months = 0)
last_month_end = last_month_end + pd.offsets.MonthEnd(n=-1)
last_month_end1 = last_month_end.strftime("%m/%d/%Y")

month_end_3m_prior = month_end -relativedelta(months=4)

month_end_3m_prior = month_end_3m_prior + pd.offsets.MonthEnd(n=0)
month_end_3m_prior = month_end_3m_prior.strftime("%m/%d/%Y")



month_end_12m_prior = month_end - relativedelta(months=12)

month_end_12m_prior = month_end_12m_prior + pd.offsets.MonthEnd(n=-1)
month_end_12m_prior = month_end_12m_prior.strftime("%m/%d/%Y")

month_end_24m_prior = month_end - relativedelta(months=24)

month_end_24m_prior = month_end_24m_prior + pd.offsets.MonthEnd(n=0)
month_end_24m_prior = month_end_24m_prior.strftime("%m/%d/%Y")



last_month = last_month_end.month
kpi_quarter = month_to_quarter(last_month)





model_name = ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage']


# %%
print(last_month_end1, kpi_quarter, month_end_12m_prior)

# %% [markdown]
# ### Establish connection to SQL server

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
# #### Section 1: Large Corp Model Performance Monitoring

# %% [markdown]
# ### SQL Query 1: Extracting data from following tables:
# #### Credit Lens Staging Table
# #### Default Flag Table
# #### GL Table (for Balances and Loan Level Info) 
# 
# 
# #### QUERY DETAILS
# #### 1-Get all columns from credit lens table (z)
# #### 2-Get first default date from defaults table (y)
# #### 3-Get crr as-of statement date from defaults table (x)
# #### 4-Get CRR with 3month forward lag from defaults table (w)
# #### 5-Get CRR with 6month forward lag from defaults table (v)
# #### 6-Get LIFESTAGE and CRR from gross loans table as-of STATEMENTDATE (u)
# #### 7-RBS is not extracted in this query

# %%


qrystr12 = """select eomonth(cast(z.statementdate as date)) as loaddt,
    z.CIF_CRM,
    
    z.CUSTOMERNAME, 
    z.STATEMENTID,
    z.STATEMENTYEAR,
    z.STATEMENTDATE,
    z.AUDITMETHOD,
    z.STATEMENTTYPE,
    z.ANALYST,
    z.SOURCECURRENCY,
    z.TARGETCURRENCY,
    z.NETSALES,
    z.TOTALASSETS,
    z.TDEBITDA,
    z.GROSSMARGIN,
    z.CURRENTRATIO,
    z.FIXEDCHARGECOVER,
   
    
    y.first_def_date,
    x.mcrr, x.mcrr_date,
    w.mcrr3, w.mcrr3_date,
    v.mcrr6, v.mcrr6_date,
    u.LIFESTAGE,u.crr_gross, u.tot_orig_bal, u.tot_net_bal
from
    CRDADMPRD.dbo.CDM_CLIENT_FINANCIALS_VW z

left outer join (SELECT cif, min(loaddt) AS first_def_date FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
    WHERE (DEFAULT_FLAG = 1 and RISK_CD in('5','6','7','8','9','10'))
    GROUP BY cif) y
    on y.cif = z.cif_crm

left outer join (SELECT cif, RISK_CD as mcrr, LOADDT as mcrr_date FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]) x
    on x.cif = z.cif_crm
    and eomonth(x.mcrr_date) = eomonth(cast(z.statementdate as date))

left outer join (SELECT cif, RISK_CD as mcrr3, LOADDT as mcrr3_date FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]) w
    on w.cif = z.cif_crm
    and eomonth(w.mcrr3_date) = eomonth(cast(z.statementdate as date),3)

left outer join (SELECT cif, RISK_CD as mcrr6, LOADDT as mcrr6_date FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]) v
    on v.cif = z.cif_crm
    and eomonth(v.mcrr6_date) = eomonth(cast(z.statementdate as date),6)

left outer join (select cif,   loaddt, max(LIFESTAGE) as LIFESTAGE, max(RISKCD) as crr_gross,
    SUM(FACEAMTOFNOTEORGNLBAL) as tot_orig_bal, SUM(NOTEPRNCPLBALNET) as tot_net_bal
    FROM CRDADMPRD..GLV_Historical_DW_Gross_Loans_Adjusted
    WHERE (FACILITY_TYPE <> 'GUD')
    GROUP BY cif, loaddt) u
    on u.cif = z.cif_crm and eomonth(cast(u.loaddt as date)) = eomonth(cast(z.statementdate as date))  
where
   
z.statementdate >= '{month_end_24m_prior}' and 
    z.statementmonths = 12
""".format(month_end_24m_prior=month_end_24m_prior)




# %% [markdown]
# ### Extracting data by running the SQL Query 1 with a connection to the Credit Database  

# %%


#creating dataframe by running SQL query 
df1 = pd.read_sql_query(qrystr12, conn)

#changing load date format to datetime
df1.loaddt = pd.to_datetime(df1.loaddt)
#changing first default date format to datetime
df1.first_def_date = pd.to_datetime(df1.first_def_date)






# %% [markdown]
# ### SQL Query 2 for creating a separate table with default data and loan level data
# ### Data sourced from: 
# #### Default Flag Table
# #### GL Table (for Balances and Loan Level Info

# %%


#query to get all defaults - this is not filtered by RBS



qrystr2 = """SELECT def.cif as cif_def, def.first_def_date, def.def_rbs_min, def.def_rbs_max,
    rbs.rbs_def, rbs.mcrr as mcrr_def,
    gross.cif as cif_gross, 
    gross.LOADDT, gross.NAMEADDRLN1, gross.LOAN_SHORTNAME, gross.RISKCD as gross_CRR,
    gross.CREDITLINEID, gross.FACILITY_TYPE, 
    gross.NOTEPRNCPLBALNET, gross.FACEAMTOFNOTEORGNLBAL,
    gross.LIFESTAGE, gross.CREDIT_LIFESTAGE
    
FROM (SELECT cif, min(loaddt) AS first_def_date, min(RISK_BAS_SEG_CD) AS def_rbs_min,  max(RISK_BAS_SEG_CD) AS def_rbs_max
    FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
    WHERE (DEFAULT_FLAG=1 and RISK_CD > 4 and RISK_CD in ('5','6','7','8','9','10'))
    GROUP BY cif) as def
    
INNER JOIN (SELECT cif, loaddt as mdate, risk_cd as mcrr, risk_bas_seg_cd as rbs_def FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]) as rbs
    ON (def.cif = rbs.cif and def.first_def_date = rbs.mdate)


    
LEFT OUTER JOIN CRDADMPRD..GLV_Historical_DW_Gross_Loans_Adjusted AS gross 
    ON RIGHT('00000' + def.cif,9) = RIGHT('00000' + gross.CIF,9)
    WHERE (((Year([def].[first_def_date]))=Year([gross].[loaddt])) AND 
           ((Month([def].[first_def_date]))=Month([gross].[loaddt])) AND
           (gross.STATUS_CD = 'A') and (gross.APPLID not in('G/', 'G/L','GL','LJ')) AND
           (gross.RISKCD in ('5','6','7','8','9','10')))
"""




# %% [markdown]
# ### Extracting data for the SQL query 2  

# %%


df2 = pd.read_sql_query(qrystr2, conn)





# %% [markdown]
# ### SQL Query 3 to source RBS for the Credit Lens Statement Date
# ### Data sourced from: 
# #### Credit Lens Staging Table
# #### Default Flag Table

# %%



#QUERY DETAILS
#1-Get identifier columns from Credit Lens table (z)
#2-Get RBS from defaults table aligned with the statement date (w)
#3-Get first date when CIF was assigned RBS CF SLBO or CF Other (x)
#4-Get rbs_last which is the rbs corresponding to the most recent date in the defaults table (v)
#5-Get rbs_first which is the rbs corresponding to the earliest in the defaults table (u)

qrystr3 = """SELECT z.CIF_CRM, RIGHT('00000' + z.CIF_CRM,9) as cif_pad, 
            z.STATEMENTDATE, z.STATEMENTYEAR, z.STATEMENTID, 
            w.mcrr as mcrr_stmtdate, w.rbs as rbs_stmtdate, x.mdate_firstCF, x.rbs_firstCF,
            v.rbs_last, v.crr_last, v.mdate as mdate_last,
            u.rbs_first, u.crr_first, u.mdate as mdate_first
            
    FROM CRDADMPRD.dbo.CDM_CLIENT_FINANCIALS_VW z
    
    LEFT OUTER JOIN (SELECT cif, risk_cd as mcrr, loaddt as mdate, risk_bas_seg_cd as rbs FROM  [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]) w
        on w.cif = z.CIF_CRM AND eomonth(w.mdate) = eomonth(z.STATEMENTDATE)
        
    LEFT OUTER JOIN (SELECT cif, min(loaddt) as mdate_firstCF, min(risk_bas_seg_cd) as rbs_firstCF FROM  [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
        WHERE risk_bas_seg_cd in ('CF - SLBO', 'CF - Other') 
        GROUP BY CIF) x
        on x.cif = z.CIF_CRM
        
    LEFT OUTER JOIN (
        SELECT a.cif, a.loaddt as mdate, a.risk_cd as crr_last, a.risk_bas_seg_cd as rbs_last FROM  [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW] a
        INNER JOIN ( select cif, max(loaddt) as mdate_max FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            where risk_cd <> '11'
            GROUP BY cif) b 
            ON a.cif = b.cif and a.loaddt = b.mdate_max
            ) v
            on v.cif = z.CIF_CRM
            
    LEFT OUTER JOIN (
    SELECT a.cif, a.loaddt as mdate, a.risk_cd as crr_first, a.risk_bas_seg_cd as rbs_first FROM  [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW] a
    INNER JOIN ( select cif, min(loaddt) as mdate_min FROM  [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
        where risk_cd <> '11'
        GROUP BY cif) b 
        ON a.cif = b.cif and a.loaddt = b.mdate_min
        ) u
        on u.cif = z.CIF_CRM

        left outer join (select distinct cif, loaddt   FROM CRDADMPRD..GLV_Historical_DW_Gross_Loans_Adjusted
    WHERE (FACILITY_TYPE <> 'GUD')
    ) s
    on s.cif = z.cif_crm and eomonth(cast(s.loaddt as date)) = eomonth(cast(z.statementdate as date)) 
        
    WHERE
       
       
    z.statementdate >= '{month_end_24m_prior}' and
        z.statementmonths = 12
""".format(month_end_24m_prior=month_end_24m_prior)




# %% [markdown]
# ### Extracting data for SQL query 3  

# %%


df3 = pd.read_sql_query(qrystr3, conn)




# %%


#define number of months to look back into financial statements to flag them as bad corresponding to a default

default_month_CUTOFF = 12




# %% [markdown]
# ### Merge subsets of df1 and df3 which adds RBS information to Financial Statements Dataset

# %%



#select columns to be merged from the df1 and df3 tables and create subsets of df1 and df3 

df1_cols = [ 'CIF_CRM', 'CUSTOMERNAME','STATEMENTID','STATEMENTYEAR','STATEMENTDATE',
            'AUDITMETHOD','STATEMENTTYPE','ANALYST','SOURCECURRENCY','TARGETCURRENCY',
            'LIFESTAGE','crr_gross', 'first_def_date','mcrr', 'mcrr_date', 'mcrr3', 'mcrr3_date','mcrr6', 'mcrr6_date',
            'tot_orig_bal', 'tot_net_bal'
            ]

df1v2 = df1[df1_cols].copy()

df3_cols = ['CIF_CRM', 'STATEMENTDATE','STATEMENTID','mcrr_stmtdate', 'rbs_stmtdate', 
            'mdate_firstCF', 'rbs_firstCF','rbs_last', 'crr_last', 'mdate_last', 'rbs_first', 'crr_first',
            'mdate_first']

df3v2 = df3[df3_cols].copy()

del df3
gc.collect()



# %% [markdown]
# ### Apply filters to exclude erroneous CIFs (Unknown, blank, NA, negative)
# 

# %%


mask2 = (df1v2['CIF_CRM'] == '')
mask3 = (df1v2['CIF_CRM'].isna())

df1v2 = df1v2[ ~mask2 & ~mask3 ]


mask2 = (df3v2['CIF_CRM'] == '')
mask3 = (df3v2['CIF_CRM'].isna())

df3v2 = df3v2[~mask2 & ~mask3 ]

# %%
# ### Merge Financial Statement dataframe with RBS dataframe

df1v3 = df1v2.merge(df3v2, 
                    how='inner',
                    left_on=['CIF_CRM','STATEMENTDATE','STATEMENTID'],
                    right_on=['CIF_CRM','STATEMENTDATE','STATEMENTID'])

del df1v2
gc.collect()




# %%
# ### Create ranks based on auditmethod, statementtype and analyst to select best statement in case of duplicates

# (1) - Rank the statement types
stmt_rnk = {"Annual":1,"Rolling Stmt":2,"FY-To-Date":3,"Quarterly":4,"Monthly":5,"placeholder": 5}


# (2) - Rank the auditmethod
audit_rnk = {"Unqualif'd":1,"Qualified":2,"Reviewed":3,"Compiled":4,"Co.Prep'd":5,"Svb Prep":6,"Tax Return":7,"placeholder": 7}


# (3) Rank analysts (accenture=2, else 1)
#set analyst_rank based on first three characters

def map_analyst(x):
    if x == 'ACS':
        map_analyst = 2
    else:
        map_analyst = 1
    return map_analyst

# %%
df1v3['ANALYST'].fillna('placeholder', inplace=True)


#create an audit rank column that provides the ranking for different audit methods

df1v3['audit_rank'] = df1v3['AUDITMETHOD'].map(audit_rnk)


#create a statement rank column that provides the ranking for different statement types

df1v3['statement_rank'] = df1v3['STATEMENTTYPE'].map(stmt_rnk)


#create an analyst rank column 

df1v3['analyst_rank'] = df1v3['ANALYST'].apply(map_analyst)

df1v3.loc[df1v3['ANALYST'].str.contains("-ACS-"), 'analyst_rank'] = 2

# analyst ACS can also be in the middle of the analyst name
# use slicing to modify the rank of those indices whose analyst name have -ACS- in the middle



# %%


# Create a sum of all ranks

df1v3 = df1v3.assign(rank_sum = lambda x: x['audit_rank'] + x['statement_rank'] + x['analyst_rank'])

# for each cif and statement year combination, sort the data by ranks so that the highest rank can be picked
# preference is to pick by best audit quality, then best statement type and then svb analyst

df1v3.sort_values(by=['CIF_CRM','STATEMENTYEAR',
                'audit_rank','statement_rank','analyst_rank','STATEMENTID','rank_sum'],
                ascending=[True,True,True,True,True,False,True], inplace=True)


# since data is sorted in the desired order of importance, create an overall rank column for each group such that
## the first entry gets rank 1
df1v3['overall_rank'] = df1v3.groupby(['CIF_CRM','STATEMENTYEAR'])['rank_sum'].rank('first')




# %%

# ### Apply filters created based on audit, statement method and analyst to pick best statement per CIF and statement date 
#pick statements with overall rank = 1 

mask1 = (df1v3['overall_rank'] == 1)

# filter out statements with unknown or blank CIF 

mask2 = (df1v3['CIF_CRM'].str.contains('UNKN'))
mask3 = (df1v3['CIF_CRM'] == '')

#create dataframes with the 3 filters

df1v4 = df1v3[mask1 & ~mask2 & ~mask3].copy()

del df1v3
gc.collect()

# %%

#Step 3
#Change from "M" to "m"
#Create a date difference column representing no. of months between statement date and default date
df1v4 = df1v4.assign(def_date_diff = (df1v4['STATEMENTDATE'] - df1v4['first_def_date']) / np.timedelta64(1, 'm'))

# %%


#create a default year column based on first default date 

df1v4['default_year'] = df1v4.first_def_date.dt.year

#create a default flag column populated with zeros

df1v4['default_flag'] = 0

#for any account with default date before statement date and default date difference more than number of cutoff months
#set the default flag column to 1

df1v4.loc[(df1v4['def_date_diff'] <=0) & (df1v4['def_date_diff'] >= -default_month_CUTOFF),'default_flag'] = 1

# %%


#create a second default flag column populated with zeros

df1v4['default_flag2'] = 0

#for any account with the first default flag set to 1 and CRR in 6,7,8,9,10 set this default flag to 1 

df1v4.loc[(df1v4['default_flag'] == 1) | (df1v4['mcrr3'].isin(['6','7','8','9','10'])),'default_flag2'] = 1


#create another version with 7 or worse
df1v4['default_flag3'] = 0
df1v4.loc[(df1v4['default_flag'] == 1) | (df1v4['mcrr3'].isin(['7','8','9','10'])),'default_flag3'] = 1
#create another version with 8 or worse
df1v4['default_flag4'] = 0
df1v4.loc[(df1v4['default_flag'] == 1) | (df1v4['mcrr3'].isin(['8','9','10'])),'default_flag4'] = 1




# %%


#creating a list of the columns in the filtered dataframe

df1v4_cols_old = ['CIF_CRM','STATEMENTDATE','STATEMENTID','crr_gross', 'first_def_date', 'mcrr', 'mcrr_date', 'mcrr3',
       'mcrr3_date', 'mcrr6', 'mcrr6_date', 'rbs_stmtdate', 'mdate_firstCF',
       'rbs_firstCF', 'rbs_last', 'crr_last', 'mdate_last', 'rbs_first',
       'crr_first', 'mdate_first', 'default_year', 'default_flag', 'default_flag2']

#resetting df1v4_cols to avoid duplication with columns already in df1

df1v4_cols = ['CIF_CRM', 'STATEMENTDATE','STATEMENTID',
       'mcrr_stmtdate', 'rbs_stmtdate', 'mdate_firstCF', 'rbs_firstCF',
       'rbs_last', 'crr_last', 'mdate_last', 'rbs_first', 'crr_first',
       'mdate_first','default_year', 'default_flag', 'default_flag2','default_flag3','default_flag4']

# %%


#apply inner join so that only the CF02 filtered borrowers remain in the dataset
df1v5 = df1.merge(df1v4[df1v4_cols], how='inner',left_on=['CIF_CRM','STATEMENTDATE','STATEMENTID'],
               right_on=['CIF_CRM','STATEMENTDATE','STATEMENTID'])

del df1v4
del df1
gc.collect()

# %%
# ### Applying level2 filters which includes filtering for target currency and netsales levels

#create filter for target currency as USD
mask4 = (df1v5['TARGETCURRENCY'] == 'USD')

#create filter for netsales number over $1 million

mask5 = (df1v5['NETSALES'] > 1000)

#create filter for total asset number over $1 million
mask6 = (df1v5['TOTALASSETS'] > 1000)

# %%


# filter out data based on target currency, netsales and total assets

df1v5 = df1v5[mask4 & mask5 & mask6].copy()

# %%
#These filters will:
#1. include all of CF - SLBO
#2. and all others with revenue greater than $75mm
mask1 = (df1v5['rbs_stmtdate'].isin(['TCSB']))
mask2 = (df1v5['NETSALES'] > 75000)

#filtering out all CF-SLBO and net sales above 75 million for non SLBO clients

df1v6 = df1v5[(mask1 & (df1v5['NETSALES'] > 0)) | (~mask1 & mask2)].copy()

del df1v5
gc.collect()

# %%


mask1 = (df1v6.crr_gross.isna())
mask2 = (df1v6.mcrr3.isna())
mask3 = (df1v6.rbs_stmtdate.isna())

# %%


#apply filters such that only those records are retained which have CRR and RBS

df1v7 = df1v6[~mask1 & ~mask2 & ~mask3].copy()

del df1v6
gc.collect()

# %%


#create mask for removing RBS that will not be used in this analysis 

mask_rbs = (df1v7['rbs_stmtdate'].isin(['ESID','MSID',
            'PB', 'PW', 'GFB','ONT']))


# ### Applying mask to create file with insignificant RBS removed  

# %%


df1v8 = df1v7[~mask_rbs].copy()

del df1v7
gc.collect()

# %%


#identify accounts in Balance Sheet Dependent and ID Later Stage

mask1 = df1v8['rbs_stmtdate'].isin(['TBSD','OID'])

#identify accounts in Cash Flow Other and SlBO


mask2 = df1v8['rbs_stmtdate'].isin(['TCFO', 'TCSB'])

#create categorical variable to identify them

df1v8.loc[mask1,'rbs_group'] = 'BS/ID'
df1v8.loc[mask2,'rbs_group'] = 'CF'

# %%

# # CF12b Binning of Financial Variables 

# ### Create a dictionary of relevant variables  

vardict = {'SCALE':['NETSALES'],
            'PROFITABILITY':['GROSSMARGIN'],
            'LEVERAGE':['TDEBITDA'],
            'LIQUIDITY':['CURRENTRATIO'],
            'COVERAGE':['FIXEDCHARGECOVER'],
            
          }




# %%
# ### Create a list of variables to subsetted from the master file  

cols2 = ['CIF_CRM','CUSTOMERNAME','STATEMENTYEAR','STATEMENTDATE','AUDITMETHOD','STATEMENTTYPE',
        'rbs_stmtdate','rbs_group', 'mcrr','mcrr3', 
        'default_flag','default_flag2','default_flag3','default_flag4',
        ] + vardict['SCALE'] + vardict['PROFITABILITY'] + vardict['LEVERAGE'] + \
        vardict['LIQUIDITY'] + vardict['COVERAGE'] 

# %%


#extract a subset of df1v8 with the relevant variables 

df1v9 = df1v8[cols2]

del df1v8
gc.collect()

# %%


#function bin_variable - bins uniformly to a set # of bins

def bin_variable(df_,var_,nbins_=4,precision_=4, frac_=1):
    dffdev = df_[[var] + ['default_flag3','CIF_CRM','STATEMENTDATE','rbs_group']].copy()
    dffdev[var + '_bin'] = pd.qcut(dffdev[var], q=nbins_, duplicates='drop',precision=precision_)
    
    x1 = dffdev.groupby(by = var + '_bin').agg({'CIF_CRM':'count','default_flag3':'sum'})
    x1 = x1.assign(dr = x1['default_flag3'] / x1['CIF_CRM'])
    x1 = x1.reset_index()
    x1.rename(columns={'CIF_CRM':'Total','default_flag3':'bads'},inplace=True)
    
    x1 = x1.assign(goods = x1['Total'] - x1['bads'])
    x1['good_pct'] = x1['goods'] / x1['goods'].sum()
    x1['bad_pct'] = x1['bads'] / x1['bads'].sum()
    x1[var + '_mid'] = x1[var + '_bin'].apply(lambda x: x.mid)
    
    y = lowess(endog=x1['dr'], exog=x1[var + '_mid'], frac =frac_)
    x1['dr_lowess'] = y[:,1]
    
    return x1

#function bin_variable2 - bins to a set percentile distribution. Can be uniform or custom based on input qtiles_

def bin_variable2(df_,var_,qtiles_=[0,0.25,0.50,0.75,1],precision_=4,frac_=1):
    dffdev = df_[[var] + ['default_flag3','CIF_CRM','STATEMENTDATE','rbs_group']].copy()
    dffdev[var + '_bin'] = pd.qcut(dffdev[var], q=qtiles_, duplicates='drop',precision=precision_)
    
    x1 = dffdev.groupby(by = var + '_bin').agg({'CIF_CRM':'count','default_flag3':'sum'})
    x1 = x1.assign(dr = x1['default_flag3'] / x1['CIF_CRM'])
    x1 = x1.reset_index()
    x1.rename(columns={'CIF_CRM':'Total','default_flag3':'bads'},inplace=True)
    
    x1 = x1.assign(goods = x1['Total'] - x1['bads'])
    x1['good_pct'] = x1['goods'] / x1['goods'].sum()
    x1['bad_pct'] = x1['bads'] / x1['bads'].sum()
    x1[var + '_mid'] = x1[var + '_bin'].apply(lambda x: x.mid)
    
    y = lowess(endog=x1['dr'], exog=x1[var + '_mid'], frac =frac_)
    x1['dr_lowess'] = y[:,1]
    
    return x1

# %%


#this function returns the lowess transformed dr by matching a financial metric to its corresponding bin
#x is self, the dataset which has the var_ column
#dfbin_ is the dataset with binned values
def lookup_lowess(x,dfbin_,var_,):
    for i in range(dfbin_.shape[0]):                #iterate through each row
        if x in dfbin_.loc[i,var_ + '_bin']:        #find a match in a bib
            #return x1.loc[i,'GROSSMARGIN_bin']
            return dfbin_.loc[i,'dr_lowess']        #return corresponding transformed dr




# %%
# ### Binning of Leverage Ratios

# #### Total Debt to EBITDA
# 

var = 'TDEBITDA'
mask1 = (df1v9[var] == 0)
mask2 = (df1v9[var].isin([np.inf,-np.inf]))
mask3 = (df1v9[var].isna()) | (df1v9[var].isnull())

# %%


binned = bin_variable2(df_=df1v9[~mask1 & ~mask2 & ~mask3], var_=var,qtiles_=[0,0.50,0.65,0.75,0.85,1],frac_=0.8)
binned['varname'] = var
max_ldr = binned.dr_lowess.max()
binned = binned.assign(score = lambda x: round(100*x['dr_lowess'] / max_ldr,0))

# %%


binned[var+'_mid2'] = binned[var+'_mid'].map('{:,.1f}'.format)
#ax = binned.plot.line(x=var + '_mid2', y = ['dr','dr_lowess'], rot=0)

#plt.show()

# %%


df1v9[var+ '_ldr'] = df1v9[var].apply(lookup_lowess,dfbin_=binned, var_=var)




# %%
# ###  Construct modified TDEBITDA_mod accounting for the replacement of 0s
# ##### step1: observe the default rate of the 0 only sample
# ##### step2: compare this to the distribution of the overall non-missing/non-zero dataset
# ##### step3: replace the 0s with the percentile corresponding to the bin with the observed default rate

var1 = 'TDEBITDA'
mask1 = (df1v9[var1] == 0)
#df1v9[mask1].default_flag2.value_counts(dropna=False,normalize=True)

# %%


df1v9['TDEBITDA_mod'] = df1v9['TDEBITDA']

# %%


#looking at the bin chart above, the 0.05 dr falls in the last bucket. 90th percentile is a resonable adjustment
df1v9[~mask1].TDEBITDA.quantile(0.90)

# %%


df1v9.loc[mask1,'TDEBITDA_mod'] = df1v9[~mask1].TDEBITDA.quantile(0.90)

# %%


var = 'TDEBITDA_mod'
mask1 = (df1v9[var] == 0)
mask2 = (df1v9[var].isin([np.inf,-np.inf]))
mask3 = (df1v9[var].isna()) | (df1v9[var].isnull())

# %%


binned = bin_variable(df_=df1v9[~mask2], var_=var,nbins_=7,frac_=0.8)

binned['varname'] = var
max_ldr = binned.dr_lowess.max()
binned = binned.assign(score = lambda x: round(100*x['dr_lowess'] / max_ldr,0))

# %%


#create empty bin table
finbin = binned.filter(items=[0,1],axis=0)
finbin.rename(columns={'LIABSTOASSETS_bin':'var_bin','LIABSTOASSETS_mid':'var_mid' },inplace=True)
finbin['varname'] = 'dummy'

# %%


#Add to the binning dataframe
finbin = pd.concat([finbin,
                    binned.rename(columns={var + '_bin':'var_bin', var + '_mid':'var_mid' })]
                  )
binned[var+'_mid2'] = binned[var+'_mid'].map('{:,.1f}'.format)
#ax = binned.plot.line(x=var + '_mid2', y = ['dr','dr_lowess'], rot=0)
#ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#plt.show()

# %%


#Add transformed variables to the raw dataframe
df1v9[var+ '_ldr'] = df1v9[var].apply(lookup_lowess,dfbin_=binned, var_=var)




# %%
# 
# ## Binning of Coverage Ratios

# ### Fixed Charge Coverage 

var = 'FIXEDCHARGECOVER'
mask1 = (df1v9[var] == 0)
mask2 = (df1v9[var].isin([np.inf,-np.inf]))
mask3 = (df1v9[var].isna()) | (df1v9[var].isnull())
mask4 = (df1v9[var] < 0)

# %%


binned = bin_variable2(df_=df1v9[~mask1], var_=var,qtiles_=[0,0.50,0.655,0.80,1],frac_=0.95)
binned['varname'] = var
max_ldr = binned.dr_lowess.max()
binned = binned.assign(score = lambda x: round(100*x['dr_lowess'] / max_ldr,0))

# %%


###Add to the binning dataframe
finbin = pd.concat([finbin,
                    binned.rename(columns={var + '_bin':'var_bin', var + '_mid':'var_mid' })]
                  )
binned[var+'_mid2'] = binned[var+'_mid'].map('{:,.1f}'.format)
#ax = binned.plot.line(x=var + '_mid2', y = ['dr','dr_lowess'], rot=0)
#ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#plt.show()

# %%


#Add transformed variables to the raw dataframe
df1v9[var+ '_ldr'] = df1v9[var].apply(lookup_lowess,dfbin_=binned, var_=var)




# %%
# 
# ## Binning of Profitability Ratios
# 

# ### Gross Margin 

var = 'GROSSMARGIN'
mask1 = (df1v9[var] == 0)
mask2 = (df1v9[var].isin([np.inf,-np.inf]))
mask3 = (df1v9[var].isna()) | (df1v9[var].isnull())
mask4 = (df1v9[var] < 0)

# %%


binned = bin_variable(df_=df1v9[~mask2], var_=var,nbins_=7,frac_=1)

binned['varname'] = var
max_ldr = binned.dr_lowess.max()
binned = binned.assign(score = lambda x: round(100*x['dr_lowess'] / max_ldr,0))

# %%


###Add to the binning dataframe
finbin = pd.concat([finbin,
                    binned.rename(columns={var + '_bin':'var_bin', var + '_mid':'var_mid' })]
                  )
binned[var+'_mid2'] = binned[var+'_mid'].map('{:,.1f}'.format)
#ax = binned.plot.line(x=var + '_mid2', y = ['dr','dr_lowess'], rot=0)
#ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#plt.show()

# %%


###Add transformed variables to the raw dataframe
df1v9[var+ '_ldr'] = df1v9[var].apply(lookup_lowess,dfbin_=binned, var_=var)




# %%
# 
# 
# ### Binning of Liquidity Ratios
# 

# ### Current Ratio

var = 'CURRENTRATIO'
mask1 = (df1v9[var] == 0)
mask2 = (df1v9[var].isin([np.inf,-np.inf]))
mask3 = (df1v9[var].isna()) | (df1v9[var].isnull())
mask4 = (df1v9[var] < 0)

# %%


#binned = bin_variable(df_=df1v9[~mask4], var_=var,nbins_=7,frac_=0.75)
binned = bin_variable2(df_=df1v9[~mask2], var_=var,qtiles_=[0,0.15,0.30,0.45,0.75,1],frac_=0.7)
binned['varname'] = var
max_ldr = binned.dr_lowess.max()
binned = binned.assign(score = lambda x: round(100*x['dr_lowess'] / max_ldr,0))

# %%


###Add to the binning dataframe
finbin = pd.concat([finbin,
                    binned.rename(columns={var + '_bin':'var_bin', var + '_mid':'var_mid' })]
                  )
binned[var+'_mid2'] = binned[var+'_mid'].map('{:,.1f}'.format)
#ax = binned.plot.line(x=var + '_mid2', y = ['dr','dr_lowess'], rot=0)
#ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#plt.show()

# %%


###Add transformed variables to the raw dataframe
df1v9[var+ '_ldr'] = df1v9[var].apply(lookup_lowess,dfbin_=binned, var_=var)




# %%
# 
# ## Binning of Scale Variables
# 

# ### Net Sales 

var = 'NETSALES'
mask1 = (df1v9[var] == 0)
mask2 = (df1v9[var].isin([np.inf,-np.inf]))
mask3 = (df1v9[var].isna()) | (df1v9[var].isnull())
mask4 = (df1v9[var] < 0)

# %%


binned = bin_variable2(df_=df1v9[~mask2], var_=var,qtiles_=[0,0.4,0.7,1],frac_=1)
binned['varname'] = var
max_ldr = binned.dr_lowess.max()
binned = binned.assign(score = lambda x: round(100*x['dr_lowess'] / max_ldr,0))

# %%


###Add to the binning dataframe
finbin = pd.concat([finbin,
                    binned.rename(columns={var + '_bin':'var_bin', var + '_mid':'var_mid' })]
                  )
binned[var+'_mid2'] = binned[var+'_mid'].map('{:,.1f}'.format)
#ax = binned.plot.line(x=var + '_mid2', y = ['dr','dr_lowess'], rot=0)
#ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#plt.show()

# %%


###Add transformed variables to the raw dataframe
df1v9[var+ '_ldr'] = df1v9[var].apply(lookup_lowess,dfbin_=binned, var_=var)

# %% [markdown]
# #### The development dataset used to train the dev model and used as KPI benchmark is pulled from a separate stored pickle file 

# %%
#this is the saved Development dataset with all of the binning and transformation already implemented. 

dev_dataset = pd.read_pickle('CF12b_df1v9_0120.pkl')


# %%
#save list of CIFs from the scoring dataset

cif_list_large_df = pd.read_csv('cif_list_large_df.csv')
cif_list_large_df['0'] = cif_list_large_df['0'].astype(str)
cif_list_large = list(cif_list_large_df['0'])

df1v9 = df1v9.loc[df1v9.CIF_CRM.isin(cif_list_large)]

# %%


pd.options.display.float_format = '{:,.2f}'.format
GLOBAL_SEED = 888





# %%
#subset testing data from development dataset to follow the model development procedure


df1v9_dev = dev_dataset.loc[dev_dataset['STATEMENTYEAR'] < 2021,:].copy()

# %%


#selection of top3 in each category
vardict3 = {'SCALE':['NETSALES_ldr'],
            'PROFITABILITY':['GROSSMARGIN_ldr'],
            'LEVERAGE':['TDEBITDA_mod_ldr'],
            'LIQUIDITY':['CURRENTRATIO_ldr'],
            'COVERAGE':['FIXEDCHARGECOVER_ldr']
          }




# %%
# ### Filter Model

x = [['NETSALES_ldr', 'GROSSMARGIN_ldr', 'TDEBITDA_mod_ldr', 'CURRENTRATIO_ldr', 'FIXEDCHARGECOVER_ldr']]

# %%


df1v9_dev.rename(columns={'default_flag3':'target'},inplace=True)
num_cols1 = x[0]
cat_cols1 = ['rbs_group']
df1m1 = pd.get_dummies(df1v9_dev, columns=cat_cols1)

def is_CF(CF_flag):
    if CF_flag == 1:
        return 'CF'
    else:
        return 'BS/ID'
    
df1m1['rbs_group'] = df1m1['rbs_group_CF'].apply(is_CF)

    #drop extraneous dummies
#df1m1.drop([ 'rbs_group_nan'],axis=1,inplace=True)


# %%
# ### Fit Model

#Generate Numpy Arrays for SKLEARN

##below two lines are for transforming using StandardScaler which is not used in this version
###scaler = StandardScaler()
###scaler.fit(df_train[numeric_cols])

#get_features_and_target_arrays2 - returns X with categorical variables included
#get_features_and_target_arrays3 - returns X with only numeric variables

def get_features_and_target_arrays2(df, numeric_cols,cat_cols):
    #X_numeric_scaled = scaler.transform(df[numeric_cols])
    X_numeric_scaled = df[numeric_cols].to_numpy()
    X_categorical = df[cat_cols].to_numpy()
    X = np.hstack((X_categorical, X_numeric_scaled))
    #X = X_numeric_scaled
    y = df['target']
    return X, y

def get_features_and_target_arrays3(df, numeric_cols):
    #X_numeric_scaled = scaler.transform(df[numeric_cols])
    X_numeric_scaled = df[numeric_cols].to_numpy()
    #X_categorical = df[cat_cols].to_numpy()
    #X = np.hstack((X_categorical, X_numeric_scaled))
    X = X_numeric_scaled
    y = df['target']
    return X, y

# %%


numeric_cols = num_cols1

cat_cols = ['rbs_group_BS/ID']
cat_cols.sort()


# %%


random_seed = 888
df_train, df_test = train_test_split(df1m1, test_size=0.2, random_state=random_seed, stratify=df1m1['target'])

info_cols = ['CIF_CRM','CUSTOMERNAME', 'STATEMENTYEAR', 'STATEMENTDATE','mcrr3']

df_train = df_train[info_cols + ['target'] + numeric_cols ]
df_test = df_test[info_cols + ['target'] + numeric_cols ]

#remove nas
df_train.dropna(axis=0,inplace=True)
df_test.dropna(axis=0,inplace=True)

# %%
print(len(df_train), len(df_test))

# %%


X, y = get_features_and_target_arrays3(df_train, numeric_cols)
X_test, y_test = get_features_and_target_arrays3(df_test, numeric_cols)


# ### Fit Logistic using Sklearn

# %%

#Step 4
#change to None
clf = LogisticRegression(penalty=None) # logistic regression with no penalty term in the cost function.
clf.fit(X, y)

# %%


coefficients_large = np.hstack((clf.intercept_, clf.coef_[0]))
dfm1 = pd.DataFrame(data={'variable': ['intercept'] + numeric_cols, 'coefficient': coefficients_large})
#compute range for each variable

"""
dfrange = pd.DataFrame(columns = ["variable",'Range'])
for var in numeric_cols:
    df111 = pd.DataFrame({'variable':var, 'Range':df_train[var].max() - df_train[var].min()})
    #dfrange = pd.concat([dfrange, df111])
#dfm1 = dfm1.merge(dfrange, on='variable')
#compute weights
#dfm1 = dfm1.assign(coeftimesrange = dfm1.coefficient*dfm1.Range)
#dfm1['weight'] = 100 * dfm1['coeftimesrange'] / dfm1.coeftimesrange.sum()


"""

# %%
dfm1

# %%
#function for calculating population stability index 


# PSI = Sum((Actual - Expected)*log(%Actual/%Expected))


def psi(actual_data, expected_data, num_bins = 10):
    
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
#bootstrap function to resample for calculating coefficients


def bootstrap_logistic_regression(Z, num_iterations):
    
#     random_seed=72
#     np.random.seed(random_seed)
    
    coefficient_estimates = pd.DataFrame()

    for _ in range(num_iterations):
        
        
        
        # Create a bootstrap sample by resampling with replacement
        bootstrap_sample = resample(Z, replace=True, random_state=_)

        # Fit a logistic regression model to the bootstrap sample
        X_boot, y_boot = get_features_and_target_arrays3(bootstrap_sample, numeric_cols)
        clf1 = LogisticRegression(penalty=None)
        clf1.fit(X_boot, y_boot)
        coefficient_mon = np.hstack((clf1.intercept_, clf1.coef_[0]))
        coeff = pd.DataFrame(data={'variable': ['intercept'] + numeric_cols, 'coefficient': coefficient_mon})
        

        coefficient_estimates = pd.concat([coefficient_estimates, coeff], axis=0)

    return coefficient_estimates

# %%
### KPI 2,3, 4, 5, 6, 7: Gini, KS, Pop Stability and Coeff Stability   

large_corp_kpi = []


coeff_stab_list = []
psi_input_large = []

cif_list = df1v9.CIF_CRM.unique()
    

ar_data_large = df1v9.copy()

    
ar_data_large.rename(columns={'default_flag3':'target'},inplace=True)
ar_data1 = pd.get_dummies(ar_data_large, columns=cat_cols1)
    
#ar_data1['rbs_group'] = ar_data1['rbs_group_CF'].apply(is_CF)
    
#drop extraneous dummies
    
ar_data1 = ar_data1[info_cols + ['target'] + numeric_cols ]
    
    #remove nas
    
ar_data1.dropna(axis=0,inplace=True)

ar_data2 = ar_data1.copy()

    #get predictive variables and target variable 

X_perf, y_perf = get_features_and_target_arrays3(ar_data2, numeric_cols)
    
#Use the model trained on development dataset to calculate predicted defaults from combined dataset 

y_perf_proba = clf.predict_proba(X_perf)[:, 1]
    
#calculate the AUC for the combined dataset

auc_perf = roc_auc_score(y_perf, y_perf_proba)


    
    

## Gini Statistic

#Using the calculated AUC to determine the Gini statistic 

gini_large = 2*auc_perf - 1 
    

#determining false positive, true positive and thresholds for calculating KS test 
fpr, tpr, thresholds = roc_curve(y_perf, y_perf_proba)

## Kolmogorov Smirnov Test

ks_large = max(tpr - fpr)


y_bench_proba = clf.predict_proba(X)[:,1]   




    

for features in numeric_cols:
    df_Mon = ar_data1[features].tolist()
    df_Dev = df_train[features].tolist()
    psi_input2 = psi(df_Mon, df_Dev)
    
    psi_input_large.append(psi_input2)

large_corp_kpi.append(psi_input_large)

#joining monitoring dataset to development dataset and re-estimating coefficients

Dev_and_Mon_combined = pd.concat([ar_data1, df_train])
    
num_iterations = 1000  # Number of bootstrap iterations
coefficient_estimates = bootstrap_logistic_regression(Dev_and_Mon_combined, num_iterations) 

summary_df = pd.DataFrame()
    
    
for features in numeric_cols:
    
    mean_coefficients = np.mean(coefficient_estimates[coefficient_estimates['variable']==features]['coefficient'], axis=0)
    std_coefficients = np.std(coefficient_estimates[coefficient_estimates['variable']==features]['coefficient'], axis=0)
    data = coefficient_estimates[coefficient_estimates['variable']==features][['coefficient']]
    sem1 = stats.sem(data)
    sem2 = np.std(data) / np.sqrt(len(data))
    summary=pd.DataFrame({'variable':[features],'mean_coefficients':[mean_coefficients],'std_coefficients':[std_coefficients]})
    summary=summary.reset_index() 
    summary_df= pd.concat([summary_df, summary])

summary_orig_model = dfm1[['variable', 'coefficient']]

summary_df = summary_df.merge(summary_orig_model, left_on = 'variable', right_on = 'variable')
summary_df['Diff'] = (summary_df['coefficient'] - summary_df['mean_coefficients'])/summary_df['coefficient']
print(summary_df)

coeff_stab = np.mean(summary_df['Diff'])
    
coeff_stab_list.append(coeff_stab)   

large_corp_kpi.append(coeff_stab_list)    




    



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

#Step 8
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
# ### Section 2: Early Stage and Mid Size Performance Monitoring

# %%
# ### SQL Query to pull GLV Data for date range 2020 to present. Date range 2020 to 2022 will be used for development data set. Only data from past quarter will be used later to identify clients for performance monitoring metrics
# 

query_glv = """
Select 
a.LOADDT
,a.RISKCD
,a.NOTEDT
,a.MTRTYDT
,a.FACEAMTOFNOTEORGNLBAL
,a.NOTEPRNCPLBALNET
,a.NOTEPRNCPLBALGROSS
,a.FACILITY_TYPE
,a.ACCTNBR
,a.CIF
,b.leveltwo
,a.LIFESTAGE
,a.client_aoteamcd
,a.BUSINESS_UNIT
,a.CUSTINDTYPEDESC
,a.NEXTMTRTYDT
,a.DTOFLASTRENEWAL
,a.NBROFRENEWALSEXT
,a.INTRATEGRNTCD
,a.PAYMENT_TYPE_CD


from CRDADMPRD.dbo.GLV_Historical_DW_Gross_Loans_Adjusted a 
left join CRDADMCLM.dbo.STG_RBStoAllCIFMapping b
on a.CIF = b.cif AND cast(a.LOADDT as date)= cast(b.period as date)
where a.status_cd='A'
AND a.LOADDT > '{month_end_24m_prior}'
""".format(month_end_24m_prior=month_end_24m_prior)




# %%
# ### Extract Data using connection to credit database

df_glv_full = pd.read_sql_query(query_glv, conn)

df_glv = df_glv_full.copy()


# ### Create Imputations where Lifestage Data is Missing



# %%
# ### Fill value 'missing' for any NA Lifestage values

df_glv["LIFESTAGE"] = df_glv["LIFESTAGE"].fillna("missing")
df_glv["LIFESTAGE"] = df_glv["LIFESTAGE"].replace("", "missing")




# %%
# ### Exclude penny loans from data

#change load date to datetime format and create a month field 
df_glv['LOADDT'] = pd.to_datetime(df_glv['LOADDT'])
df_glv['Month_yr'] = df_glv['LOADDT'].dt.to_period('M')

# Rename RBS
df_glv['RBS']=np.where(df_glv['leveltwo'].isna(),"NULL",
                       np.where(df_glv['leveltwo']=='NT- PES & VC', 'NT- GFB',
                                np.where(df_glv['leveltwo']=='ID - Other', 'ID - Later Stage',df_glv['leveltwo'])))

# Penny Loans Exclusion
df_glv['Penny_Loan']=np.where((df_glv['FACEAMTOFNOTEORGNLBAL'] != 0.01) | (df_glv['FACEAMTOFNOTEORGNLBAL'].isnull()),0,1)




# %%
# ### UK CIF exclusion
# 

## Exclude  UK Business Unit:
df_glv_1 = df_glv.copy()
df_glv_1["IS_UK"] = df_glv_1["BUSINESS_UNIT"].isin(["BUK01", "BUK02"])
count_uk = df_glv_1.groupby(["LOADDT","CIF"], as_index=False).agg({"IS_UK":"sum"})
atleast_uk = count_uk[count_uk["IS_UK"]>=1].reset_index(drop=True)
atleast_uk = atleast_uk[["LOADDT", "CIF"]]
atleast_uk["UK_EXCLUDE"] = 1

# %%


del(df_glv)
gc.collect()

df_glv_1 = df_glv_1.merge(atleast_uk, how="left", on = ["LOADDT", "CIF"])
df_glv_1 = df_glv_1[df_glv_1["UK_EXCLUDE"] != 1].reset_index(drop=True)




# %%
# ### FACILITY TYPE Exclusion: Exclude facility types GUD, CMG, BSL, SFT and NULL
# 
# 

df_glv_1["FT_Filter"] = df_glv_1["FACILITY_TYPE"].isin(["","GUD", "CMG", "BSL", "SFT", None]) | pd.isnull(df_glv_1["FACILITY_TYPE"])
ft_count = df_glv_1.groupby(["LOADDT","CIF"], as_index=False).agg({"FT_Filter":"sum", "ACCTNBR":"count"})
ft_count["FT_ONLY"] = (ft_count["FT_Filter"]>0) & (ft_count["FT_Filter"] == ft_count["ACCTNBR"])
ft_count["FT_ONLY"] = ft_count["FT_ONLY"].astype(int)
ft_count = ft_count[["LOADDT", "CIF", "FT_ONLY"]]

# %%


df_glv_1 = df_glv_1.merge(ft_count, how="left", on = ["LOADDT", "CIF"])
df_glv_2 = df_glv_1[df_glv_1["FT_ONLY"] != 1].reset_index(drop=True)

del df_glv_1
gc.collect()




# %%
# ### Excluding CIF with at least one FACILITY TYPE in PFL

df_glv_2["IS_PFL"] = df_glv_2["FACILITY_TYPE"]=="PFL"
has_pfl = df_glv_2.groupby(["LOADDT","CIF"], as_index=False).agg({"IS_PFL":"sum", "ACCTNBR":"count"})
multi_pfl = has_pfl[(has_pfl["IS_PFL"]<has_pfl["ACCTNBR"])&(has_pfl["IS_PFL"]>1)].reset_index(drop=True)
pfl_filter = has_pfl[has_pfl["IS_PFL"]>0][["LOADDT", "CIF"]].reset_index(drop=True)
pfl_filter["EXCLUDE_PFL"] = 1

# %%


df_glv_2 = df_glv_2.merge(pfl_filter, how="left", on = ["LOADDT", "CIF"])
df_glv_2 = df_glv_2[df_glv_2["EXCLUDE_PFL"] != 1].reset_index(drop=True)




# %%
# ### LIFESTAGE IMPUTATION based on nearest proximate lifestage in the last 12 months

df_glv_2a = df_glv_2.copy()

del df_glv_2
gc.collect()

# sort by acctnbr and loaddt
df_glv_2a = df_glv_2a.sort_values(by = ["ACCTNBR", "LOADDT"], ascending = [True, True]).reset_index(drop=True)
# Temporary add index for null row index - adding an extra row and setting it with an index consistent with the dataframe
#Step 9
#add ._append
df_glv_2a = pd.concat([df_glv_2a,pd.Series(None, index=df_glv_2a.columns)], ignore_index=True).reset_index(drop=True)
# Index as a separate column
df_glv_2a["IND"] = df_glv_2a.index
# Get index of non null rows
df_glv_2a["LIFESTAGE_NULL_IND"] = df_glv_2a.apply(lambda x: x["IND"] if x["LIFESTAGE"]!="missing" else None, axis=1)

# %%


# Forward Fill the lifestage index
## i.e., if jan-21 is missing and feb-21 is not missing, we impute with jan-21 index
df_glv_2a["LS_IND"] = df_glv_2a.groupby(["ACCTNBR"], as_index=False).bfill()["LIFESTAGE_NULL_IND"]

# %%


# fill all nan indexes with index number with the temporary added row
df_glv_2a["LS_IND"] = df_glv_2a["LS_IND"].fillna(df_glv_2a.index[-1])
# get loaddt of imputed lifestage
df_glv_2a["LS_IND_LOADDT"] = df_glv_2a["LS_IND"].apply(lambda x: df_glv_2a["LOADDT"][x])
# get lifestage for imputed lifestage 
df_glv_2a["LIFESTAGE_IMPUTE"] = df_glv_2a["LS_IND"].apply(lambda x: df_glv_2a["LIFESTAGE"][x])
# get date difference to see if the difference is within a year (366 days)
df_glv_2a["date_diff"] = df_glv_2a["LS_IND_LOADDT"] - df_glv_2a["LOADDT"]

# %%


# True/False filter to impute the data
## Only impute if Lifestage is missing and the date difference is within 365 days
df_glv_2a["impute_filter"] = (df_glv_2a["LIFESTAGE"] =="missing") & (df_glv_2a["date_diff"].dt.days <= 366)

# %%


# Get Imputed LIFESTAGE columns
df_glv_2a["LIFESTAGE_IMPUTED"] = df_glv_2a.apply(lambda x: x["LIFESTAGE_IMPUTE"] if x["impute_filter"]==True else x["LIFESTAGE"], axis=1)




# %%
# ### Exclude if FACILITY TYPE and LIFESTAGE IN GFB 
# 

df_glv_3 = df_glv_2a.copy()
#del(df_glv_2a)

# %%


df_glv_3["IS_GPCC"] = df_glv_3["FACILITY_TYPE"].isin(["GCC", "PCC"])
df_glv_3["IS_GPCC"] = df_glv_3["IS_GPCC"].astype(int)
has_gpcc = df_glv_3.groupby(["LOADDT","CIF"], as_index=False).agg({"IS_GPCC":"sum", "ACCTNBR":"count"})
multi_gpcc = has_gpcc[(has_gpcc["IS_GPCC"]<has_gpcc["ACCTNBR"])&(has_gpcc["IS_GPCC"]>1)].reset_index(drop=True)
gpcc_filter = has_gpcc[has_gpcc["IS_GPCC"]>0][["LOADDT", "CIF"]].reset_index(drop=True)
gpcc_filter["EXCLUDE_GPCC"] = 1

# %%


df_glv_3 = df_glv_3.merge(gpcc_filter, how="left", on = ["LOADDT", "CIF"])
df_glv_3 = df_glv_3[df_glv_3["EXCLUDE_GPCC"] != 1].reset_index(drop=True)




# %%
# ###  Exclude at least one lifestage in Private Equity and Venture Capital

df_glv_3["IS_LS_PEVC"] = df_glv_3["LIFESTAGE_IMPUTED"].isin(["Private Equity Firm", "Venture Capital Firm", "VC Firm"])
df_glv_3["IS_LS_PEVC"] = df_glv_3["IS_LS_PEVC"].astype(int)
has_pevc = df_glv_3.groupby(["LOADDT","CIF"], as_index=False).agg({"IS_LS_PEVC":"sum", "ACCTNBR":"count"})
pevc_filter = has_pevc[has_pevc["IS_LS_PEVC"]>0][["LOADDT", "CIF"]].reset_index(drop=True)
pevc_filter["EXCLUDE_PEVC"] = 1

# %%


df_glv_3 = df_glv_3.merge(pevc_filter, how="left", on = ["LOADDT", "CIF"])
df_glv_3 = df_glv_3[df_glv_3["EXCLUDE_PEVC"] != 1].reset_index(drop=True)




# %%
# ### Exclude if FACILITY TYPE NOT IN INNOVATION 


def is_innovation(x):
    if pd.isnull(x):
        return "missing"
    elif x == None:
        return "missing"
    elif x == "":
        return "missing"
    elif x == "missing":
        return "missing"
    elif x.upper() == "ET":
        return "Innovation"
    elif "EMERGING TECH" in x.upper():
        return "Innovation"
    elif x.upper() == "EARLY STAGE":
        return "Innovation"
    elif x.upper() == "MID STAGE":
        return "Innovation"
    elif x.upper() == "LATE STAGE":
        return "Innovation"
    elif "CORP TECH" in x.upper():
        return "Innovation"
    elif "LARGE CORP" in x.upper():
        return "Innovation"
    elif x.upper() == "SPONSOR LED BUYOUT":
        return "Innovation"
    else:
        return "NO_INNOVATION"
        


# %%


df_glv_4 = df_glv_3.copy()

# %%


df_glv_4["LIFESTAGE_1"] = df_glv_4["LIFESTAGE_IMPUTED"].map(lambda x: is_innovation(x))
df_glv_4["IS_INNOVATION"] = df_glv_4["LIFESTAGE_1"] == "Innovation"
df_glv_4["IS_MISSING"] = df_glv_4["LIFESTAGE_1"] == "missing"
df_glv_4["IS_NO_INNOVATION"] = df_glv_4["LIFESTAGE_1"] == "NO_INNOVATION"
df_glv_4["IS_INNOVATION"] = df_glv_4["IS_INNOVATION"].astype(int)
df_glv_4["IS_MISSING"] = df_glv_4["IS_MISSING"].astype(int)
df_glv_4["IS_NO_INNOVATION"] = df_glv_4["IS_NO_INNOVATION"].astype(int)
has_innovation = df_glv_4.groupby(["LOADDT","CIF"], as_index=False).agg({"IS_INNOVATION":"sum",
                                                                         "IS_MISSING":"sum",
                                                                         "IS_NO_INNOVATION":"sum","ACCTNBR":"count"})

# %%


def isinov_1(x):
    if x["IS_INNOVATION"] == x["ACCTNBR"]:
        return "INCLUDE"
    elif (x["IS_INNOVATION"]>0) & (x["IS_INNOVATION"]+ x["IS_MISSING"] == x["ACCTNBR"]):
        return "INCLUDE"
    elif (x["IS_INNOVATION"]==0) & (x["IS_MISSING"] == x["ACCTNBR"]):
        return "EXCLUDE"
    else: 
        return "EXCLUDE"

# %%


def isinov_2(x):
    if x["IS_INNOVATION"] == x["ACCTNBR"]:
        return "ALL_INNOVATION"
    elif (x["IS_INNOVATION"]>0) & (x["IS_INNOVATION"]+ x["IS_MISSING"] == x["ACCTNBR"]):
        return "MISSING_AND_INNOVATION"
    elif (x["IS_INNOVATION"]>0) & (x["IS_MISSING"] > 0) & (x["IS_INNOVATION"]+ x["IS_MISSING"] + x["IS_NO_INNOVATION"] == x["ACCTNBR"]):
        return "MISSING_AND_INNOVATION_AND_NOINNOVATION"
    elif (x["IS_INNOVATION"]>0) & (x["IS_MISSING"] == 0) & (x["IS_INNOVATION"]+ x["IS_MISSING"] + x["IS_NO_INNOVATION"] == x["ACCTNBR"]):
        return "INNOVATION_AND_NOINNOVATION"
    elif (x["IS_INNOVATION"]==0) & (x["IS_MISSING"] == x["ACCTNBR"]):
        return "ALL_MISSING"
    elif (x["IS_INNOVATION"]==0) & (x["IS_MISSING"] != 0) & (x["IS_INNOVATION"]+ x["IS_MISSING"] < x["ACCTNBR"]):
        return "INCLUDING_MISSING_NONE_INNOVATION"
    elif (x["IS_INNOVATION"]==0) & (x["IS_MISSING"] == 0):
        return "NONE_INNOVATION"
    else: 
        return "ERROR"

# %%


has_innovation["KEEP"] = has_innovation.apply(lambda x: isinov_1(x), axis=1)
has_innovation["LIFESTAGE_COUNT_TYPE"] = has_innovation.apply(lambda x: isinov_2(x), axis=1)
has_innovation = has_innovation[["LOADDT", "CIF", "KEEP", "LIFESTAGE_COUNT_TYPE"]]

# %%


df_glv_4 = df_glv_4.merge(has_innovation, how="left", on = ["LOADDT", "CIF"])
df_glv_5 = df_glv_4[df_glv_4["KEEP"]=="INCLUDE"].reset_index(drop=True)

# %%


df_glv_5["CRR"] = df_glv_5["RISKCD"].astype(float)
df_glv_5["CRR"] = df_glv_5["CRR"].replace(0,11)




# %%
# ### Get Unique LIFESTAGE
# 

df_glv_6 = df_glv_5.copy()
lifestg = df_glv_6["LIFESTAGE_IMPUTED"].unique()




# %%
# ### Group the LIFESTAGES into various DRR SEGMENTS
# The DRR Segments are: 
#     1. Missing (IMPUTE?)
#     2. Not Tech & LS (NOT MODEL)
#     3. Innovation <15M
#     4. Innovation between 15M AND 75m
#     5. Large Corporate

def group_lifestg(x):
    if pd.isnull(x):
        return "missing"
    elif x == "":
        return "missing"
    elif x == "missing":
        return "missing"
    elif x.upper() == "ET":
        return "Innovation_15M"
    elif "EMERGING TECH" in x.upper():
        return "Innovation_15M"
    elif x.upper() == "EARLY STAGE":
        return "Innovation_15M"
    elif x.upper() == "MID STAGE":
        return "Innovation_15M"
    elif x.upper() == "LATE STAGE":
        return "Innovation_btw_15M_75M"
    elif "CORP TECH" in x.upper():
        return "Innovation_btw_15M_75M"
    elif "LARGE CORP" in x.upper():
        return "Large_Corporate"
    elif x.upper() == "SPONSOR LED BUYOUT":
        return "Large_Corporate"
    else:
        return "Not_Tech_LS"
        


# %%


df_glv_6["LIFESTAGE_GROUP"] = df_glv_6["LIFESTAGE_IMPUTED"].apply(lambda x: group_lifestg(x))




# %%
# ### Rank the LIFESTAGE GROUPS:
# Rankings are given: 
#     1. Large Corporate : 1
#     2. Innovation between 15 and 75: 2
#     3. Innovation less than 15: 3
#     4. Non Tech and Life Sciences: 4
#     5. Missing: 5

lifestg_group_rank = {
    "Large_Corporate":1,
    "Innovation_btw_15M_75M":2,
    "Innovation_15M":3,
    "Not_Tech_LS":4,
    "missing":5
}




# %%
# ### Map rankings to lifestage group

df_glv_6["LIFESTAGE_RANKING"] = df_glv_6["LIFESTAGE_GROUP"].map(lifestg_group_rank)




# %%
# ### SELECT UNIQUE LIFESTAGE BY LOADDT AND CIF
# 

df_glv_6 = df_glv_6.sort_values(by = ["CIF", "LOADDT", "LIFESTAGE_RANKING"], ascending = [True, True, True]).reset_index(drop=True)

# %%


df_glv_6['ls_group_rank'] = df_glv_6.groupby(['CIF','LOADDT'])['LIFESTAGE_RANKING'].rank('first')
mask_ls = (df_glv_6['ls_group_rank'] == 1)
df_ls = df_glv_6[mask_ls]




# %%
# ### CRR Join for the best CRR in group

crr_glv = df_glv_5.groupby(["LOADDT", "CIF"], as_index = False).agg({"CRR":["max", "min"],
                                                                     "NOTEPRNCPLBALNET":["sum"]})
crr_glv.columns = ["LOADDT", "CIF", "WORST_CRR", "BEST_CRR","NOTEPRNCPLBALNET"]

# %%


#GL Data and list of subset CIFs

df_lss = df_ls.merge(crr_glv,how="left", on = ["LOADDT", "CIF"])




# %%
# # Importing Financial Data and Rank Ordering 

qry_fin = """select eomonth(cast(z.statementdate as date)) as loaddt,
    z.CIF_CRM,
    
   
    Z.TARGETCURRENCY,
    Z.STATEMENTTYPE,
    Z.AUDITMETHOD,
    Z.ANALYST,
    Z.STATEMENTDATE,
    Z.STATEMENTID,
    Z.NETSALES,
    Z.FUNDEDDEBT,
    Z.EBITDANC,
    Z.GROSSPROFIT,
    Z.NETPROFIT,
    z.TOTALLIABS,
    z.CASHANDEQUIVS,
    z.TOTALASSETS
   
    
from
    CRDADMPRD.dbo.CDM_CLIENT_FINANCIALS_VW z
 
where
    
    z.statementmonths=12
    AND TARGETCURRENCY = 'USD'
    AND STATEMENTTYPE != 'projection'
    
    AND (ISNULL(CIF_CRM,'') NOT LIKE '%UNKN%') 
    AND (ISNULL(CIF_CRM,'') != '')
    and statementdate > '{month_end_24m_prior}'
    
""".format(month_end_24m_prior=month_end_24m_prior)

# %%


financials = pd.read_sql_query(qry_fin, conn)




# %%
# ### Rank Financials Statements based on statement frequency and audit method

# ### Create ranks based on auditmethod, statementtype and analyst to select best statement in case of duplicates

# (1) - Rank the statement types
stmt_rnk = {"Annual":1,"Rolling Stmt":2,"FY-To-Date":3,"Quarterly":4,"Monthly":5,"placeholder": 5}


# (2) - Rank the auditmethod
audit_rnk = {"Unqualif'd":1,"Qualified":2,"Reviewed":3,"Compiled":4,"Co.Prep'd":5,"Svb Prep":6,"Tax Return":7,"placeholder": 7}


# (3) Rank analysts (accenture=2, else 1)
#set analyst_rank based on first three characters

def map_analyst(x):
    if x == 'ACS':
        map_analyst = 2
    else:
        map_analyst = 1
    return map_analyst
financials['audit_rank'] = financials['AUDITMETHOD'].map(audit_rnk)
financials['statement_rank'] = financials['STATEMENTTYPE'].map(stmt_rnk)


financials['ANALYST'].fillna('placeholder', inplace=True)
financials['analyst_rank'] = financials['ANALYST'].apply(map_analyst)
# analyst ACS can also be in the middle of the analyst name
# use slicing to modify the rank of those indices whose analyst name have -ACS- in the middle
financials.loc[financials['ANALYST'].str.contains("-ACS-"), 'analyst_rank'] = 2

# %%


# (4) Create a sum of all ranks.
financials = financials.assign(rank_sum = lambda x: x['audit_rank'] + x['statement_rank'] + x['analyst_rank'])

# sort the data by ranks so that the first rank can be picked
# preference is to pick by best audit quality, then best statement type and then svb analyst
financials.sort_values(by=['CIF_CRM','STATEMENTDATE',
                'audit_rank','statement_rank','analyst_rank','STATEMENTID','rank_sum'],
                ascending=[True,True,True,True,True,False,True], inplace=True)
financials = financials.reset_index(drop=True)

# since data is sorted in the desired order of importance, create an overall rank column for each group such that
## the first entry gets rank 1
financials['overall_rank'] = financials.groupby(['CIF_CRM','STATEMENTDATE'])['rank_sum'].rank('first')
financials_ranked=financials[financials['overall_rank']==1]




# %%
# ### GL Data Prep for DRR Analysis

## Read GLV data - DRR Group
df = df_lss.copy()
df=df[df['LOADDT']>='2007-07-31']
## Read Financials data - filtered and ranked
finn = financials_ranked.copy()




# %%
# ### Query to extract data for Sponsor Finance Clients  

qry_sponsor = """SELECT a.cif, max(a.client_aoteamcd) as spteam_code, a.loaddt
            FROM CRDADMPRD..GLV_Historical_DW_Gross_Loans_Adjusted AS a
            WHERE
            a.facility_type != 'GUD'
            AND
            a.loaddt >= '{month_end_24m_prior}' 
            GROUP BY a.cif, a.loaddt
            having max(a.client_aoteamcd) in ('38B','38C','58A','58B','58C','86A','86B','86C','86D','86E','90E')
            """.format(month_end_24m_prior=month_end_24m_prior)
df_sponsor_data = pd.read_sql_query(qry_sponsor, conn2)
df_sponsor_data.loaddt = pd.to_datetime(df_sponsor_data.loaddt)

# %%


finn['loaddt'] = pd.to_datetime(finn['loaddt'])


finn['Month_yr'] = finn['loaddt'].dt.to_period('M')
df_sponsor_data['Month_yr'] = df_sponsor_data['loaddt'].dt.to_period('M')

finn_key_vars=['CIF_CRM','STATEMENTDATE','STATEMENTID','Month_yr','NETSALES','rank_sum']
lookback_window = -18

# %%


def drr_segmentation(x,y):
    
    dfl = df[df["Month_yr"] == x].reset_index(drop=True)  
    df_finn = finn[(finn['Month_yr'] > y) & (finn['Month_yr'] <= x)][finn_key_vars]
    
    df_finn = df_finn.sort_values(by = ["CIF_CRM", "STATEMENTDATE"], ascending = [True, False]).reset_index(drop=True)
    df_finn["choose_last"] = df_finn.groupby(['CIF_CRM'])['rank_sum'].rank("first")
    mask2 = (df_finn['choose_last'] == 1)
    df_finn = df_finn[mask2].copy().reset_index(drop=True)
    
    df_merged = dfl.merge(df_finn, how="left", left_on='CIF',right_on='CIF_CRM',suffixes=('_glv', '_fin'))
    df_merged.rename(columns={"CIF": "CIF_glv"}, inplace = True)
   
    
    df_innovation = df_merged[~df_merged["LIFESTAGE_GROUP"].isin([ "missing"])].reset_index(drop=True)
    df_innovation_fin = df_innovation[df_innovation["CIF_CRM"].notnull()].reset_index(drop=True)
    df_innovation_nofin = df_innovation[df_innovation["CIF_CRM"].isnull()].reset_index(drop=True)
    
    df_innovation_75m_above = df_innovation_fin[df_innovation_fin["NETSALES"]>75000].reset_index(drop=True)
    df_innovation_75m_below = df_innovation_fin[df_innovation_fin["NETSALES"]<=75000].reset_index(drop=True)
    
    df_sponsor = df_sponsor_data[df_sponsor_data['Month_yr']==x]
    sponsor_cif = df_sponsor['cif'].unique()
    mask_sponsor_75 = (df_innovation_75m_below["LIFESTAGE"] == "Sponsor Led Buyout")|(df_innovation_75m_below["CIF_glv"].isin(sponsor_cif))
    df_innovation_75m_below_sponsor = df_innovation_75m_below[mask_sponsor_75].reset_index(drop=True)
    df_innovation_75m_below_nosponsor = df_innovation_75m_below[~mask_sponsor_75].reset_index(drop=True)
    
    mask_sponsor_nofin = (df_innovation_nofin["LIFESTAGE"] == "Sponsor Led Buyout")|(df_innovation_nofin["CIF_glv"].isin(sponsor_cif))
    df_innovation_nofin_sponsor = df_innovation_nofin[mask_sponsor_nofin].reset_index(drop=True)
    df_innovation_nofin_nosponsor = df_innovation_nofin[~mask_sponsor_nofin].reset_index(drop=True)
    
    nolarge_filter = (df_innovation_nofin_nosponsor["LIFESTAGE_GROUP"] == "Large_Corporate")
    df_innovation_nofin_nosponsor_large = df_innovation_nofin_nosponsor[nolarge_filter].reset_index(drop=True)
    df_innovation_nofin_nosponsor_nolarge = df_innovation_nofin_nosponsor[~nolarge_filter].reset_index(drop=True)
    
    Innovation_largecorp = pd.concat([df_innovation_75m_above, df_innovation_75m_below_sponsor, df_innovation_nofin_sponsor, df_innovation_nofin_nosponsor_large]).reset_index(drop=True)
    innovation_no_largecorp = pd.concat([df_innovation_75m_below_nosponsor, df_innovation_nofin_nosponsor_nolarge]).reset_index(drop=True)
    
    df_nolc_fin = innovation_no_largecorp[innovation_no_largecorp["CIF_CRM"].notnull()].reset_index(drop=True)
    df_nolc_nofin = innovation_no_largecorp[innovation_no_largecorp["CIF_CRM"].isnull()].reset_index(drop=True)
    
    df_nolc_fin_15m_above = df_nolc_fin[df_nolc_fin["NETSALES"]>15000].reset_index(drop=True)
    df_nolc_fin_15m_below = df_nolc_fin[df_nolc_fin["NETSALES"]<=15000].reset_index(drop=True)
    
    df_nolc_nofin_ls_et = df_nolc_nofin[df_nolc_nofin["LIFESTAGE_GROUP"].isin(["Innovation_15M"])]
    df_nolc_nofin_ls_noet = df_nolc_nofin[~df_nolc_nofin["LIFESTAGE_GROUP"].isin(["Innovation_15M"])]
    
    df_drr_mid = pd.concat([df_nolc_fin_15m_above, df_nolc_nofin_ls_noet]).reset_index(drop=True)
    df_drr_early = pd.concat([df_nolc_fin_15m_below, df_nolc_nofin_ls_et]).reset_index(drop=True)
     
    return (df_drr_mid,df_drr_early)




# %%
# ### GLV Financials Data - All Loaddt
snapshots_list = df['LOADDT'].unique()

# %%


## DRR Segmentation Data

snapshots = snapshots_list

data = pd.DataFrame()  

start = timeit.default_timer()

for start_date in snapshots:
    
    ts = timeit.default_timer()
    
    snapshot_date = pd.to_datetime(start_date).to_period('M')
    lookback_date = snapshot_date + lookback_window
    
    a,b = drr_segmentation(snapshot_date, lookback_date)
    a['Segment']="Innovation_15-75M"
    b['Segment']="Innovation_15M"

    #Step 10
    #add ._append
    c = pd.concat([a,b])
    data = pd.concat([data,c])
    
    tso = timeit.default_timer()
    


#data['Segment'].value_counts()

# %%


data_full = data.merge(finn, how='left',left_on=['CIF_CRM','STATEMENTDATE','STATEMENTID'],
               right_on=['CIF_CRM','STATEMENTDATE','STATEMENTID'])

# %%


data_full_1=data_full[data_full['CIF_glv']!='0-UNKN']




# %%


###Pull the GLV + Financials Merged Data (Financials Lookback =18 months) for innovation_15M and Innovation_15_75M

GLV_Finn= data_full_1.copy()

# %%


GLV_Finn['CIF_glv_final']=np.where(GLV_Finn['CIF_glv'].str.len()<9,
                                   ('00000000'+GLV_Finn['CIF_glv']).str[-9:], GLV_Finn['CIF_glv'])
GLV_Finn['CIF_glv_final']=GLV_Finn['CIF_glv_final'].str[-9:]

# Create Month year variable for LOADDT 
GLV_Finn['Month_yr']=pd.to_datetime(GLV_Finn['LOADDT']).dt.to_period('M')

# %%
GLV_Finn=GLV_Finn[~(GLV_Finn['CIF_glv_final'].str.contains('UNKN'))]

# %%


GLV_Finn['GLV_Balance']=GLV_Finn['NOTEPRNCPLBALNET_y']

# %%


GLV_Finn=GLV_Finn[['CIF_glv_final','LOADDT','CRR','NOTEPRNCPLBALNET_x','Month_yr','RBS','WORST_CRR','Segment','LIFESTAGE_GROUP','GLV_Balance','LIFESTAGE_IMPUTED','NETSALES_y']]

# %%


GLV_Finn.rename(columns={'NETSALES_y':'NETSALES'},inplace=True)
GLV_Finn.rename(columns={'NOTEPRNCPLBALNET_x':'NOTEPRNCPLBALNET'},inplace=True)




# %%
# ### Default Data

## March 2023 filter
## '2023-12-31','2023-03-31' 

qrystr_def = """

select x.cif as CIF_Default
,eomonth(x.loaddt) as LOADDT_def
,x.default_flag as defflag
,x.risk_cd as mcrr
,x.risk_bas_seg_cd as elseg
from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW] x
where eomonth(x.loaddt) > '{month_end_24m_prior}'

""".format(month_end_24m_prior=month_end_24m_prior)

Df_default=pd.read_sql_query(qrystr_def, conn)
Df_default.LOADDT_def = pd.to_datetime(Df_default.LOADDT_def)

# %%


Df_default['CIF_Default_final']=np.where(Df_default['CIF_Default'].str.len()<9,
                                   ('00000000'+Df_default['CIF_Default']).str[-9:], 
                                   Df_default['CIF_Default'])

## Month Year Variable
Df_default['Month_yr']=pd.to_datetime(Df_default['LOADDT_def']).dt.to_period('M')

# %%


###Extract the CIF's alongwith the first occurence of default
Df_default_first = Df_default[ (Df_default['defflag']=='1') & (Df_default['mcrr'].isin(['5','6','7','8','9','10']))]


Df_default_first=Df_default_first.groupby(['CIF_Default_final']).agg({'LOADDT_def':'min'}).reset_index()
Df_default_first.rename(columns={"LOADDT_def" : "first_def_date"}, inplace=True)

Df_default_first['Default_Year']=pd.to_datetime(Df_default_first['first_def_date']).dt.to_period('Y')

# %%


master_data=GLV_Finn.copy()
master_data_1=pd.merge(master_data,Df_default_first,how='left',left_on=['CIF_glv_final'],right_on=['CIF_Default_final'])




# %%
# ### First CRR7 Date 
# 

#glv_all=pd.read_pickle(in_path+'GLV_2007_2022_all.pkl')
glv_all=df_glv_full.copy()
#glv_all=pd.read_pickle('GLV_2007_2022_extra_vars.pkl')
## check 9 digit CIF 

del df_glv_full
gc.collect()

glv_all['CIF_final']=np.where(glv_all['CIF'].str.len()<9,('00000000'+glv_all['CIF']).str[-9:], glv_all['CIF'])


## Month Year variable
glv_all['Month_yr']=pd.to_datetime(glv_all['LOADDT']).dt.to_period('M')

## UNKN CIF Exclusion

glv_all=glv_all[~(glv_all['CIF_final'].str.contains('UNKN'))]

# Penny Loans Exclusion
glv_all['Penny_Loan']=np.where((glv_all['FACEAMTOFNOTEORGNLBAL'] != 0.01) | (glv_all['FACEAMTOFNOTEORGNLBAL'].isnull()),0,1)
glv_all = glv_all[glv_all['Penny_Loan']==0].reset_index(drop=True)

# %%


## CRR - 7 tagging at CIF, LOADDT level
glv_all["CRR"] = glv_all["RISKCD"].astype(float)
glv_all["CRR"] = glv_all["CRR"].replace(0,11)
glv_grouped=glv_all.groupby(['CIF_final','LOADDT','Month_yr'])['CRR'].max().reset_index()
glv_grouped[glv_grouped['CRR']==7]['CIF_final'].nunique()

# %%


###Extract the CIF's alongwith the first occurence of default
GLV_first_CRR7 = glv_grouped[ (glv_grouped['CRR']==7)]

GLV_first_CRR7=GLV_first_CRR7.groupby(['CIF_final']).agg({'LOADDT':'min'}).reset_index()
GLV_first_CRR7.rename(columns={"LOADDT" : "first_CRR7_date"}, inplace=True)

# %%


master_data_final=pd.merge(master_data_1,GLV_first_CRR7,how='left',left_on=['CIF_glv_final'],right_on=['CIF_final'])

# %%


get_ipython().run_cell_magic('capture', '--no-display', '## Creation of New Default Date\nmaster_data_final["Default_date_Enriched"]=np.where(master_data_final[\'first_def_date\'].isna(),master_data_final[\'first_CRR7_date\'],\n                                                   np.where(master_data_final[\'first_CRR7_date\']<master_data_final[\'first_def_date\'],\n                                                            master_data_final[\'first_CRR7_date\'],master_data_final[\'first_def_date\']))\n\n##Default Flag based on the first occurence of default \nmaster_data_final[\'Default_flag_Enriched\']=np.where((master_data_final[\'LOADDT\']==master_data_final[\'Default_date_Enriched\']),1,0)\n##Default Flag based on first occurence of default (It is assumed that once a CIF goes into default remains always in default )\nmaster_data_final[\'Default_flag2_Enriched\']=np.where((master_data_final[\'LOADDT\']>=master_data_final[\'Default_date_Enriched\']),1,0)\n')

# %%


get_ipython().run_cell_magic('capture', '--no-display', "## Create datediff flag based on exact months - not decimals\n\nmaster_data_final2=master_data_final[~master_data_final['Default_date_Enriched'].isna()]\n\nmaster_data_final2['Year']=(master_data_final2['LOADDT'].astype(str)).str[:4]\nmaster_data_final2['Month']=((master_data_final2['LOADDT'].astype(str)).str[:7]).str[-2:]\nmaster_data_final2['Def_Year']=(master_data_final2['Default_date_Enriched'].astype(str)).str[:4]\nmaster_data_final2['Def_Month']=((master_data_final2['Default_date_Enriched'].astype(str)).str[:7]).str[-2:]\n\nmaster_data_final2['months_default2']=(master_data_final2['Def_Year'].astype(int)-master_data_final2['Year'].astype(int))*12 + (master_data_final2['Def_Month'].astype(int)-master_data_final2['Month'].astype(int))\n\nmaster_data_final=pd.merge(master_data_final,\n                           master_data_final2[['CIF_glv_final','LOADDT','months_default2']],\n                           how='left',on=['CIF_glv_final','LOADDT'])\ndel master_data_final2\n\nmaster_data_final['default_flag_next_12_month_enriched']=np.where((master_data_final['months_default2']>=0) & \n                                            (master_data_final['months_default2']<=12),1,0)\n")




# %%
# ### True Defaults 

get_ipython().run_cell_magic('capture', '--no-display', '## Creation of New Default Date\nmaster_data_final["Default_date"]=master_data_final[\'first_def_date\']\n\n##Default Flag based on the first occurence of default \nmaster_data_final[\'Default_flag\']=np.where((master_data_final[\'LOADDT\']==master_data_final[\'Default_date\']),1,0)\n##Default Flag based on first occurence of default (It is assumed that once a CIF goes into default remains always in default )\nmaster_data_final[\'Default_flag2\']=np.where((master_data_final[\'LOADDT\']>=master_data_final[\'Default_date\']),1,0)\n')

# %%


get_ipython().run_cell_magic('capture', '--no-display', "## Create datediff flag based on exact months - not decimals\n\nmaster_data_final2=master_data_final[~master_data_final['Default_date'].isna()]\n\n\nmaster_data_final2['Year']=(master_data_final2['LOADDT'].astype(str)).str[:4]\nmaster_data_final2['Month']=((master_data_final2['LOADDT'].astype(str)).str[:7]).str[-2:]\nmaster_data_final2['Def_Year']=(master_data_final2['Default_date'].astype(str)).str[:4]\nmaster_data_final2['Def_Month']=((master_data_final2['Default_date'].astype(str)).str[:7]).str[-2:]\n\nmaster_data_final2['months_default2_true']=(master_data_final2['Def_Year'].astype(int)-master_data_final2['Year'].astype(int))*12 + (master_data_final2['Def_Month'].astype(int)-master_data_final2['Month'].astype(int))\n\nmaster_data_final=pd.merge(master_data_final,\n                           master_data_final2[['CIF_glv_final','LOADDT','months_default2_true']],\n                           how='left',on=['CIF_glv_final','LOADDT'])\ndel master_data_final2\n\nmaster_data_final['default_flag_next_12_month']=np.where((master_data_final['months_default2_true']>=0) & \n                                            (master_data_final['months_default2_true']<=12),1,0)\n")

# %%


GLV_Finn=master_data_final.copy()

# %%


Df_default['Default_Available']=1
GLV_Finn=pd.merge(GLV_Finn,Df_default[['CIF_Default_final','Month_yr','elseg','Default_Available']],
                  how='left',left_on=['CIF_glv_final','Month_yr'],right_on=['CIF_Default_final','Month_yr'])

# %%


# Rename RBS
GLV_Finn['RBS_def']=np.where(GLV_Finn['elseg'].isna(),"NULL",
                       np.where(GLV_Finn['elseg']=='NT- PES & VC', 'NT- GFB',
                                np.where(GLV_Finn['elseg']=='ID - Other', 'ID - Later Stage',GLV_Finn['elseg'])))

# %%


## Performance data check
## Missing Performance Indicator Flag

def Next_12M_Performance(x,y):
    
    snaphot=df1[df1['Month_yr'] == x]
    snaphot_CIF=snaphot['CIF_glv_final'].unique()
    
    #check performance in next 12 months in entire history of GLV
    performance_monthly=glv_grouped[(df2['CIF_final'].isin(snaphot_CIF)) & 
                                    (df2['Month_yr'] > x) &(df2['Month_yr'] <= y)]
    performance = performance_monthly.groupby(['CIF_final'])['Month_yr'].size().reset_index()
    performance['CIF_Performance']=1
    performance.rename(columns={"Month_yr" : "Obs_in_nxt_12m"}, inplace=True)
    performance_forward= pd.merge(snaphot,performance,
                                  left_on=['CIF_glv_final'],right_on=['CIF_final'],
                                  how='left',suffixes=('_snapshot', '_performance'))
    performance_forward['CIF_Missing_performance']=np.where(performance_forward['CIF_Performance']==1,0,1)
    performance_forward1 = performance_forward
    #performance_forward1=performance_forward.fillna('Missing_var')
    return performance_forward1

# %%


get_ipython().run_cell_magic('capture', '--no-display', "## All Loaddts\nsnapshots_list = GLV_Finn[['LOADDT']]\nsnapshots_list['LOADDT'] = snapshots_list['LOADDT'].astype(str).str[:7]\nsnapshots_list = list(snapshots_list['LOADDT'].unique())\n#snapshots_list\n")

# %%


performance_window=12

var_list1=['CIF_glv_final','Month_yr']
var_list2=['CIF_final','Month_yr']

df1=GLV_Finn[var_list1]
df2=glv_grouped[var_list2]

snapshots = snapshots_list
data = pd.DataFrame()  

start = timeit.default_timer()

for start_date in snapshots:
    
    ts = timeit.default_timer()
    
    snapshot_date = pd.to_datetime(start_date).to_period('M')
    
    performance_end_date = (snapshot_date + performance_window)
    #print(snapshot_date,performance_end_date)
    a = Next_12M_Performance(snapshot_date, performance_end_date)

    #Step 11
    #change to ._append
    data = pd.concat([data,a])
    
    tso = timeit.default_timer()
    
    #print('completed')
    #print("Time taken to complete for",snapshot_date," : ",(tso-ts)/60)
            
stop = timeit.default_timer()
#print("Total Time taken to complete",(stop-start)/60)

# %%


GLV_Finn=pd.merge(GLV_Finn,data[['CIF_glv_final','Month_yr','CIF_Missing_performance','Obs_in_nxt_12m']],
                  how='left',on=['CIF_glv_final','Month_yr'])

# %%


## Final Default Fields

GLV_Finn['Final_def_date']=np.where(GLV_Finn['Segment']=="Innovation_15-75M",
                                    GLV_Finn['Default_date_Enriched'],GLV_Finn['first_def_date'])

GLV_Finn['Final_Default_flag']=np.where(GLV_Finn['Segment']=="Innovation_15-75M",
                                    GLV_Finn['Default_flag_Enriched'],GLV_Finn['Default_flag'])

GLV_Finn['Final_Default_flag2']=np.where(GLV_Finn['Segment']=="Innovation_15-75M",
                                    GLV_Finn['Default_flag2_Enriched'],GLV_Finn['Default_flag2'])

GLV_Finn['Final_default_flag_next_12m']=np.where(GLV_Finn['Segment']=="Innovation_15-75M",
                                    GLV_Finn['default_flag_next_12_month_enriched'],GLV_Finn['default_flag_next_12_month'])


# ### Credit Lens Financials Data

# %%


## Read Credit Lens data - Ranked - without duplicates

Finn=financials_ranked.copy()

# %%


## 9 digit CIF
Finn['CIF_CRM_final']=np.where(Finn['CIF_CRM'].str.len()<9,('00000000'+Finn['CIF_CRM']).str[-9:], Finn['CIF_CRM'])
Finn['CIF_CRM_final']=Finn['CIF_CRM_final'].str[-9:]

## Month Year Variable
Finn['STATEMENT_Month_yr']=pd.to_datetime(Finn['STATEMENTDATE']).dt.to_period('M')

# %%


## Remove duplicates
Finn = Finn.sort_values(by = ["CIF_CRM_final", "STATEMENT_Month_yr","STATEMENTDATE"], ascending = [True, True,False]).reset_index(drop=True)
Finn["choose_last"] = Finn.groupby(['CIF_CRM_final',"STATEMENT_Month_yr"])['STATEMENTDATE'].rank("first")
mask2 = (Finn['choose_last'] == 1)
Finn = Finn[mask2].copy().reset_index(drop=True)

# %%


## Statemendate + 3 months forward
Finn['STATEMENTDATE_3M_Fwd']=Finn['STATEMENT_Month_yr']+3
Finn['STATEMENT_Available']=1

# %%


GLV_Finn=pd.merge(GLV_Finn,Finn,left_on=['CIF_glv_final','Month_yr'],
                  right_on=['CIF_CRM_final','STATEMENTDATE_3M_Fwd'],how='left')

# %%


var_list_model = ['CIF_glv_final', 'LOADDT', 'Month_yr', 'RBS', 'WORST_CRR', 'Segment',
       'NOTEPRNCPLBALNET', 'CRR', 'Final_Default_flag2',
       'Final_default_flag_next_12m', 'CIF_CRM', 
        'NETSALES_y', 'FUNDEDDEBT', 'EBITDANC',
       'GROSSPROFIT', 'NETPROFIT', 'TOTALLIABS', 'CASHANDEQUIVS',
       'TOTALASSETS', 'CIF_CRM_final',
       'STATEMENT_Month_yr',  'STATEMENTDATE_3M_Fwd','STATEMENT_Available', 'CIF_Missing_performance']




   


# %%


GLV_Finn = GLV_Finn[var_list_model]

GLV_Finn.rename(columns={'NETSALES_y':'NETSALES'},inplace=True)


# ### Credit Lens Financials only

# %%


GLV_Finn_Financials=GLV_Finn[GLV_Finn['STATEMENT_Available']==1]


# ### FMD_Data_Creation - DEV, OOS, OOT Samples

# ### Modeling Excusions Flag

# %%


df=GLV_Finn[GLV_Finn['STATEMENT_Available']==1]

# %%


## Innovation Segment Split
df_15 = df[df['Segment']=='Innovation_15M']
df_75 = df[df['Segment']=='Innovation_15-75M']

# %%


## Modeling Exclusions for Innovation_15M

mask1 = (df_15['Final_Default_flag2']==0)
mask2 = (df_15['CIF_Missing_performance']==0)
mask3 = (df_15['CRR'].isin([8,9,10,11]))
#mask4 = (df_15['Category2'].isin(['90 and above','Impaired']))
#mask5 = (df_15['Month_yr']<=pd.to_datetime('2022-03').to_period('M') )

df_15=df_15[ mask1 & mask2 & ~mask3 ]



# %%


## Modeling Exclusions for Innovation_15-75M

mask1 = (df_75['Final_Default_flag2']==0)
mask2 = (df_75['CIF_Missing_performance']==0)
mask3 = (df_75['CRR'].isin([7,8,9,10,11]))
#mask4 = (df_75['Category2'].isin(['90 and above','Impaired']))
#mask5 = (df_75['Month_yr']<=pd.to_datetime('2022-03').to_period('M') )

df_75=df_75[ mask1 & mask2 & ~mask3 ]

# %%
cif_list_mid_df = pd.read_csv('cif_list_mid_df.csv')
cif_list_early_df = pd.read_csv('cif_list_early_df.csv')

cif_list_mid_df['0'] = cif_list_mid_df['0'].astype(str)
cif_list_early_df['0'] = cif_list_early_df['0'].astype(str)
cif_list_mid = list(cif_list_mid_df['0'])
cif_list_early = list(cif_list_early_df['0'])
df_15 = df_15.loc[df_15.CIF_CRM.isin(cif_list_early)]
df_75 = df_75.loc[df_75.CIF_CRM.isin(cif_list_mid)]

# %%




df_15_dev = pd.read_pickle('Variable_Creation_final_15M_All_vars_v7.pkl')
df_15_dev['WoE_TDEBITDA_mod_tr'] = df_15_dev['WoE_TDEBITDA_mod_new_tr']




# %%


#CREATE Monitoring Sample SPLIT - Innovation 15-75M

df_75_dev = pd.read_pickle('Variable_Creation_final_75M_All_vars_v4.pkl')





# %%


#CREATE TRAIN AND TEST SPLIT - Innovation 15M

random_seed = 888
target='Final_default_flag_next_12m'


df_train_15, df_test_15 = train_test_split(df_15_dev, test_size=0.2, random_state=random_seed,stratify=df_15_dev[target])
df_train_15['Sample_Flag']='DEV'
df_test_15['Sample_Flag']='OOS'

df_15_dev = pd.concat([df_train_15, df_test_15]).reset_index(drop=True)

# %%


#CREATE TRAIN AND TEST SPLIT - Innovation 15-75M

random_seed = 888
target='Final_default_flag_next_12m'


df_train_75, df_test_75 = train_test_split(df_75_dev, test_size=0.2, random_state=random_seed,stratify=df_75_dev[target])
df_train_75['Sample_Flag']='DEV'
df_test_75['Sample_Flag']='OOS'

df_75_dev = pd.concat([df_train_75, df_test_75]).reset_index(drop=True)


# # 1.FMD Additional Variables Creation

# ### Single Factor Analysis

# #### Additional Vars

# %%


def Create_Var_Leverage(df=None,Var=None,Num=None,Den=None):
    df[Var]=np.where( (df[Den]==0) & (df[Num]<0), -999,
                     np.where((df[Den]==0) & (df[Num]>0), 999,
                              np.where((df[Den]==0) & (df[Num]==0), 0,
                                       np.where((df[Den]>0) & (df[Num]<0), -999,
                                                np.where((df[Den]>0) & (df[Num]>0), df[Num]/df[Den],
                                                         np.where((df[Den]>0) & (df[Num]==0), 0,
                                                                  np.where((df[Den]<0) & (df[Num]<0), -999,
                                                                           np.where((df[Den]<0) & (df[Num]>0), df[Num]/df[Den],
                                                                                    np.where((df[Den]<0) & (df[Num]==0), 0, np.nan)))))))))

# %%


Create_Var_Leverage(df=df_15,Var='TDEBITDA_mod',Num='FUNDEDDEBT',Den='EBITDANC')
Create_Var_Leverage(df=df_75,Var='TDEBITDA_mod',Num='FUNDEDDEBT',Den='EBITDANC')



# ### Profitability Variables

# %%


def Create_Var_Profitability(df=None,Var=None,Num=None,Den=None,Mult=None):
    df[Var]=np.where( (df[Den]==0) & (df[Num]<0), -999,
                     np.where((df[Den]==0) & (df[Num]>0), 999,
                              np.where((df[Den]==0) & (df[Num]==0), 0,
                                       np.where((df[Den]>0) & (df[Num]<0), df[Num]*Mult/df[Den],
                                                np.where((df[Den]>0) & (df[Num]>0), df[Num]*Mult/df[Den],
                                                         np.where((df[Den]>0) & (df[Num]==0), 0,
                                                                  np.where((df[Den]<0) & (df[Num]<0), -999,
                                                                           np.where((df[Den]<0) & (df[Num]>0), -999,
                                                                                    np.where((df[Den]<0) & (df[Num]==0), -999, np.nan)))))))))

# %%


# Profitability Variables
Create_Var_Profitability(df=df_15,Var='GROSSMARGIN_mod',Num='GROSSPROFIT',Den='NETSALES',Mult=100)
Create_Var_Profitability(df=df_15,Var='NETMARGIN_mod',Num='NETPROFIT',Den='NETSALES',Mult=100)
Create_Var_Profitability(df=df_75,Var='GROSSMARGIN_mod',Num='GROSSPROFIT',Den='NETSALES',Mult=100)
Create_Var_Profitability(df=df_75,Var='NETMARGIN_mod',Num='NETPROFIT',Den='NETSALES',Mult=100)

# %%


#Create Capital Structure
df_75['Num_CS']=(df_75['TOTALLIABS']-df_75['CASHANDEQUIVS'])
Create_Var_Profitability(df=df_75,Var='Capital_Structure',Num='Num_CS',Den='TOTALASSETS',Mult=1)
df_15['Num_CS']=(df_15['TOTALLIABS']-df_15['CASHANDEQUIVS'])
Create_Var_Profitability(df=df_15,Var='Capital_Structure',Num='Num_CS',Den='TOTALASSETS',Mult=1)


# %%


Modeling_vars=['GROSSMARGIN_mod','NETMARGIN_mod','NETSALES',
               'TDEBITDA_mod','Capital_Structure']


# ### Binning_15-75M

# %%


def var_transform(df1,var_list):
    df=df1
    for var in var_list:
        df[f'{var}_tr']=df[var]
    return df

# %%


def do_binning(df,var,y,neg,cut1,cut2,cut3,cut4,cut5,cut6):
    df_75_subset = df
    df_75_subset['group'] = np.where(df_75_subset[var]==-999,'-999',
                                              np.where(df_75_subset[var]==999,'999',
                                                       np.where(df_75_subset[var]<neg,'Negative',
                                    np.where(df_75_subset[var]<=cut1,"1",
                                            np.where((df_75_subset[var]>cut1) & (df_75_subset[var]<=cut2),"2",
                                                     np.where((df_75_subset[var]>cut2) & (df_75_subset[var]<=cut3),"3",
                                                              np.where((df_75_subset[var]>cut3) & (df_75_subset[var]<=cut4),"4",
                                                                       np.where((df_75_subset[var]>cut4) & (df_75_subset[var]<=cut5),"5",
                                                                                np.where((df_75_subset[var]>cut5) & (df_75_subset[var]<=cut6),"6",'Not binned')))))))))
    d0 = pd.DataFrame({f'Bin_{var}': df_75_subset['group'], 'Target': df_75_subset[y],var: df_75_subset[var],
                       'CIF_glv_final':df_75_subset['CIF_glv_final'],'LOADDT':df_75_subset['LOADDT']})
    d = d0.groupby([f'Bin_{var}']).agg({"Target": ["count", "sum"],var:['max','min','mean','median']}).reset_index()
    d.columns = [f'Bin_{var}', 'N', 'Events','Max_value','Min_value','Mean_value','Median_value']
    d['% of Events'] =np.maximum(0.5,d['Events'])/ d['Events'].sum()
    d['Non-Events'] = d['N'] - d['Events']
    d['% of Non-Events'] = np.maximum(0.5,d['Non-Events']) / d['Non-Events'].sum()
    d['Default_Rate'] = d['Events']/(d['Events']+d['Non-Events'])
    d['Log-odds']=np.log(d['Default_Rate']/(1-d['Default_Rate']))
    d[f'WoE_{var}'] = np.log(d['% of Non-Events']/d['% of Events'])
    d['IV'] = d[f'WoE_{var}'] * (d['% of Non-Events']-d['% of Events'])
    d.insert(loc=0, column='Variable', value=var)
    #print(var," ", d.Bin.unique())
    d_final = pd.merge(d0,d[[f'Bin_{var}',f'WoE_{var}']],on=[f'Bin_{var}'],how='left')
    
    df = pd.merge(df,d_final[[f'Bin_{var}',f'WoE_{var}','CIF_glv_final','LOADDT']],on=['CIF_glv_final','LOADDT'],how='left')
    return df

# %%


#binning done separately because TDEBITDA is the only case where we can commbining Negatives with bin4
def do_binning_tdebitda(df,var,y,neg,cut1,cut2,cut3,cut4,cut5,cut6):
    df_75_subset = df
    df_75_subset['group'] = np.where(df_75_subset[var]==-999,'-999',
                                              np.where(df_75_subset[var]==999,'999',
                                                       np.where(df_75_subset[var]<neg,'4',
                                    np.where(df_75_subset[var]<=cut1,"1",
                                            np.where((df_75_subset[var]>cut1) & (df_75_subset[var]<=cut2),"2",
                                                     np.where((df_75_subset[var]>cut2) & (df_75_subset[var]<=cut3),"3",
                                                              np.where((df_75_subset[var]>cut3) & (df_75_subset[var]<=cut4),"4",
                                                                       np.where((df_75_subset[var]>cut4) & (df_75_subset[var]<=cut5),"5",
                                                                                np.where((df_75_subset[var]>cut5) & (df_75_subset[var]<=cut6),"6",'Not binned')))))))))
    d0 = pd.DataFrame({f'Bin_{var}': df_75_subset['group'], 'Target': df_75_subset[y],var: df_75_subset[var],
                       'CIF_glv_final':df_75_subset['CIF_glv_final'],'LOADDT':df_75_subset['LOADDT']})
    d = d0.groupby([f'Bin_{var}']).agg({"Target": ["count", "sum"],var:['max','min','mean','median']}).reset_index()
    d.columns = [f'Bin_{var}', 'N', 'Events','Max_value','Min_value','Mean_value','Median_value']
    d['% of Events'] =np.maximum(0.5,d['Events'])/ d['Events'].sum()
    d['Non-Events'] = d['N'] - d['Events']
    d['% of Non-Events'] = np.maximum(0.5,d['Non-Events']) / d['Non-Events'].sum()
    d['Default_Rate'] = d['Events']/(d['Events']+d['Non-Events'])
    d['Log-odds']=np.log(d['Default_Rate']/(1-d['Default_Rate']))
    d[f'WoE_{var}'] = np.log(d['% of Non-Events']/d['% of Events'])
    d['IV'] = d[f'WoE_{var}'] * (d['% of Non-Events']-d['% of Events'])
    d.insert(loc=0, column='Variable', value=var)
    #print(var," ", d.Bin.unique())
    d_final = pd.merge(d0,d[[f'Bin_{var}',f'WoE_{var}']],on=[f'Bin_{var}'],how='left')
    
    df = pd.merge(df,d_final[[f'Bin_{var}',f'WoE_{var}','CIF_glv_final','LOADDT']],on=['CIF_glv_final','LOADDT'],how='left')
    return df

# %%


#Calling the binning functions for all variables
a_1 =var_transform(df_75,Modeling_vars)


a_1 = do_binning(a_1,'GROSSMARGIN_mod_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=18.20,cut2=41.40,cut3 =61.85,cut4=81.44,cut5 =100.01,cut6=999999999)
a_1 = do_binning(a_1,'NETMARGIN_mod_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=-72.32,cut2=-21.96,cut3 =2.14,cut4 =138.61,cut5 =99999999,cut6=999999999)
a_1 = do_binning(a_1,'NETSALES_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=20279.01,cut2=30465.01,cut3 =635848.01,cut4=99999999,cut5 =99999999,cut6=999999999)
a_1 = do_binning(a_1,'Capital_Structure_tr','Final_default_flag_next_12m',neg=-9999999999999999,cut1=-0.22,cut2=0.22,
                 cut3 =0.74,cut4=1.60, cut5=39.76,cut6=99999999999)     
a_1 = do_binning_tdebitda(a_1,'TDEBITDA_mod_tr','Final_default_flag_next_12m',neg=0,cut1=0.54,
                             cut2=1.66,cut3 =21.92,cut4=7229,cut5 =99999999,cut6=999999999)

# %%


#Calling the binning functions for all variables for df_15
a_2 =var_transform(df_15,Modeling_vars)


a_2= do_binning(a_2,'TDEBITDA_mod_tr','Final_default_flag_next_12m',neg = 0,cut1=-0.54,cut2=-0.19,cut3=-0.000000000001,cut4=1.92,cut5=1666.84,cut6=99999999)

a_2 = do_binning(a_2,'GROSSMARGIN_mod_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=-10.70,cut2=32.01,cut3 =999999999,cut4=999999999,cut5 =999999999,cut6=999999999)

a_2 = do_binning(a_2,'NETMARGIN_mod_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=-2022.91,cut2=-594.77,cut3 =-95.03,cut4 =-51.27,cut5 =7347.64,cut6=999999999)


a_2 = do_binning(a_2,'NETSALES_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=1732,cut2=3242,cut3 =8385,cut4=1931000,cut5 =999999999,cut6=999999999)

a_2 = do_binning(a_2,'Capital_Structure_tr','Final_default_flag_next_12m',neg=-9999999999,cut1=-0.56,cut2=-0.23,cut3=0.87,cut4=2.7,cut5=9999999999 ,cut6=999999999999)

# %%


final_df_75 = a_1.copy()
final_df_15 = a_2.copy()


# %%


# Replace the woe value for rows where value == -999 with the woe of first positive bin
final_df_75.loc[final_df_75['TDEBITDA_mod_tr'] == -999, 'WoE_TDEBITDA_mod_tr'] =  final_df_75.loc[final_df_75['Bin_TDEBITDA_mod_tr'] == '1', 'WoE_TDEBITDA_mod_tr'].values[0]




# Profitability

# Replace the woe value for rows where value == 999 with the woe of 0 bin
final_df_75.loc[final_df_75['GROSSMARGIN_mod_tr']==999, 'WoE_GROSSMARGIN_mod_tr'] =  final_df_75.loc[final_df_75['Bin_GROSSMARGIN_mod_tr'] == '1', 'WoE_GROSSMARGIN_mod_tr'].values[0]
# Replace the woe value for rows where value == -999 with the woe of worst bin
final_df_75.loc[final_df_75['GROSSMARGIN_mod_tr']==-999, 'WoE_GROSSMARGIN_mod_tr'] =  final_df_75.loc[final_df_75['Bin_GROSSMARGIN_mod_tr'] == '1', 'WoE_GROSSMARGIN_mod_tr'].values[0]
# Replace the woe value for rows where value == -999 with the woe of worst bin
final_df_75.loc[final_df_75['NETMARGIN_mod_tr'] == -999, 'WoE_NETMARGIN_mod_tr'] =  final_df_75.loc[final_df_75['Bin_NETMARGIN_mod_tr'] == '1', 'WoE_NETMARGIN_mod_tr'].values[0]
# Replace the woe value for rows where value == 999 with the woe of 0 bin
final_df_75.loc[final_df_75['NETMARGIN_mod_tr'] == 999, 'WoE_NETMARGIN_mod_tr'] =  final_df_75.loc[final_df_75['Bin_NETMARGIN_mod_tr'] == '3', 'WoE_NETMARGIN_mod_tr'].values[0]



# %%


#Imputation of 999 and -999 with WoE of different bins
     # Profitability 
    # Replace the woe value for rows where value == -999 with the woe of worst bin
final_df_15.loc[final_df_15['GROSSMARGIN_mod_tr']==-999, 'WoE_GROSSMARGIN_mod_tr'] =  final_df_15.loc[final_df_15['Bin_GROSSMARGIN_mod_tr'] == '1', 'WoE_GROSSMARGIN_mod_tr'].values[0]
    # Replace the woe value for rows where value == 999 with the woe of 0 bin
final_df_15.loc[final_df_15['GROSSMARGIN_mod_tr']==999, 'WoE_GROSSMARGIN_mod_tr'] =  final_df_15.loc[final_df_15['Bin_GROSSMARGIN_mod_tr'] == '1', 'WoE_GROSSMARGIN_mod_tr'].values[0]
final_df_15.loc[final_df_15['GROSSMARGIN_mod_tr']==999, 'WoE_GROSSMARGIN_mod_tr'] =  final_df_15.loc[final_df_15['Bin_GROSSMARGIN_mod_tr'] == '2', 'WoE_GROSSMARGIN_mod_tr'].values[0]
    
    # NETMARGIN_mod_tr Replace the woe value for rows where value == 999 with the woe of 0 bin
final_df_15.loc[final_df_15['NETMARGIN_mod_tr'] == 999, 'WoE_NETMARGIN_mod_tr'] =  final_df_15.loc[final_df_15['Bin_NETMARGIN_mod_tr'] == '5', 'WoE_NETMARGIN_mod_tr'].values[0]
       # Scale
    # Replace the woe value for rows where value == 999 with the woe of best bin\n",
final_df_15.loc[final_df_15['NETSALES_tr']==999, 'WoE_NETSALES_tr'] =  final_df_15.loc[final_df_15['Bin_NETSALES_tr'] == '4', 'WoE_NETSALES_tr'].values[0]

    # TDEBITDA_mod_tr Replace the woe value for rows where value == -999 with the woe of best bin  \n",
final_df_15.loc[final_df_15['TDEBITDA_mod_tr'] == -999, 'WoE_TDEBITDA_mod_tr'] =  final_df_15.loc[final_df_15['Bin_TDEBITDA_mod_tr'] == '4','WoE_TDEBITDA_mod_tr'].values[0]
    # TDEBITDA_mod_tr Replace the woe value for rows where value == 999 with the woe of best bin on the negative side 
final_df_15.loc[final_df_15['TDEBITDA_mod_tr'] == 999, 'WoE_TDEBITDA_mod_tr'] =  final_df_15.loc[final_df_15['Bin_TDEBITDA_mod_tr'] == '4','WoE_TDEBITDA_mod_tr'].values[0]
  
   # Capital Structure Replace the woe value for rows where value == -999 with the woe of best bin\n",
final_df_15.loc[final_df_15['Capital_Structure_tr'] == 999, 'WoE_Capital_Structure_tr'] =  final_df_15.loc[final_df_15['Bin_Capital_Structure_tr'] == '5','WoE_Capital_Structure_tr'].values[0]
    # Capital Structure Replace the woe value for rows where value == -999 with the woe of worst bin\n",
final_df_15.loc[final_df_15['Capital_Structure_tr'] == -999, 'WoE_Capital_Structure_tr'] =  final_df_15.loc[final_df_15['Bin_Capital_Structure_tr'] == '5','WoE_Capital_Structure_tr'].values[0]

# %%


train_vars_Woe=list(df_15.columns[df_15.columns.str.contains('WoE')])

# %%


DR_DEV=pd.DataFrame()
DR_bins_DEV=pd.DataFrame()

DR_OOS=pd.DataFrame()
DR_bins_OOS=pd.DataFrame()
summary=pd.DataFrame()

# %%


def Logistic_Regression(df,var_list):
    
    random_seed=72
    np.random.seed(random_seed)
    
    #Extract Dev, OOT and OOS Data
    X_DEV=df[df['Sample_Flag']=='DEV'][var_list]
    
    X_OOS=df[df['Sample_Flag']=='OOS'][var_list]
    y_DEV=df[df['Sample_Flag']=='DEV']['Final_default_flag_next_12m']
   
    y_OOS=df[df['Sample_Flag']=='OOS']['Final_default_flag_next_12m']
    
    CRR_DEV=df[df['Sample_Flag']=='DEV']['CRR']
    
    CRR_OOS=df[df['Sample_Flag']=='OOS']['CRR']
    
    ##Add Constant
    X_DEV_with_const = sm.add_constant(X_DEV)
    
    X_OOS_with_const = sm.add_constant(X_OOS)
    
    ##Fit the model
    model = sm.Logit(y_DEV, X_DEV_with_const)
    result = model.fit()  
    
    # Create a DataFrame to store the results
    var_coefficient = pd.DataFrame({'P-value': result.pvalues,
                       'coefficient': result.params,
                        'Standard_Error':result.bse,
                        'z_Score':result.tvalues}).reset_index()
    
    ###Feature Importance based on ChiSquare
    var_coefficient['ChiSq']=(var_coefficient['z_Score'])**2
    var_coefficient.rename(columns={'index':'variable'},inplace=True)
    
    sum_chiSq=var_coefficient[var_coefficient['variable']!='const']['ChiSq'].sum()
    var_coefficient['sum_chiSq']=sum_chiSq
    var_coefficient['ChiSq_proportion']=var_coefficient['ChiSq']/var_coefficient['sum_chiSq']
    var_coefficient['Feature_Importance_ChiSq']=var_coefficient[var_coefficient['variable']!='const']['ChiSq_proportion'].rank(ascending=False)
    
    # Calculate VIF for each predictor variable
    vif = pd.DataFrame()
    vif["variable"] =var_list
    if len(var_list)>=2:
        vif["VIF"] = [variance_inflation_factor(X_DEV.values, i) for i in range(X_DEV.shape[1])]
    else:
        vif["VIF"]="NA"
        
    ##merge VIF with the Coefficient summary
    var_coefficient=pd.merge(vif,var_coefficient,how='right',on='variable')
    
    var_contribution=round(var_coefficient[var_coefficient['variable']!='const'].ChiSq_proportion *100,1).tolist()

    
    ## significance of p - values 
    Beta_significant=(var_coefficient['coefficient']<0).all()
    Max_p_value=var_coefficient[var_coefficient['variable']!='const']['P-value'].max()
    
    # Make predictions on the OOT and OOS set
    y_pred_DEV = result.predict(X_DEV_with_const)
    
    y_pred_OOS = result.predict(X_OOS_with_const)
    
   
        ## Store the predictions dataset
    DEV = pd.concat([y_DEV, y_pred_DEV, CRR_DEV], axis=1)
   
    OOS = pd.concat([y_OOS, y_pred_OOS, CRR_OOS], axis=1)
    
    DEV['Sample_Flag']='DEV'
    
    OOS['Sample_Flag']='OOS'
    
    Final_df = pd.concat([DEV, OOS], axis=0)
    Final_df.columns = ['Actual','Predicted','CRR','Sample_Flag']

    ##AUC
    auc_DEV=roc_auc_score(y_DEV,y_pred_DEV)
  
    auc_OOS=roc_auc_score(y_OOS,y_pred_OOS)
    
    ##Gini
    Gini_DEV=(2*auc_DEV)-1
   
    Gini_OOS=(2*auc_OOS)-1
    
    ##Default Rate by bins DEV 
    DR_DEV['Defaults']=y_DEV
    DR_DEV['Predicted_Defaults']=y_pred_DEV
    
   
    
      ##Default Rate by bins  OOS
    DR_OOS['Defaults']=y_OOS
    DR_OOS['Predicted_Defaults']=y_pred_OOS
 
    Default_Rate_DEV=DR_DEV['Defaults'].sum()/DR_DEV.shape[0]
    
    Default_Rate_OOS=DR_OOS['Defaults'].sum()/DR_OOS.shape[0]
    
    Pred_Default_Rate_DEV=y_pred_DEV.mean()
    
    Pred_Default_Rate_OOS=y_pred_OOS.mean()

    summary=pd.DataFrame({'Variables_used':[var_list],'Variable_Contribution':[var_contribution],
                         'Default_Rate_DEV':[Default_Rate_DEV],'Default_Rate_OOS':[Default_Rate_OOS],
                        'Pred_Default_Rate_DEV':[Pred_Default_Rate_DEV],
                        'Pred_Default_Rate_OOS':[Pred_Default_Rate_OOS],
                         'Gini_DEV':[Gini_DEV],'Gini_OOS':[Gini_OOS],
                         'AUC_DEV':[auc_DEV],'AUC_OOS':[auc_OOS],
                          'All_Beta_significant':[Beta_significant],'Max p value':[Max_p_value]})
    summary=summary.reset_index()    
    return result,summary,var_coefficient,X_DEV,X_OOS,Final_df, y_pred_DEV

# %%
train_vars_list2_early = ['WoE_NETSALES_tr', 'WoE_NETMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr']
train_vars_list2_mid = ['WoE_NETSALES_tr', 'WoE_GROSSMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr']

result_early,summary_early,var_coefficient_early,X_DEV_early,X_OOS_early,Final_df_early, y_pred_early = Logistic_Regression(df_15_dev,train_vars_list2_early)
result_mid,summary_mid,var_coefficient_mid,X_DEV_mid,X_OOS_mid,Final_df_mid, y_pred_mid = Logistic_Regression(df_75_dev,train_vars_list2_mid)





# ### Create dataframe for holding all KPI values  

# %% [markdown]
# ##### --------End of Code for Data Extraction and Variable Transformation for Early Stage and Mid Size -------- 
# 
# ### Calculation of KPIs for DRR Usage and Model Performance Monitoring
# 

# %% [markdown]
# ### Threshold and Model Name Variable Definition 

# %% [markdown]
# ### Logistic Regression Function 

# %%

def bootstrap_logistic_regression3(Z, num_iterations, var_list):
    random_seed=72
    np.random.seed(random_seed)
    
    coefficient_estimates = pd.DataFrame()

    for _ in range(num_iterations):
        
        
        
        # Create a bootstrap sample by resampling with replacement
        bootstrap_sample = resample(Z, replace=True, random_state=_)
        X_DEV_c = bootstrap_sample[var_list]
        X_DEV_c_with_const = sm.add_constant(X_DEV_c)
        y_DEV_c=bootstrap_sample['Final_default_flag_next_12m']
        model_combined = sm.Logit(y_DEV_c, X_DEV_c_with_const)
        result_c = model_combined.fit()  

        coeff = pd.DataFrame({'coefficient': result_c.params}).reset_index()
        coeff.rename(columns={'index':'variable'},inplace=True)
    
    
        coefficient_estimates = pd.concat([coefficient_estimates, coeff], axis=0)

    return coefficient_estimates


# %% [markdown]
# ### KPI 3, 4, 5, 6: Gini, KS, Pop Stability and Coeff Stability   
# 

# %%

mid_kpi = []


coeff_stab_list_early = []
psi_input_early = []


early_kpi = []

coeff_stab_list_mid = []
psi_input_mid = []






train_vars_list=['Sample_Flag','WoE_NETSALES_tr', 'WoE_NETMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr','Final_default_flag_next_12m']
train_vars_list1=['WoE_NETSALES_tr', 'WoE_NETMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr','Final_default_flag_next_12m']
train_vars_list2=['WoE_NETSALES_tr', 'WoE_GROSSMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr','Final_default_flag_next_12m']



coeff_dict_early = {'WoE_NETSALES_tr': -0.73, 'WoE_NETMARGIN_mod_tr': -0.85, 'WoE_TDEBITDA_mod_tr' : -0.63, 'WoE_Capital_Structure_tr' : -0.96}
intercept_early = 0

    


    
X_Mon_early = final_df_15[train_vars_list1]
y_Mon_early = final_df_15['Final_default_flag_next_12m']
X_Mon_early = X_Mon_early.drop('Final_default_flag_next_12m', axis=1)
X_Mon_early_with_const = sm.add_constant(X_Mon_early)


X_Mon_mid = final_df_75[train_vars_list2]
X_Mon_mid = X_Mon_mid.drop('Final_default_flag_next_12m', axis = 1)
y_Mon_mid = final_df_75['Final_default_flag_next_12m']
X_Mon_mid_with_const = sm.add_constant(X_Mon_mid)
    

random_seed = 72
np.random.seed(random_seed)


   
#predictions with Performance Monitoring period data for Early Stage portfolio
#calculation of default predictions with Development Data for Early Stage portfolio

#Extract Dev Data
X_DEV_early =df_15_dev[df_15_dev['Sample_Flag']=='DEV'][train_vars_list2_early]
     
y_DEV_early=df_15_dev[df_15_dev['Sample_Flag']=='DEV']['Final_default_flag_next_12m']
      
##Add Constant
X_DEV_with_const_early = sm.add_constant(X_DEV_early)
    
   
    
##Fit the model
model_early_1 = sm.Logit(y_DEV_early, X_DEV_with_const_early)
result_early_1 = model_early_1.fit()  
y_pred_Mon_early = result_early_1.predict(X_Mon_early_with_const)



#calculation of auc for the Performance Monitoring dataset for Early Stage portfolio
    
auc_Mon_early =roc_auc_score(y_Mon_early,y_pred_Mon_early)

    

#calculate default predictions for Performance Monitoring dataset for Mid Size portfolio


train_vars_list=['Sample_Flag','WoE_NETSALES_tr', 'WoE_NETMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr','Final_default_flag_next_12m']
train_vars_list1=['WoE_NETSALES_tr', 'WoE_NETMARGIN_mod_tr', 'WoE_TDEBITDA_mod_tr','WoE_Capital_Structure_tr','Final_default_flag_next_12m']


coeff_dict_mid = {'WoE_NETSALES_tr': -0.73, 'WoE_NETMARGIN_mod_tr': -0.85, 'WoE_TDEBITDA_mod_tr' : -0.63, 'WoE_Capital_Structure_tr' : -0.96}
intercept_mid = 0

   
   
    

    
    

   
    #calculation of default predictions with Development Data for Mid Size portfolio
    #Extract Dev Data
X_DEV_mid =df_75_dev[df_75_dev['Sample_Flag']=='DEV'][train_vars_list2_mid]
     
y_DEV_mid=df_75_dev[df_75_dev['Sample_Flag']=='DEV']['Final_default_flag_next_12m']
      
    ##Add Constant
X_DEV_with_const_mid = sm.add_constant(X_DEV_mid)
    
   
    
    ##Fit the model
model_mid_1 = sm.Logit(y_DEV_mid, X_DEV_with_const_mid)
result_mid_1 = model_mid_1.fit()  
y_pred_Mon_mid = result_mid_1.predict(X_Mon_mid_with_const)


    #AUC with Performance Monitoring data for Mid Size portfolio
    
auc_Mon_mid =roc_auc_score(y_Mon_mid,y_pred_Mon_mid)
    
    
    #Gini for Early Stage 
    
    
gini_early = 2*auc_Mon_early - 1
    


    #Gini for Mid Size 


gini_mid = 2*auc_Mon_mid - 1
   


    #KS for Early Stage 

fpr_early, tpr_early, thresholds = roc_curve(y_Mon_early, y_pred_Mon_early)
ks_early = max(tpr_early - fpr_early)
   


    #KS for Mid Size 

fpr_mid, tpr_mid, thresholds = roc_curve(y_Mon_mid, y_pred_Mon_mid)
ks_mid = max(tpr_mid - fpr_mid)
    



   
    #Output PSI for Early Stage 

y_pred_early = y_pred_early.tolist()
y_pred_Mon_early = y_pred_Mon_early.tolist()



     #Output PSI for Mid Size


y_pred_mid = y_pred_mid.tolist()
y_pred_Mon_mid = y_pred_Mon_mid.tolist()
  


    #Input PSI for Early Stage 


for features in train_vars_list2_early:
    df_Mon = X_Mon_early[features].tolist()
    df_Dev = X_DEV_early[features].tolist()
    psi_input2 = psi(df_Mon, df_Dev)
    
    psi_input_early.append(psi_input2)

early_kpi.append(psi_input_early)    

for features2 in train_vars_list2_mid: 
    df_Mon = X_Mon_mid[features2].tolist()
    df_Dev = X_DEV_mid[features2].tolist()
    psi_input2 = psi(df_Mon, df_Dev)
    
    psi_input_mid.append(psi_input2)

mid_kpi.append(psi_input_mid)

num_iterations = 1000  # Number of bootstrap iterations

    

    
coefficient_estimates_early = bootstrap_logistic_regression3(df_15_dev, num_iterations, train_vars_list2_early)
coefficient_estimates_mid = bootstrap_logistic_regression3(df_15_dev, num_iterations, train_vars_list2_mid)



summary_df_early = pd.DataFrame()
summary_df_mid = pd.DataFrame()

for features in train_vars_list2_early:
    
    mean_coefficients_early = np.mean(coefficient_estimates_early[coefficient_estimates_early['variable']==features]['coefficient'], axis=0)
    summary_early =pd.DataFrame({'variable':[features],'mean_coefficients':[mean_coefficients_early]})
    summary_early=summary_early.reset_index() 
    summary_df_early= pd.concat([summary_df_early, summary_early])

orig_model_early = var_coefficient_early[['variable', 'coefficient']]   
summary_df_early = summary_df_early.merge(orig_model_early, left_on = 'variable', right_on = 'variable')
summary_df_early['Diff'] = abs(summary_df_early['coefficient'] - summary_df_early['mean_coefficients'])/summary_df_early['coefficient']
coeff_stab_early = np.mean(summary_df_early['Diff'])
coeff_stab_list_early.append(coeff_stab_early)
early_kpi.append(coeff_stab_list_early)

for features in train_vars_list2_mid:
    mean_coefficients_mid = np.mean(coefficient_estimates_mid[coefficient_estimates_mid['variable']==features]['coefficient'], axis=0)
    summary_mid =pd.DataFrame({'variable':[features],'mean_coefficients':[mean_coefficients_mid]})
    summary_mid=summary_mid.reset_index() 
    summary_df_mid= pd.concat([summary_df_mid, summary_mid])

orig_model_mid = var_coefficient_mid[['variable', 'coefficient']]
summary_df_mid = summary_df_mid.merge(orig_model_mid, left_on = 'variable', right_on = 'variable')
summary_df_mid['Diff'] = abs(summary_df_mid['coefficient'] - summary_df_mid['mean_coefficients'])/summary_df_mid['coefficient']

coeff_stab_mid = np.mean(summary_df_mid['Diff'])
coeff_stab_list_mid.append(coeff_stab_mid)
mid_kpi.append(coeff_stab_list_mid)



    






# %%
table_cols = ['KPI NUMBER','KPI NAME','MODEL','LOADDT','QUARTER','KPI VALUE']

kpi_ref = {model_name[0]: large_corp_kpi, model_name[1] : mid_kpi, model_name[2] : early_kpi}

kpi_table = []

for model in model_name: 
   for i in range(2):
      row = [list(kpi_dict2.keys())[i],list(kpi_dict2.values())[i],model,last_month_end1,kpi_quarter,kpi_ref[model][i]]
      kpi_table.append(row)


kpi_table2 = pd.DataFrame(kpi_table, columns = table_cols)
kpi_table1 = pd.read_csv('all_kpi_Q1_2026_updated_04_13_2026.csv')
kpi_table_consolidated = pd.concat([kpi_table1, kpi_table2])

#kpi_table_consolidated.to_csv('all_kpi_results_q2_2025.csv')

kpi_table_consolidated_v2 = kpi_table_consolidated.explode('KPI VALUE')
kpi_table_consolidated_v2.to_csv('all_kpi_results_q1_2026_v2.csv')

# %% [markdown]
# ### Saving KPI outputs for Early Stage and Mid Stage 

# %% [markdown]
# ### Generating Graphs for Data Distribution for the 3 Models 

# %%
var_large = ['NETSALES', 'GROSSMARGIN', 'TDEBITDA', 'CURRENTRATIO', 'FIXEDCHARGECOVER']

for var in var_large: 
    data_large = ar_data_large[var]
    
    #Calculate quartiles and IQR
    Q1 = data_large.quantile(0.25)
    Q3 = data_large.quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    filtered_data = data_large[(data_large >= lower_bound) & (data_large <= upper_bound)]




    #plt.xlabel = 'Variable'
    #plt.ylabel = 'Frequency'
    
    plt.hist(filtered_data,bins = 30,  color = 'orange', edgecolor = 'black' )
    plt.title('Large Corp_' + var + '_predict_data')
    
    plt.savefig('Large_Corp_' + var + '_predict_data' + '.jpg')
    plt.show()
    
    plt.close()
    

# %% [markdown]
# ### Graphs for KPIs
# 

# %%
df_75_graph = final_df_75.copy()
    
    
df_15_graph = final_df_15.copy()
    

# %%
""" for i in range(6):
    for j in range(3):
        fig, ax = plt.subplots()
        ax.plot(eval_dates, kpi_list.iloc[i,j], linestyle='--', marker='o', color='blue')
        #ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_xlabel('Monitoring Period')
        ax.set_ylabel(kpi_names_graph[i], color='black')
        ax.set_title(model_name[j] + ": " +  kpi_names_graph[i])
        ax.set_xticks(eval_dates)
        #ax.set_ylim([0,plot2_y_max])
        #plt.figtext(0.5, -0.1, txt, wrap=True, horizontalalignment='center', fontsize=10)
        plt.xticks(rotation=45)
        #ax.legend(loc=0)
        #plt.show()
#fig.savefig("{}\{}\Pct_Grades_NotMonotonic.png".format(image_path,name)) 
    
"""

# %%
var_early = ['NETSALES',
 'NETMARGIN_mod',
 'TDEBITDA_mod',
 'Capital_Structure']

var_mid = ['NETSALES',
 'GROSSMARGIN_mod',
 'TDEBITDA_mod',
 'Capital_Structure']

for var in var_mid: 
    data_large = df_75_graph[var]
    
    #Calculate quartiles and IQR
    Q1 = data_large.quantile(0.25)
    Q3 = data_large.quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    filtered_data = data_large[(data_large >= lower_bound) & (data_large <= upper_bound)]




    #plt.xlabel = 'Variable'
    #plt.ylabel = 'Frequency'
    
    plt.hist(filtered_data,bins = 30,  color = 'orange', edgecolor = 'black' )
    plt.title('Mid_Size_' + var + '_predict_data')
    
    plt.savefig('Mid_Size_' + var + '_predict_data' + '.jpg')
    plt.show()
    plt.close()
    

# %%
file = pd.DataFrame({'Factor': var_early,'Input_PSI': psi_input_early})
file.to_csv('early_input_psi.csv')

# %%
train_vars_list2_early

# %%
var_early = ['NETSALES',
 'NETMARGIN_mod',
 'TDEBITDA_mod',
 'Capital_Structure']

var_mid = ['NETSALES',
 'GROSSMARGIN_mod',
 'TDEBITDA_mod',
 'Capital_Structure']

for var in var_early: 
    data_large = df_15_graph[var]
    
    #Calculate quartiles and IQR
    Q1 = data_large.quantile(0.25)
    Q3 = data_large.quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    filtered_data = data_large[(data_large >= lower_bound) & (data_large <= upper_bound)]




    #plt.xlabel = 'Variable'
    #plt.ylabel = 'Frequency'
    
    plt.hist(filtered_data,bins = 30,  color = 'orange', edgecolor = 'black' )
    plt.title('Early_Stage_' + var + '_predict_data')
    
    plt.savefig('Early_Stage_' + var + '_predict_data' + '.jpg')
    plt.show()
    plt.close()
    

# %%
psi_input_mid2 = pd.DataFrame({'Factor': var_mid, 'PSI': psi_input_mid})
psi_input_mid2.to_csv('mid_input_psi.csv')

psi_input_large2 = pd.DataFrame({'Factor': var_large, 'PSI': psi_input_large})
psi_input_large2.to_csv('large_corp_input_psi.csv')


