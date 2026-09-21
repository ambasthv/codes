SELECT Supplementary_Data.*, Filtered_Balances.Balance,
		isnull(SEC_UNFUNDED,0) + isnull(SVB_UTILIZED_EXPOSURE_AMT,0) + isnull([Final Payment],0) AS 'Total Commitment', 
		isnull(SEC_UNFUNDED,0) + isnull(SVB_UTILIZED_EXPOSURE_AMT,0) + isnull([Final Payment],0) -  isnull(Balance,0) AS 'Unfunded Commitment'

FROM
	(
	SELECT  Base.LoadDT, [Entity ID], Base.LECE_FLG, Base.UNDRWRTNG_MTHD, Base.CIF, coalesce(CLIENT_LEGAL_NAME, CLIENT_NM) AS 'CLIENT_NM', CUST_LINE_NBR, 
			RISK_BAS_SEG_CD AS 'RBS Code', FACILITY_TYPE, Facility_Type_DESC, Lifestage, Risk_CD, Base.CL_OBLIGOR_RISK_RATING, Base.FINAL_LGD, Base.DUAL_RISK_RATING, NICHECD, portfolio_segment AS 'segment', BUSINESS_UNIT,
			BP_FLAG,
			Sales_Niche, 
			SEC_UNFUNDED, SVB_UTILIZED_EXPOSURE_AMT 
				

	FROM CRDADMPRD.dbo.CDM_CREDIT_LINES_VIEW Base 

	LEFT JOIN CRDADMPRD.dbo.REF_FACILITY_TYPE Facility_Table
	ON Facility_Table.FACILITY_TYPE_CD = Base.facility_type

	LEFT JOIN 
		(
		SELECT LoadDT, CLIENT_RELATIONSHIP_ENTITYID AS 'Entity ID', CIF, TEAMCODE
		FROM CRDADMPRD.dbo.CDM_CLIENTS
		WHERE 1 = 1
			AND CLIENT_RELATIONSHIP_ENTITYID is NOT NULL
			AND (
			LoadDT = '{last_month_end1}')
		)
	Entity_Table
	ON 1 =1 
		AND Entity_Table.LoadDT = Base.LoadDT 
		AND Entity_Table.CIF = Base.CIF

	LEFT JOIN 
	(
	SELECT team_code, portfolio_segment
	FROM 
		(
		SELECT *, ROW_NUMBER () OVER (PARTITION BY team_code ORDER BY create_date DESC) AS 'Ranking'
		FROM [CRDADMANALYSIS].[dbo].[ref_portfolio_segment_bk_20250105_OBSOLETE]
		)
		Segment_Rankings
		WHERE Ranking = 1
	) Portfolio_Segments
	ON Portfolio_Segments.team_code = Entity_Table.TEAMCODE

	LEFT JOIN ---not joining this qualitative data on CDM_CREDIT_LINES date. (using the max date for both; the dates don't match)
	(
	SELECT distinct Entity_Id, Sales_Niche, Sales_Sector, SCO_Name
	FROM CRDADMPRD.dbo.CDM_ENTITY_RELATIONSHIP
	WHERE 1 = 1
		AND LoadDT = (SELECT max(LoadDT) FROM CRDADMPRD.dbo.CDM_ENTITY_RELATIONSHIP WHERE DATEPART(dw, LoadDT) NOT IN (1, 7))
		AND (Sales_Niche is NOT NULL AND Sales_Sector is NOT NULL AND SCO_NAME is NOT NULL) 
	) Qualitative_Data
	ON Qualitative_Data.Entity_Id = Entity_Table.[Entity ID]

	LEFT JOIN
		(
			SELECT *
			FROM 
				(
				SELECT LoadDT AS 'Client Date', CIF AS 'Client CIF', CLIENT_LEGAL_NAME, 
						row_number () OVER (PARTITION BY LoadDT, CIF ORDER BY BP_FLAG ASC) AS 'Priority'
				FROM CRDADMPRD.dbo.CDM_CLIENTS_VIEW
				) Step_1
			WHERE Priority = 1
		) Clients

	ON 1 = 1
		AND Clients.[Client Date] = Base.LoadDT
		AND Clients.[Client CIF] = Base.CIF

				--------------------------

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'Cust_Line_NBR'
			) Exclusions_1

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_1.qtr_start_date
				AND Base.LoadDT < Exclusions_1.next_qtr_end_date
				AND Base.Cust_Line_NBR = Exclusions_1.exclusion_value

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'BUSINESS_UNIT'
			) Exclusions_2

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_2.qtr_start_date
				AND Base.LoadDT < Exclusions_2.next_qtr_end_date
				AND Base.BUSINESS_UNIT = Exclusions_2.exclusion_value

			--------------------------

	WHERE 1 =1 
		AND (Base.LoadDT = '{last_month_end1}')

		AND Exclusions_1.Flag IS NULL
		AND Exclusions_2.FLAG IS NULL

		AND (UPPER(LINE_STATUS) != 'EXPIRED' OR (UPPER(LINE_STATUS) = 'EXPIRED' AND SVB_UTILIZED_EXPOSURE_AMT > 0 )) 
	)
	Supplementary_Data

