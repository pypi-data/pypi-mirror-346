import re

table_pattern = r"TABLE (.+) \((.+) CONSTRAINT (.+)\)"

column_pattern = r"[(.+)] [(.+)]"


def find_all_tables_from_schema_via_regex(
    schema_file_path: str,
):
    schema = __read_schema(
        schema_file_path,
    )

    table_compiled_pattern = re.compile(
        table_pattern,
        re.DOTALL,
    )

    col_compiled_pattern = re.compile(
        column_pattern,
        re.DOTALL,
    )

    for (
        table_pattern_match
    ) in re.finditer(
        table_compiled_pattern,
        schema,
    ):
        table_name = (
            table_pattern_match.group(1)
        )

        col_data = (
            table_pattern_match.group(2)
        )

        for (
            col_pattern_match
        ) in re.finditer(
            col_compiled_pattern,
            col_data,
        ):
            col_name = (
                col_pattern_match.group(
                    1,
                )
            )

            col_type = (
                col_pattern_match.group(
                    2,
                )
            )


def __read_schema(
    schema_file_path: str,
) -> str:
    schema_file = open(schema_file_path)

    schema = schema_file.read()

    return schema
