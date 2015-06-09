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
    #default hpdci was created using 'SQL' as the proc name.
    # thisdefault instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()


def testa01(desc="""Length of <role-name> param below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = 'create role "1";'
    output = _dci.cmdexec(stmt)

    stmt = 'create role "_1";'
    output = _dci.cmdexec(stmt)

    stmt ='create role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127;'
    output = _dci.cmdexec(stmt)

    stmt ='create role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)

    stmt='grant role \"1\" to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='grant role \"_1\" to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='grant role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127,\"_1\" to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='grant role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role \"1\" from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='revoke role \"_1\" from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='revoke role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127,\"_1\" from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='revoke role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='drop role "1";'
    output = _dci.cmdexec(stmt)


    stmt='drop role "_1";'
    output = _dci.cmdexec(stmt)


    stmt='drop role qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127;'
    output = _dci.cmdexec(stmt)

    stmt='drop role  qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)   
    
def testa02(desc="""Length of <role-name> param blank, out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role  RER_a02role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)

    stmt='create role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;'
    output = _dci.cmdexec(stmt)

    stmt='create role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)

    stmt='grant role to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role  RER_a02role1, to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
 
    stmt='grant role ,  RER_a02role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 to qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='grant role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 to qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='grant role , qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 to qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    stmt='revoke role from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role  RER_a02role1, from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 from qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='revoke role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 from qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='revoke role , qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129 from qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')     

    stmt='drop role RER_a02role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456129;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='drop role qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')
    
    _testmgr.testcase_end(desc)   

def testa03(desc="""rolename valid chars"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='register user qauser3;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser4;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a03role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role dewqrq___3423532;'
    output = _dci.cmdexec(stmt)

    stmt='create role "Test";'
    output = _dci.cmdexec(stmt)

    stmt='create role "/test";'
    output = _dci.cmdexec(stmt)

    stmt='create role "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)


    stmt='grant role RER_a03role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role dewqrq___3423532, \"Test\" to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role \"/test\", "1289-_@./XYZabc" to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a03role1  from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role dewqrq___3423532, \"Test\" from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role \"/test\", "1289-_@./XYZabc" from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a03role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role dewqrq___3423532;'
    output = _dci.cmdexec(stmt)

    stmt='drop role "Test";'
    output = _dci.cmdexec(stmt)

    stmt='drop role "/test";'
    output = _dci.cmdexec(stmt)

    stmt='drop role "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)
    
    stmt='unregister user qauser3;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser4;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   

def testa04(desc="""rolename invalid chars"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a04role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role test;'
    output = _dci.cmdexec(stmt)

    stmt='create role "_AABB";'
    output = _dci.cmdexec(stmt)

    stmt='create role "_aabb";'
    output = _dci.cmdexec(stmt)
 
    stmt='create role "Avdcd"afet";'
    output = _dci.cmdexec(stmt)

    stmt='create role "@test1";'
    output = _dci.cmdexec(stmt)

    stmt='create role  \"^testa**$\";'
    output = _dci.cmdexec(stmt)

    stmt='create role " ";'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a04role1,test to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role \"_AABB\",\"_aabb\" to  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1351')

    stmt='grant role  \"Avdcd\"afet\",\" \", "@test1" to  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')


    stmt='grant role RER_a04role1,\" \" to  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3004');

    stmt='grant role RER_a04role1,\"_aabb\", \"_AABB\" to  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1351')


    stmt='revoke role RER_a04role1,test from  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role \"_AABB\",\"_aabb\" from  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1351')

    stmt='revoke role  \"Avdcd\"afet\",\" \", "@test1" from  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='revoke role RER_a04role1,\" \" from  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3004');

    stmt='revoke role RER_a04role1,\"_aabb\", \"_AABB\" from  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1351')


    stmt='drop role RER_a04role1;'    
    output = _dci.cmdexec(stmt)

    stmt='drop role test;'
    output = _dci.cmdexec(stmt)

    stmt='drop role "_AABB";'
    output = _dci.cmdexec(stmt)


    stmt='drop role "_aabb";'
    output = _dci.cmdexec(stmt)

    stmt='drop role "Avdcd"afet";'
    output = _dci.cmdexec(stmt)

    stmt='drop role "@test1";'
    output = _dci.cmdexec(stmt)

    stmt='drop role \"^testa**$\";'
    output = _dci.cmdexec(stmt)

    stmt='drop role " ";'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   

