# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
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


def testa01(desc="""Length of <dir-user-name> param below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = 'unregister user qauser1;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser2;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser1 set external name qauser2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user qauser1;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW2" AS "PAULLOW1";')


    stmt='alter user qauser1 set external name qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user qauser1;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER\n  "QA901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128"\n  AS "PAULLOW1";');


    stmt='alter user qauser1 set external name qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER\n  "QA911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127"\n  AS "PAULLOW1";');

    stmt='alter user qauser1 set external name QA912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user qauser1;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER\n  "QA912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126"\n  AS "PAULLOW1";');


    stmt='unregister user qauser2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')     

    stmt='unregister user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')     

    stmt='unregister user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')     

    stmt='unregister user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')     

    stmt='unregister user qauser1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    _testmgr.testcase_end(desc)  

def testa02(desc="""Length of <dir-user-name> param blank out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = 'unregister user qauser3;'
    output = _dci.cmdexec(stmt)

    stmt='register user qauser3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser3 set external name ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')     

    stmt='alter user qauser3 set external name qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='unregister user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='unregister user qauser3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    _testmgr.testcase_end(desc)  
    

def testa03(desc="""Length of <user-name> param below max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
		
    stmt = 'unregister user qauser4;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser5;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)


    stmt='register user qauser4;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser4 set external name qauser5;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser4;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128 set external name qauser5;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
 
    stmt='unregister user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)

    stmt='register user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127 set external name qauser5;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser4;'
    output = _dci.cmdexec(stmt)
    stmt='register user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)


    stmt='alter user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126 set external name qauser5;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='unregister user qauser4;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser5;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  
    
def testa04(desc="""Length of <user-name> param blank out of max"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='register user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser6;'
    output = _dci.cmdexec(stmt)


    stmt='alter user set external user qauser6;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 set external user qauser6;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='alter user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 set external user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='alter user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='alter user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130 offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3118')    

    stmt='unregsiter user qauser6;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qa921_7810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130;'
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)  
    
