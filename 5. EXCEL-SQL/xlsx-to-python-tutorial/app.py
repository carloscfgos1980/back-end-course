import openpyxl
from openpyxl import Workbook, load_workbook


book = load_workbook('menu.xlsx')
sheet = book.active

print(sheet['A2'].value)  # access to a unique value

sheet['A2'].value = 'spaghetti'  # change the value

print(sheet['A2'].value)

book.save('menu.xlsx')  # save the changes

sheet['A2'].value = 'tortellini'
book.save('seasonal_menu.xlsx')  # save in a different .xlsx file
