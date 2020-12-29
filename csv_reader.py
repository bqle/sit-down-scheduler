import csv
import xlrd
import pandas as pd

def csv_from_excel():
    """ Name of spreadsheet """
    wb = xlrd.open_workbook('Sitdown-Dinner-Data.xlsm')

    sd = wb.sheet_by_name('Student Data')
    student_data_csv = open('Student Data.csv', 'w')
    wr = csv.writer(student_data_csv, quoting=csv.QUOTE_ALL)
    for rownum in range(sd.nrows):
        wr.writerow(sd.row_values(rownum))

    td = wb.sheet_by_name('Table Data')
    table_data_csv = open('Table Data.csv', 'w')
    wr_1 = csv.writer(table_data_csv, quoting=csv.QUOTE_ALL)
    for rownum in range (td.nrows):
        wr_1.writerow(td.row_values(rownum))

    student_data_csv.close()
    table_data_csv.close()

    student_data = list (csv.reader(open("Student Data.csv")))
    table_data = list (csv.reader(open("Table Data.csv")))
    return student_data, table_data

def array_to_dataframe():
    data_arrays = csv_from_excel()
    student_data = data_arrays[0]
    table_data = data_arrays[1]
    pd_sd = pd.DataFrame(student_data)
    pd_td = pd.DataFrame(table_data)

    """ -3 is necessary because last 3 rows are useless """
    pd_td = pd_td.iloc[0:(pd_td.shape[0]-3)]

    # print(pd_td)
    return pd_sd, pd_td

