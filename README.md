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

# %% [markdown]
# ##### create dates to be used for generating migration matrix
# 

# %%

import os
#print(os.getcwd())

current_date = date.today()
month_end = current_date + relativedelta(day=31)
last_month_end = month_end - relativedelta(months = 1)
last_month_end = last_month_end + pd.offsets.MonthEnd(n=0)
last_month_end1 = last_month_end.strftime("%m/%d/%Y")

month_end_3m_prior = month_end -relativedelta(months=4)

month_end_3m_prior = month_end_3m_prior + pd.offsets.MonthEnd(n=0)
month_end_3m_prior = month_end_3m_prior.strftime("%m/%d/%Y")



month_end_12m_prior = month_end - relativedelta(months=13)

month_end_12m_prior = month_end_12m_prior + pd.offsets.MonthEnd(n=0)
month_end_12m_prior = month_end_12m_prior.strftime("%m/%d/%Y")

month_end_24m_prior = month_end - relativedelta(months=24)

month_end_24m_prior = month_end_24m_prior + pd.offsets.MonthEnd(n=0)
month_end_24m_prior = month_end_24m_prior.strftime("%m/%d/%Y")



last_month = last_month_end.month
kpi_quarter = month_to_quarter(last_month)





model_name = ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage', 'GFB CCLOC', 'GFB NAV', 'GFB Firm']


# %%
print(last_month_end1, kpi_quarter, month_end_3m_prior)

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




# %%
# download CIF lists for all Innovation portfolios

cif_list_ccloc_df = pd.read_csv('cif_list_ccloc_df.csv')
cif_list_ccloc_df['0'] = cif_list_ccloc_df['0'].astype(str)
cif_list_ccloc = list(cif_list_ccloc_df['0'])

cif_list_nav_df = pd.read_csv('cif_list_nav_df.csv')
cif_list_nav_df['0'] = cif_list_nav_df['0'].astype(str)
cif_list_nav = list(cif_list_nav_df['0'])

cif_list_firm_df = pd.read_csv('cif_list_firm_df.csv')
cif_list_firm_df['0'] = cif_list_firm_df['0'].astype(str)
cif_list_firm = list(cif_list_firm_df['0'])

cif_list_large_df = pd.read_csv('cif_list_large_df.csv')
cif_list_large_df['0'] = cif_list_large_df['0'].astype(str)
cif_list_large = list(cif_list_large_df['0'])

cif_list_mid_df = pd.read_csv('cif_list_mid_df.csv')
cif_list_mid_df['0'] = cif_list_mid_df['0'].astype(str)
cif_list_mid = list(cif_list_mid_df['0'])

cif_list_early_df = pd.read_csv('cif_list_early_df.csv')
cif_list_early_df['0'] = cif_list_early_df['0'].astype(str)
cif_list_early = list(cif_list_early_df['0'])




# %%
def flatten_matrix(summatrix1, model_name):
    rows,cols = summatrix1.shape
    mm_row = []
    for i in range(rows):
        for j in range(cols): 
            value = summatrix1.item(i, j)
            #lst = []
            mm_row.append(['KPI 3', 'Migration Matrix', model_name, last_month_end, kpi_quarter, i, j])
    
    return mm_row

# %%
#extracting total portfolio data

sql_this_qtr = """
                select CIF as CIF_CRM, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
                """.format(last_month_end1=last_month_end1)
sql_last_qtr  = """
                select CIF as CIF_CRM, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
                """.format(month_end_3m_prior=month_end_3m_prior)


last_qtr =  pd.read_sql_query(sql_last_qtr, conn)

this_qtr = pd.read_sql_query(sql_this_qtr, conn)

all_qtr = pd.concat([this_qtr, last_qtr])

# %% [markdown]
# ### Migration Matrix for GFB CCLOC Portfolio

# %%
#KPI 3: GFB CCLOC Migration Matrix of Previous Period DRR to Current Period DRR 



cif_mask2 = all_qtr['CIF_CRM'].isin(cif_list_ccloc)

all_qtr = all_qtr[cif_mask2]

all_qtr.dropna(inplace = True)

all_qtr['FINAL_ORR'] = pd.to_numeric(all_qtr['FINAL_ORR'])

num_lc = max(all_qtr['FINAL_ORR'].unique()) + 1
print(num_lc)
#create transition matrix function

def tr_matrix(tr):
    #n = 1+max(tr) #number of states
    n = num_lc
    M = [[0]*n for _ in range(n)]
    for (i, j) in zip(tr, tr[1:]):
        M[i][j] += 1
    #for row in M:
        #s = sum(row)
        #if s > 0:
            #row[:] = [round(f/s,2) for f in row]
    return M


