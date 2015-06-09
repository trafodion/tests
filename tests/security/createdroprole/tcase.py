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


def testa01(desc="""ength of <role-name> param below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop role W;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop role "1";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role \"\"\"\";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role "_";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role AA;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role A1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role "_A";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)


        #role name  min length 1 char 
    stmt = """create role W;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #role name min length 1 delimited numeric
    stmt = """create role "1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        #role name min length 1 delimited symbol

    stmt = """create role \"\"\"\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')

        #role name min length 1 delimited symbol
    stmt = """create role "_";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #role name length 2
    stmt = """create role AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #role name length 2
    stmt = """create role A1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        #role name length 2
    stmt = """create role "_A";"""
    _dci.expect_complete_msg(output)
        #role name length max-1
    stmt = """create role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #role name length max
    stmt = """create role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role W;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role "1";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role \"\"\"\";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role "_";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role AA;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop role A1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role "_A";"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa02(desc="""Length of <role-name> param blank out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """create role  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    #max+1
    stmt = """create role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    #max+n
    stmt = """create role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
                
    stmt = """drop role ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
                

def testa03(desc="""rolename using valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return    
    
    stmt = """drop role AaBcderser;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role ACD123531;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role dewqrq___3423532;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "13344//23";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "areqw31324dafd3AAA";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"Test\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "test";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "/test";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "1test1";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "1test1/";"""
    output = _dci.cmdexec(stmt)

    ##valid regular and delimited identifiers
    stmt = """create role AaBcderser;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role ACD123531;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role dewqrq___3423532;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "areqw31324dafd3AAA";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role \"Test\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
        
    stmt = """create role "/test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "1test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "1test1 ";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """drop role AaBcderser;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role ACD123531;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role dewqrq___3423532;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "13344//23";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "areqw31324dafd3AAA";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"""Test""\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "test";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "/test";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "1test1 ";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "1test1";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



def testa04(desc="""rolename using invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """drop role AABB;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role AabB;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role aabb;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role 12aab2f;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"\"\"AABB\"\"\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "AaBB";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_Aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "Avdcd"afet";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "@test1";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "";"""
    output = _dci.cmdexec(stmt)

    stmt = """create role AABB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
   #regular identifiers case insensitivity
    stmt = """create role AabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role aabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    #begin with number
    stmt = """create role 12aab2f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #begin with underscore
    stmt = """create role _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    #role name use reserved word
    stmt = """create role test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    _dci.expect_error_msg(output, '15001')

    #delimited identifiers case sensitivity
    stmt = """create role \"\"\"AABB\"\"\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')
    
    stmt = """create role "AaBB";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role "aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role "_aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "_Aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    #contain (@, \, ^) and other not supported delimited identifiers
    stmt = """create role "Avdcd"afet";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
    
    stmt = """create role "@test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')
    
    stmt = """create role "1test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "1test1 ";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3004')
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role AABB;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role AabB;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role aabb;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role 12aab2f;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"\"\"AABB\"\"\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "AaBB";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_Aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "Avdcd"afet";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "1test1";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa05(desc="""Length of <grantor> param"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """unregister user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser83;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user A;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user AA;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a05test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a05test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a05test3;"""
    output = _dci.cmdexec(stmt)

        #grantor  min length 1 char 
    stmt = """register user qauser81 as A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """register user qauser82 as AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """register user qauser83 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #create role with admin
    stmt = """create role C_a05test1 with admin A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a05test2 with admin AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a05test3 with admin qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #cleanup
    stmt = """drop role C_a05test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a05test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a05test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user A;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa06(desc="""Length of <grantor> param"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser82;"""
    output = _dci.cmdexec(stmt)

    #grantor param
    stmt = """register user qauser81 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    
    stmt = """register user qauser82 as qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt = """create role C_a06test1 with admin ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a06test2 with admin qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    
    stmt = """create role C_a06test3 with admin qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output,'3118')

    stmt = """drop role C_a06test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    stmt = """drop role C_a06test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    stmt = """drop role C_a06test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser80;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser83;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
           
  
def testa07(desc="""grantor using valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """unregister user "qauser81//";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser83;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser84;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "test//";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "1test/";"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test5;"""
    output = _dci.cmdexec(stmt)
           
    stmt = """register  user qauser81 as "qauser81//";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser83 as "test//";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser84 as "1test/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a07test1 with admin qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a07test2 with admin "qauser81//";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a07test3 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
        
    stmt = """create role C_a07test4 with admin "test//";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a07test5 with admin "1test/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role C_a07test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a07test5;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "qauser81//";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "test//";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "1test/";"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



def testa08(desc="""grantor using invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return  
    
    stmt = """drop role C_a08test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a08test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a08test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a08test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a08test5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a08test6;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a08test7;"""
    output = _dci.cmdexec(stmt)

    stmt = """unregister user _qauser2;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser85;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "qauser85//";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user 3qauser;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "@qauser84";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "^qauser86";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "qauser87";"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser81 as qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82 as _qauser2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """register user qauser83 as 3qauser;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """register user qauser84 as "@qauser84";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """register user qauser85 as "qauser85//";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser86 as "^qauser86";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """register user qauser87 as "qauser87";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a08test1 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a08test2 with admin _qauser2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a08test3 with admin 3qauser;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a08test4 with admin "@qauser84";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a08test5 with admin "qauser85//";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a08test6 with admin "^qauser86";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a08test7 with admin "qauser87";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
    stmt = """drop role C_a08test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a08test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    
    stmt = """drop role C_a08test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    
    stmt = """drop role C_a08test4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    
    stmt = """drop role C_a08test5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a08test6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    
    stmt = """drop role C_a08test7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """unregister user _qauser2;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user 3qauser;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "@qauser84";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "qauser85//";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "^qauser86";"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user "qauser87";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



def testa09(desc="""missing keywords disorder error spelling"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a09test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a09test2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a09test1 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #missing keyword
    stmt = """create C_a09test2 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a09test2 with qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a09test2 admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a09test2 qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a09test2 with administrator qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create roles C_a09test2 with administrator qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a09test2 admin with qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create with admin qauser81 role C_a09test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role C_a09test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a09test2;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



def testa10(desc="""create more than a role with admin more a owner in a stat"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a10test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a10test2;"""
    output = _dci.cmdexec(stmt)

    #create 2 roles in a stat
    stmt = """create role C_a10test1,C_a10test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #create role with admin 2 grantors
    stmt = """create role C_a10test1 with admin qauser91,qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #create 2 roles with admin more than one grantor
    stmt = """create role C_a10test1,C_a10test2 with admin qauser91,qauser92,qauser93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role C_a10test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a10test2;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



def testa11(desc="""create role using predefined names"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"\"\"PUBLIC\"\"\" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"\"\"_System\"\"\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "NONE";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role current_role_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role public_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role none_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "CURRENT_USER";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "CURRENT_ROLE";"""
    output = _dci.cmdexec(stmt)

    stmt = """create role PUBLIC ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role "PUBLIC" ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role \"\"\"PUBLIC\"\"\" ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')
    
    stmt = """create role PUBLIC with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role _System;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role "_System";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role \"\"\"_System\"\"\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')
    
    stmt = """create role "db__root";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role db__USERADMIN with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role db__admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role "db__USERADMINUSER";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role DB__Services;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role db__test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role "db__*";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role NONE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role "NONE";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    
    stmt = """create role CURRENT_USER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role CURRENT_ROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role "CURRENT_USER";"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create role "CURRENT_ROLE";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
           
    stmt = """create role current_role_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role public_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role none_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role \"\"\"PUBLIC\"\"\" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"\"\"_System\"\"\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "NONE";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role current_role_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role public_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role none_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "CURRENT_USER";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "CURRENT_ROLE";"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa12(desc="""create role rolename that is new/was dropped"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a12test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a12test2;"""
    output = _dci.cmdexec(stmt)
           
    stmt = """create role C_a12test1 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a12test1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #create role using drop rolename 
    stmt = """create role C_a12test1 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #expect any *CREATE ROLE C_A12TEST1 WITH ADMIN PAULLOW81*
    stmt = """showddl role C_a12test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE ROLE "C_A12TEST1" WITH ADMIN "PAULLOW81"' );
    _dci.expect_any_substr(output,'-- GRANT ROLE "C_A12TEST1" TO "PAULLOW81" WITH ADMIN OPTION' );
        
    stmt = """create role C_a12test2 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a12test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a12test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  
           

def testa13(desc="""create role with admin user who is dropped"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qausertest;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qausertest;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a13test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser81 as qausertest;"""
    output = _dci.cmdexec(stmt)
    
    #expect any *REGISTER USER PAULLOW81 AS PAULLOWTEST LOGON ROLE NONE*
    stmt = """showddl user qausertest;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW81" AS "PAULLOWTEST"' );
    
    stmt = """unregister user qausertest;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #using the dropped username to create role
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role qausertest with admin qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a13test1 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
           
           
    #recovery user
    stmt = """drop role qausertest;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a13test1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa14(desc="""create role using existingrolename"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a14test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a14test2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a14test1 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role C_a14test2 with admin qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()

    stmt = """grant role C_a14test1 to qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
            

    #roles with no object; roles with users/priv
    stmt = """create role C_a14test1 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test2 with admin qauser93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    #different user create same name role
    stmt = """create role C_a14test1 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test1 with admin qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role C_a14test2 with admin qauser93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """revoke role C_a14test1 from qauser93 granted by qauser91;"""
    output = _dci.cmdexec(stmt)
     
    mydci = basic_defs.switch_session_qi_user2()
        
    stmt = """drop role C_a14test1;"""
    output = mydci.cmdexec(stmt)


    stmt = """drop role C_a14test2;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   


def testa15(desc="""rolename using username that match/not match dir-username"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """unregister user qauser1test;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser2test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser1test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser2test;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser83;"""
    output = _dci.cmdexec(stmt)

        #role name is username match dir-username
    stmt = """create role qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role qauser81 with admin qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role qauser81 with admin qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

        #role name is username not match dir-username
    stmt = """unregister user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser81 as qauser1test;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82 as qauser2test;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role qauser1test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role qauser1test with admin qauser1test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt = """create role qauser2test with admin qauser83;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

        #role name is dir-username not register
    stmt = """unregister user qauser1test;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser2test;"""
    output = _dci.cmdexec(stmt)
           
    stmt = """create role qauser81 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #expect any *CREATE ROLE PAULLOW81 WITH ADMIN DB__USERADMINUSER*
    stmt = """showddl role qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE ROLE "PAULLOW81"' );
    
    stmt = """create role qauser82 with admin qauser83;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
        #expect any *CREATE ROLE PAULLOW82 WITH ADMIN PAULLOW83*
    stmt = """showddl role qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'CREATE ROLE "PAULLOW82" WITH ADMIN "PAULLOW83"' );

    stmt = """drop role qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser82;"""
    output = _dci.cmdexec(stmt)

        #role name is dir-username but not match username
    stmt = """register user qauser81 as qauser1test;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82 as qauser2test;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role qauser81 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role qauser82 with admin qauser2test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role qauser81;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #recovery user
    stmt = """unregister user qauser1test;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser2test;"""
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  


def testa16(desc="""rolename using username that match/not match dir-username"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a16test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a16test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user C_a16test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a16test1 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        #register as role name
    stmt = """register user qauser81 as C_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

        #drop role ,register user use rolename
    stmt = """drop role C_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser81 as C_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a16test2 with admin C_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a16test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user C_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  
           
           
           
def testa17(desc="""role owner drop role/grant role/revoke role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser81;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser83;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser84;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a17test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a17test2;"""
    output = _dci.cmdexec(stmt)
           
    stmt = """create role C_a17test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create role C_a17test2 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role C_a17test1 to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role C_a17test1 to qauser92, qauser93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #after granting to user,cannot be dropped
    stmt = """drop role C_a17test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1348')
    
    stmt = """revoke role C_a17test1 from qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role C_a17test1 from qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role C_a17test1 from qauser93;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #other user can't drop role
    mydci = basic_defs.switch_session_qi_user2()
        
    stmt = """drop role C_a17test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

        #after revoking ,can be dropped
    stmt = """drop role C_a17test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #owner drop role, grant and revoke the role to users
        
    mydci = basic_defs.switch_session_qi_user2()    
        
    stmt = """grant role C_a17test2 to qauser91;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1223')
        
    stmt = """grant role C_a17test2 to qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """grant role C_a17test2 to qauser93,qauser94;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
        
    stmt = """grant role C_a17test2 to qauser_1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')
    
        #after granting to user,cannot be dropped
    stmt = """drop role C_a17test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1348')
    
        #revoke role from user
    stmt = """revoke role C_a17test2 from qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke role C_a17test2 from qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """revoke role C_a17test2 from qauser94;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """drop role C_a17test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)     
        
    stmt = """drop role C_a17test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a17test2;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa18(desc="""DB__ROOT  grant/revoke each other's role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a18test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a18test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a18test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a18test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a18test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role C_a18test1 to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
        #another user has create role priv 
        #expect any *Connected to DataSource *
    stmt = """create role C_a18test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role C_a18test2 to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role C_a18test1 from qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role C_a18test2 from qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop role C_a18test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #u1 u2 create role ,grant/revoke each other
    stmt = """create role C_a18test3 with admin DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role C_a18test3 to qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role C_a18test4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """grant role C_a18test4 to qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """revoke role C_a18test3 from qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role C_a18test4 from qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
    stmt = """drop role C_a18test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a18test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a18test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a18test1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
    
    
def testa19(desc="""ordinary user with admin priv create/grant/revoke role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a19test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """grant role DB__ROOTROLE to qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create role C_a19test1 with admin qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
        #expect any *CREATE ROLE C_A19TEST1 WITH ADMIN PAULLOW92*
    stmt = """showddl role C_a19test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'CREATE ROLE "C_A19TEST1" WITH ADMIN "PAULLOW92"' );

    mydci = basic_defs.switch_session_qi_user4()
                
    stmt = """grant role C_a19test1 to qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

        #creator revoke role from user whom owner grant role to
    mydci = basic_defs.switch_session_qi_user2()    
    
    stmt = """revoke role C_a19test1 from qauser93;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    mydci.expect_error_msg(output, '1018')

                
    mydci = basic_defs.switch_session_qi_user4()  
    stmt = """revoke role C_a19test1 from qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

                
    stmt = """revoke role DB__ROOTROLE from qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
    stmt = """drop role C_a19test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  


def testa20(desc="""grantor with CURRENT_USER/existing username"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a20test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a20test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a20test1 with admin CURRENT_USER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
        #expect any *CREATE ROLE C_A20TEST1 WITH ADMIN DB__ROOT*
    stmt = """showddl role C_a20test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'CREATE ROLE "C_A20TEST1";' );

    stmt = """showddl role C_a20test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '  -- GRANT ROLE "C_A20TEST1" TO "DB__ROOT" WITH ADMIN OPTION;' );
    
    stmt="""grant role DB__ROOTROLE to qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #ordinary user use CURRENT_USER
    
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt="""create role C_a20test2 with admin CURRENT_USER;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt="""showddl role C_a20test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output, 'CREATE ROLE "C_A20TEST2" WITH ADMIN "PAULLOW91";' );

    stmt="""showddl role C_a20test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output, '  -- GRANT ROLE "C_A20TEST2" TO "PAULLOW91" WITH ADMIN OPTION;' );

    stmt="""grant role C_a20test2 to qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt="""grant role C_a20test2 to qauser92 granted by qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    stmt="""grant role C_a20test2 to qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt="""revoke role C_a20test2 from qauser92 granted by qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
    mydci = basic_defs.switch_session_qi_user2()       
    
    stmt="""drop role C_a20test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt="""revoke role DB__ROOTROLE from qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop role C_a20test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
          

    _testmgr.testcase_end(desc)   


def testa21(desc="""<grantor> is not valid"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a21test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a21test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a21test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a21test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser2_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """unregister user qauser82;"""
    output = _dci.cmdexec(stmt)
           
    stmt = """create role C_a21test1 with admin qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
           
        #WITH ADMIN existingrolename
    stmt = """create role C_a21test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role C_a21test3 with admin C_a21test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340')

        #WITH ADMIN usernamenotexist
    stmt = """create role C_a21test4 with admin qauser2_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt = """drop role C_a21test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a21test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a21test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a21test4;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



def testa22(desc="""create role by user who does not have admin privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a22test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a22test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a22test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser94;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser95;"""
    output = _dci.cmdexec(stmt)

        #user does not have admin priv
        
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """create role C_a22test1 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
    stmt = """create role C_a22test2 with admin qauser92 ;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');


    #grant admin privilege to user
    stmt="""grant role DB__ROOTROLE to qauser92 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    mydci = basic_defs.switch_session_qi_user4()   
    
    stmt="""create role C_a22test3 with admin qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
      
                
    stmt = """revoke role DB__ROOTROLE from qauser92 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a22test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a22test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a22test1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  


def testa23(desc="""create role by DB__ROOT"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a23test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test5;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a23test1 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        #no with admin clause
    stmt = """create role C_a23test2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
        #with admin clause current_user
    stmt = """create role C_a23test3 with admin CURRENT_USER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create role C_a23test4 with admin DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create role C_a23test5 with admin ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role C_a23test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a23test5;"""
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  



def testa24(desc="""change grantor or given to someone else"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a25test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
           
        #change grantor
    stmt = """create role C_a25test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #change with admin 
    stmt = """alter role C_a25test1 set admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create role C_a25test1 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

        #grantor gives role to someone else
    mydci = basic_defs.switch_session_qi_user5()
                
    stmt = """alter role C_a25test1 set admin qauser91;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
           
    stmt = """drop role C_a25test1;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  

    
    
def testa25(desc="""revoke ordinary user's admin priv then create role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a26test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a26test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)

    #grant create role to ordinary user
    stmt="""grant role DB__ROOTROLE to qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    mydci = basic_defs.switch_session_qi_user2()

    stmt="""create role C_a26test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt="""create role C_a26test2 with admin qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt="""grant role C_a26test1 to qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    #revoke create priv from qauser91
    stmt="""revoke role DB__ROOTROLE from qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    #role create by qauser91 still can be used
    mydci = basic_defs.switch_session_qi_user2()
    
    stmt="""revoke role C_a26test1 from qauser92;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
           
    #owner can drop role
    stmt = """drop role C_a26test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user4()   
    
    stmt = """grant role C_a26test2 to qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt = """revoke role C_a26test2 from qauser93;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop role C_a26test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

        #role owner drop role
    mydci = basic_defs.switch_session_qi_user4()    
    
    stmt = """drop role C_a26test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
          

    stmt = """drop role C_a26test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role C_a26test2;"""
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  
 



def testa26(desc="""unregister user who is owner of a role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role C_a27test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role C_a27test1 with admin qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
        #unregister user
    stmt = """unregister user qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1347')

        #role be dropped
    stmt = """drop role C_a27test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """unregister user qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """register user qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
           
    stmt = """grant role C_a27test1 to qauser83;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
    
    stmt = """create role C_a27test1 with admin qauser82;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role C_a27test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  
           

def testa27(desc="""Length of <role-name> param below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role W;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role "1";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role """";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role "_";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role AA;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role A1;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role "_A";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)

        #role name  min length 1 char 
    stmt = """create role W;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name min length 1 delimited numeric
    stmt = """create role "1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name min length 1 delimited symbol
    stmt = """create role \"\"\"\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')
                
        #role name min length 1 delimited symbol
    stmt = """create role "_";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name length 2
    stmt = """create role AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name length 2
    stmt = """create role A1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name length 2
    stmt = """create role "_A";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name length max-1
    stmt = """create role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #role name length max
    stmt = """create role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role W;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role "1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role \"\"\"\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
                
    stmt = """drop role "_";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role A1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role "_A";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234127;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  



def testa28(desc="""Length of <role-name> param blank out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
        #blank
    stmt = """create role  ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
        #max+1
    stmt = """create role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
                
        #max+n
    stmt = """create role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
                
    stmt = """drop role ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
                
    stmt = """drop role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')


    _testmgr.testcase_end(desc)  


def testa29(desc="""rolename valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role AaBcderser;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role ACD123531;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role dewqrq___3423532;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role "13344//23";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role ".areqw31324dafd3AAA";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role "Test\";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """drop role "test";"""
    output = _dci.cmdexec(stmt)

        #valid regular and delimited identifiers
    stmt = """create role AaBcderser;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role ACD123531;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role dewqrq___3423532;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role ".areqw31324dafd3AAA";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
                
    stmt = """create role "Test/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role "test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role AaBcderser;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role ACD123531;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role dewqrq___3423532;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role "13344//23";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role ".areqw31324dafd3AAA";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
       
                
    stmt = """drop role "Test/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role "test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)  


def testa30(desc="""rolename invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role AABB;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role AabB;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role aabb;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role 12aab2f;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "/AABB/";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "AaBB";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_Aabb";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "Avdcd"afet";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "@test";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "test1 ";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "test1";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "test1/";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "";"""
    output = _dci.cmdexec(stmt)

    stmt = """create role AABB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #regular identifiers case insensitivity
    stmt = """create role AabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """create role aabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
                
        #begin with number
    stmt = """create role 12aab2f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
        #begin with underscore
    stmt = """create role _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
                
        #role name use reserved word
    stmt = """create role test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    _dci.expect_error_msg(output, '15001')

        #delimited identifiers case insensitivity

    stmt = """create role "/AABB/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role "/AaBB/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """create role "/aabb/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
                
    stmt = """create role "_aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role "_Aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

        #contain (@, \, ^) and other not supported delimited identifiers
    stmt = """create role "Avdcd"afet";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
                
    stmt = """create role "@test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')

    stmt = """create role \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1370')
                
    stmt = """create role "test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role "test1 ";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """create role "test1/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')

    stmt = """create role "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3004')
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role AABB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role AabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """drop role aabb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
                
    stmt = """drop role 12aab2f;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role _W1245wereqwr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role "/AABB/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role "AaBB";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """drop role "aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')
                
    stmt = """drop role "_aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role "_Aabb";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """drop role "Avdcd"afet";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')
                
    stmt = """drop role "@test";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role \"~!#$%^&\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """drop role "test1";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)        
    
    stmt = """drop role "test1 ";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """drop role "test1/";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role \"^testa**$\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role "";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3004')
    _dci.expect_error_msg(output, '15001')



    _testmgr.testcase_end(desc)  



def testa31(desc="""missing keywords disorder error spelling"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role D_a05test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a05test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #drop role missing keywords
    stmt = """drop D_a05test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop D_a05test1 role;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """role D_a05test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop roel D_a05test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role D_a05test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  



def testa32(desc="""drop role using predefined names"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role current_role_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role public_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role none_test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role PUBLIC ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "PUBLIC" ;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role _System;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "_System";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role db__root;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role db__USERADMIN;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role db__services;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role db__test;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "db__*";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role db__admin;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role NONE;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "NONE";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role CURRENT_USER;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role CURRENT_ROLE;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "CURRENT_USER";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role "CURRENT_ROLE";"""
    output = _dci.cmdexec(stmt)
                
    stmt = """create role PUBLIC ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create role "PUBLIC" ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

        #create role \"PUBLIC\" ;
    stmt = """create role PUBLIC with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """create role _System;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3127')
    _dci.expect_error_msg(output, '15001')

    stmt = """create role "_System";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """create role db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """create role db__USERADMIN with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """create role DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """create role db__admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """create role db__services;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """create role db__test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """create role "db__*";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """create role NONE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create role "NONE";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """create role CURRENT_USER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """create role CURRENT_ROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role "CURRENT_USER";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role "CURRENT_ROLE";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt = """create role current_role_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role public_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role none_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role current_role_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role public_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role none_test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #drop
    stmt = """drop role PUBLIC ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role "PUBLIC" ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """drop role _System;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role "_System";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """drop role db__root;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """drop role db__USERADMIN;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """drop role DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """drop role db__services;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """drop role db__test;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """drop role "db__*";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')

    stmt = """drop role db__admin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """drop role NONE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role "NONE";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
                
    stmt = """drop role CURRENT_USER;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role CURRENT_ROLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role "CURRENT_USER";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  



def testa33(desc="""drop Name for <role-name> does not already exist/not vaild"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
    
    stmt = """drop role D_a07test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a07test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)

        #drop role does not already exist
    stmt = """drop role D_a07test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    stmt = """create role D_a07test2 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """drop role D_a07test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
        #consecutive drop role in same session 
    stmt = """drop role D_a07test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """drop role D_a07test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1338')
                

    stmt = """drop role D_a07test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338')

        #drop role existinguser
    stmt = """drop role qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1339')

    _testmgr.testcase_end(desc)  

                
                

def testa34(desc="""unregister user/role existingrolename restrict/cascade"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """drop role D_a08test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a08test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

                
        #unregister user/role
        
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """unregister user D_a08test1;"""
    output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output, '1340')
    mydci.expect_error_msg(output, '1017')
                
    stmt = """unregister role D_a08test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """unregister role D_a08test1 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
                
    stmt = """unregister role D_a08test1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop role D_a08test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)  
                

def testa35(desc="""Drop role that still assigned logon role/users/priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """drop role D_a09test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test5;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test6;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a09test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a09test2 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a09test3 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #create role; register user logon role; drop role
        #register a user as a logon role 
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)


        #one or more users still are granted to role; drop role
        #grant D_a09test3 role to user

    stmt = """grant role D_a09test3 to qauser92, qauser93 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #try to drop the granted role
    mydci = basic_defs.switch_session_qi_user5()        
        
    stmt = """drop role D_a09test3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1348')
                
        #after revoking ,drop role
    stmt = """revoke role D_a09test3 from qauser92 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role D_a09test3 from qauser93 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    mydci = basic_defs.switch_session_qi_user5()        
         
    stmt = """drop role D_a09test3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

        #======role is still granted to one or more priv; drop role====*
                
    stmt = """create schema cd_sch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema cd_sch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a09test4 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select,insert on tab1 to D_a09test4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #role is still granted to priv
        
    mydci = basic_defs.switch_session_qi_user5() 
    
    stmt = """drop role D_a09test4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1228')

    stmt = """set schema cd_sch1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """revoke select,insert on tab1 from D_a09test4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
#sh sleep $sleeptime

        
    mydci = basic_defs.switch_session_qi_user5() 
    
    stmt = """drop role D_a09test4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop schema cd_sch1 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


        #======create role; register user; set role during session; drop role============
        #process UserAdmin
    stmt = """create role D_a09test05 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a09test06 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)

    stmt = """grant role D_a09test06 to qauser91 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

                
#expect any *Connected to DataSource *


    stmt = """drop role D_a09test06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1348')

    stmt = """drop role D_a09test05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #end qauser91 session.

        #user still granted to role
    mydci = basic_defs.switch_session_qi_user5()     
        
    stmt = """drop role D_a09test06;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1348')

    stmt = """drop role D_a09test05;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1338')



    stmt = """revoke role D_a09test06 from qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)         
    stmt = """drop role D_a09test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a09test06;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  


def testa36(desc="""grant role to user revoke role from user then drop role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a11test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a11test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role D_a11test1 to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                

    mydci = basic_defs.switch_session_qi_user5()
                
    stmt = """revoke role D_a11test1 from qauser91;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop role D_a11test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)  

                


def testa37(desc="""grant priv to role revoke priv from role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a12test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a12test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                              
    stmt = """create schema cd_sch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema cd_sch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant all on tab1 to D_a12test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #before revoke priv from role ,role can't be dropped
    mydci = basic_defs.switch_session_qi_user5()    
    
    stmt = """drop role D_a12test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1228')
                
    stmt = """set schema cd_sch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """revoke all on tab1 from D_a12test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #drop schema ,catalog

    stmt = """set schema cd_sch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema cd_sch2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5() 
    
    stmt = """drop role D_a12test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  


def testa38(desc="""grant priv to role/grant role to user revoke all then drop role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a13test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a13test2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a13test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """create role D_a13test2 with admin qauser90;"""
    output = _dci.cmdexec(stmt)

    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
                                
    stmt = """create schema sch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema sch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table tab1(a int, b int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant insert on tab1 to D_a13test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select on tab1 to D_a13test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role D_a13test2 to qauser91 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()
    
    stmt = """set schema sch40;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

                
    stmt = """insert into tab1 values(1,2);"""
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output, 1);

    stmt = """select * from tab1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output, 1);
                

    stmt = """set schema sch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """revoke insert ,select on tab1 from D_a13test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        
    mydci = basic_defs.switch_session_qi_user5() 
    
    stmt = """drop role D_a13test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1348')
    
        #revoke role from user
    stmt = """revoke role D_a13test2 from qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)                
        #no priv,no user,no logon role relate to D_a13test2
        
    mydci = basic_defs.switch_session_qi_user5() 
    
    stmt = """drop role D_a13test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
               
    stmt = """drop role D_a13test1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop role D_a13test2;"""
    output = _dci.cmdexec(stmt)

    stmt = """set schema sch40;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

                
    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema sch40;"""
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  
 


                
def testa39(desc="""executed by user not role owner has/has not admin privilege(p,n)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser92;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser93;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a14test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a14test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a14test3;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a14test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a14test2 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a14test3 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant role DB__ROOTROLE to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""grant role DB__ROOTROLE to qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    time.sleep(10)


    #drop role who does not have admin privilege and not the role owner

    mydci = basic_defs.switch_session_qi_user6()    
    
    stmt = """drop role D_a14test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
                
    stmt = """drop role D_a14test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')

        #role owner drop role

    mydci = basic_defs.switch_session_qi_user5()          

    stmt = """drop role D_a14test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
             
        #who have admin privilege and role owner
        
    mydci = basic_defs.switch_session_qi_user2()         
                
    stmt = """drop role D_a14test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
                                
        
    mydci = basic_defs.switch_session_qi_user4()           

    stmt = """drop role D_a14test3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
                
          
    stmt="""revoke role DB__ROOTROLE from qauser91 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt="""revoke role DB__ROOTROLE from qauser92 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    _testmgr.testcase_end(desc)  


                
def testa40(desc="""user is role owner but does not have other admin priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a15test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a15test2;"""
    output = _dci.cmdexec(stmt)

    stmt = """create role D_a15test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a15test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user5()   
        
        #qauser90 is role owner
    stmt = """drop role D_a15test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

                
        #not role owner, no other admin priv
    stmt = """drop role D_a15test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
                
                
    stmt = """drop role D_a15test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  




def testa41(desc="""role has dependency using drop role cascade(not support)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                    
                
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a16test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a16test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a16test3;"""
    output = _dci.cmdexec(stmt)
                
        #role has obj priv
    stmt = """create role D_a16test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a16test2 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a16test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role D_a16test3 to qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create schema sch_sch43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """set schema sch_sch43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table a16tab1(col1 int ,col2 int)no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant select ,insert on a16tab1 to D_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #role is granted to user
    mydci = basic_defs.switch_session_qi_user5()
    
    stmt = """grant role D_a16test2 to qauser91;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

        #drop role

    stmt = """drop role D_a16test1;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1228')

    stmt = """drop role D_a16test1 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop role D_a16test1 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop role D_a16test2;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1348')

    stmt = """drop role D_a16test2 restrict;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop role D_a16test2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

                
    stmt = """drop role D_a16test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1348')

    stmt = """drop role D_a16test3 restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role D_a16test3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """set schema sch_sch43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop table a16tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop schema sch_sch43;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
               
                
    stmt = """revoke role D_a16test2 from qauser91 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """revoke role D_a16test3 from qauser92;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role D_a16test1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role D_a16test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """drop role D_a16test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  



def testa42(desc="""user is revoke from admin priv drop/grant/revoke already created role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
         
    stmt = """drop role D_a17test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test4;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test5;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)

    stmt="""grant role DB__ROOTROLE to qauser90 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a17test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a17test2 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role D_a17test1 to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """grant role D_a17test2 to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a17test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a17test4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

                
    mydci = basic_defs.switch_session_qi_user5()         
    
    stmt = """drop role D_a17test3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
                
    stmt = """create role D_a17test5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt = """drop role D_a17test5;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt="""revoke role DB__ROOTROLE from qauser90 granted by DB__ROOT;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        
    mydci = basic_defs.switch_session_qi_user5()   
    
    stmt = """drop role D_a17test4;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')
                

    stmt = """revoke role D_a17test1 from qauser91 granted by qauser90;"""
    output = _dci.cmdexec(stmt)

    stmt = """revoke role D_a17test2 from qauser91 granted by qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test3;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a17test4;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  



           
def testa43(desc="""drop more than a role"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                         
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a18test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a18test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a18test3;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """create role D_a18test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a18test2 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
                
    stmt = """create role D_a18test3 with admin qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

        #drop more than a role in a stat
    stmt = """drop role D_a18test1,D_a18test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    stmt = """drop role D_a18test1,D_a18test3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """drop role D_a18test1,D_a18test3 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
                
    mydci = basic_defs.switch_session_qi_user5()    
    
    stmt = """drop role D_a18test1,D_a18test2 cascade;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')

    stmt = """drop role D_a18test1,D_a18test3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '15001')
                

    stmt = """drop role D_a18test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a18test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a18test3;"""
    output = _dci.cmdexec(stmt)
                
           
    _testmgr.testcase_end(desc)  
                
def testa44(desc="""An user have user administrative privileges for the roles can create and drop roles"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
                         
    stmt = """register user qauser90;"""
    output = _dci.cmdexec(stmt)
    stmt = """register user qauser91;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a19test1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a19test2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role D_a19test3;"""
    output = _dci.cmdexec(stmt)
                
    stmt = """create role D_a19test1 with admin qauser90;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create role D_a19test2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt = """grant component privilege manage_roles on SQL_OPERATIONS to qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    mydci = basic_defs.switch_session_qi_user2()    

    stmt = """create role D_a19test3;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   

    stmt = """grant role D_a19test1 to qauser92;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_error_msg(output, '1017')

    stmt = """grant role D_a19test2 to qauser92;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_error_msg(output, '1017')

    stmt = """grant role D_a19test3 to qauser92;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_complete_msg(output) 

    stmt = """revoke role D_a19test3 from qauser92;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_complete_msg(output) 

    stmt = """drop role D_a19test1;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_complete_msg(output) 

    stmt = """drop role D_a19test2;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_complete_msg(output) 

    stmt = """drop role D_a19test3;"""
    output = mydci.cmdexec(stmt)             
    mydci.expect_complete_msg(output) 

    stmt = """revoke component privilege manage_roles on SQL_OPERATIONS from qauser91;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 


    _testmgr.testcase_end(desc) 
