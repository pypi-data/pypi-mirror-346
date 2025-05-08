from bclearer_interop_services.b_dictionary_service.common_knowledge.table_register_b_dictionary_return_types import (
    TableRegisterBDictionaryReturnTypes,
)
from bclearer_interop_services.b_dictionary_service.objects.b_dictionaries import (
    BDictionaries,
)
from bclearer_interop_services.b_dictionary_service.objects.table_b_dictionaries import (
    TableBDictionaries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class TableRegisters(BDictionaries):
    def __init__(self):
        super().__init__()

    def create_table_b_dictionary(
        self,
        table_name: str,
        bie_table_id: BieIds,
    ) -> TableRegisterBDictionaryReturnTypes:
        if (
            bie_table_id
            in self.dictionary
        ):
            return (
                TableRegisterBDictionaryReturnTypes.TABLE_ALREADY_EXISTS
            )

        table_b_dictionary = TableBDictionaries(
            table_name=table_name,
            bie_table_id=bie_table_id,
        )

        self.dictionary[
            bie_table_id
        ] = table_b_dictionary

        return (
            TableRegisterBDictionaryReturnTypes.TABLE_CREATED
        )

    def get_table_b_dictionary(
        self,
        bie_table_id: BieIds,
    ) -> TableBDictionaries:
        return self.dictionary[
            bie_table_id
        ]

    def add_new_table_b_dictionary(
        self,
        table_b_dictionary: TableBDictionaries,
    ) -> TableRegisterBDictionaryReturnTypes:
        if (
            table_b_dictionary.bie_table_id
            in self.dictionary
        ):
            return (
                TableRegisterBDictionaryReturnTypes.TABLE_ALREADY_EXISTS
            )

        self.dictionary[
            table_b_dictionary.bie_table_id
        ] = table_b_dictionary

        return (
            TableRegisterBDictionaryReturnTypes.TABLE_ADDED
        )

    def add_new_or_update_table_b_dictionary(
        self,
        table_b_dictionary: TableBDictionaries,
    ) -> None:
        self.dictionary[
            table_b_dictionary.bie_table_id
        ] = table_b_dictionary
