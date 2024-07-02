from data_manager import exporter
from settings import EXPORT_ONLY_FROM_CAYMANCHEM

import os

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), '../Exports')
    exporter.export_data(path, EXPORT_ONLY_FROM_CAYMANCHEM)
    