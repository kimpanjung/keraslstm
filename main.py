import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import random

import threading

# import Singleton
import ezKeras

from PIL import Image


def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


class Singleton:
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.epohc = 0
        self.batch = 0
        self.units = 0

        self.learn = False

        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

    def printParameter(self, epoch, batch, units):
        self.epohc = epoch
        self.batch = batch
        self.units = units

        print(self.epohc, self.batch, self.units)

    def getEpoch(self):
        # if self.learn == True:
        #     self.epohc = epoch
        return self.epohc


class MyApp(QDialog):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Parameter로 각각 Machine()을 받아야 할 듯.
        # Tab
        tabs = QTabWidget()
        tabs.addTab(FirstTab(), 'Dataset')
        tabs.addTab(SecondTab(), 'Learning')
        tabs.addTab(ThirdTab(), 'Compare Model')

        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        vbox.addWidget(buttonbox)

        self.setLayout(vbox)

        self.setWindowTitle('EZinfotech')
        self.setGeometry(300, 300, 400, 300)
        self.center()
        self.show()

    def center(self):
        self.setWindowTitle('EZinfotech')
        self.setGeometry(300, 300, 1000, 1000)
        # self.setFixedSize(1000,1000)
        self.show()

        qr = self.frameGeometry()  # 창 위치와 크기 정보 get
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Close 시 MsgBox
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


