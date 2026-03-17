from collections.abc import Callable

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar


def build_main_toolbar(
	parent: QMainWindow,
	*,
	on_new: Callable[[], None],
	on_open: Callable[[], None],
	on_save: Callable[[], None],
	on_run: Callable[[], None],
) -> QToolBar:
	toolbar = QToolBar("Main")
	toolbar.setMovable(False)

	new_action = QAction("New", parent)
	new_action.triggered.connect(on_new)
	toolbar.addAction(new_action)

	open_action = QAction("Open", parent)
	open_action.triggered.connect(on_open)
	toolbar.addAction(open_action)

	save_action = QAction("Save", parent)
	save_action.triggered.connect(on_save)
	toolbar.addAction(save_action)

	toolbar.addSeparator()

	run_action = QAction("Run", parent)
	run_action.triggered.connect(on_run)
	toolbar.addAction(run_action)

	return toolbar
