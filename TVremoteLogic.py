from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys

class Television:
    MIN_VOLUME = 0
    MAX_VOLUME = 5
    MIN_CHANNEL = 0
    MAX_CHANNEL = 4

    def __init__(self):
        self.__status = "Off"
        self.__muted = "Off"
        self.__volume = Television.MIN_VOLUME
        self.__channel = Television.MIN_CHANNEL

    def power(self):
        self.__status = "Off" if self.__status == "On" else "On"

    def mute(self):
        if self.__status == "On":
            self.__muted = "Off" if self.__muted == "On" else "On"

    def channel_up(self):
        if self.__status == "On":
            self.__channel = (
                Television.MIN_CHANNEL
                if self.__channel == Television.MAX_CHANNEL
                else self.__channel + 1
            )

    def channel_down(self):
        if self.__status == "On":
            self.__channel = (
                Television.MAX_CHANNEL
                if self.__channel == Television.MIN_CHANNEL
                else self.__channel - 1
            )

    def volume_up(self):
        if self.__status == "On":
            if self.__muted == "On":
                self.__muted = "Off"
            if self.__volume < Television.MAX_VOLUME:
                self.__volume += 1

    def volume_down(self):
        if self.__status == "On":
            if self.__muted == "On":
                self.__muted = "Off"
            if self.__volume > Television.MIN_VOLUME:
                self.__volume -= 1

class TVRemote(QWidget):
    def __init__(self):
        super().__init__()
        self.tv = Television()
        self.setWindowTitle("TV Remote")
        self.channel_images = []
        self.load_channel_images()
        self.setup_ui()

    def load_channel_images(self):
        for i in range(5):
            pixmap = QPixmap(f"channel{i}.png")
            if pixmap.isNull():
                print(f"Warning: channel{i}.png not found or invalid.")
            self.channel_images.append(pixmap)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.screen_label = QLabel()
        self.screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_label.setStyleSheet("border: 2px solid black; padding: 10px;")
        self.screen_label.setFixedSize(300, 200)  
        layout.addWidget(self.screen_label)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        row1 = QHBoxLayout()
        self.power_button = QPushButton("⏻")
        self.power_button.setStyleSheet("font-size: 20px;")
        self.power_button.clicked.connect(self.power_tv)
        row1.addWidget(self.power_button)

        self.mute_button = QPushButton("🔇")
        self.mute_button.setStyleSheet("font-size: 20px;")
        self.mute_button.clicked.connect(self.mute_tv)
        row1.addWidget(self.mute_button)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.volume_up_button = QPushButton("Volume +")
        self.volume_up_button.clicked.connect(self.volume_up)
        row2.addWidget(self.volume_up_button)

        self.volume_down_button = QPushButton("Volume -")
        self.volume_down_button.clicked.connect(self.volume_down)
        row2.addWidget(self.volume_down_button)
        layout.addLayout(row2)

        row3 = QHBoxLayout()
        self.channel_up_button = QPushButton("Channel +")
        self.channel_up_button.clicked.connect(self.channel_up)
        row3.addWidget(self.channel_up_button)

        self.channel_down_button = QPushButton("Channel -")
        self.channel_down_button.clicked.connect(self.channel_down)
        row3.addWidget(self.channel_down_button)
        layout.addLayout(row3)

        dpad_layout = QVBoxLayout()

        up_row = QHBoxLayout()
        up_row.addStretch()
        self.up_button = QPushButton("↑")
        self.up_button.clicked.connect(self.handle_up)
        up_row.addWidget(self.up_button)
        up_row.addStretch()
        dpad_layout.addLayout(up_row)

        middle_row = QHBoxLayout()
        self.left_button = QPushButton("←")
        self.left_button.clicked.connect(self.handle_left)
        middle_row.addWidget(self.left_button)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.handle_ok)
        middle_row.addWidget(self.ok_button)

        self.right_button = QPushButton("→")
        self.right_button.clicked.connect(self.handle_right)
        middle_row.addWidget(self.right_button)
        dpad_layout.addLayout(middle_row)

        down_row = QHBoxLayout()
        down_row.addStretch()
        self.down_button = QPushButton("↓")
        self.down_button.clicked.connect(self.handle_down)
        down_row.addWidget(self.down_button)
        down_row.addStretch()
        dpad_layout.addLayout(down_row)

        layout.addLayout(dpad_layout)

        self.setLayout(layout)

    def update_status(self):
        fixed_size = self.screen_label.size()

        if self.tv._Television__status == "On":
            channel = self.tv._Television__channel
            if 0 <= channel < len(self.channel_images):
                pixmap = self.channel_images[channel]
                self.screen_label.setPixmap(pixmap.scaled(
                    fixed_size, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.screen_label.setText("Channel image not available")
        else:
            self.screen_label.clear()  

        status = f"Power: {self.tv._Television__status} | "
        status += f"Volume: {self.tv._Television__volume} | "
        status += f"Mute: {self.tv._Television__muted}"
        self.status_label.setText(status)

    def power_tv(self):
        self.tv.power()
        self.update_status()

    def mute_tv(self):
        self.tv.mute()
        self.update_status()

    def volume_up(self):
        self.tv.volume_up()
        self.update_status()

    def volume_down(self):
        self.tv.volume_down()
        self.update_status()

    def channel_up(self):
        self.tv.channel_up()
        self.update_status()

    def channel_down(self):
        self.tv.channel_down()
        self.update_status()

    def handle_up(self):
        print("Up button pressed")

    def handle_down(self):
        print("Down button pressed")

    def handle_left(self):
        print("Left button pressed")

    def handle_right(self):
        print("Right button pressed")

    def handle_ok(self):
        print("OK button pressed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TVRemote()
    window.show()
    sys.exit(app.exec())