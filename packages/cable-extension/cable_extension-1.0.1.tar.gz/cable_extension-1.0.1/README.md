# Cable Extension

**Cable Extension** is a plugin for [NetBox](https://github.com/netbox-community/netbox) that enhances cable-related data and provides optional integration with device inventories. With this plugin, you can create and manage cables using a custom form, optionally create InventoryItems on both ends, and store extended information (such as manufacturer or custom comments) in a linked model.

---

## Features

- **Extended Cable Creation**: A dedicated form (`CableCreateForm`) to create cables between one or two Interfaces, capturing extra details (serial, part ID, etc.).
- **Inventory Item Integration**: Automatically creates `InventoryItem` records for each device end if desired.
- **Manufacturer/Comments**: Supports additional cable metadata (manufacturer, comments) through the `CableExtension` model.
- **NetBox UI Integration**: Provides a clear user interface under the plugin’s menu for creating cables and editing extended data.

---

## Requirements

- **NetBox**: version `4.1.6`  
- **Python**: version `3.10.12` or higher  

These are the versions used during development and testing. If you run into compatibility issues on other versions, please open an issue.

---

## Installation

### Step 1: Install using pip

```bash
pip install cable_extension

```
### Step 2: Add the plugin into PLUGINS array in configuration.py
```bash
PLUGINS = [
    'cable_extension',
    # Other plugins...
]
```
### Step 3: Apply migrations(don't forget activating virtual enviroment)
```bash
python manage.py migrate cable_extension
```
### Step 4: Run netbox(for example)
```bash
python manage.py runserver
```

## Usage
###Creating a Cable

1. In NetBox, navigate to Plugins → Cable Extension → Create Cable (or your chosen URL path).

2. Fill out details like:
    - Interfaces for end A and B
    - Cable serial, part ID, label, description, length
    - Check “Create InventoryItem for both ends?” to add inventory entries on both devices

3. Click Save. The plugin:
    - Creates a new cable in NetBox
    - Sets up cable terminations on the specified interfaces        
    - Optionally creates InventoryItem objects for each end
    - Stores any extra details (like manufacturer, comments) in its own CableExtension model

## Project Structure
```
cable_extension/
├── models.py          # CableExtension model for extended cable data
├── forms.py           # CableCreateForm for cable + inventory creation
├── views.py           # View classes for creating/editing cables
├── templates/         # HTML templates
│   └── cable_extension/
│       ├── cable_create.html
│       └── cable_extension_edit.html
├── urls.py            # URL definitions for the plugin
```

## Changelog
### v1.0.1
- Added headers in each file, fixed some comments
### v1.0
- Initial release with custom cable creation form
- Optional InventoryItem creation on both ends
- Extended cable data stored in CableExtension model

## Notes
- Non-Invasive: The plugin does not modify NetBox’s core cable logic – it simply provides an alternate creation flow and extension points.

- Customization: Feel free to adapt the forms or models to suit your environment. The plugin is designed to be extendable without impacting NetBox’s base code.

- License/Contributions: Contributions and forks are welcome. Please see the repository for more details on licensing.

## Author
Viktor Kubec  
BUT FIT Brno student  
MIT License  
GitHub: [vubeckubec/cable_extension](https://github.com/vubeckubec/cable_extension)
