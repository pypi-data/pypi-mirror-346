from pathlib import Path


def convert_relative_path_to_absolute(
    input_path: str,
    base_root_path: str,
) -> str:
    if is_relative_to_base_root(
        input_path,
        base_root_path,
    ):
        absolute_path = str(
            Path(base_root_path)
            / input_path,
        )

        return absolute_path

    return input_path


def is_relative_to_base_root(
    input_path: str,
    base_root_path: str,
) -> bool:
    input_path_instance = Path(
        input_path,
    )

    base_root_path_obj = Path(
        base_root_path,
    ).resolve()

    if (
        not input_path_instance.is_absolute()
    ):
        absolute_input_path = (
            base_root_path_obj
            / input_path_instance
        ).resolve()

        is_relative_to_base_root_bool = (
            absolute_input_path.parts[
                : len(
                    base_root_path_obj.parts,
                )
            ]
            == base_root_path_obj.parts
        )

        return is_relative_to_base_root_bool

    return False
