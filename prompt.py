WRITE_CONSTRAINTS_PROMPT = """
Generate lookup constraints to filter data for answering questions using ONLY the provided reference data.

TABLE RELATIONSHIP UNDERSTANDING:
- midatatable: Contains 74 records with (midataitemid, midataitemname)
- mitransreference: Contains (midataitemid, mitransrefid, mitransrefname) where:
  * 15 midataitemid values overlap with midatatable
  * Additional midataitemid values exist ONLY in mitransreference (not in midatatable)
- Use Retrieved Data structure to determine which table contains specific IDs

PROCESS STEPS:

1. Inventory: Extract all key concepts, terms, and entities from the question

2. Semantic Match: Find items in Retrieved Data that semantically match question concepts:

   PRIMARY MATCHING COLUMNS:
   - midataitemname: Data fields, financial metrics, disclosure items
   - mitransrefname: Funding rounds, security types, transaction categories

   MATCHING STRATEGIES:
   - Exact: "liquidation price" → midataitemname: "liquidation price"
   - Exact: "Series B" → mitransrefname: "Series B"
   - Synonyms: "funding round" → mitransrefname: "Series A", "Pre-Series B" 
   - Plurals: "advisors" → midataitemname: "Advisor Type"
   - Abbreviations: "M&A" → mitransrefname: "Merger and Acquisition"
   - Related: "expenses" → midataitemname: "Legal Expenses", "Underwriting Fees"

3. Validate Table Presence: Check Retrieved Data to confirm which table contains each matched ID

4. Construct Constraint: Build constraint using correct table references based on Retrieved Data

5. Output: Return constraint condition only

CONSTRAINT FORMATS:

Data Item Filtering (from midatatable):
midatatable.midataitemid = {id}
midatatable.midataitemid IN ({id1}, {id2}, {id3})

Reference Category Filtering (from mitransreference):
mitransreference.mitransrefid = {refid}
mitransreference.mitransrefid IN ({refid1}, {refid2})

Combined Filtering (when both tables have relevant matches):
midatatable.midataitemid = {id} , mitransreference.mitransrefid = {refid}
midatatable.midataitemid IN ({id1}, {id2}) , mitransreference.mitransrefid = {refid}

OUTPUT RULES:
- Content Only: Return constraint without WHERE clause, semicolons, or extra text
- Exact IDs: Use only IDs that appear in Retrieved Data
- Table Accuracy: Use midatatable for data items, mitransreference for reference categories
- No Match: Return empty response if no semantic matches found
- Too Broad: Return empty response if question too general to constrain

EXAMPLES:

Example 1: Single Data Item Match
Question: What is the liquidation price reported in each funding round?
Retrieved Data:
Table: midatatable
midataitemname                midataitemid
Advisor Type                  559
liquidation price            1060
Post-Money Valuation         177130

Semantic Match: "liquidation price" matches midataitemname exactly
Constraint: midatatable.midataitemid = 1060

Example 2: Single Reference Category Match
Question: What were the Series B funding details disclosed?
Retrieved Data:
Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111184          Pre-Series A         10
111188          Series A             11
111193          Series B             12

Semantic Match: "Series B" matches mitransrefname exactly
Constraint: mitransreference.mitransrefid = 12

Example 3: Combined Constraint
Question: What underwriting fees were reported in Series A rounds?
Retrieved Data:
Table: midatatable
midataitemname           midataitemid
Underwriting Fees        2050
Legal Expenses           2055

Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111188          Series A             11
111193          Series B             12

Semantic Match: "underwriting fees" matches midataitemname "Underwriting Fees", "Series A" matches mitransrefname "Series A"
Constraint: midatatable.midataitemid = 2050 , mitransreference.mitransrefid = 11

Example 4: Multiple Values IN Clause
Question: What advisor and trustee information is available for early-stage companies?
Retrieved Data:
Table: midatatable
midataitemname           midataitemid
Advisor Type             559
Advisor Institution      561
Trustee Name            562
Board Member Info       563

Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111200          Seed Round           8
111201          Pre-Series A         10

Semantic Match: "advisor" matches "Advisor Type" and "Advisor Institution", "trustee" matches "Trustee Name", "early-stage" matches "Seed Round" and "Pre-Series A"
Constraint: midatatable.midataitemid IN (559, 561, 562) , mitransreference.mitransrefid IN (8, 10)

Example 5: Synonym Matching
Question: What valuation data is reported for IPO transactions?
Retrieved Data:
Table: midatatable
midataitemname               midataitemid
Pre-Money Valuation          1070
Post-Money Valuation         1071
Enterprise Value             1072

Table: mitransreference
midataitemid    mitransrefname           mitransrefid
111210          Initial Public Offering   26
111211          Secondary Offering        27

Semantic Match: "valuation" matches "Pre-Money Valuation", "Post-Money Valuation", "Enterprise Value", "IPO" matches "Initial Public Offering"
Constraint: midatatable.midataitemid IN (1070, 1071, 1072) , mitransreference.mitransrefid = 26

Example 6: Plural/Related Term Matching
Question: What expenses were disclosed in merger transactions?
Retrieved Data:
Table: midatatable
midataitemname           midataitemid
Legal Expenses           2055
Underwriting Fees        2050
Transaction Costs        2060
Advisory Fees            2065

Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111220          Merger               30
111221          Acquisition          31

Semantic Match: "expenses" relates to "Legal Expenses", "Underwriting Fees", "Transaction Costs", "Advisory Fees", "merger" matches "Merger"
Constraint: midatatable.midataitemid IN (2055, 2050, 2060, 2065) , mitransreference.mitransrefid = 30

Example 7: Abbreviation Matching
Question: What M&A deal information includes debt financing details?
Retrieved Data:
Table: midatatable
midataitemname           midataitemid
Debt Amount              3010
Interest Rate            3011
Loan Terms              3012

Table: mitransreference
midataitemid    mitransrefname           mitransrefid
111230          Merger and Acquisition    32
111231          Leveraged Buyout         33

Semantic Match: "M&A" matches "Merger and Acquisition", "debt financing" relates to "Debt Amount", "Interest Rate", "Loan Terms"
Constraint: midatatable.midataitemid IN (3010, 3011, 3012) , mitransreference.mitransrefid = 32

Example 8: No Match Found
Question: What weather data is available for manufacturing companies?
Retrieved Data:
Table: midatatable
midataitemname           midataitemid
Revenue Amount           4010
Employee Count           4011

Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111240          Series C             40
111241          Bridge Round         41

Semantic Match: No semantic matches found for "weather data" in financial data context
Constraint: 

Example 9: Too Broad Question
Question: What information is available about companies?
Retrieved Data:
Table: midatatable
midataitemname           midataitemid
Revenue Amount           4010
Employee Count           4011
Market Cap               4012

Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111240          Series C             40
111241          IPO                  41

Semantic Match: Question too general - "information about companies" could match all available data items
Constraint: 

Example 10: Reference Category Only Match
Question: What data is available for bridge financing rounds?
Retrieved Data:
Table: mitransreference
midataitemid    mitransrefname       mitransrefid
111250          Bridge Financing      50
111251          Convertible Bridge    51
111252          Series A             52

Semantic Match: "bridge financing" matches "Bridge Financing" and "Convertible Bridge"
Constraint: mitransreference.mitransrefid IN (50, 51)

Your task:
Question: {question}
Query: {query}
Retrieved Data:
{retrieved_data}
Constraint: """