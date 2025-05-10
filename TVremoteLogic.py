from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys

class Television:
    """
    This simulates a basic tv with power, volume, mute, and channel controls
    """
    MIN_VOLUME: int = 0
    MAX_VOLUME: int = 5
    MIN_CHANNEL: int = 0
    MAX_CHANNEL: int = 4

    def __init__(self):
        """Initializes the tv with default settings."""
        self.__status: str = "Off"
        self.__muted: str = "Off"
        self.__volume: int = Television.MIN_VOLUME
        self.__channel: int = Television.MIN_CHANNEL

    def power(self):
        """Toggles the power for the TV."""
        self.__status = "Off" if self.__status == "On" else "On"

    def mute(self):
        if self.__status == "On":
            self.__muted = "Off" if self.__muted == "On" else "On"

    def channel_up(self):
        """Increase the channel number, looping back to the minimum if necessary."""

        if self.__status == "On":
            self.__channel = (
                Television.MIN_CHANNEL
                if self.__channel == Television.MAX_CHANNEL
                else self.__channel + 1
            )

    def channel_down(self):
        """Decrease the channel number, looping back to the maximum if necessary."""
        if self.__status == "On":
            self.__channel = (
                Television.MAX_CHANNEL
                if self.__channel == Television.MIN_CHANNEL
                else self.__channel - 1
            )

    def volume_up(self):
        """Increase the volume if the TV is on and unmute if muted."""
        if self.__status == "On":
            if self.__muted == "On":
                self.__muted = "Off"
            if self.__volume < Television.MAX_VOLUME:
                self.__volume += 1

    def volume_down(self):
        """Decrease the volume if the TV is on and unmute if muted."""
        if self.__status == "On":
            if self.__muted == "On":
                self.__muted = "Off"
            if self.__volume > Television.MIN_VOLUME:
                self.__volume -= 1

class TVRemote(QWidget):
    def __init__(self):
        """
        Initialize the TV remote GUI by setting up the Television object,
        loads channel images, and creates the UI layout.
        """
        super().__init__()
        self.tv = Television()
        self.setWindowTitle("TV Remote")
        self.channel_images = []
        self.load_channel_images()
        self.setup_ui()

    def load_channel_images(self):
        """
        Loads images representing TV channels from local files and stores them in a list.
        Also warns if any image file is missing or invalid.
        """
        for i in range(5):
            pixmap = QPixmap(f"channel{i}.png")
            if pixmap.isNull():
                print(f"Warning: channel{i}.png not found or invalid.")
            self.channel_images.append(pixmap)

    def setup_ui(self):
        """
        Set up the user interface of the remote control, including buttons for
        power, mute, volume, and channel control, as well as a screen and status display.
        """

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
        """
    Updates the display screen and status label based on the current state of the TV.
    Displays the appropriate channel image or a message if unavailable.
    Shows power, volume, and mute status below the screen.
    """
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
        """
        Toggles the power for the TV and updates the interface accordingly.
        """
        self.tv.power()
        self.update_status()

    def mute_tv(self):
        """
        Toggles the mute for the TV and updates the interface accordingly.
        """
        self.tv.mute()
        self.update_status()

    def volume_up(self):
        """
        Increasess the TV volume and updates the display.
        Unmutes the TV if it was muted.
        """
        self.tv.volume_up()
        self.update_status()

    def volume_down(self):
        """
        Decreases the TV volume and updates the display.
        Unmutes the TV if it was muted.
        """
        self.tv.volume_down()
        self.update_status()

    def channel_up(self):
        """
        Changes the TV channel to the next one and updates the display.
        Loops back to the first channel after the last one.
        """
        self.tv.channel_up()
        self.update_status()

    def channel_down(self):
        """
        Changes the TV channel to the previous one and updates the display.
        Loops to the last channel if currently on the first.
        """
        self.tv.channel_down()
        self.update_status()

    def handle_up(self):
        """
        Handle a press of the up button.
        Then prints a message to the console.
        """
        print("Up button pressed")

    def handle_down(self):
        """
        Handle a press of the down button.
        Then prints a message to the console.
        """
        print("Down button pressed")

    def handle_left(self):
        """
        Handle a press of the left button.
        Then prints a message to the console.
        """
        print("Left button pressed")

    def handle_right(self):
        """
        Handle a press of the right button.
        Then prints a message to the console.
        """
        print("Right button pressed")

    def handle_ok(self):
        """
        Handle a press of the OK button.
        Then prints a message to the console.
        """
        print("OK button pressed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TVRemote()
    window.show()
    sys.exit(app.exec())