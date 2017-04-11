# algos-redfams
Second pass at Reddit Families project for Algorithms class

## Installation
Make sure python3.5 and virtualenv are installed on your system
Make sure postgresql is installed and is accepting connections on port 5432.

Run the following commands from the root directory (using the Windows equivalent where applicable):

1. `virtualenv -p $(which python3.5) reddit-venv --no-site-packages`
2. `source reddit-venv/bin/activate`
3. `pip install -r requirements.txt`
4. To deactivate the virtualenv, `deactivate`.
