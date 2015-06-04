# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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

import pd15004_ddl
from ...lib import hpdci
from ...lib import gvars
import defs

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
    
    pd15004_ddl._init(_testmgr)
    
    ##sh import ${my_schema}.pd15004 -I ${qagdata1}/dat10500
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd15004 select * from """ + gvars.g_schema_cmureg + """.dat10500;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd15004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, '10500')
