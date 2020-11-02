# -*- coding: UTF-8 -*-
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from downloader import Downloader


class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__(parent=QDesktopWidget())

        self.downloader = Downloader()

        self.resize(360, 360)
        self.setWindowTitle("xet下载器")

        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(10, 10, 10, 10)

        self.root_layout.addWidget(QLabel('下载地址：'))

        self.editUrl = QTextEdit('')
        self.root_layout.addWidget(self.editUrl)

        self.btn = QPushButton('下载')
        self.btn.clicked.connect(self.on_download)
        self.root_layout.addWidget(self.btn)

        self.btn_help = QCommandLinkButton('使用帮助')
        self.btn_help.clicked.connect(self.on_help)
        self.root_layout.addWidget(self.btn_help)

    def on_download(self):
        url = self.editUrl.toPlainText()
        items = url.split('|')
        if len(items) != 4:
            QMessageBox.warning(None, "错误", "下载地址无效！", QMessageBox.Ok)
            return
        filename = self.downloader.download(items[0], items[1], items[2], items[3])
        QMessageBox.information(None, "提示", "下载完成！文件名：{}".format(filename), QMessageBox.Ok)

    def on_help(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/xxNull-lsk/video_downloder'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec())
