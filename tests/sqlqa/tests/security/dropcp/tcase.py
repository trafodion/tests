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
    
    stmt = """register component users1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create component privilege created as \'cr\' on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	

    stmt = """create component privilege abcd as \'a\' on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')

    stmt = """create component privilege dropped as \'dr\' on users1 system detail \'drop users privileges\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1221')

    stmt = """create component privilege added as \'ad\' on users1 detail \'add users privileges\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create component privilege wertfg  as \'we\' on users1 detail \'add users privileges\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""drop component privilege created on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""drop component privilege abcd on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

	
    stmt="""drop component privilege dropped on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt="""drop component privilege added on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""drop  component privilege wertfg on users1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	

    stmt = """unregister component users1 cascade ;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  


def testa02(desc="""priv_name blank, out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """register component users2;"""
    output = _dci.cmdexec(stmt)
 
    #blank
    stmt = """create component privilege  as \'cr\' on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt='create component privilege " "  as \'cr\' on users2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    #max+n
    stmt = """create component privilege qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 as \'pa\' on user2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
	
    stmt = """create component privilege qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567131 as \'pb\' on users2 system detail \'create privilege on users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
	
	
    stmt="""drop component privilege on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt="""drop component privilege " "  on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt="""drop component privilege a921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130  on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
	
	
	
    stmt="""drop  component privilege qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567131  on users2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
	
                
    stmt = """unregister component users2 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
                

def testa03(desc="""priv_name valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """register component users3;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cr\' on users3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on users3 detail \'update users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege deleted as \'de\' on users3 detail \'delete users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege adcd as \'ad\' on users3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
	
    stmt = """drop component privilege created on users3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt = """drop component privilege updated on users3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop component privilege deleted on users3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop component privilege adcd  on users3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)		
	
    
    stmt = """unregister component users3 cascade;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  



def testa04(desc="""priv_name invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component users4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create component privilege "test" as \'t\' on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create  component privilege  "1289-_@" as \'1\' on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1220')
    
    stmt = """create  component privilege  "_asdf" as \'as\' on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    stmt = """create component privilege "/test" as \'/t\' on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	

    stmt = """drop component privilege "test" on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	

    stmt = """drop component privilege  "1289-_@" on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	

    stmt = """drop component privilege  "_asdf"  on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """drop component privilege "/test" on users4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """unregister component users4 cascade;"""
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  


def testa05(desc="""missing, invaild keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component users5;"""
    output = _dci.cmdexec(stmt)

    stmt = """create privilege create as \'cd\' on users5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """drop privilege create on users5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """create component privilege created as \'cd\' on users5 details \'create users\'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop component privilege created as \'cd\' on users5 details \'create users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """create component privilege created as \'cd\' on users5 detail \'create users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop component privilege created as \'cd\' on users5 detail \'create users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt="""create component privilege created as \'cr\' on users5 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1357')	

    stmt = """drop component privilege created ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')	
	
    stmt = """drop component privilege created on users5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """create component privilege created as \'cd\' on users5 detail \'create users\'; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """drop component privilege created as \'cd\' on users5 detail \'create users\' system;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')	
	
    stmt = """create component privilege created   as \'c\' system detail \'create users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')	
	
    stmt = """drop component privilege created as \'cr\' on system detail \'create users\';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')		
    
    stmt = """unregister component users5 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa06(desc="""priv_name exists and doesn't exist component"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component users61;"""
    output = _dci.cmdexec(stmt)

    stmt = """register component users62;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'cd\' on users61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege dropped as \'cd\' on users61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1356')

    stmt = """create component privilege updated as \'up\' on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege deleted as \'cd\' on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop component privilege created  on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'1004')

    stmt = """drop component privilege created  on users61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """drop component privilege dropped on users61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    stmt = """drop component privilege \'cd\' on users61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """drop component privilege updated on users61;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')

    stmt = """drop component privilege \'cd\' on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
	
    stmt = """drop component privilege deleted on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """drop component privilege \'up\' on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
	
    stmt = """drop component privilege updated on users62;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt = """unregister component users61 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister component users62 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
           
  
def testa07(desc="""drop component privilege on non-existing name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component users71;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """register component users72;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """unregister component users72;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'ca\' on users71;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on users71 system; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1221')
    
    stmt = """drop component privilege created on users72; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    
    stmt = """drop component privilege updated on users73;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    
    stmt = """unregister component users71 cascade; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop component privilege created on users71 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
        
    stmt = """drop component privilege updated on users71 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
	
    _testmgr.testcase_end(desc)  


