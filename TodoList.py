import PySimpleGUI as sg

sg.theme("Material2")

todolist = []
importance = []
deadline = []

with open("Data.txt"  ,"r") as p:
    array = p.readlines()
    size = len(array) + 1


with open("Data.txt", "r") as p:
    for i in range(size - 1):
        val = p.readline()
        if i !=0:
            val = val.split("+")
            todolist.append(val[0])
            importance.append(val[1])
            deadline.append(val[2])



res = ["         " + task  for task in todolist]
result = [i + j for i, j in zip(deadline , res)]

layout = [
    [sg.Image("image.png" , size = (600,100))],
    [sg.Text("To Do: " , font = ("Simplified Arabic Fixed",15), pad = (20,20)),
     sg.InputText("" , size = (35 , 1), font = ("Simplified Arabic" , 14), key = 'task' , background_color= "white" , text_color= "black" ),
     sg.Combo(['Very High' , 'High' , 'Normal' , 'Low'] ,font = ("Simplified Arabic Fixed" , 9) , background_color= "white", text_color= "black" , key = 'priority') ],
    [sg.CalendarButton("DeadLine" , font = ("Simplified Arabic Fixed" , 10) , pad = (255 , 10) )],
    [sg.Button("Add", font = ("Simplified Arabic Fixed", 15) , key = 'add_save' , pad = (200 , 20) , size = (100,1) )],
    [sg.Listbox(result, size = (40,9) , font = ("Cambria" , 14) , key = 'tasklist' , background_color = "white" , pad = (100 , 20) , text_color = "black")],
    [sg.Button("Edit", font = ("Simplified Arabic Fixed", 14) , pad = (90 , 10) , size = (10,1)), sg.Button("Delete", font = ("Simplified Arabic Fixed", 14) , pad = (90 , 10),  size = (10,1))]

]

def add_tasks(values):
    global todolist,importance,deadline
    window.FindElement('add_save').Update("Add")
    window.FindElement('priority').Update(value="Normal")
    task = values['task']
    order = values['priority']
    date = values['DeadLine']
    todolist.append(task)
    importance.append(order)
    deadline.append(date)

    todolist , importance , deadline = check_order(todolist,importance,deadline)

    deadline = [date.split(' ', 1)[0] for date in deadline]

    res = ["         " + task for task in todolist]
    result = [i + j for i, j in zip(deadline, res)]

    window.FindElement('tasklist').Update(values = result)
    window.FindElement('task').Update(value = "")

    with open('Data.txt', 'w') as f:
        size = len(todolist) + 1

        for i in range(size):
            if i == 0:
                f.write("None" + "+" + "None" + "0000-00-00" + "+" + "\n")
            else:
                f.write(todolist[i - 1])
                f.write("+")
                f.write(importance[i - 1])
                f.write("+")
                f.write(deadline[i - 1])
                f.write("+")
                f.write("\n")

def check_order(todo, impor , dead):
    dictionary = {'Very High':1 , 'High':2 , 'Normal':3 , 'Low':4}
    list1 = []

    for i in impor:
        list1.append(dictionary[i])

    zipped_lists = zip(list1, todo, dead)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    impor, todo , dead = [list(tuple) for tuple in tuples]

    for i in dictionary:
        for j in range(len(impor)):
            if dictionary[i] == impor[j]:
                impor[j] = i


    return todo, impor , dead

def delete_tasks(values):
    delete = values['tasklist'][0]
    delete = delete.split('         ',1)[1]
    index = todolist.index(delete)
    importance.pop(index)
    deadline.pop(index)
    todolist.remove(delete)
    res = ["         " + task for task in todolist]
    result = [i + j for i, j in zip(deadline, res)]
    window.FindElement('tasklist').Update(values = result)

    with open('Data.txt', 'w') as f:
        size = len(todolist) + 1

        for i in range(size):
            if i == 0:
                f.write("None" + "+" + "None" + "0000-00-00"+ "+" + "\n")
            else:
                f.write(todolist[i-1])
                f.write("+")
                f.write(importance[i-1])
                f.write("+")
                f.write(deadline[i-1])
                f.write("+")
                f.write("\n")

def edit_tasks(values):
    edit = values['tasklist'][0]
    edit = edit.split('         ', 1)[1]
    index = todolist.index(edit)
    importance.pop(index)
    deadline.pop(index)
    window.FindElement('task').Update(value = edit)
    window.FindElement('add_save').Update("Save")
    todolist.remove(edit)


window = sg.Window("To Do List", layout , size = (600 , 700))
while True:
    events,values = window.Read()

    if events == 'add_save':
        add_tasks(values)

    elif events == 'Delete':
        delete_tasks(values)

    elif events == 'Edit':
        edit_tasks(values)

    else:
        break

window.Close()