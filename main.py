import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QVBoxLayout
from PyQt5 import uic


class AddCoffeeForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.lineEdit_5.setEnabled(False)
        self.error.hide()
        self.not_error.hide()
        self.pushButton.clicked.connect(self.add)

    def add(self):
        try:
            title = self.lineEdit.text()
            roast_degree = self.lineEdit_2.text()
            _type = self.comboBox.currentText()
            price = self.lineEdit_4.text() + '₽'
            volume = float(self.lineEdit_3.text())
            if roast_degree and _type and price and volume and title:
                con = sqlite3.connect('coffee.sqlite')
                cur = con.cursor()
                cur.execute(f"""INSERT INTO espresso(title, roast_degree, type, price, volume)
                                     VALUES('{title}',
                                      '{roast_degree}', '{_type}', '{price}', {volume})""")
                con.commit()
                self.parent().get_data()
                self.parent().tbl_init()
            else:
                raise Exception
        except Exception:
            self.error.show()
            return False
        self.not_error.show()
        self.setEnabled(False)


class EditCoffeeForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi('addEditCoffeeForm.ui', self)
        self.error.hide()
        self.not_error.hide()
        self.pushButton.clicked.connect(self.edit)

    def edit(self):
        try:
            _id = self.lineEdit_5.text()
            title = self.lineEdit.text()
            roast_degree = self.lineEdit_2.text()
            _type = self.comboBox.currentText()
            price = self.lineEdit_4.text() + '₽'
            volume = float(self.lineEdit_3.text())
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            params = {
                'title': title,
                'roast_degree': roast_degree,
                'type': _type,
                'price': price,
                'volume': volume
            }
            for key in params:
                if params[key] == '':
                    continue
                cur.execute(f'''
                                    UPDATE espresso
                                    SET {key} = "{params[key]}"
                                    WHERE id = {_id}''')
            con.commit()
            self.parent().get_data()
            self.parent().tbl_init()
        except Exception as exc:
            print(exc)
            self.error.show()
            return False
        self.not_error.show()
        self.setEnabled(False)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Капучино')
        self.setGeometry(300, 100, 800, 800)
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.pushButton_3.hide()
        self.get_data()
        self.tbl_init()

    def tbl_init(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'title', 'roast_degree', 'type', 'price', 'volume'])
        self.tableWidget.setRowCount(0)
        for row in range(len(self.data)):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.data[row][col])))

    def get_data(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        self.data = cur.execute("""
        SELECT * FROM espresso
        """).fetchall()

    def add(self):
        bb = AddCoffeeForm(self)
        bb.show()

    def edit(self):
        bb = EditCoffeeForm(self)
        bb.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    exit(app.exec_())
