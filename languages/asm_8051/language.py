from pathlib import Path

from languages.asm_8051.emulator.emulator import Emulator
from languages.asm_8051.parser.parser import parse_program


def run_program(assembly_text: str):
	instructions = parse_program(assembly_text)
	return Emulator().run(instructions)


def run_program_file(path: str | Path):
	assembly_text = Path(path).read_text(encoding="utf-8")
	return run_program(assembly_text)
