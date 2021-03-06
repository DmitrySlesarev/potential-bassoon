# -*- coding: utf-8 -*-

"""
The Program is to speed up verifying compliance with RFC 3261.  
The applied concepts are taken from free access, no paid content.  
All the conditions are in accordance with Russian Networks. If   
intend to use it in different country, code inspection is needed.  
"""

import re
from sys import argv
from sys import exit
from os.path import exists

# Windows10 doesn't support colors for console by default.  
# Thus you need to enable them. The code is about that. 
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Importing the module to compare SIP files
import difflib

# There is no inheritance since the class is based on an object.  
class Decoration:
    """The class is for design of other classes."""  

    def start(self, func):
        """The method adds frame with '=' at the beginning."""  
        print(('{red}={endcolor}'*20).format(red='\033[31m', endcolor='\033[0m'))
        print(func.upper())
        print(('{red}={endcolor}'*20).format(red='\033[31m', endcolor='\033[0m'))

    def finish(self):
        """The method adds frame with '=' at the end"""  
        print(('{red}-{endcolor}'*20).format(red='\033[31m', endcolor='\033[0m'))
        print("FINISHED\n")


class Entry_point(Decoration):
    """The class initiates work with input."""  
    
    def __init__(self):
        """The method provides information about license."""  
        print("""\n{gray}Copyright 2020 Dmitry Slesarev @ Sony Mobile Communications.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.{endcolor}\n""".format(gray='\033[37m', endcolor='\033[0m'))
        
        with open('LICENSE.txt', 'r') as l:
            file = str(l.read())
        print("Do you want to read the License? {red}Y/N{endcolor}".format(red='\033[31m', endcolor='\033[0m'))
        decision = str(input("> "))
        if "y" == decision or "Y" == decision:
            print(file)
        else:
            pass

    def enter(self):
        """The method requires name of the file to open."""  
        print("""Put file of .txt format into the directory \
and enter its name here:""")
        name_of_file = str(input("> "))
        with open(name_of_file, "r+") as f:
            message = str(f.read())
        return message

    def processing_file(self):
        """The method handles content of the file."""  
        while True:
            try:
                message = self.enter()
                self.start("STARTING ANALYSIS")
                print(message)
                break
            except NameError as ex:
                print("Caught the EOF error:{0}".format(ex))
                print("Wrong name. Let's try again.")		
                continue
            except EOFError as ex:
                print("Caught the EOF error:{0}".format(ex))
                print("Wrong name. Let's try again.")
                continue
            except IOError as ex:
                print("Caught the I/O error:{0}".format(ex))
                print("Wrong name. Let's try again.")
                continue	
        return message        


