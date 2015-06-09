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
from ...lib import gvars
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


def testa01(desc="""vary ordering of clauses, misspell keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    
    stmt = 'register user qauser41 as qauser41;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt = 'unregister qauser41 user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
   
    stmt = 'unregister user qauser41 as qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = 'unregister user qauser41 by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
        
    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  


def testa02(desc="""database-user-name was not previously registered,exceeds max length, uses illegal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)
        

    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)
        
    stmt='register user qauser42 as qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser42 as qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
                
    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41 as qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
        
    stmt='unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
        
    stmt='register user qauser41 as 12345;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
        
    stmt='unregister user 12345;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')        

    stmt='register user qauser41 as "@test1";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')        
        
    stmt='unregister user "@test1";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='unregister user qauser42test;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)
    
    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
    

def testa03(desc="""database-user-name valid with various lengths, max, symbols"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)
        
    stmt='register user qauser41 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='register user qauser42 as qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt='unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)
    
    stmt='register user qauser41 as  "efgh@.wxyz0/";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='unregister user "efgh@.wxyz0/";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    
    
    stmt='register user qauser41 as  "KLM@./345678";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='unregister user  "KLM@./345678";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='register user qauser41 as  "1234";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='unregister user  "1234";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)
 
    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  



def testa04(desc="""regsiter dir-name as username  unregister user dir name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='register user qauser41 as qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
        
    stmt='register user qauser41 as qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
        
    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
        
    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa05(desc="""unregister a predefined user ,existing role name,reversed name/role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt='unregister user db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt='unregister user db__useradminuser;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
        
    stmt='unregister user "SUPER.SUPER";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
        
    stmt='unregister user "DB__ADMIN";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt='unregister user "DB__";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')


    stmt='unregister user none;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');


    stmt='unregister user public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');


    stmt='unregister user "_system";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')


    _testmgr.testcase_end(desc)  


def testa06(desc=""" unregister user by db__root immutable configuration authentication, ordering clauses(n)s"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
    
    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='register user qauser42  configuration 1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt='unregister user qauser41test by__root immutable; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');

    stmt='unregister user qauser41test by__root configuration; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');    
    
    stmt='unregister user qauser42 by__root configuration; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');    

    stmt='unregister user qauser42 by__root immutable; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');    
    
    stmt='unregister user qauser41test; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
        
    stmt='unregister user qauser42; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
       
  
def testa07(desc="""unregister user using by command"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
       
    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='register user qauser41 as qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    stmt='register user qauser41 as qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser41test by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');    
        
    stmt='unregister user qauser42 by qauser99;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');    
        
    stmt='unregister user qauser41 by qauser99;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001');    
        
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333');    

    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  


def testa08(desc="""execute command by user not authorized"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)
                
    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt = 'unregister user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
   
    stmt = 'unregister user qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
    
    stmt = 'unregister user qauser41 by qauser99;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
        
    _testmgr.testcase_end(desc)  
      
def testa09(desc="""unregister by user who did not register the user and has not privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)

        
    stmt='register user qauser41 as qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser41test;'
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='unregister user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    stmt='unregister user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    stmt='unregister user qauser41test;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    mydci = basic_defs.switch_session_qi_user3()         
    stmt='unregister user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    stmt='unregister user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)
        
    _testmgr.testcase_end(desc)          

def testa10(desc="""register user by one , unregister by another(has and has no privileges)"""):
    global _testmgr
    global _testlis
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
        

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)  


    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser41test;'
    output = _dci.cmdexec(stmt) 

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='register user qauser41 as qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    mydci = basic_defs.switch_session_qi_user4()     
    stmt='register user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 


    mydci = basic_defs.switch_session_qi_user2()     
    stmt='unregister user qauser41test;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    mydci = basic_defs.switch_session_qi_user4()     
    stmt='unregister user qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 
        
    stmt='unregister user qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017') 

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)  

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)              
        
def testa11(desc="""unregister user cascade/restrict"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)
   
    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser41test;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41 as qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)
    
    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
        
    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
        
    stmt='unregister user qauser41 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
        
    stmt='unregister user qauser41 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1048')
    
    stmt='unregister user qauser42 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
        
    stmt='unregister user qauser42 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1048')

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)          

def testa12(desc="""double unregister a registered user""" ):    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)   
    
    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser41test;'
    output = _dci.cmdexec(stmt)   

    stmt='register user qauser41 as qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)   

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')  
        
    stmt='unregister user qauser79test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser41 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    mydci = basic_defs.switch_session_qi_user2()     
    stmt='unregister user qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
        
    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)   

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)      

