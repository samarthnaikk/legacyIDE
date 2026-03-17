from PySide6.QtWidgets import QPlainTextEdit


class ConsoleWidget(QPlainTextEdit):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)
		self.setReadOnly(True)
		self.setPlaceholderText("Program output appears here...")

	def write_line(self, text: str) -> None:
		self.appendPlainText(text)

	def write_block(self, text: str) -> None:
		if text:
			self.appendPlainText(text)
