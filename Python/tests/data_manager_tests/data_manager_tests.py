from data_manager import importer, exporter
from database import database

import unittest
import json

class TestDataManager(unittest.TestCase):
    """IMPORTANT: Each test case must be run individually, as the import/export process is destructive.
    The export process will overwrite the file at ./Exports/substances.json.
    The import process will overwrite the database.
    """
    
    def run_import_export(self, test_name, fix_substances):
        database.clear_substances()
        
        import_file = f"./Python/tests/data_manager_tests/{test_name}_in.json"
        change_file = f"./Python/tests/data_manager_tests/{test_name}_change.json"
        export_file = f"./Python/tests/data_manager_tests/{test_name}_out.json"
        
        importer.import_data_from_file(import_file, fix_substances)
        importer.import_data_from_file(change_file, fix_substances)
        exporter.export_data(only_from_caymanchem=True)
        
        with open(export_file) as f:
            export_data = json.load(f)
        with open("./Exports/substances.json") as f:
            actual_data = json.load(f)
            
        
    
    def test_import_export_valid(self):
        self.run_import_export("test_valid", True)
    
    def test_import_export_invalid(self):
        self.run_import_export("test_invalid", True)
        
    def test_import_export_edit(self):
        self.run_import_export("test_edit", True)
    