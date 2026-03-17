from pathlib import Path

from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.emulator.emulator import Emulator
from languages.asm_8051.parser.parser import parse_program


def run_program(assembly_text: str):
	instructions = parse_program(assembly_text)
	return Emulator().run(instructions)


def run_program_file(path: str | Path):
	assembly_text = Path(path).read_text(encoding="utf-8")
	return run_program(assembly_text)


def format_exact_output(cpu: CPU) -> str:
	"""Return deterministic compiler-style output for current CPU state."""
	return "\n".join(
		[
			"OUTPUT:",
			f"A = {cpu.a}",
			f"A_HEX = 0x{cpu.a:02X}",
			f"A_BIN = 0b{cpu.a:08b}",
		]
	)
