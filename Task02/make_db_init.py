#!/usr/bin/env python3

import csv

BATCH_SIZE = 1000
OUTPUT_FILE = "db_init.sql"

def sql_str(value):
    if value is None:
        return "NULL"
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def sql_num(value):
    if value is None:
        return "NULL"
    return str(value)

def write_table(out, table_name, columns, rows):
    column_names = ", ".join(name for name, _ in columns)
    column_defs = ", ".join(f"{name} {spec}" for name, spec in columns)

    out.write(f"DROP TABLE IF EXISTS {table_name};\n")
    out.write(f"CREATE TABLE {table_name} ({column_defs});\n")

    for start in range(0, len(rows), BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]
        values_block = ",\n".join(
            "(" + ", ".join(row) + ")" for row in batch
        )
        out.write(f"INSERT INTO {table_name} ({column_names}) VALUES\n")
        out.write(values_block + ";\n")

    out.write("\n")


def parse_movies():
    result = []
    with open("movies.csv", encoding="utf-8", newline="") as f:
        for record in csv.DictReader(f):
            title = record["title"]
            year = "NULL"

            if title.endswith(")") and "(" in title:
                open_paren = title.rfind("(")
                candidate = title[open_paren + 1:-1]
                if candidate.isdigit():
                    year = candidate
                    title = title[:open_paren].strip()

            result.append((
                sql_num(int(record["movieId"])),
                sql_str(title),
                year,
                sql_str(record["genres"]),
            ))
    return result


def parse_ratings():
    result = []
    with open("ratings.csv", encoding="utf-8", newline="") as f:
        for row_number, record in enumerate(csv.DictReader(f), start=1):
            result.append((
                sql_num(row_number),
                sql_num(int(record["userId"])),
                sql_num(int(record["movieId"])),
                sql_num(float(record["rating"])),
                sql_num(int(record["timestamp"])),
            ))
    return result


def parse_tags():
    result = []
    with open("tags.csv", encoding="utf-8", newline="") as f:
        for row_number, record in enumerate(csv.DictReader(f), start=1):
            result.append((
                sql_num(row_number),
                sql_num(int(record["userId"])),
                sql_num(int(record["movieId"])),
                sql_str(record["tag"]),
                sql_num(int(record["timestamp"])),
            ))
    return result


def parse_users():
    result = []
    with open("users.txt", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue

            uid, name, email, gender, register_date, occupation = line.split("|")
            result.append((
                sql_num(int(uid)),
                sql_str(name),
                sql_str(email),
                sql_str(gender),
                sql_str(register_date),
                sql_str(occupation),
            ))
    return result



def main():
    schema = [
        ("movies", [
            ("id",     "INTEGER PRIMARY KEY"),
            ("title",  "TEXT"),
            ("year",   "INTEGER"),
            ("genres", "TEXT"),
        ], parse_movies),

        ("ratings", [
            ("id",        "INTEGER PRIMARY KEY"),
            ("user_id",   "INTEGER"),
            ("movie_id",  "INTEGER"),
            ("rating",    "REAL"),
            ("timestamp", "INTEGER"),
        ], parse_ratings),

        ("tags", [
            ("id",        "INTEGER PRIMARY KEY"),
            ("user_id",   "INTEGER"),
            ("movie_id",  "INTEGER"),
            ("tag",       "TEXT"),
            ("timestamp", "INTEGER"),
        ], parse_tags),

        ("users", [
            ("id",            "INTEGER PRIMARY KEY"),
            ("name",          "TEXT"),
            ("email",         "TEXT"),
            ("gender",        "TEXT"),
            ("register_date", "TEXT"),
            ("occupation",    "TEXT"),
        ], parse_users),
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for table_name, columns, parser in schema:
            write_table(out, table_name, columns, parser())


if __name__ == "__main__":
    main()