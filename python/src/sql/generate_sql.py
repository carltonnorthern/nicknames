import csv

# The script must be run from the main project directory
NICKNAME_RESOURCE = "./names.csv"
NAMES_SQL = "names.sql"
NAMES_TABLE = "nicknames"
NAMES_NORMALIZED_SQL = "names_normalized.sql"
NAMES_NORMALIZED_TABLE = "nicknames_normalized"


def main():
    with open(NICKNAME_RESOURCE) as f:
        r = csv.reader(f)
        max_nicknames = 0

        # Build the normalized inserts while iterating over nicknames
        # Build the basic inserts one level higher (one for each row)
        insert_sql = ""
        insert_normalized_sql = ""
        for row in r:
            nickname_count = len(row) - 1
            if nickname_count > max_nicknames:
                max_nicknames = nickname_count
            field_names = ""
            field_values = ""
            for idx in range(len(row)):
                if idx == 0:
                    field_names += "canonical_name, "
                    field_values += f"'{row[0]}', "
                elif 0 < idx < nickname_count:
                    field_names += f"nickname_{idx}, "
                    field_values += f"'{row[idx]}', "
                    insert_normalized_sql += generate_normalized_insert(
                        row[0], row[idx]
                    )
                else:
                    field_names += f"nickname_{idx}"
                    field_values += f"'{row[idx]}'"
                    insert_normalized_sql += generate_normalized_insert(
                        row[0], row[idx]
                    )
            insert_sql += f"insert into {NAMES_TABLE} ("
            insert_sql += field_names + ") values (" + field_values + ");\n"

    create_sql = generate_create_table_sql(max_nicknames)
    write_nicknames_sql(create_sql, insert_sql)

    create_normalized_sql = generate_create_normalized_table_sql()
    write_nicknames_normalized_sql(create_normalized_sql, insert_normalized_sql)


# Normalized insert always includes exactly 2 fields
def generate_normalized_insert(canonical_name: str, nickname: str):
    insert_sql = f"insert into {NAMES_NORMALIZED_TABLE} "
    insert_sql += "(canonical_name, nickname) values "
    insert_sql += f"('{canonical_name}', '{nickname}');\n"
    return


def write_nicknames_sql(create_sql: str, insert_sql: str):
    with open(NAMES_SQL, "w") as f:
        f.write("-- This creation script should work in most flavors of SQL.\n")
        f.write(
            "-- Logically, canonical_name is a primary key although no constraint or index is included."  # noqa: E501
        )
        f.write(create_sql)
        f.write(
            "\n-- These insert statements are verbose, but they could not be simpler to use.\n"  # noqa: E501
        )
        f.write(insert_sql)


def write_nicknames_normalized_sql(create_sql: str, insert_sql: str):
    with open(NAMES_NORMALIZED_SQL, "w") as f:
        f.write(
            "-- This creation script should work in most flavors of SQL.\n"  # noqa: E501
        )
        f.write(create_sql)
        f.write(
            "\n-- These insert statements are verbose, but they could not be simpler to use.\n"  # noqa: E501
        )
        f.write(insert_sql)


# table creation SQL [for non-normalized data]
# depends only on the maximum number of nicknames
def generate_create_table_sql(nick_name_count: int):
    create_table_sql = f"create table {NAMES_TABLE} (\n"
    create_table_sql += "  canonical_name varchar(255),\n"
    for i in range(nick_name_count):
        create_table_sql += f"  nickname_{i+1} varchar(255)"
        if i < nick_name_count - 1:
            create_table_sql += ","
        create_table_sql += "\n"
    create_table_sql += ");\n"
    return create_table_sql


# table creation SQL for normalized data is 100% static
def generate_create_normalized_table_sql():
    create_table_sql = f"create table {NAMES_NORMALIZED_TABLE} (\n"
    create_table_sql += "  canonical_name varchar(255),\n"
    create_table_sql += "  nickname varchar(255)\n);\n"
    return create_table_sql


if __name__ == "__main__":
    main()
