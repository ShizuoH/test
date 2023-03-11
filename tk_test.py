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
root.geometry('400x300')

# Create the treeview
treeview = ttk.Treeview(root)
treeview.pack(fill='both', expand=True)

# Populate the treeview with the sample dictionary
populate_treeview(treeview, '', my_dict)

root.mainloop()
