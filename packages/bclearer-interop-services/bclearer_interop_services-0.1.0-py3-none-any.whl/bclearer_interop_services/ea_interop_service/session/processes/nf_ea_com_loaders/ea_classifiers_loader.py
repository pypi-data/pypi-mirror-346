from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.factories.i_dual_element_factory import (
    create_i_dual_element,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.model_loader.maps.nf_uuids_to_com_objects_mappings import (
    NfUuidsToIDualObjectsMappings,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)
from bclearer_interop_services.ea_interop_service.session.processes.nf_ea_com_loaders.ea_stereotypes_load_helper import (
    get_ea_stereotype_ex,
)
from pandas import DataFrame
from tqdm import tqdm


def load_ea_classifiers(
    ea_classifiers: DataFrame,
    stereotype_usage_with_names: DataFrame,
):
    nf_uuid_column_name = (
        NfColumnTypes.NF_UUIDS.column_name
    )

    name_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    )

    type_column_name = (
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
    )

    ea_guid_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
    )

    parent_column_name = (
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name
    )

    classifier_column_name = (
        NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name
    )

    notes_column_name = (
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NOTES.column_name
    )

    for (
        index,
        ea_classifier_row,
    ) in tqdm(
        ea_classifiers.iterrows(),
        total=ea_classifiers.shape[0],
    ):
        ea_classifier = __load_ea_classifier(
            nf_uuid=ea_classifier_row[
                nf_uuid_column_name
            ],
            ea_package_parent_nf_uuid=ea_classifier_row[
                parent_column_name
            ],
            ea_classifier_name=ea_classifier_row[
                name_column_name
            ],
            ea_classifier_type=ea_classifier_row[
                type_column_name
            ],
            ea_classifier_nf_uuid=ea_classifier_row[
                classifier_column_name
            ],
            ea_classifier_notes=ea_classifier_row[
                notes_column_name
            ],
            stereotype_usage_with_names=stereotype_usage_with_names,
        )

        ea_classifiers.at[
            index, ea_guid_column_name
        ] = ea_classifier.element_guid

    return ea_classifiers


def __load_ea_classifier(
    nf_uuid: str,
    ea_package_parent_nf_uuid: str,
    ea_classifier_name: str,
    ea_classifier_type: str,
    ea_classifier_nf_uuid: str,
    ea_classifier_notes: str,
    stereotype_usage_with_names: DataFrame,
) -> IDualElement:
    ea_package_parent = NfUuidsToIDualObjectsMappings.get_i_dual_package(
        nf_uuid=ea_package_parent_nf_uuid
    )

    if (
        ea_classifier_notes
        == DEFAULT_NULL_VALUE
    ):
        ea_classifier_notes = ""

    ea_stereotype_ex = get_ea_stereotype_ex(
        client_nf_uuid=nf_uuid,
        stereotype_usage_with_names=stereotype_usage_with_names,
    )

    ea_classifier = create_i_dual_element(
        container=ea_package_parent,
        element_name=ea_classifier_name,
        element_type=ea_classifier_type,
        element_notes=ea_classifier_notes,
        stereotype_ex=ea_stereotype_ex,
    )

    NfUuidsToIDualObjectsMappings.map_nf_uuid_to_i_dual_element(
        nf_uuid=nf_uuid,
        i_dual_element=ea_classifier,
    )

    if (
        ea_classifier_nf_uuid
        == DEFAULT_NULL_VALUE
    ):
        return ea_classifier

    ea_classifier_classifier = NfUuidsToIDualObjectsMappings.get_i_dual_element(
        nf_uuid=ea_classifier_nf_uuid
    )

    if not isinstance(
        ea_classifier_classifier,
        IDualElement,
    ):
        raise TypeError

    ea_classifier.classifier_id = (
        ea_classifier_classifier.element_id
    )

    ea_classifier.update()

    return ea_classifier
