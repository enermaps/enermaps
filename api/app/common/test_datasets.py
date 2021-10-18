from app.common import datasets
from app.common.test import BaseApiTest


class TestParametersTimePeriodsProcessing(BaseApiTest):
    def testCustomTimeGranularity(self):
        parameters = {
            "variables": [],
            "time_periods": ["2000", "2010", "2020"],
            "fields": {},
            "levels": [],
            "temporal_granularity": "custom",
            "start_at": "2000-01-01 00:00",
            "end_at": None,
            "default_parameters": {"start_at": "2020-01-01 00:00"},
        }

        datasets.process_parameters(parameters)

        self.assertEqual(parameters["time_periods"], ["2000", "2010", "2020"])
        self.assertEqual(parameters["temporal_granularity"], "custom")
        self.assertTrue("start_at" not in parameters["default_parameters"])

    def testYearTimeGranularity(self):
        parameters = {
            "variables": [],
            "time_periods": [],
            "fields": {},
            "levels": [],
            "temporal_granularity": "year",
            "start_at": "2000-01-01 00:00",
            "end_at": "2005-01-01 00:00",
            "default_parameters": {"start_at": "2005-01-01 00:00"},
        }

        datasets.process_parameters(parameters)

        self.assertEqual(
            parameters["time_periods"], ["2000", "2001", "2002", "2003", "2004", "2005"]
        )
        self.assertEqual(parameters["temporal_granularity"], "custom")
        self.assertTrue("start_at" not in parameters["default_parameters"])

    def testMonthTimeGranularitySmallPeriod(self):
        parameters = {
            "variables": [],
            "time_periods": [],
            "fields": {},
            "levels": [],
            "temporal_granularity": "month",
            "start_at": "2000-01-01 00:00",
            "end_at": "2000-12-01 00:00",
            "default_parameters": {"start_at": "2000-01-01 00:00"},
        }

        datasets.process_parameters(parameters)

        self.assertEqual(
            parameters["time_periods"],
            ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
        )
        self.assertEqual(parameters["temporal_granularity"], "custom")
        self.assertTrue("start_at" not in parameters["default_parameters"])

    def testMonthTimeGranularitySmallPeriodSpanningDifferentYears(self):
        parameters = {
            "variables": [],
            "time_periods": [],
            "fields": {},
            "levels": [],
            "temporal_granularity": "month",
            "start_at": "2000-06-01 00:00",
            "end_at": "2001-05-01 00:00",
            "default_parameters": {"start_at": "2000-01-01 00:00"},
        }

        datasets.process_parameters(parameters)

        self.assertEqual(
            parameters["time_periods"],
            [
                "2000-06",
                "2000-07",
                "2000-08",
                "2000-09",
                "2000-10",
                "2000-11",
                "2000-12",
                "2001-01",
                "2001-02",
                "2001-03",
                "2001-04",
                "2001-05",
            ],
        )
        self.assertEqual(parameters["temporal_granularity"], "custom")
        self.assertTrue("start_at" not in parameters["default_parameters"])

    def testMonthTimeGranularityBigPeriod(self):
        parameters = {
            "variables": [],
            "time_periods": [],
            "fields": {},
            "levels": [],
            "temporal_granularity": "month",
            "start_at": "2000-01-01 00:00",
            "end_at": "2005-12-01 00:00",
            "default_parameters": {"start_at": "2000-01-01 00:00"},
        }

        datasets.process_parameters(parameters)

        self.assertEqual(parameters["time_periods"], [])
        self.assertEqual(parameters["temporal_granularity"], "month")
        self.assertTrue("start_at" in parameters["default_parameters"])

    def testSixMonthTimeGranularity(self):
        parameters = {
            "variables": [],
            "time_periods": [],
            "fields": {},
            "levels": [],
            "temporal_granularity": "six-month",
            "start_at": "2000-01-01 00:00",
            "end_at": "2003-07-01 00:00",
            "default_parameters": {"start_at": "2000-01-01 00:00"},
        }

        datasets.process_parameters(parameters)

        self.assertEqual(
            parameters["time_periods"],
            [
                "2000-01",
                "2000-07",
                "2001-01",
                "2001-07",
                "2002-01",
                "2002-07",
                "2003-01",
                "2003-07",
            ],
        )
        self.assertEqual(parameters["temporal_granularity"], "custom")
        self.assertTrue("start_at" not in parameters["default_parameters"])
