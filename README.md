Extracted SQL Code Blocks — Migration Matrix Notebook
Extracted verbatim from the provided Jupyter notebook script (sql_this_qtr / sql_last_qtr variables). Each block is labeled with the notebook section it appears under. Python string-formatting placeholders like {last_month_end1} are noted where they appear.

sql_this_qtr  (Extracting total portfolio data)
select CIF as CIF_CRM, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
Note: {last_month_end1} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_last_qtr  (Extracting total portfolio data)
select CIF as CIF_CRM, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
Note: {month_end_3m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_this_qtr  (Migration Matrix for DRR Large Corp Portfolio)
select CIF as CIF_CRM, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
Note: {last_month_end1} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_last_qtr  (Migration Matrix for DRR Large Corp Portfolio)
select CIF as CIF_CRM, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
Note: {month_end_3m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_this_qtr  (Migration Matrix for Mid Size Portfolio)
select CIF as CIF_CRM_final, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
Note: {last_month_end1} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_last_qtr  (Migration Matrix for Mid Size Portfolio)
select CIF as CIF_CRM_final, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
Note: {month_end_3m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_this_qtr  (Migration Matrix for Early Stage Portfolio)
select CIF as CIF_CRM_final, LOADDT, max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{last_month_end1}'
                group by CIF, LOADDT
Note: {last_month_end1} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_last_qtr  (Migration Matrix for Early Stage Portfolio)
select CIF as CIF_CRM_final, LOADDT,max(CL_OBLIGOR_RISK_RATING) as FINAL_ORR 
                from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where LOADDT = '{month_end_3m_prior}'
                group by CIF, LOADDT
Note: {month_end_3m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

