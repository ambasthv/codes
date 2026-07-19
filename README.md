
# GL / Financial Reporting Interview Question Bank

**How to use this guide**
- Each JD line has 5 questions, labeled A (easiest) → E (hardest).
- A–B suit freshers (definitions, core concepts). C is a "walk me through the process" question good for both. D–E are scenario/judgment questions best suited to experienced candidates.
- For freshers, it's fine if D/E answers are incomplete — listen for sound reasoning, not a textbook answer.

---

## General Ledger Processing

### 1. Prepare and post GL monthly journal entries with supporting documentation for a clear audit trail

**1A.** What is a journal entry, and what should every JE include to be audit-ready?
*Answer:* A JE records a financial transaction with debit/credit lines. A complete JE includes date, account codes, amount, description/narrative, and reference to supporting documents (invoice, contract, calculation sheet). Example: an accrual JE referencing the accrual workbook and an approval email as backup.

**1B.** What does "audit trail" mean, and why does it matter?
*Answer:* It's the chain of documentation letting someone trace a reported number back to its source transaction. It matters because auditors/regulators need to verify entries are legitimate and correctly recorded. Example: if a $50,000 accrual is questioned, the audit trail should let you pull the JE, the supporting calc, and the approval within minutes.

**1C.** Walk me through the steps to prepare and post a manual JE.
*Answer:* Gather transaction detail and support, calculate the amount, prepare the JE with correct account codes, get it reviewed/approved per the approval matrix, post it, and file the support for retrieval. Example: a rent accrual — pull the lease, calculate the month's portion, get sign-off, post before the close deadline.

**1D.** You're close to the JE deadline and haven't received final supporting documentation from a business partner. What do you do?
*Answer:* Post a well-reasoned estimate (e.g., based on prior month trend), clearly flag it as an estimate pending true-up, and follow up to true-up once actuals arrive. Example: accrue based on last month's invoice amount, noting "estimate — to true up next period" in the JE description.

**1E.** You find an error in a JE posted after books were closed. How do you handle it, and how do you prevent recurrence?
*Answer:* Assess materiality; correct in the current period with a clear note if immaterial, or follow the formal correction/restatement policy and notify management if material. Then find the root cause and fix the process, e.g., adding a mandatory secondary review. Example: a duplicate accrual corrected via reversal, plus a duplicate-check step added to the close checklist.

### 2. Coordinate with AR/business teams on revenue accrual and deferral journals; ensure revenue recognition per accounting standards

**2A.** What's the difference between accrued and deferred revenue?
*Answer:* Accrued revenue is earned but not yet billed/received; deferred revenue is cash received before it's earned. Example: interest earned in March but billed in April is accrued; an annual fee paid upfront and recognized monthly is deferred.

**2B.** Which standard governs revenue recognition, and what's its core principle?
*Answer:* ASC 606 (US GAAP); revenue is recognized when control of a good/service transfers to the customer, for the amount the entity expects to be entitled to. Example: a set-up fee bundled with a 12-month service contract may need to be recognized over the contract term rather than upfront.

**2C.** How would you calculate a revenue accrual for a banking fee product where the invoice hasn't been issued yet?
*Answer:* Use the fee schedule and activity data from the business team to estimate the amount earned, post an accrual JE, and reverse it once the actual invoice books. Example: wire transfer fee accrual = number of wires processed × per-wire fee.

**2D.** A business team gives you inconsistent data for a deferral calculation. How do you validate it before posting?
*Answer:* Cross-check against a second source (contract terms, prior month, sub-ledger), ask clarifying questions, and don't post until the numbers tie out or the difference is documented. Example: comparing the deferral schedule to the original contract value to catch a data entry error.

**2E.** Business wants to recognize revenue upfront for commercial reasons, but you believe ASC 606 requires it over time. How do you handle it?
*Answer:* Explain the accounting requirement and misstatement risk, involve technical accounting for a formal position if needed, and hold the GAAP-compliant line regardless of business pressure. Example: escalating to technical accounting with the contract so a documented position memo settles the treatment.

### 3. Loan and treasury accounting: interest accruals, loan/debt amortization, true-ups, equity/stock/bond purchase accounting

**3A.** How is interest accrual calculated on a loan?
*Answer:* Principal × interest rate × (days elapsed / days in year), using actual/360 or actual/365 per the loan agreement. Example: $1,000,000 × 6% × (30/360) = $5,000 accrued.

