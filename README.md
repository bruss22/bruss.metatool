![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-lab%20tool-orange)
![Use Case](https://img.shields.io/badge/use%20case-SD--WAN%20%7C%20FMG%20%7C%20MetaVar-green)
# bruss.metatool

A lightweight **Python meta-utility** for generating and managing **FortiManager meta-variables** from CSV input.

This tool is designed to help automation and infrastructure workflows by:
- Converting CSV-based network metadata into importable FMG meta-variables
- Staging data in SQLite
- Optionally migrating results into MySQL
- Printing main.j2 jinja.loop Jinja templates based on specific use case meta-variables

---

## Features

- CSV → SQLite table generation
- SQLite → MySQL migration
- Automatic column and table creation
- Basic type inference during database migration
- Consistent, repeatable metavariable output
- Designed for lab, POC, and automation workflows

---

### File Overview

- **`input_meta.csv`**  
  Source metadata describing devices, networks, ports, subnets, etc.

- **`meta_creator.py`**  
  Main workflow that:
  - Parses CSV input
  - Generates metavariables
  - Writes output to SQLite / CSV
  - Optionally migrates data to MySQL
  - Prints main.j2 jinja.loop Jinja template

- **`main.py`**  
  Utility functions including:
  - CSV → SQLite table creation
  - SQLite → MySQL migration helpers
  - PrettyTable output helpers

---

## Requirements

- Python 3.8+
- Python libraries:
  - `prettytable`
  - `mysql-connector-python` (only required for MySQL mode)

Install dependencies:

```bash
pip install prettytable mysql-connector-python
```

⸻

Usage<br>

1. Prepare Input CSV

Edit input_meta.csv to match your environment.<br>
Each row represents a device/network definition used to generate metavariables.<br>

⸻

2. Run the Generator
```
python3 meta_creator.py
```
You will be prompted to choose:<br>
	•	CSV output mode (local file)<br>
	•	MySQL mode (uses SQLite as a staging DB)<br>

⸻

3. Output

Depending on your selection, the tool will:<br>
	•	Generate an output CSV file containing metavariables<br>
	•	OR migrate generated tables into MySQL<br>
	•	Print a Jinja snippet for jinja.loop scripts for FortiManager templates<br>

All output follows a consistent schema:<br>
	•	variable_name<br>
	•	default_value<br>
	•	description<br>
	•	device<br>
	•	VDOM<br>
	•	mapped_value<br>

```
#python3 meta_creator.py
✅Table 'metavar' created successfully in 'metavar.db'.
✅Table 'outfile' created successfully in 'metavar.db'.
Meta-Variable Columns from input_meta.csv: ['device', 'name', 'port', 'netid', 'subnet', 'dhcp', 'vrf']
Meta-Variable Columns from meta_creator_out.csv: ['variable_name', 'default_value', 'description', 'device', 'VDOM', 'mapped_value']
Create a Local CSV FIle? (N): 
Writing to x.x.x.x as ##########
Found tables: ['metavar', 'outfile']

=== Migrating table: metavar ===
  → Found 6 rows in SQLite table 'metavar'
  ✓ Inserted 6 rows into MySQL table 'metavar'

=== Migrating table: outfile ===
  → Found 46 rows in SQLite table 'outfile'
  ✓ Inserted 46 rows into MySQL table 'outfile'

✅ Conversion complete!

{# Script #1: Main jinja.loop Import CLI template For FMG. Create new FMG CLI Jinja Template#}
{%- set vlans = 
  [
        {'name':network-1_name, 'port':network-1_port, 'netid':network-1_netid, 'subnet':network-1_subnet, 'dhcp':network-1_dhcp, 'vrf':network-1_vrf},
        {'name':network-2_name, 'port':network-2_port, 'netid':network-2_netid, 'subnet':network-2_subnet, 'dhcp':network-2_dhcp, 'vrf':network-2_vrf},
  ]
-%}
```

⸻
Intended for POC and Lab use. use at your own risk
⸻

Database Utilities

CSV → SQLite

The tool dynamically creates SQLite tables based on CSV headers:<br>
	•	Headers are sanitized for SQL compatibility<br>
	•	All columns are created as TEXT<br>
	•	Existing tables are replaced automatically<br>

⸻

SQLite → MySQL

The migration utility:<br>
	•	Discovers all non-system SQLite tables<br>
	•	Creates matching MySQL tables<br>
	•	Maps SQLite types to basic MySQL types<br>
	•	Inserts all rows using batch operations<br>

This is intended for automation and staging, not as a full schema-migration framework.<br>

⸻

Attribution

Some helper functions implement common Python patterns for:<br>
	•	CSV → SQLite table creation<br>
	•	SQLite → MySQL migration<br>

These patterns are widely documented in public Python and database tutorials.<br>
The implementations in this project are adapted and combined for this specific workflow.<br>

⸻
