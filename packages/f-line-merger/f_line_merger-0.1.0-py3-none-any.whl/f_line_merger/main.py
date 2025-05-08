from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QPushButton, QLabel
)
import sys

class LineBreakReplacer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Line Break Replacer (\\n)")
        self.setMinimumSize(800, 600)

        # Layout
        layout = QVBoxLayout()

        # Input Text
        layout.addWidget(QLabel("Input Text:"))
        self.input_box = QTextEdit()
        layout.addWidget(self.input_box)

        # Convert Button
        self.convert_button = QPushButton("Convert Line Breaks")
        self.convert_button.clicked.connect(self.replace_line_breaks)
        layout.addWidget(self.convert_button)

        # Output Text
        layout.addWidget(QLabel("Output Text (\\n replaced):"))
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def replace_line_breaks(self):
        input_text = self.input_box.toPlainText()
        converted = "\\n".join(input_text.splitlines())
        self.output_box.setPlainText(converted)

def main():
    app = QApplication(sys.argv)
    window = LineBreakReplacer()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()