**3B.** Explain the effective interest rate (EIR) method for loan/debt amortization.
*Answer:* EIR spreads fees, premiums, or discounts over the loan's life so recognized interest reflects a constant rate on the carrying amount, rather than straight-line. Example: an origination fee is spread over the term, gradually increasing the effective yield recognized versus the stated rate.

**3C.** What is a "true-up" entry — walk through an example.
*Answer:* An adjustment matching a prior estimated accrual to the actual amount once known. Example: $10,000 interest was accrued as an estimate, actual statement shows $10,450 — post a $450 true-up.

**3D.** How do you account for premium/discount amortization on a bond purchase?
*Answer:* A premium (bought above face value) is amortized down over the bond's life, reducing interest income; a discount is amortized up, increasing it — typically via the effective interest method. Example: a bond bought at 102 has its carrying value reduced toward 100 by maturity, offsetting part of the coupon income.

**3E.** Explain the accounting differences between held-to-maturity (HTM), available-for-sale (AFS), and trading securities.
*Answer:* HTM stays at amortized cost with no fair value adjustments; AFS is marked to fair value with changes in OCI until sold; trading securities are marked to fair value with changes through P&L immediately. Example: the same bond dropping in market price wouldn't hit earnings under HTM, would hit OCI under AFS, and would hit P&L under trading classification.

### 4. Warrant accounting: new warrant setup, valuation/volatility, pricing updates, income reporting, IPO tracking, gain-loss analysis

**4A.** What is a warrant in a banking context (e.g., venture lending)?
*Answer:* A right, often given to a lender alongside a startup loan, to purchase equity (usually preferred stock) at a set strike price later. Example: a bank lending to a startup receives a warrant for 10,000 shares at a $1 strike.

**4B.** What inputs are needed to value a warrant, e.g., via Black-Scholes?
*Answer:* Underlying share price, strike price, time to expiration, risk-free rate, and volatility. Example: for a private company, volatility is often estimated from comparable public companies since there's no trading history.

**4C.** Walk through how you'd set up a newly received warrant in the system.
*Answer:* Enter the terms (issuer, shares, strike, expiration, grant date) from deal documents, run the initial valuation, book the initial fair value entry, and set it up for recurring revaluation. Example: entering a warrant from a Q3 loan closing and running its first valuation before month-end.

**4D.** How does an IPO event affect warrant valuation and tracking?
*Answer:* Once public, the warrant can be revalued using the observable market price instead of a modeled private valuation, and tracking shifts toward exercise/sale/expiration around lock-up. Example: replacing the modeled private-company volatility with the stock's actual trading volatility post-IPO.

**4E.** How would you perform a gain/loss analysis on a warrant portfolio and report it?
*Answer:* Compare each warrant's current fair value to its prior value/cost basis, split realized (exercised/sold) from unrealized (mark-to-market) gains, and roll up portfolio-level results with commentary on key drivers. Example: reporting that unrealized gains rose mainly from two portfolio companies' post-IPO price appreciation.

### 5. Run preliminary trial balance and trending reports, perform variance analysis

**5A.** What is a trial balance used for?
*Answer:* It lists all GL account balances to confirm debits equal credits and gives a snapshot before finalizing financials. Example: running a preliminary TB mid-close to spot an unusually high account before books lock.

**5B.** Why perform variance analysis before final close?
*Answer:* It catches errors or unusual activity early enough to investigate and correct before numbers are reported externally. Example: spotting a 300% jump in an expense account and tracing it to a duplicate JE before the deadline.

**5C.** Walk through investigating an unexpected variance versus last month.
*Answer:* Pull the transaction detail behind both periods, identify what drove the change, determine if it's one-time or a trend, and confirm with the business owner if needed. Example: a variance traced to a single large true-up entry that explains the whole swing.

**5D.** What typically determines whether a variance needs escalation?
*Answer:* A materiality threshold (dollar and/or % change) set by policy — unexplained variances above threshold get escalated regardless of direction. Example: any variance over $100,000 or 10% that can't be explained same-day gets escalated.

**5E.** How would you design a trending report to proactively catch anomalies across many GL accounts?
*Answer:* Show each account's balance over a rolling 6–12 months with automated flags for balances outside a defined threshold, so reviewers focus only on exceptions. Example: a Python/pandas script computing month-over-month % change per account and auto-highlighting outliers.

### 6. Ensure accuracy and completeness of documents processed

