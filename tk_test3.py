import tkinter as tk
from tkinter import ttk

def populate_treeview(treeview, parent, dictionary):
    """
    Populate the given treeview recursively with the given dictionary.
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            # This node has children, so create a new node and populate it
            node = treeview.insert(parent, "end", text=key, open=False)
            populate_treeview(treeview, node, value)
        else:
            # This node doesn't have children, so just add it to the parent
            treeview.insert(parent, "end", text=key, values=(value))

def search_treeview(treeview, query, parent=""):
    """
    Search the given treeview for nodes that match the given query.
    """
    if query == "":
        # If the query is empty, return all nodes
        return treeview.get_children(parent)
    matching_nodes = []
    for node in treeview.get_children(parent):
        if query.lower() in treeview.item(node)["text"].lower():
            # If the query is found in the node text, add the node to the results
            matching_nodes.append(node)
        matching_nodes.extend(search_treeview(treeview, query, node))
    return matching_nodes

def on_search(query):
    """
    Handle a search event.
    """
    # Clear the current selection and the treeview
    treeview.selection_remove(*treeview.get_children())
    treeview.delete(*treeview.get_children())

    # Populate the treeview with the matching nodes
    matching_nodes = search_treeview(treeview, query)
    for node in matching_nodes:
        treeview.insert("", "end", node, text=treeview.item(node)["text"], values=treeview.item(node)["values"])

# Create a sample dictionary to populate the treeview
my_dict = {
    'Key 1': {
        'Subkey 1.1': 'Value 1.1',
        'Subkey 1.2': 'Value 1.2'
    },
    'Key 2': {
        'Subkey 2.1': {
            'Subsubkey 2.1.1': 'Value 2.1.1',
            'Subsubkey 2.1.2': 'Value 2.1.2'
        },
        'Subkey 2.2': 'Value 2.2'
    }
}

# Create the GUI
root = tk.Tk()
root.geometry('400x400')

# Create the search bar
search_frame = tk.Frame(root)
search_frame.pack(fill='x')

search_var = tk.StringVar()

def on_search_var_changed(*args):
    """
    Handle changes to the search bar text variable.
    """
    query = search_var.get()
    on_search(query)

search_var.trace_add("write", on_search_var_changed)

search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.pack(side='left', fill='x', expand=True)

# Create the treeview
treeview = ttk.Treeview(root)
treeview.pack(fill='both', expand=True)

# Populate the treeview with the sample dictionary
populate_treeview(treeview, '', my_dict)

root.mainloop()
