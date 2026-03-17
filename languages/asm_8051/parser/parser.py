import re
from difflib import get_close_matches

from languages.asm_8051.metadata.syntax_rules import DIRECTIVES, INSTRUCTIONS

from .ast_nodes import InstructionNode


class ParserError(ValueError):
	pass


_MOV_RE = re.compile(r"^MOV\s+(?:A\s*,\s*)?#(.+)$", re.IGNORECASE)
_ADD_RE = re.compile(r"^ADD\s+A\s*,\s*#(.+)$", re.IGNORECASE)
_SINGLE_TOKEN_RE = re.compile(r"^(INC|DEC|CPL)\s+A$", re.IGNORECASE)
_LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")
_ORG_RE = re.compile(r"^ORG\s+(.+)$", re.IGNORECASE)
_SUPPORTED_MNEMONICS = ["MOV", "ADD", "INC", "DEC", "CPL"]
_SUPPORTED_DIRECTIVES = ["ORG"]
_KNOWN_MNEMONICS = list(INSTRUCTIONS)
_KNOWN_DIRECTIVES = list(DIRECTIVES)


def _parse_value(raw_value: str, *, line_number: int, instruction: str) -> int:
	value_text = raw_value.strip()
	upper_text = value_text.upper()

	try:
		if upper_text.endswith("H"):
			return int(upper_text[:-1], 16)
		if upper_text.endswith("B"):
			return int(upper_text[:-1], 2)
		if upper_text.endswith("D"):
			return int(upper_text[:-1], 10)

		# Accept decimal literals with leading zeros (e.g. 04) as base-10.
		if re.fullmatch(r"[0-9]+", value_text):
			return int(value_text, 10)

		return int(value_text, 0)
	except ValueError as exc:
		raise ParserError(
			f"Line {line_number}: invalid immediate value '{value_text}' for {instruction} #value"
		) from exc


def _unsupported_instruction_error(line_number: int, stripped: str) -> ParserError:
	mnemonic = stripped.split(maxsplit=1)[0].rstrip(",").upper()
	if mnemonic in _SUPPORTED_DIRECTIVES:
		return ParserError(
			f"Line {line_number}: directive '{mnemonic}' is valid but this form is not supported."
		)

	if mnemonic in _KNOWN_MNEMONICS and mnemonic not in _SUPPORTED_MNEMONICS:
		return ParserError(
			f"Line {line_number}: instruction '{mnemonic}' is recognized but not yet executable in this minimal runtime. "
			f"Currently executable mnemonics: {', '.join(_SUPPORTED_MNEMONICS)}"
		)

	if mnemonic in _KNOWN_DIRECTIVES:
		return ParserError(
			f"Line {line_number}: directive '{mnemonic}' is recognized but not yet supported in this minimal runtime. "
			f"Currently supported directives: {', '.join(_SUPPORTED_DIRECTIVES)}"
		)

	suggestion = get_close_matches(mnemonic, _KNOWN_MNEMONICS + _KNOWN_DIRECTIVES, n=1, cutoff=0.6)
	if suggestion:
		return ParserError(
			f"Line {line_number}: unsupported instruction '{stripped}'. Did you mean '{suggestion[0]}'?"
		)

	return ParserError(
		f"Line {line_number}: unsupported instruction '{stripped}'. Supported mnemonics: {', '.join(_SUPPORTED_MNEMONICS)}"
	)


def parse_program(assembly_text: str) -> list[InstructionNode]:
	instructions: list[InstructionNode] = []
	labels: dict[str, int] = {}

	for line_number, raw_line in enumerate(assembly_text.splitlines(), start=1):
		stripped = raw_line.split(";", 1)[0].strip()
		if not stripped:
			continue

		while True:
			label_match = _LABEL_RE.match(stripped)
			if not label_match:
				break

			label_name = label_match.group(1).upper()
			if label_name in labels:
				raise ParserError(f"Line {line_number}: duplicate label '{label_name}'")

			labels[label_name] = len(instructions)
			stripped = label_match.group(2).strip()
			if not stripped:
				break

		if not stripped:
			continue

		org_match = _ORG_RE.match(stripped)
		if org_match:
			_parse_value(org_match.group(1), line_number=line_number, instruction="ORG")
			continue

		mov_match = _MOV_RE.match(stripped)
		if mov_match:
			instructions.append(
				InstructionNode(
					opcode="MOV",
					operand=_parse_value(mov_match.group(1), line_number=line_number, instruction="MOV"),
					line_number=line_number,
				)
			)
			continue

		add_match = _ADD_RE.match(stripped)
		if add_match:
			instructions.append(
				InstructionNode(
					opcode="ADD",
					operand=_parse_value(add_match.group(1), line_number=line_number, instruction="ADD"),
					line_number=line_number,
				)
			)
			continue

		single_token_match = _SINGLE_TOKEN_RE.match(stripped)
		if single_token_match:
			instructions.append(InstructionNode(opcode=single_token_match.group(1).upper(), line_number=line_number))
			continue

		raise _unsupported_instruction_error(line_number, stripped)

	return instructions
