from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from knowledge_base import KnowledgeBase


class KBCheckWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Проверка базы знаний")

        self.box = QTextEdit()
        self.box.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.box)
        self.setLayout(layout)

        self.run_check()

    def run_check(self):
        kb = KnowledgeBase("knowledge_base.json")
        errors = []

        # --- проверка признаков ---
        if not kb.features:
            errors.append("Ошибка: отсутствуют признаки.")

        for feat, info in kb.features.items():
            if "normal" not in info or not info["normal"]:
                errors.append(f"Ошибка: признак «{feat}» не имеет нормальных значений.")

            if "possible" not in info or not info["possible"]:
                errors.append(f"Ошибка: признак «{feat}» не имеет списка возможных значений.")

        # --- проверка диагнозов ---
        if not kb.diagnoses:
            errors.append("Ошибка: отсутствуют диагнозы.")

        for diag, info in kb.diagnoses.items():
            # диагноз "Исправен" — особый случай
            if diag == kb.healthy:
                continue

            feats = info.get("features", [])
            vals = info.get("values", {})

            if not feats:
                errors.append(f"Ошибка: диагноз «{diag}» не содержит признаков.")
                continue

            for feat in feats:
                if feat not in kb.features:
                    errors.append(f"Ошибка: диагноз «{diag}» ссылается на несуществующий признак «{feat}».")
                    continue

                if feat not in vals or not vals[feat]:
                    errors.append(
                        f"Ошибка: диагноз «{diag}» не имеет диагностических значений для признака «{feat}»."
                    )

        # --- вывод ---
        if errors:
            text = "Обнаружены ошибки:\n\n" + "\n".join(errors)
        else:
            text = (
                f"База знаний заполнена.\n"
                f"Признаков: {len(kb.features)}\n"
                f"Диагнозов: {len(kb.diagnoses)}"
            )

        self.box.setText(text)
