# robotframework-MarcinKoperski
Bundle containg all useful libraries that are used by me and my projects

require to install and use all capacities install
http://www.imagemagick.org/script/binary-releases.php
and add system variable "MAGICK_HOME"
Microsoft Visual C++ Compiler for Python 2.7
http://www.microsoft.com/en-us/download/details.aspx?id=44266  (location of VCForPython27.msi)

To use it add "TestToolsMK" to Library 

best way to setup is to using https://chocolatey.org/
choco install python2
choco install pip
choco install imagemagick.tool
VCForPython27.msi
setx MAGICK_HOME "C:\ProgramData\chocolatey\lib\imagemagick.tool\tools"

pip install robotframework
pip install robotframework-MarcinKoperski


to install latest
pip install --upgrade https://github.com/IlfirinPL/robotframework-MarcinKoperski/archive/master.zip