**6A.** What does "completeness" mean in financial documentation?
*Answer:* All required evidence for a transaction is present — approval, calculation, source document — nothing material missing. Example: a JE package missing manager sign-off is incomplete even if the numbers are correct.

**6B.** What quality checks would you run before submitting a JE package?
*Answer:* Confirm debits equal credits, account codes are correct, amounts tie to support, approvals are attached, and the narrative is clear. Example: tie-out check comparing the JE total to the source calculation sheet.

**6C.** How do you ensure supporting documents tie out to the JE amount?
*Answer:* Recalculate or cross-foot the supporting workbook, match line by line to the JE, and document any rounding or timing difference. Example: reconciling a $24,500 accrual JE to a supporting spreadsheet summing to exactly $24,500.

**6D.** You discover a systemic documentation gap affecting multiple entries. What do you do?
*Answer:* Quantify the scope, notify management, and fix both the existing gaps and the underlying process. Example: a recurring accrual template missing an approval field for three months — fix the template and re-collect the missing approvals.

**6E.** How would you build a control/checklist for ongoing accuracy and completeness across a large team?
*Answer:* Standardized JE templates with mandatory fields, a mandatory review step before posting, and a visible close tracker with sign-off status. Example: a shared tracker showing each preparer's JEs as "prepared / reviewed / posted," with posting blocked until reviewed.

### 7. Interact with other teams for open items/issues from book closure activities

**7A.** Why is cross-team communication important during month-end close?
*Answer:* Close is time-boxed and depends on inputs from multiple teams; a delay in one area cascades into others. Example: waiting on a business team's revenue number can hold up the revenue JE and downstream reporting.

**7B.** How would you track and follow up on open items during close?
*Answer:* Maintain an open-items log with owner, due date, and status, and send targeted follow-ups as deadlines near. Example: a shared tracker listing 5 open items, each with owner and expected resolution date.

**7C.** Describe how you'd escalate an unresolved open item close to the deadline.
*Answer:* Notify your manager and the counterpart's manager with a factual summary of issue, impact, and deadline, and propose a fallback (estimate now, true up later). Example: escalating a missing data file two hours before deadline with a proposed estimate-and-true-up plan.

**7D.** How do you balance close deadlines against getting complete information from business teams?
*Answer:* Use well-documented estimates when full info isn't available, and true up next period — completeness of process matters more than waiting indefinitely. Example: booking an estimated accrual flagged "pending true-up" rather than missing the deadline.

**7E.** Describe how you'd handle a close issue requiring two business teams to agree before you can proceed.
*Answer:* Get both teams into a quick joint discussion rather than relaying messages, lay out the requirement and deadline clearly, and drive toward a decision or interim estimate. Example: a fee-allocation dispute resolved via a short call ending in an agreed split, formalized post-close.

---

## Reconciliations

### 8. Reconcile balance sheet accounts, generate reconciliation/certification report

**8A.** What is a balance sheet reconciliation?
*Answer:* Confirming a GL balance is supported by and agrees to an independent source (sub-ledger, bank statement, third-party statement). Example: reconciling the bank GL cash account to the actual bank statement.

**8B.** What are the key components of a reconciliation/certification report?
*Answer:* GL balance, supporting balance, the reconciling difference with explanation, aging of open items, and a preparer/reviewer sign-off. Example: GL $500,000 vs. sub-ledger $498,500, with a $1,500 timing difference explained and aged under 30 days.

**8C.** Walk through reconciling a bank GL account to the sub-ledger.
*Answer:* Pull both balances as of the same date, match transactions line by line, list unmatched/timing items, and document explanations. Example: two outstanding wires identified as the sole reconciling items.

**8D.** What's your approach when a reconciling item can't be explained?
*Answer:* Dig into transaction detail on both sides, involve the relevant ops/business team, and if still unresolved by deadline, flag it as an open item rather than certifying it as clean. Example: escalating an unexplained $2,000 difference to ops while noting "pending investigation."

**8E.** How would you design a certification process treating high-risk and low-risk accounts differently?
*Answer:* More frequent, detailed review and senior sign-off for high-risk/high-judgment accounts; a lighter-touch process for stable, low-risk accounts — driven by materiality and error history. Example: a suspense account reconciled monthly with manager sign-off vs. a stable fixed asset account reconciled quarterly.

### 9. Ensure sub-ledger reconciliations follow procedure and month-end close calendar

