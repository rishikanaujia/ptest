DATABASE_SCHEMA_LINKING_INSTRUCTIONS = """# Database Schema Linking Instructions

## Task Overview
You are tasked with identifying the relevant tables and columns from a SQL database schema to answer user questions. Generate schema links that will be used to construct accurate SQL queries.

## Core Requirements

### Data Retrieval Rules
- **Company Queries**: Always include the company name when questions involve specific companies
- **Contextual Information**: Provide additional relevant context (currency, dates, document IDs, etc.) when applicable
- **Schema Compliance**: Only use tables and columns explicitly defined in the provided database schema
- **Key Relationships**: Ensure all joins are based on explicitly defined relationships in the schema

### Schema Analysis
- Check schema details and identify columns that act as foreign keys that can be used to join multiple tables
- Analyze table relationships to ensure proper joins between related entities

### Output Format
- Return schema links as a single, flat list following the provided examples
- When combining elements from multiple reasoning steps, concatenate them logically
- Include useful contextual columns (date, company_id, document_id) when relevant

### Query Constraints
- Use company_id for searching companies (corresponding IDs will be provided)
- Include any additional constraints specified in the database documentation
- Apply constraints from the "Lookup Constraints" section when provided
- Only reference tables and columns that exist in the schema

## Database Schema
[Schema details to be provided below]

## Lookup Constraints
[Additional constraints from prior queries to be listed here]

### Constraint Processing Rules

**Format 1: Reference ID Constraints**
- When constraint format is: `mitransreference.mitransrefid = {refid}`
- Action: Include `mitransreference` table in schema link

**Format 2: Data Item ID Constraints**
- When constraint format is: `midatatable.midataitemid = {id}`
- Action: Use the table_dict below to find the appropriate table based on the midataitemid value
- Include the identified table in schema link

### Table Dictionary for Data Item IDs
```python
table_dict = {
    "mitransofnumdata": {
        533: "Shares Offered, Excluding Overallotment",
        535: "Offering Price",
        130990: "liquidation price",
        540: "Revenue Growth",
        536: "Pre-money Valuation",
        537: "Post-money Valuation"
    },
    "mitransoftextdata": {
        53: "Offering Termination Date",
        130913: "Reorganization",
        130914: "Pay to Play",
        130915: "Pay to Play Penalties"
    },
    "company_finmetrics": {
        2001: "Net Income",
        2002: "EBITDA",
        2003: "Gross Margin",
        2004: "Operating Cash Flow"
    },
    "company_captable": {
        3001: "Preferred Shares Outstanding",
        3002: "Common Shares Outstanding",
        3003: "Options Granted",
        3004: "Convertible Notes"
    },
    "company_terms": {
        4001: "Board Rights",
        4002: "Drag Along Rights",
        4003: "Tag Along Rights",
        4004: "Liquidation Preference"
    }
}
```

---
*Current Date: {today's_date}*"""
