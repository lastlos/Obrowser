from functools import cached_property
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.currentChanged.connect(self.ctc)
        self.tabs.tabCloseRequested.connect(self.cct)
        self.tabs.tabBarDoubleClicked.connect(self.new)
        self.setCentralWidget(self.tabs)
        tool = QToolBar()
        self.addToolBar(tool)
        self.showMaximized()
        tool.adjustSize()
        self.setWindowTitle("Obrowser")
        home = QAction('🏠', self)
        home.triggered.connect(self.home)
        tool.addAction(home)
        rel = QAction('↺', self)
        rel.triggered.connect(lambda: self.tabs.currentWidget().reload())
        tool.addAction(rel)
        self.ubar = QLineEdit()
        self.ubar.returnPressed.connect(self.oluw)
        tool.addWidget(self.ubar)
        self.sbar = QLineEdit("Search")
        self.sbar.returnPressed.connect(self.osr)
        tool.addWidget(self.sbar)
        goback = QAction('◀️', self)
        goback.triggered.connect(lambda: self.tabs.currentWidget().back())
        tool.addAction(goback)   
        go = QAction('▶️', self)
        go.triggered.connect(lambda: self.tabs.currentWidget().forward())
        tool.addAction(go)                 
        self.add_new_tab(QUrl('http://www.duckduckgo.com'), 'Ana Sayfa')
        self.show()

    def ctc(self, i):
        qurl = self.tabs.currentWidget().url()
        self.ouw(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def add_new_tab(self, qurl = None, label ="Blank"):
        if qurl is None:
            qurl = QUrl('http://www.duckduckgo.com')
        brws = QWebEngineView()
        brws.setUrl(qurl)
        i = self.tabs.addTab(brws, label)
        self.tabs.setCurrentIndex(i)
        brws.urlChanged.connect(lambda qurl, brws = brws:
                                   self.ouw(qurl, brws))
        brws.loadFinished.connect(lambda _, i = i, brws = brws:
                                     self.tabs.setTabText(i, brws.page().title()))

    def update_title(self, brws):
        if brws != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - OBrowser" % title)

    def cct(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def new(self, i):
        if i == -1:
            self.add_new_tab()

    def oluw(self):
        url = self.ubar.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def ouw(self, q, brws = None):
        if brws != self.tabs.currentWidget():
 
            return

        self.ubar.setText(q.toString())
        self.ubar.setCursorPosition(0)

    def home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com"))

    def osr(self):
        search = self.sbar.text()
        url = "https://duckduckgo.com/?q="
        bas = url, search
        self.tabs.currentWidget().setUrl(QUrl(''.join(bas)))

def run():
    app = QApplication(sys.argv)
    x = MainWindow()
    x.show
    app.exec()

run()