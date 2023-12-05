import os
import matplotlib
import numpy as np
from math import isfinite

matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,QLabel
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QTimer,Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib

from math_interpreter.compiler import evaluate_expr


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Calculator")

        self.setGeometry(390,150,600,800)
        self.setStyleSheet("background-color: rgb(8,3,50);")

        self.base_widget = BaseWidget()

        self.setCentralWidget(self.base_widget)

class BaseWidget(QWidget):
    def __init__(self):

        super().__init__()
        
        v_layout = QVBoxLayout()

        self.setLayout(v_layout)

        self.tabs = PageTabs()

        v_layout.addWidget(self.tabs)

        self.calculator_page = CalculatorPage()
        self.functions_page  = FunctionsPage()
        
        v_layout.addWidget(self.calculator_page)
        v_layout.addWidget(self.functions_page)
        self.functions_page.hide()

        for btn in self.tabs.btn_list:
            btn.clicked.connect(self.select_page)
    
    def select_page(self):
        btn = self.sender()
        btn_name = btn.text()
        print(btn_name)
        if btn_name == "Calculator":
            self.calculator_page.show()
            self.functions_page.hide()
        elif btn_name == "Functions":
            self.functions_page.show()
            self.calculator_page.hide()
        else:
            print("invalid page")

class PageTabs(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.btn_calculator = TabButton("Calculator")
        self.btn_functions = TabButton("Functions")
        self.btn_graph = TabButton("Graph")
        self.main_layout.addWidget(self.btn_calculator)
        self.main_layout.addWidget(self.btn_functions)
        self.main_layout.addWidget(self.btn_graph)

        self.main_layout.setSpacing(0)
        self.main_layout.setStretch(0,0)
        self.setContentsMargins(0,0,0,0)
        self.setMaximumHeight(50)

        self.setLayout(self.main_layout)
        self.btn_list = [self.btn_calculator,self.btn_functions,self.btn_graph]

class CalculatorPage(QWidget):
    def __init__(self):
        super().__init__()

        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        self.user_input = ExpressionView()
        self.btn_user_submit = QPushButton("Submit")
        self.btn_user_submit.setMinimumSize(100,70)
        self.btn_user_submit.setMaximumSize(100,70)
        self.btn_user_submit.setStyleSheet("background-color: rgb(8,3,68); font-size: 18px; color: white; outline: 1px; border-style: solid; border-width: 4px; border-color: rgb(20,8,130); border-radius: 4px;")

        self.btn_user_submit.clicked.connect(self.evaluate)

        self.user_input.setReadOnly(1)

        user_in_container = QHBoxLayout()
        user_in_container.addWidget(self.user_input)
        user_in_container.addWidget(self.btn_user_submit)
        user_in_container.setContentsMargins(0,0,0,0)

        v_layout.addLayout(user_in_container)

        self.calc_btns = CalculatorButtonsGrid()

        for btn in self.calc_btns.btns_arr:
            btn.clicked.connect(self.handle_calc_btn_clicks)

        v_layout.addWidget(self.calc_btns)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setStyleSheet("background-color: rgb(8,3,68); font-size: 16px; color: white; border: 4px; border-style: solid; border-color: rgb(20,8,130); border-radius: 4px;")

        self.btn_clear.clicked.connect(self.clear_input)
        v_layout.addWidget(self.btn_clear)

    def handle_calc_btn_clicks(self):
        btn = self.sender()
        btn_name = btn.text()
        print(f"{btn_name} clicked")

        curr_text = self.user_input.text()
        self.user_input.setText(curr_text + btn_name)
    
    def clear_input(self):
        self.user_input.clear()
    
    def evaluate(self):
        res = evaluate_expr(self.user_input.text().replace("÷","/"))
        ans = res[0]
        if (type(ans) != str and not isfinite(ans)):
            return "INFINITY"
        
        ans_string = str(ans)
        if ans_string.count('.') > 0:
            ans_string = ans_string.rstrip('0')

        # If the result ends with a decimal point, remove it
        if ans_string.endswith('.'):
            ans_string = ans_string[:-1]

        self.user_input.setText(ans_string)
    
    def keyPressEvent(self, event) -> None:

        if self.user_input.text() == "ERROR":
            self.user_input.clear()
        key = event.key()
        curr_text = self.user_input.text()
        if key == Qt.Key_1:
            self.user_input.setText(curr_text + "1")
        elif key == Qt.Key_2:
            self.user_input.setText(curr_text + "2")
        elif key == Qt.Key_3:
            self.user_input.setText(curr_text + "3")
        elif key == Qt.Key_4:
            self.user_input.setText(curr_text + "4")
        elif key == Qt.Key_5:
            self.user_input.setText(curr_text + "5")
        elif key == Qt.Key_6:
            self.user_input.setText(curr_text + "6")
        elif key == Qt.Key_7:
            self.user_input.setText(curr_text + "7")
        elif key == Qt.Key_8:
            self.user_input.setText(curr_text + "8")
        elif key == Qt.Key_9:
            self.user_input.setText(curr_text + "9")
        elif key == Qt.Key_0:
            self.user_input.setText(curr_text + "0")
        elif key == Qt.Key_Plus:
            self.user_input.setText(curr_text + "+")
        elif key == Qt.Key_Minus:
            self.user_input.setText(curr_text + "-")
        elif key == 42:
            self.user_input.setText(curr_text + "*")
        elif key == 46:
            self.user_input.setText(curr_text + ".")
        elif key == 47:
            self.user_input.setText(curr_text + "÷")
        elif key == 16777220:
            self.evaluate()
        elif key == 67:
            self.user_input.clear()
        elif key == 68:
            self.user_input.setText(curr_text[:len(curr_text)-1])
        else:
            print("invalid keypress")

        print(f"pressed key:{key} ")
        return super().keyPressEvent(event)

class CalculatorButtonsGrid(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QGridLayout()
        # self.main_layout.setContentsMargins(0,0,0,0)

        self.setLayout(self.main_layout)

        self.btns_arr = []

        self.make_calc_buttons()
    
    def make_calc_buttons(self):
        self.calc_btn_1 = MainGridButton("1")
        self.calc_btn_2 = MainGridButton("2")
        self.calc_btn_3 = MainGridButton("3")
        self.calc_btn_4 = MainGridButton("4")
        self.calc_btn_5 = MainGridButton("5")
        self.calc_btn_6 = MainGridButton("6")
        self.calc_btn_7 = MainGridButton("7")
        self.calc_btn_8 = MainGridButton("8")
        self.calc_btn_9 = MainGridButton("9")
        self.calc_btn_decimal = MainGridButton(".")
        self.calc_btn_0 = MainGridButton("0")
        self.calc_btn_neg = MainGridButton("-")

        self.calc_btn_add = MainGridButton("+")
        self.calc_btn_minus = MainGridButton("-")
        self.calc_btn_multiply = MainGridButton("*")
        self.calc_btn_divide = MainGridButton("÷")
        
        self.main_layout.addWidget(self.calc_btn_1, 0, 1)
        self.main_layout.addWidget(self.calc_btn_2, 0, 2)
        self.main_layout.addWidget(self.calc_btn_3, 0, 3)
        self.main_layout.addWidget(self.calc_btn_add, 0, 4)
        self.main_layout.addWidget(self.calc_btn_4, 1, 1)
        self.main_layout.addWidget(self.calc_btn_5, 1, 2)
        self.main_layout.addWidget(self.calc_btn_6, 1, 3)
        self.main_layout.addWidget(self.calc_btn_minus, 1, 4)
        self.main_layout.addWidget(self.calc_btn_7, 2, 1)
        self.main_layout.addWidget(self.calc_btn_8, 2, 2)
        self.main_layout.addWidget(self.calc_btn_9, 2, 3)
        self.main_layout.addWidget(self.calc_btn_multiply, 2, 4)
        self.main_layout.addWidget(self.calc_btn_decimal, 3, 1)
        self.main_layout.addWidget(self.calc_btn_0, 3, 2)
        self.main_layout.addWidget(self.calc_btn_neg, 3, 3)
        self.main_layout.addWidget(self.calc_btn_divide, 3, 4)


        self.btns_arr.append(self.calc_btn_1)
        self.btns_arr.append(self.calc_btn_2)
        self.btns_arr.append(self.calc_btn_3)
        self.btns_arr.append(self.calc_btn_4)
        self.btns_arr.append(self.calc_btn_5)
        self.btns_arr.append(self.calc_btn_6)
        self.btns_arr.append(self.calc_btn_7)
        self.btns_arr.append(self.calc_btn_8)
        self.btns_arr.append(self.calc_btn_9)
        self.btns_arr.append(self.calc_btn_0)
        self.btns_arr.append(self.calc_btn_neg)
        self.btns_arr.append(self.calc_btn_divide)
        self.btns_arr.append(self.calc_btn_add)
        self.btns_arr.append(self.calc_btn_minus)
        self.btns_arr.append(self.calc_btn_multiply)
        self.btns_arr.append(self.calc_btn_divide)

class FunctionsPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.user_in_layout = QHBoxLayout()

        self.func_in_1_label = QLabel("F(x) = ")
        self.func_in_1_label.setMinimumSize(60,36)
        self.func_in_1_label.setMaximumSize(60,36)
        self.func_in_1_label.setStyleSheet("font-size: 16px; color: white;")

        self.func_in_1 = QLineEdit()
        self.func_in_1.setMinimumHeight(36)
        self.func_in_1.setMaximumHeight(36)
        self.func_in_1.setStyleSheet("background-color: rgb(20,8,130); font-size: 16px; color: white;")

        self.btn_gen_func_1 = QPushButton("Generate")
        self.btn_gen_func_1.setMinimumHeight(36)
        self.btn_gen_func_1.setMaximumHeight(36)
        self.btn_gen_func_1.setStyleSheet("background-color: rgb(8,3,68); font-size: 16px; color: white; outline: 1px; border-style: solid; border-width: 4px; border-color: rgb(20,8,130); border-radius: 4px;")


        self.xmin_in_1 = NumInput("xmin:")
        self.xmax_in_1 = NumInput("xmax:")
        self.ymin_in_1 = NumInput("ymin:")
        self.ymax_in_1 = NumInput("ymax:")

        self.axes_set = False

        self.btn_set_limits = QPushButton("Set")
        self.btn_set_limits.setStyleSheet("background-color: rgb(20,8,130); color: white;")

        self.axes_ins_container = QHBoxLayout()

        self.axes_ins_container.addWidget(self.xmin_in_1)
        self.axes_ins_container.addWidget(self.xmax_in_1)
        self.axes_ins_container.addWidget(self.ymin_in_1)
        self.axes_ins_container.addWidget(self.ymax_in_1)
        self.axes_ins_container.addWidget(self.btn_set_limits)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.grid(which='major', color="#888888")
        self.canvas.axes.grid(which='minor', color="#DDDDDD")
        self.canvas.axes.minorticks_on()

        self.timer = None
        self.num_loops = 0
        self.n_pts = 100

        self.connect_buttons()

        self.user_in_layout.addWidget(self.func_in_1_label)
        self.user_in_layout.addWidget(self.func_in_1)
        self.user_in_layout.addWidget(self.btn_gen_func_1)

        self.main_layout.addLayout(self.user_in_layout)
        self.main_layout.addLayout(self.axes_ins_container)
        self.main_layout.addWidget(self.canvas)
    
    def connect_buttons(self):
        self.btn_gen_func_1.clicked.connect(self.start_plotting)
        self.btn_set_limits.clicked.connect(self.set_axes)

    def set_axes(self):
        self.axes_set = False
        if (self.xmin_in_1.input.text() != "" and self.xmax_in_1.input.text() != "" and self.ymin_in_1.input.text() != "" and self.ymax_in_1.input.text() != ""):
            self.axes_set = True
            self.canvas.axes.set_xlim(int(self.xmin_in_1.input.text()),int(self.xmax_in_1.input.text()))
            self.canvas.axes.set_ylim(int(self.ymin_in_1.input.text()),int(self.ymax_in_1.input.text()))
            self.canvas.draw()
        
    def start_plotting(self):
        if (self.axes_set == True):
            x_limits = self.canvas.axes.get_xlim()
            y_limits = self.canvas.axes.get_ylim()
            self.canvas.axes.clear()
            self.canvas.axes.grid(which='major', color="#888888")
            self.canvas.axes.grid(which='minor', color="#DDDDDD")
            self.canvas.axes.minorticks_on()
            self.canvas.axes.set_xlim(x_limits)
            self.canvas.axes.set_ylim(y_limits)
            self.canvas.axes.set_title("F(x) = " + self.func_in_1.text())
            self.x_data = list(np.linspace(x_limits[0],x_limits[1],self.n_pts))
            expr = self.func_in_1.text()
            self.y_data = [evaluate_expr(expr.replace('x',str(self.x_data[i]))) for i in range(self.n_pts)]
            self.timer = QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.update_plot)
            self.timer.start()
        else:
            print("axes not set")

    def update_plot(self):
        print("attempting to update plot...")

        if self.num_loops < self.n_pts:
            self.canvas.axes.plot(self.x_data[0:self.num_loops],self.y_data[0:self.num_loops],'r')
            self.canvas.draw()
            print(self.num_loops)
            self.num_loops += 1
            print("success")
        else:
            print("done")
            self.num_loops = 0
            self.timer.stop()
        
class ExpressionView(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 48px;")
        font_path = "/Users/snwilson/Desktop/personal/python_projects/graphing_calculator/assets/digital_font/Digital7Mono-Yz9J4.ttf"

        self.setMaximumHeight(70)
        self.setMinimumHeight(70)
        self.setStyleSheet("background-color: rgb(20,8,131); font-size: 40px;")

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)

            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)
                if font_family:
                    self.font = self.font()
                    self.font.setFamily(font_family[0])
                    self.setFont(self.font)
                else:
                    print("Font family not found.")
            else:
                print("Failed to load the font.")
        else:
            print(f"Font file not found at: {font_path}")

