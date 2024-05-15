import datetime
import yaml
import string
import os

try:
    inventory_file: str = f"{os.path.abspath(__file__).replace('fetcher.py','')}inventory.yaml"
    print(inventory_file)
    dict_formatting = True

    class yml:
        def __init__(self) -> None:
            self.invfile = inventory_file
            print('Fetcher running')

        def yread(self):
            try:
                with open(self.invfile, 'r', encoding='utf-8') as f:
                    content: dict = yaml.safe_load(f)
                return content
            except Exception as e:
                print(f"There was an error loading {self.invfile}\n Error: {e}")
                raise Exception(__file__)
            
        def yappend(self, new_content):
            try:
                with open(self.invfile, 'r', encoding='utf-8') as f:
                    old_content: dict = yaml.safe_load(f)
                if old_content != None:
                    old_content.update(new_content)
                    with open(self.invfile, 'w', encoding='utf-8') as f:
                        yaml.dump(old_content, f, default_flow_style=dict_formatting, sort_keys=False)
                else:
                    with open(self.invfile, 'w', encoding='utf-8') as f:
                        yaml.dump(new_content, f, default_flow_style=dict_formatting, sort_keys=False)
                print(f"{self.invfile} appended content successfully")
            except Exception as e:
                print(f"There was an error loading {self.invfile}\n Error: {e}")
                raise Exception(__file__)
            
        def ywrite(self, new_content):
            try:
                with open(self.invfile, 'w') as f:
                    yaml.dump(new_content, f, default_flow_style=dict_formatting)
                print(f"{self.invfile} wrote content successfully")
            except Exception as e:
                print(f"There was an error loading {self.invfile}\n Error: {e}")
                raise Exception(__file__)

    class Fetch:
        def __init__(self) -> None:
            self.yml = yml()
            # self.inv is inventory
            self.inv: dict = self.yml.yread()

            if self.inv == None or self.inv != None and 'ITEM_ORIGIN' not in self.inv:
                self.inv = self.yml.ywrite({'ITEM_ORIGIN': {'DEVELOPER': 'MaG|tehllama.','DO_NOT_DELETE':True,'FILE_CREATION_DATE': self.get_time()}})

        def check_item(self, key):
            inv = self.yml.yread()
            if inv != None:
                if key in self.yml.yread():
                    print(f"{key} exists")
                    return True
                return False
            
        def get_time(self):
            return "[{} {}]".format(datetime.datetime.now().strftime("%H:%M:%S"), datetime.datetime.now().strftime("%d/%m/%Y"))

        def get_allContent(self):
            return self.yml.yread() 
        
        def get_keysAmount(self):
            yaml_data = dict(self.yml.yread())
            if isinstance(yaml_data, dict):
                return len(yaml_data)-1
            else:
                return 0
        
        def add_item(self, itemname:str, description:str, quantity:list, colors:list=None, sizes:list=None):
            if colors != None and len(colors) > 1:
                if len(colors) != len(quantity):
                    print('Colors must have same amount of quantity for each color')
                    return False
                content = {string.capwords(itemname): {"description": description, "sizes": sizes, "colors": [f"{color}/{number}" for color, number in zip(colors, quantity)], "timestamp": self.get_time()}}
            else:
                content = {string.capwords(itemname): {"description": description, "sizes": sizes, "quantity": quantity,"colors": colors, "timestamp": self.get_time()}}
            if self.check_item(itemname) != True:
                self.yml.yappend(content)

        def edit_item(self, itemname:str, updates:dict):
            inv = self.yml.yread()
            itemname = string.capwords(itemname)
            if self.check_item(itemname):
                if "quantity" in dict(inv[itemname]).keys() and updates["quantity"] == 1:
                    for key in updates:
                        if key not in inv[itemname]:
                            print(f'{key} does not exist in {itemname}')
                            continue
                        inv[itemname][key] = updates[key]
                    self.yml.ywrite(inv)
                else:
                    try:
                        del inv[itemname]['quantity']
                    except Exception:
                        print(f' Quantity does not yet exist in {itemname}')
                    for key in updates:
                        if key not in inv[itemname]:
                            print(f'{key} does not exist in {itemname}')
                            continue
                        inv[itemname][key] = updates[key]
                    if "colors" in updates and "quantity" in updates:
                        colors = updates["colors"]
                        quantity = updates["quantity"]
                        inv[itemname]['colors'] = [f"{color}/{quantity[i]}" for i, color in enumerate(colors)]
                    elif "colors" not in updates and "quantity" in updates:
                        inv[itemname]['colors'] = None
                        inv[itemname]['quantity'] = updates['quantity']
                        print("Both 'colors' and 'quantity' keys are required to update 'colors' key.")
                    if "colors" in updates and len(updates['colors']) == 1:
                        split_color = str(inv[itemname]['colors'][0]).split("/")
                        inv[itemname]['colors'] = [split_color[0]]
                        inv[itemname]['quantity'] = [int(split_color[1])]
                    self.yml.ywrite(inv)
            else:
                print(f'{itemname} does not exist')
                return 0
        
        def remove_item(self, itemname:str):
            inv = self.yml.yread()
            if self.check_item(string.capwords(itemname)):
                del inv[string.capwords(itemname)]
                self.yml.ywrite(inv)
                print(f'{itemname} removed successfully')
            else:
                print(f'{itemname} does not exist')
                return 0
except Exception as e:
    print(e)
    input('Press enter to continue...')