##### Dataset & Hyper Parameter Tap #####
class FirstTab(QWidget):

    def __init__(self):
        super().__init__()

        # Singleton
        self.singleton = Singleton()
        print("singleton test : ", self.singleton)

        # Dataset file Open
        self.fname = []  # filename
        self.total_le = QLineEdit()
        self.train_le = QLineEdit()
        self.test_le = QLineEdit()
        self.dir_le = QLineEdit()
        # index
        self.idxStart_le = QLineEdit()
        self.idxEnd_le = QLineEdit()

        # set hyper parameter
        self.epochs_spinBox = QSpinBox()
        self.units_spinBox = QSpinBox()
        self.batch_spinBox = QSpinBox()

        # Dataset Head Display
        self.head_te = QTextEdit()

        # Learning Instance
        self.machine = ezKeras.Machine()
        # machine.run(epochs=1, units=1, batch_size=512)

        # canvas
        self.datafigure = plt.figure()
        self.dataCanvas = FigureCanvas(self.datafigure)

        self.distributionfigure = plt.figure()
        self.distributionCanvas = FigureCanvas(self.distributionfigure)

        # fit() monitiring test
        self.fit_te = QTextEdit()

        # Dataset Graph
        self.datasetgraph = QLabel()

        # UI initialize
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.createDatasetGroup(), 0, 0)
        grid.addWidget(self.createHyperParameterGroup(), 0, 1)
        # grid.setColumnMinimumWidth(0,400)

        grid.addWidget(self.datasetGraph(), 1, 0)
        grid.addWidget(self.distributionGraph(), 1, 1)
        # grid.rowStretch(0)
        # grid.columnStretch(1)
        # grid.addWidget(self.createTrainingLoggingGroup(), 2, 0)
        # grid.addWidget(self.createTrainingResultGroup(), 2, 1)

        self.setLayout(grid)

    def display_textEdit(self, epochs, units, batch_size):
        self.fit_te.setText(str(self.machine.run(epochs=epochs, units=units, batch_size=batch_size)))

    def set_hyperparameter(self):

        self.epochs_spinBox.text()
        self.units_spinBox.text()
        self.batch_spinBox.text()

        print(self.epochs_spinBox.text(), self.units_spinBox.text(), self.batch_spinBox.text())

        epochs = int(self.epochs_spinBox.text())
        units = int(self.units_spinBox.text())
        batch = int(self.batch_spinBox.text())

        ## 학습 시작 ##
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        t = threading.Thread(target=self.machine.run, args=(epochs,units,batch))
        # #self.machine.run(epochs=epochs, units=units, batch_size=batch)
        # self.fit_te.setText(str(t))
        # t. start()
        #
        # t = threading.Thread(target=self.display_textEdit, args=(epochs, units, batch))
        # self.fit_te.setText(str(t))

        # single ton
        self.singleton.printParameter(epochs, batch, units)
        self.singleton.epohc = epochs
        self.singleton.learn = True

        t.start()

        #self.fit_te.setText(str(self.machine.run(epochs=epochs, units=units, batch_size=batch)))

        # 190723
        # 1 시작~ 끝난 시간 추가
        # 2 Tab 2 (learning tab) 확인하라는 메시지박스 표시
        # 3 데이터 셋 없을 경우 데이터셋 추가하라는 메시지 추가
        # 4 쓰레드 추가

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            # self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            # self.btn.setText('Stop')

        print(self.epochs_spinBox.text(), self.units_spinBox.text(), self.batch_spinBox.text())

    # 불러온 파일 이름 저장
    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        # @fname = 'C:\\Users\PJ\PycharmProjects\ezKeras\inner_data_new_0705.csv'

        if fname[0]:
            # pixmap = QPixmap(fname[0])
            # self.label.append(QLabel())
            # self.label[-1].setPixmap(pixmap.scaledToWidth(pixmap.width() * 1.1))
            self.fname.append(fname[0])
            print(self.fname)
            # self.x_le.append("파일 경로 : " + str(self.fname))
            # self.dir_le.setText(str(self.fname))
            self.dir_le.setText(fname[0])
            # machine = ezKeras.Machine(fname[0])
            self.machine.datasetLoad(fname[0])
            # self.machine.run(epochs=1, units=1, batch_size=512)

            self.total_le.setText(str(self.machine.totalDatasetNumber()))
            self.train_le.setText(str(self.machine.trainDatasetNumber()))
            self.test_le.setText(str(self.machine.testDatasetNumber()))

            self.head_te.setText(str(self.machine.datasethead()))

            # index
            self.idxStart_le.setText(str(self.machine.dayOfStart()))
            self.idxEnd_le.setText(str(self.machine.dayOfEnd()))

            self.plot()

            # Dataset 호출
            # self.hbox_label.addWidget(self.label[-1])

    def createDatasetGroup(self):

        groupbox = QGroupBox('■ Dataset Preview')
        layout = QVBoxLayout()

        hbox_index = QHBoxLayout()
        hbox_index.addWidget(QLabel('● Start Day:'))
        hbox_index.addWidget(self.idxStart_le)
        hbox_index.addWidget(QLabel('● End Day:'))
        hbox_index.addWidget(self.idxEnd_le)

        hbox_total = QHBoxLayout()
        hbox_total.addWidget(QLabel('● Total:'))
        hbox_total.addWidget(self.total_le)
        hbox_total.addWidget(QLabel('● Train:'))
        hbox_total.addWidget(self.train_le)
        hbox_total.addWidget(QLabel('● Test:'))
        hbox_total.addWidget(self.test_le)

        # self.total_le.setMaximumWidth(10)
        # self.train_le.setMaximumWidth(10)
        # self.test_le.setMaximumWidth(10)

        # self.idxStart_le.setFixedWidth(50)
        # self.idxEnd_le.setFixedWidth(50)

        self.total_le.setFixedWidth(90)
        self.train_le.setFixedWidth(90)
        self.test_le.setFixedWidth(90)

        self.total_le.setMinimumWidth(50)
        self.train_le.setMinimumWidth(50)
        self.test_le.setMinimumWidth(50)

        hbox_dir = QHBoxLayout()
        hbox_dir.addWidget(QLabel('● Directory:'))
        # self.dir_le.setta
        hbox_dir.addWidget(self.dir_le)
        self.dir_le.setMinimumWidth(10)
        # layout.addStretch(1)

        open_btn2 = QPushButton('Open Dataset')
        open_btn2.resize(open_btn2.sizeHint())
        open_btn2.clicked.connect(self.show_dialog)
        # hbox_dir.addStretch(1)
        hbox_dir.addWidget(open_btn2)
        # hbox_dir.addStretch(1)

        # hbox_xy.addStretch(3)
        layout.addLayout(hbox_index)
        layout.addLayout(hbox_total)
        # layout.addLayout(hbox_train)
        # layout.addLayout(hbox_test)
        layout.addLayout(hbox_dir)

        # Dataset sample view
        # layout.addLayout(hbox_head)
        # layout.addLayout(hbox_open)

        # layout.addStretch(1)
        groupbox.setLayout(layout)

        return groupbox

    # Hyper Parameter
    def createHyperParameterGroup(self):
        groupbox = QGroupBox('Set Hyper Parameters')
        # groupbox.setFlat(True)

        layout = QVBoxLayout()

        hbox_epochs = QHBoxLayout()
        hbox_epochs.addWidget(QLabel('● Epochs'))
        hbox_epochs.addWidget(self.epochs_spinBox)
        self.epochs_spinBox.setMinimum(0)
        self.epochs_spinBox.setMaximum(10001)
        self.epochs_spinBox.setAlignment(Qt.AlignLeft)

        hbox_units = QHBoxLayout()
        hbox_units.addWidget(QLabel('● Units'))
        hbox_units.addWidget(self.units_spinBox)
        self.units_spinBox.setMinimum(0)
        self.units_spinBox.setMaximum(10001)
        self.units_spinBox.setAlignment(Qt.AlignLeft)

        hbox_batch = QHBoxLayout()
        hbox_batch.addWidget(QLabel('● Batch_Size'))
        hbox_batch.addWidget(self.batch_spinBox)
        self.batch_spinBox.setMinimum(0)
        self.batch_spinBox.setMaximum(10001)
        self.batch_spinBox.setAlignment(Qt.AlignLeft)

        hbox_learning = QHBoxLayout()
        learning_btn = QPushButton('Done')
        learning_btn.resize(learning_btn.sizeHint())
        learning_btn.clicked.connect(self.set_hyperparameter)  # 학습함수

        # learning_btn.clicked.connect(self.plot)  # plot 테스트

        save_btn = QPushButton('Save')
        save_btn.resize(learning_btn.sizeHint())

        load_btn = QPushButton('Load')
        load_btn.resize(learning_btn.sizeHint())

        hbox_learning.addWidget(learning_btn)
        hbox_learning.addWidget(save_btn)
        hbox_learning.addWidget(load_btn)

        # learning test
        # hbox_test = QHBoxLayout()
        #
        # self.fit_te = QTextEdit(self)
        # self.fit_te.setText("( fit() test )")
        # self.fit_te.resize(self.fit_te.sizeHint())
        # hbox_test.addWidget(self.fit_te)
        # txt = self.textedit.toPlainText()
        # 내용글 얻어오기 self.statusbar.showMessage(txt) # 상태바에 출력

        # vbox = QVBoxLayout()
        # vbox2.addWidget(textedit)

        layout.addLayout(hbox_epochs)
        layout.addLayout(hbox_units)
        layout.addLayout(hbox_batch)
        layout.addLayout(hbox_learning)
        # layout.addLayout(hbox_test)

        # 190724 크기 조절 완료
        # layout.addStretch(1)
        groupbox.setLayout(layout)
        return groupbox

    # Dataset head
    def datasetGraph(self):
        groupbox = QGroupBox('Dataset Graph')
        groupbox.setFlat(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.dataCanvas)
        # self.dataCanvas.resize(450,900)
        groupbox.setLayout(vbox)

        return groupbox

    # Training Start, save, load
    def distributionGraph(self):

        groupbox = QGroupBox('Dataset Distribution Graph ')
        # groupbox.setCheckable(True)
        groupbox.setChecked(True)

        pushbutton = QPushButton('Training Start')
        togglebutton = QPushButton('Model Load')
        togglebutton.setCheckable(True)
        togglebutton.setChecked(True)

        vbox = QVBoxLayout()
        # vbox.addWidget(pushbutton)
        # vbox.addWidget(togglebutton)
        vbox.addStretch(1)

        ########### Canvas ##########
        vbox.addWidget(self.distributionCanvas)

        groupbox.setLayout(vbox)

        return groupbox

    # Canvas Test
    def plot(self):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]
        #
        # # create an axis
        # ax = self.datafigure.add_subplot(111)
        #
        # # discards the old graph
        # #ax.hold(False)
        #
        # # plot data
        # ax.plot(data, '*-')

        # refresh canvas
        # df = self.machine.data.origindataframe()
        df = self.machine.data.df_temp
        print(df.head(5))
        target_names = ['inner_temperature', 'inner_humidity', 'inner_co2']

        # self.datafigure = plt.figure(figsize=(10, 5))
        ax1 = self.datafigure.add_subplot(3, 1, 1)
        ax2 = self.datafigure.add_subplot(3, 1, 2)
        ax3 = self.datafigure.add_subplot(3, 1, 3)

        ax1.plot(df['inner_temperature'])
        ax1.set_ylabel(target_names[0])

        ax2.plot(df['inner_humidity'])
        ax2.set_ylabel(target_names[1])

        ax3.plot(df['inner_co2'])
        ax3.set_ylabel(target_names[2])
        # plt.show()

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(10)
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(10)
        for label in ax3.xaxis.get_ticklabels():
            label.set_rotation(10)

        self.dataCanvas.draw()

    def createTrainingLoggingGroup(self):
        # groupbox = QGroupBox('Training Log')
        # groupbox.setFlat(True)

        groupbox = QGroupBox('Dataset Graph')
        groupbox.setFlat(True)

        #######################
        hbox = QHBoxLayout()
        # hbox.addWidget(self.datasetgraph)
        # im = Image.open('C:\Users\PJ\Desktop\test_dirrush_hour.png')
        # pixmap = QPixmap('C:\\Users\PJ\Desktop\\test_dir\co2.png')
        # self.datasetgraph.setPixmap(pixmap.scaledToWidth(pixmap.width() * 0.5))

        groupbox.setLayout(hbox)
        return groupbox

    def createTrainingResultGroup(self):

        # 정규분포 화면
        groupbox = QGroupBox('-')
        groupbox.setFlat(True)

        textedit = QTextEdit(self)
        textedit.setText("(Graph)")
        textedit.resize(textedit.sizeHint())
        # txt = self.textedit.toPlainText()
        # 내용글 얻어오기 self.statusbar.showMessage(txt) # 상태바에 출력

        vbox = QVBoxLayout()
        vbox.addWidget(textedit)
        # vbox.addWidget(radio2)
        # vbox.addWidget(radio3)
        # vbox.addWidget(checkbox)
        # vbox.addStretch(1)
        groupbox.setLayout(vbox)
        # vbox.addStretch(1)

        return groupbox


