set PY_PYTHON=3 
py -m pip install -U pip wheel pywin32 setuptools
py -m pip install -U -r https://raw.githubusercontent.com/IlfirinPL/robotframework-MarcinKoperski/master/requirements.txt
py -m pip install -U git+https://github.com/IlfirinPL/robotframework-MarcinKoperski.git
py -m pip install -U git+https://github.com/robotframework/RIDE.git
py -m robot --version
