from io import StringIO
import pandas as pd

from api.google_bucket import download_google_bucket_blob
from api.models import MaterialData, StatisticMaterialType, StatisticMaterialMeasureUnit


def save_material_type_statistic(statistic_material_type_df: pd.DataFrame) -> None:
    """save statistic and counted data for Material type"""
    material_items = []
    StatisticMaterialType.objects.all().delete()
    for i, row in statistic_material_type_df.iterrows():
        material_items.append(
            StatisticMaterialType(
                material_type=row.material_type,
                material_name=row.material_name,
                amount=row.amount,
                cost=row.cost,
            )
        )
    StatisticMaterialType.objects.bulk_create(material_items)


def save_material_unit_statistic(statistic_material_type_df: pd.DataFrame) -> None:
    """save statistic and counted data for Material according unit of measure"""
    material_items = []
    StatisticMaterialMeasureUnit.objects.all().delete()
    for i, row in statistic_material_type_df.iterrows():
        material_items.append(
            StatisticMaterialMeasureUnit(
                short_name=row.short_name,
                measure_type=row.measure_type,
                amount=row.amount,
                cost=row.cost,
            )
        )
    StatisticMaterialMeasureUnit.objects.bulk_create(material_items)


def save_material_df(material_df: pd.DataFrame) -> None:
    """save Material data after denormalization"""
    material_items = []
    material_to_db = material_df.where((pd.notnull(material_df)), None)

    for i, row in material_to_db.iterrows():
        material_items.append(
            MaterialData(
                uuid=row.id,
                notes=row.notes,
                created=row.created,
                modified=row.modified,
                material_type=row.material_type,
                amount=row.amount,
                license=row.license,
                cost=row.cost,
                cultivation_tax=row.cultivation_tax,
                amount_history=row.amount_history,
                slug=row.slug,
                sequence=row.sequence,
                creation_run=row.creation_run,
                strain=row.strain,
                batch_number=row.batch_number,
                custom_fields=row.custom_fields,
                short_name=row.short_name,
                kind=row.kind
            )
        )

    # Create and update fields in existing table by one request
    MaterialData.objects.bulk_update_or_create(
        material_items,
        ['notes', 'modified', 'material_type', 'amount', 'license', 'cost', 'cultivation_tax', 'amount_history',
         'slug', 'sequence', 'creation_run', 'strain', 'batch_number', 'custom_fields', 'short_name', 'kind'],
        match_field='uuid')


def get_material_type(material_type_df: pd.DataFrame, material_id: pd.Series, row_name: str) -> str:
    """get kind of material type by material type id"""
    material_type_row = material_type_df.loc[material_type_df.id == material_id, row_name]
    return material_type_row.values[0]


def get_unit_type(unit_of_measure_df, uid_short_name: pd.Series, row_name: str) -> str:
    """get unit of measure name by type"""
    material_type_row = unit_of_measure_df.loc[unit_of_measure_df.short_name == uid_short_name, row_name]
    return material_type_row.values[0]


def get_unit_measure(material_type_df, unit_of_measure_df, material_id: pd.Series, row_name: str) -> str:
    """get short name of unit of measure by material type id"""
    material_unit_value = get_material_type(material_type_df, material_id, 'unit')
    unit_measure_row = unit_of_measure_df.loc[unit_of_measure_df.name == material_unit_value, row_name]
    return unit_measure_row.values[0]


def denormilize_data() -> bool:
    """load data from Google cloud storage,
        denormilize table Material and add column 'short_name' and 'kind',
        preparing statistic and counting data for building graphs"""

    # Load data from Cloud Storage
    material_df = pd.read_csv(StringIO(download_google_bucket_blob('Material.csv')), sep=',', chunksize=1000)
    material_type_df = pd.read_csv(StringIO(download_google_bucket_blob('MaterialType.csv')), sep=',')
    unit_of_measure_df = pd.read_csv(StringIO(download_google_bucket_blob('UnitOfMeasure.csv')), sep=',')

    chunk_list = []  # save dataframe of Materials after demoralization
    if material_df:
        for material_chunk in material_df:
            # add new fields to Material table
            material_chunk["short_name"] = material_chunk.apply(
                lambda row: get_unit_measure(material_type_df, unit_of_measure_df, row.material_type, 'short_name'), axis=1)
            material_chunk["kind"] = material_chunk.apply(
                lambda row: get_material_type(material_type_df, row.material_type, 'kind'), axis=1)

            # save chunk to database
            save_material_df(material_chunk)

            # append the chunk to list with columns that will be used for counting
            chunk_list.append(material_chunk[['material_type', 'amount', 'cost', 'short_name']])

        material_df_concat = pd.concat(chunk_list)

        # aggregate data and make statistic for graphs

        statistic_material_type_df = material_df_concat.groupby(
            ['material_type'])[['amount', 'cost']].agg('sum').reset_index()
        statistic_material_type_df["material_name"] = statistic_material_type_df.apply(
            lambda row: get_material_type(material_type_df, row.material_type, 'name'), axis=1)
        save_material_type_statistic(statistic_material_type_df)

        statistic_unit_of_measure_df = material_df_concat.groupby(
            ['short_name'])[['amount', 'cost']].agg('sum').reset_index()
        statistic_unit_of_measure_df["measure_type"] = statistic_unit_of_measure_df.apply(
            lambda row: get_unit_type(unit_of_measure_df, row.short_name, 'name'), axis=1)
        save_material_unit_statistic(statistic_unit_of_measure_df)

        return True
    else:
        return False
