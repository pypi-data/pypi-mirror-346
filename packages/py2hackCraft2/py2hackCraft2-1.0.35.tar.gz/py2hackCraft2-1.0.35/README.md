setup:
    <command>
    pip install setuptools wheel twine

build:
    <command>
    rm -rf build/ dist/ *.egg-info
    python3 setup.py sdist bdist_wheel

deploy:
    <command>
    twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u "__token__"

doc:
    <command>
    make html