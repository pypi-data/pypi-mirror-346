"""Tests for the compute function."""
import datetime
import os
import unittest

import pandas as pd

from timeseriesfeatures.compute import compute
from timeseriesfeatures.feature import Feature, FEATURE_TYPE_LAG, VALUE_TYPE_INT


class TestCompute(unittest.TestCase):

    def setUp(self):
        self.dir = os.path.dirname(__file__)

    def test_compute(self):
        rows = 100
        df = pd.DataFrame(data={
            "feature1": [float(x) for x in range(rows)],
            "feature2": [float(x + 1) for x in range(rows)],
        }, index=[
            datetime.datetime(2022, 1, 1) + datetime.timedelta(x) for x in range(rows)
        ])
        features = compute(df, 30)
        expected_features = [
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature1"], value1=VALUE_TYPE_INT, value2=1),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature1"], value1=VALUE_TYPE_INT, value2=2),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature1"], value1=VALUE_TYPE_INT, value2=3),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature1"], value1=VALUE_TYPE_INT, value2=4),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature2"], value1=VALUE_TYPE_INT, value2=1),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature2"], value1=VALUE_TYPE_INT, value2=2),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature2"], value1=VALUE_TYPE_INT, value2=3),
            Feature(feature_type=FEATURE_TYPE_LAG, columns=["feature2"], value1=VALUE_TYPE_INT, value2=4),
        ]
        self.assertListEqual(features, expected_features)
