import re

from .ast_nodes import InstructionNode


class ParserError(ValueError):
	pass


_MOV_RE = re.compile(r"^MOV\s+A\s*,\s*#(.+)$", re.IGNORECASE)
_ADD_RE = re.compile(r"^ADD\s+A\s*,\s*#(.+)$", re.IGNORECASE)
_SINGLE_TOKEN_RE = re.compile(r"^(INC|DEC|CPL)\s+A$", re.IGNORECASE)


def _parse_value(raw_value: str) -> int:
	value_text = raw_value.strip()
	try:
		return int(value_text, 0)
	except ValueError as exc:
		raise ParserError(f"Invalid immediate value: {value_text}") from exc


def parse_program(assembly_text: str) -> list[InstructionNode]:
	instructions: list[InstructionNode] = []

	for line_number, raw_line in enumerate(assembly_text.splitlines(), start=1):
		stripped = raw_line.split(";", 1)[0].strip()
		if not stripped:
			continue

		mov_match = _MOV_RE.match(stripped)
		if mov_match:
			instructions.append(InstructionNode(opcode="MOV", operand=_parse_value(mov_match.group(1))))
			continue

		add_match = _ADD_RE.match(stripped)
		if add_match:
			instructions.append(InstructionNode(opcode="ADD", operand=_parse_value(add_match.group(1))))
			continue

		single_token_match = _SINGLE_TOKEN_RE.match(stripped)
		if single_token_match:
			instructions.append(InstructionNode(opcode=single_token_match.group(1).upper()))
			continue

		raise ParserError(f"Line {line_number}: unsupported instruction '{stripped}'")

	return instructions
