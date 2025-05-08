## python package publishing from
https://www.youtube.com/watch?v=Kz6IlDCyOUY&t=4s

## Commands so far
```
conda create -n qiskit_noise_analysis
conda activate qiskit_noise_analysis
conda install python 

pip install setuptools wheel twine

# create necessary files for package + setup.py file

# to create the package
python setup.py sdist bdist_wheel

# testing locally
pip install dist/qiskit_noise_analysis-0.1-py3-none-any.whl

# uploading to pypi
twine upload dist/*
```


## Packages untill now:
- python 3.13.2
- pip 25.1



## Folder setup

qiskit_noise_analysis
|---qiskit_noise_analysis
|    |--- __init__.py
|    |___ main.py
|---setup.py
|---README.py