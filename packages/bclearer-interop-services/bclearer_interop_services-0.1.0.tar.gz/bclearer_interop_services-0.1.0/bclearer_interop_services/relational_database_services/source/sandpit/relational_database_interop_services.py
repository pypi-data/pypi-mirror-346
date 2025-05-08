import json

import pandas as pd
from storage_interop_services_source.code.object_models.RelationalDatabaseClients import (
    RelationalDatabaseClient,
)


def fetch_data_in_chunks(
    cursor,
    base_query: str,
    filter_list: [],
    csv_file_path: str,
    chunk_size=5,
):
    columns_written = False

    for i in range(
        0,
        len(filter_list),
        chunk_size,
    ):
        chunk = filter_list[
            i : i + chunk_size
        ]

        filter_tuple = tuple(chunk)

        placeholders = ", ".join(
            "?" for _ in filter_tuple
        )
        query = (
            base_query
            + f" IN ({placeholders})"
        )

        cursor.execute(
            query,
            filter_tuple,
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        results = cursor.fetchall()

        df_chunk = (
            pd.DataFrame.from_records(
                results,
                columns=columns,
            )
        )

        if not columns_written:
            df_chunk.to_csv(
                csv_file_path,
                index=False,
                mode="w",
                header=True,
            )

            columns_written = True

        else:
            print("wrote chunk to csv")

            df_chunk.to_csv(
                csv_file_path,
                index=False,
                mode="a",
                header=False,
            )


configuration_file = r"C:\Apps\S\bclearer_common_services\relational_database_interop_services\source\sandpit\configuration.json_service"

with open(
    configuration_file,
) as configuration_file:
    configuration = json.load(
        configuration_file,
    )

relational_database_client = (
    RelationalDatabaseClient(
        configuration[
            "connection_string"
        ],
    )
)

cursor = (
    relational_database_client.cursor
)

lubricants_sharepoint_sites_sheet = pd.read_excel(
    r"C:\Apps\S\bclearer_common_services\relational_database_interop_services\source\data\PTX-T sites - Finalize.xlsx",
    "PTXT Data",
)

lubricants_site_filter_list = (
    lubricants_sharepoint_sites_sheet[
        "WebURl"
    ].tolist()
)

print(
    "searching for data in the following sites: ",
    lubricants_site_filter_list,
)

base_query = "SELECT * FROM SPO_ItemLevel_Data WHERE SiteURL"

fetch_data_in_chunks(
    cursor=cursor,
    base_query=base_query,
    filter_list=lubricants_site_filter_list,
    csv_file_path=r"bclearer_interop_services\data\filtered_data.csv",
    chunk_size=1,
)

print(
    "The filtered data has been successfully written to 'filtered_data.csv'",
)


"""
CREATE TABLE [dbo].[Teams_ItemLevel_Data](
	[TeamUrl] [nvarchar](1000) NULL,
	[TeamsName] [nvarchar](255) NULL,
	[Topology2] [nvarchar](255) NULL,
	[topology3] [nvarchar](255) NULL,
	[Topology4] [nvarchar](255) NULL,
	[TopologyPath] [nvarchar](1200) NULL,
	[Item URL] [nvarchar](1024) NULL,
	[File Name] [nvarchar](2048) NULL,
	[File Type] [nvarchar](256) NULL,
	[File Size] [bigint] NULL,
	[Version] [nvarchar](10) NULL,
	[Security Classification] [nvarchar](1024) NULL,
	[Creation Date] [datetime2](7) NULL,
	[Modification Date] [datetime2](7) NOT NULL,
	[Labeling Date] [datetime2](7) NULL,
	[Retention Label Name] [nvarchar](2048) NULL,
	[Retention Label Applied Date] [datetime2](7) NULL,
	[Expiry Date] [date] NULL,
	[Created By] [nvarchar](1024) NULL,
	[Modifed By] [nvarchar](1024) NULL
) ON [PRIMARY]
GO

CREATE TABLE [dbo].[SPO_ItemLevel_Data](
	[SiteCollectionURL] [nvarchar](512) NOT NULL,
	["SiteURL""] [nvarchar](1024) NOT NULL,
	[Topology2] [nvarchar](256) NULL,
	[topology3] [nvarchar](256) NULL,
	[Topology4] [nvarchar](256) NULL,
	[TopologyPath] [nvarchar](1024) NULL,
	[SiteCollectionname] [nvarchar](1024) NULL,
	[Sitename] [nvarchar](1024) NOT NULL,
	[Item URL] [nvarchar](1024) NULL,
	[File Name] [nvarchar](2048) NULL,
	[File Type] [nvarchar](256) NULL,
	[File Size] [bigint] NULL,
	[Version] [nvarchar](10) NULL,
	[Security Classification] [nvarchar](1024) NULL,
	[Creation Date] [datetime2](7) NULL,
	[Modification Date] [datetime2](7) NOT NULL,
	[Labeling Date] [datetime2](7) NULL,
	[Retention Label Name] [nvarchar](2048) NULL,
	[Retention Label Applied Date] [datetime2](7) NULL,
	[Expiry Date] [datetime2](7) NULL,
	[Created By] [nvarchar](1024) NULL,
	[Modifed By] [nvarchar](1024) NULL
) ON [PRIMARY]
GO
"""
