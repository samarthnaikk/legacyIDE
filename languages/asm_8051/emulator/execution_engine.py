from collections.abc import Iterable

from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.instructions.instruction_set import ExecutionError, execute_instruction
from languages.asm_8051.parser.ast_nodes import InstructionNode


def execute(cpu: CPU, instructions: Iterable[InstructionNode]) -> CPU:
	program = list(instructions)
	pc = 0
	steps = 0
	max_steps = 200_000

	while 0 <= pc < len(program):
		steps += 1
		if steps > max_steps:
			raise ExecutionError("Execution step limit reached (possible infinite loop)")

		pc = execute_instruction(cpu, program[pc], pc)
		if pc == -1:
			break

	return cpu
