from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from languages.asm_8051.cpu.cpu import CPU


class RegisterPanel(QWidget):
	def __init__(self, parent=None) -> None:
		super().__init__(parent)

		self.a_value = QLabel("0 (0x00)")
		self.z_value = QLabel("1")
		self.r_values = [QLabel("0 (0x00)") for _ in range(8)]

		layout = QFormLayout()
		layout.addRow("A", self.a_value)
		layout.addRow("Z", self.z_value)
		for index, label in enumerate(self.r_values):
			layout.addRow(f"R{index}", label)
		self.setLayout(layout)

	def update_cpu(self, cpu: CPU) -> None:
		self.a_value.setText(f"{cpu.a} (0x{cpu.a:02X})")
		self.z_value.setText(str(int(cpu.z)))
		for index, label in enumerate(self.r_values):
			value = cpu.r[index]
			label.setText(f"{value} (0x{value:02X})")

	def reset(self) -> None:
		self.a_value.setText("0 (0x00)")
		self.z_value.setText("1")
		for label in self.r_values:
			label.setText("0 (0x00)")
