# LegacyIDE Developer Guide (Minimal asm_8051 Slice)

This guide explains how to use and extend the minimal vertical slice implemented for 8051 assembly.

## What is implemented

The current implementation intentionally supports only:

- `MOV A,#value`
- `ADD A,#value`
- `INC A`
- `DEC A`
- `CPL A`

The execution flow is:

assembly file -> parser -> instruction list -> emulator -> CPU state

## Project files

- `run.py`: CLI entrypoint that loads an assembly file, parses, executes, and prints CPU state
- `examples/8051/counter.asm`: minimal sample input program
- `languages/asm_8051/cpu/cpu.py`: minimal CPU state (`A` register)
- `languages/asm_8051/parser/ast_nodes.py`: instruction node representation
- `languages/asm_8051/parser/parser.py`: parser for supported instruction subset
- `languages/asm_8051/instructions/instruction_set.py`: instruction dispatcher and execution entrypoint
- `languages/asm_8051/emulator/execution_engine.py`: sequential instruction execution loop
- `languages/asm_8051/language.py`: parser and emulator integration

## How to use

From the project root:

```bash
python run.py examples/8051/counter.asm
```

Launch GUI (PySide6):

```bash
python ui/app.py
```

Alternative launch mode:

```bash
python -m ui.app
```

Expected output:

```text
Running program...

MOV A,#5
ADD A,#3
INC A

Program finished

A = 9
```

## Parser behavior

- Lines are processed in order.
- Empty lines are ignored.
- Inline comments starting with `;` are ignored.
- Unsupported mnemonics raise a `ParserError` with line context and typo suggestions when possible.
- Invalid immediates report the exact failing line and instruction form.

## CLI behavior

- The runner prints only the first 10 lines of the source file as preview.
- If the file has more than 10 lines, a truncation line is printed.
- Parse and execution failures are reported as clean user-facing errors (no traceback by default).

## GUI behavior

- Includes source editor, run action, output console, and register panel.
- Uses the same parser and emulator pipeline as CLI.
- Shows parser and execution errors in the output panel with readable messages.
- Displays source preview with first 10 lines before execution.

## Emulator behavior

- Instructions are executed sequentially.
- Register `A` is always stored as 8-bit (`0..255`) using wrap-around behavior.
- Instruction semantics are implemented under `languages/asm_8051/instructions/` to keep CPU state and operation logic separate.

## Extending instruction support

To add a new instruction:

1. Add parser recognition in `languages/asm_8051/parser/parser.py`.
2. Add execution behavior in `languages/asm_8051/instructions/` and wire it in `instruction_set.py`.
3. Add an example in `examples/`.
4. Optionally update `run.py` output if additional state should be printed.

Keep new work minimal and isolated so the vertical slice remains clear and testable.