def testa08(desc="""ordinary user drop component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """register component users8;"""
    output = _dci.cmdexec(stmt)


    stmt = """create component privilege created as \'ca\' on users8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt = """create component privilege updated as \'up\' on users8;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop component privilege created on users8 cascade; """
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    stmt = """drop component privilege updated on users8 restrict; """
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1004')
    
    stmt = """drop component privilege created on users8 restrict; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component users8 cascade;"""
    output = _dci.cmdexec(stmt)    
    
    _testmgr.testcase_end(desc)  


def testa09(desc="""ordinary user with admin privilege drop component privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component users9;"""
    output = _dci.cmdexec(stmt)

    stmt = """create component privilege created as \'ca\' on users9; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on users9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role db__rootrole to qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)	
	
    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt = """drop component privilege updated on users9 cascade;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
    
    
    stmt = """drop component privilege created on users9 restrict;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1017')
    mydci.expect_complete_msg(output)
    
    
    stmt = """revoke role db__rootrole from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister component users9 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  



def testa10(desc="""grant privilege to users and roles, then drop component privilege cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component users10;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create role a10role1;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege created as \'ca\' on users10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create component privilege updated as \'up\' on users10; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant component privilege created ,updated on users10 to qauser_tsang with grant option; """
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt = """grant component privilege created on users10 to qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
	
    stmt="""grant component privilege updated on users10 to a10role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)	
	
    stmt="""drop component privilege updated on users10 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')
    	
    stmt="""drop component privilege created on users10 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   

    stmt="""drop component privilege updated on users10 cascade;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)	
	
    stmt="""drop component privilege created on users10 cascade;"""
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)	

    stmt = """unregister component users10 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt = """drop role a10role1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa11(desc="""grant privilege to users and roles, then drop component privilege restrict"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
   
    stmt = """register component users11;"""
    output = _dci.cmdexec(stmt)
	
    stmt='create role a11role1;'
    output = _dci.cmdexec(stmt)

    stmt="""create component privilege created as \'ca\' on users11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""create component privilege updated as \'up\' on users11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""grant component privilege created ,updated on users11 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt = """grant component privilege created on users11 to qauser_sqlqaa;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
	
    stmt="""grant component privilege updated, created on users11 to a11role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt="""drop component privilege updated on users11 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   
	
    stmt="""drop component privilege created on users11 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   
	
    stmt="""revoke component privilege created on users11 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""drop component privilege created on users11 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   
	
    stmt="""revoke component privilege created on users11 from a11role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
	
	
    stmt="""drop component privilege created on users11 restrcit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
	
    stmt="""drop component privilege updated on users11 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   

	
    stmt="""revoke component privilege updated on users11 from a11role1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt="""revoke component privilege updated on users11 from qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt="""drop component privilege updated on users11 restrcit;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt="""unregister component users11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt="""drop role a11role1;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  


def testa12(desc="""drop component privilege restrict mix with granted  and ungranted priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register component users12;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create role a12role1;"""
    output = _dci.cmdexec(stmt)
	
    stmt = """create component privilege created as \'ca\' on users12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """create component privilege updated as \'up\' on users12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
           
    stmt = """grant component privilege created ,updated on users12 to qauser_tsang with grant option;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    mydci = basic_defs.switch_session_qi_user2()  
	
    stmt = """grant component privilege created ,updated on users12 to a12role1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
	
           
    stmt = """grant component privilege updated on users12 to qauser_sqlqaa;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """revoke component privilege updated on users12 from qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt = """drop component privilege updated on users12 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   
	
    stmt = """revoke component privilege updated on users12 from qauser_sqlqaa ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt = """drop component privilege updated on users12 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt = """revoke grant option for component privilege created on users12 from  qauser_tsang;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025')   
	
    stmt = """drop component privilege created on users12 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1025') 
	
    stmt = """revoke  grant option for  component privilege created on users12 from  qauser_tsang cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
	
    stmt = """drop component privilege created  on users12 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
	
    stmt="""unregister component users12 cascade;"""
    output = _dci.cmdexec(stmt)

    stmt="""drop role a12role1;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)  

def testa13(desc="""cleanup"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister component users12 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role a12role1;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users11 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role a11role1;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users10 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role a10role1;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users9 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users8 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users71 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component users72 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users61 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users62 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component users5 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users4 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component users3 cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister component users2 cascade;"""
    output = _dci.cmdexec(stmt)    
    stmt = """unregister component users1 cascade;"""
    output = _dci.cmdexec(stmt)
	
    _testmgr.testcase_end(desc)   

