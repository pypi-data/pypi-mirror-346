from bclearer_interop_services.b_dictionary_service.common_knowledge.table_b_dictionary_return_types import (
    TableBDictionaryReturnTypes,
)
from bclearer_interop_services.b_dictionary_service.objects.b_dictionaries import (
    BDictionaries,
)
from bclearer_interop_services.b_dictionary_service.objects.row_b_dictionaries import (
    RowBDictionaries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creators.bie_id_for_multiple_objects_creator import (
    create_bie_id_for_multiple_objects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class TableBDictionaries(BDictionaries):
    def __init__(
        self,
        table_name: str,
        bie_table_id: BieIds,
    ):
        super().__init__()

        self.table_name = table_name

        self.bie_table_id = bie_table_id

    def add_new_row_b_dictionary(
        self,
        bie_row_id: BieIds,
        row_b_dictionary: RowBDictionaries,
    ) -> TableBDictionaryReturnTypes:
        if (
            bie_row_id
            in self.dictionary
        ):
            return (
                TableBDictionaryReturnTypes.ROW_ALREADY_EXISTS
            )

        self.dictionary[bie_row_id] = (
            row_b_dictionary
        )

        return (
            TableBDictionaryReturnTypes.ROW_ADDED
        )

    def add_new_or_update_row_b_dictionary(
        self,
        bie_row_id: BieIds,
        row_b_dictionary: RowBDictionaries,
    ) -> None:
        self.dictionary[bie_row_id] = (
            row_b_dictionary
        )

    def get_next_bie_row_id(
        self,
    ) -> BieIds:
        next_row_number = len(
            self.dictionary,
        )

        strings = [
            "row",
            self.table_name,
            str(next_row_number),
        ]

        next_bie_row_id = create_bie_id_for_multiple_objects(
            input_objects=strings,
        )

        return next_bie_row_id
