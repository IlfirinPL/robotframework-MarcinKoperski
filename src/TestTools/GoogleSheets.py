#  Copyright (c) 2015 Cutting Edge QA

import json
import gspread
import re

from oauth2client.client import SignedJwtAssertionCredentials

class GoogleSheets:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def __init__(self, file='Resources/googlesheet-key.json', id='1RBVyDC-HrUc5Ct0gHU0mlkfhHErmdPz0DJJgGT_XQ_Y'):
         json_key = json.load(open(file))
         scope = ['https://spreadsheets.google.com/feeds']
         credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
         gc = gspread.authorize(credentials)
         sht1 = gc.open_by_key(id)
         self.ACCOUNTS_TAB = sht1.worksheet("Accounts")
         self.login_list = self.ACCOUNTS_TAB.col_values(1)
         self.password_list = self.ACCOUNTS_TAB.col_values(2)
         self.dictionary = dict(zip(self.login_list, self.password_list))
    
    def get_dictonary_logins_and_passwords(self):
        return self.dictionary
    def get_password_for_login(self,login):
       """Return password for provided login, rise error when login is missing"""
       return self.dictionary[login] 
    def find_cell_using_regex(self,regex):
       """Return password for provided login, rise error when login is missing"""
       pattern = r'%s' % regex
       print pattern
       amount_re = re.compile(pattern)
       return self.ACCOUNTS_TAB.find(amount_re)
    def find_all_cell_using_regex(self,regex):
       """Return password for provided login, rise error when login is missing"""
       pattern = r'%s' % regex
       print pattern
       amount_re = re.compile(pattern)
       return self.ACCOUNTS_TAB.findall(amount_re)