**9A.** What is a sub-ledger? Give examples.
*Answer:* A detailed ledger supporting a GL control account — e.g., AR sub-ledger, loan sub-ledger, fixed asset register — whose total should tie to the GL. Example: the loan sub-ledger detail should sum to the GL's total loans receivable.

**9B.** Why must sub-ledger reconciliations follow a close calendar?
*Answer:* Close activities are sequenced and interdependent; missing a scheduled rec date can delay the entire close. Example: the loan sub-ledger rec must complete before the TB is pulled for the close packet.

**9C.** How do you reconcile a sub-ledger total to the GL control account?
*Answer:* Sum the sub-ledger detail, compare to the GL balance, and investigate any difference to specific transactions. Example: a $10,000 difference traced to a manual adjustment posted to GL without a matching sub-ledger update.

**9D.** The sub-ledger and GL are out of sync at month end. What do you do?
*Answer:* Identify the specific transactions causing the break, determine if it's timing or an error, book a correction if needed, and document the item until it clears. Example: a batch interface failure that missed three transactions — post manually and confirm the rec ties out.

**9E.** How would you handle a recurring timing difference between sub-ledger and GL across periods?
*Answer:* If genuinely explainable timing, document it as a standing item each period; if it's growing or unclear, investigate root cause (system interface, process gap) rather than just re-documenting it. Example: raising a system interface issue with IT instead of re-explaining the same $5,000 gap monthly.

### 10. Escalate variances to business for resolution and facilitate resolution

**10A.** What is a reconciling variance?
*Answer:* The unexplained difference between two balances that should otherwise agree, such as GL vs. sub-ledger. Example: a $3,000 unexplained gap between GL cash and the bank statement.

**10B.** What information do you need before escalating a variance?
*Answer:* The exact amount, when it first appeared, what's already been checked, and who owns the likely underlying process. Example: escalating with "GL vs. bank differs by $3,000 since March, not a posting error our side, likely an unrecorded fee."

**10C.** How would you write an escalation note to business about a variance?
*Answer:* State the account, amount, duration, what's already been checked, the deadline, and a specific ask. Example: "AR sub-ledger for Client X shows a $15,000 variance vs. GL since April — can you confirm if this relates to the March credit memo?"

**10D.** Business is unresponsive to a variance escalation near the deadline. What's your approach?
*Answer:* Escalate to both managers, and if still unresolved, book it as an open/unreconciled item per policy rather than leaving it silently unaddressed. Example: flagging the item "unresolved — escalated to management" on the certification instead of certifying it clean.

**10E.** Business repeatedly dismisses a recurring variance as immaterial, but you suspect it's systemic. How do you handle it?
*Answer:* Quantify the trend over several periods to show it's not immaterial in aggregate, and present the data-driven case to management. Example: showing a "small" $2,000/month variance has totaled $24,000 unexplained over the year, prompting a root-cause review.

### 11. Process authorized adjustments and/or write-offs via the JE template

**11A.** What is a write-off?
*Answer:* Removing an asset (like an uncollectible receivable) from the books, recognizing the loss, once it's non-recoverable. Example: writing off a $5,000 receivable from a client that went bankrupt.

**11B.** What approvals are typically required before processing an adjustment or write-off?
*Answer:* Sign-off from the business owner and finance management, per a delegated authority matrix based on dollar thresholds. Example: a $50,000 write-off needs both a business unit head's and a controller's approval; a $500 adjustment needs only supervisor sign-off.

**11C.** Walk through the JE template process for a write-off.
*Answer:* Confirm authorization and policy compliance, complete the JE template with account codes and reference to the approval, get it reviewed, and post with approval documentation attached. Example: attaching the signed write-off approval email as JE backup.

**11D.** How do you ensure segregation of duties when processing adjustments?
*Answer:* The requester/authorizer shouldn't be the poster, and posting requires independent review. Example: a business analyst requests a write-off; a different finance team member reviews and posts it.

**11E.** Describe controls you'd implement to prevent unauthorized adjustments from being processed.
*Answer:* System-enforced approval workflows blocking posting without approval on file, an authority matrix by threshold, and periodic audit sampling of posted adjustments against approvals. Example: the GL system technically rejecting a write-off JE above $10,000 without a matching approval record.

---

## Financial & Regulatory Reporting

### 12. Creation of close packet: extract financial reports, management reports, trial balance, financial statements post-close

**12A.** What is a close packet and what does it typically include?
*Answer:* The compiled outputs from month-end close — TB, financial statements (P&L, balance sheet), management reports, and supporting schedules. Example: a packet with TB, income statement, balance sheet, and variance commentary.

