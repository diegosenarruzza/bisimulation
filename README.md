# bisimulation


## Installation

This was executed using python *3.6.5* in a virtualenv environment.

- Install https://github.com/pyenv/pyenv-virtualenv, a plugin for pyenv.

To create virtualenv with libraries:
  ```sh
    pyenv install 3.6.5
    pyenv virtualenv 3.6.5 bisimulation
    pyenv activate bisimulation
    pip install -r requirements.txt
  ```

Assuming pip is installed.

As there is an ".python-version" file with this virtualenv, it will be automatically activated when cd in to directory.