#!/bin/bash
source .venv/bin/activate
for i in pip hatch build; do
    pip install --upgrade $i
done
python3 -m build .

