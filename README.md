SQL Query 1: Extracting data from following tables:
Credit Lens Staging Table
Default Flag Table
GL Table (for Balances and Loan Level Info)
select eomonth(cast(z.statementdate as date)) as loaddt,
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
SQL Query 2 for creating a separate table with default data and loan level data
Data sourced from:
Default Flag Table
GL Table (for Balances and Loan Level Info)
SELECT def.cif as cif_def, def.first_def_date, def.def_rbs_min, def.def_rbs_max,
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
SQL Query 3 to source RBS for the Credit Lens Statement Date
Data sourced from:
Credit Lens Staging Table
Default Flag Table
SELECT z.CIF_CRM, RIGHT('00000' + z.CIF_CRM,9) as cif_pad, 
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
SQL Query to pull GLV Data for date range 2020 to present.
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
Importing Financial Data and Rank Ordering
select eomonth(cast(z.statementdate as date)) as loaddt,
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
Query to extract data for Sponsor Finance Clients
SELECT a.cif, max(a.client_aoteamcd) as spteam_code, a.loaddt
            FROM CRDADMPRD..GLV_Historical_DW_Gross_Loans_Adjusted AS a
            WHERE
            a.facility_type != 'GUD'
            AND
            a.loaddt >= '{month_end_24m_prior}' 
            GROUP BY a.cif, a.loaddt
            having max(a.client_aoteamcd) in ('38B','38C','58A','58B','58C','86A','86B','86C','86D','86E','90E')
Default Data
select x.cif as CIF_Default
,eomonth(x.loaddt) as LOADDT_def
,x.default_flag as defflag
,x.risk_cd as mcrr
,x.risk_bas_seg_cd as elseg
from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW] x
where eomonth(x.loaddt) > '{month_end_24m_prior}'
