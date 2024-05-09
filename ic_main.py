from tkinter import *
import customtkinter as ctk
from fetcher import Fetch
import string

try:
    fetch = Fetch()
    spacesAmount = ' '*2
    startup_inv: dict = fetch.get_allContent()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.wm_iconbitmap('crateicon.ico')
    root.title('Item Crate - Inventory Manager')
    root.geometry('700x850')

    # MAX CHARS (69)
    # root.title('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABccccccccccddddddE')

    # AUTO REFRESH WHEN SWITCHING TO Overview TAB
    def refreshView():
        inv: dict = fetch.get_allContent()
        if sort_mode == 0:
            update_view(inv.items())
        else:
            update_view(sorted(inv.items()))

    def get_values_by_itemname(d, itemname):
        values = None
        for key, value in d.items():
            if key == itemname:
                values = value
                break
            elif isinstance(value, dict):
                values = get_values_by_itemname(value, itemname)
                if values is not None:
                    break
        return values
    def save_values_to_dict(d, itemname):
        values = get_values_by_itemname(d, itemname)
        if values is not None:
            result_dict = {itemname: values}
            return result_dict
        else:
            return {}

    # Create Tabview
    def refreshOnSelectedTab():
        selected_tab = tabview.get()
        if selected_tab == f'{spacesAmount}Overview{spacesAmount}':
            root.title('Item Crate - Inventory Manager')
            oldAmount = int(topLabel.cget('text').replace('Total items: ',''))
            if oldAmount != fetch.get_keysAmount():
                root.title(f'Item Crate - Inventory Manager / Auto Refreshed -> Old Keys: {oldAmount} / New Keys: {fetch.get_keysAmount()}')
                refreshView()
        elif selected_tab == f'{spacesAmount}Remove Item{spacesAmount}':
            root.title('Item Crate - Remove Item')
            r_error_label.configure(text="")
        elif selected_tab == f'{spacesAmount}Add Item{spacesAmount}':
            root.title('Item Crate - Add Item')
            error_label.configure(text="")
            preview_frame.configure(text="", fg_color=itemsAdd.cget('fg_color'))
        elif selected_tab == f'{spacesAmount}Edit Item{spacesAmount}':
            root.title('Item Crate - Edit Item')
            e_error_label.configure(text="")

    tabview = ctk.CTkTabview(root, width=650, height=790, corner_radius=0, anchor=NW, command=refreshOnSelectedTab)  
    tabview.pack(pady=10)
    custom_font = ctk.CTkFont("Verdana", 13)
    tabview._segmented_button.configure(font=custom_font)

    # Create Tabs
    itemsOverview_Main = tabview.add(f"{spacesAmount}Overview{spacesAmount}")
    itemsOverview = ctk.CTkScrollableFrame(itemsOverview_Main, height=660)

    itemsAdd = tabview.add(f"{spacesAmount}Add Item{spacesAmount}")
    itemsEdit = tabview.add(f"{spacesAmount}Edit Item{spacesAmount}")
    itemsRemove = tabview.add(f"{spacesAmount}Remove Item{spacesAmount}")

    # ITEMS OVERVIEW TAB
    # Create headline frame
    headlineFrame = ctk.CTkFrame(itemsOverview_Main, fg_color='transparent', corner_radius=0)
    headlineFrame.pack(fill=X, pady=10)

    def sortBy():
        global sort_mode
        inv: dict = fetch.get_allContent()
        sort_mode = (sort_mode + 1) % 2
        if sort_mode == 0:
            root.title('Changed sort_mode to 0 NORMAL')
            sortbyButton.configure(text="Sorting Mode: Normal")
            update_view(inv.items())
        else:
            root.title('Changed sort_mode to 1 ALPHA')
            sortbyButton.configure(text="Sorting Mode: Alphabetical")
            update_view(sorted(inv.items()))

    # SORT MODE 1: Start on Alphabetic | SORT MODE 0: Start on Normal
    sort_mode = 1

    sortbyButton = ctk.CTkButton(headlineFrame, text='Toggle Sorting', corner_radius=0, command=sortBy)
    sortbyButton.pack(anchor=SE, padx=15, ipadx=10, side=RIGHT)
    refreshviewButton = ctk.CTkButton(headlineFrame, text='Refresh View', corner_radius=0, command=refreshView)
    refreshviewButton.pack(anchor=SE, padx=0, ipadx=10, side=RIGHT)

    topLabel = ctk.CTkLabel(itemsOverview_Main, text=f'Total Items: {fetch.get_keysAmount()}', font=custom_font)
    topLabel.pack(pady=5, padx=15, anchor=NW)
    def update_view(sortmode=sorted(startup_inv.items())):
        inv: dict = fetch.get_allContent()
        keysamount: int = fetch.get_keysAmount()
        for widget in itemsOverview.winfo_children():
            widget.pack_forget()
        topLabel.configure(text=f"Total items: {keysamount}")
        itemsOverview.pack(fill=X)
        if isinstance(inv, dict):
            colorCounter = 1
            for itemname, value in sortmode:
                if itemname != 'ITEM_ORIGIN' and value != None:
                    if colorCounter % 2 == 0:
                        frameColor = 'gray7'
                        scrollbarColor = 'gray10'
                    else:
                        frameColor = 'gray4'
                        scrollbarColor = 'gray7'
                    itemFrame = ctk.CTkFrame(itemsOverview, fg_color=frameColor, width=500, height=50, corner_radius=0)
                    itemFrame.pack(fill=X, ipady=15)

                    topSpacer = ctk.CTkLabel(itemFrame, text='').pack(ipady=1)
                    nameLabel = ctk.CTkLabel(itemFrame, text=string.capwords(str(itemname)), font=("Arial", 18, 'bold'), text_color='#F4EF5F').pack(anchor=W, ipadx=15)
                    descriptionLabel = ctk.CTkLabel(itemFrame, text=value.get("description"), font=("Verdana", 15,'italic'), text_color='#4bb7fa', wraplength=550, justify=LEFT).pack(anchor=W, ipadx=15)
                    if value.get('sizes') != None:
                        sizesFrame = ctk.CTkFrame(itemFrame, fg_color=frameColor)
                        sizesFrame.pack(anchor=W)
                        availableSizesLabel = ctk.CTkLabel(sizesFrame, text=f"Available Sizes:", font=("Verdana", 15)).pack(anchor=W, ipadx=15, side=LEFT)
                        sizeslbracket = ctk.CTkLabel(sizesFrame, text=f"[", font=("Verdana", 15), text_color="#4ef5a1")
                        sizeslbracket.pack(anchor=W, side=LEFT)
                        for count, size in enumerate(list(value.get('sizes'))):
                            sizesLabel = ctk.CTkLabel(sizesFrame, text=f"{size}", font=("Verdana", 15), text_color='#F5634E').pack(anchor=W, side=LEFT)
                            if count+1 != len(list(value.get('sizes'))):
                                addComma = ctk.CTkLabel(sizesFrame, text=', ', font=("Verdana", 15)).pack(anchor=W, side=LEFT)
                        sizesrbracket = ctk.CTkLabel(sizesFrame, text=f"]", font=("Verdana", 15), text_color="#4ef5a1")
                        sizesrbracket.pack(anchor=W, side=LEFT)

                    if value.get('quantity') != None and value.get('colors') == None:
                        quantityFrame = ctk.CTkFrame(itemFrame, fg_color=frameColor)
                        quantityFrame.pack(anchor=W)
                        quantityMainLabel = ctk.CTkLabel(quantityFrame, text=f"Quantity:", font=("Verdana", 15)).pack(anchor=W, ipadx=15, side=LEFT)
                        quantityLabel = ctk.CTkLabel(quantityFrame, text=str(value.get('quantity')).replace('[','').replace(']','').replace("'",''), font=("Verdana", 15), text_color='#ff59af').pack(anchor=W, side=LEFT)
                    if value.get('colors') != None:
                        colorToplabel = ctk.CTkLabel(itemFrame, text='Color & Quantity:', font=("Verdana",15))
                        colorToplabel.pack(anchor=W, ipadx=15)
                        if value.get('quantity') == None:
                            colorqScroll = ctk.CTkScrollableFrame(itemFrame, fg_color=frameColor, height=20, width=650, orientation='horizontal', corner_radius=0, scrollbar_button_color=scrollbarColor)
                            colorqScroll.pack(anchor=W)
                            spacer = ctk.CTkLabel(colorqScroll, text='')
                            spacer.pack(anchor=W, side=LEFT, ipadx=16)
                            for colorq in value.get("colors"):
                                lbracket = ctk.CTkLabel(colorqScroll, text=f"[", font=("Verdana", 15), text_color="#5cff59")
                                lbracket.pack(anchor=W, side=LEFT)
                                colorColorLabel = ctk.CTkLabel(colorqScroll, text=f"{string.capwords(colorq.split('/')[0])}", font=("Verdana", 15, 'bold'))
                                colorColorLabel.pack(anchor=W, ipadx=0, side=LEFT)
                                detailSeperator = ctk.CTkLabel(colorqScroll, text=f" : ", font=("Verdana", 15), text_color="#ff8059")
                                detailSeperator.pack(anchor=W, side=LEFT)
                                colorQuantityLabel = ctk.CTkLabel(colorqScroll, text=f"{colorq.split('/')[1]}", font=("Verdana", 15), text_color='#ff59af')
                                colorQuantityLabel.pack(anchor=W, ipadx=0, side=LEFT)
                                rbracket = ctk.CTkLabel(colorqScroll, text=f"]  ", font=("Verdana", 15), text_color="#5cff59")
                                rbracket.pack(anchor=W, side=LEFT)
                        else:
                            detailsFrame = ctk.CTkFrame(itemFrame, fg_color=frameColor)
                            detailsFrame.pack(anchor=W)

                            spacer = ctk.CTkLabel(detailsFrame, text='')
                            spacer.pack(anchor=W, side=LEFT, ipadx=16)
                            lbracket = ctk.CTkLabel(detailsFrame, text=f"[", font=("Verdana", 15), text_color="#5cff59")
                            lbracket.pack(anchor=W, side=LEFT)
                            colorColorLabel = ctk.CTkLabel(detailsFrame, text=string.capwords(str(value.get("colors")).replace('[','').replace(']','').replace("'",'')), font=("Verdana", 15, 'bold'))
                            colorColorLabel.pack(anchor=W, ipadx=0, side=LEFT)
                            detailSeperator = ctk.CTkLabel(detailsFrame, text=f" : ", font=("Verdana", 15), text_color="#ff8059")
                            detailSeperator.pack(anchor=W, side=LEFT)
                            colorQuantityLabel = ctk.CTkLabel(detailsFrame, text=value.get("quantity"), font=("Verdana", 15), text_color='#ff59af')
                            colorQuantityLabel.pack(anchor=W, ipadx=0, side=LEFT)
                            rbracket = ctk.CTkLabel(detailsFrame, text=f"]  ", font=("Verdana", 15), text_color="#5cff59")
                            rbracket.pack(anchor=W, side=LEFT)
                    timestampLabel = ctk.CTkLabel(itemFrame, text=value.get("timestamp"), font=("Courier", 11)).pack(anchor=W, ipadx=15)
                    colorCounter += 1
    update_view()

    # ADD ITEMS SECTION
    def submit_form():
        # Clear previous error message
        root.title(f'Cleared error_label')
        error_label.configure(text="")
        root.title(f'Hiding preview_frame fields')
        preview_frame.configure(text="", fg_color=itemsAdd.cget('fg_color'))

        root.title(f'Getting and stripping new fields')
        item_name = item_name_entry.get().lstrip()
        description = description_entry.get().lstrip()
        quantity_str = quantity_entry.get()

        # Check if mandatory fields are empty
        if not item_name:
            root.title(f'Error Occured / Item Name is mandatory')
            error_label.configure(text="Error: Item Name is mandatory.", text_color="red", font=("Verdana", 15))
            return
        if fetch.check_item(string.capwords(item_name)) == True:
            error_label.configure(text=f"Error: '{string.capwords(item_name)}' already exists in inventory.", text_color="red", font=("Verdana", 15))
            return
        if not description:
            root.title(f'Error Occured / Description is mandatory')
            error_label.configure(text="Error: Description is mandatory.", text_color="red", font=("Verdana", 15))
            return
        if not quantity_str:
            root.title(f'Error Occured / Quantity is mandatory')
            error_label.configure(text="Error: Quantity is mandatory.", text_color="red", font=("Verdana", 15))
            return

        # Check if quantity is a valid integer
        try:
            quantity = [int(q) for q in quantity_str.split(',')]
        except ValueError:
            root.title(f'Error Occured / Quantity must be int or CSV if multiple items')
            error_label.configure(text="Error: Quantity must be integers separated by commas\nif you have multiple items.", text_color="red", font=("Verdana", 15))
            return
        
        if item_name == 'ITEM_ORIGIN':
            root.title(f'Error Occured / Reserved Name')
            error_label.configure(text="Error: ITEM_ORIGIN is a reserved name and cannot be used.", text_color="red", font=("Verdana", 15))
            return

        # Check if quantity and colors list lengths match
        colors = [color.lstrip() for color in colors_entry.get().split(',')]
        if len(quantity) > 1 and len(colors) != len(quantity):
            root.title(f'Error Occured / Non-equal colors and quantity')
            error_label.configure(text="Error: To add an item with multiple colors,\nthe quantity and colors item amount must be the same\nExample - Colors: Red, Blue | Quantity: 4, 6", text_color="red", font=("Verdana", 15))
            return
        
        # Check if colors list length is not greater than quantity
        if len(colors) > len(quantity):
            root.title(f'Error Occured / Non-equal colors and quantity')
            error_label.configure(text="Error: Number of colors cannot exceed the quantity of items,\nthe quantity and colors itemamount must be the\nsame for mutlicolor items", text_color="red", font=("Verdana", 15))
            return
        
        sizes = [color.lstrip() for color in sizes_entry.get().split(',')]
        if len(colors) == 1 and colors == [''] and sizes != ['']:
            fetch.add_item(item_name, description, quantity, sizes=sizes)
            preview_frame.configure(text=f"\n{string.capwords(item_name)}\n'{description}'\n Sizes: {sizes}\nQuantity: {quantity}\n", fg_color='grey4', font=("Verdana", 13))
        elif len(sizes) == 1 and sizes == [''] and colors != ['']:
            fetch.add_item(item_name, description, quantity, colors=colors)
            preview_frame.configure(text=f"\n{string.capwords(item_name)}\n'{description}'\n Colors: {colors}\nQuantity: {quantity}\n", fg_color='grey4', font=("Verdana", 13))
        elif len(sizes) == 1 and sizes == [''] and len(colors) == 1 and colors == ['']:
            fetch.add_item(item_name, description, quantity)
            preview_frame.configure(text=f"\n{string.capwords(item_name)}\n'{description}'\nQuantity: {quantity}\n", fg_color='grey4', font=("Verdana", 13))
        else:
            fetch.add_item(item_name, description, quantity, colors, sizes)
            preview_frame.configure(text=f"\n{string.capwords(item_name)}\n'{description}'\nSizes: {sizes}\n Colors: {colors}\nQuantity: {quantity}\n", fg_color='grey4', font=("Verdana", 13))
        
        clear_form()
        root.title(f'Added {item_name}')
        error_label.configure(text=f"Success! '{string.capwords(item_name)}' added, preview above.", text_color="#30E64D", font=("Verdana", 15))

    def clear_form():
        root.title(f'Cleared Form')
        item_name_entry.delete(0, ctk.END)
        description_entry.delete(0, ctk.END)
        sizes_entry.delete(0, ctk.END)
        colors_entry.delete(0, ctk.END)
        quantity_entry.delete(0, ctk.END)
        error_label.configure(text="", text_color="black")

    def focus_next_entry(current_entry, next_entry):
        root.title(f'Focusing Next Entry (Enter)')
        next_entry.focus()

    # Create a frame with light gray background color
    form_frame = ctk.CTkFrame(itemsAdd, fg_color="transparent", corner_radius=0)
    form_frame.pack(pady=40, expand=False, fill=BOTH)

    section_label = ctk.CTkLabel(form_frame, text="Add Item", text_color="#DFDFE1", font=("Verdana", 25))
    section_label.pack(anchor='s', pady=2)

    avise_label = ctk.CTkLabel(form_frame, text="For color, quantity and size use comma seperated\nvalues for multiple inputs", text_color="#DFDFE1", font=("Verdana", 11))
    avise_label.pack(anchor='s', pady=20)

    # Item Name
    item_name_label = ctk.CTkLabel(form_frame, text="Item Name:", font=("Verdana", 15))
    item_name_label.pack(anchor="w", ipadx=255)
    item_name_entry = ctk.CTkEntry(form_frame)
    item_name_entry.pack(anchor="center")
    item_name_entry.bind("<Return>", lambda event: focus_next_entry(item_name_entry, description_entry))

    # Description
    description_label = ctk.CTkLabel(form_frame, text="Description:", font=("Verdana", 15))
    description_label.pack(anchor="w", ipadx=255)
    description_entry = ctk.CTkEntry(form_frame)
    description_entry.pack(anchor="center")
    description_entry.bind("<Return>", lambda event: focus_next_entry(description_entry, sizes_entry))

    # Sizes
    sizes_label = ctk.CTkLabel(form_frame, text="Sizes (optional):", font=("Verdana", 15))
    sizes_label.pack(anchor="w", ipadx=255)
    sizes_entry = ctk.CTkEntry(form_frame)
    sizes_entry.pack(anchor="center")
    sizes_entry.bind("<Return>", lambda event: focus_next_entry(sizes_entry, colors_entry))

    # Colors
    colors_label = ctk.CTkLabel(form_frame, text="Colors (optional):", font=("Verdana", 15))
    colors_label.pack(anchor="w", ipadx=255)
    colors_entry = ctk.CTkEntry(form_frame)
    colors_entry.pack(anchor="center")
    colors_entry.bind("<Return>", lambda event: focus_next_entry(colors_entry, quantity_entry))

    # Quantity
    quantity_label = ctk.CTkLabel(form_frame, text="Quantity:", font=("Verdana", 15))
    quantity_label.pack(anchor="w", ipadx=255)
    quantity_entry = ctk.CTkEntry(form_frame)
    quantity_entry.pack(anchor="center")
    quantity_entry.bind("<Return>", lambda event: submit_form())

    # Submit button
    submit_button = ctk.CTkButton(form_frame, text="Submit", command=submit_form, fg_color='#30E64D', text_color='black', hover_color='#24AB3A', font=("Arial", 15, "bold"))
    submit_button.pack(anchor='center', padx=5, pady=20)

    # Clear form button
    clear_button = ctk.CTkButton(form_frame, text="Clear Form", command=clear_form, fg_color="#db160f", text_color='white', hover_color='#9D130E' ,font=("Arial", 15, "bold"))
    clear_button.pack(anchor='center', padx=5, pady=0)

    # Item preview
    preview_frame = ctk.CTkLabel(form_frame, text="")
    preview_frame.pack(anchor='s', pady=15, ipadx=30, ipady=30)

    # Error label
    error_label = ctk.CTkLabel(form_frame, text="", text_color="red")
    error_label.pack(anchor='s', pady=0)

    # REMOVE ITEMS SECTION
    def check_or_remove():
        root.title(f'Cleared r_error_label')
        r_error_label.configure(text='')
        root.title(f'Getting item name')
        r_item_name = r_item_name_entry.get()
        
        if not r_item_name:
            root.title(f'Error Occurred / No item name provided')
            r_error_label.configure(text="Error: Please enter item's name.", text_color="red", font=("Verdana", 15))
            return
        
        if fetch.check_item(string.capwords(r_item_name)):
            if r_check_button.cget("text") == "Check Item":
                r_cancel_button.configure(state="normal")
                root.title(f'Checking removal')
                r_item_name_label.configure(text=f"Are you sure you want to remove '{string.capwords(r_item_name)}'?\n(This action is irreversible)", font=("Verdana", 17, 'italic'), text_color='#FABE41')
                r_item_name_label.pack_configure(anchor='center', ipadx=0)
                r_check_button.configure(text="Remove Item", fg_color="#FFA500", hover_color='#C58000')
                r_cancel_button.configure(fg_color="#db160f", text_color='white', hover_color='#9D130E')
                r_item_name_entry.configure(fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=0)
                r_item_name_entry.configure(state="disabled")
                r_error_label.configure(text="")
                r_item_label.configure(fg_color='gray4')


                r_itemname_values = save_values_to_dict(fetch.get_allContent(), str(string.capwords(r_item_name)))

                for widget in r_item_label.winfo_children():
                    widget.pack_forget()

                topSpacer = ctk.CTkLabel(r_item_label, text='').pack(ipady=1)
                nameLabel = ctk.CTkLabel(r_item_label, text=string.capwords(str(r_item_name)), font=("Arial", 18, 'bold'), text_color='#F4EF5F').pack(anchor=W, ipadx=15)
                descriptionLabel = ctk.CTkLabel(r_item_label, text=r_itemname_values[str(string.capwords(r_item_name))].get("description"), font=("Verdana", 15,'italic'), text_color='#4bb7fa', wraplength=550, justify=LEFT).pack(anchor=W, ipadx=15)
                
                if r_itemname_values[str(string.capwords(r_item_name))].get('sizes') != None:
                    sizesFrame = ctk.CTkFrame(r_item_label, fg_color='gray4')
                    sizesFrame.pack(anchor=W)
                    availableSizesLabel = ctk.CTkLabel(sizesFrame, text=f"Available Sizes:", font=("Verdana", 15)).pack(anchor=W, ipadx=15, side=LEFT)
                    sizeslbracket = ctk.CTkLabel(sizesFrame, text=f"[", font=("Verdana", 15), text_color="#4ef5a1")
                    sizeslbracket.pack(anchor=W, side=LEFT)
                    for count, size in enumerate(list(r_itemname_values[str(string.capwords(r_item_name))].get('sizes'))):
                        sizesLabel = ctk.CTkLabel(sizesFrame, text=f"{size}", font=("Verdana", 15), text_color='#F5634E').pack(anchor=W, side=LEFT)
                        if count+1 != len(list(r_itemname_values[str(string.capwords(r_item_name))].get('sizes'))):
                            addComma = ctk.CTkLabel(sizesFrame, text=', ', font=("Verdana", 15)).pack(anchor=W, side=LEFT)
                    sizesrbracket = ctk.CTkLabel(sizesFrame, text=f"]", font=("Verdana", 15), text_color="#4ef5a1")
                    sizesrbracket.pack(anchor=W, side=LEFT)

                if r_itemname_values[str(string.capwords(r_item_name))].get('quantity') != None and r_itemname_values[str(string.capwords(r_item_name))].get('colors') == None:
                    quantityFrame = ctk.CTkFrame(r_item_label, fg_color='gray4')
                    quantityFrame.pack(anchor=W)
                    quantityMainLabel = ctk.CTkLabel(quantityFrame, text=f"Quantity:", font=("Verdana", 15)).pack(anchor=W, ipadx=15, side=LEFT)
                    quantityLabel = ctk.CTkLabel(quantityFrame, text=str(r_itemname_values[str(string.capwords(r_item_name))].get('quantity')).replace('[','').replace(']','').replace("'",''), font=("Verdana", 15), text_color='#ff59af').pack(anchor=W, side=LEFT)
                if r_itemname_values[str(string.capwords(r_item_name))].get('colors') != None:
                    colorToplabel = ctk.CTkLabel(r_item_label, text='Color & Quantity:', font=("Verdana",15))
                    colorToplabel.pack(anchor=W, ipadx=15)
                    if r_itemname_values[str(string.capwords(r_item_name))].get('quantity') == None:
                        colorqScroll = ctk.CTkScrollableFrame(r_item_label, fg_color='gray4', height=20, width=300, orientation='horizontal', corner_radius=0, scrollbar_button_color='gray7')
                        colorqScroll.pack(anchor=W)
                        spacer = ctk.CTkLabel(colorqScroll, text='')
                        spacer.pack(anchor=W, side=LEFT, ipadx=16)
                        for colorq in r_itemname_values[str(string.capwords(r_item_name))].get("colors"):
                            lbracket = ctk.CTkLabel(colorqScroll, text=f"[", font=("Verdana", 15), text_color="#5cff59")
                            lbracket.pack(anchor=W, side=LEFT)
                            colorColorLabel = ctk.CTkLabel(colorqScroll, text=f"{string.capwords(colorq.split('/')[0])}", font=("Verdana", 15, 'bold'))
                            colorColorLabel.pack(anchor=W, ipadx=0, side=LEFT)
                            detailSeperator = ctk.CTkLabel(colorqScroll, text=f" : ", font=("Verdana", 15), text_color="#ff8059")
                            detailSeperator.pack(anchor=W, side=LEFT)
                            colorQuantityLabel = ctk.CTkLabel(colorqScroll, text=f"{colorq.split('/')[1]}", font=("Verdana", 15), text_color='#ff59af')
                            colorQuantityLabel.pack(anchor=W, ipadx=0, side=LEFT)
                            rbracket = ctk.CTkLabel(colorqScroll, text=f"]  ", font=("Verdana", 15), text_color="#5cff59")
                            rbracket.pack(anchor=W, side=LEFT)
                    else:
                        detailsFrame = ctk.CTkFrame(r_item_label, fg_color='gray4')
                        detailsFrame.pack(anchor=W)

                        spacer = ctk.CTkLabel(detailsFrame, text='')
                        spacer.pack(anchor=W, side=LEFT, ipadx=16)
                        lbracket = ctk.CTkLabel(detailsFrame, text=f"[", font=("Verdana", 15), text_color="#5cff59")
                        lbracket.pack(anchor=W, side=LEFT)
                        colorColorLabel = ctk.CTkLabel(detailsFrame, text=string.capwords(str(r_itemname_values[str(string.capwords(r_item_name))].get("colors")).replace('[','').replace(']','').replace("'",'')), font=("Verdana", 15, 'bold'))
                        colorColorLabel.pack(anchor=W, ipadx=0, side=LEFT)
                        detailSeperator = ctk.CTkLabel(detailsFrame, text=f" : ", font=("Verdana", 15), text_color="#ff8059")
                        detailSeperator.pack(anchor=W, side=LEFT)
                        colorQuantityLabel = ctk.CTkLabel(detailsFrame, text=r_itemname_values[str(string.capwords(r_item_name))].get("quantity"), font=("Verdana", 15), text_color='#ff59af')
                        colorQuantityLabel.pack(anchor=W, ipadx=0, side=LEFT)
                        rbracket = ctk.CTkLabel(detailsFrame, text=f"]  ", font=("Verdana", 15), text_color="#5cff59")
                        rbracket.pack(anchor=W, side=LEFT)
                timestampLabel = ctk.CTkLabel(r_item_label, text=r_itemname_values[str(string.capwords(r_item_name))].get("timestamp"), font=("Courier", 11)).pack(anchor=W, ipadx=15)
                bottomSpacer = ctk.CTkLabel(r_item_label, text='').pack(ipady=1)
            else:
                fetch.remove_item(r_item_name)
                root.title(f'Removed item {r_item_name}')
                r_item_name_label.configure(text="Item Name:", font=("Verdana", 15), text_color='gray84')
                r_item_name_label.pack_configure(anchor='w', ipadx=255)
                r_cancel_button.configure(state="disabled")
                r_error_label.configure(text=f"Removed item '{string.capwords(r_item_name)}'", text_color="#30E64D", font=("Verdana", 15))
                r_check_button.configure(text="Check Item", fg_color="#74D3B7", hover_color='#549985')
                r_item_name_entry.configure(state="normal")
                r_cancel_button.configure(fg_color="transparent", text_color_disabled='gray13')
                r_item_name_entry.delete(0, ctk.END)
                r_item_label.configure(fg_color='transparent', height=0)
                r_item_name_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
                for widget in r_item_label.winfo_children():
                    widget.pack_forget()
        else:
            r_error_label.configure(text=f"Error: '{string.capwords(r_item_name)}' does not exists in inventory.", text_color="red", font=("Verdana", 15))
            return
        
    def cancel_action():
        root.title(f'Cancelled Removal')
        r_item_name_label.configure(text="Item Name:", font=("Verdana", 15), text_color='gray84')
        r_item_name_label.pack_configure(anchor='w', ipadx=255)
        r_error_label.configure(text="")
        r_item_label.configure(fg_color='transparent', height=0)
        r_cancel_button.configure(fg_color="transparent", text_color_disabled='gray13')
        r_check_button.configure(text="Check Item", fg_color="#74D3B7", hover_color='#549985')
        r_item_name_entry.configure(state="normal")
        r_item_name_entry.delete(0, ctk.END)
        r_cancel_button.configure(state="disabled")
        r_item_name_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
        for widget in r_item_label.winfo_children():
                widget.pack_forget()

    # Main label
    r_main_label = ctk.CTkLabel(itemsRemove, text="\nRemove Item", font=("Verdana", 25))
    r_main_label.pack(pady=10)

    # Form to input item's name
    r_item_name_label = ctk.CTkLabel(itemsRemove, text="Item Name:", font=("Verdana", 15), text_color='gray84')
    r_item_name_label.pack(anchor="w", ipadx=255)
    r_item_name_entry = ctk.CTkEntry(itemsRemove, fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
    r_item_name_entry.pack()
    r_item_name_entry.bind("<Return>", lambda event: check_or_remove())

    # Label to display item name if found
    r_item_label = ctk.CTkFrame(itemsRemove, fg_color='transparent', corner_radius=0, height=0, width=250)
    r_item_label.pack(pady=5)

    # Button to check or remove item
    r_check_button = ctk.CTkButton(itemsRemove, text="Check Item", command=check_or_remove, fg_color="#74D3B7", text_color='black', hover_color='#549985', font=("Arial", 15, "bold"))
    r_check_button.pack(padx=5, pady=10)

    # Cancel button
    r_cancel_button = ctk.CTkButton(itemsRemove, text="Cancel Removal", command=cancel_action, fg_color="transparent", text_color_disabled='gray13', font=("Arial", 15, "bold"))
    r_cancel_button.pack(padx=0, pady=10)
    r_cancel_button.configure(state="disabled")

    # Error label
    r_error_label = ctk.CTkLabel(itemsRemove, text="", font=("Verdana", 11), text_color="red")
    r_error_label.pack(pady=5)

    # EDIT ITEMS SECTION
    def edit_or_submit():
        root.title(f'Cleared e_error_label')
        e_error_label.configure(text='')
        e_item_name = e_item_name_entry.get().lstrip()

        if not e_item_name:
            root.title(f'Error Occurred / No item name provided')
            e_error_label.configure(text="Error: Please enter item's name.", text_color="red", font=("Verdana", 15))
            return
        
        if fetch.check_item(string.capwords(e_item_name)):
            if e_edit_button.cget("text") == "Edit Item":
                root.title(f'Editing item: {string.capwords(e_item_name)}')
                e_item_name_entry.configure(fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=0)
                e_item_name_label.configure(text=f'Editing {string.capwords(e_item_name)}', font=("Verdana", 17, 'italic'), text_color='#5FE5D1')
                e_item_name_label.pack_configure(anchor='center')
                e_item_name_entry.configure(state="disabled")
                e_cancel_button.configure(state="normal")
                e_edit_button.configure(text="Submit Changes", fg_color="#30E64D", hover_color='#24AB3A')
                e_cancel_button.configure(fg_color="#db160f", text_color='white', hover_color='#9D130E')
                e_error_label.configure(text="")

                e_hold_entrys.propagate(True)

                e_description_label.configure(text_color='gray84')
                e_sizes_label.configure(text_color='gray84')
                e_colors_label.configure(text_color='gray84')
                e_quantity_label.configure(text_color='gray84')

                e_description_entry.configure(state="normal")
                e_sizes_entry.configure(state="normal")
                e_colors_entry.configure(state="normal")
                e_quantity_entry.configure(state="normal")

                e_description_label.configure(text="Description:", font=("Verdana", 15))
                e_sizes_label.configure(text="Sizes (optional):", font=("Verdana", 15))
                e_colors_label.configure(text="Colors (optional):", font=("Verdana", 15))
                e_quantity_label.configure(text="Quantity:", font=("Verdana", 15))

                e_description_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
                e_sizes_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
                e_colors_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
                e_quantity_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)

                e_itemname_values = save_values_to_dict(fetch.get_allContent(), str(string.capwords(e_item_name)))[str(string.capwords(e_item_name))]

                entrys_list = [e_description_entry, e_sizes_entry, e_colors_entry, e_quantity_entry]
                methods = ['description', 'sizes', 'colors', 'quantity']
                for entry, method in zip(entrys_list, methods):
                    try:
                        if e_itemname_values[method] != None:
                            if method == 'sizes':
                                entry.insert(0, ','.join(e_itemname_values[method]))
                            else:
                                entry.insert(0, e_itemname_values[method])
                        else:
                            entry.insert(0, '')
                    except KeyError as ke:
                        if str(ke) == "'quantity'":
                            current_ecolor = e_colors_entry.get().split(' ')
                            e_colors_entry.delete(0, ctk.END)
                            for count, group in enumerate(current_ecolor):
                                color_quantity = group.split('/')
                                if count + 1 == len(current_ecolor):
                                    e_colors_entry.insert(0, f'{color_quantity[0]},')
                                    e_quantity_entry.insert(0, f'{color_quantity[1]},')
                                else:
                                    e_colors_entry.insert(0, color_quantity[0])
                                    e_quantity_entry.insert(0, color_quantity[1])
            else:
                e_description = e_description_entry.get().lstrip()
                e_quantity_str = e_quantity_entry.get()
                
                # Check if mandatory fields are empty
                if not e_description:
                    root.title(f'Error Occurred / Description is mandatory')
                    e_error_label.configure(text="Error: Description is mandatory.", text_color="red", font=("Verdana", 15))
                    return
                if not e_quantity_str:
                    root.title(f'Error Occurred / Quantity is mandatory')
                    e_error_label.configure(text="Error: Quantity is mandatory.", text_color="red", font=("Verdana", 15))
                    return

                # Check if quantity is a valid integer
                try:
                    e_quantity = [int(q) for q in e_quantity_str.split(',')]
                except ValueError:
                    root.title(f'Error Occurred / Quantity must be int or CSV if multiple items')
                    e_error_label.configure(text="Error: Quantity must be integers separated by commas.", text_color=   "red", font=("Verdana", 15))
                    return

                edit_parseitems_list = ['description','sizes','colors','quantity']
                # Check if quantity and colors list lengths match
                e_colors = [color.lstrip() for color in e_colors_entry.get().split(',') if color != ""]
                e_sizes = [sizes.lstrip() for sizes in e_sizes_entry.get().split(',') if sizes != ""]
                if len(e_quantity) > 1 and len(e_colors) != len(e_quantity):
                    root.title(f'Error Occurred / Quantity must be int or CSV if multiple items')
                    e_error_label.configure(text="Error: To add an item with multiple colors,\nthe quantity and colors item amount must be the same\nExample - Colors: Red, Blue | Quantity: 4, 6", text_color="red", font=("Verdana", 15))
                    return
            
                # Check if colors list length is not greater than quantity
                if len(e_colors) > len(e_quantity):
                    root.title(f'Error Occured / Non-equal colors and quantity')
                    e_error_label.configure(text="Error: Number of colors cannot exceed the quantity of items,\nthe quantity and colors itemamount must be the\nsame for mutlicolor items", text_color="red", font=("Verdana", 15))
                    return
                
                edited = []
                for edit, values in zip([e_description_entry, e_sizes_entry, e_colors_entry, e_quantity_entry], [e_description, e_sizes, e_colors, e_quantity]):
                    if len(edit.get()) != 0 or edit.get() != '':
                        edited.append(values)
                    else:
                        edited.append(None)

                fetch.edit_item(string.capwords(e_item_name), {key: method for key, method in zip(edit_parseitems_list, edited) if method is not None})

                e_edit_button.configure(text="Edit Item", fg_color="#EB96FA", hover_color='#B473C0')
                e_item_name_entry.configure(state="normal")
                e_clear_form()
                e_cancel_action()
                root.title(f'Remember to REFRESH VIEW in overview! / Successfully edited item')
                e_error_label.configure(text=f"Successfully edited item '{string.capwords(e_item_name)}'", text_color="#30E64D", font=("Verdana", 15))
        else:
            root.title(f'Error Occurred / {string.capwords(e_item_name)} does not exists in inventory')
            e_error_label.configure(text=f"Error: '{string.capwords(e_item_name)}' does not exists in inventory.", text_color="red", font=("Verdana", 15))
            return

    def e_clear_form():
        root.title(f'Cleared form')
        e_item_name_entry.delete(0, ctk.END)
        e_error_label.configure(text="", text_color="black")

    def e_cancel_action():
        root.title(f'Cancelled action')
        e_item_name_label.configure(text="Item Name:", font=("Verdana", 15), text_color='gray84')
        e_item_name_label.pack_configure(anchor='w')
        e_item_name_entry.configure(state="normal")
        e_item_name_entry.delete(0, ctk.END)
        e_item_name_entry.configure(fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)

        e_hold_entrys.configure(height=0)
        e_hold_entrys.propagate(False)

        root.title(f'Reset entrys')
        e_description_entry.configure(fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=0)
        e_sizes_entry.configure(fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=0)
        e_colors_entry.configure(fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=0)
        e_quantity_entry.configure(fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=0)

        root.title(f'Reset labels')
        e_description_label.configure(text_color=itemsRemove.cget('fg_color'))
        e_sizes_label.configure(text_color=itemsRemove.cget('fg_color'))
        e_colors_label.configure(text_color=itemsRemove.cget('fg_color'))
        e_quantity_label.configure(text_color=itemsRemove.cget('fg_color'))

        root.title(f'Clear fields')
        e_description_entry.delete(0, ctk.END)
        e_sizes_entry.delete(0, ctk.END)
        e_colors_entry.delete(0, ctk.END)
        e_quantity_entry.delete(0, ctk.END)
        e_description_entry.configure(state="disabled")
        e_sizes_entry.configure(state="disabled")
        e_colors_entry.configure(state="disabled")
        e_quantity_entry.configure(state="disabled")

        e_error_label.configure(text="")
        e_cancel_button.configure(fg_color="transparent", text_color_disabled='gray13')
        e_edit_button.configure(text="Edit Item", fg_color="#EB96FA", hover_color='#B473C0')
        e_cancel_button.configure(state="disabled")
        root.title(f'Item Crate - Edit Item')

    def e_focus_next_entry(current_entry, next_entry):
        root.title(f'Focusing Next Entry (Enter)')
        next_entry.focus()

    # Main edit items label
    e_main_label = ctk.CTkLabel(itemsEdit, text="\nEdit Item", font=("Verdana", 25))
    e_main_label.pack(pady=10)

    e_avise_label = ctk.CTkLabel(itemsEdit, text="For color, quantity and size use comma seperated\nvalues for multiple inputs", text_color="#DFDFE1", font=("Verdana", 11))
    e_avise_label.pack(anchor='s', pady=20)

    # Form to input item's name
    e_item_name_label = ctk.CTkLabel(itemsEdit, text="Item Name:", font=("Verdana", 15))
    e_item_name_label.pack(anchor="w", ipadx=255)
    e_item_name_entry = ctk.CTkEntry(itemsEdit, fg_color='#343638', border_color='#565B5E', text_color='gray84', height=28)
    e_item_name_entry.pack()
    e_item_name_entry.bind("<Return>", lambda event: edit_or_submit())

    # Label to display frame name if found

    e_hold_entrys = ctk.CTkFrame(itemsEdit, height=0)
    e_hold_entrys.pack()
    e_hold_entrys.propagate(False)

    # Description
    e_description_label = ctk.CTkLabel(e_hold_entrys, text="Description:", font=("Verdana", 15), text_color=itemsRemove.cget('fg_color'))
    e_description_label.pack(anchor="w", ipadx=255)
    e_description_entry = ctk.CTkEntry(e_hold_entrys, fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=28)
    e_description_entry.configure(height=0)
    e_description_entry.pack(anchor="center")
    e_description_entry.bind("<Return>", lambda event: e_focus_next_entry(e_description_entry, e_sizes_entry))
    e_description_entry.configure(state="disabled")

    # Sizes
    e_sizes_label = ctk.CTkLabel(e_hold_entrys, text="Sizes (optional):", font=("Verdana", 15), text_color=itemsRemove.cget('fg_color'))
    e_sizes_label.pack(anchor="w", ipadx=255)
    e_sizes_entry = ctk.CTkEntry(e_hold_entrys, fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=28)
    e_sizes_entry.configure(height=0)
    e_sizes_entry.pack(anchor="center")
    e_sizes_entry.bind("<Return>", lambda event: e_focus_next_entry(e_sizes_entry, e_colors_entry))
    e_sizes_entry.configure(state="disabled")

    # Colors
    e_colors_label = ctk.CTkLabel(e_hold_entrys, text="Colors (optional):", font=("Verdana", 15), text_color=itemsRemove.cget('fg_color'))
    e_colors_label.pack(anchor="w", ipadx=255)
    e_colors_entry = ctk.CTkEntry(e_hold_entrys, fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=28)
    e_colors_entry.configure(height=0)
    e_colors_entry.pack(anchor="center")
    e_colors_entry.bind("<Return>", lambda event: e_focus_next_entry(e_colors_entry, e_quantity_entry))
    e_colors_entry.configure(state="disabled")

    # Quantity
    e_quantity_label = ctk.CTkLabel(e_hold_entrys, text="Quantity:", font=("Verdana", 15), text_color=itemsRemove.cget('fg_color'))
    e_quantity_label.pack(anchor="w", ipadx=255)
    e_quantity_entry = ctk.CTkEntry(e_hold_entrys, fg_color=itemsRemove.cget('fg_color'), border_color=itemsRemove.cget('fg_color'), text_color=itemsRemove.cget('fg_color'), height=28)
    e_quantity_entry.configure(height=0)
    e_quantity_entry.pack(anchor="center")
    e_quantity_entry.bind("<Return>", lambda event: edit_or_submit())
    e_quantity_entry.configure(state="disabled")

    # Button to edit or submit item
    e_edit_button = ctk.CTkButton(itemsEdit, text="Edit Item", command=edit_or_submit, fg_color="#EB96FA", hover_color='#B473C0', text_color='black', font=("Arial", 15, "bold"))
    e_edit_button.pack(padx=5, pady=20)

    # Cancel button
    e_cancel_button = ctk.CTkButton(itemsEdit, text="Cancel Edit", command=e_cancel_action, fg_color="transparent", text_color_disabled='gray13', font=("Arial", 15, "bold"))
    e_cancel_button.pack(padx=0, pady=0)
    e_cancel_button.configure(state="disabled")

    # Error label
    e_error_label = ctk.CTkLabel(itemsEdit, text="", font=("Verdana", 11), text_color="red")
    e_error_label.pack(pady=5)
except Exception as e:
    print(e)
    input('Press enter to continue...')

root.mainloop()