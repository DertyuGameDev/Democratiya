import sys
import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QMainWindow, QMessageBox
from editform import Ui_AddEditCoffeeForm
from main1 import Ui_MainWindow


class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_data=None):
        super().__init__(parent)
        self.setupUi(self)
        self.coffeedata = coffee_data
        self.is_edit = bool(coffee_data)

        if self.is_edit:
            self.populate_fields()

        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.reject)

    def populate_fields(self):
        self.nameLineEdit.setText(self.coffee_data.get('name', ''))
        self.roastDegreeComboBox.setCurrentText(self.coffee_data.get('roast_level', 'Светлая'))
        self.groundBeansComboBox.setCurrentText(self.coffee_data.get('ground_or_whole', 'Молотый'))
        self.tasteDescriptionTextEdit.setPlainText(self.coffee_data.get('flavor_description', ''))
        self.priceLineEdit.setText(str(self.coffee_data.get('price', '')))
        self.packageSizeLineEdit.setText(self.coffee_data.get('package_volume', ''))

    def save(self):
        name = self.nameLineEdit.text().strip()
        roast_level = self.roastDegreeComboBox.currentText().strip()
        ground_or_whole = self.groundBeansComboBox.currentText().strip()
        flavor_description = self.tasteDescriptionTextEdit.toPlainText().strip()
        price_text = self.priceLineEdit.text().strip()
        package_volume = self.packageSizeLineEdit.text().strip()

        if not name or not roast_level or not ground_or_whole or not flavor_description or not price_text or not package_volume:
            QMessageBox.warning(self, "Ошибка ввода", "Заполните все обязательные поля")
            return

        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Цена должна быть числом")
            return

        self.result_data = {
            'name': name,
            'roast_level': roast_level,
            'ground_or_whole': ground_or_whole,
            'flavor_description': flavor_description,
            'price': price,
            'package_volume': package_volume,
        }

        if self.is_edit:
            self.result_data['id'] = self.coffee_data['id']

        self.accept()


class CoffeeApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadButton.clicked.connect(self.load_coffee_data)
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.load_coffee_data()

    def load_coffee_data(self):
        connection = sqlite3.connect('data/coffee.sqlite')
        cursor = connection.cursor()

        try:
            cursor.execute("select * FROM coffee")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось получить данные: {e}")
            return
        finally:
            connection.close()

        self.coffeeTable.setRowCount(0)
        self.coffeeTable.setColumnCount(len(column_names))
        self.coffeeTable.setHorizontalHeaderLabels(column_names)

        for row in rows:
            row_position = self.coffeeTable.rowCount()
            self.coffeeTable.insertRow(row_position)
            for column, data in enumerate(row):
                self.coffeeTable.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))

        header = self.coffeeTable.horizontalHeader()
        header.setStretchLastSection(True)

        self.coffeeTable.resizeColumnsToContents()

    def add_coffee(self):
        form = AddEditCoffeeForm(self)
        if form.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = form.result_data
            connection = sqlite3.connect('data/coffee.sqlite')
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    insert into coffee (name, roast_level, ground_or_whole, flavor_description, price, package_volume)
                    values (?, ?, ?, ?, ?, ?)
                """, (
                    data['name'],
                    data['roast_level'],
                    data['ground_or_whole'],
                    data['flavor_description'],
                    data['price'],
                    data['package_volume']
                ))
                connection.commit()
                QMessageBox.information(self, "Успех", "Кофе добавлено успешно")
                self.load_coffee_data()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить кофе: {e}")
            finally:
                connection.close()

    def edit_coffee(self):
        selected_items = self.coffeeTable.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка выбора", "Выберите запись для редактирования.")
            return

        selected_row = selected_items[0].row()
        coffee_id = self.coffeeTable.item(selected_row, 0).text()
        name = self.coffeeTable.item(selected_row, 1).text()
        roast_level = self.coffeeTable.item(selected_row, 2).text()
        ground_or_whole = self.coffeeTable.item(selected_row, 3).text()
        flavor_description = self.coffeeTable.item(selected_row, 4).text()
        price = self.coffeeTable.item(selected_row, 5).text()
        package_volume = self.coffeeTable.item(selected_row, 6).text()

        coffee_data = {
            'id': coffee_id,
            'name': name,
            'roast_level': roast_level,
            'ground_or_whole': ground_or_whole,
            'flavor_description': flavor_description,
            'price': price,
            'package_volume': package_volume,
        }

        form = AddEditCoffeeForm(self, coffee_data=coffee_data)
        if form.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = form.result_data
            connection = sqlite3.connect('data/coffee.sqlite')
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    UPDATE coffee
                    SET name = ?, roast_level = ?, ground_or_whole = ?, flavor_description = ?, price = ?, package_volume = ?
                    WHERE id = ?
                """, (
                    data['name'],
                    data['roast_level'],
                    data['ground_or_whole'],
                    data['flavor_description'],
                    data['price'],
                    data['package_volume'],
                    data['id']
                ))
                connection.commit()
                QMessageBox.information(self, "Успех", "Кофе обновлен успешно.")
                self.load_coffee_data()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось обновить кофе: {e}")
            finally:
                connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
