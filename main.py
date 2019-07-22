import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon

import ezKeras

from PIL import Image


def main():

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


class MyApp(QDialog):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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
        self.show()

        qr = self.frameGeometry() # 창 위치와 크기 정보 get
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

        # Dataset file Open
        self.fname = [] # filename
        self.total_le = QLineEdit()
        self.train_le = QLineEdit()
        self.test_le = QLineEdit()
        self.dir_le = QLineEdit()

        # Dataset Head Display
        self.head_te = QTextEdit()

        # Learning Instance
        self.machine = ezKeras.Machine()
        #machine.run(epochs=1, units=1, batch_size=512)

        # Dataset Graph
        self.datasetgraph = QLabel()

        # UI initialize
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createDatasetGroup(), 0, 0)
        grid.addWidget(self.createHyperParameterGroup(), 0, 1)

        grid.addWidget(self.createTrainingModelGroup(), 1, 0)
        grid.addWidget(self.createTrainingManageGroup(), 1, 1)

        grid.addWidget(self.createTrainingLoggingGroup(), 2, 0)
        grid.addWidget(self.createTrainingResultGroup(), 2, 1)

        self.setLayout(grid)

        # Button
        self.setButton()

    # Button setting
    def setButton(self):
        # buttons
        startBtn = QPushButton('Load', self)
        startBtn.setToolTip('<b>Training</b>')
        startBtn.move(850, 800/3)
        startBtn.resize(startBtn.sizeHint())

        setBtn = QPushButton('Save', self)
        setBtn.setToolTip('<b>Set Parameter</b>')
        setBtn.move(850, 800/3 - 25)
        setBtn.resize(setBtn.sizeHint())

        # Quit
        #open_btn.clicked.connect(QCoreApplication.instance().quit)

    # 불러온 파일 이름 저장
    def show_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

        if fname[0]:
            #pixmap = QPixmap(fname[0])
            #self.label.append(QLabel())
            #self.label[-1].setPixmap(pixmap.scaledToWidth(pixmap.width() * 1.1))
            self.fname.append(fname[0])
            print(self.fname)
            #self.x_le.append("파일 경로 : " + str(self.fname))
            # self.dir_le.setText(str(self.fname))
            self.dir_le.setText(fname[0])
            #machine = ezKeras.Machine(fname[0])
            self.machine.datasetLoad(fname[0])
            #self.machine.run(epochs=1, units=1, batch_size=512)

            self.total_le.setText(str(self.machine.totalDatasetNumber()))
            self.train_le.setText(str(self.machine.trainDatasetNumber()))
            self.test_le.setText(str(self.machine.testDatasetNumber()))

            self.head_te.setText(str(self.machine.datasethead()))



            # Dataset 호출

            #self.hbox_label.addWidget(self.label[-1])

    def createDatasetGroup(self):

        groupbox = QGroupBox('■ Dataset Preview')

        layout = QVBoxLayout()

        hbox_total = QHBoxLayout()
        #hbox_xy.addStretch(5)
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

    # Hyper Parameter
    def createHyperParameterGroup(self):
        groupbox = QGroupBox('Set Hyper Parameters')
        groupbox.setFlat(True)

        lbl1 = QLabel('Epoch')
        spinbox = QSpinBox()
        spinbox.setMinimum(-10)
        spinbox.setMaximum(30)
        # self.spinbox.setRange(-10, 30)
        spinbox.setSingleStep(2)
        #lbl2 = QLabel('0')

        #spinbox.valueChanged.connect(self.value_changed)
        #lbl2.setText(str(spinbox.value()))

        lbl2 = QLabel('Batch_size')
        spinbox2 = QSpinBox()
        spinbox2.setMinimum(-10)
        spinbox2.setMaximum(30)
        spinbox2.setSingleStep(2)

        # Activation
        lbl3 = QLabel('Activation Func')
        spinbox3 = QSpinBox()
        spinbox3.setMinimum(-10)
        spinbox3.setMaximum(30)
        spinbox3.setSingleStep(2)

        vbox = QVBoxLayout()

        vbox.addWidget(lbl1)
        vbox.addWidget(spinbox)

        vbox.addWidget(lbl2)
        vbox.addWidget(spinbox2)

        vbox.addWidget(lbl3)
        vbox.addWidget(spinbox3)

        vbox.addStretch()

        groupbox.setLayout(vbox)

        return groupbox

    # Dataset head
    def createTrainingModelGroup(self):
        groupbox = QGroupBox('Dataset Sample (50 Indexes)')
        groupbox.setFlat(True)
        return groupbox


    # Training Start, save, load
    def createTrainingManageGroup(self):

        groupbox = QGroupBox('Dataset Normal Distribution ')
        #groupbox.setCheckable(True)
        groupbox.setChecked(True)

        pushbutton = QPushButton('Training Start')
        togglebutton = QPushButton('Model Load')
        togglebutton.setCheckable(True)
        togglebutton.setChecked(True)

        vbox = QVBoxLayout()
        #vbox.addWidget(pushbutton)
        #vbox.addWidget(togglebutton)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

    def createTrainingLoggingGroup(self):
        # groupbox = QGroupBox('Training Log')
        # groupbox.setFlat(True)

        groupbox = QGroupBox('Dataset Graph')
        groupbox.setFlat(True)

        #######################
        hbox = QHBoxLayout()
        hbox.addWidget(self.datasetgraph)
        #im = Image.open('C:\Users\PJ\Desktop\test_dirrush_hour.png')
        pixmap = QPixmap('C:\\Users\PJ\Desktop\\test_dir\co2.png')
        self.datasetgraph.setPixmap(pixmap.scaledToWidth(pixmap.width() * 0.5))

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
        #vbox.addStretch(1)
        groupbox.setLayout(vbox)
        #vbox.addStretch(1)

        return groupbox


