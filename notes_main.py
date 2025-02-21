from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QLineEdit, QInputDialog
import json

app = QApplication([])
main_win = QWidget()
main_win.resize(900,600)
main_win.setWindowTitle("Розумні замітки")

notes = {
    "Назва замітки": {
        "text":"Дуже важливий текст замітки",
        "tags":["чернетка","думки"]
    }
}

with open("notes_data.json", "w", encoding="UTF-8") as file:
    json.dump(notes, file)


main_text = QTextEdit()

name_label = QLabel("Список заміток")
names_list = QListWidget()
generate_btn = QPushButton("Створити замітку")
delete_btn = QPushButton("Видалити замітку")
save_btn = QPushButton("Зберегти замітку")

name2_label = QLabel("Список тегів")
tags_list = QListWidget()
input_edit = QLineEdit("")
input_edit.setPlaceholderText("Введіть тег...")
add_btn = QPushButton("Додати до замітки")
remove_btn = QPushButton("Відкріпити від замітки")
search_btn = QPushButton("Шукати замітки по тегу")

v_layout1 = QVBoxLayout()
v_layout2 = QVBoxLayout()

h_layout1 = QHBoxLayout()
h_layout2 = QHBoxLayout()
h_layout3 = QHBoxLayout()

v_layout1.addWidget(main_text)

h_layout1.addWidget(generate_btn)
h_layout1.addWidget(delete_btn)

h_layout2.addWidget(add_btn)
h_layout2.addWidget(remove_btn)

v_layout2.addWidget(name_label)
v_layout2.addWidget(names_list)
v_layout2.addLayout(h_layout1)
v_layout2.addWidget(save_btn)
v_layout2.addWidget(name2_label)
v_layout2.addWidget(tags_list)
v_layout2.addWidget(input_edit)
v_layout2.addLayout(h_layout2)
v_layout2.addWidget(search_btn)

h_layout3.addLayout(v_layout1)
h_layout3.addLayout(v_layout2)

main_win.setLayout(h_layout3)




def show_note():
    name = names_list.selectedItems()[0].text()
    main_text.setText(notes[name]["text"])
    tags_list.clear()
    tags_list.addItems(notes[name]["tags"])

def add_note():
    note_name, result = QInputDialog.getText(main_win, "Додати замітку","Назва замітки:")
    if note_name and result != "":
        notes[note_name] = {"text" : "", "tags" : []}
        names_list.addItem(note_name)
        tags_list.addItems(notes[note_name]["tags"])
        print(notes)

def del_note():
    if names_list.selectedItems():
        key = names_list.selectedItems()[0].text()
        del notes[key]
        names_list.clear()
        tags_list.clear()
        main_text.clear()
        names_list.addItems(notes)
        
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print("Замітка для вилучення не вибрана")

def save_note():
    if names_list.selectedItems():
        key = names_list.selectedItems()[0].text()
        text = main_text.toPlainText()
        notes[key]["text"] = text

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)

def add_tag():
    if names_list.selectedItems():
        key = names_list.selectedItems()[0].text()
        tag = input_edit.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            tags_list.addItem(tag)
            input_edit.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
        print(notes)
    else:
        print("Замітка для додавання тега не обрана!")

        
def del_tag():
    if tags_list.selectedItems():
        key = names_list.selectedItems()[0].text()
        tag = tags_list.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        tags_list.clear()
        tags_list.addItems(notes[key]["tags"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True)
    else:
        print("Тег для вилучення не вибраний!")

def search_tag():
    print(search_btn.text())
    tag = input_edit.text()
    if search_btn.text() == "Шукати замітки по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["tags"]:
                notes_filtered[note] = notes[note]
        search_btn.setText("Скинути пошук")
        tags_list.clear()
        names_list.clear()
        names_list.addItems(notes_filtered)
        print(search_btn.text())
    elif search_btn.text() == "Скинути пошук":
        names_list.clear()
        tags_list.clear()
        input_edit.clear()
        names_list.addItems(notes)
        search_btn.setText("Шукати замітки по тегу")
        print(search_btn.text())

    else:
        pass

generate_btn.clicked.connect(add_note)
delete_btn.clicked.connect(del_note)
save_btn.clicked.connect(save_note)
add_btn.clicked.connect(add_tag)
remove_btn.clicked.connect(del_tag)
search_btn.clicked.connect(search_tag)
names_list.clicked.connect(show_note)











main_win.show()

with open("notes_data.json", "r") as file:
    notes = json.load(file)
    
names_list.addItems(notes)

app.exec_()