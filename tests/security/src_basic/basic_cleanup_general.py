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
import basic_defs

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

    # It's easier to let super does all of these, even though schema was
    # created by user1
    _dci = basic_defs.switch_session_super_user()
    _dci.cleanup_schema(basic_defs.TestVars.test_schema_full)

    # If the tests have been allowed to run to the end, we shouldn't need
    # the following code, since each test should have done the necessary
    # cleanup at the end.  But sometimes the tests get interrupted in the
    # middle and there are roles left over.  The following code clears them.
    # All errors are ignored, as they have been cleared earlier.
    
    # The schema has been dropped.  All objects are cleared.  We don't have
    # to worry about revoking object privs one by one.
    
    # Revoke roles from users
    stmt = """revoke role \"""" + basic_defs.TestVars.myrole1 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
    output = _dci.cmdexec(stmt)
    stmt = """revoke role \"""" + basic_defs.TestVars.myrole2 + """\" from \"""" + basic_defs.TestVars.qi_user2 + """\";"""
    output = _dci.cmdexec(stmt)
    
    # Drop roles
    # Can't call super_drop_all_roles; that has expect in it.
    stmt = """drop role \"""" + basic_defs.TestVars.myrole1 + """\";"""
    output = _dci.cmdexec(stmt)
    stmt = """drop role \"""" + basic_defs.TestVars.myrole2 + """\";"""
    output = _dci.cmdexec(stmt)
    
