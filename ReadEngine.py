# -*_ coding: utf-8 -*-
import string


row_delimiter = ' '
column_delimiter = '\n'

#내부 구분자

def Read_To_String(filedir: str):
    try:
        target = open(filedir, 'r', encoding = 'utf-8')
    except:
        target = open(filedir, 'w', encoding = 'utf-8')
        target.close()
        target = open(filedir, 'r', encoding = 'utf-8')
    else:
        target_string = target.read()
        target.close()
        return target_string

def Read_To_Diction(filedir: str):
    temp_list1 = []
    temp_list2 = []
    target_diction = {}

    target_string = Read_To_String(filedir)
    temp_list1 = target_string.split(column_delimiter)
    
    for i in range(0, len(temp_list1)-1, 1):
        temp_list2 = temp_list1[i].split(row_delimiter)
        target_diction[float(temp_list2[0])] = float(temp_list2[1])
    
    return target_diction

def Add_To_Text(filedir: str, str1: str, str2: str):
    target = open(filedir, 'a', encoding = 'utf-8')
    target.write('{0}{1}{2}{3}'.format(str1, row_delimiter, str2, column_delimiter))
    target.close()

def Write_List_To_Text(filedir: str, list1: list, list2: list):
    length = min(len(list1), len(list2))

    target = open(filedir, 'w', encoding = 'utf-8')
    target.close()

    target = open(filedir, 'a', encoding = 'utf-8')

    for i in range(length):
        target.write('{0}{1}{2}{3}'.format(list1[i], row_delimiter, list2[i], column_delimiter))

    target.close()