def testa05(desc="""grantee length below max"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='unregister user qauser5;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser6;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser7;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser8;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser9;'
    output = _dci.cmdexec(stmt)


    stmt='unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127;'
    output = _dci.cmdexec(stmt)


    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser5 as T;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser6 as T1;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser7 as "93";'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser8 as qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser9 as qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a05role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a05role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012346128;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a05role1 to T,T1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a05role2 to T,T1,"93";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a05role2,qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012346128 to qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127,qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a05role1 from T,T1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a05role2 from T,T1,"93";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a05role2,qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012346128 from qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127,qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='unregister user T;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user T1;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "93";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser_10123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201239127;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012349128;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a05role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a05role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012346128;'
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)   

  
def testa06(desc="""grantee length 0 out of max"""):
        
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt='unregister user qauser10;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a06role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a06role2;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser10;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a06role1 to;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a06role1 to granted by Current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008');

    stmt='grant role RER_a06role1 to qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='grant role RER_a06role1 to qauser1 ,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='grant role RER_a06role2 to qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')


    stmt='grant role RER_a06role1 to qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 granted by current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='revoke role RER_a06role1 from;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a06role1 from granted by Current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1008');

    stmt='revoke role RER_a06role1 from qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='revoke role RER_a06role1 from qauser10 ,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='revoke role RER_a06role2 from qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128,qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')

    stmt='revoke role RER_a06role1 from qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132 granted by current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')


    stmt='unregister user qauser_101234567820123456783012345678401234567850123456786012345678701234567880123456789012345671001234567110123456712012345128;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser_1012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120123456789132;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a06role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a06role2;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser10;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa07(desc="""grantee valid chars"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt='unregister user qauser1;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser2;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser3;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser4;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser5;'
    output = _dci.cmdexec(stmt)
    
    stmt='register user qauser1 as dewqrq___3423532;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser2 as "test";'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser3 as "_areqw3132";'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser4 as "1test1 ";'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser5 as "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a07role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a07role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a07role3;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a07role4;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a07role1 to dewqrq___3423532;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a07role1 to "test","_areqw3132";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a07role2 to dewqrq___3423532,\"1test1 \";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a07role3,RER_a07role4 to \"1test1 \","1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a07role1 from dewqrq___3423532;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a07role1 from "test","_areqw3132";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a07role2 from dewqrq___3423532,\"1test1 \";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a07role3,RER_a07role4 from \"1test1 \","1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='unregister user dewqrq___3423532;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "1test1 ";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "_areqw3132";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)
    
    stmt='unregister user "test";'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a07role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a07role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a07role3;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a07role4;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa08(desc="""grantee valid chars"""):
        
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt='unregister user qauser1;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser1 as "@test1";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='unregister user qauser2;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser2 as \"^testa**$\";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='unregister user qauser3 ;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser3 as "Avdcd"afet";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='unregister user qauser4;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser4 as 123qwe;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='unregister user qauser5;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser5 as "test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='unregister user qauser6;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser6 as "Test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334');

    stmt='create role RER_a08role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a08role2;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a08role1 to "test","@test1";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a08role2 to \"^testa**$\",\"test\",\"Test\";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a08role1 ,RER_a08role2 to 123qwe,\"Avdcd\"afet\";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='grant role RER_a08role1 ,RER_a08role2 to \"Avdcd\"afet\",123qwe;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='revoke role RER_a08role1 from "test","@test1";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a08role2 from \"^testa**$\",\"test\",\"Test\";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a08role1 ,RER_a08role2 from  123qwe,\"Avdcd\"afet\";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='revoke role RER_a08role1 ,RER_a08role2 from \"Avdcd\"afet\",123qwe;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')


    stmt='unregister user "test";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "@test1";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user \"^testa**$\";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "Avdcd"afet";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user 123qwe;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "TEST";'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a08role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a08role2;'
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)   
  
