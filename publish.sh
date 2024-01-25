rm dist/*
python3 -m build --sdist
twine check dist/*
twine upload dist/*