class SecondTab(QWidget):

    def __init__(self):
        super().__init__()

        self.hyper_te = QTextEdit()
        self.hyper_te2 = QTextEdit()
        self.hyper_te3 = QTextEdit()

        self.singleton = Singleton.getInstance()
        print("2nd singleton test : ", self.singleton)

        # GroupBox #

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.hyperParameters(), 0, 0)
        # grid.addWidget(self.learningStart(), 0, 1)

        grid.addWidget(self.learningLogging(), 1, 0)
        grid.addWidget(self.learningResult(), 2, 0)
        # grid.rowStretch(0)
        # grid.columnStretch(1)
        # grid.addWidget(self.createTrainingLoggingGroup(), 2, 0)
        # grid.addWidget(self.createTrainingResultGroup(), 2, 1)

        self.setLayout(grid)

    def hyperParameters(self):
        groupbox = QGroupBox('Hyper Parameters')
        groupbox.setFlat(True)

        #######################
        hbox = QHBoxLayout()
        hbox.addWidget(self.hyper_te)

        singleton = Singleton.getInstance()
        if singleton.learn == True:
            self.hyper_te.setText(str(singleton.getEpoch()))

        groupbox.setLayout(hbox)
        return groupbox

    def learningStart(self):
        groupbox = QGroupBox('Hyper Parameters')
        groupbox.setFlat(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.hyper_te2)
        #######################
        hbox = QHBoxLayout()
        hbox.addWidget(self.hyper_te2)

        groupbox.setLayout(hbox)
        return groupbox

    def learningLogging(self):
        groupbox = QGroupBox('Training Log')
        groupbox.setFlat(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.hyper_te2)
        #######################
        hbox = QHBoxLayout()
        hbox.addWidget(self.hyper_te2)

        groupbox.setLayout(hbox)
        return groupbox

    def learningResult(self):
        groupbox = QGroupBox('Result')
        groupbox.setFlat(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.hyper_te3)
        #######################
        hbox = QHBoxLayout()
        hbox.addWidget(self.hyper_te3)

        groupbox.setLayout(hbox)
        return groupbox


class ThirdTab(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        lbl = QLabel('Terms and Conditions')
        text_browser = QTextBrowser()
        text_browser.setText('This is the terms and conditions')
        checkbox = QCheckBox('Check the terms and conditions.')

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(text_browser)
        vbox.addWidget(checkbox)

        self.setLayout(vbox)


if __name__ == '__main__':
    main()