#create empty list

tlist = []

def check(k, l):
    if k.shape[0] == 2:
        l.append(k) 

#populate list with one sublist for each cif
for CIF_CRM in all_qtr.CIF_CRM.unique():
    tlist1 = all_qtr.loc[all_qtr.CIF_CRM == CIF_CRM]
    check(tlist1, tlist)
            
#create one transition matrix for each account    
tr_mat_list = []

for t in tlist:
    #print(tlist)
    print(t.FINAL_ORR)
    mat = np.matrix(tr_matrix(t.FINAL_ORR))
    tr_mat_list.append(mat)

#add up all the matrices    
    
summatrix = np.zeros((num_lc,num_lc))
for  s in tr_mat_list:
    summatrix = summatrix + s

    
#normalize the matrix so probabilities sum to 1    
summatrix_ccloc = summatrix/summatrix.sum(axis=1)

summatrix_ccloc[np.isnan(summatrix_ccloc)] = 0
#summatrix_large[0,0] = 1
np.set_printoptions(formatter={'float_kind':'{:f}'.format})




# %% [markdown]
# ### Migration Matrix for GFB NAV Portfolio

# %%
#KPI 3: GFB Firm Migration Matrix of Previous Period DRR to Current Period DRR 




cif_mask2 = all_qtr['CIF_CRM'].isin(cif_list_nav)

all_qtr = all_qtr[cif_mask2]

all_qtr.dropna(inplace = True)

all_qtr['FINAL_ORR'] = pd.to_numeric(all_qtr['FINAL_ORR'])

try: 
    num_lc = max(all_qtr['FINAL_ORR'].unique()) + 1
except ValueError:
    num_lc = 0

print(num_lc)
#create transition matrix function

def tr_matrix(tr):
    #n = 1+max(tr) #number of states
    n = num_lc
    M = [[0]*n for _ in range(n)]
    for (i, j) in zip(tr, tr[1:]):
        M[i][j] += 1
    #for row in M:
        #s = sum(row)
        #if s > 0:
            #row[:] = [round(f/s,2) for f in row]
    return M


#create empty list

tlist = []

def check(k, l):
    if k.shape[0] == 2:
        l.append(k) 

#populate list with one sublist for each cif
for CIF_CRM in all_qtr.CIF_CRM.unique():
    tlist1 = all_qtr.loc[all_qtr.CIF_CRM == CIF_CRM]
    check(tlist1, tlist)
            
#create one transition matrix for each account    
tr_mat_list = []

for t in tlist:
    #print(tlist)
    print(t.FINAL_ORR)
    mat = np.matrix(tr_matrix(t.FINAL_ORR))
    tr_mat_list.append(mat)

#add up all the matrices    
    
summatrix = np.zeros((num_lc,num_lc))
for  s in tr_mat_list:
    summatrix = summatrix + s

    
#normalize the matrix so probabilities sum to 1    
summatrix_nav = summatrix/summatrix.sum(axis=1)

summatrix_nav[np.isnan(summatrix_nav)] = 0
#summatrix_nav[0,0] = 1
np.set_printoptions(formatter={'float_kind':'{:f}'.format})




# %% [markdown]
# ### Migration Matrix for GFB Firm Portfolio

# %%
#KPI 3: GFB Firm Migration Matrix of Previous Period DRR to Current Period DRR 


cif_mask2 = all_qtr['CIF_CRM'].isin(cif_list_firm)

all_qtr = all_qtr[cif_mask2]

all_qtr.dropna(inplace = True)

all_qtr['FINAL_ORR'] = pd.to_numeric(all_qtr['FINAL_ORR'])


try:
    num_lc = max(all_qtr['FINAL_ORR'].unique()) + 1
except ValueError:
    num_lc = 0
print(num_lc)
#create transition matrix function

def tr_matrix(tr):
    #n = 1+max(tr) #number of states
    n = num_lc
    M = [[0]*n for _ in range(n)]
    for (i, j) in zip(tr, tr[1:]):
        M[i][j] += 1
    #for row in M:
        #s = sum(row)
        #if s > 0:
            #row[:] = [round(f/s,2) for f in row]
    return M


#create empty list

tlist = []

def check(k, l):
    if k.shape[0] == 2:
        l.append(k) 

#populate list with one sublist for each cif
for CIF_CRM in all_qtr.CIF_CRM.unique():
    tlist1 = all_qtr.loc[all_qtr.CIF_CRM == CIF_CRM]
    check(tlist1, tlist)
            
