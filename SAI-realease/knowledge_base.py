import json
import os
from typing import Dict, List, Any


class KnowledgeBase:
    def __init__(self, path: str):
        self.path = path

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.full_path = os.path.join(base_dir, path)

        with open(self.full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.features: Dict[str, Dict[str, Any]] = data["features"]
        self.diagnoses: Dict[str, Dict[str, Any]] = data["diagnoses"]
        self.healthy: str = data["healthy_diagnosis"]

    # -----------------------------
    # Сохранение
    # -----------------------------
    def save(self):
        data = {
            "features": self.features,
            "diagnoses": self.diagnoses,
            "healthy_diagnosis": self.healthy
        }
        with open(self.full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # -----------------------------
    # Работа с признаками
    # -----------------------------
    def add_feature(self, name: str, ftype: str, possible: List[Any], normal: List[Any]):
        self.features[name] = {
            "type": ftype,
            "possible": possible,
            "normal": normal
        }
        self.save()

    def remove_feature(self, name: str):
        if name in self.features:
            del self.features[name]
        # удалить из всех диагнозов
        for diag in self.diagnoses.values():
            if name in diag["features"]:
                diag["features"].remove(name)
            if name in diag["values"]:
                del diag["values"][name]
        self.save()

    def update_feature(self, name: str, ftype=None, possible=None, normal=None):
        if ftype is not None:
            self.features[name]["type"] = ftype
        if possible is not None:
            self.features[name]["possible"] = possible
        if normal is not None:
            self.features[name]["normal"] = normal
        self.save()

    # -----------------------------
    # Работа с диагнозами
    # -----------------------------
    def add_diagnosis(self, name: str):
        self.diagnoses[name] = {
            "features": [],
            "values": {}
        }
        self.save()

    def remove_diagnosis(self, name: str):
        if name == self.healthy:
            return  # нельзя удалить "Исправен"
        if name in self.diagnoses:
            del self.diagnoses[name]
        self.save()

    def set_diag_features(self, diag: str, features: List[str]):
        self.diagnoses[diag]["features"] = features
        # очистить значения, которых нет в features
        for f in list(self.diagnoses[diag]["values"].keys()):
            if f not in features:
                del self.diagnoses[diag]["values"][f]
        self.save()


    # -----------------------------
    # Геттеры для чтения базы знаний
    # -----------------------------
    def get_features(self) -> List[str]:
        return list(self.features.keys())

    def get_possible_values(self, feature: str):
        return self.features[feature]["possible"]

    def get_normal_values(self, feature: str):
        return self.features[feature]["normal"]

    def get_feature_type(self, feature: str):
        return self.features[feature]["type"]

    def get_diagnoses(self) -> List[str]:
        return list(self.diagnoses.keys())

    def get_diag_features(self, diag: str) -> List[str]:
        return self.diagnoses[diag]["features"]

    def get_diag_values(self, diag: str, feature: str):
        return self.diagnoses[diag]["values"].get(feature, [])
