from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PortPanel(QWidget):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)

		label = QLabel("Port view is not implemented in the minimal slice.")
		label.setWordWrap(True)

		layout = QVBoxLayout()
		layout.addWidget(label)
		layout.addStretch(1)
		self.setLayout(layout)
