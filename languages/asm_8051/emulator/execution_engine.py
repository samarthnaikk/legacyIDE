from collections.abc import Iterable

from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.instructions.instruction_set import execute_instruction
from languages.asm_8051.parser.ast_nodes import InstructionNode


def execute(cpu: CPU, instructions: Iterable[InstructionNode]) -> CPU:
	for instruction in instructions:
		execute_instruction(cpu, instruction)
	return cpu