def testa05(desc="""<user-name> and <dir-user-name> valid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
 
    stmt='unregsiter user qauser90;'
    output = _dci.cmdexec(stmt)
    
    stmt='unregsiter user qauser80;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user A;'
    output = _dci.cmdexec(stmt)


    stmt='register user qauser90 as A;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user A set external name qauser80;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user A;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='register user qauser90 as "_";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user "_" set external name qauser80;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user "_";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='register user qauser90 as "set";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user "set" set external name qauser80;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='unregister user "set";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser90 as "test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user "test" set external name qauser80;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='unregister user "test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser90 as "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user  "1289-_@./XYZabc" set external name qauser80;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user  "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser90 as "/test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    
    stmt='alter user "/test" set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='unregister user "/test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='register user qauser90 as "_abb";'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user "_abb" set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user "_abb";'
    output = _dci.cmdexec(stmt)  

    _testmgr.testcase_end(desc)  
    
def testa06(desc="""missing keywords disorder of clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser7;'
    output = _dci.cmdexec(stmt)  

    stmt='unregister user qauser8;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser7  as qauser7test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser7test external name qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test set name qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test set external qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter qauser7test set external name qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test set qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test set name external qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test external set name  qauser8;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser7test offline set;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='unregister user qauser7;'
    output = _dci.cmdexec(stmt) 

    
    stmt='unregister user qauser8;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser7test;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  
    

def testa07(desc="""missing keywords disorder of clause"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser9;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser10;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser11;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser12;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser13;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser9 as qauser9test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser10 as qauser10test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    stmt='register user qauser11;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser9test,qauser10test set external name qauser11;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test set external name qauser12,qauser13;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test,qauser9test set external name qauser12;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test set external name qauser12test,qauser13;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test,qauser9test set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test,qauser10test set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test,qauser10test set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test set online,offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user qauser9test, qauser10test set external name qauser12, set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    


    stmt='unregister user qauser9test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser10test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser9;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser10;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser11;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser12;'
    output = _dci.cmdexec(stmt) 
    
    stmt='unregister user qauser13;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  
    
def testa08(desc="""alter <user-name> using  predefined name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser14;'
    output = _dci.cmdexec(stmt) 


    stmt='alter user DB__ROOT set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    

    stmt='alter user DB__UserAdminUser set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    

    stmt='alter user current_user set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    


    stmt='alter user DB__useradmin set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    


    stmt='alter user DB__services set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    

    stmt='alter user Public set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user "_system" set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    


    stmt='alter user current_role set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    

    stmt='alter user NONE set external name qauser14;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    stmt='alter user DB__ROOT set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    


    stmt='alter user DB__UserAdminUser set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    


    #stmt='alter user sqluser_admin set offline;'
    # self._odbc.expect_error_msg(stmt, 1333);


    #stmt='alter user $supername set offline;'
    #self._odbc.expect_error_msg(stmt, 1333);

    stmt='alter user current_user set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    

    #some predefine role 

    stmt='alter user DB__useradmin set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    


    stmt='alter user DB__admin set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    

    stmt='alter user DB__services set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')
    

    stmt='alter user Public set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='alter user "_system" set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1337')    

    stmt='alter user current_role set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')    

    stmt='alter user NONE set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')    
	
    stmt='alter user db__root set external name trafodion;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser14;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa09(desc="""alter username does not already exist"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser15;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser16;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser17;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser18;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a09role1;'
    output = _dci.cmdexec(stmt) 

    #db user has been unregsiter
    stmt='register user qauser15 as p15a09test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user p15a09test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user p15a09test1 set external name qauser18;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    


    stmt='alter user p15a09test1 set external name qauser17;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='alter user p15a09test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='alter user p15a09test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    #username exists as a dirusername, but not a dbusername
    stmt='register user qauser16 as p16a09test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser16 set external name qauser18;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser16 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser16 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    #username is a rolename

    stmt='create role a09role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    #stmt='alter user a09role1 set external name qauser18;'
    #self._odbc.expect_error_msg(stmt,1340);

    #stmt='alter user a09role1 set online;'
    #self._odbc.expect_error_msg(stmt, 1340)

    #stmt='alter user a09role1 set offline;'
    #self._odbc.expect_error_msg(stmt, 1340)

    stmt='unregister user p15a09test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p16a09test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user a09role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser15;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser16;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser17;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser18;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a09role1;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa10(desc="""alter username matches dirusername"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser19;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser20;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser19 set external name qauser20;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser19 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser20 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    #stmt='showddl user qauser20;'
    #self._odbc.expect_error_msg(stmt, 1333);

    stmt='showddl user qauser19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW20" AS "PAULLOW19";')


    stmt='unregister user qauser20;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='register user qauser19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')

    stmt='register user qauser19 as p19a10test1 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser19;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser20;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='unregister user p19a10test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    _testmgr.testcase_end(desc)  

