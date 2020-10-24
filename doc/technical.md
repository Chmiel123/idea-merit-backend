# Technical documentation

## Miscellanous folders

### `doc`

Documentation, manuals, help documents

### `tmp`

Generated files etc.

## Source folders

### `config`

Configuration parser and config files in yaml

### `model`

Data objects, direct access and manipulation of database.
Each subfolder is a different schema in the database.

### `logic`

One step above model. Manipulates models. Does not use the database directly.
Raises IMExceptions.

### `resources`

Flask resources. Uses logic files. Catches exceptions and returns standardized messages.

### `test`

Unit tests, tests above three layers.

### `util`

Miscellanous classes and utilities.
