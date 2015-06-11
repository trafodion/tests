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
