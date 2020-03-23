import sys
import time
import requests
from configparser import ConfigParser
from win32clipboard import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.dialog import Ui_Dialog
from ui.mainwindow import Ui_MainWindow


class Bbox(object):
    def __init__(self):
        self._x1, self._y1 = 0, 0
        self._x2, self._y2 = 0, 0

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

    def __str__(self):
        return str(self.bbox)


class ScreenLabel(QLabel):
    signal = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        self._press_flag = False
        self._bbox = Bbox()
        self._pen = QPen(Qt.white, 2, Qt.DashLine)
        self._painter = QPainter()
        self._bbox = Bbox()
        self._pixmap = QPixmap(width, height)
        self._pixmap.fill(QColor(255, 255, 255))
        self.setPixmap(self._pixmap)
        self.setWindowOpacity(0.4)

        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置背景颜色为透明

        QShortcut(QKeySequence("esc"), self, self.close)

        self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出

        # palette = QPalette()
        # palette.
        # self.setPalette()

    def _draw_bbox(self):
        pixmap = self._pixmap.copy()
        self._painter.begin(pixmap)
        self._painter.setPen(self._pen)  # 设置pen必须在begin后
        rect = QRect(*self._bbox.bbox)
        self._painter.fillRect(rect, Qt.SolidPattern)  # 区域不透明
        self._painter.drawRect(rect)  # 绘制虚线框
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
            self.signal.emit(QRect(*self._bbox.bbox))

    def mouseMoveEvent(self, QMouseEvent):
        if self._press_flag:
            print("鼠标移动：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._draw_bbox()


class ShotDialog(QDialog, Ui_Dialog):
    def __init__(self, rect):
        super().__init__()
        self.setupUi(self)
        self.adjustSize()
        self.setWindowFlag(Qt.FramelessWindowHint)  # 没有窗口栏
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明

        self.pushButton_clipboard.clicked.connect(self.save_to_clipboard)
        self.pushButton_markdown.clicked.connect(self.upload_to_picbed)
        self.pushButton_save.clicked.connect(self.save_local)
        self.pushButton_cancel.clicked.connect(self.close)

        self.label_shot.setPixmap(QApplication.primaryScreen().grabWindow(0).copy(rect))
        self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出

    def get_shot_img(self):
        return self.label_shot.pixmap().toImage()

    def get_shot_bytes(self):
        shot_bytes = QByteArray()
        buffer = QBuffer(shot_bytes)
        buffer.open(QIODevice.WriteOnly)
        shot_img = self.get_shot_img()
        shot_img.save(buffer, 'png')
        return shot_bytes.data()

    def save_local(self):
        file, _ = QFileDialog.getSaveFileName(self, '保存到' './', 'screenshot.jpg',
                                              'Image files(*.jpg *.gif *.png)')
        if file:
            shot_img = self.get_shot_img()
            shot_img.save(file)
        self.close()

    def save_to_clipboard(self):
        shot_bytes = self.get_shot_bytes()
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_BITMAP, shot_bytes[14:])
        CloseClipboard()
        self.close()

    def upload_to_picbed(self):
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
        dialog.exec_()


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.adjustSize()
        self.setupUi(self)
        self.setWindowTitle("截图工具")
        self.setWindowIcon(QIcon('./icon/cut.png'))
        self.screen = QApplication.primaryScreen()
        # 托盘行为
        self.action_quit = QAction("退出", self, triggered=self.close)
        self.action_show = QAction("主窗口", self, triggered=self.show)
        self.menu_tray = QMenu(self)
        self.menu_tray.addAction(self.action_quit)
        # 设置最小化托盘
        self.tray = QSystemTrayIcon(QIcon('./icon/screenshot.png'), self)  # 创建系统托盘对象
        self.tray.activated.connect(self.shot)  # 设置托盘点击事件处理函数
        self.tray.setContextMenu(self.menu_tray)
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
        self.hide()
        # time.sleep(0.2)  # 保证隐藏窗口
        # pixmap = self.screen.grabWindow(0)
        # painter = QPainter()
        # painter.setOpacity(0.5)
        # painter.begin(pixmap)
        # painter.end()

        self.label = ScreenLabel()
        # self.label.setPixmap(pixmap)
        self.label.showFullScreen()
        self.label.signal.connect(self.callback)

    def callback(self, pixmap):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        dialog = ShotDialog(pixmap)
        dialog.exec_()
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口

    def change_api(self):
        cfg.set('picbed', "api", self.lineEdit_api.text())

    def change_cookie(self):
        cfg.set('picbed', "cookie", self.lineEdit_cookie.text())

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            self.tray.showMessage("通知", "已最小化到托盘，点击开始截图")
            self.tray.show()
            self.hide()

    def closeEvent(self, event):
        reply = QMessageBox.information(self, "消息", "是否退出程序", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            print("修改配置文件")
            cfg.write(open("config.ini", "r+", encoding="utf-8"))
        else:
            event.ignore()


if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('config.ini')
    cfg.get('picbed', 'cookie')
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    height = QApplication.desktop().screenGeometry().height()
    width = QApplication.desktop().screenGeometry().width()
    sys.exit(app.exec_())
