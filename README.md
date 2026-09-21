```sql
-- Portfolio Data for ORR for each Month End in 45M Evaluation Period

SET NOCOUNT ON

select  loaddt as MonthEnd, CIF, max(CL_OBLIGOR_RISK_RATING) as orr1 

from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW]

where loaddt in ('{last_45_month_ends1}')

group by loaddt, cif


-- PD Models Override - Large Corp

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
'Innovation > $75MM & Sponsor – ID/BS')	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and b.CREDIT_REQ_STATUS = 'Booked'
and a.cif is not null


-- PD Models Override - Mid Size

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in (  'Innovation > $15MM up to $75MM' )	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and b.CREDIT_REQ_STATUS = 'Booked'
and a.cif is not null


-- PD Models Override - Early Stage

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'Innovation up to $15MM' )	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and b.CREDIT_REQ_STATUS = 'Booked'
and a.cif is not null


-- PD Models Override - GFB Firm

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'GFB Firm' )	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and b.CREDIT_REQ_STATUS = 'Booked'
and a.cif is not null


-- PD Models Override - GFB CCLOC

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'CCLOC' )	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and b.CREDIT_REQ_STATUS = 'Booked'
and a.cif is not null


-- PD Models Override - GFB NAV

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'NAV' )	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and b.CREDIT_REQ_STATUS = 'Booked'
and a.cif is not null


-- DRR Large Corp Default Pull

SET NOCOUNT ON
    
select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template				
				
into #temp1				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 'Innovation > $75MM & Sponsor – ID/BS')				
				
--and b.DATE_APPROVED > '{month_end_12m_prior}'
and a.cif is not null
and b.CREDIT_REQ_STATUS = 'Booked'

SELECT distinct g.*, h.load_date, h.default_flag
 
FROM #temp1 g 

left join 

(select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
group by cif, default_flag) h

on g.cif = h.cif

drop table #temp1, #temp2


-- DRR Mid Size Default Pull

SET NOCOUNT ON

select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
    a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template				
				
into #temp4				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'Innovation > $15MM up to $75MM')				
				
--and b.DATE_APPROVED > '{month_end_12m_prior}'
and a.cif is not null
and b.CREDIT_REQ_STATUS = 'Booked'

select #temp4.*

into #temp5 
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp4
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp4 

on max_date_per_cif.Date_CIF = #temp4.date_approved
and max_date_per_cif.cif = #temp4.cif

SELECT distinct g.*, h.load_date, h.default_flag
 
FROM #temp5 g 

left join 

(select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
group by cif, default_flag) h

on g.cif = h.cif

drop table #temp4, #temp5


-- DRR Firm Default Pull

SET NOCOUNT ON

select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
    a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template				
				
into #temp4				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'GFB Firm')				
				
--and b.DATE_APPROVED > '{month_end_12m_prior}'
and a.cif is not null
and b.CREDIT_REQ_STATUS = 'Booked'

select #temp4.*

into #temp5 
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp4
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp4 

on max_date_per_cif.Date_CIF = #temp4.date_approved
and max_date_per_cif.cif = #temp4.cif

SELECT distinct g.*, h.load_date, h.default_flag
 
FROM #temp5 g 

left join 

(select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
group by cif, default_flag) h

on g.cif = h.cif

drop table #temp4, #temp5


-- DRR CCLOC Default Pull

SET NOCOUNT ON

select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR,a.OVERRIDE_COMMENTS, a.risk_grade_template				
				
into #temp7				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'CCLOC')	

--and b.DATE_APPROVED > '{month_end_12m_prior}'
and a.cif is not null
and b.CREDIT_REQ_STATUS = 'Booked'

select #temp7.*

into #temp8
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp7
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp7 

on max_date_per_cif.Date_CIF = #temp7.date_approved
and max_date_per_cif.cif = #temp7.cif

SELECT distinct g.*, h.load_date, h.default_flag
 
FROM #temp8 g 

left join 

(select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
group by cif, default_flag) h

on g.cif = h.cif

drop table #temp7, #temp8


-- DRR Early Stage Default Pull

SET NOCOUNT ON

select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
    a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template				
				
into #temp1				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'Innovation up to $15MM')				
				
--and b.DATE_APPROVED > '{month_end_12m_prior}'
and a.cif is not null
and b.CREDIT_REQ_STATUS = 'Booked'

select #temp1.*

into #temp2 
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp1
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp1 

on max_date_per_cif.Date_CIF = #temp1.date_approved
and max_date_per_cif.cif = #temp1.cif

SELECT distinct g.*, h.load_date, h.default_flag
 
FROM #temp2 g 

left join 

(select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
group by cif, default_flag) h

on g.cif = h.cif

drop table #temp1, #temp2


-- DRR NAV Default Pull

SET NOCOUNT ON

select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR,a.OVERRIDE_COMMENTS, a.risk_grade_template				
				
into #temp10				
				
from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join 				
     [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
     a.credit_req_nbr = b.CREDIT_REQ_NBR
				
and a.risk_grade_template in ( 'NAV')				
				
--and b.DATE_APPROVED > '{month_end_12m_prior}'
and a.cif is not null
and b.CREDIT_REQ_STATUS = 'Booked'

select #temp10.*

into #temp11 
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp10
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp10

on max_date_per_cif.Date_CIF = #temp10.date_approved
and max_date_per_cif.cif = #temp10.cif

SELECT distinct g.*, h.load_date, h.default_flag
 
FROM #temp11 g 

left join 

(select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
group by cif, default_flag) h

on g.cif = h.cif

Drop table #temp10, #temp11
```

Sources
