import pyodbc 


connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=AdventureWorks2025;"
    "Trusted_Connection=yes;"
)

#connection.close()

cursor = connection.cursor()
#-----------------------------------------------------------
# TABLES
query = """
SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_SCHEMA , TABLE_NAME ;

"""


cursor.execute(query)

tables = cursor.fetchall()
'''
for table in tables :
    print(table.TABLE_SCHEMA , table.TABLE_NAME)
'''

#----------------------------------------------------------------
#COLUMNS
cursor2 = connection.cursor()

query = """
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY
    TABLE_SCHEMA,
    TABLE_NAME,
    ORDINAL_POSITION;
"""

cursor2.execute(query)

columns = cursor2.fetchall()

#print('#'*190)
'''
for row in columns:
    print(
        row.TABLE_SCHEMA,
        row.TABLE_NAME,
        row.COLUMN_NAME,
        row.DATA_TYPE,
        row.IS_NULLABLE
)
'''
#-------------------------------------------------------------
#Primary_key
query = """
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE CONSTRAINT_NAME LIKE 'PK_%'
ORDER BY
    TABLE_SCHEMA,
    TABLE_NAME;
"""

cursor3 = connection.cursor()

cursor3.execute(query)

primary_keys = cursor3.fetchall()
#print("#"*190)
'''
for row in primary_keys:
    print(
        row.TABLE_SCHEMA,
        row.TABLE_NAME,
        row.COLUMN_NAME,
        row.CONSTRAINT_NAME
    )
'''
#------------------------------------------------------------
#Forign key
query = """
SELECT
    fk.name AS ForeignKeyName,
    OBJECT_SCHEMA_NAME(fk.parent_object_id) AS FromSchema,
    OBJECT_NAME(fk.parent_object_id) AS FromTable,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS FromColumn,
    OBJECT_SCHEMA_NAME(fk.referenced_object_id) AS ToSchema,
    OBJECT_NAME(fk.referenced_object_id) AS ToTable,
    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ToColumn
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc
    ON fk.object_id = fkc.constraint_object_id
ORDER BY
    FromSchema,
    FromTable;
"""

cursor4 = connection.cursor()

cursor4.execute(query)

foreign_keys = cursor4.fetchall()

#print("#"*190)
'''
for row in foreign_keys:
    print(
        row.FromSchema,
        row.FromTable,
        row.FromColumn,
        "->",
        row.ToSchema,
        row.ToTable,
        row.ToColumn
    )
'''
#connection.close()

#print(columns[0])
#print(type(columns[0]))
#print("x"*190)

# Columns

column_info = []

for row in columns:
    column = {
        "schema": row.TABLE_SCHEMA,
        "table": row.TABLE_NAME,
        "column": row.COLUMN_NAME,
        "data_type": row.DATA_TYPE,
        "nullable": row.IS_NULLABLE
    }

    column_info.append(column)

# tables

tables_info = {}

for column in column_info:
    table_name = f"{column['schema']}.{column['table']}"
    if table_name not in tables_info:
        tables_info[table_name]={
            'columns':[]
        }
    tables_info[table_name]["columns"].append(column)


# Primary key


for row in primary_keys:

    table_name = f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}"

    if "primary_keys" not in tables_info[table_name]:
        tables_info[table_name]["primary_keys"] = []

    tables_info[table_name]["primary_keys"].append(
        row.COLUMN_NAME
    )


# Froeign key

for row in foreign_keys:

    from_table = f"{row.FromSchema}.{row.FromTable}"

    foreign_key = {
        "column": row.FromColumn,
        "references": f"{row.ToSchema}.{row.ToTable}.{row.ToColumn}"
    }

    if "foreign_keys" not in tables_info[from_table]:
        tables_info[from_table]["foreign_keys"] = []

    tables_info[from_table]["foreign_keys"].append(foreign_key)

