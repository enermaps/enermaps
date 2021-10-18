from app.common import path
from app.common.test import BaseApiTest

ENCODED_VAR = path.encode("var")


class VariableEncodingTest(BaseApiTest):
    def testEncodingDecoding(self):
        encoded = path.encode("test")
        self.assertTrue(isinstance(encoded, str))

        decoded = path.decode(encoded)
        self.assertTrue(isinstance(decoded, str))
        self.assertEqual(decoded, "test")


class MakePathTest(BaseApiTest):
    def testAreaLayer(self):
        name = path.make_unique_layer_name(path.AREA, "NUTS2")
        self.assertEqual(name, "area/NUTS2")

    def testAreaLayerWithVariable(self):
        name = path.make_unique_layer_name(path.AREA, "NUTS2", variable="var")
        self.assertEqual(name, "area/NUTS2")

    def testAreaLayerWithTimePeriod(self):
        name = path.make_unique_layer_name(path.AREA, "NUTS2", time_period="2015")
        self.assertEqual(name, "area/NUTS2")

    def testAreaLayerWithVariableAndTimePeriod(self):
        name = path.make_unique_layer_name(
            path.AREA, "NUTS2", variable="var", time_period=2015
        )
        self.assertEqual(name, "area/NUTS2")

    def testAreaLayerWithTaskId(self):
        name = path.make_unique_layer_name(
            path.AREA, "NUTS2", task_id="01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(name, "area/NUTS2")

    def testVectorLayer(self):
        name = path.make_unique_layer_name(path.VECTOR, 42)
        self.assertEqual(name, "vector/42")

    def testVectorLayerWithVariable(self):
        name = path.make_unique_layer_name(path.VECTOR, 42, variable="var")
        self.assertEqual(name, f"vector/42//{ENCODED_VAR}")

    def testVectorLayerWithTimePeriodYear(self):
        name = path.make_unique_layer_name(path.VECTOR, 42, time_period="2015")
        self.assertEqual(name, "vector/42/2015")

    def testVectorLayerWithTimePeriodYearMonth(self):
        name = path.make_unique_layer_name(path.VECTOR, 42, time_period="2015-01")
        self.assertEqual(name, "vector/42/2015-01")

    def testVectorLayerWithNullTimePeriod(self):
        name = path.make_unique_layer_name(path.VECTOR, 42, time_period="None")
        self.assertEqual(name, "vector/42/None")

    def testVectorLayerWithVariableAndTimePeriodYear(self):
        name = path.make_unique_layer_name(
            path.VECTOR, 42, variable="var", time_period="2015"
        )
        self.assertEqual(name, f"vector/42/2015/{ENCODED_VAR}")

    def testVectorLayerWithVariableAndTimePeriodYearMonth(self):
        name = path.make_unique_layer_name(
            path.VECTOR, 42, variable="var", time_period="2015-01"
        )
        self.assertEqual(name, f"vector/42/2015-01/{ENCODED_VAR}")

    def testVectorLayerWithVariableAndNullTimePeriod(self):
        name = path.make_unique_layer_name(
            path.VECTOR, 42, variable="var", time_period="None"
        )
        self.assertEqual(name, f"vector/42/None/{ENCODED_VAR}")

    def testVectorLayerWithTaskId(self):
        name = path.make_unique_layer_name(
            path.VECTOR, 42, task_id="01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(name, "vector/42")

    def testRasterLayer(self):
        name = path.make_unique_layer_name(path.RASTER, 42)
        self.assertEqual(name, "raster/42")

    def testRasterLayerWithVariable(self):
        name = path.make_unique_layer_name(path.RASTER, 42, variable="var")
        self.assertEqual(name, f"raster/42//{ENCODED_VAR}")

    def testRasterLayerWithTimePeriodYear(self):
        name = path.make_unique_layer_name(path.RASTER, 42, time_period="2015")
        self.assertEqual(name, "raster/42/2015")

    def testRasterLayerWithTimePeriodYearMonth(self):
        name = path.make_unique_layer_name(path.RASTER, 42, time_period="2015-01")
        self.assertEqual(name, "raster/42/2015-01")

    def testRasterLayerWithNullTimePeriod(self):
        name = path.make_unique_layer_name(path.RASTER, 42, time_period="None")
        self.assertEqual(name, "raster/42/None")

    def testRasterLayerWithVariableAndTimePeriodYear(self):
        name = path.make_unique_layer_name(
            path.RASTER, 42, variable="var", time_period="2015"
        )
        self.assertEqual(name, f"raster/42/2015/{ENCODED_VAR}")

    def testRasterLayerWithVariableAndTimePeriodYearMonth(self):
        name = path.make_unique_layer_name(
            path.RASTER, 42, variable="var", time_period="2015-01"
        )
        self.assertEqual(name, f"raster/42/2015-01/{ENCODED_VAR}")

    def testRasterLayerWithVariableAndNullTimePeriod(self):
        name = path.make_unique_layer_name(
            path.RASTER, 42, variable="var", time_period="None"
        )
        self.assertEqual(name, f"raster/42/None/{ENCODED_VAR}")

    def testRasterLayerWithTaskId(self):
        name = path.make_unique_layer_name(
            path.RASTER, 42, task_id="01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(name, "raster/42")

    def testCMLayer(self):
        name = path.make_unique_layer_name(
            path.CM, "heat_demand", task_id="01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(name, "cm/heat_demand/01234567-0000-0000-0000-000000000000")

    def testCMLayerWithoutTaskId(self):
        name = path.make_unique_layer_name(path.CM, "heat_demand")
        self.assertTrue(name is None)

    def testCMLayerWithVariable(self):
        name = path.make_unique_layer_name(
            path.CM,
            "heat_demand",
            task_id="01234567-0000-0000-0000-000000000000",
            variable="var",
        )
        self.assertEqual(name, "cm/heat_demand/01234567-0000-0000-0000-000000000000")

    def testCMLayerWithTimePeriod(self):
        name = path.make_unique_layer_name(
            path.CM,
            "heat_demand",
            task_id="01234567-0000-0000-0000-000000000000",
            time_period=2015,
        )
        self.assertEqual(name, "cm/heat_demand/01234567-0000-0000-0000-000000000000")

    def testCMLayerWithVariableAndTimePeriod(self):
        name = path.make_unique_layer_name(
            path.CM,
            "heat_demand",
            task_id="01234567-0000-0000-0000-000000000000",
            variable="var",
            time_period=2015,
        )
        self.assertEqual(name, "cm/heat_demand/01234567-0000-0000-0000-000000000000")

    def testVectorLayerWithInvalidTimePeriod1(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="abcd")
        )

    def testVectorLayerWithInvalidTimePeriod2(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="2015-0a")
        )

    def testVectorLayerWithInvalidTimePeriod3(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="20a5")
        )

    def testVectorLayerWithInvalidTimePeriod4(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="201")
        )

    def testVectorLayerWithInvalidTimePeriod5(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="20150")
        )

    def testVectorLayerWithInvalidTimePeriod6(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="2015-001")
        )

    def testVectorLayerWithInvalidTimePeriod7(self):
        self.assertFalse(
            path.make_unique_layer_name(path.VECTOR, 42, time_period="2015-01-01")
        )


