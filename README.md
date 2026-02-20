# bruss.metatool
Metavar File Generator for Fortimanager Import.


### Attribution

The function `create_table_from_csv` is based on a common
CSV → SQLite dynamic table creation pattern found in public
Python SQLite tutorials, where:

- CSV headers are read,
- sanitized (spaces/special chars replaced with underscores),
- and used to build a CREATE TABLE SQL command.

This approach is described in Python SQLite import examples such as:
- https://github.com/zblesk/csv-to-sqlite
- https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
- https://blog.csdn.net/weixin_42107409/article/details/151851732
