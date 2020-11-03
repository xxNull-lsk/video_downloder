# -*- coding: UTF-8 -*-
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from downloader import Downloader


class RunThread(QThread):
    download_progress = pyqtSignal(str, str, int, int)
    download_finished = pyqtSignal(str, int)

    def __init__(self, items, win):
        super().__init__()
        self.items = items
        self.win = win
        self.curr = 0

    def run(self):
        downloader = Downloader()
        filename, file_size = downloader.download(self.items[0],  # name
                                                  self.items[1],  # data url
                                                  self.items[2],  # key url
                                                  self.items[3],  # referer url
                                                  progress=self.download_progress.emit)
        self.download_finished.emit(filename, file_size)


class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__(parent=QDesktopWidget())
        self.setWindowIcon(QIcon('./icons/app.ico'))
        self.center()
        self.thread = None

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

        self.download_progress = QProgressBar()
        self.download_progress.setRange(0, 1000)
        self.download_progress.setFixedHeight(1)
        self.download_progress.setVisible(False)
        self.root_layout.addWidget(self.download_progress)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    @staticmethod
    def format_size(size):
        if size < 1024:
            return "{} Bytes".format(size)
        size /= 1024
        if size < 1024:
            return "{:.2f} KB".format(size)
        size /= 1024
        if size < 1024:
            return "{:.2f} MB".format(size)
        size /= 1024
        if size < 1024:
            return "{:.2f} GB".format(size)
        size /= 1024
        return "{:.2f} TB".format(size)

    def on_progress(self, filename, url, finished, total):
        curr = int(finished * 1000 / total)
        if curr != self.download_progress.value():
            self.download_progress.setValue(curr)

    def on_finished(self, filename, total):
        self.btn.setEnabled(True)
        self.download_progress.setVisible(False)
        QMessageBox.information(None,
                                "提示", "下载完成！\n\n文件路径：{}\n文件大小: {}".format(filename, self.format_size(total)),
                                QMessageBox.Ok)

    def on_download(self):
        url = self.editUrl.toPlainText()
        items = url.split('|')
        if len(items) != 4:
            QMessageBox.warning(None, "错误", "下载地址无效！", QMessageBox.Ok)
            return
        self.btn.setEnabled(False)
        self.download_progress.setVisible(True)
        self.thread = RunThread(items, self)
        self.thread.download_progress.connect(self.on_progress)
        self.thread.download_finished.connect(self.on_finished)
        self.thread.start()

    def on_help(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/xxNull-lsk/video_downloder'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow()
    ex.show()
    sys.exit(app.exec())
