from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.emulator.execution_engine import execute
from languages.asm_8051.parser.ast_nodes import InstructionNode


class Emulator:
	def __init__(self, cpu: CPU | None = None) -> None:
		self.cpu = cpu or CPU()

	def run(self, instructions: list[InstructionNode]) -> CPU:
		return execute(self.cpu, instructions)
