from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication,
                             QWidget, QPushButton, QTextEdit,
                             QLabel, QLineEdit, QListWidget,
                             QVBoxLayout, QHBoxLayout, QInputDialog)
import json
app = QApplication([])



with open('f.json', 'r') as file:
    notes=json.load(file)

#параметри вікна
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)

# Віджети вікна програми
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

btn_note_create = QPushButton('Створити замітку')
btn_note_save = QPushButton('Зберегти')
btn_note_delete = QPushButton("Видалити")

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть назву тегу')

field_text = QTextEdit()

btn_tag_add = QPushButton('Додати тег до замітки')
btn_tag_delete = QPushButton('Видалити тег замітки')
btn_tag_search = QPushButton("Шукати замітки по тегу")

list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

# розташування віджетів

layout_notes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(field_text)
#додаємо поле із списком заміток та кнопками
col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)
row1 = QHBoxLayout()
row1.addWidget(btn_note_create)
row1.addWidget(btn_note_delete)
row2 = QHBoxLayout()
row2.addWidget(btn_note_save)
col2.addLayout(row1)
col2.addLayout(row2)
#додаємо поле із списком тегів заміток та кнопками
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)
row3 = QHBoxLayout()
row3.addWidget(btn_tag_add)
row3.addWidget(btn_tag_delete)
col2.addLayout(row3)
row4 = QHBoxLayout()
row4.addWidget(btn_tag_search)
col2.addLayout(row4)

layout_notes.addLayout(col1)
layout_notes.addLayout(col2)
notes_win.setLayout(layout_notes)
def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])
def add_note():
    note_name, ok = QInputDialog.getText(notes_win,"Додати замітку","Назва замітки")
    if ok and note_name!='':
        notes[note_name]={'текст': '','теги':[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)
def save_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        notes[key]['текст']=field_text.toPlainText()
        with open ('f.json','w') as file:
            json.dump(notes,file,sort_keys=True)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_tags.clear()
        list_notes.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('f.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print("Замітка для видалення не вибрана!")


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('f.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print('Замітка для додавання теги не обрана')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag =list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        with open('f.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print('Такий тег не знайдено')


def search_tag():
    tag = field_tag.text()
    if btn_tag_search.text()=="Шукати замітки по тегу":
        notes_filtered={}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        btn_tag_search.setText('Скинути пошук')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif btn_tag_search.text()=='Скинути пошук':
        list_tags.clear()
        list_notes.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        btn_tag_search.setText("Шукати замітки по тегу")
    else:
        pass

    print(notes_filtered)


btn_note_create.clicked.connect(add_note)
btn_note_save.clicked.connect(save_note)
btn_note_delete.clicked.connect(del_note)
btn_tag_add.clicked.connect(add_tag)
btn_tag_delete.clicked.connect(del_tag)
btn_tag_search.clicked.connect(search_tag)

list_notes.itemClicked.connect(show_note)
list_notes.addItems(notes)
notes_win.show()
app.exec_()