def testa09(desc="""missing keywords invalid keywords"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    
    stmt='create role RER_a09role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a09role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a09role3;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser1;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser2;'
    output = _dci.cmdexec(stmt)

    stmt='grant RER_a09role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a09role2 to qauser1 granted DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a09role3 granted by DB__ROOT to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role select to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role insert,select to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant create,delete, update to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a09role1 to qauser_tsang granted by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke RER_a09role1 from qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a09role2 from qauser_tsang granted DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a09role3 granted by DB__ROOT from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role select from  qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role insert,select from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke create,delete, update from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a09role1 from qauser_tsang granted by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='drop role RER_a09role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a09role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a09role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa10(desc="""missing comma separators using other separators"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a10role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a10role2;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a10role1 RER_a10role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt='grant role RER_a10role1,RER_a10role2 to qauser_tsang qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    stmt='grant role RER_a10role1.RER_a10role2 to qauser_tsang granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a10role1.RER_a10role2 to qauser_tsang.qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    stmt='revoke role RER_a10role1 RER_a10role2 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    
    stmt='revoke role RER_a10role1,RER_a10role2 from qauser_tsang qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    stmt='revoke role RER_a10role1.RER_a10role2 from qauser_tsang granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a10role1.RER_a10role2 from qauser_tsang.qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='drop role RER_a10role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a10role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa11(desc=""" multiple grantee in a stat"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a11role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create role RER_a11role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create role RER_a11role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='grant role RER_a11role1 to qauser_tsang ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a11role1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a11role2 to db__root,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1223');

    stmt='grant role RER_a11role3 to qauser_tsang, qauser_sqlqaa, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a11role1 from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='revoke role RER_a11role2 from db__root,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');


    stmt='revoke role RER_a11role3 from qauser_tsang, qauser_sqlqaa, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a11role1;'
    output = _dci.cmdexec(stmt)
    
    stmt='drop role RER_a11role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a11role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa12(desc="""options not yet supported"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a12role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a12role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a12role3;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a12role4;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a12role1 to group AA;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a12role2 to groups abc;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a12role1 to RER_a12role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340');

    stmt='grant role RER_a12role1 to qauser_tsang, public,current_role,group;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a12role3 to qauser_tsang,public,current_user with admin option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a12role4 to qauser_tsang granted by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a12role4 to qauser_sqlqaa granted by RER_a12role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340');

    #stmt='set connectopt role RER_a12role4;'
    #output = _dci.cmdexec(stmt)
    #_dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a12role1 from group AA;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a12role2 from groups abc;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a12role1 from RER_a12role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340');

    stmt='revoke role RER_a12role1 from qauser_tsang, public,current_role,group;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a12role3 from qauser_tsang,public,current_user with admin option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a12role4 from qauser_tsang granted by db__root;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a12role4 from qauser_sqlqaa granted by RER_a12role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340');


    stmt='drop role RER_a12role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a12role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a12role3;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a12role4;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa13(desc="""revoke predefined rolenames before from users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt='create role RER_a13role1;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a13role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role  DB__Useradmin to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');


    stmt='grant role DB__Useradmin,DB__admin to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='grant role DB__Useradmin,DB__admin to qauser_sqlqab, qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');


    stmt='revoke role RER_a13role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role  DB__Useradmin from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='revoke role DB__Useradmin,DB__admin from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='revoke role DB__Useradmin,DB__admin from qauser_sqlqab,qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='grant role DB__admin, public to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role DB__admin, public from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    stmt='revoke role DB__admin from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');


    stmt='grant role public to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role public from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role DB__Services to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='revoke role DB__Services from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='grant role none to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role none from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role current_role to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='revoke role current_role from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='grant role NONE, RER_a13role1 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role NONE, RER_a13role1 from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role \"_system\" to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='revoke role \"_system\" from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='grant role NONE,\"_system\",public,current_role to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role NONE,\"_system\",public,current_role from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='drop role RER_a13role1;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa14(desc="""revoke rolenames to predefine users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a14role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a14role2 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a14role3;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a14role4;'
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()  
    
    stmt='grant role RER_a14role1 to DB__Useradminuser ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333');

    stmt='revoke role RER_a14role1 from DB__Useradminuser ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333');


    stmt='grant role RER_a14role1 to DB__ROOT ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1223');

    stmt='revoke role RER_a14role1 from DB__ROOT ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='grant role RER_a14role2 to public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1355')

    stmt='revoke role RER_a14role2 from public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018')

    stmt='grant role RER_a14role3 to current_role;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')    


    stmt='revoke role RER_a14role3 from current_role;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')    


    stmt='grant role RER_a14role3 to current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a14role3 from current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')


    stmt='grant role RER_a14role3 to DB__useradmin, DB__admin;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')    


    stmt='revoke role RER_a14role3 from DB__useradmin, DB__ROOT;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')    



    stmt='grant role RER_a14role4 to DB__services;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')    


    stmt='revoke role RER_a14role4 from DB__services;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1333')    


    stmt='grant role RER_a14role4 to None;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt='revoke role RER_a14role4 from NONE;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='drop role RER_a14role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a14role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a14role3;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a14role4;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa15(desc="""revoke multiple roles from multiple users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a15role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a15role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a15role3;'
    output = _dci.cmdexec(stmt)


    stmt='grant role RER_a15role1 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a15role2,RER_a15role3 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a15role1,RER_a15role2,RER_a15role3 to qauser_sqlqab, qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a15role1 from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a15role2,RER_a15role3 from qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a15role1,RER_a15role2,RER_a15role3 from qauser_sqlqab, qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a15role1;'
    output = _dci.cmdexec(stmt)


    stmt='drop role RER_a15role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a15role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa16(desc="""grant multiple role revoke individually"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt='create role RER_a16role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a16role2;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a16role3;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a16role4;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a16role1,RER_a16role2 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a16role1,RER_a16role2 to qauser_sqlqab , qausertest;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    


    stmt='grant role RER_a16role1, RER_a16role2 to  qauser_teg ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

  
    stmt='revoke role RER_a16role1,RER_a16role2 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a16role1,RER_a16role2 from qauser_tsang, qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a16role3,RER_a16role4 from qauser_sqlqab,qausertest;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333');


    stmt='revoke role RER_a16role1 from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');


    stmt='revoke role RER_a16role2 from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');


    stmt='drop role RER_a16role1;'
    output = _dci.cmdexec(stmt)


    stmt='drop role RER_a16role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a16role3;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a16role4;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)   
  
