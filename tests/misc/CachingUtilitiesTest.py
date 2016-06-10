import os
import unittest

from pyprint.NullPrinter import NullPrinter

from coalib.misc.CachingUtilities import (
    get_settings_hash, settings_changed, update_settings_db,
    get_data_path, pickle_load, pickle_dump, delete_cache_files)
from coalib.misc.Caching import FileCache
from coalib.output.printers.LogPrinter import LogPrinter


class CachingUtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

    def test_pickling(self):
        test_data = {"answer": 42}

        pickle_dump(self.log_printer, "test_file", test_data)
        self.assertEqual(pickle_load(self.log_printer, "test_file"), test_data)
        os.remove(get_data_path(self.log_printer, "test_file"))

    def test_pickling_nonexistant_file(self):
        self.assertEqual(pickle_load(
            self.log_printer, "nonexistant_file"), None)
        self.assertEqual(pickle_load(
            self.log_printer, "nonexistant_file", fallback=42), 42)

    def test_corrupt_cache_files(self):
        file_path = get_data_path(self.log_printer, "corrupt_file")
        with open(file_path, "wb") as f:
            f.write(bytes([1] * 100))

        self.assertTrue(os.path.isfile(file_path))
        self.assertEqual(pickle_load(
            self.log_printer, "corrupt_file", fallback=42), 42)

    def test_delete_cache_files(self):
        pickle_dump(self.log_printer, "coala_test", {"answer": 42})
        self.assertTrue(delete_cache_files(
            self.log_printer, ["coala_test"]))
        self.assertFalse(os.path.isfile(get_data_path(
            self.log_printer, "coala_test")))

    def test_delete_invalid_file(self):
        self.assertFalse(delete_cache_files(
            self.log_printer, ["non_existant_file"]))

    @unittest.mock.patch("os.makedirs")
    def test_permission_error(self, makedirs):
        makedirs.side_effect = PermissionError
        self.assertEqual(get_data_path(self.log_printer, "test"), None)

        self.assertFalse(pickle_dump(self.log_printer, "test", {"answer": 42}))


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

    def test_settings_change(self):
        sections = {}
        settings_hash = get_settings_hash(sections)
        update_settings_db(self.log_printer, settings_hash)
        self.assertFalse(settings_changed(self.log_printer, settings_hash))

        sections = {"a": 1}
        settings_hash = get_settings_hash(sections)
        self.assertTrue(settings_changed(self.log_printer, settings_hash))
