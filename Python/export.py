from data_manager import exporter
from settings import EXPORT_ONLY_FROM_CAYMANCHEM

if __name__ == "__main__":
    exporter.export_data(EXPORT_ONLY_FROM_CAYMANCHEM)
    