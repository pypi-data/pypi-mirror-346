# uipathlib

* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [License](#license)

## Package Description

UiPath Cloud client Python package that uses the [requests](https://pypi.org/project/requests/) library.

> [!IMPORTANT]
> This packages uses pydantic~=1.0!

## Usage

* [uipathlib](#uipathlib)

from a script:

```python
import uipathlib
```

## Installation

* [uipathlib](#uipathlib)

Install python and pip if you have not already.

Then run:

```bash
pip3 install pip --upgrade
pip3 install wheel
```

For production:

```bash
pip3 install uipathlib
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:

```bash
git clone https://github.com/aghuttun/uipathlib.git
cd uipathlib
pip3 install -e .[dev]
```

To test the development package: [Testing](#testing)

## License

* [uipathlib](#uipathlib)

BSD License (see license file)
