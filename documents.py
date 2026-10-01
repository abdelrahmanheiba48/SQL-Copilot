import metadata


def table_to_document(table_name, table_info):

    lines = []

    lines.append(f"TABLE: {table_name}")

    lines.append("")
    lines.append("COLUMNS:")

    for column in table_info["columns"]:
        nullable = "NULL" if column["nullable"] == "YES" else "NOT NULL"

        lines.append(
            f"- {column['column']}: {column['data_type']}, {nullable}"
        )

    lines.append("")
    lines.append("PRIMARY KEYS:")

    for pk in table_info.get("primary_keys", []):
        lines.append(f"- {pk}")

    lines.append("")
    lines.append("FOREIGN KEYS:")

    for fk in table_info.get("foreign_keys", []):
        lines.append(
            f"- {fk['column']} -> {fk['references']}"
        )

    return "\n".join(lines)


documents = []

for table_name, table_info in metadata.tables_info.items():

    document = table_to_document(
        table_name,
        table_info
    )

    documents.append(document)


metadatas = []

for table_name in metadata.tables_info:
    schema , table = table_name.split('.',1)

    metadatas.append(
        {
            'schema':schema,
            'table':table
        }
    )

#print(metadatas[0])
#print(metadatas[1])