def testa11(desc="""alter username does not match dirusername"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser21;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser22;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser21 as p21a11test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser21 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser21 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser21 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user p21a11test1 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p21a11test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user p21a11test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user p21a11test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW22" AS "P21A11TEST1";')


    stmt='unregister user P21a11TEST1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser22 as p21a11test2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser21 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser21 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    #re-use newdirusername that was once used by another user

    stmt='unregister user p21a11test2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser21 as p21a11test2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
 
    stmt='alter user qauser21 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='alter user qauser21 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user p21a11test2 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user p21a11test2 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user p21a11test2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW22" AS "P21A11TEST2";')


    #new dirusername changed to become the same as db username

    stmt='unregister user qauser21;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser22;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p21a11test2;'
    output = _dci.cmdexec(stmt) 


    stmt='register user qauser21 as qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user qauser21 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser21 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='register user qauser22 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt='alter user qauser22 set external name qauser22;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user qauser22 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    #stmt='showddl user qauser21 ;'
    #self._odbc.expect_error_msg(stmt, 1333)

    stmt='showddl user qauser22 ;'
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output, 'ALTER USER "PAULLOW22" SET OFFLINE;')

    stmt='unregister user qauser21;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser22;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p21a11test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p21a11test2;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa12(desc="""alter username to the same state"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser23;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser24;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser25;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser26;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser27;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser23;'
    output = _dci.cmdexec(stmt) 

    stmt='alter user qauser23 set external name qauser23;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    

    stmt='alter user qauser23 set external name qauser25;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser23 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser23 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser24 as p24a12test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p24a12test1 set external name  qauser24;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    

    stmt='alter user p24a12test1 set external name qauser25;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    

    stmt='alter user p24a12test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p24a12test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p24a12test1 set external name qauser26;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p24a12test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p24a12test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    stmt='register user qauser26 as p26a12test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    

    #after alter ,the original diruser can be used 

    stmt='register user qauser24 as p24a12test2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser27 as p26a12test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser23;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser24;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser25;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser26;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser27;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p24a12test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p24a12test2;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p26a12test1;'
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)  

def testa13(desc="""alter user that dirname does not already exist/or registered"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser28;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser29;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser30;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser28;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser29 as p29a13test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='create role a13role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='create schema sch1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='set schema sch1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='create table tab1(a int not null primary key);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser28 set external name qauser30;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    # dirname does not already exist
    stmt='alter user qauser28 set external name p28a13test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')
    


    stmt='alter user qauser28 set external name p29a13test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')
    


    stmt='alter user qauser28 set external name a13role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')
    

    #stmt='alter user qauser28 set external name $cat1;'
    #self._odbc.expect_error_msg(stmt, 1331)

    stmt='alter user qauser28 set external name "sch1";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')
    


    stmt='alter user qauser28 set external name tab1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')
    


    stmt='alter user qauser28 set external name qauser29;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    


    stmt='unregister user qauser28;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser29;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser30;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p29a13test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p30a13test1;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a13role1;'
    output = _dci.cmdexec(stmt) 
    
    stmt='drop schema sch1 cascade;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa14(desc="""register user using existingusername"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser31;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser32;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser33;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser34;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser35;'
    output = _dci.cmdexec(stmt) 

    stmt='create role a14role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt='register user qauser31 as p31a14test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='grant role a14role1 to  p31a14test1,qauser32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user p31a14test1 set external name qauser33;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser31 as p31a14test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    stmt='register user qauser31 as p31a14test2 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user qauser32 set external name qauser34; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='register user qauser35 as qauser32 ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1334')
    
    #stmt='showddl user qauser35;'
    #self._odbc.expect_error_msg(stmt, 1333)

    stmt='showddl user p31a14test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW33" AS "P31A14TEST1";')

    stmt='showddl user p31a14test2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW31" AS "P31A14TEST2";')


    stmt='unregister user qauser31;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1349')

    stmt='unregister user qauser33;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser34;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser35;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p31a14test1;'
    output = _dci.cmdexec(stmt) 
    _dci.expect_error_msg(output, '1349')

    stmt='unregister user p31a14test2;'
    output = _dci.cmdexec(stmt)

	
    stmt='revoke role a14role1 from  p31a14test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt='revoke role a14role1 from  qauser32;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 

    stmt='unregister user qauser32;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user p31a14test1;'
    output = _dci.cmdexec(stmt)
	
    stmt='drop role a14role1;'
    output = _dci.cmdexec(stmt)


    _testmgr.testcase_end(desc)  
    
