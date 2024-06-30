from data_manager import exporter

EXPORT_ONLY_FROM_CAYMANCHEM = True

if __name__ == "__main__":
    exporter.export_data(EXPORT_ONLY_FROM_CAYMANCHEM)
    