#create one transition matrix for each account    
tr_mat_list = []

for t in tlist:
    #print(tlist)
    print(t.FINAL_ORR)
    mat = np.matrix(tr_matrix(t.FINAL_ORR))
    tr_mat_list.append(mat)

#add up all the matrices    
    
summatrix = np.zeros((num_lc,num_lc))
for  s in tr_mat_list:
    summatrix = summatrix + s

    
#normalize the matrix so probabilities sum to 1    
summatrix_firm = summatrix/summatrix.sum(axis=1)

summatrix_firm[np.isnan(summatrix_firm)] = 0
#summatrix_firm[0,0] = 1
np.set_printoptions(formatter={'float_kind':'{:f}'.format})




# %% [markdown]
# ### Migration Matrix for DRR Large Corp Portfolio

# %%
#KPI 3: Migration Matrix of DRR Large Corp Previous Period DRR to Current Period DRR 




#Large Corp

sql_this_qtr = """
                select CIF as CIF_CRM, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
                """.format(last_month_end1=last_month_end1)
sql_last_qtr  = """
                select CIF as CIF_CRM, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
                """.format(month_end_3m_prior=month_end_3m_prior)

last_qtr =  pd.read_sql_query(sql_last_qtr, conn)

this_qtr = pd.read_sql_query(sql_this_qtr, conn)

all_qtr = pd.concat([this_qtr, last_qtr])

cif_mask2 = all_qtr['CIF_CRM'].isin(cif_list_large)

all_qtr = all_qtr[cif_mask2]

all_qtr.dropna(inplace = True)

all_qtr['FINAL_ORR'] = pd.to_numeric(all_qtr['FINAL_ORR'])

num_lc = max(all_qtr['FINAL_ORR'].unique()) + 1
print(num_lc)
#create transition matrix function

def tr_matrix(tr):
    #n = 1+max(tr) #number of states
    n = num_lc
    M = [[0]*n for _ in range(n)]
    for (i, j) in zip(tr, tr[1:]):
        M[i][j] += 1
    #for row in M:
        #s = sum(row)
        #if s > 0:
            #row[:] = [round(f/s,2) for f in row]
    return M


#create empty list

tlist = []

def check(k, l):
    if k.shape[0] == 2:
        l.append(k) 

#populate list with one sublist for each cif
for CIF_CRM in all_qtr.CIF_CRM.unique():
    tlist1 = all_qtr.loc[all_qtr.CIF_CRM == CIF_CRM]
    check(tlist1, tlist)
            
#create one transition matrix for each account    
tr_mat_list = []

for t in tlist:
    #print(tlist)
    print(t.FINAL_ORR)
    mat = np.matrix(tr_matrix(t.FINAL_ORR))
    tr_mat_list.append(mat)

#add up all the matrices    
    
summatrix = np.zeros((num_lc,num_lc))
for  s in tr_mat_list:
    summatrix = summatrix + s

    
#normalize the matrix so probabilities sum to 1    
summatrix_large = summatrix/summatrix.sum(axis=1)

summatrix_large[np.isnan(summatrix_large)] = 0
#summatrix_large[0,0] = 1
np.set_printoptions(formatter={'float_kind':'{:f}'.format})




# %% [markdown]
# ### Migration Matrix for Mid Size Portfolio

# %%



#Large Corp

sql_this_qtr = """
                select CIF as CIF_CRM_final, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
                """.format(last_month_end1=last_month_end1)
sql_last_qtr  = """
                select CIF as CIF_CRM_final, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
                """.format(month_end_3m_prior=month_end_3m_prior)

last_qtr =  pd.read_sql_query(sql_last_qtr, conn)

this_qtr = pd.read_sql_query(sql_this_qtr, conn)

all_qtr = pd.concat([this_qtr, last_qtr])

cif_mask2 = all_qtr['CIF_CRM_final'].isin(cif_list_mid)

all_qtr = all_qtr[cif_mask2]

all_qtr.dropna(inplace = True)

all_qtr['FINAL_ORR'] = pd.to_numeric(all_qtr['FINAL_ORR'])

num_lc = max(all_qtr['FINAL_ORR'].unique()) + 1
print(num_lc)
#create transition matrix function

def tr_matrix(tr):
    #n = 1+max(tr) #number of states
    n = num_lc
    M = [[0]*n for _ in range(n)]
    for (i, j) in zip(tr, tr[1:]):
        M[i][j] += 1
    #for row in M:
        #s = sum(row)
        #if s > 0:
            #row[:] = [round(f/s,2) for f in row]
    return M


