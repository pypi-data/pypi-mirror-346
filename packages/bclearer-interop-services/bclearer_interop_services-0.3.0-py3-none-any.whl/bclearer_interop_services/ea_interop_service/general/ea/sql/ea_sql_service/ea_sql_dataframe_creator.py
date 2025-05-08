from bclearer_interop_services.ea_interop_service.general.ea.sql.ea_sql_service.xml_to_pandas.t_table_dataframe_creator import (
    create_t_table_dataframe,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_attribute_column_types import (
    EaTAttributeColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_cardinality_column_types import (
    EaTCardinalityColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_column_types import (
    EaTConnectorColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_connector_types_column_types import (
    EaTConnectorTypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagram_column_types import (
    EaTDiagramColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagramlinks_column_types import (
    EaTDiagramlinksColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagramobjects_column_types import (
    EaTDiagramobjectsColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_diagramtypes_column_types import (
    EaTDiagramTypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_object_column_types import (
    EaTObjectColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_objecttypes_column_types import (
    EaTObjectTypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_operation_column_types import (
    EaTOperationColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_stereotypes_column_types import (
    EaTStereotypesColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_xref_column_types import (
    EaTXrefColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_collection_types import (
    EaCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.objects.ea_repositories import (
    EaRepositories,
)
from bclearer_interop_services.ea_interop_service.session.ea_repository_mappers import (
    EaRepositoryMappers,
)
from pandas import DataFrame


def create_ea_sql_dataframe(
    ea_repository: EaRepositories,
    ea_collection_type: EaCollectionTypes,
) -> DataFrame:
    i_dual_repository = EaRepositoryMappers.get_i_dual_repository(
        ea_repository=ea_repository
    )

    ea_t_table_as_xml_string = i_dual_repository.sql_query(
        sql="SELECT * FROM "
        + ea_collection_type.collection_name
    )

    ea_t_table_dataframe = __create_ea_t_table_dataframe(
        ea_t_table_as_xml_string=ea_t_table_as_xml_string,
        ea_collection_type=ea_collection_type,
    )

    return ea_t_table_dataframe


def __create_ea_t_table_dataframe(
    ea_t_table_as_xml_string: str,
    ea_collection_type: EaCollectionTypes,
) -> DataFrame:
    if (
        ea_collection_type
        == EaCollectionTypes.T_OBJECT
    ):
        t_object_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTObjectColumnTypes,
        )

        return t_object_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_CONNECTOR
    ):
        t_connector_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTConnectorColumnTypes,
        )

        return t_connector_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_ATTRIBUTE
    ):
        t_attribute_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTAttributeColumnTypes,
        )

        return t_attribute_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_DIAGRAM
    ):
        t_diagram_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTDiagramColumnTypes,
        )

        return t_diagram_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_DIAGRAMLINKS
    ):
        t_diagramlinks_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTDiagramlinksColumnTypes,
        )

        return t_diagramlinks_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_DIAGRAMOBJECTS
    ):
        t_diagramobjects_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTDiagramobjectsColumnTypes,
        )

        return (
            t_diagramobjects_dataframe
        )

    if (
        ea_collection_type
        == EaCollectionTypes.T_PACKAGE
    ):
        t_package_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTPackageColumnTypes,
        )

        return t_package_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_STEREOTYPES
    ):
        t_stereotypes_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTStereotypesColumnTypes,
        )

        return t_stereotypes_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_XREF
    ):
        t_xref_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTXrefColumnTypes,
        )

        return t_xref_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_OPERATION
    ):
        t_operation_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTOperationColumnTypes,
        )

        return t_operation_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_CONNECTORTYPES
    ):
        t_connector_types_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTConnectorTypesColumnTypes,
        )

        return (
            t_connector_types_dataframe
        )

    if (
        ea_collection_type
        == EaCollectionTypes.T_OBJECTTYPES
    ):
        t_objecttypes_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTObjectTypesColumnTypes,
        )

        return t_objecttypes_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_DIAGRAMTYPES
    ):
        t_diagramtypes_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTDiagramTypesColumnTypes,
        )

        return t_diagramtypes_dataframe

    if (
        ea_collection_type
        == EaCollectionTypes.T_CARDINALITY
    ):
        t_cardinality_dataframe = create_t_table_dataframe(
            t_table_as_xml_string=ea_t_table_as_xml_string,
            column_types_enum=EaTCardinalityColumnTypes,
        )

        return t_cardinality_dataframe
