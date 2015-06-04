# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

_testmgr = None
_testlist = []
_dci = None

# test007
# VALUES tests: The 3 USER commands & SQRT() in a values statement
#
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """values (cast (USER as char (20)),
cast (sqrt (443556) as dec (12,0))
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '666')
    
    stmt = """values (cast (CURRENT_USER as char (20)),
cast (sqrt (443556) as numeric (12,0))
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '666')
    
    stmt = """values (cast (SESSION_USER as char (20)),
cast (sqrt (443556) as smallint)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 1)
    _dci.expect_str_token(output, '666')
    
    # expect my name & 666 3 times
    
