Extracted SQL Code Blocks — PD Model Performance KPI Notebook
Extracted verbatim from the provided Jupyter notebook script (sql_* variables). Each block is labeled with the variable name and the notebook section it appears under. Python string-formatting placeholders like {month_end_12m_prior} are noted where they appear.

sql_override_all  (troubleshooting extract — all risk templates)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS', 'Innovation > $15MM up to $75MM',
      'Innovation up to $15MM','CCLOC', 'NAV', 'GFB Firm' )	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_port_12m  (Portfolio Data for ORR for each Month End in 12M Evaluation Period)
SET NOCOUNT ON
 
select  loaddt as MonthEnd, CIF, max(CL_OBLIGOR_RISK_RATING) as orr1 
 
 
from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW]
 
where loaddt in ('{last_12_month_ends1}')
 
group by loaddt, cif
Note: {last_12_month_ends1} is a Python string-formatted placeholder (a comma-separated list of date strings), not literal SQL syntax.

sql_override  (DRR Large Corp — overrides)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS')	
 
     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_override3  (DRR Mid Size — overrides)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in (  'Innovation > $15MM up to $75MM' )	
 
     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_override2  (DRR Early Stage — overrides)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM' )	
 
     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_override4  (DRR GFB Firm — overrides)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm' )	
 
     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_override4  (DRR GFB CCLOC — overrides; note: variable name reused from the Firm query above)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC' )	
 
     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_override5  (DRR GFB NAV — overrides)
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV' )	
 
     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_default  (Default Status Data for all Models)
SELECT distinct cif, loaddt, default_flag
 
from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
 
			where loaddt > '01-01-2024'

sql_large  (PD accuracy — DRR Large Corp)
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS')	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_mid  (PD accuracy — DRR Mid Size)
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $15MM up to $75MM')	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_firm  (PD accuracy — GFB Firm)
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm')	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_ccloc  (PD accuracy — CCLOC)
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC')	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_early  (PD accuracy — Early Stage)
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM')	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

sql_nav  (PD accuracy — NAV)
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV')	
 
     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Note: {month_end_12m_prior} is a Python string-formatted placeholder (a date string), not literal SQL syntax.