class TabButton(QPushButton):
    def __init__(self, text):
        super().__init__()

        self.setStyleSheet("background-color: rgb(8,3,68); font-size: 16px; color: white; outline: 1px; border-style: solid; border-left: none; border-right: none; border-width: 4px; border-color: rgb(20,8,130); border-radius: 4px;")
        # self.setContentsMargins(0,0,0,0)
        self.setMaximumSize(200,80)
        self.setText(text)

class MainGridButton(QPushButton):
    def __init__(self, text):
        super().__init__()

        self.setStyleSheet("background-color: rgb(8,3,68); font-size: 72px; color: white; outline: 1px; border-style: solid; border-width: 4px; border-color: rgb(20,8,130); border-radius: 4px;")
        
        self.setMaximumSize(100,100)
        self.setText(text)

class NumInput(QWidget):
    def __init__(self, label_text):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(label_text)

        self.setMaximumSize(120,60)
        self.setMinimumSize(120,60)

        self.label.setMinimumWidth(60)
        self.label.setMaximumWidth(60)
        self.label.setStyleSheet("font-weight: bold; color: white; font-size: 16px")
        
        self.input = QLineEdit()

        self.input.setMinimumWidth(60)
        self.input.setMaximumWidth(60)
        self.input.setStyleSheet("background-color: rgb(20,8,130); font-size: 16px; color: white;")
        self.input.setMaxLength(5)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)