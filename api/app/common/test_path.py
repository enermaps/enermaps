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
        name = path.make_unique_layer_name(path.AREA, "NUTS2", time_period=2015)
        self.assertEqual(name, "area/NUTS2")

    def testAreaLayerWithVariableAndTimePeriod(self):
        name = path.make_unique_layer_name(
            path.AREA, "NUTS2", variable="var", time_period=2015
        )
        self.assertEqual(name, "area/NUTS2")

    def testVectorLayer(self):
        name = path.make_unique_layer_name(path.VECTOR, 42)
        self.assertEqual(name, "vector/42")

    def testVectorLayerWithVariable(self):
        name = path.make_unique_layer_name(path.VECTOR, 42, variable="var")
        self.assertEqual(name, f"vector/42//{ENCODED_VAR}")

    def testVectorLayerWithTimePeriod(self):
        name = path.make_unique_layer_name(path.VECTOR, 42, time_period=2015)
        self.assertEqual(name, "vector/42/2015")

    def testVectorLayerWithVariableAndTimePeriod(self):
        name = path.make_unique_layer_name(
            path.VECTOR, 42, variable="var", time_period=2015
        )
        self.assertEqual(name, f"vector/42/2015/{ENCODED_VAR}")

    def testRasterLayer(self):
        name = path.make_unique_layer_name(path.RASTER, 42)
        self.assertEqual(name, "raster/42")

    def testRasterLayerWithVariable(self):
        name = path.make_unique_layer_name(path.RASTER, 42, variable="var")
        self.assertEqual(name, f"raster/42//{ENCODED_VAR}")

    def testRasterLayerWithTimePeriod(self):
        name = path.make_unique_layer_name(path.RASTER, 42, time_period=2015)
        self.assertEqual(name, "raster/42/2015")

    def testRasterLayerWithVariableAndTimePeriod(self):
        name = path.make_unique_layer_name(
            path.RASTER, 42, variable="var", time_period=2015
        )
        self.assertEqual(name, f"raster/42/2015/{ENCODED_VAR}")

    def testCMLayer(self):
        name = path.make_unique_layer_name(
            path.CM, "heat_demand_01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(name, "cm/heat_demand_01234567-0000-0000-0000-000000000000")

    def testCMLayerWithVariable(self):
        name = path.make_unique_layer_name(
            path.CM, "heat_demand_01234567-0000-0000-0000-000000000000", variable="var"
        )
        self.assertEqual(name, "cm/heat_demand_01234567-0000-0000-0000-000000000000")

    def testCMLayerWithTimePeriod(self):
        name = path.make_unique_layer_name(
            path.CM,
            "heat_demand_01234567-0000-0000-0000-000000000000",
            time_period=2015,
        )
        self.assertEqual(name, "cm/heat_demand_01234567-0000-0000-0000-000000000000")

    def testCMLayerWithVariableAndTimePeriod(self):
        name = path.make_unique_layer_name(
            path.CM,
            "heat_demand_01234567-0000-0000-0000-000000000000",
            variable="var",
            time_period=2015,
        )
        self.assertEqual(name, "cm/heat_demand_01234567-0000-0000-0000-000000000000")


class ParsePathTest(BaseApiTest):
    def testAreaLayer(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name("area/NUTS2")
        self.assertEqual(type, path.AREA)
        self.assertEqual(id, "NUTS2")
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)

    def testVectorLayer(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name("vector/42")
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)

    def testVectorLayerWithVariable(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            f"vector/42//{ENCODED_VAR}"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertTrue(time_period is None)

    def testVectorLayerWithTimePeriod(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            "vector/42/2015"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, 2015)

    def testVectorLayerWithVariableAndTimePeriod(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            f"vector/42/2015/{ENCODED_VAR}"
        )
        self.assertEqual(type, path.VECTOR)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertEqual(time_period, 2015)

    def testRasterLayer(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name("raster/42")
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertTrue(time_period is None)

    def testRasterLayerWithVariable(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            f"raster/42//{ENCODED_VAR}"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertTrue(time_period is None)

    def testRasterLayerWithTimePeriod(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            "raster/42/2015"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertTrue(variable is None)
        self.assertEqual(time_period, 2015)

    def testRasterLayerWithVariableAndTimePeriod(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            f"raster/42/2015/{ENCODED_VAR}"
        )
        self.assertEqual(type, path.RASTER)
        self.assertEqual(id, 42)
        self.assertEqual(variable, "var")
        self.assertEqual(time_period, 2015)

    def testCMLayer(self):
        (type, id, variable, time_period) = path.parse_unique_layer_name(
            "cm/heat_demand_01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(type, path.CM)
        self.assertEqual(id, "heat_demand_01234567-0000-0000-0000-000000000000")
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

    def testVectorLayerWithTimePeriod(self):
        type = path.get_type("vector/42/2015")
        self.assertEqual(type, path.VECTOR)

    def testVectorLayerWithVariableAndTimePeriod(self):
        type = path.get_type(f"vector/42/2015/{ENCODED_VAR}")
        self.assertEqual(type, path.VECTOR)

    def testRasterLayer(self):
        type = path.get_type("raster/42")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithVariable(self):
        type = path.get_type(f"raster/42//{ENCODED_VAR}")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithTimePeriod(self):
        type = path.get_type("raster/42/2015")
        self.assertEqual(type, path.RASTER)

    def testRasterLayerWithVariableAndTimePeriod(self):
        type = path.get_type(f"raster/42/2015/{ENCODED_VAR}")
        self.assertEqual(type, path.RASTER)

    def testCMLayer(self):
        type = path.get_type("cm/heat_demand_01234567-0000-0000-0000-000000000000")
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
        self.assertEqual(folder_path, f"42/{ENCODED_VAR}")

    def testVectorLayerWithTimePeriod(self):
        folder_path = path.to_folder_path("vector/42/2015")
        self.assertEqual(folder_path, "42/2015")

    def testVectorLayerWithVariableAndTimePeriod(self):
        folder_path = path.to_folder_path(f"vector/42/2015/{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/2015/{ENCODED_VAR}")

    def testRasterLayer(self):
        folder_path = path.to_folder_path("raster/42")
        self.assertEqual(folder_path, "42")

    def testRasterLayerWithVariable(self):
        folder_path = path.to_folder_path(f"raster/42//{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/{ENCODED_VAR}")

    def testRasterLayerWithTimePeriod(self):
        folder_path = path.to_folder_path("raster/42/2015")
        self.assertEqual(folder_path, "42/2015")

    def testRasterLayerWithVariableAndTimePeriod(self):
        folder_path = path.to_folder_path(f"raster/42/2015/{ENCODED_VAR}")
        self.assertEqual(folder_path, f"42/2015/{ENCODED_VAR}")

    def testCMLayer(self):
        folder_path = path.to_folder_path(
            "cm/heat_demand_01234567-0000-0000-0000-000000000000"
        )
        self.assertEqual(
            folder_path, "heat_demand_01234567-0000-0000-0000-000000000000"
        )
