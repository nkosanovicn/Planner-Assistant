import streamlit as st
from db_update import *

def sidebar():
    create_table()
    taskstodo = view_todo()
    tasksdone = view_done()

    container1 = st.sidebar.container(border=None)
    ondo = st.sidebar.toggle("Tasks")
    container2 = st.sidebar.container(border=None)
    ondone= st.sidebar.toggle("Completed")
    container3 = st.sidebar.container(border=None)

    if ondo:
        for task in taskstodo:
            if container2.checkbox(f"{task[1]}", key= f"key1_{task[0]}"):
                todo_to_done(task[0], task[1])
                st.rerun()

    if ondone:
        for task in tasksdone:
            if container3.checkbox(f"{task[1]}", key = f"key2_{task[0]}"):
                done_to_todo(task[0], task[1])
                st.rerun()
            elif container3.button("Remove",type="primary",width = "stretch", key= f"button1_{task[0]}"):
                delete(task[0], task[1])
                st.rerun()

    name = container1.text_input("Enter a task: ")
    if container1.button("Add task"):
        if name.strip():
            add_data(name.strip())
            st.rerun()
            st.success("You added a task.")