**12B.** What's the difference between financial statements and management reports?
*Answer:* Financial statements follow standardized formats for external/regulatory use; management reports are internally tailored (e.g., by product line) for business decisions. Example: a management report breaking revenue down by banking product, unlike the formal income statement.

**12C.** Walk through compiling a close packet after period close.
*Answer:* Confirm the TB is final, extract each required report, cross-check totals tie between reports, add commentary, and distribute per the close calendar. Example: pulling TB, P&L, and balance sheet from the same closed period and confirming net income matches across both.

**12D.** How do you ensure the close packet ties to the trial balance with no discrepancies?
*Answer:* Cross-foot each report's totals against the TB before distribution; trace any discrepancy to a timing or mapping error and correct. Example: catching that the balance sheet was pulled before a late JE posted, then regenerating it.

**12E.** How would you streamline or automate the close packet creation process?
*Answer:* Standardize report templates and pull logic, e.g., a script that extracts and formats reports directly from the system, cutting manual copy-paste errors. Example: a Python script pulling the TB, auto-generating standard formats, and flagging any report that doesn't tie before distribution.

### 13. Review prior period's financial reporting process/data for MoM comparison and commentary, identify process changes

**13A.** What is month-on-month (MoM) analysis?
*Answer:* Comparing the current period's figures to the immediately prior period to spot trends or anomalies. Example: comparing this month's interest expense to last month's to explain a 15% increase.

**13B.** Why review the prior period's reporting process, not just the numbers?
*Answer:* Reviewing process surfaces inefficiencies or recurring errors that number comparison alone wouldn't reveal. Example: noticing a report required three manual reformatting steps that could be automated.

**13C.** How would you write commentary explaining a significant MoM variance?
*Answer:* State the amount/percentage, identify the specific driver with supporting data, and note if it's one-time or expected to continue. Example: "Fee income increased $200K (12%) MoM, driven by a one-time volume spike; not expected to recur next month."

**13D.** What process improvements might you identify from reviewing prior period reporting?
*Answer:* Manual steps that could be templated/automated, recurring last-minute data requests that could be scheduled earlier, or report formats needing rework. Example: moving a standing data request two days earlier after it caused delays for three straight months.

**13E.** How would you implement a reporting process change without disrupting the current close cycle?
*Answer:* Pilot it in a low-risk area or run it in parallel with the old process for one cycle before fully switching over. Example: testing an automated variance report alongside the manual one for one month before retiring the manual version.

### 14. Update financial reporting with supplemental financial information received from business

**14A.** What is supplemental financial information? Give examples.
*Answer:* Additional data not captured directly in the GL but needed for complete reporting — e.g., off-system schedules or manually tracked metrics. Example: a business team's manually tracked loan commitment schedule not yet in the core system.

**14B.** How do you validate supplemental info before incorporating it into reports?
*Answer:* Cross-check against a known total or prior period for reasonableness, confirm it's from an authorized source, and clarify anything that looks off. Example: comparing a supplemental commitment figure to last month's to catch a stale or duplicate file.

**14C.** Walk through updating a report with late supplemental data.
*Answer:* Confirm validity and cut-off relevance, incorporate with a clear note on source and timing, and re-validate totals tie after the update. Example: adding a late warrant valuation update and flagging it was received after the initial draft.

**14D.** Supplemental info contradicts previously reported numbers. What do you do?
*Answer:* Investigate which figure is correct via source documentation, don't silently overwrite prior numbers, and follow the proper correction process if a revision is needed. Example: finding the new figure reflects a post-report business update, requiring a documented revision note.

**14E.** How would you build a control to track and log supplemental info updates for audit purposes?
*Answer:* Maintain a log of what changed, source, date received, approver, and impact — so any number can be traced back to why and when it changed. Example: "Row 45, Commitment amount, updated $2M→$2.3M, source: [email], approved by [name]."

### 15. Validate quality of reports via data validation, trend analysis, variance analysis; escalate business attention items

**15A.** What is data validation in reporting?
*Answer:* Checking report data is accurate, complete, and internally consistent before finalizing — totals tie, no blank critical fields, figures within expected ranges. Example: confirming a report's total row equals the sum of its line items before submission.

**15B.** What's the difference between trend analysis and variance analysis?
*Answer:* Trend analysis tracks a metric across multiple periods for a pattern; variance analysis compares two specific periods (or actual vs. budget) to quantify a difference. Example: trend analysis shows expenses steadily rising over 6 months; variance analysis explains why this month jumped 8% vs. last.

