from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog,
    QGraphicsDropShadowEffect, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer

import sys


class FlyAlert(QDialog):
    ICONS = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'question': '❓'
    }

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.position = config.get("position", "center")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        self.opacity_anim = None
        self.init_ui()
        self.start_animation()

    def init_ui(self):
        self.container = QWidget(self)
        self.container.setGeometry(10, 10, 380, 280)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        self.container.setStyleSheet("background-color: white; border-radius: 15px;")

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        icon_label = QLabel(self.ICONS.get(self.config.get("icon", "info"), 'ℹ️'))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 50))
        layout.addWidget(icon_label)

        title_label = QLabel(self.config.get("title", "Default Title"))
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        message_label = QLabel(self.config.get("message", "Default Message"))
        message_label.setFont(QFont("Arial", 12))
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        if self.config.get("ConfirmButton", True):
            btn = QPushButton(self.config.get("ConfirmButtonText", "Confirm Button"))
            btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.config.get("ConfirmButtonColor", "#4CAF50")};
                            color: white;
                            padding: 8px 16px;
                            border: none;
                            border-radius: 8px;
                        }}
                        QPushButton:hover {{
                            background-color: #45A049;
                        }}
                    """)
            btn.clicked.connect(self.config.get("ConfirmButtonClicked", self.accept))
            button_layout.addWidget(btn)
        else:
            btn = QPushButton("Confirm Button")
            btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: #4CAF50;
                            color: white;
                            padding: 8px 16px;
                            border: none;
                            border-radius: 8px;
                        }}
                        QPushButton:hover {{
                            background-color: #45A049;
                        }}
                    """)
            btn.clicked.connect(self.accept)
            button_layout.addWidget(btn)

        if self.config.get("CancelButton", False):
            btn = QPushButton(self.config.get("CancelButtonText", "Cancel Button"))
            btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.config.get("CancelButtonColor", "#F44336")};
                            color: white;
                            padding: 8px 16px;
                            border: none;
                            border-radius: 8px;
                        }}
                        QPushButton:hover {{
                            background-color: #E53935;
                        }}
                    """)
            btn.clicked.connect(self.config.get("CancelButtonClicked", self.reject))
            button_layout.addWidget(btn)

        if self.config.get("InfoButton", False):
            btn = QPushButton(self.config.get("InfoButtonText", "Info Button"))
            btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.config.get("InfoButtonColor", "#2196F3")};
                            color: white;
                            padding: 8px 16px;
                            border: none;
                            border-radius: 8px;
                        }}
                        QPushButton:hover {{
                            background-color: #1E88E5;
                        }}
                    """)
            btn.clicked.connect(self.config.get("InfoButtonClicked", self.accept))
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

    def start_animation(self):
        self.setWindowOpacity(0.0)
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.opacity_anim.start()

    def close_animation(self):
        self.close_anim = QPropertyAnimation(self, b"windowOpacity")
        self.close_anim.setDuration(300)
        self.close_anim.setStartValue(1.0)
        self.close_anim.setEndValue(0.0)
        self.close_anim.setEasingCurve(QEasingCurve.InQuad)
        self.close_anim.start()
        QTimer.singleShot(300, self.close)

    def show(self):
        if self.parent():
            parent_geo = self.parent().geometry()
            parent_x, parent_y = parent_geo.x(), parent_geo.y()

            positions = {
                "top-right": (parent_x + parent_geo.width() - self.width() - 10, parent_y + 10),
                "top-left": (parent_x + 10, parent_y + 10),
                "bottom-right": (parent_x + parent_geo.width() - self.width() - 10,
                                 parent_y + parent_geo.height() - self.height() - 10),
                "bottom-left": (parent_x + 10, parent_y + parent_geo.height() - self.height() - 10),
                "center": (parent_x + parent_geo.width() // 2 - self.width() // 2,
                           parent_y + parent_geo.height() // 2 - self.height() // 2)
            }
        else:
            screen = QApplication.primaryScreen()
            available_geometry = screen.availableGeometry()

            positions = {
                "top-right": (available_geometry.width() - self.width() - 20, 20),
                "top-left": (20, 20),
                "bottom-right": (available_geometry.width() - self.width() - 20,
                                 available_geometry.height() - self.height() - 20),
                "bottom-left": (20, available_geometry.height() - self.height() - 20),
                "center": (available_geometry.center().x() - self.width() // 2,
                           available_geometry.center().y() - self.height() // 2)
            }

        pos_x, pos_y = positions.get(self.position, positions["center"])
        self.move(pos_x, pos_y)

        super().exec_()

    def accept_def(self):
        self.accept()

    def reject_def(self):
        self.reject()


class MinimalFlyAlert(FlyAlert):
    def __init__(self, config):
        super().__init__(config)
        self.position = config.get("position", "center")
        self.auto_close_time = config.get("auto_close_time", 5000)
        self.setFixedSize(400, 80)
        self.init_ui()
        self.start_auto_close_timer()

    def init_ui(self):
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 400, 80)
        self.container.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QGridLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)

        icon_label = QLabel(self.ICONS.get(self.config.get("icon", "info"), 'ℹ️'))
        icon_label.setFont(QFont("Arial", 32))

        message_label = QLabel(self.config.get("message", "پیام پیش‌فرض"))
        message_label.setFont(QFont("Arial", 14))

        close_button = QPushButton("✖")
        close_button.setFont(QFont("Arial", 24))
        close_button.setStyleSheet("""
            QPushButton {
                background: transparent; font-size: 24px; border: none;
                color: black;
            }
            QPushButton:hover {
                color: red;
                font-size: 26px;
            }
        """)
        close_button.clicked.connect(self.close_animation)

        layout.addWidget(icon_label, 0, 0)
        layout.addWidget(message_label, 0, 1)
        layout.addWidget(close_button, 0, 2)

    def start_auto_close_timer(self):
        if self.auto_close_time:
            QTimer.singleShot(self.auto_close_time, self.close_animation)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    alert = FlyAlert({
        'icon': 'success',
        'ConfirmButton': True,
    })

    alert.show()
    sys.exit(app.exec_())
