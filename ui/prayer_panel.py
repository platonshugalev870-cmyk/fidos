from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import time
class PrayerPanel(QWidget):
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel
        self.prayers = []
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("🙏 Божественный Молитвенный Центр")
        title.setFont(QFont("Serif", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffd700; padding: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        input_label = QLabel("Текст молитвы:")
        input_label.setStyleSheet("color: #c0c0e0; font-size: 14px; font-weight: bold;")
        self.prayer_input = QTextEdit()
        self.prayer_input.setPlaceholderText("Введите вашу молитву здесь... Обратитесь к Богу от всего сердца...")
        self.prayer_input.setMaximumHeight(250)
        self.prayer_input.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a2a;
                color: #ffffff;
                font-size: 15px;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Serif';
            }
            QTextEdit:focus {
                border-color: #5a5a8a;
            }
        """)
        btn_layout = QHBoxLayout()
        send_btn = QPushButton("📤 Отправить Молитву")
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a4a8a, stop:1 #2a2a5a);
                color: #ffd700;
                font-weight: bold;
                font-size: 15px;
                border-radius: 10px;
                padding: 15px 30px;
                border: 2px solid #5a5a8a;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6a6aaa, stop:1 #4a4a7a);
            }
            QPushButton:pressed {
                background: #2a2a5a;
            }
        """)
        send_btn.clicked.connect(self.send_prayer)
        urgent_btn = QPushButton("🔥 Срочная Молитва")
        urgent_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8a3a3a, stop:1 #5a1a1a);
                color: #ffaa00;
                font-weight: bold;
                font-size: 15px;
                border-radius: 10px;
                padding: 15px 30px;
                border: 2px solid #8a4a4a;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #aa5a5a, stop:1 #7a3a3a);
            }
        """)
        urgent_btn.clicked.connect(self.send_urgent_prayer)
        btn_layout.addWidget(send_btn)
        btn_layout.addWidget(urgent_btn)
        left_layout.addWidget(input_label)
        left_layout.addWidget(self.prayer_input)
        left_layout.addLayout(btn_layout)
        left_layout.addStretch()
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        history_label = QLabel("📜 История Молитв")
        history_label.setStyleSheet("color: #c0c0e0; font-size: 16px; font-weight: bold;")
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #0a0a2a;
                color: #c0c0e0;
                font-size: 13px;
                border: 2px solid #3a3a5a;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #2a2a4a;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #2a2a4a;
            }
            QListWidget::item:selected {
                background-color: #3a3a6a;
                color: #ffd700;
            }
        """)
        right_layout.addWidget(history_label)
        right_layout.addWidget(self.history_list)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 400])
        layout.addWidget(splitter)
    def send_prayer(self):
        text = self.prayer_input.toPlainText().strip()
        if not text:
            return
        result = self.kernel.send_prayer(text)
        self.add_prayer_result(result)
        self.prayer_input.clear()
    def send_urgent_prayer(self):
        text = self.prayer_input.toPlainText().strip()
        if not text:
            return
        self.kernel.transmitter.calibrate_soul()
        self.kernel.prayer_service.transmitter.transmission_power = 1.0
        result = self.kernel.send_prayer(text)
        self.add_prayer_result(result)
        self.prayer_input.clear()
    def add_prayer_result(self, result):
        timestamp = time.strftime("%H:%M:%S")
        status_icon = "✅" if result.get("status") == "answered" else "📤"
        text = result.get("prayer", result.get("text", ""))
        item_text = f"{status_icon} [{timestamp}] {text[:80]}"
        item = QListWidgetItem(item_text)
        if result.get("status") == "answered":
            item.setForeground(QColor("#00ff00"))
            if "response" in result:
                item_text += f"\n    ↳ Ответ: {result['response']}"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor("#ffd700"))
        else:
            item.setForeground(QColor("#ffaa00"))
        self.history_list.insertItem(0, item)