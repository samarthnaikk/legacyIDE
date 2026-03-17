from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget

from core.editor.syntax_highlighter import Asm8051SyntaxHighlighter


class EditorPanel(QWidget):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)

		self.editor = QPlainTextEdit(self)
		self.editor.setPlaceholderText("Write 8051 assembly here...")
		self.editor.setFont(QFont("Menlo", 12))
		self.highlighter = Asm8051SyntaxHighlighter(self.editor.document())

		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.addWidget(self.editor)
		self.setLayout(layout)

	def text(self) -> str:
		return self.editor.toPlainText()

	def set_text(self, text: str) -> None:
		self.editor.setPlainText(text)

	def read_file(self, path: str | Path) -> str:
		return Path(path).read_text(encoding="utf-8")

	def write_file(self, path: str | Path) -> None:
		Path(path).write_text(self.text(), encoding="utf-8")
