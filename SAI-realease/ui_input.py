from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QSpinBox, QPushButton,
    QVBoxLayout, QFormLayout
)
from knowledge_base import KnowledgeBase
from expert_system import ExpertSystem
from ui_output import OutputWindow


class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ввод исходных данных")

        self.kb = KnowledgeBase("knowledge_base.json")
        self.es = ExpertSystem(self.kb)

        self.form = QFormLayout()
        self.widgets = {}

        # создаём виджеты строго в порядке признаков KB
        for feature in self.kb.features.keys():
            info = self.kb.features[feature]

            if info["type"] in ("binary", "categorical"):
                w = QComboBox()
                w.addItems(info["possible"])

                # установить нормальное значение
                normal_value = info["normal"][0]
                index = w.findText(normal_value)
                if index >= 0:
                    w.setCurrentIndex(index)

            elif info["type"] == "integer":
                w = QSpinBox()
                w.setRange(min(info["possible"]), max(info["possible"]))

                # ставим нижнюю границу нормального диапазона
                normal_value = info["normal"][0]
                w.setValue(normal_value)

            else:
                continue

            self.widgets[feature] = w
            self.form.addRow(QLabel(feature), w)

        self.btn = QPushButton("Определить диагноз")
        self.btn.clicked.connect(self.process)

        layout = QVBoxLayout()
        layout.addLayout(self.form)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def process(self):
        instance = {}

        # собираем значения признаков строго в порядке KB
        for feature in self.kb.features.keys():
            widget = self.widgets[feature]

            if isinstance(widget, QComboBox):
                instance[feature] = widget.currentText()
            else:
                instance[feature] = widget.value()

        # экспертная система
        suitable, explanations = self.es.diagnose(instance)

        # передаём instance в OutputWindow
        self.output_window = OutputWindow(suitable, explanations, instance)
        self.output_window.show()
