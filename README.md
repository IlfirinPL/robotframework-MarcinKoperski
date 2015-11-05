# robotframework-MarcinKoperski

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

* [Microsoft Visual C++ Compiler for Python 2.7] (http://www.microsoft.com/en-us/download/details.aspx?id=44266 )
* [Chocolatey](https://chocolatey.org/)



## Installation 

best way to setup is to use following commands , skip steps that you already have

```
choco install python2
choco install pip
choco install imagemagick.tool
setx MAGICK_HOME "C:\ProgramData\chocolatey\lib\imagemagick.tool\tools"

pip install robotframework
pip install robotframework-MarcinKoperski
```

to install latest

```
pip install --upgrade https://github.com/IlfirinPL/robotframework-MarcinKoperski/archive/master.zip
```