def testa15(desc="""alter user username set online/offline after alter external name"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser36;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser37;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser38;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser37 as p37a15test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser36 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='alter user qauser36 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser36 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    stmt='unregister user qauser36;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user p37a15test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='register user qauser36 as p37a15test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser36 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser36 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser37 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser37 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user p37a15test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p37a15test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user p37a15test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW36" AS "P37A15TEST1";')

    #===alter user after alter external name

    stmt='alter user p37a15test1 set external name qauser37;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p37a15test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p37a15test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user p37a15test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW37" AS "P37A15TEST1";')


    stmt='alter user p37a15test1 set external name qauser38;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p37a15test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user p37a15test1 set online;' 
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='showddl user p37a15test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW38" AS "P37A15TEST1";')

    stmt='unregister user p37a15test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser36;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser37;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser38;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa16(desc="""executed others by user who does not have admin privilege"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser39;'
    output = _dci.cmdexec(stmt)  

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser39 as p39a16test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    mydci = basic_defs.switch_session_qi_user2()  

    stmt='alter user  p39a16test1 set online;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='alter user  p39a16test1 set offline;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='alter user  p39a16test1 set external name qauser41;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='showddl user p39a16test1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'REGISTER USER "PAULLOW39" AS "P39A16TEST1";');

 
    stmt='unregister user qauser39;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p39a16test1;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa17(desc="""executed by user himself but does not have other admin priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt)   

    mydci = basic_defs.switch_session_qi_user2()  
    
    stmt='alter user qauser_tsang set online;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='alter user qauser_tsang set external name qauser42;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');

    stmt='alter user qauser_tsang set offline;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output, '1017');
    
    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)  

def testa18(desc="""alter username by ordinary user has admin priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser43;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser44;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser45;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser46;'
    output = _dci.cmdexec(stmt) 

    stmt='grant role DB__rootrole to qauser_tsang granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  


    #stmt='alter user qauser43 set logon role DB__UserAdmin;'
    #self._odbc.expect_complete(stmt);

    mydci = basic_defs.switch_session_qi_user2() 
    
    stmt='create role a18role1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);


    stmt='register user qauser44 as p44a18test1 ;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);
    
    stmt='grant role a18role1 to p44a18test1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='alter user qauser_tsang set online;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    stmt='alter user qauser_tsang set offline;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);

    #stmt='alter user qauser_tsang set external name qauser45;'    
    #output = mydci.cmdexec(stmt)
    #mydci.expect_complete_msg(output);

    stmt='alter user p44a18test1 set offline;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);


    #stmt='alter user p44a18test1 set external name qauser45;'
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output,'1335');

    stmt='alter user p44a18test1 set external name qauser46;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output);


    stmt='revoke role a18role1 from p44a18test1 granted by qauser_tsang;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='revoke role db__rootrole from qauser_tsang granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='drop role a18role1;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user palllow44;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user qauser45;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user palllow46;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user p44a18test1;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc) 
    
def testa19(desc="""set all clauses all valid alter user clauses"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser47;'
    output = _dci.cmdexec(stmt) 
    stmt='unregister user qauser48;'
    output = _dci.cmdexec(stmt) 
    stmt='unregister user qauser49;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser47 as p47a19test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser47 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    stmt='alter user p47a19test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user p47a19test1 set external name qauser48;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user p47a19test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   


    stmt='showddl user p47a19test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW48" AS "P47A19TEST1";')

    #stmt='connect qauser47/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #self._odbc.test_connect('qauser48', 'QAPassword')

    stmt='alter user p47a19test1 set external name qauser49;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   


    #stmt='alter user p47a19test1 set logon role a19role1;'
    #self._odbc.expect_complete(stmt)


    stmt='showddl user p47a19test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW49" AS "P47A19TEST1";')

    #stmt='connect qauser47/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #stmt='connect qauser48/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #self._odbc.test_connect('qauser49', 'QAPassword')


    stmt='alter user p47a19test1 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   


    #stmt='alter user p47a19test1 set logon role none;'
    #self._odbc.expect_complete(stmt)


    stmt='showddl user p47a19test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW49" AS "P47A19TEST1";')

    #stmt='connect qauser47/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #stmt='connect qauser48/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #stmt='connect qauser49/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    stmt='alter user p47a19test1 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   


    #stmt='alter user p47a19test1 set logon role none;'
    #self._odbc.expect_complete(stmt) 

    stmt='showddl user p47a19test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW49" AS "P47A19TEST1";')

    #stmt='connect qauser47/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #stmt='connect qauser48/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #self._odbc.test_connect('qauser49', 'QAPassword')


    stmt='unregister user qauser47;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser48;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser49;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p47a19test1;'
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)  

