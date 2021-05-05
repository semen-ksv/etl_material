import numpy as np
import pandas as pd
import datatest as dt

from django.test import TestCase

from api.services import get_material_type, get_unit_measure


class TestDenormalization(TestCase):
    def setUp(self):

        with dt.working_directory(__file__):
            self.material_df = pd.read_csv('./files/Material_test.csv', sep=';')
        with dt.working_directory(__file__):
            self.material_type_df = pd.read_csv('./files/MaterialType_test.csv', sep=';')
        with dt.working_directory(__file__):
            self.unit_of_measure_df = pd.read_csv('./files/UnitOfMeasure_test.csv', sep=';')

    def test_get_material_type(self):
        row = self.material_type_df.iloc[1]
        self.assertEqual(get_material_type(
            self.material_type_df, row.id, 'kind'), 'RAW_MATERIAL')

    def test_get_material_type_nan(self):
        cars = {'id': [22], 'name': ['first']}
        test_df = pd.DataFrame(cars, columns=['id', 'name'])
        self.assertEqual(type(get_material_type(
            self.material_type_df, test_df.iloc[0].id, 'kind')), type(np.nan))

    def test_get_short_unit_name(self):
        self.assertEqual(get_unit_measure(
            self.material_type_df, self.unit_of_measure_df, self.material_type_df.loc[1].id, 'short_name'), 'lb')

    def test_get_type_name(self):
        self.assertEqual(get_material_type(self.material_type_df, self.material_type_df.loc[1].id, 'name'), 'Dry Biomass')

