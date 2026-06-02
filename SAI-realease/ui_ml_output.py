from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout

class MLOutputWindow(QWidget):
    def __init__(self, preds):
        super().__init__()
        self.setWindowTitle("Результаты ML-модуля")

        self.box = QTextEdit()
        self.box.setReadOnly(True)

        text = "Результаты ML-модуля:\n\n"
        for diag, prob in preds:
            text += f"{diag}: {prob:.3f}\n"

        self.box.setText(text)

        layout = QVBoxLayout()
        layout.addWidget(self.box)
        self.setLayout(layout)
