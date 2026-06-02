from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QPushButton, QMessageBox
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from knowledge_base import KnowledgeBase
from ui_editor_diagnoses import DiagnosesTab
from ui_editor_features import FeaturesTab
from ui_editor_diag_features import DiagnosisFeaturesTab
from ui_editor_diag_values import DiagnosisValuesTab
from ui_kb_check import KBCheckWindow


class KnowledgeEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор знаний")
        self.setAttribute(Qt.WA_DeleteOnClose)   # важно: корректное удаление окна

        self.kb = KnowledgeBase("knowledge_base.json")

        # --- вкладки ---
        self.tabs = QTabWidget()
        self.tab_diagnoses = DiagnosesTab(self.kb)
        self.tab_features = FeaturesTab(self.kb)
        self.tab_diag_features = DiagnosisFeaturesTab(self.kb)
        self.tab_diag_values = DiagnosisValuesTab(self.kb)

        self.tabs.addTab(self.tab_diagnoses, "Диагнозы")
        self.tabs.addTab(self.tab_features, "Признаки")
        self.tabs.addTab(self.tab_diag_features, "Описание признаков диагноза")
        self.tabs.addTab(self.tab_diag_values, "Значения признаков диагноза")

        # --- кнопка проверки ---
        self.btn_check = QPushButton("Проверить полноту базы знаний")
        self.btn_check.clicked.connect(self.open_kb_check)

        # --- layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.btn_check)
        self.setLayout(layout)

    # ---------------------------------------------------------
    # 🔍 ВАЛИДАЦИЯ БАЗЫ ЗНАНИЙ
    # ---------------------------------------------------------
    def validate_kb(self):
        errors = []
        kb = self.kb

        # --- проверка признаков ---
        for feat, info in kb.features.items():

            if "type" not in info:
                errors.append(f"Признак «{feat}» не имеет поля type.")
                continue

            if "possible" not in info or not info["possible"]:
                errors.append(f"Признак «{feat}» не имеет списка возможных значений.")

            if "normal" not in info or not info["normal"]:
                errors.append(f"Признак «{feat}» не имеет нормальных значений.")

            if info["type"] == "integer":
                normals = info["normal"]
                if (
                    not isinstance(normals, list)
                    or len(normals) != 2
                    or not all(isinstance(x, int) for x in normals)
                ):
                    errors.append(f"Признак «{feat}» имеет некорректный диапазон normal.")

        # --- проверка диагнозов ---
        for diag, info in kb.diagnoses.items():

            if diag == kb.healthy:
                continue

            feats = info.get("features", [])
            vals = info.get("values", {})

            if not feats:
                errors.append(f"Диагноз «{diag}» не содержит признаков.")
                continue

            for feat in feats:
                if feat not in kb.features:
                    errors.append(f"Диагноз «{diag}» ссылается на несуществующий признак «{feat}».")
                    continue

                if feat not in vals or not vals[feat]:
                    errors.append(
                        f"Диагноз «{diag}» не имеет диагностических значений для признака «{feat}»."
                    )

        return errors

    # ---------------------------------------------------------
    # 🔥 БЕЗОПАСНАЯ ПОДСВЕТКА ОШИБОК (исправляет падение 0xC0000409)
    # ---------------------------------------------------------
    def highlight_errors(self, errors):

        # безопасная очистка подсветки
        for tab in (
            self.tab_features,
            self.tab_diagnoses,
            self.tab_diag_features,
            self.tab_diag_values
        ):
            if tab is not None and hasattr(tab, "clear_highlight"):
                try:
                    tab.clear_highlight()
                except RuntimeError:
                    pass

        # подсветка ошибок
        for err in errors:

            # --- ошибки признаков ---
            if "Признак «" in err:
                feat = err.split("«")[1].split("»")[0]

                for tab in (
                    self.tab_features,
                    self.tab_diag_features,
                    self.tab_diag_values
                ):
                    if tab is not None and hasattr(tab, "highlight_feature"):
                        try:
                            tab.highlight_feature(feat)
                        except RuntimeError:
                            pass

            # --- ошибки диагнозов ---
            if "Диагноз «" in err:
                diag = err.split("«")[1].split("»")[0]

                for tab in (
                    self.tab_diagnoses,
                    self.tab_diag_features,
                    self.tab_diag_values
                ):
                    if tab is not None and hasattr(tab, "highlight_diagnosis"):
                        try:
                            tab.highlight_diagnosis(diag)
                        except RuntimeError:
                            pass

            # --- ошибки значений ---
            if "значений" in err and "для признака" in err:
                feat = err.split("признака «")[1].split("»")[0]

                if self.tab_diag_values is not None:
                    try:
                        self.tab_diag_values.highlight_feature(feat)
                    except RuntimeError:
                        pass

    def open_kb_check(self):
        errors = self.validate_kb()

        if errors:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Обнаружены ошибки в базе знаний:\n\n" + "\n".join(errors)
            )
            self.highlight_errors(errors)
            return

        self.check_window = KBCheckWindow()
        self.check_window.show()