**15C.** Walk through validating a regulatory report before submission.
*Answer:* Reconcile figures back to the GL/TB, check prior-period comparatives for consistency, apply regulator-specific edit checks, and get a second reviewer's sign-off. Example: confirming total assets in the regulatory report matches the balance sheet before submission.

**15D.** What criteria determine whether an anomaly needs escalation vs. just noting?
*Answer:* Materiality, whether it affects an externally reported/regulatory number, and whether the cause is understood — unexplained + material + external-facing means immediate escalation. Example: a small internal rounding difference is just noted; an unexplained variance in a regulatory submission is escalated immediately.

**15E.** How would you design an automated validation framework to catch reporting errors before submission?
*Answer:* Build rule-based checks (totals tie, no missing fields, values within historical range) that run automatically and flag exceptions before human sign-off, rather than relying on manual eyeballing. Example: a script flagging any line item deviating more than 2 standard deviations from its 12-month average.

### 16. Production of regulatory reports for US Federal Reserve, FDIC submissions

**16A.** What are the Federal Reserve and FDIC, and why do banks report to them?
*Answer:* The Fed is the US central bank and a bank regulator; the FDIC insures deposits and monitors bank safety/soundness. Banks report so regulators can supervise capital adequacy and risk. Example: quarterly submissions confirm a bank holds sufficient capital relative to its risk profile.

**16B.** Name common regulatory reports banks submit.
*Answer:* The Call Report (FFIEC 031/041) to the FDIC/Fed/OCC, and the FR Y-9C to the Fed for bank holding companies, both summarizing financial condition. Example: the Call Report includes detailed schedules on loans, deposits, and capital ratios.

**16C.** Walk through preparing a regulatory report submission.
*Answer:* Extract data from GL/sub-ledgers per the report's schedule definitions, map to the regulator's line items, validate figures tie to internal financials, get sign-offs, and submit by deadline. Example: mapping GL loan balances into the correct Call Report loan category.

**16D.** What controls ensure accuracy and timeliness of regulatory submissions?
*Answer:* A prep/review timeline working back from the deadline, independent review before submission, and reconciliation of report totals to the GL. Example: requiring the Call Report be reconciled to the TB and reviewed by a second preparer two days before filing.

**16E.** You discover an error in a regulatory report after submission. What do you do?
*Answer:* Assess materiality, notify management/compliance immediately, and follow the formal amended-filing process — regulatory errors carry compliance risk beyond a normal accounting fix. Example: filing an amended Call Report and documenting the root cause after finding a misclassified loan category.

### 17. Respond to queries on reports, facilitate additional reporting information to stakeholders and auditors

**17A.** What kind of queries might auditors typically raise?
*Answer:* Requests to explain variances, support for judgmental estimates, and evidence a balance ties to underlying documentation. Example: an auditor asking for support behind a warrant valuation assumption.

**17B.** How do you prepare to respond to an auditor's request for supporting data?
*Answer:* Pull the exact documentation referenced, ensure it's complete and self-explanatory, and provide it with a brief cover note. Example: sending the accrual calculation workbook with a short methodology explanation.

**17C.** Walk through responding to a stakeholder query about a variance.
*Answer:* Understand exactly what's being asked, pull the specific driver from your analysis, and respond clearly and concisely with the supporting number. Example: responding to "why did opex jump?" with the specific line item and cause, not a vague summary.

**17D.** How do you manage multiple simultaneous audit/stakeholder requests under time pressure?
*Answer:* Triage by deadline and complexity, communicate realistic timelines upfront, and knock out quick ones first. Example: telling an auditor a complex request needs until tomorrow while answering two simpler queries same-day.

**17E.** An auditor's query reveals a genuine reporting error. How do you handle it?
*Answer:* Acknowledge it transparently, quantify the impact, and work with management on the correction and any disclosure — obscuring a finding damages credibility more than the error itself. Example: confirming the error, providing the corrected figure and root cause, and proposing a process fix in the same response.

### 18. Support ad-hoc analysis and reporting

**18A.** What is ad-hoc analysis?
*Answer:* Analysis requested outside standard recurring reporting to answer a specific one-off business question. Example: a one-time request to break down loan losses by industry sector for a presentation.

