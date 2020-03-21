import sys
import time
import requests
import configparser
from win32clipboard import *
from PyQt5.QtGui import QPen, QPainter, QPixmap, QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.dialog import Ui_Dialog
from ui.mainwindow import Ui_MainWindow


class Bbox(object):
    def __init__(self):
        self._empty = True
        self.init_bbox()

    @property
    def point1(self):
        return self._x1, self._y1

    @point1.setter
    def point1(self, position: tuple):
        self._x1 = position[0]
        self._y1 = position[1]

    @property
    def point2(self):
        return self._x2, self._y2

    @point2.setter
    def point2(self, position: tuple):
        self._empty = False
        self._x2 = position[0]
        self._y2 = position[1]

    @property
    def bbox(self):
        if self._x1 < self._x2:
            x_min, x_max = self._x1, self._x2
        else:
            x_min, x_max = self._x2, self._x1

        if self._y1 < self._y2:
            y_min, y_max = self._y1, self._y2
        else:
            y_min, y_max = self._y2, self._y1
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def is_empty(self):
        return self._empty

    def init_bbox(self):
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._empty = True

    def __str__(self):
        return str(self.bbox)


class ScreenLabel(QLabel):
    signal = pyqtSignal(QPixmap)

    def __init__(self, pixmap):
        super().__init__()
        self._press_flag = False
        self._bbox = Bbox()
        self._pen = QPen(Qt.white, 2, Qt.DashLine)
        self._painter = QPainter()
        self._bbox = Bbox()
        self._pixmap = pixmap

    def _draw_bbox(self):
        pixmap = self._pixmap.copy()
        self._painter.begin(pixmap)
        self._painter.setPen(self._pen)  # 设置pen必须在begin后
        rect = QRect(*self._bbox.bbox)
        self._painter.drawRect(rect)
        self._painter.end()
        self.setPixmap(pixmap)
        self.update()
        self.showFullScreen()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("鼠标左键：", [QMouseEvent.x(), QMouseEvent.y()])
            self._press_flag = True
            self._bbox.point1 = [QMouseEvent.x(), QMouseEvent.y()]

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton and self._press_flag:
            print("鼠标释放：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._press_flag = False
            self.signal.emit(self._pixmap.copy(*self._bbox.bbox))

    def mouseMoveEvent(self, QMouseEvent):
        if self._press_flag:
            print("鼠标移动：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._draw_bbox()


class ShotDialog(QDialog, Ui_Dialog):
    def __init__(self, pixmap):
        super().__init__()
        self.setupUi(self)
        self.adjustSize()

        self.pushButton_clipboard.clicked.connect(self.clipboard)
        self.pushButton_markdown.clicked.connect(self.markdown)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_cancel.clicked.connect(self.close)

        self._pixmap = pixmap
        self.label_shot.setPixmap(self._pixmap)

    def get_shot_img(self):
        return self.label_shot.pixmap().toImage()

    def get_shot_bytes(self):
        shot_bytes = QByteArray()
        buffer = QBuffer(shot_bytes)
        buffer.open(QIODevice.WriteOnly)
        shot_img = self.get_shot_img()
        shot_img.save(buffer, 'png')
        return shot_bytes.data()

    def save(self):
        file, _ = QFileDialog.getSaveFileName(self, '保存到' './', 'screenshot.jpg',
                                              'Image files(*.jpg *.gif *.png)')
        if file:
            shot_img = self.get_shot_img()
            shot_img.save(file)
        self.close()

    def clipboard(self):
        shot_bytes = self.get_shot_bytes()
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_BITMAP, shot_bytes[14:])
        CloseClipboard()
        self.close()

    def markdown(self):
        shot_bytes = self.get_shot_bytes()
        filename = "shot" + str(time.time()).split('.')[0] + '.jpg'
        files = {
            "image_field": (filename, shot_bytes, "image/jpeg")
        }
        headers = {
            "Cookie": cfg.get("picbed", 'cookie')
        }
        try:
            res = requests.post(cfg.get("picbed", 'api'), files=files, headers=headers)
        except Exception as e:
            self.showMessage("requests error, message:".format(e))

        if res.status_code == 200:
            self.showMessage(res.json()['data']['img_url'])
        else:
            self.showMessage("http error, code: {}".format(res.status_code))
        self.close()

    def showMessage(self, message):
        dialog = QDialog()
        dialog.adjustSize()
        text = QLineEdit(message, dialog)
        text.adjustSize()
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("截图工具")
        self.setWindowIcon(QIcon('./icon/cut.png'))
        self.screen = QApplication.primaryScreen()
        # 设置最小化托盘
        self.screen = QApplication.primaryScreen()
        self.tray = QSystemTrayIcon(QIcon('./icon/screenshot.png'), self)  # 创建系统托盘对象
        self.tray.activated.connect(self.shot)  # 设置托盘点击事件处理函数
        self.tray.show()
        # 快捷键
        QShortcut(QKeySequence("F1"), self, self.shot)
        # 信号与槽
        self.pushButton_shot.clicked.connect(self.shot)
        self.pushButton_exit.clicked.connect(self.close)
        self.lineEdit_api.textChanged.connect(self.change_api)
        self.lineEdit_cookie.textChanged.connect(self.change_cookie)

        # 读取配置
        self.lineEdit_api.setText(cfg.get('picbed', 'api'))
        self.lineEdit_cookie.setText(cfg.get('picbed', 'cookie'))

    def shot(self):
        """开始截图"""
        pixmap = self.screen.grabWindow(0)
        self.label = ScreenLabel(pixmap)
        self.label.setPixmap(pixmap)
        self.label.showFullScreen()
        self.label.signal.connect(self.callback)

    def callback(self, pixmap):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        self.dialog = ShotDialog(pixmap)
        self.dialog.exec_()

    def change_api(self):
        cfg.set('picbed', "api", self.lineEdit_api.text())

    def change_cookie(self):
        cfg.set('picbed', "cookie", self.lineEdit_cookie.text())

    def close(self):
        print("修改配置文件")
        cfg.write(open("config.ini", "r+", encoding="utf-8"))
        super().close()


if __name__ == "__main__":
    from configparser import ConfigParser

    cfg = ConfigParser()
    cfg.read('config.ini')
    cfg.get('picbed', 'cookie')
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