def testa17(desc="""revoke roles from users be unregistered/offline"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='unregister user qauser22;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser23;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser24;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser25;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser22;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a17role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a17role2;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a17role3;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser23 as qauser23test;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser24 as qauser24test;'
    output = _dci.cmdexec(stmt)

    stmt='alter user qauser24test set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a17role1 to qauser22,qauser23test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a17role2 to qauser24test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a17role3 to qauser22 ,qauser25;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    


    stmt='grant role RER_a17role3 to qauser22; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a17role1 from qauser22,qauser23test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a17role2 from qauser24test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='revoke role RER_a17role3 from qauser22 ,qauser25;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    


    stmt='revoke role RER_a17role3 from qauser22 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='unregister user qauser22;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser23test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser24test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser25;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a17role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a17role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a17role3;'
    output = _dci.cmdexec(stmt)
   
    _testmgr.testcase_end(desc)   
     
def testa18(desc="""grantor unable to revoke all listed roles from all users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a18role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a18role2 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a18role3;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a18role4;'
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt='grant role RER_a18role1 to qauser_sqlqab, qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='grant role RER_a18role2 to qauser_sqlqab, qauser_sqlqaa, qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='grant role RER_a18role3,RER_a18role4 to qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a18role3 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a18role1 from qauser_sqlqaa , qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role  RER_a18role1 from qauser_tsang , qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')    


    stmt='revoke role RER_a18role3,RER_a18role4 from qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a18role3 from qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a18role4 from qauser_sqlqab, RER_a18role0 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333');

    stmt='revoke role RER_a18role0,RER_a18role2,RER_a18role4 from qauser_sqlqab restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1338');

    stmt='revoke role RER_a18role1,RER_a18role0 from qauser_sqlqaa,qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1338');

    stmt='revoke role RER_a18role3, RER_a18role4 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a18role2 from qauser_teg, qauser_sqlqaa, qauser_sqlqab cascade;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
	
    stmt='revoke role RER_a18role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

    stmt='revoke role RER_a18role1 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 

	
    stmt='revoke role RER_a18role3,RER_a18role4 from qauser_teg restrict;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a18role3 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='drop role RER_a18role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a18role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a18role3;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a18role4;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa19(desc="""revoke same role from same user in a stat"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a19role1;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a19role2;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a19role3;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a19role1 to current_user;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='grant role RER_a19role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a19role2 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a19role3 to public;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1355');

    stmt='revoke role  RER_a19role from current_user,current_user,qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role  RER_a19role1,RER_a19role1 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1351')

    stmt='revoke role  RER_a19role1 from qauser_tsang, qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1352');

    stmt='revoke role RER_a19role1,RER_a19role2,RER_a19role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1351')

    stmt='revoke role RER_a19role2 from qauser_tsang, qauser_sqlqaa,qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1352');

    stmt='revoke role RER_a19role3 from public, qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a19role1 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a19role2 from qauser_tsang, qauser_sqlqaa restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a19role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a19role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a19role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa20(desc="""revoke role from role itself revoke user from  user himself"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a20role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a20role2;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a20role1,RER_a20role2 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a20role1 from RER_a20role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340');

    stmt='revoke role RER_a20role1 from RER_a20role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1340');

    stmt='revoke qauser_tsang from role RER_a20role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke qauser_tsang from qauser32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke qauser_tsang from qauser33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role RER_a20role1,RER_a20role2 from qauser_tsang, qauser_sqlqaa cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='drop role RER_a20role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a20role2;'
    output = _dci.cmdexec(stmt)
 
    _testmgr.testcase_end(desc)   
    