def testa20(desc="""combine clause mix some invalid alter user clauses"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser50;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser51;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser52;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser53;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser50 as p50a20test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user qauser50 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    
    stmt='alter user qauser50 set external name qauser51;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')
    

    #self._odbc.test_connect('qauser50', 'QAPassword')

    #stmt='connect qauser51/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)


    stmt='alter user p50a20test1 set offline, set external name qauser51,;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='showddl user p50a20test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW50" AS "P50A20TEST1";')


    #self._odbc.test_connect('qauser50', 'QAPassword')

    #stmt='connect qauser51/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    stmt='register user qauser52;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user p50a20test1 set external name qauser52;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1335')
    

    stmt='showddl user p50a20test1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW50" AS "P50A20TEST1";')

    stmt='alter user qauser52 set external name qauser53 ,online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    #stmt='connect qauser51/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #self._odbc.test_connect('qauser52', 'QAPassword')

    stmt='unregister user qauser50;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser51;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser52;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser53;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p50a20test1;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a20role1;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  

def testa21(desc="""<user-name> and <dir-user-name> invalid chars"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser54;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser55;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser56;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser57;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser58;'
    output = _dci.cmdexec(stmt) 


    stmt='register user qauser54 as "^test";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    


    stmt='alter user "^test" set external name qauser55;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='register user qauser54 as _123;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='alter user _123 set external name qauser55;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='register user qauser54 as 12qqq;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='alter user 12qqq set external name qauser55;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='register user qauser54 as "Avdcd"afet";'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='alter user "Avdcd"afet" set external name qauser55;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15005')

    stmt='register user qauser54 as AABB;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user AABB set external name qauser55;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user aaBB set external name qauser56;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user "aabb" set external name qauser57;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='unregister user AABB;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser54 as test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    

    stmt='alter user test online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')

    stmt='alter user test offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3128')

    stmt='register user qauser58;'
    output = _dci.cmdexec(stmt) 

    stmt='alter user qauser58 set external name qauser58test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1331')
    

    stmt='unregister user "^test";'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user _123;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user 12qqq;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user "Avdcd"afet";'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user AABB;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser58test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser58;'
    output = _dci.cmdexec(stmt) 
	
    stmt='unregister user qauser54;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser55;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser56;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser57;'
    output = _dci.cmdexec(stmt) 

    _testmgr.testcase_end(desc)  
    