class Options(Entry_point):
    """The class provides options for handling the content."""  

    def header_verification(self, arg):
        """The method checks if the headers comply RFC 3261."""  
        self.arg = arg
         
        headers_list = {
            'via' : 'Via',
            'max_forwards' : 'Max-Forwards',
            'to' : 'To',
            'from' : 'From',
            'call_id' : 'Call-ID',
            'cseq' : 'CSeq',
            }

        headers_invite = headers_list.copy()
        headers_invite['contact'] = 'Contact'

        self.start("Headers check:")
        if re.search('INVITE', self.arg):
            for key in headers_invite:
                if re.search(headers_invite[key], self.arg):
                    print(key.upper(), True)
                else:
                    print(headers_invite[key].upper(), False)	
        else:
            for key in headers_list:
                if re.search(headers_list[key], self.arg):
                    print(key.upper(), True)
                else:
                    print(headers_list[key], False)
        self.finish()


    def client_verification(self, arg):
        """The method verifies errors of client for SIP message."""  
        self.arg = arg        

        client_errors = {
            'bad_request' : '(400)',
            'unathorized' : '(401)',
            'forbidden' : '(403)',
            'not_found' : '(404)',
            'proxy_authentication_required' : '(407)',
            'request_timeout' : '(408)',
            'temporary_unavailable' : '(480)',
            'call_or_transaction_does_not_exist' : '(481)',
            'busy_here' : '(486)',
            'request_terminated' : '(487)',
            }

        self.start("Errors of Client:")
        for key in client_errors:
                if re.search(client_errors[key], self.arg):
                    print(key.upper(), True)
                else:
                    print(client_errors[key].upper(), False)
        self.finish()


    def server_verification(self, arg):
        """The method checks if there are any Server Errors."""  
        self.arg = arg

        server_errors = {
            'bad_gateway' : '(502)',
            'service_unavailable' : '(503)',
            }

        self.start("Server errors:")
        for key in server_errors:
            if re.search(server_errors[key], self.arg):
                print(key.upper(), True)
            else:
                print(server_errors[key].upper(), False)
        self.finish()


    def global_errors_verification(self, arg):
        """The method checks if there are any Global Errors."""  
        self.arg = arg

        global_errors = {
            'busy_everywhere' : '(600)', 
            'decline' : '(603)',
        }

        self.start("Global errors:")
        for key in global_errors:
            if re.search(global_errors[key], self.arg):
                print(key.upper(), True)
            else:
                print(global_errors[key].upper(), False)	
        self.finish()


    def phone_context_verification(self, arg):
        """The method checks the phone-context attribute."""  
        self.arg = arg

        self.start("Phone context check:")
        
        phone_context = [
            '.i-wlan.ims.mnc',
            ]
        for i in phone_context:
            if i in self.arg:
                print("""In accordance with Megafon NW requirements, 
                     the FQDN cannot have WiFi MAC address & i-wlan string.\n
                     PROHIBITED:\n
                     INVITE sip:89262000099;phone-context=d460e3ed8420.i-wlan.ims.mnc002.mcc250.3gppnetwork.org@ims.mnc002.mcc250.3gppnetwork.org;user=phone SIP/2.0\n
                     REQUIRED:\n
                     phone-context=ims.mnc002.mcc250.3gppnetwork.org@ims.mnc002.mcc250.3gppnetwork.org\n
                     Please, comply.""")
            else:
                print("Phone context matches the requirements")
        self.finish()


    def crosscheck(self, arg):
        """The method doesn't comply PEP8 for purpose."""  
        self.arg = arg

        self.start("Crosscheck:")
        print('Complies RFC 3261') if re.search('z9hG4bK', self.arg) else print('Doesn\'t comply RFC 3261')
        print('GEO PIDF is present') if re.search('<gml:pos>', self.arg) else print('Doesn\'t comply AOSA')
        print('EVS is allowed') if re.search('EVS', self.arg) else print('No EVS codec')
        print('SDP is checked') if re.search('sendrecv', self.arg) else print('Check SDP: no bilateral voice')
        print('P-Early-Media:supported') if re.search('P-Early-Media: supported', self.arg) else print('P-Early-Media: NOT supported')
        print('P-Access-Network-Info: IEEE-802.11') if re.search('P-Access-Network-Info: IEEE-802.11', self.arg) else print('No VoWiFi PANI')
        print('Cellular-Network-Info: 3GPP-E-UTRAN') if re.search('Cellular-Network-Info: 3GPP-E-UTRAN', self.arg) else print('No CNI for VoWiFi')
        self.finish()

    def compare_files(self):
        """The method to compare two files i.g.
        the current file with reference"""
        print("Enter the full path for the file #1")
        file1 = str(input("> "))

        print("Enter the full path for the file #2")
        file2 = str(input("> "))

        with open(file1, 'r') as f1:
            text1 = f1.read()

        with open(file2, 'r') as f2:
            text2 = f2.read()

        file1_split = text1.splitlines()
        file2_split = text2.splitlines()

        diff = difflib.Differ().compare(file1_split, file2_split)
        for i in diff:
            print(i)

        x = 'DONE.\n'
        print("\033[31m {} \033[0m".format(x))

    def reference(self):
        """The method's still vague."""  
        print("\aUNDER CONSTRUCTION!!!")

class Action(Options):
    """The class defines the menu."""  

    def action_points(self):
        """The method defines options of choice."""  
        list_of_functions = {
            'header_verification' : 'Header verification',
            'client_verification' : 'Client Errors verification',
            'server_verification' : 'Server Errors verification',
            'global_errors_verification' : 'Global Errors verification',
            'phone_context': 'Attribute verification',
            'crosshcheck' : 'Crosscheck',
            'all' : 'All above mentioned items',
            'compare': 'Compare two SIP files',
            'exit' : 'EXIT',
            }

        argument = self.processing_file()

        while True:
            self.start("Available options:")
            index = 1
            for key in list_of_functions:
                print("{}.".format(index), list_of_functions[key])
                index+=1
            print("\nEnter any number from the options:")
        
            next = int(input(">"))
            '''
            assert type(next) != str, "Should be int"   
            assert type(next) != float, "Should be int"  
            assert type(next) != bool, "Should be int"  
            assert type(next) != None, "Should not be empty"  
            '''
            try:
                if next == int(1): self.header_verification(argument)
                if next == int(2): self.client_verification(argument)
                if next == int(3): self.server_verification(argument)
                if next == int(4): self.global_errors_verification(argument)
                if next == int(5): self.phone_context_verification(argument)
                if next == int(6): self.crosscheck(argument)
                if next == int(7):
                    self.header_verification(argument)
                    self.client_verification(argument)
                    self.server_verification(argument)
                    self.global_errors_verification(argument)
                    self.phone_context_verification(argument)
                    self.crosscheck(argument)
                if next == int(8): self.compare_files()
                if next == int(9): exit(1)
                if next >= int(10): self.reference()                
            except Exception as ex:
                print("The input contains wrong symbol(s):{}".format(ex))
                print("Please, try again.")    

# The common entry point.  
if __name__ == "__main__":
    new = Action()
    new.action_points()
