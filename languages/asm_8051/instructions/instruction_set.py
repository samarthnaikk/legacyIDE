from languages.asm_8051.cpu.cpu import CPU
from languages.asm_8051.instructions.arithmetic import add_a_immediate, dec_a, inc_a
from languages.asm_8051.instructions.data_transfer import mov_a_immediate
from languages.asm_8051.instructions.logical import cpl_a
from languages.asm_8051.parser.ast_nodes import InstructionNode


class ExecutionError(ValueError):
	pass


def _line_prefix(instruction: InstructionNode) -> str:
	if instruction.line_number > 0:
		return f"Line {instruction.line_number}: "
	return ""


def execute_instruction(cpu: CPU, instruction: InstructionNode) -> None:
	if instruction.opcode == "MOV":
		if instruction.operand is None:
			raise ExecutionError(f"{_line_prefix(instruction)}MOV requires an immediate operand")
		mov_a_immediate(cpu, instruction.operand)
		return

	if instruction.opcode == "ADD":
		if instruction.operand is None:
			raise ExecutionError(f"{_line_prefix(instruction)}ADD requires an immediate operand")
		add_a_immediate(cpu, instruction.operand)
		return

	if instruction.opcode == "INC":
		inc_a(cpu)
		return

	if instruction.opcode == "DEC":
		dec_a(cpu)
		return

	if instruction.opcode == "CPL":
		cpl_a(cpu)
		return

	raise ExecutionError(f"{_line_prefix(instruction)}unsupported opcode: {instruction.opcode}")
