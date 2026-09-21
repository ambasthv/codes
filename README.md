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
