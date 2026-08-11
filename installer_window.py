import logging
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from config import VERSION
from pages.installation_сomplete import InstallationComplite
from pages.lisence import LicensePage
from pages.setup_options import SetupOptions
from pages.welcome_page import WelcomePage
from resources.styles import stylesheet
from widget.page_indicator import PageIndicator

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

os.environ["QT_QPA_PLATFORMTHEME"] = "xdgdesktopportal"


class Installer(QWidget):
    page_class = {
        0: WelcomePage,
        1: LicensePage,
        2: SetupOptions,
        3: InstallationComplite,
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ruwa Installer")
        self.setStyleSheet(stylesheet.widget_style)
        self.setStyleSheet(stylesheet.label_style)
        
        self.setFixedSize(720, 540)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        background = QPixmap("resources/images/bg.webp").scaled(
            400, 440, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )

        self.background_label = QLabel(self)
        self.background_label.setGeometry(self.rect())

        self.background_label.setPixmap(background)
        self.background_label.setScaledContents(True)
        self.background_label.lower()
        
        version_label = QLabel(VERSION, self)
        version_label.setMargin(10)
        
        self.stack = QStackedWidget()
        self.pages = {}
        self.options = {}
        layout.addWidget(self.stack)
        
        self.indicator = PageIndicator(parent=self.stack, count=4)
        self.indicator.move(
            (self.width()-self.indicator.width()) // 2,
            480
        )
        
        self.load_page(0)
        self.indicator.raise_()

    def load_page(self, index):
        if index in self.pages:
            return self.pages[index]

        page_class = self.page_class.get(index, None)
        
        if page_class is None:
            return
            
        if page_class is InstallationComplite:
            page = page_class(self.options)
        else:
            page = page_class()
        
        self.pages[index] = page     
        self.stack.addWidget(page)
        
        if hasattr(page, "installRequested"):
            page.installRequested.connect(self.handle_install_options)
            
        if hasattr(page, "nextRequested"):
            page.nextRequested.connect(
                lambda: self.show_page(1)
            )
            
        if hasattr(page, "backRequested"):
            page.backRequested.connect(
                lambda: self.show_page(-1)
            )
          
        if hasattr(page, "closeRequested"):
            page.closeRequested.connect(self.close)

    def handle_install_options(self, options: dict):
        self.options = options
    
    def show_page(self, step_offset):
        step = self.stack.currentIndex() + step_offset
        self.load_page(step)
        self.stack.setCurrentWidget(self.pages[step])
        self.indicator.set_step(step)
        self.indicator.raise_()

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = QApplication()
    win = Installer()
    win.show()


    sys.exit(app.exec())