**18B.** What tools would you use for a quick ad-hoc financial analysis?
*Answer:* Excel for quick pivots/lookups; Python (pandas) or SQL for larger or more complex/repeatable analysis. Example: pandas to segment a large loan portfolio by risk grade, vs. a quick Excel pivot for a small dataset.

**18C.** Walk through approaching a same-day request for an unusual ad-hoc report.
*Answer:* Clarify exactly what's needed and by when, identify the fastest reliable data source, build the analysis, and sanity-check output against a known number before sending. Example: confirming whether gross or net figures are needed before starting, to avoid rework.

**18D.** How do you balance ad-hoc requests against BAU close deadlines?
*Answer:* Communicate honestly about capacity and prioritize by urgency; flag genuine trade-offs to your manager rather than silently deprioritizing close work. Example: telling a stakeholder an ad-hoc request will be ready the day after close rather than rushing and risking a close error.

**18E.** Describe a complex ad-hoc analysis you'd build from scratch with limited specifications.
*Answer:* Clarify the actual business question behind the request, scope the data needed and available, build iteratively, and validate before presenting. Example: a request to "analyze portfolio risk trends" clarified into delinquency rate trends by borrower segment over 12 months.

---

## Financial Modelling

### 19. Draft and maintain documents related to modelling methodology and governance

**19A.** What is model governance, and why does it matter in banking?
*Answer:* The framework of policies, documentation, and oversight ensuring models are developed, validated, and used appropriately — flawed models can drive bad risk/capital decisions and regulatory scrutiny. Example: requiring every model to have an owner, documented methodology, and periodic independent validation.

**19B.** What should a model methodology document include?
*Answer:* The model's purpose, inputs/data sources, statistical approach, key assumptions and limitations, and validation results. Example: a credit risk model doc explaining segmentation logic and a known limitation like limited data for a new product line.

**19C.** Walk through documenting a change in model methodology.
*Answer:* Describe the prior approach, the change and why, the impact on outputs, and get it reviewed/approved per governance policy before implementation. Example: documenting a shift from a flat to a segmented assumption, with before/after output comparison.

**19D.** How does model governance align with regulatory expectations like SR 11-7?
*Answer:* SR 11-7 expects independent validation, clear documentation, ongoing monitoring, and defined roles between developers and validators — governance documentation is what evidences this to regulators. Example: maintaining a model inventory with validation status, as regulators would review during an exam.

**19E.** A model undergoing revalidation gets findings. How would you update the documentation?
*Answer:* Document the findings, the remediation plan and timeline, and update the methodology doc once changes are implemented, keeping a clear issue-to-resolution trail. Example: logging an outdated-assumption finding as "in progress" until the recalibrated assumption is documented and approved.

### 20. Support the maintenance and re-calibration of models

**20A.** What does "model recalibration" mean?
*Answer:* Updating a model's parameters using more recent data so it continues to reflect current conditions. Example: updating a credit loss model's default rate assumptions using the latest year of loan performance data.

**20B.** Why do models need periodic recalibration?
*Answer:* Underlying relationships and conditions change over time, so a model on old data can drift from reality if not refreshed. Example: a model calibrated pre-recession may understate risk without recalibration on more recent, higher-default-rate data.

**20C.** Walk through recalibrating a model's parameters using updated data.
*Answer:* Collect and clean updated data, re-estimate parameters using the model's methodology, compare new vs. old parameters/outputs, and document/get approval before implementing. Example: re-running a regression with an additional year of data and comparing coefficients.

**20D.** How would you test whether a recalibrated model outperforms the previous version?
*Answer:* Use out-of-sample or back-testing to compare predictive accuracy between old and new calibration on the same holdout data. Example: back-testing both versions against last year's actual defaults and comparing which was closer.

**20E.** New data introduces a structural break during recalibration. How do you handle it?
*Answer:* Investigate whether pre-break data should still be included, weighted differently, or excluded, since blending different regimes can distort parameters — this needs judgment and discussion with model risk stakeholders. Example: deciding whether to exclude a pandemic-period spike from a "normal" recalibration or model it separately.

### 21. Support data collation and analysis for modelling

**21A.** Why is data quality important for models?
*Answer:* A model is only as good as its inputs — errors, gaps, or bias in the data lead to unreliable outputs regardless of methodology soundness. Example: a credit model built on incomplete income data for one borrower segment underperforms for that segment.

**21B.** What steps ensure data used for modelling is clean and representative?
*Answer:* Check for missing values, duplicates, and outliers; validate against an independent source; confirm the sample represents the population the model will be applied to. Example: confirming a sample's industry mix roughly matches the actual portfolio's mix before training a model.