class SecondTab(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        hyper_group = QGroupBox('Hyper Parameters')

        #groupbox = QGroupBox('Dataset Preview')

        label1 = QLabel('Epochs : ', self)
        label1.setAlignment(Qt.AlignVCenter)

        label2 = QLabel('Batch_size : ', self)
        label2.setAlignment(Qt.AlignVCenter)

        label3 = QLabel('Units : ', self)
        label3.setAlignment(Qt.AlignVCenter)

        font1 = label1.font()
        font1.setPointSize(11)

        # font2 = label2.font()
        # font2.setFamily('Times New Roman')
        # font2.setBold(True)

        label1.setFont(font1)
        label2.setFont(font1)
        label3.setFont(font1)
        # label2.setFont(font2)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addStretch(1)

        hyper_group.setLayout(layout)
        #groupbox.setLayout(layout)
        hyper_group.setLayout(layout)
        #hyper_group.setLayout(vbox1)

        ####################################
        logging_group = QGroupBox('Training Log')

        vbox2 = QVBoxLayout()

        textedit = QTextEdit(self)
        textedit.setText("(Epoch)")
        textedit.resize(textedit.sizeHint())
        # txt = self.textedit.toPlainText()
        # 내용글 얻어오기 self.statusbar.showMessage(txt) # 상태바에 출력

        #vbox = QVBoxLayout()
        vbox2.addWidget(textedit)


        logging_group.setLayout(vbox2)

        ##############################
        result_group = QGroupBox('Result Graph')

        vbox3 = QVBoxLayout()

        textedit2 = QTextEdit(self)
        textedit2.setText("(Graph)")
        textedit2.resize(textedit2.sizeHint())
        # txt = self.textedit.toPlainText()
        # 내용글 얻어오기 self.statusbar.showMessage(txt) # 상태바에 출력

        # vbox = QVBoxLayout()
        vbox3.addWidget(textedit2)

        result_group.setLayout(vbox3)
        #####

        vbox = QVBoxLayout()
        vbox.addWidget(hyper_group)
        vbox.addWidget(logging_group)
        vbox.addWidget(result_group)
        self.setLayout(vbox)


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