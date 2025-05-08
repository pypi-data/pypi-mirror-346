from collections.abc import Generator


def get_list_chunks(
    list_of_elements: list,
    chunk_size: int,
) -> Generator:
    return (
        list_of_elements[
            pos : pos + chunk_size
        ]
        for pos in range(
            0,
            len(list_of_elements),
            chunk_size,
        )
    )
