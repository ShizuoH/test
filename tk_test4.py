import tkinter as tk
from tkinter import ttk


def populate_treeview(treeview, node_dict, parent=""):
    """
    Recursively populate the given treeview with data from the given node dictionary.
    """
    for key in node_dict:
        if isinstance(node_dict[key], dict):
            # If the value for this key is a dictionary, create a new node and populate it
            node_id = treeview.insert(parent, "end", text=key)
            populate_treeview(treeview, node_dict[key], node_id)
        else:
            # If the value for this key is not a dictionary, create a new leaf node
            treeview.insert(parent, "end", text=key, values=(node_dict[key]))


def show_treeview(treeview, nodes=None):
    """
    Show the given nodes in the given treeview. If nodes is None, show all nodes.
    """
    if nodes is None:
        # If nodes is None, show all nodes
        nodes = treeview.get_children()
    for node in nodes:
        treeview.item(node, open=True)
        show_treeview(treeview, treeview.get_children(node))


def search_treeview(treeview, query, parent=""):
    """
    Search the given treeview for nodes that match the given query.
    """
    query = query.lower()  # Convert the query to lowercase
    if query == "":
        # If the query is empty, return all nodes
        return treeview.get_children(parent)
    matching_nodes = []
    for node in treeview.get_children(parent):
        label = treeview.item(node)["text"].lower()  # Convert the node label to lowercase
        if query in label:
            # If the query is found in the node text, add the node to the results
            matching_nodes.append(node)
        matching_nodes.extend(search_treeview(treeview, query, node))
    return matching_nodes


def on_search_box_changed(event):
    """
    Called when the search box text is changed.
    """
    query = search_box.get()
    if query == "":
        # If the query is empty, show all nodes
        show_treeview(treeview)
    else:
        # Otherwise, search the treeview for matching nodes
        matching_nodes = search_treeview(treeview, query)
        show_treeview(treeview, matching_nodes)


# Define the data to populate the treeview
data = {
    "Key 1": {
        "Subkey 1": "Value 1",
        "Subkey 2": "Value 2",
        "Subkey 3": {
            "Subsubkey 1": "Value 3",
            "Subsubkey 2": "Value 4"
        }
    },
    "Key 2": {
        "Subkey 4": {
            "Subsubkey 3": "Value 5"
        },
        "Subkey 5": "Value 6"
    }
}

# Create the main window and treeview
root = tk.Tk()
treeview = ttk.Treeview(root, columns=("value"))
treeview.pack(fill="both", expand=True)

# Populate the treeview with the data
populate_treeview(treeview, data)

# Create a search box and bind it to the search function
search_box = tk.Entry(root)
search_box.pack(fill="x")
search_box.bind("<KeyRelease>", on_search_box_changed)

# Start the main loop
root.mainloop()