def testa13(desc="""unregister user who owns objects and has been granted any privielges""" ):    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)
        
    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser42 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    mydci = basic_defs.switch_session_qi_user2()             
    stmt='register user qauser1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
    
    
    stmt='create schema sch1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt='set schema sch1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt='create table t1(a int)no partition;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt='grant select on t1 to qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt='unregister user qauser42 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1343')

    stmt='unregister user qauser42 restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1227')
	
    stmt='unregister user qauser42 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        
    stmt='drop schema sch1 cascade;'
    output = mydci.cmdexec(stmt)


    stmt='unregister user qauser42 restrict;'
    output = _dci.cmdexec(stmt)
	
    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)
	
	

    _testmgr.testcase_end(desc)  

def testa14(desc="""unregister an immutable user""" ):    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)

     
    stmt='register user qauser41 as qauser41test immutable;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser42 by db__root immutable;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='register user qauser42  immutable configuration 1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1387')    

    stmt='unregister user qauser42; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1387')    

    stmt='unregister user qauser42 immutable; '
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser41test reset immutable;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser42 reset immutable;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)      

    stmt='unregister user qauser42; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
        
def testa15(desc="""unregister multiple internal user(n)""" ):    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    

    stmt = 'unregister user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'unregister user qauser42;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41 as qauser41test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser41 as qauser42 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')    

    stmt='register user qauser41 as "' + gvars.user2email + '" configuration 1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt='unregister user qauser41test ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser42 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt='unregister user "' + gvars.user2email + '";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
      
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')  

    stmt = 'register user qauser41;'
    output = _dci.cmdexec(stmt)
        
    stmt = 'register user qauser42;'
    output = _dci.cmdexec(stmt)  

    _testmgr.testcase_end(desc)  
    
def testa16(desc="""unregister different authentication user(n)""" ):    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    
    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)


    stmt='register user qauser41 as qauser41test configuration 1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser41 as "' + gvars.user2email + '"configuration 2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt='register user qauser42 configuration 1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user "' + gvars.user2email + '" as "' gvars.user2 + '" configuration 3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user "' + gvars.user1email + '"  authentication 3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    

    stmt='unregister user qauser41test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user ' + gvars.user2email + '" restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    

    stmt='unregister user  qauser42 ;'
    output = _dci.cmdexec(stmt)


    stmt='unregister user  "' + gvars.user2 + '" restrict;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "' + gvars.user1email + '" ;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser41;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser42;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc) 
 
def testa17(desc="""cleanup"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    #stmt = 'unregister user qauser41;'
    #output = _dci.cmdexec(stmt)

    #stmt = 'unregister user qauser42;'
    #output = _dci.cmdexec(stmt)
        
    #stmt = 'unregister user qauser43;'
    #output = _dci.cmdexec(stmt)
        
    #stmt = 'unregister user qauser44;'
    #output = _dci.cmdexec(stmt)
        
    #stmt = 'unregister user qauser45;'
    #output = _dci.cmdexec(stmt)
        
    #stmt = 'unregister user qauser46;'
    #output = _dci.cmdexec(stmt)
        
    #stmt = 'unregister user qauser47;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser42test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user  "efgh@.wxyz0/";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "KLM@./345678";'
    output = _dci.cmdexec(stmt)
        
    stmt='unregister user "1234";'
    output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser53;'
    #output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser53test;'
    output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser54;'
    #output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser55;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser57test;'
    output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser57;'
    #output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser56;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser58test; '
    output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser59; '
    #output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser58; '
    #output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser64;'
    #output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser62;'
    #output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser60test;'
    output = _dci.cmdexec(stmt)

    #stmt = 'unregister user qauser65;'
    #output = _dci.cmdexec(stmt)
        
    #stmt = 'unregister user qauser66;'
    #output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser67;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser69test;'
    output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser68;'
    #output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser69test;'
    output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser73;'
    #output = _dci.cmdexec(stmt)
        
    stmt='unregister user qauser70test;'
    output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser73;'
    #output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser72;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser74test;'
    output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser76 ;'
    #output = _dci.cmdexec(stmt)
    
    #stmt='unregister user qauser78;'
    #output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser77;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser79test;'
    output = _dci.cmdexec(stmt)
        
    #stmt='unregister user qauser81;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser82test;'
    output = _dci.cmdexec(stmt)


    #stmt='unregister user qauser83 ;'
    #output = _dci.cmdexec(stmt)


    stmt='unregister user qauser84test;'
    output = _dci.cmdexec(stmt)
    

    #stmt='unregister user qauser85; '
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser86test ;'
    output = _dci.cmdexec(stmt)

    #stmt='unregister user qauser87 ;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user "' + gvars.user2email + '";'
    output = _dci.cmdexec(stmt)

      
    #stmt='unregister user qauser86;'
    #output = _dci.cmdexec(stmt)
    

    #stmt='unregister user qauser88;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser88test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "' + gvars.user2email + '";'
    output = _dci.cmdexec(stmt)

    #stmt='unregister user  qauser89 ;'
    #output = _dci.cmdexec(stmt)

    stmt='unregister user qauser90test;'
    output = _dci.cmdexec(stmt)

    stmt='drop schema sch1 cascade;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)  


