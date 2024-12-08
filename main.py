import sys
import sqlite3
from PyQt6 import QtWidgets, uic


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.loadButton.clicked.connect(self.load_coffee_data)

    def load_coffee_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.coffeeTable.setRowCount(0)

        for row in rows:
            row_position = self.coffeeTable.rowCount()
            self.coffeeTable.insertRow(row_position)
            for column, data in enumerate(row):
                self.coffeeTable.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))

        connection.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