def testa21(desc="""grant first revoke last"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a21role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a21role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a21role3;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a21role1 to qauser_tsang, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a21role2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a21role3 to qauser_sqlqaa, qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a21role3 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a21role3 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a21role1,RER_a21role2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a21role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='drop role RER_a21role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a21role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a21role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa22(desc="""alter user after granting revoke role from user"""):
        
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='unregister user qauser34;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser35;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser36;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser34 as qauser34test ;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser35 as qauser35test;'
    output = _dci.cmdexec(stmt)


    stmt='create role RER_a22role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a22role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a22role3;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a22role1 to qauser34test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a22role2,RER_a22role3 to qauser35test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='alter user qauser34test set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='alter user qauser34test set external name qauser36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='alter user qauser35test set external name qauser34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='revoke role RER_a22role1 from qauser36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    



    stmt='revoke role RER_a22role1 from qauser34test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a22role2,RER_a22role3 from qauser34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    


    stmt='revoke role RER_a22role2,RER_a22role3 from qauser35test restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='revoke role RER_a22role2 from qauser35test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a22role3 from qauser35test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='drop role RER_a22role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a22role3;'
    output = _dci.cmdexec(stmt)


    stmt='drop role RER_a22role2;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser34test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser35test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser36;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
  
def testa23(desc="""unregister user after granting role then revoke role"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='unregister user qauser37;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser38;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a23role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a23role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a23role3;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser37 as qauser37test;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser38 as qauser38test;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a23role2 to  qauser38test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='grant role RER_a23role1,RER_a23role3 to qauser37test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='unregister user qauser37;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    


    stmt='unregister user qauser38;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    


    stmt='unregister user qauser37test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1349');

    stmt='unregister user qauser38test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1349');

    stmt='revoke role RER_a23role1, RER_a23role3 from qauser37test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a23role2,RER_a23role3 from qauser38test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');
	
    stmt='revoke role RER_a23role2 from qauser38test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a23role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a23role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a23role3;'
    output = _dci.cmdexec(stmt)
	
    stmt='unregister user qauser37test;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser38test;'
    output = _dci.cmdexec(stmt)

    
    _testmgr.testcase_end(desc)   
    
  
def testa24(desc="""executed by user who does not have admin privilege and not role owner"""):
 
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a24role1 ;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a24role2 ;'
    output = _dci.cmdexec(stmt)

    stmt='grant role RER_a24role1 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a24role2 to qauser_sqlqaa, qauser_sqlqab ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2() 

    stmt='revoke role RER_a24role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a24role2 from qauser_sqlqaa, qauser_sqlqab ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');
    
    mydci = basic_defs.switch_session_qi_user3()     

    stmt='revoke role RER_a24role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a24role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a24role1 from qauser_sqlqaa restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a24role2 from qauser_sqlqaa, qauser_sqlqab cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a24role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a24role1;'
    output = _dci.cmdexec(stmt)
  
    _testmgr.testcase_end(desc)   
    
