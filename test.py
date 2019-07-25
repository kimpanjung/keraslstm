import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class App(QMainWindow):

    def init(self):
        super().init()
        self.title = "Hello PyQt5 users"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    def init(self, parent):
        super(QWidget, self).init(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("Press here to open Tab 2")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.pushButton1.clicked.connect(self.on_click_select_tab2)


def on_click_select_tab2(self):
    QtWidgets.QTabWidget.setCurrentIndex(self.tabs, 1)


if name == 'main':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    # set hyper parameter
    self.epochs_spinBox = QSpinBox()
    self.units_spinBox = QSpinBox()
    self.batch_spinBox = QSpinBox()

    def createDatasetGroup(self):

        groupbox = QGroupBox('■ Dataset Preview')
        layout = QVBoxLayout()

        hbox_total = QHBoxLayout()
        hbox_total.addWidget(QLabel(' ● Total : '))
        hbox_total.addWidget(self.total_le)
        self.total_le.setAlignment(Qt.AlignLeft)

        hbox_train = QHBoxLayout()
        hbox_train.addWidget(QLabel(' ● Train : '))
        hbox_train.addWidget(self.train_le)
        self.train_le.setAlignment(Qt.AlignLeft)

        hbox_test = QHBoxLayout()
        hbox_test.addWidget(QLabel(' ● Test : '))
        hbox_test.addWidget(self.test_le)
        self.test_le.setAlignment(Qt.AlignLeft)

        hbox_dir = QHBoxLayout()
        hbox_dir.addWidget(QLabel(' ● Directory : '))
        hbox_dir.addWidget(self.dir_le)
        # layout.addStretch(1)

        hbox_head = QVBoxLayout()
        hbox_head.addWidget(QLabel(' ● Dataset Sample (50 Indexes) : '))
        self.head_te = QTextEdit(self)
        self.head_te.setText("Dataset head()")
        self.head_te.resize(self.head_te.sizeHint())
        hbox_head.addWidget(self.head_te)

        hbox_open = QHBoxLayout()
        open_btn2  = QPushButton('Open Dataset (*.csv)')
        open_btn2.resize(open_btn2 .sizeHint())
        open_btn2.clicked.connect(self.show_dialog)
        hbox_open.addWidget(open_btn2)

        #
        #hbox_xy.addStretch(3)
        layout.addLayout(hbox_total)
        layout.addLayout(hbox_train)
        layout.addLayout(hbox_test)
        layout.addLayout(hbox_dir)
        layout.addLayout(hbox_head)
        layout.addLayout(hbox_open)

        layout.addStretch(1)
        groupbox.setLayout(layout)

        return groupbox

