import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidget, QTableWidgetItem, \
    QVBoxLayout
from PyQt5 import uic


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Эсспрессо')
        self.setGeometry(300, 100, 800, 800)
        self.layout = QVBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.layout.addWidget(self.tableWidget)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
