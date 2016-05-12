# robotframework-MarcinKoperski


.. image:: https://travis-ci.org/IlfirinPL/robotframework-MarcinKoperski.png
    :target: https://travis-ci.org/IlfirinPL/robotframework-MarcinKoperski

.. image:: https://img.shields.io/pypi/v/robotframework-MarcinKoperski.svg
    :target: https://pypi.python.org/pypi/robotframework-MarcinKoperski

.. image:: https://img.shields.io/pypi/dm/robotframework-MarcinKoperski.svg
    :target: https://pypi.python.org/pypi/robotframework-MarcinKoperski

.. image:: https://img.shields.io/pypi/l/robotframework-MarcinKoperski.svg


Bundle contains all useful libraries that are used by me in my projects
[Keywords documentation](http://htmlpreview.github.io/?https://github.com/IlfirinPL/robotframework-MarcinKoperski/blob/master/doc/TestToolsMK.html) 





## Example 
To use it add Library "TestToolsMK" to your robotframework projects


```
*** Settings ***
Documentation       This test show how to create delta gif and evalute if screenshot are similar
Library             TestToolsMK
Library             Selenium2Library
Library             Collections

*** Test Cases ***
Example
      Image Self Check
      Open Browser Extension      https://www.google.com/search?hl=en&q=test      browser=ff      width=1366      height=768      x=0      y=0
      ${path1}      Capture Page Screenshot Extension
      Go To Smart      https://www.google.com/search?hl=en&q=testX
      ${path2}      Capture Page Screenshot Extension
      Comment      Show list of screenshot taken during test
      Log List      ${list of screenshots}
      ${delta value}      Image Should Be Difference Less Then      ${path1}      ${path2}      difference_percent=2      embedded_gif=True
      [Teardown]      Close All Browsers


```

## Prerequisites to install

* [Microsoft Visual C++ Compiler for Python 2.7] (http://www.microsoft.com/en-us/download/details.aspx?id=44266 ) //for windows
* [Chocolatey](https://chocolatey.org/) //for windows
* Python 2.7.X  https://www.python.org/downloads/ //for windows


## Installation 

best way to setup is to use following commands , skip steps that you already have

windows
```
choco install pip
choco install imagemagick.tool
setx MAGICK_HOME "C:\ProgramData\chocolatey\lib\imagemagick.tool\tools"

pip install robotframework
pip install robotframework-MarcinKoperski
```

linux
```
sudo apt-get install imagemagick
sudo pip install robotframework
sudo pip install robotframework-MarcinKoperski
```

to update 
```
pip install -U robotframework-MarcinKoperski
```

to install from sources may install unstable release

```
pip install --upgrade https://github.com/IlfirinPL/robotframework-MarcinKoperski/archive/master.zip
```
