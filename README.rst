robotframework-MarcinKoperski
===============
library for Robot Framework


.. image:: https://img.shields.io/pypi/v/robotframework-MarcinKoperski.svg
    :target: https://pypi.python.org/pypi/robotframework-MarcinKoperski

.. image:: https://img.shields.io/pypi/l/robotframework-MarcinKoperski.svg
    :target: http://www.gnu.org/licenses/mit.html

.. contents::
   :local:

News/Changelog
------------
* Get File PDF - read pdf file content
* better support python3 add automatic test in github, also automatic release in https://pypi.org



=================================================

Introduction
------------
Robot framework is great tools but there is always some functions that were missing, to solve it issues this library were created.
Also to make environment more consistent.


Keyword documentation
---------------------
Link to `Keyword Documentation`_

.. _`Keyword Documentation`: http://ilfirinpl.github.io/robotframework-MarcinKoperski/doc/TestToolsMK.html

Example 
------------

To use it add Library "TestToolsMK" to your robotframework projects


.. code:: robotframework

	*** Settings ***
	Documentation       This test show how to create delta gif and evalute if screenshot are similar
	Library             TestToolsMK
	Library             Selenium2Library
	Library             Collections

	*** Test Cases ***
	Example Test
		Image Self Check
		Open Browser Extension      https://www.google.com/search?hl=en&q=test      browser=ff      width=1366      height=768      x=0      y=0
		${path1}      Capture Page Screenshot Extension
		Go To Smart      https://www.google.com/search?hl=en&q=testX
		${path2}      Capture Page Screenshot Extension
		Comment      Show list of screenshot taken during test
		Log List      ${list of screenshots}
		${delta value}      Image Should Be Difference Less Then      ${path1}      ${path2}      difference_percent=2     embedded_gif=True
		[Teardown]      Close All Browsers


Prerequisites
-------------
- `Microsoft Visual C++ Compiler for Python 3.X`__
- `Chocolatey`__ // for windows only
- Python 3.6,3.7,3.8  // tested on linux


__ http://www.microsoft.com/en-us/download/details.aspx?id=44266
__ https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15
__ https://chocolatey.org/
__ https://www.python.org/downloads

Installation or Update
------------

Best way to setup is to use following commands , skip steps that you already have

windows
::
	choco install pip
	choco install imagemagick.tool
	setx MAGICK_HOME "C:\ProgramData\chocolatey\lib\imagemagick.tool\tools"

	pip install -U robotframework-MarcinKoperski


linux
::
	sudo apt-get install imagemagick
	sudo pip install -U robotframework-MarcinKoperski

RIDE for python 3
::
	py -m pip install -U git+https://github.com/robotframework/RIDE.git
