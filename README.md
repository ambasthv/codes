# %%
# ### Importing libraries to be used for getting data and KPI calculations


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

from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta 
import timeit
from pandas.tseries.offsets import DateOffset

from sklearn.metrics import log_loss, roc_auc_score, recall_score, precision_score
from sklearn.metrics import average_precision_score, f1_score, classification_report
from sklearn.metrics import accuracy_score

from sklearn.metrics import roc_curve
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')
start = datetime.now()
#print(start)


# %%
model_name = ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage', 'GFB CCLOC', 'GFB NAV', 'GFB Firm']

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

# %%
sql_drr_all = """


select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS', 'Innovation > $15MM up to $75MM',
      'Innovation up to $15MM','CCLOC', 'NAV', 'GFB Firm' )	

     	
      		
				
				
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
                
                
    
    
    """


# %%
drr_all = pd.DataFrame(pd.read_sql_query(sql_drr_all, conn))

# %%
drr_all_v2 = drr_all[['CIF', 'DATE_APPROVED','FINAL_ORR','risk_grade_template']]
drr_all_v2 = drr_all_v2.drop_duplicates()

# %%

pivot = pd.pivot_table(
    drr_all_v2,
    index='FINAL_ORR',      # rows
    columns='risk_grade_template',   # columns
    aggfunc='size',           # count occurrences
    fill_value=0
)

print(pivot)


# %%
pivot.to_csv('risk_model_orr_distribution.csv')


