from data_manager import importer, exporter


if __name__ == "__main__":
    # exporter.export_data(only_from_caymanchem=True)
    
    importer.import_data_from_file("./exports/substances.json", fix_substances=True)