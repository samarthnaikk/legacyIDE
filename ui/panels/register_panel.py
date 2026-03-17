from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from languages.asm_8051.cpu.cpu import CPU


class RegisterPanel(QWidget):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)

		self.a_value = QLabel("0 (0x00)")

		layout = QFormLayout()
		layout.addRow("A", self.a_value)
		self.setLayout(layout)

	def update_cpu(self, cpu: CPU) -> None:
		self.a_value.setText(f"{cpu.a} (0x{cpu.a:02X})")

	def reset(self) -> None:
		self.a_value.setText("0 (0x00)")
