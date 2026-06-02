import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
import joblib


class MLModule:
    def __init__(self, kb, model_path="ml_model.pkl"):
        self.kb = kb
        self.model_path = model_path
        self.model = None

        # кэш структуры one-hot для категориальных признаков
        # {feat_name: possible_values_list}
        self.cat_schema = {
            feat: info["possible"]
            for feat, info in self.kb.features.items()
            if info["type"] != "integer"
        }

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

                    if feat in diag_features:
                        vals = diag_values.get(feat, normal)
                        val = random.choice(vals)
                    else:
                        if random.random() < 0.85:
                            val = random.choice(normal)
                        else:
                            val = random.choice(possible)

                    row.append(val)

                X.append(row)
                y.append(diag)

        return np.array(X, dtype=object), np.array(y)

    # ---------------------------------------------------------
    # One-hot кодирование категориальных признаков
    # ---------------------------------------------------------
    def _encode_row(self, row):
        """
        row: список значений признаков в порядке self.kb.features.keys()
        возвращает: числовой вектор (list[float])
        """
        new_row = []

        for i, feat in enumerate(self.kb.features.keys()):
            info = self.kb.features[feat]
            ftype = info["type"]
            val = row[i]

            if ftype == "integer":
                # просто числовое значение
                new_row.append(float(val))
            else:
                # one-hot по self.cat_schema[feat]
                possible = self.cat_schema[feat]
                for p in possible:
                    new_row.append(1.0 if val == p else 0.0)

        return new_row

    def _encode(self, X):
        """
        X: np.array shape (n_samples, n_features_raw)
        возвращает: np.array shape (n_samples, n_features_encoded)
        """
        X_new = []
        for row in X:
            X_new.append(self._encode_row(row))
        return np.array(X_new, dtype=float)

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

        # сохраняем вместе с информацией о размере признакового пространства
        self.model = model
        joblib.dump(
            {
                "model": model,
                "n_features_encoded": X_encoded.shape[1],
                "cat_schema": self.cat_schema,
                "feature_order": list(self.kb.features.keys()),
            },
            self.model_path
        )

    # ---------------------------------------------------------
    # Загрузка модели с авто‑переобучением при несовместимости
    # ---------------------------------------------------------
    def load(self):
        try:
            data = joblib.load(self.model_path)
            model = data["model"]
            n_features_encoded_saved = data["n_features_encoded"]
            saved_cat_schema = data.get("cat_schema", {})
            saved_feature_order = data.get("feature_order", [])

            # проверяем порядок признаков
            current_feature_order = list(self.kb.features.keys())
            if current_feature_order != saved_feature_order:
                print("⚠ Изменился порядок или состав признаков. Переобучение модели...")
                self.train()
                return

            # проверяем схему категориальных признаков
            current_cat_schema = {
                feat: info["possible"]
                for feat, info in self.kb.features.items()
                if info["type"] != "integer"
            }
            if current_cat_schema != saved_cat_schema:
                print("⚠ Изменились возможные значения категориальных признаков. Переобучение модели...")
                self.train()
                return

            # проверяем размерность закодированного пространства
            # (на случай, если что-то изменилось в кодировании)
            # создаём одну тестовую строку
            dummy_row = []
            for feat, info in self.kb.features.items():
                if info["type"] == "integer":
                    dummy_row.append(info["normal"][0])
                else:
                    dummy_row.append(info["possible"][0])

            dummy_encoded = np.array([self._encode_row(dummy_row)], dtype=float)
            n_features_encoded_current = dummy_encoded.shape[1]

            if n_features_encoded_current != n_features_encoded_saved:
                print("⚠ Изменилась размерность признакового пространства. Переобучение модели...")
                self.train()
                return

            # если всё совпало — используем загруженную модель
            self.model = model
            self.cat_schema = saved_cat_schema

        except Exception:
            print("⚠ Модель отсутствует или повреждена. Обучение новой модели...")
            self.train()

    # ---------------------------------------------------------
    # Предсказание
    # ---------------------------------------------------------
    def predict(self, instance):
        if self.model is None:
            self.load()

        # формируем строку признаков в порядке self.kb.features.keys()
        row = []
        for feat in self.kb.features.keys():
            row.append(instance[feat])

        row = np.array([row], dtype=object)
        row_encoded = self._encode(row)

        probs = self.model.predict_proba(row_encoded)[0]
        classes = self.model.classes_

        return list(zip(classes, probs))