def testa25(desc="""executed by user who does not have admin privilege but role owner"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a25role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a25role2 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a25role3;'
    output = _dci.cmdexec(stmt)
	
    mydci = basic_defs.switch_session_qi_user2()   
    stmt='grant role RER_a25role1 to qauser_tsang, qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1223');

    stmt='grant role RER_a25role2 to  qauser_sqlqaa,db__root ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1223');

    stmt='grant role RER_a25role3 to qauser_sqlqaa,db__root ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='grant role RER_a25role1,RER_a25role3 to qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');


    stmt='revoke role RER_a25role1 from qauser_tsang, qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');


    stmt='revoke role RER_a25role2 ,RER_a25role3 from qauser_sqlqaa,db__root ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a25role3 from qauser_sqlqaa,db__root ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a25role2 from qauser_sqlqaa, db__root;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a25role1 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');


    stmt='revoke role RER_a25role1,RER_a25role3 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='drop role RER_a25role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a25role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a25role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa26(desc="""executed by user who has admin privilege but not role owner"""):
      
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a26role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a26role2 ;'
    output = _dci.cmdexec(stmt)


    stmt='grant role DB__rootrole to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a26role1 to  qauser_sqlqaa, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a26role1 to DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1223');


    stmt='grant role RER_a26role1,RER_a26role2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a26role2 to qauser_sqlqab by qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1017')    

    
    mydci = basic_defs.switch_session_qi_user2()  
    stmt='revoke role  RER_a26role1 from qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a26role2 from qauser_sqlqab ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt='revoke role  RER_a26role1 from qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a26role1 from qauser_sqlqaa,qauser_sqlqab by db__root;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');   
	
    stmt='revoke role RER_a26role1 from qauser_sqlqaa,qauser_sqlqab by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='revoke role RER_a26role1 from DB__ROOT;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    mydci = basic_defs.switch_session_qi_user3() 
    stmt='revoke role RER_a26role1,RER_a26role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a26role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a26role2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt='revoke role RER_a26role1 from  qauser_sqlqaa, qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='revoke role DB__rootrole from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a26role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a26role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)  
    
def testa27(desc="""grant special rolename to users"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role role;'
    output = _dci.cmdexec(stmt)

    stmt='create role "from";'
    output = _dci.cmdexec(stmt)

    stmt='create role logon;'
    output = _dci.cmdexec(stmt)

    stmt='create role granted ;'
    output = _dci.cmdexec(stmt)

    stmt='create role "by";'
    output = _dci.cmdexec(stmt)

    stmt='create role "to";'
    output = _dci.cmdexec(stmt)

    stmt='create role "user";'
    output = _dci.cmdexec(stmt)

    stmt='grant role role, \"from\", logon to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role role to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role granted to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role \"user\" to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role \"by\" to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role \"to\" to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role role, from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt='revoke role role,\"from\" from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role role from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='revoke role logon,granted, \"user\",\"by\",\"to\" from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role logon,granted from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='drop role role;'
    output = _dci.cmdexec(stmt)

    stmt='drop role "from";'
    output = _dci.cmdexec(stmt)

    stmt='drop role logon;'
    output = _dci.cmdexec(stmt)

    stmt='drop role granted;'
    output = _dci.cmdexec(stmt)

    stmt='drop role "user";'
    output = _dci.cmdexec(stmt)

    stmt='drop role "by";'
    output = _dci.cmdexec(stmt)

    stmt='drop role "to";'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa28(desc="""grant role by admin revoke role by owner"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a28role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a28role2;'
    output = _dci.cmdexec(stmt)

    stmt='grant role DB__rootrole to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='grant role RER_a28role1 to qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');


    stmt='grant role RER_a28role2 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    stmt='revoke role RER_a28role1,RER_a28role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a28role1 from qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='revoke role RER_a28role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    mydci = basic_defs.switch_session_qi_user3() 
	
    stmt='create role  RER_a28role3 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='grant role  RER_a28role3 to qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='grant role RER_a28role2 to qauser_sqlqab  ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');


    stmt='revoke role  RER_a28role2 from qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='revoke role RER_a28role1,RER_a28role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a28role1 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a28role1 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    mydci = basic_defs.switch_session_qi_user3() 
    stmt='revoke role RER_a28role3 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)    
    mydci.expect_complete_msg(output);

    stmt='revoke role DB__rootrole from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a28role2 from qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    
    stmt='drop role RER_a28role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a28role2;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a28role3;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa29(desc="""grant role by owner revoke role by other who has admin priv"""):
    
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a29role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a29role2;'
    output = _dci.cmdexec(stmt)


    stmt='grant role DB__rootrole to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a29role1 to qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt='grant role RER_a29role1 to qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='grant role RER_a29role1,RER_a29role2 to qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt='revoke role RER_a29role1 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');
	
    stmt='revoke role RER_a29role1 from qauser_sqlqab by db__root;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');
    
    stmt='revoke role  RER_a29role1 from qauser_sqlqab by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='revoke role DB__rootrole from qauser_sqlqaa ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a29role1;'
    output = _dci.cmdexec(stmt)


    stmt='drop role RER_a29role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa30(desc="""grant role by owner revoke role by admin"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a30role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a30role2 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='grant role DB__rootrole to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt='grant role RER_a30role1  to qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='grant role RER_a30role2 to qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);
    
    mydci = basic_defs.switch_session_qi_user3()     
    stmt='revoke role RER_a30role1 from  qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');
    
    stmt='revoke role RER_a30role1 from  qauser_sqlqab by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    mydci = basic_defs.switch_session_qi_user2()     
    stmt='revoke role RER_a30role1 from  qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a30role2 from qauser_teg;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role DB__rootrole from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='drop role RER_a30role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a30role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   

def testa31(desc="""after revoke consecutive grant"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a31role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a31role2 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='grant role RER_a31role1 to qauser_sqlqaa, qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);
    
    stmt='grant role RER_a31role1 to qauser_sqlqaa, qauser_sqlqab by db__root;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='revoke role RER_a31role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);


    stmt='revoke role RER_a31role1 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='grant role RER_a31role1 to qauser_sqlqaa, qauser_sqlqab by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a31role1 from qauser_sqlqaa, qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='grant role RER_a31role1 ,RER_a31role2 to qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017')    

    stmt='drop role RER_a31role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a31role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa32(desc="""revoke by one consecutive revoke by another"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a32role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a32role2;'
    output = _dci.cmdexec(stmt)

    stmt='grant role DB__rootrole to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt='grant role RER_a32role1 to qauser_sqlqab, qauser_teg ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt='grant role RER_a32role2 to  qauser_sqlqab;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a32role1 from qauser_sqlqab by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output)
    mydci.expect_error_msg(output, '1017')

    stmt='revoke role RER_a32role2 from qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')

    mydci = basic_defs.switch_session_qi_user3()     
    stmt='revoke role RER_a32role1 from qauser_sqlqab, qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018')

    stmt='revoke role RER_a32role1 from qauser_teg,qauser_sqlqab by qauser_tsang ;'
    output =_dci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    
    stmt='revoke role RER_a32role2 from qauser_sqlqab by db__root;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    stmt='revoke role DB__rootrole from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a32role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a32role2;'
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)   

