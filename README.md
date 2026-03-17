# LegacyIDE
*A modern IDE for running and experimenting with legacy and hard-to-access programming languages*

---

# Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI sample:

```bash
python run.py examples/8051/counter.asm
```

Launch the PySide6 desktop interface:

```bash
python ui/app.py
```

Alternative module mode:

```bash
python -m ui.app
```

---

# Overview

LegacyIDE is a lightweight development environment designed to make it easy to write, run, and experiment with programming languages that are typically difficult to access on modern systems. Many classic or embedded languages require specialized compilers, proprietary IDEs, or outdated software environments. LegacyIDE aims to remove those barriers by providing a unified platform where such languages can be executed through built-in emulation and interpretation.

The first language supported by LegacyIDE is **8051 Assembly**, a low-level language used to program the widely known :contentReference[oaicite:0]{index=0} architecture. Traditionally, development for this platform requires proprietary tools such as :contentReference[oaicite:1]{index=1} or hardware-dependent toolchains. LegacyIDE replaces this requirement by implementing a software-based emulator that replicates the behavior of the 8051 processor.

The long-term goal of LegacyIDE is to expand support to additional legacy, embedded, and niche programming languages that are otherwise difficult to run in modern environments.

---

# Purpose

LegacyIDE was created to solve several common problems faced by students, hobbyists, and developers who want to experiment with older or specialized programming languages:

- Many legacy languages require proprietary software.
- Some development tools only run on specific operating systems.
- Installation and configuration can be complex for beginners.
- Error messages in traditional assemblers are often unclear.
- Visualization of hardware behavior is limited.

LegacyIDE addresses these issues by providing a modern, simplified environment that emulates hardware behavior while offering better feedback and usability.

---

# Key Features

## Integrated Code Editor

LegacyIDE includes a built-in editor for writing assembly programs. The editor allows users to write and edit programs directly inside the environment without relying on external text editors.

The editor supports standard 8051 assembly syntax and provides a clean workspace designed for low-level programming.

---

## Assembly Parsing and Validation

Before execution, LegacyIDE processes the program through an internal parser.

The parser performs several steps:

- Identifies instructions and operands
- Validates syntax
- Detects invalid instructions
- Resolves labels and jump targets
- Converts assembly instructions into executable operations

If errors are found, the IDE reports them clearly along with the corresponding line number and explanation.

---

# 8051 Microcontroller Emulation

The core of LegacyIDE is a software emulator that simulates the behavior of the **8051 microcontroller architecture**.

Instead of executing machine code on real hardware, the IDE interprets instructions and updates an internal representation of the processor state.

This allows assembly programs to run as if they were executing on a real 8051 chip.

---

## CPU Simulation

The emulator replicates the internal components of the processor including:

- Accumulator (A)
- B register
- Program Counter (PC)
- Stack Pointer (SP)
- Program Status Word (PSW)
- Register banks (R0–R7)

Each instruction modifies these registers according to the rules of the 8051 instruction set.

The state of the CPU can be viewed during program execution to understand how each instruction affects the processor.

---

## Memory Simulation

LegacyIDE maintains a virtual representation of the **8051 internal RAM**.

Programs can access and modify memory using standard addressing modes such as:

- Immediate addressing
- Direct addressing
- Register addressing
- Indirect addressing

The IDE allows users to observe memory values while the program is running.

---

## Port Simulation

The emulator also simulates the microcontroller's digital input/output ports:

- P0
- P1
- P2
- P3

Programs can manipulate individual bits of these ports using instructions such as:

- SETB
- CLR
- CPL

The IDE visually displays port values so users can observe digital output changes in real time.

---

# Instruction Execution Model

LegacyIDE executes programs using a simplified version of the processor’s instruction cycle.

For each instruction:

1. The instruction is fetched from program memory.
2. The instruction is decoded.
3. The corresponding operation is executed.
4. The program counter advances to the next instruction.

Branch instructions modify the program counter to change program flow.

This model closely mirrors how the real 8051 processor operates.

---

# Debugging and Execution Control

LegacyIDE includes several execution modes to help users understand program behavior.

### Run Mode
Executes the program continuously until it finishes or enters an infinite loop.

### Step Mode
Executes one instruction at a time so users can observe how registers and memory change.

### Register Monitoring
Users can view the values of CPU registers during execution.

### Memory Monitoring
Internal RAM values can be inspected while the program runs.

These tools make it easier to understand the effects of assembly instructions.

---

# Educational Focus

LegacyIDE is designed primarily as a learning tool. By simulating hardware behavior and exposing internal processor states, the IDE allows users to see exactly how assembly instructions affect the system.

This makes it particularly useful for:

- Embedded systems students
- Microcontroller programming courses
- Assembly language learners
- Hobbyists experimenting with classic architectures

---

# Future Goals

LegacyIDE is designed to support additional languages in the future. Possible expansions include other legacy or embedded programming environments that currently lack accessible development tools.

Potential future additions may include:

- Additional microcontroller assembly languages
- Legacy programming languages
- Hardware simulation modules
- Enhanced debugging tools
- Visual hardware interaction interfaces

The long-term vision is to create a unified development platform for experimenting with legacy and specialized programming languages.

---

# Philosophy

LegacyIDE is built around the idea that older programming technologies should remain accessible. Many foundational computing concepts were developed using low-level languages and microcontroller architectures, yet the tools required to explore them are often outdated or difficult to use.

By recreating these environments in a modern, accessible IDE, LegacyIDE helps preserve and teach important aspects of computing history while making them easier to explore.

---

# Target Audience

LegacyIDE is intended for:

- Students learning assembly or microcontroller programming
- Educators teaching embedded systems
- Developers interested in legacy architectures
- Hobbyists experimenting with low-level programming

---

# Summary

LegacyIDE is a modern platform designed to make legacy programming languages accessible again. By combining a code editor, assembly parser, and microcontroller emulator into a single environment, the IDE allows users to write and execute programs without relying on proprietary tools or hardware.

Starting with 8051 assembly support, the project aims to grow into a broader platform capable of supporting many legacy and specialized programming environments in the future.