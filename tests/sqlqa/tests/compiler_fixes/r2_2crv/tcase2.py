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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Spurious warnings in EMS log during update statistics"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table cust1 like """ + gvars.g_schema_tpch2x + """.customer
with constraints with partitions;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = gvars.inscmd + """ cust1 (select * from """ + gvars.g_schema_tpch2x + """.customer);"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = """select count(*) from cust1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '300000')
    
    stmt = """update statistics for table cust1 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # cleanup
    stmt = """control query default ustat_log reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table cust1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