#create empty list

tlist = []

def check(k, l):
    if k.shape[0] == 2:
        l.append(k) 

#populate list with one sublist for each cif
for CIF_CRM_final in all_qtr.CIF_CRM_final.unique():
    tlist1 = all_qtr.loc[all_qtr.CIF_CRM_final == CIF_CRM_final]
    check(tlist1, tlist)
            
#create one transition matrix for each account    
tr_mat_list = []

for t in tlist:
    #print(tlist)
    print(t.FINAL_ORR)
    mat = np.matrix(tr_matrix(t.FINAL_ORR))
    tr_mat_list.append(mat)

#add up all the matrices    
    
summatrix = np.zeros((num_lc,num_lc))
for  s in tr_mat_list:
    summatrix = summatrix + s

    
#normalize the matrix so probabilities sum to 1    
summatrix_mid = summatrix/summatrix.sum(axis=1)

summatrix_mid[np.isnan(summatrix_mid)] = 0
#summatrix_mid[0,0] = 1
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

kpi3_row = flatten_matrix(summatrix_mid, model_name[1])


# %% [markdown]
# ### Migration Matrix for Early Stage Portfolio

# %%




#Early Stage

sql_this_qtr = """
                select CIF as CIF_CRM_final, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
                """.format(last_month_end1=last_month_end1)
sql_last_qtr  = """
                select CIF as CIF_CRM_final, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
                """.format(month_end_3m_prior=month_end_3m_prior)

last_qtr =  pd.read_sql_query(sql_last_qtr, conn)

this_qtr = pd.read_sql_query(sql_this_qtr, conn)

all_qtr = pd.concat([this_qtr, last_qtr])

cif_mask2 = all_qtr['CIF_CRM_final'].isin(cif_list_early)

all_qtr = all_qtr[cif_mask2]

all_qtr.dropna(inplace = True)

all_qtr['FINAL_ORR'] = pd.to_numeric(all_qtr['FINAL_ORR'])

num_lc = max(all_qtr['FINAL_ORR'].unique()) + 1
print(num_lc)
#create transition matrix function

def tr_matrix(tr):
    #n = 1+max(tr) #number of states
    n = num_lc
    M = [[0]*n for _ in range(n)]
    for (i, j) in zip(tr, tr[1:]):
        M[i][j] += 1
    #for row in M:
        #s = sum(row)
        #if s > 0:
            #row[:] = [round(f/s,2) for f in row]
    return M


#create empty list

tlist = []

def check(k, l):
    if k.shape[0] == 2:
        l.append(k) 

#populate list with one sublist for each cif
for CIF_CRM_final in all_qtr.CIF_CRM_final.unique():
    tlist1 = all_qtr.loc[all_qtr.CIF_CRM_final == CIF_CRM_final]
    check(tlist1, tlist)
            
#create one transition matrix for each account    
tr_mat_list = []

for t in tlist:
    #print(tlist)
    print(t.FINAL_ORR)
    mat = np.matrix(tr_matrix(t.FINAL_ORR))
    tr_mat_list.append(mat)

#add up all the matrices    
    
summatrix = np.zeros((num_lc,num_lc))
for  s in tr_mat_list:
    summatrix = summatrix + s

    
#normalize the matrix so probabilities sum to 1    
summatrix_early = summatrix/summatrix.sum(axis=1)

summatrix_early[np.isnan(summatrix_early)] = 0
#summatrix_early[0,0] = 1
np.set_printoptions(formatter={'float_kind':'{:f}'.format})

kpi3_row = flatten_matrix(summatrix_early, model_name[2])


# %% [markdown]
# ### Saving Transition Matrices as CSV Files 

# %%
summatrix_early1 = pd.DataFrame(summatrix_early)
summatrix_early1.to_csv('migration_matrix_early.csv')

summatrix_mid1 = pd.DataFrame(summatrix_mid)
summatrix_mid1.to_csv('migration_matrix_mid.csv')

summatrix_large1 = pd.DataFrame(summatrix_large)
summatrix_large1.to_csv('migration_matrix_large.csv')

summatrix_firm1 = pd.DataFrame(summatrix_firm)
summatrix_firm1.to_csv('migration_matrix_firm.csv')

summatrix_nav1 = pd.DataFrame(summatrix_nav)
summatrix_nav1.to_csv('migration_matrix_nav.csv')

summatrix_ccloc1 = pd.DataFrame(summatrix_ccloc)
summatrix_ccloc1.to_csv('migration_matrix_ccloc.csv')