def testa33(desc="""verify user's revoked role priv"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a33role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a33role2;'
    output = _dci.cmdexec(stmt)

    stmt='create shared schema RER_sch33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='set schema RER_sch33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant insert on tab1 to RER_a33role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select on tab1 to RER_a33role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a33role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a33role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    mydci = basic_defs.switch_session_qi_user2()     
    stmt='set schema RER_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='grant role RER_a33role2 to  qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='revoke role RER_a33role2 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sch33;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='drop schema RER_sch33 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt=' drop role RER_a33role1;'
    output = _dci.cmdexec(stmt)

    stmt=' drop role RER_a33role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa34(desc="""revoke part of role from user, verify user privilege"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a34role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a34role2;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a34role3;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a34role4;'
    output = _dci.cmdexec(stmt)

    stmt='create shared schema RER_sch34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='set schema RER_sch34;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table tab1(a int, b int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant insert(a) on tab1 to RER_a34role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select, insert(b) on tab1 to RER_a34role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant update(a) on tab1 to RER_a34role3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant delete on tab1 to RER_a34role4;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a34role1, RER_a34role2,RER_a34role3,RER_a34role4 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2()     
    stmt='set schema RER_sch34;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    


    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1);

    stmt='update tab1 set a=a+1 where b>0;'
    output = mydci.cmdexec(stmt)
    mydci.expect_updated_msg(output,1);

    stmt='delete from tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_deleted_msg(output,1);

    stmt='revoke role RER_a34role2,RER_a34role4 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    time.sleep(6)


    stmt='set schema RER_sch34 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1(a) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    


    stmt='insert into tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='update tab1 set a=a+1 where b>0;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '4481');


    stmt='delete from tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='revoke role RER_a34role1,RER_a34role3 from qauser_tsang cascade ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='set schema RER_sch34;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1(a) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='insert into tab1 values(1,1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(stmt, '4481');

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='update tab1 set a=a+1 where b>0;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');


    stmt='delete from tab1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='drop schema RER_sch34 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt=' drop role RER_a34role1;'
    output = _dci.cmdexec(stmt)

    stmt=' drop role RER_a34role2;'
    output = _dci.cmdexec(stmt)

    stmt=' drop role RER_a34role3;'
    output = _dci.cmdexec(stmt)

    stmt=' drop role RER_a34role4;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa35(desc="""revoke role restrict while objects still exists"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a35role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a35role2;'
    output = _dci.cmdexec(stmt)

    stmt='create shared schema RER_sch35;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sch35;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table a35tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt='insert into a35tab1 values(1,2);'
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output,1);

    stmt='grant insert on a35tab1 to RER_a35role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt='grant select on a35tab1 to RER_a35role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)    

    stmt='grant role RER_a35role1,RER_a35role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a35role2 to qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='set schema RER_sch35;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    

    
    stmt='insert into a35tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    

    
    stmt='select * from a35tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2);
	
    stmt='create view v1 as select * from a35tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
	
	
    mydci = basic_defs.switch_session_qi_user3() 
    stmt='set schema RER_sch35;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);
    
    stmt='select * from a35tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,2);


    stmt='revoke role RER_a35role1,RER_a35role2 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1364');


    stmt='revoke role RER_a35role1 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='revoke role RER_a35role2 from qauser_sqlqaa restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1364');
	

    stmt='drop schema RER_sch35 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt='revoke role RER_a35role2 from qauser_sqlqaa restrict;'
    output = _dci.cmdexec(stmt)	
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a35role1;'
    output = _dci.cmdexec(stmt)

    stmt='drop role RER_a35role2;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)   
    
def testa36(desc="""after drop objects revoke role from user restrict"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a36role1;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a36role2;'
    output = _dci.cmdexec(stmt)

    stmt='create shared schema RER_sche36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sche36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table tab1(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table tab2(col1 int, col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create view v1 as select * from tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create view v2 as select tab1.col1,tab2.col2 from tab1,tab2 where tab1.col2=tab2.col1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select on tab1 to RER_a36role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select, insert on tab2 to RER_a36role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select on v1 to RER_a36role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select on v2 to RER_a36role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a36role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='set schema RER_sche36;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  


    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='create view v11 as select * from tab1;'	
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from v1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');


    stmt='select * from v2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='revoke role RER_a36role1 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1364');
	
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='set schema RER_sche36;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
	
    stmt='drop view v11 cascade;'	
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
	
    stmt='revoke role RER_a36role1 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt='grant role RER_a36role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sche36;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='insert into tab2 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    


    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1);

    stmt='select * from v1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='select * from v2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='grant role RER_a36role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='set schema RER_sche36;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output, 0);

    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1);

    stmt='select * from v1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='select * from v2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='revoke role RER_a36role1 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='revoke role RER_a36role2 from qauser_tsang restrict;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt='drop schema RER_sche36 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a36role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a36role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)   
    
def testa37(desc="""revoke role from user cascade object created based on this role dropped"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a37role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create role RER_a37role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create shared schema RER_sche37;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sche37;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table tab1(col1 int,col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create table tab2(col1 int,col2 int)no partition;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='create view v1 as select * from tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select(col1) ,insert(col1,col2),delete on tab1 to RER_a37role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select on tab2 to RER_a37role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant select ,insert(col1) on v1 to RER_a37role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a37role1 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='set schema RER_sche37;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    


    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');
	
    stmt='create view v11 as select col1 from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='select col1 from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1);

    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from v1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');


    stmt='revoke role RER_a37role1 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='grant role RER_a61role2 to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	

    stmt='set schema RER_sche37;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)    
	
    stmt='select * from v11;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'4082');


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='select * from v1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0);

    stmt='insert into v1(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)    


    stmt='revoke role RER_a37role2 from qauser_tsang cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='set schema RER_sche37;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   


    stmt='insert into tab1 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='select * from v1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');

    stmt='insert into v1(col1) values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '4481');


    stmt='drop schema RER_sche37 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a37role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a37role2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)   
    
