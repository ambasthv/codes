This code segment is to extract dataset for troubleshooting in case a deep dive into the KPIs is required
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
Portfolio Data for ORR for each Month End in 12M Evaluation Period
SET NOCOUNT ON

select  loaddt as MonthEnd, CIF, max(CL_OBLIGOR_RISK_RATING) as orr1 

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW]

where loaddt in ('{last_12_month_ends1}')

group by loaddt, cif
Section 1: PD Models Override - In this segment data is extracted for overrides per risk template for the evaluation period.
DRR Large Corp
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
DRR Mid Size
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in (  'Innovation > $15MM up to $75MM' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
DRR Early Stage
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
DRR GFB Firm
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
DRR GFB CCLOC
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
DRR GFB NAV
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
Section 2: PD Models Accuracy
#Default Status Data for all Models
SELECT distinct cif, loaddt, default_flag

from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]

			where loaddt > '01-01-2024'
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $15MM up to $75MM')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
