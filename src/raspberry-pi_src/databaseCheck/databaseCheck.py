import json
import os
from typing import Union

# Caminho para o arquivo Database plates.json
DB_PATH = os.path.join(os.path.dirname(__file__), "plates.json")


def checkDatabase(license_plate: Union[str, None]) -> bool:
    """Recebe a string da placa e retorna True se estiver no banco, False se não."""
    if not license_plate or not isinstance(license_plate, str):
        return False

    clean_plate = license_plate.strip().upper()

    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                plates = json.load(f)
                return clean_plate in [p.strip().upper() for p in plates]
        except (json.JSONDecodeError, IOError):
            return False

    return False