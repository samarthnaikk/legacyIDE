```text
legacyide/

README.md
LICENSE
pyproject.toml / requirements.txt

legacyide/

│
├── core/
│   │
│   ├── editor/
│   │   ├── editor.py
│   │   ├── syntax_highlighter.py
│   │   ├── buffer.py
│   │   └── cursor.py
│   │
│   ├── runner/
│   │   ├── run_manager.py
│   │   ├── execution_controller.py
│   │   ├── step_executor.py
│   │   └── runtime_state.py
│   │
│   ├── errors/
│   │   ├── error_handler.py
│   │   ├── error_types.py
│   │   └── diagnostics.py
│   │
│   ├── languages/
│   │   ├── language_loader.py
│   │   ├── language_registry.py
│   │   └── language_interface.py
│   │
│   ├── project/
│   │   ├── project_manager.py
│   │   └── workspace.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── constants.py
│   │
│   └── utils/
│       ├── logger.py
│       ├── file_utils.py
│       └── helpers.py
│
│
├── languages/
│   │
│   ├── asm_8051/
│   │   │
│   │   ├── language.py
│   │   │
│   │   ├── parser/
│   │   │   ├── tokenizer.py
│   │   │   ├── parser.py
│   │   │   ├── label_resolver.py
│   │   │   └── ast_nodes.py
│   │   │
│   │   ├── emulator/
│   │   │   ├── emulator.py
│   │   │   ├── execution_engine.py
│   │   │   └── instruction_decoder.py
│   │   │
│   │   ├── cpu/
│   │   │   ├── cpu.py
│   │   │   ├── registers.py
│   │   │   ├── flags.py
│   │   │   └── program_counter.py
│   │   │
│   │   ├── memory/
│   │   │   ├── memory.py
│   │   │   ├── ram.py
│   │   │   ├── stack.py
│   │   │   └── ports.py
│   │   │
│   │   ├── instructions/
│   │   │   ├── instruction_set.py
│   │   │   ├── data_transfer.py
│   │   │   ├── arithmetic.py
│   │   │   ├── logical.py
│   │   │   ├── branching.py
│   │   │   └── bit_operations.py
│   │   │
│   │   ├── assembler/
│   │   │   ├── assembler.py
│   │   │   ├── opcode_table.py
│   │   │   └── addressing_modes.py
│   │   │
│   │   ├── debugger/
│   │   │   ├── debugger.py
│   │   │   ├── breakpoints.py
│   │   │   └── state_inspector.py
│   │   │
│   │   └── metadata/
│   │       ├── instruction_docs.py
│   │       └── syntax_rules.py
│   │
│   │
│   ├── asm_avr/            (future)
│   │
│   ├── chip8/              (future)
│   │
│   └── z80/                (future)
│
│
├── ui/
│   │
│   ├── app.py
│   │
│   ├── windows/
│   │   ├── main_window.py
│   │   └── settings_window.py
│   │
│   ├── panels/
│   │   ├── editor_panel.py
│   │   ├── register_panel.py
│   │   ├── memory_panel.py
│   │   └── port_panel.py
│   │
│   ├── components/
│   │   ├── toolbar.py
│   │   ├── status_bar.py
│   │   └── console.py
│   │
│   └── themes/
│       ├── dark_theme.py
│       └── light_theme.py
│
│
├── plugins/                 (future extensions)
│
├── examples/
│   ├── 8051/
│   │   ├── led_blink.asm
│   │   ├── delay.asm
│   │   └── counter.asm
│
├── docs/
│   ├── architecture.md
│   ├── language_support.md
│   └── development.md
│
└── tests/
    │
    ├── core/
    │
    └── languages/
        └── asm_8051/
```