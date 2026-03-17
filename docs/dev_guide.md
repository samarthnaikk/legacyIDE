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
- `examples/test.asm`: minimal sample input program
- `languages/asm_8051/cpu.py`: minimal CPU state (`A` register)
- `languages/asm_8051/instructions.py`: instruction representation
- `languages/asm_8051/parser.py`: parser for supported instruction subset
- `languages/asm_8051/instruction_logic.py`: instruction execution logic
- `languages/asm_8051/emulator.py`: sequential instruction execution engine

## How to use

From the project root:

```bash
python run.py examples/test.asm
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
- Any unsupported instruction raises a `ParserError` with line context.

## Emulator behavior

- Instructions are executed sequentially.
- Register `A` is always stored as 8-bit (`0..255`) using wrap-around behavior.
- All instruction semantics are implemented in `instruction_logic.py` to keep CPU state and operation logic separate.

## Extending instruction support

To add a new instruction:

1. Add parser recognition in `languages/asm_8051/parser.py`.
2. Add execution behavior in `languages/asm_8051/instruction_logic.py`.
3. Add an example in `examples/`.
4. Optionally update `run.py` output if additional state should be printed.

Keep new work minimal and isolated so the vertical slice remains clear and testable.
