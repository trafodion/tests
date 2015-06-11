# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

from ...lib import hpdci
import defs
import basic_defs
import unittest
import time

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()


def testa01(desc="""piv_name below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """register component user1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create component privilege created as \'cr\' on user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	

    stmt = """create component privilege abcd as \'ac\' on user1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege dropped as \'dr\' on user1 detail \'drop users privileges\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege added as \'ad\' on user1 detail \'add users privileges\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege wertfg  as \'we\' on user1 detail \'add users privileges\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister component user1 cascade ;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  


def testa02(desc="""priv_name blank, out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """register component user2;"""
    output = _dci.cmdexec(stmt)
 
    #blank
    stmt = """create component privilege  as \'cr\' on user2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    #max+n
    stmt = """create component privilege qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 as \'pa\' on user2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
                
    stmt = """unregister component user2 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
                

def testa03(desc="""priv_name valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """register component user3;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on user3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on user3 detail \'update users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege deleted as \'de\' on user3 detail \'delete users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege adcd as \'ad\' on user3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component user3 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  



def testa04(desc="""priv_name invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component user4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create component privilege "test" as \'t\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create  component privilege  "1289-_@" as \'1\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create  component privilege  "_asdf" as \'as\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    stmt = """create component privilege "/test" as \'/t\' on user4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """unregister component user4 cascade;"""
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  


def testa05(desc=""" priv_abbr 1 or 2 character"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component user5;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on user5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """create component privilege updated as \'up\' on user5  detail \'update users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """create component privilege aaaa as \'a4\' on user5  detail \'update users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege aabb as \'ab\' on user5  detail \'update users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component user5 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa06(desc="""priv_abbr in not 1 or 2 character , invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component user6;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'create\' on user6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3301')
    
    stmt = """create component privilege updated as \'\' on user6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')

    stmt = """create component privilege abcd as \'abcd\' on user6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3301')
    
    stmt = """create component privilege abcd as \'_\' on user6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create component privilege abcd as \'_1\' on user6;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'15001')
    _dci.expect_complete_msg(output)

    stmt = """create component privilege abcd as \'1_\' on user6;;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output,'15001')
    _dci.expect_error_msg(output,'1357')
	
    stmt = """create component privilege "123_" as \'1_\' on user6;"""
    output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output, '15001')
    _dci.expect_complete_msg(output)
	
    stmt = """create component privilege "^123_" as \'1/\' on user6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister component user6 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
           
  
def testa07(desc="""missing, invaild keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component user7;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privileges created as \'cd\' on user7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create component privilege created as \'cd\' on user7 details \'create users;\'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create component privilege created  on user7 ; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create component privilege created  system on user7 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create component privilege created as \'cd\' on user7 details \'create users;\'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create component privilege create   as \'cr\' system detail \'create users;\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = """unregister component user7 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  


def testa08(desc="""priv_name exists in same/different component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component user81;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component user82;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on user81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    stmt = """create component privilege dropped as \'dr\' on user81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege created as \'ce\' on user81; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1357')
    
    stmt = """create component privilege created as \'ce\' on user82; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege dropped as \'dr\' on user82; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component user81 cascade;"""
    output = _dci.cmdexec(stmt)    
    
    stmt = """unregister component user82 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  



def testa09(desc="""priv_abb exists in same/different component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component user91;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component user92;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on user91; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege dropped as \'dr\' on user91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege dropped as \'cr\' on user91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1357')
    
    stmt = """create component privilege create1 as \'cr\' on user91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1356')
    
    stmt = """create component privilege created as \'cr\' on user92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege dropped as \'CR\' on user92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1356')
    
    stmt = """create component privilege dropped as \'dr\' on user92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component user91 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component user92 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    _testmgr.testcase_end(desc)  



def testa10(desc="""component name does not exist"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component user101;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component user102;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister component user102;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on user10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    
    stmt = """create component privilege created as \'cr\' on user101; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege created as \'cr\' on user102; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    stmt = """unregister component user101 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege created as \'cr\' on user101;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    _testmgr.testcase_end(desc)  



def testa11(desc="""ordinary user create component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
   
    stmt = """register component user11;"""
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()      
    stmt = """create component privilege created as \'cr\' on user11;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

    _testmgr.testcase_end(desc)  


def testa12(desc="""ordinary user with admin privilege create component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component user12;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """grant role DB__rootrole to  qauser_tsang;"""
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()  
    stmt = """create component privilege created as \'cr\' on user12;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
           
    stmt = """unregister component user12 cascade;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """revoke role DB__rootrole from  qauser_tsang;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
           

def testa13(desc="""after dropping component privilege ,then create again"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component user13;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on user13; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege dropped as \'dr\' on user13; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    
    stmt = """drop component privilege created on user13 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop component privilege dropped  on user13 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege dropped as \'cr\' on user13; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege created as \'dr\' on user13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
    stmt = """unregister component user13 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa14(desc="""cleanup"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister component user13 cascade;;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user12 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user11 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user101 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user102 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user91 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user92 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user81 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user7 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component user6 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user5 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user4 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component user3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component user2 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component user1 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)   

