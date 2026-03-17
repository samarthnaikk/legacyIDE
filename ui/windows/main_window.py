from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFileDialog,
	QMainWindow,
	QMessageBox,
	QSplitter,
	QTabWidget,
	QWidget,
)

from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.instructions.instruction_set import execute_instruction
from languages.asm_8051.instructions.instruction_set import ExecutionError
from languages.asm_8051.language import format_exact_output, run_program
from languages.asm_8051.parser.ast_nodes import InstructionNode
from languages.asm_8051.parser.parser import ParserError
from languages.asm_8051.parser.parser import parse_program
from ..components.console import ConsoleWidget
from ..components.status_bar import build_status_bar
from ..components.toolbar import build_main_toolbar
from ..panels.editor_panel import EditorPanel
from ..panels.memory_panel import MemoryPanel
from ..panels.port_panel import PortPanel
from ..panels.register_panel import RegisterPanel


class MainWindow(QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		self.current_file: Path | None = None
		self._step_source_snapshot: str | None = None
		self._step_cpu: CPU | None = None
		self._step_instructions: list[InstructionNode] = []
		self._step_pc: int = 0
		self._step_finished = True

		self.setWindowTitle("LegacyIDE - asm_8051")
		self.resize(1200, 760)

		self.editor_panel = EditorPanel(self)
		self.console = ConsoleWidget(self)
		self.register_panel = RegisterPanel(self)
		self.memory_panel = MemoryPanel(self)
		self.port_panel = PortPanel(self)

		toolbar = build_main_toolbar(
			self,
			on_new=self.new_file,
			on_open=self.open_file,
			on_save=self.save_file,
			on_run=self.run_program,
			on_step=self.step_program,
		)
		self.addToolBar(toolbar)
		self.setStatusBar(build_status_bar())
		self.setCentralWidget(self._build_layout())

	def _build_layout(self) -> QWidget:
		right_tabs = QTabWidget(self)
		right_tabs.addTab(self.register_panel, "Registers")
		right_tabs.addTab(self.memory_panel, "Memory")
		right_tabs.addTab(self.port_panel, "Ports")

		top_split = QSplitter(Qt.Orientation.Horizontal)
		top_split.addWidget(self.editor_panel)
		top_split.addWidget(right_tabs)
		top_split.setStretchFactor(0, 4)
		top_split.setStretchFactor(1, 2)

		vertical_split = QSplitter(Qt.Orientation.Vertical)
		vertical_split.addWidget(top_split)
		vertical_split.addWidget(self.console)
		vertical_split.setStretchFactor(0, 4)
		vertical_split.setStretchFactor(1, 1)
		return vertical_split

	def _update_title(self) -> None:
		file_name = self.current_file.name if self.current_file else "Untitled"
		self.setWindowTitle(f"LegacyIDE - {file_name}")

	def _show_error(self, title: str, message: str) -> None:
		QMessageBox.critical(self, title, message)
		self.statusBar().showMessage(message, 5000)

	def new_file(self) -> None:
		self.editor_panel.set_text("")
		self.current_file = None
		self._reset_step_session()
		self.register_panel.reset()
		self.console.clear()
		self._update_title()
		self.statusBar().showMessage("New file", 2000)

	def open_file(self) -> None:
		file_path, _ = QFileDialog.getOpenFileName(
			self,
			"Open Assembly File",
			str(Path.cwd()),
			"Assembly Files (*.asm);;All Files (*)",
		)
		if not file_path:
			return

		path = Path(file_path)
		try:
			source = self.editor_panel.read_file(path)
		except (OSError, UnicodeDecodeError) as exc:
			self._show_error("Open Failed", str(exc))
			return

		self.editor_panel.set_text(source)
		self.current_file = path
		self._reset_step_session()
		self._update_title()
		self.statusBar().showMessage(f"Opened {path.name}", 2000)

	def save_file(self) -> None:
		if self.current_file is None:
			file_path, _ = QFileDialog.getSaveFileName(
				self,
				"Save Assembly File",
				str(Path.cwd()),
				"Assembly Files (*.asm);;All Files (*)",
			)
			if not file_path:
				return
			self.current_file = Path(file_path)

		try:
			self.editor_panel.write_file(self.current_file)
		except OSError as exc:
			self._show_error("Save Failed", str(exc))
			return

		self._update_title()
		self.statusBar().showMessage(f"Saved {self.current_file.name}", 2000)

	def _reset_step_session(self) -> None:
		self._step_source_snapshot = None
		self._step_cpu = None
		self._step_instructions = []
		self._step_pc = 0
		self._step_finished = True

	def _render_live_output(self) -> None:
		if self._step_cpu is None:
			return
		self.console.write_block(format_exact_output(self._step_cpu))

	def _ensure_step_session(self, source: str) -> bool:
		if (
			not self._step_finished
			and self._step_source_snapshot == source
			and self._step_cpu is not None
			and self._step_instructions
		):
			return True

		try:
			instructions = parse_program(source)
		except ParserError as exc:
			self.console.write_line("\nParse error:")
			self.console.write_line(str(exc))
			self.statusBar().showMessage("Parse error", 5000)
			self._reset_step_session()
			return False

		self._step_source_snapshot = source
		self._step_cpu = CPU()
		self._step_instructions = instructions
		self._step_pc = 0
		self._step_finished = False
		self.console.clear()
		self.console.write_line("Step mode started")
		self.register_panel.update_cpu(self._step_cpu)
		self._render_live_output()
		return True

	def step_program(self) -> None:
		source = self.editor_panel.text()
		if not self._ensure_step_session(source):
			return

		if self._step_cpu is None:
			self._reset_step_session()
			return

		if not (0 <= self._step_pc < len(self._step_instructions)):
			self._step_finished = True
			self.console.write_line("\nProgram finished")
			self._render_live_output()
			self.statusBar().showMessage("Program finished", 3000)
			return

		instruction = self._step_instructions[self._step_pc]
		try:
			next_pc = execute_instruction(self._step_cpu, instruction, self._step_pc)
		except ExecutionError as exc:
			self.console.write_line("\nExecution error:")
			self.console.write_line(str(exc))
			self.statusBar().showMessage("Execution error", 5000)
			self._step_finished = True
			return

		self.console.write_line(
			f"Step line {instruction.line_number}: {instruction.opcode}"
		)
		self.register_panel.update_cpu(self._step_cpu)
		self.console.write_line("")
		self._render_live_output()

		if next_pc == -1:
			self._step_finished = True
			self._step_pc = len(self._step_instructions)
			self.console.write_line("\nProgram finished")
			self.statusBar().showMessage("Program finished", 3000)
			return

		self._step_pc = next_pc
		if not (0 <= self._step_pc < len(self._step_instructions)):
			self._step_finished = True
			self.console.write_line("\nProgram finished")
			self.statusBar().showMessage("Program finished", 3000)

	def run_program(self) -> None:
		source = self.editor_panel.text()
		self._reset_step_session()
		self.console.clear()
		self.console.write_line("Running program...")

		try:
			cpu = run_program(source)
		except ParserError as exc:
			self.console.write_line("\nParse error:")
			self.console.write_line(str(exc))
			self.statusBar().showMessage("Parse error", 5000)
			return
		except ExecutionError as exc:
			self.console.write_line("\nExecution error:")
			self.console.write_line(str(exc))
			self.statusBar().showMessage("Execution error", 5000)
			return
		except Exception as exc:
			self.console.write_line("\nUnexpected error:")
			self.console.write_line(str(exc))
			self.statusBar().showMessage("Unexpected error", 5000)
			return

		self.register_panel.update_cpu(cpu)
		self.console.write_line("\nProgram finished\n")
		self.console.write_block(format_exact_output(cpu))
		self.statusBar().showMessage("Program finished", 3000)
