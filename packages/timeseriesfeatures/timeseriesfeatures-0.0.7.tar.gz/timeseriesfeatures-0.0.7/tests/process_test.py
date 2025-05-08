"""Tests for the process function."""
import datetime
import os
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from timeseriesfeatures.process import process
from timeseriesfeatures.feature import Feature, FEATURE_TYPE_LAG, FEATURE_TYPE_ROLLING, VALUE_TYPE_NONE, VALUE_TYPE_DAYS


class TestProcess(unittest.TestCase):

    def setUp(self):
        self.dir = os.path.dirname(__file__)

    def test_process(self):
        rows = 100
        df = pd.DataFrame(data={
            "feature1": [float(x) for x in range(rows)],
            "feature2": [float(x + 1) for x in range(rows)],
        }, index=[
            datetime.datetime(2022, 1, 1) + datetime.timedelta(x) for x in range(rows)
        ])
        features = [
            Feature(feature_type=FEATURE_TYPE_LAG, value1=1),
            Feature(feature_type=FEATURE_TYPE_LAG, value1=2),
            Feature(feature_type=FEATURE_TYPE_LAG, value1=4),
            Feature(feature_type=FEATURE_TYPE_LAG, value1=8),
            Feature(feature_type=FEATURE_TYPE_ROLLING, value1=VALUE_TYPE_NONE, value2=None),
            Feature(feature_type=FEATURE_TYPE_ROLLING, value1=VALUE_TYPE_DAYS, value2=30),
        ]
        features_df = process(df, features=features)
        expected_features_df = pd.read_parquet(os.path.join(self.dir, "expected.parquet"))
        assert_frame_equal(features_df, expected_features_df)