def testa22(desc="""alter user external name verify user existing priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser58;'
    output = _dci.cmdexec(stmt) 
    
    stmt='unregister user qauser59;'
    output = _dci.cmdexec(stmt) 
    
    stmt='register user qauser59 as qauser59test;'
    output = _dci.cmdexec(stmt) 


    stmt='create schema sch2;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    #mydci = basic_defs.switch_session_qi_user2()  
	
    _testmgr.create_dci_proc('qi_mxci6', _dci._target, _dci._dsn, 'qauser59', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci6')

    stmt='create table sch2.tab1(a int not null primary key);'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='alter user qauser59test set external name qauser58;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='showddl user qauser59test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW58" AS "PAULLOW59TEST";')


    stmt='grant role DB__rootrole to qauser59test granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    _testmgr.create_dci_proc('qi_mxci7', _dci._target, _dci._dsn, 'qauser58', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci7')
    #mydci = basic_defs.switch_session_qi_user3() 

    stmt='create table sch2.tab2(a int not null,b int)no partition;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='select * from sch2.tab1;'
    time.sleep(5)
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)   

    stmt='alter user qauser59test set online ; '
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   
	
    stmt='register user qauser59;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 	
	
    mydci = _testmgr.get_dci_proc('qi_mxci7')
	
    stmt='insert into sch2.tab1 values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)   

    stmt='select * from  sch2.tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)   
	
    #mydci = basic_defs.switch_session_qi_user2() 
    _testmgr.create_dci_proc('qi_mxci8', _dci._target, _dci._dsn, 'qauser59', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci8')
	
    stmt='insert into  sch2.tab1 values(2);'
    time.sleep(10)	
    output = mydci.cmdexec(stmt)	
    mydci.expect_error_msg(output,'4481')   

    stmt='select * from  sch2.tab2;'
    time.sleep(10)
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'4481') 
	
    stmt='drop schema sch2 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser58;'
    output = _dci.cmdexec(stmt)
	
    stmt='revoke role DB__rootrole from qauser59test ;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user qauser59test;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt='unregister user qauser59;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    _dci = _testmgr.delete_dci_proc('qi_mxci6')
    _dci = _testmgr.get_default_dci_proc()
    _dci = _testmgr.delete_dci_proc('qi_mxci7')
    _dci = _testmgr.get_default_dci_proc()
    _dci = _testmgr.delete_dci_proc('qi_mxci8')
    _dci = _testmgr.get_default_dci_proc()

    _testmgr.testcase_end(desc)  
    
def testa23(desc="""alter user online/offline verify user existing priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser60;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser61;'
    output = _dci.cmdexec(stmt) 
	
    stmt='register user qauser61;'
    output = _dci.cmdexec(stmt) 
    
    stmt='create schema sch3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='set schema sch3;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='create table sch3.tab1(col1 int not null primary key);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='grant select on sch3.tab1 to qauser61;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser61 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser61 set offline;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser61 set external name qauser60;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser61 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    stmt='showddl user  qauser60;'
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1333')

    stmt='showddl user qauser61;'
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW60" AS "PAULLOW61";')

    #mydci = basic_defs.switch_session_qi_user2() 

    #stmt='select * from sch3.tab1;'
    #output = mydci.cmdexec(stmt)
    #mydci.expect_error_msg(output,'4481')  
    
    _testmgr.create_dci_proc('qi_mxci10', _dci._target, _dci._dsn, 'qauser60', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci10')

    stmt='select * from sch3.tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)  
    
    stmt='drop schema sch3 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='unregister user qauser60;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser61;'
    output = _dci.cmdexec(stmt) 

    _dci = _testmgr.delete_dci_proc('qi_mxci10')
    _dci = _testmgr.get_default_dci_proc()


    _testmgr.testcase_end(desc)  
    
   
def testa24(desc="""register user by a user alter user by another(p/n)"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser66;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser67;'
    output = _dci.cmdexec(stmt) 

    stmt='grant role DB__rootrole to qauser_tsang,qauser_sqlqaa granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
 

    stmt='create role a24role1;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    mydci = basic_defs.switch_session_qi_user2() 

    stmt='register user qauser66 as p66a24test1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    mydci = basic_defs.switch_session_qi_user3() 

    stmt='alter user qauser66 set online;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1333')  

    stmt='alter user p66a24test1 set online;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='alter user p66a24test1 set external name qauser67; '
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='grant role a24role1 to p66a24test1 granted by DB__root;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    mydci = basic_defs.switch_session_qi_user4() 

    stmt='alter user p66a24test1 set offline;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1017')  


    stmt='alter user p66a24test1 set external name qauser67;'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'1017')  


    mydci = basic_defs.switch_session_qi_user2() 

    stmt='showddl user p66a24test1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'REGISTER USER "PAULLOW67" AS "P66A24TEST1";');
    
    stmt='revoke role DB__rootrole from qauser_tsang granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
	
    stmt='revoke role DB__rootrole from qauser_sqlqaa granted by DB__ROOT;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  	

    stmt='unregister user qauser66;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser67;'
    output = _dci.cmdexec(stmt) 

    stmt='revoke role a24role1 from  p66a24test1 ;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a24role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p66a24test1;'
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)  

def testa25(desc="""DB__ROOT alter user"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 
	
    stmt='unregister user qauser68;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser69;'
    output = _dci.cmdexec(stmt) 

    stmt='register user qauser68;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser68 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='alter user qauser68 set external name qauser69;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    #stmt='connect qauser68/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    #mydci = basic_defs.switch_session_qi_user3() 
    _testmgr.create_dci_proc('qi_mxci6', _dci._target, _dci._dsn, 'qauser69', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci6')

    stmt='showddl user qauser68;'
    output = mydci.cmdexec(stmt)
    mydci.expect_any_substr(output,'REGISTER USER "PAULLOW69" AS "PAULLOW68";');


    stmt='alter user qauser68 set offline ;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    #stmt='connect qauser69/QAPassword;'
    #self._odbc.expect_error_msg(stmt, 8837)

    stmt='showddl user qauser68;'
    output = _dci.cmdexec(stmt) 
    _dci.expect_any_substr(output,'REGISTER USER "PAULLOW69" AS "PAULLOW68"');

    stmt='unregister user PAULLOW68;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user PAULLOW69;'
    output = _dci.cmdexec(stmt)
	
	
    _dci = _testmgr.delete_dci_proc('qi_mxci6')
    _dci = _testmgr.get_default_dci_proc()
    
    
    _testmgr.testcase_end(desc)  

      
def testa26(desc="""alter user online/offline, external name verify user existing priv"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt='unregister user qauser70;'
    output = _dci.cmdexec(stmt) 
	
    stmt='unregister user qauser71;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser72;'
    output = _dci.cmdexec(stmt) 
	
    stmt='register user qauser71;'
    output = _dci.cmdexec(stmt) 
	
    stmt='register user qauser72;'
    output = _dci.cmdexec(stmt) 

    stmt='create schema sch7;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='set schema sch7;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='create table sch7.tab1(a int not null primary key);'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='grant select on sch7.tab1 to  qauser71;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  
    
    #mydci = basic_defs.switch_session_qi_user2() 
	
    _testmgr.create_dci_proc('qi_mxci6', _dci._target, _dci._dsn, 'qauser71', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci6')

    stmt='set schema sch7;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt='create table tab2(b int not null primary key, c int);'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)


    stmt='grant insert,select on tab2 to qauser72;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)

    stmt='insert into tab1 values(1);'
    output = mydci.cmdexec(stmt)
    mydci.expect_error_msg(output,'4481')

    stmt='set schema sch7;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)  

    stmt='grant insert on tab1 to  qauser71;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user qauser71 set offline; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='alter user qauser71 set external name qauser70; '
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   
    
    _testmgr.create_dci_proc('qi_mxci7', _dci._target, _dci._dsn, 'qauser72', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci7')
    
    stmt='set schema sch7;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)  

    stmt='insert into tab2 values(1,2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)  

    stmt='select * from tab2;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,1)


    stmt='alter user qauser71 set online;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    #mydci = basic_defs.switch_session_qi_user4() 
    _testmgr.create_dci_proc('qi_mxci9', _dci._target, _dci._dsn, 'qauser70', 'QAPassword','')
    mydci = _testmgr.get_dci_proc('qi_mxci9')

    stmt='set schema sch7;'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   

    stmt='create table tab3(b int not null primary key, c int,d varchar(10));'
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)   

    stmt='select * from tab1;'
    output = mydci.cmdexec(stmt)
    mydci.expect_selected_msg(output,0)   

    stmt='insert into tab1 values(2);'
    output = mydci.cmdexec(stmt)
    mydci.expect_inserted_msg(output,1)   

    stmt='drop schema sch7 cascade;'
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)   

    stmt='unregister user qauser71;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser72;'
    output = _dci.cmdexec(stmt) 
	
    stmt='unregister user qauser70;'
    output = _dci.cmdexec(stmt)
	
    _dci = _testmgr.delete_dci_proc('qi_mxci9')
    _dci = _testmgr.get_default_dci_proc()
	
    _dci = _testmgr.delete_dci_proc('qi_mxci7')
    _dci = _testmgr.get_default_dci_proc()
	
    _dci = _testmgr.delete_dci_proc('qi_mxci6')
    _dci = _testmgr.get_default_dci_proc()
	
	
    
    _testmgr.testcase_end(desc)  

def testa27(desc="""clean up"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return 

    stmt = 'unregister user qauser1;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser2;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa901_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120_____128;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa911_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120____127;'
    output = _dci.cmdexec(stmt)

    stmt ='unregister user qa912_781012345678201234567830123456784012345678501234567860123456787012345678801234567890123456710012345671101234567120___126;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser3;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser4;'
    output = _dci.cmdexec(stmt)

    stmt = 'unregister user qauser5;'
    output = _dci.cmdexec(stmt)


    stmt='unregister user qauser6;'
    output = _dci.cmdexec(stmt)

    stmt='unregsiter user qauser90;'
    output = _dci.cmdexec(stmt)
    
    stmt='unregsiter user qauser80;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user A;'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "set";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user "test";'
    output = _dci.cmdexec(stmt)

    stmt='unregister user  "1289-_@./XYZabc";'
    output = _dci.cmdexec(stmt)


    stmt='unregister user "/test";'
    output = _dci.cmdexec(stmt)


    stmt='unregister user "_abb";'
    output = _dci.cmdexec(stmt)  

    stmt='unregister user qauser7;'
    output = _dci.cmdexec(stmt) 

    
    stmt='unregister user qauser8;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser7test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser9test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser10test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser9;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser10;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser11;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser12;'
    output = _dci.cmdexec(stmt) 
    
    stmt='unregister user qauser13;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser14;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p15a09test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p16a09test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user a09role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser15;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser16;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser17;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser18;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a09role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser19;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser20;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser21;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser22;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p21a11test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p21a11test2;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser23;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser24;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser25;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser26;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser27;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p24a12test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p24a12test2;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p26a12test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p19a10test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser28;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser29;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser30;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p29a13test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p30a13test1;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a13role1;'
    output = _dci.cmdexec(stmt) 


    stmt='unregister user qauser31;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser32;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser33;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser34;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser35;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p31a14test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p31a14test2;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p37a15test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser36;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser37;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser38;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser39;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser40;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p39a16test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser41;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser42;'
    output = _dci.cmdexec(stmt) 


    stmt='drop role a18role1;'
    output = _dci.cmdexec(stmt) 
    
    stmt='unregister user qauser43;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user palllow44;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user qauser45;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user palllow46;'
    output = _dci.cmdexec(stmt) 
 
    stmt='unregister user p44a18test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser47;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser48;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser49;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p47a19test1;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a19role1;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a19role2;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser50;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser51;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser52;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser53;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p50a20test1;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a20role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user "^test";'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user _123;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user 12qqq;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user "Avdcd"afet";'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user AABB;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser58test;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser54;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser55;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser56;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser57;'
    output = _dci.cmdexec(stmt) 



    stmt='unregister user qauser58;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser59;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p58a22test1;'
    output = _dci.cmdexec(stmt) 


    stmt='unregister user qauser60;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser61;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser62;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a24role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p64a24test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p65a24test1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user p66a24test1;'
    output = _dci.cmdexec(stmt) 


    stmt='unregister user qauser68;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser69;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a25role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser68;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser69;'
    output = _dci.cmdexec(stmt) 

    stmt='drop role a25role1;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser70;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser71;'
    output = _dci.cmdexec(stmt) 

    stmt='unregister user qauser72;'
    output = _dci.cmdexec(stmt) 

    stmt='drop schema sch1 cascade;'
    output = _dci.cmdexec(stmt) 

    stmt='drop schema sch2 cascade;'
    output = _dci.cmdexec(stmt) 

    stmt='drop schema sch3 cascade;'
    output = _dci.cmdexec(stmt) 

    stmt='drop schema sch7 cascade;'
    output = _dci.cmdexec(stmt) 
    
    _testmgr.testcase_end(desc)  

