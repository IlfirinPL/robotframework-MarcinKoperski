#!/usr/bin/env bash

wget -N http://chromedriver.storage.googleapis.com/LATEST_RELEASE
lastbuild=`cat LATEST_RELEASE`

wget -N http://chromedriver.storage.googleapis.com/$lastbuild/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

rm LATEST_RELEASE
rm chromedriver_linux64.zip
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -f -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -f -s /usr/local/share/chromedriver /usr/bin/chromedriver