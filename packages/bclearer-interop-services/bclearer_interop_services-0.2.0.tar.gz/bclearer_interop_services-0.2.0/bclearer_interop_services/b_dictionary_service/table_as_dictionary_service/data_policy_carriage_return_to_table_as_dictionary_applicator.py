def apply_data_policy_carriage_return_to_table_as_dictionary(
    table_as_dictionary: dict,
) -> None:
    for (
        key,
        row_as_dictionary,
    ) in table_as_dictionary.items():
        __apply_data_policy_carriage_return_to_row_dictionary(
            row_as_dictionary=row_as_dictionary,
        )


def __apply_data_policy_carriage_return_to_row_dictionary(
    row_as_dictionary: dict,
) -> None:
    for (
        column_name,
        cell_value,
    ) in row_as_dictionary.items():
        __apply_data_policy_carriage_return_to_cell_value(
            column_name=column_name,
            cell_value=cell_value,
            row_as_dictionary=row_as_dictionary,
        )


# TODO: Generalise the replacement at the end? two versions, apply windows new line/unix new line policy?
#  then generalise the higher level to table as dictionary services?
def __apply_data_policy_carriage_return_to_cell_value(
    column_name: str,
    cell_value: str,
    row_as_dictionary: dict,
) -> None:
    if isinstance(cell_value, str):
        cleaned_cell = (
            cell_value.replace(
                "\r\n",
                "\n",
            )
        )

        row_as_dictionary[
            column_name
        ] = cleaned_cell
