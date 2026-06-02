import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
import joblib


class MLModule:
    def __init__(self, kb, model_path="ml_model.pkl"):
        self.kb = kb
        self.model_path = model_path
        self.model = None

    # ---------------------------------------------------------
    # Генерация большого синтетического датасета
    # ---------------------------------------------------------
    def generate_dataset(self, samples_per_diag=300):
        X = []
        y = []

        for diag, info in self.kb.diagnoses.items():
            diag_features = info["features"]
            diag_values = info["values"]

            for _ in range(samples_per_diag):
                row = []

                for feat, f_info in self.kb.features.items():
                    possible = f_info["possible"]
                    normal = f_info["normal"]

                    # Если признак относится к диагнозу → берём одно из значений диагноза
                    if feat in diag_features:
                        vals = diag_values.get(feat, normal)
                        val = random.choice(vals)

                    else:
                        # Признак не относится к диагнозу → чаще нормальное значение
                        if random.random() < 0.85:
                            val = random.choice(normal)
                        else:
                            # иногда — любое допустимое
                            val = random.choice(possible)

                    row.append(val)

                X.append(row)
                y.append(diag)

        return np.array(X), np.array(y)

    # ---------------------------------------------------------
    # Кодирование категориальных признаков
    # ---------------------------------------------------------
    def _encode(self, X):
        X_new = []

        for row in X:
            new_row = []
            for i, feat in enumerate(self.kb.features.keys()):
                ftype = self.kb.features[feat]["type"]
                val = row[i]

                if ftype == "integer":
                    new_row.append(val)
                else:
                    possible = self.kb.features[feat]["possible"]
                    new_row.append(possible.index(val))

            X_new.append(new_row)

        return np.array(X_new)

    # ---------------------------------------------------------
    # Обучение модели
    # ---------------------------------------------------------
    def train(self):
        X, y = self.generate_dataset()

        X_encoded = self._encode(X)

        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1
        )
        model.fit(X_encoded, y)

        joblib.dump(model, self.model_path)
        self.model = model

    # ---------------------------------------------------------
    # Загрузка модели
    # ---------------------------------------------------------
    def load(self):
        try:
            model = joblib.load(self.model_path)

            # --- Проверяем совместимость модели с текущей базой знаний ---
            # Модель хранит количество признаков в деревьях
            n_features_model = model.n_features_in_
            n_features_kb = len(self.kb.features)

            if n_features_model != n_features_kb:
                print("⚠ Обнаружено изменение структуры признаков. Переобучение модели...")
                self.train()
            else:
                self.model = model

        except Exception:
            # если файл отсутствует или повреждён — обучаем заново
            print("⚠ Модель отсутствует или повреждена. Обучение новой модели...")
            self.train()

    # ---------------------------------------------------------
    # Предсказание
    # ---------------------------------------------------------
    def predict(self, instance):
        if self.model is None:
            self.load()

        row = []
        for feat in self.kb.features.keys():
            row.append(instance[feat])

        row = np.array([row])
        row_encoded = self._encode(row)

        probs = self.model.predict_proba(row_encoded)[0]
        classes = self.model.classes_

        return list(zip(classes, probs))