class ParsePathTest(BaseApiTest):
    def testAreaLayer(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "area/NUTS2"
        )
        self.assertEqual(type, path.AREA)
        self.assertEqual(id, "NUTS2")
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)
        self.assertTrue(task_id is None)

    def testVectorLayer(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "vector/42"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)
        self.assertTrue(task_id is None)

    def testVectorLayerWithVariable(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            f"vector/42//{ENCODED_VAR}"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertTrue(time_period is None)
        self.assertTrue(task_id is None)

    def testVectorLayerWithTimePeriodYearOnly(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "vector/42/2015"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, "2015")
        self.assertTrue(task_id is None)

    def testVectorLayerWithTimePeriodYearMonth(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "vector/42/2015-01"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, "2015-01")
        self.assertTrue(task_id is None)

    def testVectorLayerWithNullTimePeriod(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "vector/42/None"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, "None")
        self.assertTrue(task_id is None)

    def testVectorLayerWithVariableAndTimePeriodYear(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            f"vector/42/2015/{ENCODED_VAR}"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertEqual(time_period, "2015")
        self.assertTrue(task_id is None)

    def testVectorLayerWithVariableAndTimePeriodYearMonth(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            f"vector/42/2015-01/{ENCODED_VAR}"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertEqual(time_period, "2015-01")
        self.assertTrue(task_id is None)

    def testVectorLayerWithVariableAndNullTimePeriod(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            f"vector/42/None/{ENCODED_VAR}"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertEqual(time_period, "None")
        self.assertTrue(task_id is None)

    def testRasterLayer(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "raster/42"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)
        self.assertTrue(task_id is None)

    def testRasterLayerWithVariable(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            f"raster/42//{ENCODED_VAR}"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertTrue(time_period is None)
        self.assertTrue(task_id is None)

    def testRasterLayerWithTimePeriodYear(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "raster/42/2015"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, "2015")
        self.assertTrue(task_id is None)

    def testRasterLayerWithTimePeriodYearMonth(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "raster/42/2015-01"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, "2015-01")
        self.assertTrue(task_id is None)

    def testRasterLayerWithNullTimePeriod(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "raster/42/None"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, "None")
        self.assertTrue(task_id is None)

    def testRasterLayerWithVariableAndTimePeriod(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            f"raster/42/2015/{ENCODED_VAR}"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertEqual(time_period, "2015")
        self.assertTrue(task_id is None)

    def testCMLayer(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "cm/heat_demand/01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(type, path.CM)
        self.assertEqual(id, "heat_demand")
        self.assertEqual(task_id, "01234567-0000-0000-0000-000000000000")
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)

    def testCMLayerWithoutTaskId(self):
        (type, id, variable, time_period, task_id) = path.parse_unique_layer_name(
            "cm/heat_demand"
        )
        self.assertTrue(type is None)
        self.assertTrue(id is None)
        self.assertTrue(task_id is None)
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)


class GetTypeTest(BaseApiTest):
    def testAreaLayer(self):
        type = path.get_type("area/NUTS2")
        self.assertEqual(type, path.AREA)

    def testVectorLayer(self):
        type = path.get_type("vector/42")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithVariable(self):
        type = path.get_type(f"vector/42//{ENCODED_VAR}")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithTimePeriodYear(self):
        type = path.get_type("vector/42/2015")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithTimePeriodYearMonth(self):
        type = path.get_type("vector/42/2015-01")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithNullTimePeriod(self):
        type = path.get_type("vector/42/None")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithVariableAndTimePeriodYear(self):
        type = path.get_type(f"vector/42/2015/{ENCODED_VAR}")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithVariableAndTimePeriodYearMonth(self):
        type = path.get_type(f"vector/42/2015-01/{ENCODED_VAR}")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithVariableAndNullTimePeriod(self):
        type = path.get_type(f"vector/42/None/{ENCODED_VAR}")
        self.assertEqual(type, path.VECTOR)

    def testRasterLayer(self):
        type = path.get_type("raster/42")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithVariable(self):
        type = path.get_type(f"raster/42//{ENCODED_VAR}")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithTimePeriodYear(self):
        type = path.get_type("raster/42/2015")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithTimePeriodYearMonth(self):
        type = path.get_type("raster/42/2015-01")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithNullTimePeriod(self):
        type = path.get_type("raster/42/None")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithVariableAndTimePeriodYear(self):
        type = path.get_type(f"raster/42/2015/{ENCODED_VAR}")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithVariableAndTimePeriodYearMonth(self):
        type = path.get_type(f"raster/42/2015-01/{ENCODED_VAR}")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithVariableAndNullTimePeriod(self):
        type = path.get_type(f"raster/42/None/{ENCODED_VAR}")
        self.assertEqual(type, path.RASTER)

    def testCMLayer(self):
        type = path.get_type("cm/heat_demand/01234567-0000-0000-0000-000000000000")
        self.assertEqual(type, path.CM)


class ToFolderPathTest(BaseApiTest):
    def testAreaLayer(self):
        folder_path = path.to_folder_path("area/NUTS2")
        self.assertEqual(folder_path, "NUTS2")

    def testVectorLayer(self):
        folder_path = path.to_folder_path("vector/42")
        self.assertEqual(folder_path, "42")

    def testVectorLayerWithVariable(self):
        folder_path = path.to_folder_path(f"vector/42//{ENCODED_VAR}")
        self.assertEqual(folder_path, "42")

    def testVectorLayerWithTimePeriodYear(self):
        folder_path = path.to_folder_path("vector/42/2015")
        self.assertEqual(folder_path, "42/2015")

    def testVectorLayerWithTimePeriodYearMonth(self):
        folder_path = path.to_folder_path("vector/42/2015-01")
        self.assertEqual(folder_path, "42/2015-01")

    def testVectorLayerWithNullTimePeriod(self):
        folder_path = path.to_folder_path("vector/42/None")
        self.assertEqual(folder_path, "42/None")

    def testVectorLayerWithVariableAndTimePeriodYear(self):
        folder_path = path.to_folder_path(f"vector/42/2015/{ENCODED_VAR}")
        self.assertEqual(folder_path, "42/2015")

    def testVectorLayerWithVariableAndTimePeriodYearMonth(self):
        folder_path = path.to_folder_path(f"vector/42/2015-01/{ENCODED_VAR}")
        self.assertEqual(folder_path, "42/2015-01")

    def testVectorLayerWithVariableAndNullTimePeriod(self):
        folder_path = path.to_folder_path(f"vector/42/None/{ENCODED_VAR}")
        self.assertEqual(folder_path, "42/None")

    def testRasterLayer(self):
        folder_path = path.to_folder_path("raster/42")
        self.assertEqual(folder_path, "42")

    def testRasterLayerWithVariable(self):
        folder_path = path.to_folder_path(f"raster/42//{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/{ENCODED_VAR}")

    def testRasterLayerWithTimePeriodYear(self):
        folder_path = path.to_folder_path("raster/42/2015")
        self.assertEqual(folder_path, "42/2015")

    def testRasterLayerWithTimePeriodYearMonth(self):
        folder_path = path.to_folder_path("raster/42/2015-01")
        self.assertEqual(folder_path, "42/2015-01")

    def testRasterLayerWithNullTimePeriod(self):
        folder_path = path.to_folder_path("raster/42/None")
        self.assertEqual(folder_path, "42/None")

    def testRasterLayerWithVariableAndTimePeriodYear(self):
        folder_path = path.to_folder_path(f"raster/42/2015/{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/2015/{ENCODED_VAR}")

    def testRasterLayerWithVariableAndTimePeriodYearMonth(self):
        folder_path = path.to_folder_path(f"raster/42/2015-01/{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/2015-01/{ENCODED_VAR}")

    def testRasterLayerWithVariableAndNullTimePeriod(self):
        folder_path = path.to_folder_path(f"raster/42/None/{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/None/{ENCODED_VAR}")

    def testCMLayer(self):
        folder_path = path.to_folder_path(
            "cm/heat_demand/01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(
            folder_path, "heat_demand/01/23/45/67/01234567-0000-0000-0000-000000000000"
        )
