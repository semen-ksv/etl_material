from io import StringIO
import pandas as pd

from api.google_bucket import download_google_bucket_blob
from api.models import MaterialData, StatisticMaterialType, StatisticMaterialMeasureUnit


def save_material_type_statistic(statistic_material_type_df: pd.DataFrame) -> None:
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

    MaterialData.objects.bulk_update_or_create(
        material_items,
        ['notes', 'modified', 'material_type', 'amount', 'license', 'cost', 'cultivation_tax', 'amount_history',
         'slug', 'sequence', 'creation_run', 'strain', 'batch_number', 'custom_fields', 'short_name', 'kind'],
        match_field='uuid')


def denormilize_data():
    material_df = pd.read_csv(StringIO(download_google_bucket_blob('Material.csv')), sep=',')
    material_type_df = pd.read_csv(StringIO(download_google_bucket_blob('MaterialType.csv')), sep=',')
    unit_of_measure_df = pd.read_csv(StringIO(download_google_bucket_blob('UnitOfMeasure.csv')), sep=',')

    def get_material_type(material_id: pd.Series, row_name: str) -> str:
        material_type_row = material_type_df.loc[material_type_df.id == material_id, row_name]
        return material_type_row.values[0]

    def get_unit_type(uid_short_name: pd.Series, row_name: str) -> str:
        material_type_row = unit_of_measure_df.loc[unit_of_measure_df.short_name == uid_short_name, row_name]
        return material_type_row.values[0]

    def get_unit_measure(material_id: pd.Series, row_name: str) -> str:
        material_unit_value = get_material_type(material_id, 'unit')
        unit_measure_row = unit_of_measure_df.loc[unit_of_measure_df.name == material_unit_value, row_name]
        return unit_measure_row.values[0]

    material_df["short_name"] = material_df.apply(lambda row: get_unit_measure(row.material_type, 'short_name'), axis=1)
    material_df["kind"] = material_df.apply(lambda row: get_material_type(row.material_type, 'kind'), axis=1)
    save_material_df(material_df)

    statistic_material_type_df = material_df.groupby(['material_type'])[['amount', 'cost']].agg('sum').reset_index()
    statistic_material_type_df["material_name"] = statistic_material_type_df.apply(
        lambda row: get_material_type(row.material_type, 'name'), axis=1)
    save_material_type_statistic(statistic_material_type_df)

    statistic_unit_of_measure_df = material_df.groupby(['short_name'])[['amount', 'cost']].agg('sum').reset_index()
    statistic_unit_of_measure_df["measure_type"] = statistic_unit_of_measure_df.apply(
        lambda row: get_unit_type(row.short_name, 'name'), axis=1)
    save_material_unit_statistic(statistic_unit_of_measure_df)

