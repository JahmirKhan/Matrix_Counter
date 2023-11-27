import random

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

from kivy.clock import Clock

import matrix as mtx

#Класс создания матрицы и надписей указывающих на матрицу
class MyInputMatrix(GridLayout):
    def __init__(self, size_col, size_row, **kwargs):
        super(MyInputMatrix, self).__init__(**kwargs)
        self.cols = 1

        self.result_matrix = GridLayout(
            spacing=3,
            size_hint=(1, 1),
            padding=(5, 5, 5, 5))
        self.result_matrix.cols = size_col
        size = (size_col + size_row) / 2
        self.result = []
        for i in range(size_col):
            for j in range(size_row):
                textinput = TextInput(background_color=(80/255, 80/255, 80/255, 1),foreground_color = (1,1,1,1),
                    font_size=int(120 / size),
                    size_hint_y=1)
                self.result.append(textinput)
                self.result_matrix.add_widget(textinput)

        self.input_matrix = GridLayout(height=self.width, spacing=3, padding=(10, 10, 10, 10))
        self.input_matrix.cols = size_col
        self.input = []
        for i in range(size_col):
            for j in range(size_row):
                textinput = TextInput(background_color=(80/255, 80/255, 80/255, 1),foreground_color = (1,1,1,1),
                    font_size=int(100 / size),
                    size_hint_y=1)

                self.input.append(textinput)
                self.input_matrix.add_widget(textinput)

        self.output = Label(text=f'Матрица B размером {size_row}х{size_col}:', font_size=25, size_hint=(0.1, 0.1),outline_color='green')
        self.add_widget(self.output)
        self.add_widget(self.result_matrix)
        self.ishod = Label(text=f'Матрица А размером {size_row}х{size_col}:', font_size=25, size_hint=(0.1, 0.1))
        self.add_widget(self.ishod)
        self.add_widget(self.input_matrix)

