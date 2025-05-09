# Interface Relationship Manager

**Interface Relationship Manager** is a plugin for [NetBox](https://github.com/netbox-community/netbox) that allows you to split a single physical or virtual interface into two separate logical interfaces for RX and TX traffic, while retaining the original interface as the "main" interface. This plugin is useful for scenarios where you need granular control or monitoring of inbound and outbound traffic on an interface.

## Features
- **Easy interface splitting**: Split any interface into separate RX and TX interfaces with a single click.
- **Retains the original interface**: Automatically establishes a relationship between the main interface and the newly created RX/TX interfaces.
- **CRUD Operations**: Create, read, update, and delete interface relationships easily.
- **Integration with NetBox UI**: Accessible through the NetBox main menu, enabling quick splitting and review of existing relationships.

## Requirements
These are the versions of NetBox and Python tested with the plugin. It is recommended to use these versions (or as close as possible) to avoid incompatibilities.

- **NetBox** NetBox Community `v4.1.6` (2024-10-31)
- **Python** version `3.10.12` or higher

## Installation
The plugin is available on PyPI, so you can install it easily with pip.

### Step 1: Install using pip
```bash
pip install interface_relationship_manager
```

### Step 2: Add the plugin into PLUGINS array in configuration.py
```bash
PLUGINS = [
    'interface_relationship_manager',
    # Other plugins...
]
```
### Step 3: Apply migrations(don't forget activating virtual enviroment)
```bash
python manage.py migrate interface_relationship_manager
```
### Step 4: Run netbox(for example)
```bash
python manage.py runserver
```

## Usage
### Splitting an Interface
1. Open the Interface Splitting Manager page from the plugin menu or go to the device you want to manage.

2. Choose the device that contains the interface you want to split.

3. Select the interface.

4. Click Split Interface.

5. The plugin will create two new interfaces, interface_name_rx and interface_name_tx, and establish a relationship with the main interface.
or

After splitting:
- The plugin automatically links main_interface to its rx_interface and tx_interface.
- Any future UI or API calls can show these relationships for easy management.

## Project Structure
```
interface_splitting_manager/
├── models.py                    # InterfaceRelationship model definition
├── views.py                     # Views for selecting device and splitting interfaces
├── forms.py                     # Forms to handle user input
├── templates/                   # HTML templates
├── urls.py                      # Plugin URLs
├── navigation.py                # Plugin menu entries
└── migrations/                  # DB migrations
```

## Changelog
### v1.3.1
- added headers into each file

### v1.3
- actually added template - wrong name in toml file

### v1.2
- added template that i forgot to upload 

### v1.1
- fixed README

### v1.0
- Initial release with basic interface splitting and relationship tracking.
- Created a dedicated InterfaceRelationship model to keep track of main, RX, and TX interfaces.
- Added a management UI for selecting interfaces and performing splits.
- Improved error handling and user feedback in the UI.


## Notes
- No core override: The plugin doesn't override NetBox's core behavior. It only adds new features related to interface splitting.

- Relationships: When an interface is split, the original interface remains available as the main interface, and the two new interfaces (RX and TX) are each associated with the main interface through the InterfaceRelationship model.

- Custom Buttons: To add custom buttons or links in various NetBox UI areas, you can:
    - Edit NetBox core templates (not recommended, as changes can be lost during upgrades),
    - Use NetBox's built-in Custom Links feature,
    - Or override specific templates if needed (though results may vary).

## Author
Viktor Kubec  
BUT FIT Brno student  
MIT License  
GitHub: [vubeckubec/interface_relationship_manager](https://github.com/vubeckubec/interface_relationship_manager)
