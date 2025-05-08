# TODO move to CypherQueries class


def read_cypher_query_from_file(
    file_path,
):
    try:
        with open(file_path) as file:
            query = file.read()
            print(
                f"Cypher Query:\n {query}\n",
            )
            return query
    except FileNotFoundError:
        print(
            f"File not found: {file_path}",
        )
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def generate_list_from_text(text):
    if not text:
        return []

    # Split the text by the delimiter ';'
    result_list = text.split(";")

    # Strip any leading/trailing whitespace from each element
    result_list = [
        item.strip()
        for item in result_list
    ]

    print(result_list)
    return result_list
