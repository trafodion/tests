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


def testa01(desc="""Test register user, vary ordering of clauses, misspell keywords"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    
    stmt = """register qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """reg user qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """user register qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register qauser11 user;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 as;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user as qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 sa qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register qauser11 as qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user by qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 yb qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register qauser11 by qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 as qauser11 by;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 as by qauser11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 as qauser11 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 by cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    _testmgr.testcase_end(desc)

def testa02(desc="""Test register user a02, dir-user-name avalid with various lengths, max, symbols"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
 
    stmt = """unregister user a;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user "qa1001@qa.com";"""
    output = _dci.cmdexec(stmt)

    stmt = """register user "qa1001@qa.com";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user "americas_qa1004";"""
    output = _dci.cmdexec(stmt)

    stmt = """register user "americas_qa1004";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    
    
def testa03(desc="""Test register user a03, dir-user-name exceeds max length,illegal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
          
    stmt = """register user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
         
    stmt = """register user 12aab2f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user $%*(*dsaf;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
     
    stmt = """register user _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
 
    _testmgr.testcase_end(desc)
    

def testa04(desc="""Test register user a04, database-user-name various lengths, max, symbols,legal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister user qauser1;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser2;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """unregister user qauser3;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser4;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser5;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser1 as qauser1test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser2 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser3 as qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser4 as "123456789-_@./";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser5 as "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser1test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user  qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "123456789-_@./";"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


def testa05(desc="""Test register user a05, data-user-name exceeds max length,illegal characters"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    stmt = """unregister user qauser6;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser7;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """unregister user qauser8;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser9;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser10;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser11;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser12;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser6 as qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
       
    stmt = """register user qauser7 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """register user qauser8 as AABB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser9 as aabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """register user qauser10 as _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser11 as "@test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser12 as \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister user AABB;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    

def testa06(desc="""Test register user a06,register user that is the same as an existing user name(predefined,user-defined,reversed), existing role name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
        
    stmt = """register user sqluser_admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """register user "SUPER.SUPER";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')

    stmt = """unregister user qauser13;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser14;"""
    output = _dci.cmdexec(stmt)
 
    stmt = """register user qauser13 as qauser14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser14 as qauser14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """unregister user qauser14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt = """register user public;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user none;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser13 as "_system";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """register user qauser13 as "DB__";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    _testmgr.testcase_end(desc)  
    

def testa07(desc="""Test register user a07, user does not exist on the LDAP server"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    stmt = """register user qauser_dne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')

        #check length, max 128?
    stmt = """register user qauser_dne_3456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

        #check illegal characters, single quote allowed?
    stmt = """register user qauser_'000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    _testmgr.testcase_end(desc)
    

def testa08(desc="""Test register user a08, user was just registered"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """unregister user qauser15;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    _testmgr.testcase_end(desc)
    
    

def testa09(desc="""Test register user a09, user was just unregistered"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """unregister user qauser16;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser16;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser16;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser16 as qauser16test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser16test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
    

def testa10(desc="""Test register user a10, data-user-name is the same and different as dir-user-name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
       
    stmt = """unregister user qauser17;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser17 as qauser17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser18;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser18 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)    


def testa12(desc="""Test register user a12, register user using by command"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
   
    stmt = """register user qauser1 by db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')  

    stmt = """register user qauser1 by qauser12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001') 
   
        
    stmt = """register user qauser1 by sqluser_admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    _testmgr.testcase_end(desc) 
    
    

def testa13(desc="""Test register user a13, execute command by user not authorized"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
 
    stmt = """unregister user qauser22;"""
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2()    

    stmt = """register user qauser22;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')  
      
    stmt = """register user qauser22 by superuser;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')  

    stmt = """register user qauser22 as qauser22 by sqluser_admin;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001') 

    stmt = """register user qauser22;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc) 
    

def testa16(desc="""Test register user a16, the same external is registered to multiple internal users(including reversed,predefined username)(n)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    stmt = """unregister user qauser26;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser27;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser28;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser26;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser26 as qauser26test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt = """register user qauser26 as db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """register user qauser26 as "db__";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
           
    #stmt ="""register user qauser27 as "super.super";"""
    #output = _dci.cmdexec(stmt)
    #self._odbc.expect_complete(stmt);

    stmt = """register user qauser26 as qauser27 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt = """register user qauser27 as qauser28;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser27 as qauser27test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt = """register user qauser27;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt = """register user qauser28 as qauser28test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser26;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser26test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser27;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser27test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser28;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser28test;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)
    

def testa17(desc="""Test register user a17, two external users are registered as same internal user(n)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """unregister user qauser29;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser30;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser31;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser29 as qauser29test ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """register user qauser30 as qauser29test ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """register user qauser29 as qauser30;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    
    stmt = """register user qauser31 as qauser29test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """register user qauser30 as qauser31;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        
    stmt = """register user qauser30 as qauser30test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')

    stmt = """register user qauser31 as qauser31test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user qauser29test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser30;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser30test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser31;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser31test;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)
    
    
def testa18(desc="""Test register user a18, regsiter user with local ,remote , enterprise ,cluster authentication  different configuration(n)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """unregister user qauser32;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser33;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser34;"""
    output = _dci.cmdexec(stmt)


    stmt = """unregister user qauser35;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser36;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser32 local authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
  
    stmt = """register user qauser33 as qauser33test enterprise authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user \"""" + gvars.user2email + """\" cluster authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user \"""" + gvars.user1email + """\" as "user1test" remote authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user \"""" + gvars.user1email + """\" as \"""" + gvars.user2email + """\" cluster authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user \"""" + gvars.user1email + """\" as "qauser33" cluster authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser32 as qauser32test enterprise authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser34 as qauser32test enterprise authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser34 as qauser33 enterprise authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """register user qauser35 as qauser33 local authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """register user qauser36 as \"""" + gvars.user1email + """\" enterprise authentication;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """unregister user qauser32;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser33;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser34;"""
    output = _dci.cmdexec(stmt)


    stmt = """unregister user qauser35;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser36;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser32test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser33test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "user1test";"""
    output = _dci.cmdexec(stmt)


    stmt = """unregister user \"""" + gvars.user2email + """\" ;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user \"""" + gvars.user1email + """\";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)


def testa19(desc="""cleanup"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = """unregister user a;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "qa1001@qa.com";"""
    output = _dci.cmdexec(stmt)


    stmt = """unregister user "americas_qa1004";"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser1test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qa902_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
   
    stmt = """unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "123456789-_@./";"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "LMNOP-./ghij_@klmnop";"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user AABB;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser13;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser14;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser15;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser16;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser16test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser17;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser18;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser19;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser20 ;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser21 ;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser20test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser21test;"""
    output = _dci.cmdexec(stmt)
 
    #stmt = """unregister user qauser22;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser23test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser23;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser24;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser24test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser25;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser26;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser26test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser27;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser27test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser28;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser28test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser29test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser29;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser30;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser30test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser31;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser31test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser35;"""
    #output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser36;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser32test;"""
    output = _dci.cmdexec(stmt)

    #stmt = """unregister user qauser32;"""
    #output = _dci.cmdexec(stmt)

    stmt = """unregister user qauser33test;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "user1test";"""
    output = _dci.cmdexec(stmt)


    stmt = """unregister user \"""" + gvars.user2email + """\" ;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user \"""" + gvars.user1email + """\";"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user "SUPER.SUPER";"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