**21C.** Walk through using pandas to prepare a dataset for a credit risk model.
*Answer:* Load and inspect for nulls/dtypes, handle missing values (impute or drop based on materiality), treat outliers, and bucket continuous variables into risk segments — e.g., `pd.qcut()` for equal-population quantile bins, or `pd.cut()` for fixed thresholds. Example: using `pd.qcut()` on a debt-to-income column to create risk deciles, watching for duplicate bin edges on skewed data.

**21D.** How would you handle missing or outlier data in a modelling dataset?
*Answer:* For missing data, choose exclusion, imputation, or a "missing" flag based on how much is missing and whether it's random; for outliers, investigate if they're genuine or errors before capping, winsorizing, or excluding — and document the treatment chosen. Example: winsorizing a ratio at the 1st/99th percentile while explicitly disclosing that treatment in the output.

**21E.** Describe how you'd identify and correct a data bias affecting model output.
*Answer:* Compare model performance across sub-segments to see if errors concentrate in one group, trace it to a data collection or representativeness gap, and correct via sample adjustment, added features, or re-weighting. Example: finding a model underperforms for a newer loan product due to training data mostly from an older product, then supplementing the dataset.

---

## Internal Control and Accounting Compliance

### 22. Maintain documents relating to accounting compliance (SOX) and internal controls

**22A.** What is SOX (Sarbanes-Oxley) and why does it matter for accounting?
*Answer:* US legislation requiring public companies to maintain and document effective internal controls over financial reporting (ICFR), aiming to prevent fraud and ensure reliable statements. Example: SOX requires documented evidence a JE review control was actually performed each month, not just that a policy exists.

**22B.** What is an internal control? Give an example relevant to GL processing.
*Answer:* A process or check designed to prevent or detect errors/fraud in financial reporting. Example: a control requiring a second person to review and approve every JE above a set dollar threshold before posting.

**22C.** Walk through documenting a control for a JE approval process.
*Answer:* Describe the control objective, who performs it, how often, what evidence is retained, and how it's tested — clear enough for someone unfamiliar to verify it. Example: "All JEs >$25,000 require manager approval before posting; evidence: approval log; tested: monthly sample review."

**22D.** How would you respond to a SOX control testing exception or finding?
*Answer:* Investigate the root cause, document the finding and impact, and build a remediation plan with a timeline — transparency with the audit team matters more than minimizing the issue. Example: finding 2 of 25 sampled JEs lacked approval evidence, tracing it to a staffing transition, and implementing a backup approver.

**22E.** How would you design a remediation plan for a recurring SOX control deficiency?
*Answer:* Identify the true root cause, redesign the control to be system-enforced rather than manually dependent where possible, assign clear ownership, and set a timeline with follow-up testing. Example: replacing a manual "remember to get approval" step with a system workflow blocking posting without approval, then re-testing next quarter.

### 23. Ensure compliance with accounting policy

**23A.** What is an accounting policy, and why must it be applied consistently?
*Answer:* The specific method a company adopts to apply accounting standards to its transactions; consistency keeps financial statements comparable period-over-period. Example: a consistent interest income recognition policy keeps quarterly numbers comparable.

**23B.** How do you stay updated on changes to accounting policy or standards?
*Answer:* Follow updates from technical accounting/controllership, FASB releases, and internal policy memos, and attend training when standards change. Example: reading an internal memo summarizing how a new ASC update affects the company's revenue recognition policy.

**23C.** How would you check if a transaction was recorded in line with policy?
*Answer:* Compare the treatment applied to the documented policy for that transaction type, and consult technical accounting if there's ambiguity or it's a new scenario. Example: checking a new fee type against the existing revenue recognition policy to see if it fits an existing category.

**23D.** A team persistently deviates from policy for convenience. What do you do?
*Answer:* Address it directly, explain the compliance/audit risk, and escalate to management if it continues — consistent policy application isn't optional. Example: flagging a team's habit of loosely rounding accruals instead of following the documented method, escalating if it persists.

**23E.** How would you handle a conflict between a new accounting standard and legacy practice still in use?
*Answer:* Assess the gap between current practice and the new requirement, quantify the transition impact, and work with technical accounting on an implementation plan — legacy practice gives way to the current standard, but deliberately, not abruptly. Example: planning a phased transition of a legacy revenue treatment to a newly adopted standard, with clear cut-over documentation for audit.
