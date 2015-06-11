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

import time
from ...lib import hpdci
from ...lib import gvars
import basic_defs

_testmgr = None
_testlist = []
_dci = None

# Default Test Body

# Create & grant role(s)
# super user
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
   

def mytest(super_grant_test_roles, super_revoke_test_roles,
           user1_revoke_test_privs, super_revoke_test_privs,
           user2_check_cache, user3_check_cache,
           user2_exec_expect_what, user3_exec_expect_what):

    basic_defs.super_create_all_roles()

    super_grant_test_roles()
    
    # Grant priv, the query should work.
    # user1
    basic_defs.user1_grant_all_privs_to_all()
    
    # user2
    mydci = basic_defs.switch_session_qi_user2()
    user2_qryqid = basic_defs.prepare_test_query(mydci)
    
    # user3
    mydci = basic_defs.switch_session_qi_user3()
    user3_qryqid = basic_defs.prepare_test_query(mydci)
    
    # Revoke priv, the query should not work.
    # user1
    user1_revoke_test_privs()

    # super
    super_revoke_test_privs()
    
    # user2
    mydci = basic_defs.switch_session_qi_user2()
    #user2_check_cache(mydci)
    stmt = """begin work;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = mydci.cmdexec(stmt)
    user2_exec_expect_what(mydci, output)
    stmt = """rollback work;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
   
    # verify AQR counters from rms
    #basic_defs.verify_aqr_counters(mydci, user2_qryqid)
  
    # user3
    # QI hashes security invalidation keys.  Two <subject,object,priv> keys may
    # end up with the same hash value.  It means that false positive AQR
    # recompilation of a different query is possible.  However, we also know
    # that it only hashes the object part.  Since user3 and user2 are two
    # different subjects, we should be able to check that AQR does not occur.
    mydci = basic_defs.switch_session_qi_user3()
    #user3_check_cache(mydci)
    stmt = """begin work;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
    stmt = """execute xx;"""
    output = mydci.cmdexec(stmt)
    user3_exec_expect_what(mydci, output)
    stmt = """rollback work;"""
    output = mydci.cmdexec(stmt)
    mydci.expect_complete_msg(output)
   
    # verify AQR counters from rms
    #basic_defs.verify_aqr_counters(mydci, user3_qryqid)
    
    # Grant priv again, the query should work again.
    # user1
    # WST #call switch_session_qi_user1
    # WST $SQL_complete_msg
    # WST grant ${testop} on mytable1 to "$qi_user2";
    
    # user2
    # WST #call switch_session_qi_user2
    # WST #unexpect any *ERROR*
    # WST execute xx;
    # WST #call prepare_test_query
    
    # Clean up
    # user1
    basic_defs.user1_revoke_all_privs_from_all()
    
    # super user
    super_revoke_test_roles()
    basic_defs.super_drop_all_roles()
    
    # This is necessary so that the effect of the revokes done in the cleanup
    # can be felt before the next test starts to compile the query.  Otherwise,
    # it will interfere with the next test (CR 5464)
    time.sleep(basic_defs.qi_rvkrole_sleeptime)
    
