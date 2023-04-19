from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import matplotlib.pyplot as plt
import requests
import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from requests_html import HTMLSession
import multiprocessing
import time
def getTweetText(link,queue):
    try:
        session = HTMLSession()
        r = session.get(link)
        r.html.render(sleep=2)
        tweet_text = r.html.find('.css-1dbjc4n.r-1s2bzr4', first=True)
        fetched_text = tweet_text.text
        queue.put(tweet_text.text)
        return fetched_text
    except:
        queue.put(None)
        return None

class Ui_Form(QDialog):
    def updateProgress(self):
        i=0
        while(i<101):
            if(not self.process.is_alive()):
                self.progress_dialog.setValue(100)
                break
            time.sleep(0.08)
            self.progress_dialog.setValue(i)
            i+=1
        self.progress_dialog.close()
            
    def showProgressBar(self,link):
        queue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=getTweetText, args=(link,queue))
        self.process.start()
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setLabelText("Fetching tweet...")
        self.progress_dialog.setRange(0, 100)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.show()
        self.updateProgress()
        self.process.join()
        return queue.get()
        
    def showPlot(self, stats):
        toxicity_classes = list(stats.keys())
        toxicity_levels = list(stats.values())
        colors = ['#0077B3', '#009E73', '#66CC66',
                  '#99CCFF', '#FFCC99', '#FF9966', '#FF6666']
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(toxicity_classes, toxicity_levels, color=colors)
        ax.set_xlabel('Toxicity Levels')
        ax.set_ylabel('Toxicity Classes')
        ax.set_title('Levels of Toxicity Classes')
        ax.set_xlim(0, 1)
        ax.grid(True, axis='x', linestyle='--', color='gray', alpha=0.5)
        ax.spines[['right', 'top']].set_visible(False)
        for i in range(len(toxicity_classes)):
            ax.text(toxicity_levels[i] + 0.02, i,
                    f'{toxicity_levels[i]:.2f}', ha='left', va='center')
        self.canvas = FigureCanvas(fig)
        self.verticalLayout_2.addWidget(self.canvas)

    def getStats(self, text):
        url = 'http://127.0.0.1:5000/predict'
        payload = {"text": text}
        headers = {'content-type': 'application/json'}
        response = requests.post(
            url, data=json.dumps(payload), headers=headers)
        data = response.json()
        return dict(data)

    def reset(self):
        self.text_input.clear()
        self.link_bool.setChecked(False)
        self.form.resize(700, 364)
        self.input.setText("Text:")
        self.text_input.setPlaceholderText("Enter text here!")
        self.retrived_display.setVisible(False)
        self.retrived_text_display.setVisible(False)
        try:
            self.canvas.deleteLater()
            self.verticalLayout_2.removeWidget(self.canvas)
        except Exception as e:
            print(e)
            pass
    def showStats(self):
        try:
            self.canvas.deleteLater()
            self.verticalLayout_2.removeWidget(self.canvas)
        except Exception as e:
            print(e)
            pass
        text = self.text_input.toPlainText()
        text = text.strip()
        if(text == "" or text==None):
            QMessageBox.critical(
                self, "Error", "Empty Text Passed. Cannot process!")
            self.reset()
            return
        if(self.link_bool.isChecked()):
            link = text.strip()
            text = self.showProgressBar(link)
            if(text == None):
                QMessageBox.critical(
                    self, "Error", "Link is not valid, or Tweet is older than one week!")
                self.reset()
                return
        self.retrived_display.setVisible(True)
        self.retrived_text_display.setVisible(True)
        self.retrived_text_display.setText(text)
        stats = self.getStats(text)
        self.form.resize(1100, 600)
        self.showPlot(stats)
    def onLinkCheck(self):
        if(self.link_bool.isChecked()):
            self.input.setText('Link:')
            self.text_input.setPlaceholderText("Enter link here!")
        else:
            self.input.setText('Text:')
            self.text_input.setPlaceholderText("Enter text here!")
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.canvas = None
        Form.resize(700, 364)
        self.form = Form
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.input = QLabel(Form)
        self.input.setObjectName(u"input")

        self.horizontalLayout.addWidget(self.input)

        self.text_input = QPlainTextEdit(Form)
        self.text_input.setObjectName(u"text_input")

        self.horizontalLayout.addWidget(self.text_input)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.link_bool = QRadioButton(Form)
        self.link_bool.setObjectName(u"link_bool")

        self.verticalLayout.addWidget(self.link_bool)

        self.submit_button = QPushButton(Form)
        self.submit_button.setObjectName(u"submit_button")

        self.verticalLayout.addWidget(self.submit_button)

        self.reset_button = QPushButton(Form)
        self.reset_button.setObjectName(u"reset_button")

        self.verticalLayout.addWidget(self.reset_button)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retrived_display = QLabel(Form)
        self.retrived_display.setObjectName(u"retrived_display")
        self.retrived_display.setText("Retrived Text:-")
        self.verticalLayout_2.addWidget(self.retrived_display)

        self.retrived_text_display = QLabel(Form)
        self.retrived_text_display.setObjectName(u"retrived_text_display")
        self.retrived_text_display.setText("Retrived Text:-")
        self.verticalLayout_2.addWidget(self.retrived_text_display)
        self.result_display = QLabel(Form)
        self.result_display.setObjectName(u"result_display")

        self.verticalLayout_2.addWidget(self.result_display)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.submit_button.clicked.connect(self.showStats)
        self.reset_button.clicked.connect(self.reset)
        self.link_bool.toggled.connect(self.onLinkCheck)
        self.retrived_display.setVisible(False)
        self.retrived_text_display.setVisible(False)
        
        
        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate(
            "Form", u"Text Toxicity Detector",  None))
        self.input.setText(QCoreApplication.translate("Form", u"Text:", None))
        self.text_input.setPlaceholderText(
            QCoreApplication.translate("Form", u"Enter text here!", None))
        self.link_bool.setText(QCoreApplication.translate(
            "Form", u"Is it a link?", None))
        self.submit_button.setText(
            QCoreApplication.translate("Form", u"Submit", None))
        self.reset_button.setText(
            QCoreApplication.translate("Form", u"Reset", None))
        self.result_display.setText(
            QCoreApplication.translate("Form", u"Result:-", None))
    # retranslateUi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    MainWindow.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
    MainWindow.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
    app.setStyle("Fusion")
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