#Основная программа, в которой создаются все кнопки, и их методы
class MyGridLayout(GridLayout):

    #Метод создания кнопок
    def add_button(self, text, button_action,buttons,background_color=(58/255, 58/255, 58/255,1)):
        size_hint=(0.1, 0.1)
        button = Button(text=text, size_hint=size_hint, font_size=17,
        background_normal = '',background_color=background_color)
        button.bind(on_press=button_action)
        buttons.add_widget(button)

    # Задание кнопок
    def create_buttons(self):
        buttons_dir = []

        self.buttons = GridLayout(cols=1, size_hint=(0.5, 0.5), padding=10,spacing=2)
        self.change_size_row = GridLayout(cols=2,size_hint=(0.2, 0.2),padding=(5,0,5,0),spacing=2)
        self.change_size_col = GridLayout(cols=2,size_hint=(0.2, 0.2),padding=(5,0,5,0),spacing=2)
        self.help_grid = GridLayout(cols=2, size_hint=(0.5, 0.5), padding=5,spacing=2)
        self.calc_grid = GridLayout(cols=2, size_hint=(0.5, 0.5), padding=5,spacing=2)
        self.det_grid = GridLayout(cols=2, size_hint=(0.5, 0.5), padding=5,spacing=2)

        self.add_button('уменьшить i', self.change_size_down_row,self.change_size_row)
        self.add_button('увеличить i', self.change_size_up_row,self.change_size_col)
        self.add_button('уменьшить j', self.change_size_down_col,self.change_size_row)
        self.add_button('увеличить j', self.change_size_up_col,self.change_size_col)
        self.buttons.add_widget(self.change_size_col)
        self.buttons.add_widget(self.change_size_row)

        self.add_button('Обратная матрица',self.oposit, self.calc_grid,(230/255,97/255,0,1))
        self.add_button('Ранг матрицы', self.rank, self.calc_grid,(230/255,97/255,0,1))
        self.add_button('Произведение матриц',self.multy, self.calc_grid,(230/255,97/255,0,1))
        # self.add_button('Единичная матрица',self.e_matrix, self.calc_grid,(230/255,97/255,0,1))
        self.add_button('Сумма матриц',self.sum, self.calc_grid,(230/255,97/255,0,1))
        self.add_button('Поменять местами матрицы',self.multy, self.help_grid,)
        self.add_button('Сделать квадратную матрицу', self.square, self.help_grid,)
        self.add_button('Автоматически заполнить',self.auto,self.help_grid,)
        self.add_button('Очистить',self.clear,self.help_grid,)

        self.buttons.add_widget(self.help_grid)
        self.det_grid.add_widget(
            Button(
            text = 'Определитель',
            on_press = self.det,background_normal = '',
            background_color=(230/255,97/255,0,1),
            size_hint=(0.1, 0.5),
            font_size=32
                )
          )
        self.buttons.add_widget(self.det_grid)
        self.buttons.add_widget(self.calc_grid)
        self.add_widget(self.buttons)

    # Основной метод, который запускается один раз, после запуска программы
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_mtx_row = 3
        self.size_mtx_col = 3

        self.cols = 1
        self.matrix_input = MyInputMatrix(self.size_mtx_row,self.size_mtx_col)  # Default to 2x2 matrix
        self.add_widget(self.matrix_input)
        self.count = 0

        self.create_buttons()

    # Метод, который выводит сообщение о матрице
    def show_the_result(self, result, title, font_size, width=200):
        popup = Popup(title=title, content=Label(text=f'{result}', font_size=font_size),
                      size_hint=(None, None), size=(width, 200))
        popup.open()

    # Преобразование матрицы в квадрат
    def square(self, event):
        if self.size_mtx_col > self.size_mtx_row:
            self.size_mtx_row = self.size_mtx_col
            self.change_size()

        elif self.size_mtx_col < self.size_mtx_row:
            self.size_mtx_col = self.size_mtx_row
            self.change_size()

    # Автоматическое заполнение матрицы
    def auto(self, event):
        count = 0
        for j in range(self.size_mtx_col):
            for i in range(self.size_mtx_row):

                self.matrix_input.input[count].text = str(random.randint(-10, 10))
                count += 1

    # Изменение кол-во колонок матрицы в большую сторону
    def change_size_up_col(self, event):
        if self.size_mtx_col<8:
            self.size_mtx_col = self.size_mtx_col + 1
            self.change_size()

    # Изменение кол-во колонок матрицы в меньшую сторону
    def change_size_down_col(self, event):
        if self.size_mtx_col > 1:
            self.size_mtx_col = self.size_mtx_col - 1
            self.change_size()

    # Изменение кол-во строк матрицы в большую сторону
    def change_size_up_row(self, event):
        if self.size_mtx_row<8:
            self.size_mtx_row = self.size_mtx_row + 1
            self.change_size()

    # Изменение кол-во строк матрицы в меньшую сторону
    def change_size_down_row(self, event):
        if self.size_mtx_row > 1:
            self.size_mtx_row = self.size_mtx_row - 1
            self.change_size()

    # Изменение матрицы
    def change_size(self):
        try:
            self.remove_widget(self.matrix_input)
            self.remove_widget(self.buttons)
            self.matrix_input = MyInputMatrix(self.size_mtx_col,self.size_mtx_row)

            self.add_widget(self.matrix_input)
            self.add_widget(self.buttons)

        except:
            pass

    def set_matrix(self,matrix):
        count = 0
        for j in range(self.size_mtx_col):
            for i in range(self.size_mtx_row):
                self.matrix_input.result[count].text = str(int(matrix[i][j]))
                count += 1

    #Преобразование матрицы введенной с экрана, в массив из чисел
    def fill_check(self,event):
        matrix1 = self.get_matrix()
        matrix2 = self.get_matrix_second()
        for row in matrix1:
            if '' in row:
                return False
        for row in matrix2:
            if '' in row:
                return False
        return True

    def get_matrix(self):
        matrix = []

        mtx_size = self.size_mtx_row * self.size_mtx_col

        for i in range(mtx_size):
            m = self.matrix_input.input[i].text
            matrix.append(m)
        m = []

        for i in range(mtx_size):
            g = self.matrix_input.result[i].text
            m.append(g)
        if '' in matrix and not ('' in m):
            for i in range(mtx_size):
                m = self.matrix_input.result[i].text
                self.matrix_input.input[i].text = self.matrix_input.result[i].text
                matrix.append(m)
                self.matrix_input.result[i].text = ''
        matrix = list(mtx.chunks(list(map(int, matrix)), self.size_mtx_col))
        return matrix

    # Получение элементов второй матрицы (при умножение и сложение)
    def get_matrix_second(self):
        matrix = []
        for i in range(self.size_mtx_col *self.size_mtx_row):
            m = self.matrix_input.result[i].text
            matrix.append(m)
        matrix = list(mtx.chunks(list(map(float, matrix)), self.size_mtx_col))
        return matrix

    # Запись в первую матрицу единичную матрицу (думаю удалить)
    def e_matrix(self,event):
        for i in range(self.size_mtx_col):
            self.matrix_input.input[i+self.size_mtx_col*i].text = '1'

        try:
            for i in range(len(self.matrix_input.input)):
                if self.matrix_input.input[i].text != '1':
                     self.matrix_input.input[i].text = '0'
            self.matrix_input.output.text = 'Единичная матрица:'
        except:
            pass

    # Вычисление определителя первой или второй матрицы

    def det_auto(self,event):
        try:
            if self.size_mtx_col != self.size_mtx_row:
                self.det_label.text='Матрица не квадратная!'
                return

            matrix = self.get_matrix()

            det = mtx.deter(matrix, self.size_mtx_col)
        except:
            det =  'Не найден!'
        self.det_label.text=f'Определитель (det) = {det}'


    def det(self, event):

        try:
            if self.size_mtx_col != self.size_mtx_row:
                oposit = 'Матрица должна быть квадратной!'
                self.show_the_result(oposit, 'Определитель', 25, 500)
                return
            matrix = self.get_matrix()

            det = mtx.deter(matrix, self.size_mtx_col)
        except:
            det = 'Не найден!'
        self.show_the_result(det, 'Определитель:', 50, 500)

    # Запись обратной матрицы
    def oposit(self, event):
        try:
            matrix = self.get_matrix()
            if self.size_mtx_col != self.size_mtx_row:
                oposit = 'Матрица должна быть квадратной!'
                self.show_the_result(oposit, 'Обратная матрица', 25, 500)
                return

            det = mtx.deter(matrix, self.size_mtx_col)
            oposit_matrix = mtx.opositMatrix(matrix, self.size_mtx_col)
            self.set_matrix(oposit_matrix)

            oposit = f'Умноженная на {det}'
            self.matrix_input.output.text = 'Обратная матрица:'
        except:
            oposit = 'Матрица не имеет обратной!'
        self.show_the_result(oposit, 'Обратная матрица', 30, 500)

    def rank(self, event):
        try:
            matrix = self.get_matrix()
            rank = mtx.rank(matrix)
        except:
            rank = 'Не найден!'
        self.show_the_result(rank, 'Ранг матрицы:', 50, 500)

    def multy(self, event):
        try:
            count = 0
            self.cols = 1
            matrix = self.get_matrix()
            matrix1 = self.get_matrix_second()

            matrix = (mtx.multiplyMatrices(matrix, matrix1, self.size_mtx_row))

            self.set_matrix(matrix)

            self.matrix_input.output.text = 'Произведение матриц A и В:'
        except:
            pass

    def sum(self, event):
        count = 0
        try:
            matrix = self.get_matrix()
            matrix1 = self.get_matrix_second()

            matrix = (mtx.Matrix_sum(matrix, matrix1, self.size_mtx_row))

            self.set_matrix(mtx.transpose(matrix, self.size_mtx_row))
            self.matrix_input.output.text = 'Сумма матриц:'
        except:
            pass

    def clear(self, event):
        size_row = self.size_mtx_row
        size_col = self.size_mtx_col
        count = 0
        for j in range(self.size_mtx_row):
            for i in range(self.size_mtx_col):
                self.matrix_input.result[count].text = ''
                count += 1
        count = 0
        for j in range(self.size_mtx_row):
            for i in range(self.size_mtx_col):
                self.matrix_input.input[count].text = ''
                count += 1
        self.size_mtx_col = self.size_mtx_row = 3
        self.matrix_input.output.text = f'Матрица B размером {size_row}х{size_col}:'
        self.matrix_input.ishod.text = f'Матрица А размером {size_row}х{size_col}:'
        self.change_size()

class MyMatrixCalc(App):
    def build(self):
        Window.size = (540, 1200)
        R = 36
        G = 36
        B = 36

        Window.clearcolor = (R/255,G/255,B/255,1)
        # background_color = [.92, .35, .36, 1]

        return MyGridLayout()

if __name__ == '__main__':
    MyMatrixCalc().run()
