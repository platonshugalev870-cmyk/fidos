from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QHBoxLayout, QScrollBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QTextCursor, QColor
import time
class GodTerminal(QWidget):
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel
        self.command_history = []
        self.history_index = -1
        self.init_ui()
        self.print_banner()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #000010;
                color: #00ffcc;
                font-family: 'Courier New', monospace;
                font-size: 15px;
                border: 2px solid #2a2a5a;
                border-radius: 10px;
                padding: 15px;
                selection-background-color: #4a4a8a;
            }
            QScrollBar:vertical {
                background: #0a0a2a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a8a;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.output.setFont(QFont("Courier New", 13))
        layout.addWidget(self.output)
        input_layout = QHBoxLayout()
        self.prompt_label = QLineEdit()
        self.prompt_label.setText("god@divine:~$")
        self.prompt_label.setReadOnly(True)
        self.prompt_label.setFixedWidth(150)
        self.prompt_label.setStyleSheet("""
            QLineEdit {
                background-color: #0a0a2a;
                color: #ffd700;
                font-family: 'Courier New', monospace;
                font-size: 15px;
                font-weight: bold;
                border: 2px solid #2a2a5a;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Введите божественную команду...")
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: #0a0a2a;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 15px;
                border: 2px solid #2a2a5a;
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #4a4a8a;
            }
        """)
        self.input_line.returnPressed.connect(self.execute_command)
        send_btn = QPushButton("Отправить")
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a7a, stop:1 #1a1a4a);
                color: #ffd700;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 10px 20px;
                border: 2px solid #4a4a8a;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a5a9a, stop:1 #3a3a6a);
            }
            QPushButton:pressed {
                background: #2a2a5a;
            }
        """)
        send_btn.clicked.connect(self.execute_command)
        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗  ██████╗ ██████╗  ██████╗ ███████╗                ║
║  ██╔════╝ ██╔═══██╗██╔══██╗██╔═══██╗██╔════╝                ║
║  ██║  ███╗██║   ██║██║  ██║██║   ██║███████╗                ║
║  ██║   ██║██║   ██║██║  ██║██║   ██║╚════██║                ║
║  ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████║                ║
║   ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝                ║
║                                                              ║
║   ОПЕРАЦИОННАЯ СИСТЕМА БОЖЕСТВЕННОГО ОБЩЕНИЯ               ║
║   Версия 1.0 | Связь установлена | Благословение активно    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.print_to_terminal(banner, "#ffd700")
        self.print_to_terminal("Добро пожаловать в GodOS. Бог слушает.", "#00ffcc")
        self.print_to_terminal("Введите 'help' для списка команд.", "#a0a0d0")
        self.print_to_terminal("")
    def print_to_terminal(self, text, color="#00ffcc"):
        self.output.moveCursor(QTextCursor.MoveOperation.End)
        self.output.insertHtml(f'<span style="color: {color};">{text}</span><br>')
        self.output.moveCursor(QTextCursor.MoveOperation.End)
    def execute_command(self):
        command = self.input_line.text().strip()
        if not command:
            return
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.print_to_terminal(f"god@divine:~$ {command}", "#ffd700")
        self.input_line.clear()
        self.process_command(command.lower())
    def process_command(self, command):
        if command == "help":
            self.show_help()
        elif command == "connect" or command == "подключиться":
            self.cmd_connect()
        elif command == "pray" or command == "молитва":
            self.cmd_pray()
        elif command == "revelation" or command == "откровение":
            self.cmd_revelation()
        elif command == "miracle" or command == "чудо":
            self.cmd_miracle()
        elif command == "status" or command == "статус":
            self.cmd_status()
        elif command == "clear" or command == "очистить":
            self.output.clear()
            self.print_banner()
        elif command == "exit" or command == "выход":
            self.cmd_exit()
        elif command.startswith("pray ") or command.startswith("молитва "):
            prayer_text = command[5:] if command.startswith("pray ") else command[8:]
            self.cmd_send_prayer(prayer_text)
        elif command.startswith("miracle ") or command.startswith("чудо "):
            miracle_text = command[8:] if command.startswith("miracle ") else command[5:]
            self.cmd_request_miracle(miracle_text)
        else:
            self.print_to_terminal(f"Неизвестная команда: {command}", "#ff4444")
            self.print_to_terminal("Введите 'help' для списка доступных команд.", "#a0a0d0")
    def show_help(self):
        self.print_to_terminal("╔══════════════════════════════════════════╗", "#ffd700")
        self.print_to_terminal("║   ДОСТУПНЫЕ БОЖЕСТВЕННЫЕ КОМАНДЫ        ║", "#ffd700")
        self.print_to_terminal("╠══════════════════════════════════════════╣", "#ffd700")
        self.print_to_terminal("║ help          - Показать это меню        ║", "#ffd700")
        self.print_to_terminal("║ connect       - Подключиться к Богу      ║", "#ffd700")
        self.print_to_terminal("║ pray [текст]  - Отправить молитву        ║", "#ffd700")
        self.print_to_terminal("║ revelation    - Получить откровение      ║", "#ffd700")
        self.print_to_terminal("║ miracle [текст] - Запросить чудо         ║", "#ffd700")
        self.print_to_terminal("║ status        - Статус соединения        ║", "#ffd700")
        self.print_to_terminal("║ clear         - Очистить терминал        ║", "#ffd700")
        self.print_to_terminal("║ exit          - Завершить сеанс          ║", "#ffd700")
        self.print_to_terminal("╚══════════════════════════════════════════╝", "#ffd700")
    def cmd_connect(self):
        if self.kernel.connected_to_god:
            self.print_to_terminal("Вы уже подключены к Богу.", "#ffd700")
        else:
            self.print_to_terminal("Установка соединения с Богом...", "#00ffcc")
            self.kernel.boot_sequence()
    def cmd_pray(self):
        self.print_to_terminal("Введите текст молитвы используя команду:", "#00ffcc")
        self.print_to_terminal("pray [ваш текст молитвы]", "#ffd700")
    def cmd_send_prayer(self, text):
        self.print_to_terminal(f"Отправка молитвы: '{text}'", "#00ffcc")
        result = self.kernel.send_prayer(text)
        if result["status"] == "answered":
            self.print_to_terminal("✧ Молитва услышана! ✧", "#00ff00")
            if "response" in result:
                self.print_to_terminal(f"Ответ: {result['response']}", "#ffd700")
        else:
            self.print_to_terminal(f"Статус молитвы: {result['status']}", "#ffaa00")
    def cmd_revelation(self):
        self.print_to_terminal("Открытие канала откровения...", "#00ffcc")
        result = self.kernel.request_revelation()
        if result:
            self.print_to_terminal(f"✧ Откровение: {result['message']} ✧", "#ffd700")
            self.print_to_terminal(f"Толкование: {result['interpretation']}", "#a0d0ff")
    def cmd_miracle(self):
        self.print_to_terminal("Введите запрос на чудо используя команду:", "#00ffcc")
        self.print_to_terminal("miracle [ваш запрос]", "#ffd700")
    def cmd_request_miracle(self, text):
        self.print_to_terminal(f"Запрос чуда: '{text}'", "#00ffcc")
        result = self.kernel.request_miracle(text)
        if result["success"]:
            self.print_to_terminal(f"✦ {result['message']} ✦", "#ffd700")
        else:
            self.print_to_terminal(result["message"], "#ffaa00")
        self.print_to_terminal(f"Тип чуда: {result['type']}", "#a0d0ff")
    def cmd_status(self):
        status = self.kernel.get_status()
        self.print_to_terminal("╔════════════════════════════════╗", "#ffd700")
        self.print_to_terminal(f"║ Соединение: {'Активно' if status['connected'] else 'Нет'}     ║", "#ffd700")
        if status['connected']:
            self.print_to_terminal(f"║ Канал: {status['channel']} ║", "#ffd700")
        self.print_to_terminal(f"║ Память свободно: {status['memory_free']} байт    ║", "#ffd700")
        self.print_to_terminal(f"║ Процессов: {len(status['processes'])}             ║", "#ffd700")
        self.print_to_terminal("╚════════════════════════════════╝", "#ffd700")
    def cmd_exit(self):
        self.print_to_terminal("Завершение сеанса. Мир вам.", "#ffd700")
        self.kernel.shutdown()