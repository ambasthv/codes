Extracted SQL Code Blocks
Extracted verbatim from the provided Jupyter notebook script (sql_* variables). Python string-formatting placeholders like {list2} are noted where they appear.

sql_override
select distinct  a.CIF, a.RISK_GRADE_TEMPLATE	
            				
            
 
            from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
			[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
			a.credit_req_nbr = b.CREDIT_REQ_NBR
			
and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 'Innovation > $75MM & Sponsor – ID/BS', 'GFB Firm'
 , 'Innovation > $15MM up to $75MM', 'Innovation up to $15MM', 'CCLOC', 'NAV' )	
 
 		
			and b.CREDIT_REQ_STATUS = 'Booked'
			
			and a.cif is not null

sql_chargeoff
SET NOCOUNT ON
 
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

sql_default
SELECT a.LOADDT, a.CIF, a.RISK_CD, a.DEFAULT_FLAG
  FROM [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW] a
 
  inner join 
 
  (select CIF, min(loaddt) as min_date
 
from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
 
where default_flag = 1
group by cif ) b 
 
on a.cif = b.cif and a.loaddt = b.min_date

sql_balance
select a.LOADDT, a.CIF, a.FACILITY_TYPE AS FACILITYTYPE, a.NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] a
 
inner join 
 
(select cif, facility_type, max(loaddt) as max_date from 
 
[CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' and NET_LOAN_BAL > 0
group by cif, facility_type) b
 
on a.cif = b.cif and a.loaddt = b.max_date and a.facility_type = b.facility_type 
 
where a.cif in ({list2})
Note: {list2} is a Python string-formatted placeholder in the original script (a comma-separated, quoted list of CIF values built at runtime), not literal SQL syntax.

sql_large
select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 
 
and  cif in ({list_large}) and loaddt in ( '09-30-2025', '03-31-2026')
Note: {list_large} is a Python string-formatted placeholder (list of CIF values), not literal SQL syntax.

sql_mid
select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 
 
and  cif in ({list_large}) and loaddt in ( '09-30-2025', '03-31-2026')
Note: this block's .format() call uses list_large=list_mid2 — so {list_large} in the string is populated with the Mid Size CIF list at runtime, not literal SQL syntax.

sql_early
select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 
 
and  cif in ({list_early}) and loaddt in ( '09-30-2025', '03-31-2026')
Note: {list_early} is a Python string-formatted placeholder (list of CIF values), not literal SQL syntax.

sql_ccloc
select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 
 
and  cif in ({list_ccloc}) and loaddt in ( '09-30-2025', '03-31-2026')
Note: {list_ccloc} is a Python string-formatted placeholder (list of CIF values), not literal SQL syntax.

sql_nav
select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 
 
and  cif in ({list_nav}) and loaddt in ( '09-30-2025', '03-31-2026')
Note: {list_nav} is a Python string-formatted placeholder (list of CIF values), not literal SQL syntax.

sql_firm
select LOADDT, CIF, FINAL_LGD, NET_LOAN_BAL
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES] where line_status = 'Active' 
 
and  cif in ({list_firm}) and loaddt in ( '09-30-2025', '03-31-2026')
Note: {list_firm} is a Python string-formatted placeholder (list of CIF values), not literal SQL syntax.

