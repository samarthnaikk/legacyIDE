import re

from PySide6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter

from languages.asm_8051.metadata.syntax_rules import DIRECTIVES, INSTRUCTIONS, PORT_SYMBOLS, SPECIAL_FUNCTION_REGISTERS


def _format(*, color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
	text_format = QTextCharFormat()
	text_format.setForeground(QColor(color))
	if bold:
		text_format.setFontWeight(700)
	text_format.setFontItalic(italic)
	return text_format


class Asm8051SyntaxHighlighter(QSyntaxHighlighter):
	"""Simple 8051 syntax highlighter for the editor pane."""

	def __init__(self, document) -> None:
		super().__init__(document)

		self.comment_format = _format(color="#6A9955", italic=True)
		self.mnemonic_format = _format(color="#569CD6", bold=True)
		self.directive_format = _format(color="#C586C0", bold=True)
		self.register_format = _format(color="#4EC9B0")
		self.label_format = _format(color="#DCDCAA")
		self.number_format = _format(color="#B5CEA8")

		self.comment_re = re.compile(r";.*$")
		self.label_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:")
		self.number_re = re.compile(r"#\s*(?:0x[0-9A-Fa-f]+|0b[01]+|\d+)")

		self.mnemonic_patterns = self._build_token_patterns(INSTRUCTIONS)
		self.directive_patterns = self._build_token_patterns(DIRECTIVES)
		self.register_patterns = self._build_token_patterns((*SPECIAL_FUNCTION_REGISTERS, *PORT_SYMBOLS))

	@staticmethod
	def _build_token_patterns(tokens: tuple[str, ...]) -> list[re.Pattern[str]]:
		unique_tokens = sorted(set(tokens), key=len, reverse=True)
		return [
			re.compile(rf"(?<![A-Za-z0-9_.]){re.escape(token)}(?![A-Za-z0-9_.])", re.IGNORECASE)
			for token in unique_tokens
		]

	def _apply_pattern(self, text: str, pattern: re.Pattern[str], text_format: QTextCharFormat) -> None:
		for match in pattern.finditer(text):
			self.setFormat(match.start(), match.end() - match.start(), text_format)

	def highlightBlock(self, text: str) -> None:  # noqa: N802 (Qt naming style)
		self._apply_pattern(text, self.comment_re, self.comment_format)
		self._apply_pattern(text, self.number_re, self.number_format)

		label_match = self.label_re.match(text)
		if label_match:
			self.setFormat(label_match.start(1), label_match.end(1) - label_match.start(1), self.label_format)

		for pattern in self.mnemonic_patterns:
			self._apply_pattern(text, pattern, self.mnemonic_format)

		for pattern in self.directive_patterns:
			self._apply_pattern(text, pattern, self.directive_format)

		for pattern in self.register_patterns:
			self._apply_pattern(text, pattern, self.register_format)

