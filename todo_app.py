import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
import sqlite3


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("برنامه مدیریت کارها با PyQt")
        self.resize(600, 450)

        self.conn = sqlite3.connect("tasks_pyqt.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_input_area()
        self.create_task_table()
        self.create_buttons()

        self.load_tasks()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                done INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def create_input_area(self):
        layout = QHBoxLayout()

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("عنوان تسک")

        self.input_date = QDateEdit()
        self.input_date.setDisplayFormat("yyyy-MM-dd")
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())

        self.btn_add = QPushButton("افزودن تسک")
        self.btn_add.clicked.connect(self.add_task)

        layout.addWidget(QLabel("عنوان:"))
        layout.addWidget(self.input_title)
        layout.addWidget(QLabel("تاریخ انجام:"))
        layout.addWidget(self.input_date)
        layout.addWidget(self.btn_add)

        self.layout.addLayout(layout)

    def create_task_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["عنوان", "تاریخ", "انجام شده"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.cellChanged.connect(self.toggle_task_done)
        self.layout.addWidget(self.table)

    def create_buttons(self):
        btn_layout = QHBoxLayout()
        self.btn_delete = QPushButton("حذف تسک انتخاب‌شده")
        self.btn_delete.clicked.connect(self.delete_task)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_delete)
        self.layout.addLayout(btn_layout)

    def add_task(self):
        title = self.input_title.text().strip()
        due_date = self.input_date.date().toString("yyyy-MM-dd")

        if not title:
            QMessageBox.warning(self, "خطا", "عنوان تسک نمی‌تواند خالی باشد.")
            return

        self.cursor.execute("INSERT INTO tasks (title, due_date) VALUES (?, ?)", (title, due_date))
        self.conn.commit()
        self.input_title.clear()
        self.input_date.setDate(QDate.currentDate())
        self.load_tasks()

    def load_tasks(self):
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        self.cursor.execute("SELECT id, title, due_date, done FROM tasks")
        tasks = self.cursor.fetchall()
        for task_id, title, due_date, done in tasks:
            self.add_table_row(task_id, title, due_date, done)
        self.table.blockSignals(False)

    def add_table_row(self, task_id, title, due_date, done):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_title = QTableWidgetItem(title)
        item_title.setData(Qt.ItemDataRole.UserRole, task_id)

        item_date = QTableWidgetItem(due_date)

        item_done = QTableWidgetItem()
        item_done.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        item_done.setCheckState(Qt.CheckState.Checked if done else Qt.CheckState.Unchecked)

        self.table.setItem(row, 0, item_title)
        self.table.setItem(row, 1, item_date)
        self.table.setItem(row, 2, item_done)

    def toggle_task_done(self, row, column):
        if column == 2:
            task_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            state = self.table.item(row, 2).checkState()
            done = 1 if state == Qt.CheckState.Checked else 0
            self.cursor.execute("UPDATE tasks SET done=? WHERE id=?", (done, task_id))
            self.conn.commit()

    def delete_task(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "هشدار", "هیچ تسکی انتخاب نشده است.")
            return

        task_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
