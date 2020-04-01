#!/bin/bash
find . -type f \( -name "*.py" ! -name "test*.py" \) | xargs pylint3
python3 -m venv env
source env/bin/activate
pip3 install -r python_dependencies.txt
coverage run -m --branch unittest discover -p test*.py -v
if [ $? -eq 0 ]
then
    coverage report -m --omit */env/*,*/__init__.py,*/test_*.py
else
    coverage report -m --omit */env/*,*/__init__.py,*/test_*.py
    exit 1
fi
mypy .