LEFT JOIN  
	(
	SELECT LoadDT, CUST_LINE_NBR, 
		   sum(isnull(NOTEPRNCPLBALNET,0) + isnull(LOAN_FEES_RECEIVABLE_AMT,0)) AS 'Balance',
		   sum(isnull(LOAN_FEES_RECEIVABLE_AMT,0)) AS 'Final Payment'

	FROM CRDADMPRD.dbo.CDM_INSTRUMENTS_VIEW Base

				--------------------------

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'ACCTNBR'
			) Exclusions_1

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_1.qtr_start_date
				AND Base.LoadDT < Exclusions_1.next_qtr_end_date
				AND Base.ACCTNBR = Exclusions_1.exclusion_value

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'BUSINESS_UNIT'
			) Exclusions_2

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_2.qtr_start_date
				AND Base.LoadDT < Exclusions_2.next_qtr_end_date
				AND Base.BUSINESS_UNIT = Exclusions_2.exclusion_value

			--------------------------

	WHERE 1 =1 
		AND CUST_LINE_NBR is NOT NULL

		AND applid not in ('MUNI','CORP')	
		AND isnull(status_cd,'None') <>'Inactive'

		AND left(isnull(LOAN_TYPE,0),1) <>'4'	
		AND Exclusions_1.Flag IS NULL
		AND Exclusions_2.Flag IS NULL
		
	GROUP BY  LoadDT, CUST_LINE_NBR
	)
Filtered_Balances 

ON 1 = 1
	AND Supplementary_Data.LoadDT = Filtered_Balances.LoadDT 
	AND Supplementary_Data.CUST_LINE_NBR = Filtered_Balances.CUST_LINE_NBR
select distinct a.cif,b.DATE_APPROVED , a.RISK_GRADE_TEMPLATE, a.DIFFERENCE_OF_CALC_AND_FINAL_ORR

from  [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a  join 

[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
a.credit_req_nbr = b.CREDIT_REQ_NBR
where a.RISK_GRADE_TEMPLATE is not null
and b.CREDIT_REQ_STATUS = 'Booked'
SET NOCOUNT ON

select 

        a.cif_crm, 
        b.maxdate, 
        a.statementid,   
        a.statementmonths, 
        a.statementtype, 
        a.NETSALES

        into #temp1

        from    [CRDADMPRD].[dbo].[CDM_CLIENT_FINANCIALS_VW] a

        join (select cif_crm, max(statementdate) as maxdate from 
        [CRDADMPRD].[dbo].[CDM_CLIENT_FINANCIALS_VW] group by cif_crm) b

        on a.cif_crm = b.cif_crm and a.statementdate = b.maxdate

        where a.cif_crm in ('{statement_cif}')
        and a.statementdate > '01-01-2020';

WITH RankedRecords AS (
    SELECT
        cif_crm, 
        maxdate, 
        statementid,   
        statementmonths, 
        statementtype, 
        NETSALES,      
        
        ROW_NUMBER() OVER (PARTITION BY cif_crm, maxdate ORDER BY statementid DESC) as rn
    FROM
        #temp1

        )

        SELECT
    cif_crm, 
        maxdate, 
        statementid,  
        statementmonths, 
        statementtype, 
        NETSALES, 
        rn
    
FROM
    RankedRecords
WHERE
    rn = 1;

drop table #temp1 