def testa38(desc="""grant same role to user by u1 u2 revoke role by u1"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a38role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='create role RER_a38role2 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)
    
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='grant role RER_a38role1,RER_a38role2 to qauser_sqlqaa;'     
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt='grant role RER_a38role1,RER_a38role2 to qauser_sqlqaa;' 
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt='revoke role RER_a38role1 from qauser_sqlqaa restrict;' 
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt='revoke role RER_a38role1 from qauser_sqlqaa cascade;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1350');

    stmt='revoke role RER_a38role2 from qauser_sqlqaa restrict;' 
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt='drop role RER_a38role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt='drop role RER_a38role2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)   

def testa39(desc="""user has admin role revoke role from himself twice"""):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a39role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)

    stmt='grant role db__rootrole to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)


    stmt='grant role  RER_a39role1 to qauser_tsang, qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1223');

    stmt='revoke role  RER_a39role1 from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    mydci = basic_defs.switch_session_qi_user2() 
    stmt='revoke role RER_a39role1 from qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a39role1 from qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1018');

    stmt='revoke role RER_a39role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1018');

    stmt='revoke role db__rootrole from qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='drop role RER_a39role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)   

    
def testa40(desc="""grant role WITH ADMIN OPTION """):

    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt='create role RER_a40role1 with admin qauser_tsang;'
    output = _dci.cmdexec(stmt)
	
    stmt='create role RER_a40role2 with admin qauser_sqlqaa;'
    output = _dci.cmdexec(stmt)

    stmt='grant role db__rootrole to qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt='grant role RER_a40role1 to qauser_sqlqaa with admin option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    stmt='grant role RER_a40role2 to qauser_sqlqab with admin option;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
	
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='grant role RER_a40role1 to qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
	
    stmt='grant role RER_a40role2 to qauser_teg by qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
	
    stmt='grant role RER_a40role2 to qauser_teg by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
	
    stmt='grant role RER_a40role2 to qauser_teg by qauser_tsang;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
	
    stmt='grant role RER_a40role2,RER_a40role1 to qauser_teg by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
		
    mydci = basic_defs.switch_session_qi_user3() 
    stmt='grant role RER_a40role1 to  qauser_sqlqab;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
    
    stmt='grant role RER_a40role2 to qauser_sqlqab with admin option;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  
	
    stmt='grant role RER_a40role2 to qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
	   
    mydci = basic_defs.switch_session_qi_user4()    
    stmt='grant role RER_a40role2,RER_a40role1 to qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
        
    mydci = basic_defs.switch_session_qi_user2() 
    stmt='revoke role RER_a40role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1330');
	
    stmt='revoke role RER_a40role1 from qauser_sqlqab by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 	
	
    stmt='revoke role RER_a40role1 from qauser_teg by qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 	
	
    stmt='revoke role RER_a40role1 from qauser_sqlqaa;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output) 	

    mydci = basic_defs.switch_session_qi_user3() 
    stmt='revoke role RER_a40role2 from qauser_sqlqab restrict;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1330'); 

    mydci = basic_defs.switch_session_qi_user4()    
    stmt='revoke role RER_a40role2 from qauser_teg;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  	
        
    mydci = basic_defs.switch_session_qi_user3() 
    stmt='revoke role RER_a40role2 from qauser_sqlqab,qauser_teg restrict;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  	
	
    stmt='drop role RER_a40role1 ;'
    output = _dci.cmdexec(stmt)
	
    stmt='drop role RER_a40role2;'
    output = _dci.cmdexec(stmt)	

    stmt='revoke  role db__rootrole from qauser_tsang;'
    output = _dci.cmdexec(stmt)	
	
	
    _testmgr.testcase_end(desc)   


  
