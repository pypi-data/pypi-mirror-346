# Module Swap
**Module Swap** is a plugin for [NetBox](https://github.com/netbox-community/netbox) that allows easy swapping of Modules between Devices, linking of Modules and InventoryItems and makes sure that linked Modules and InventoryItems have synchronized data.

## Features
- **Easy Module swapping**: Swapping Modules between Devices made easy with just a few clicks and keeping module history.
- **One-to-One Binding**: Establish a unique relationship between a module and an inventory item.
- **CRUD Operations**: Create, read, update, and delete bindings between modules and inventory items.
- **Safe Deletion**: Deletes associated inventory items when a module is deleted.
- **Integration with NetBox UI**: Seamlessly integrates into NetBox's main menu for easy access to binding functionalities.

## Requirements
These are the versions of NetBox and Python that I used when developing my plugin. I highly recommend using this version of NetBox since i don't know if they changed anything in newer versions that could break the plugin.

- **NetBox** NetBox Community `v4.1.6` (2024-10-31).
- **Python** version `3.10.12` or higher.

## Installation
Plugin is available on PYPI so you can install it easily with pip.
### Step 1: Install using pip
```bash
pip install module_swap
```
### Step 2: Add the plugin into PLUGINS array in configuration.py
```bash
PLUGINS = [
    'module_swap',
    # Other plugins...
]
```
### Step 3: Apply migrations(don't forget activating virtual enviroment)
```bash
python manage.py migrate module_swap
```
### Step 4: Run netbox(for example)
```bash
python manage.py runserver
```

## Usage
### ✉️ Transfer a module between devices
1. Open the module detail page
2. Click the **"Transfer module"** button
3. Select the target device and module bay

or

1. From the plugin navigation, open **"Module Swap"**
2. Select the target device and module bay
3. Done

The transfer:
- automatically removes the module from the original device,
- reassigns it to the target device,
- updates the associated Inventory Item if linked.

### ⚙️ Linking with Inventory Item
1. From the plugin navigation, open **"Inventory item and module links"**
2. Create a new link between a Module and an InventoryItem
3. When the module is transferred, the InventoryItem device will update automatically

## Project Structure
```
module_swap/
├── models.py              # Link model definition
├── views.py               # Transfer and linking logic
├── forms.py               # User forms
├── templates/             # HTML templates
├── urls.py                # Plugin URLs
├── navigation.py          # Plugin menu entries
└── migrations/            # DB migrations
```

## Changelog
### v1.2.1
- Added headers into each file

### v1.2
- Added Inventory Item ↔ Module linking
- Automatic Inventory Item updates on module movement
- Removed debugging code parts, added comments in code, cleanup
- Added complete README

### v1.1
- Added templates to the PYPI project (forgot about it in v1.0)

### v1.0
- Initial implementation of module swapping logic and templates

## Notes
- The plugin does not override NetBox core behavior (only extends it)
    - This means, that i didn't do any sort of changes to the core code - would it be logic or appearence since this would be against the logic of using plugins - if you want to do sort of edits to the application core do it on your own NetBox instance  

- When linking Module and InventoryItem, the InventoryItem Device gets updated to the Device that is linked with the Module - this made sense to me since when you create InventoryItem it requires Device and we shouldn't keep a different device in the InventoryItem other than the one that is linked with the Module - hope this makes sense :)

- If you wish to add some sort of buttons for accessing plugin you can do it a couple of ways
    - you can edit the core of NetBox app - edit html template file you want the button on
    - you can use the Custom Links function in NetBox under the customization section
    - you can try to override html template - i tried but it didn't work - maybe i did something wrong

- As i said earlier this is a PLUGIN - it should be adding new functionality, not poke in core thing hence i strogly recommend using the stuff i created because when you will edit the core app you will probably have to do it everytime you upgrade NetBox - only Custom Links should stay since i think they are saved as a DB object so as long as you keep your DB you should be good

- Supports changelog history (Journal + changelog tabs)

## Author
Viktor Kubec  
BUT FIT Brno student  
MIT License  
GitHub: [vubeckubec/Module_Swap](https://github.com/vubeckubec/Module_Swap)
