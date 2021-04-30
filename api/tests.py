import os
import sys
from pathlib import Path

from django.test import TestCase
import unittest
import pandas as pd
import datatest as dt
from api.services import denormilize_data, get_material_type, get_unit_type, get_unit_measure
from django import setup as django_setup
import logging

dir = Path(__file__).resolve().parent.parent

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_metabase.settings")
# sys.path.append(dir)

# This is so my local_settings.py gets loaded.
os.chdir(dir)
django_setup()

class TestMovies(dt.DataTestCase):
    @dt.mandatory
    def test_material_columns(self):

        material_df_test = pd.read_csv('/api/files/Material_test.csv')
        self.assertValid(
            material_df_test.columns,
            {'id', 'created', 'modified', 'material_type', 'amount', 'cost'},
        )


class TestDenormilization(TestCase):
    def setUp(self):

        with dt.working_directory(__file__):
            self.material_df = pd.read_csv('/api/files/Material_test.csv')
        with dt.working_directory(__file__):
            self.material_type_df = pd.read_csv('/api/files/MaterialType_test.csv')
        with dt.working_directory(__file__):
            self.unit_of_measure_df = pd.read_csv('/api/files/UnitOfMeasure_test.csv')

    def test_get_material_type(self):
        self.assertEqual(get_material_type(
            self.material_type_df, self.material_type_df.loc[1], 'kind'), 'PACKAGING')

    def test_get_short_unit_name(self):
        self.assertEqual(get_unit_measure(
            self.material_type_df, self.unit_of_measure_df, self.material_type_df.loc[1], 'short_name'), 'ea')

    def test_get_type_name(self):
        self.assertEqual(get_material_type(self.material_type_df, self.material_type_df.loc[1], 'name'), '500ml Bottle')

