import os
import sys
import tempfile
import time

from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from posemon import Ui_MainWindow

from pulgin.modelLearn import *
from pulgin.movenetPoseMark import MoveNetPoseMark
from pulgin.movenetClassifier import MoveNetClassifier


class ConsoleRedirect:
    def __init__(self, console):
        self.console = console
        self.original_stdout = sys.stdout

    def write(self, message):
        self.original_stdout.write(message)
        self.console.moveCursor(QtGui.QTextCursor.End) # 移动光标到文本末尾
        self.console.insertPlainText(message) # 添加消息到文本末尾，会自动在新行开始添加


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        with open(f'./data/labels.txt', 'r') as label_file:
            self.class_names = list(label_file)
        self.classifier = MoveNetClassifier()
        self.classifier.build_model(model_path="./model/run_classifier")

        self.ui.pushButton.clicked.connect(self.openFolder)
        self.ui.pushButton_2.clicked.connect(self.predict)

    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.ui.textEdit.setText(folder_path)

    def predict(self):
        folder_path = self.ui.textEdit.toPlainText().strip()
        if len(folder_path) == 0:
            QMessageBox.warning(self, "提示", "请先打开图片或者视频所在文件夹！")
            return
        predict_method = self.ui.comboBox.currentText()
        predict_model = self.ui.comboBox_2.currentText()
        # y_pred_label, messages = None, None
        if predict_method == "图片估计":
            csvs_path = tempfile.mkdtemp() + "/predict.csv"
            poseMark = MoveNetPoseMark(model_path=f"./model/{predict_model}")
            messages, predict_pose = poseMark.img_predict(folder=folder_path, csvs_path=csvs_path)
            filename, data_value, _ = split_pose_landmarks(predict_pose)
            y_pred = self.classifier.predict(data_value)
            file = [name.split("_")[0] for name in filename]
            y_pred = [self.class_names[i].rstrip() for i in np.argmax(y_pred, axis=1)]
            y_pred_label = [f"{f} is {p}" for f, p in zip(filename, y_pred)]
            # self.ui.textEdit_1.setText('\n'.join(y_pred_label))
            # self.ui.textEdit_2.setText('\n'.join(messages))
        else:
            csvs_path = tempfile.mkdtemp() + "/predict.csv"
            filename, messages, file, y_pred = os.listdir(folder_path), [], [], []
            poseMark = MoveNetPoseMark(model_path=f"./model/{predict_model}")
            for name in filename:
                message, predict_pose = poseMark.vid_predict(vid_path=f"{folder_path}/{name}", csvs_path=csvs_path)
                messages.extend(message)
                _, data_value, _ = split_pose_landmarks(predict_pose)
                pred = self.classifier.predict(data_value)
                file.append(name.split("_")[0])
                y_pred.append(self.class_names[np.argmax(np.sum(pred, axis=0), axis=0)].rstrip())
            y_pred_label = [f"{f} is {p}" for f, p in zip(filename, y_pred)]
            # self.ui.textEdit_1.setText('\n'.join(y_pred_label))
            # self.ui.textEdit_2.setText('\n'.join(messages))
        self.ui.textEdit_1.setText('\n'.join(y_pred_label))
        self.ui.textEdit_2.setText('\n'.join(messages))
        result = np.sum(np.array(file) == np.array(y_pred))
        print("accuracy: {}%".format(result / len(y_pred) * 100))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # # 在控制台窗口关闭之前等待一段时间
    # print("程序正在运行...")
    # time.sleep(1)
    sys.exit(app.exec())
