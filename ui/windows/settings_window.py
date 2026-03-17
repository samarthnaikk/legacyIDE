from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsWindow(QWidget):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowTitle("Settings")

		label = QLabel("Settings are not implemented in the minimal slice.")
		label.setWordWrap(True)

		layout = QVBoxLayout()
		layout.addWidget(label)
		self.setLayout(layout)
