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
* Image processing is using PILLOW instead of Image Magick ( all dependenices with choco removed)
* Remove Support for Python 2.7
* Remove Keywords that are better supported via RPAFramework
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
	Library             SeleniumLibrary
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
- Python 3.9  // tested on linux

__ https://www.python.org/downloads

Installation or Update
------------

Best way to setup is to use following commands , skip steps that you already have

windows
::
	pip install -U robotframework-MarcinKoperski

linux
::
	sudo pip install -U robotframework-MarcinKoperski
