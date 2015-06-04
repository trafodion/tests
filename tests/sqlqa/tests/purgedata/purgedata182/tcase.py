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

import pd182_ddl
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

#
#                       purgedata182
#
#    A1: SQL utility purgedata -- Limit test.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""purgedata from a table with 512 partitions."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    pd182_ddl._init(_testmgr)
    
    ##sh import ${my_schema}.pd182 -I ${qagdata1}/big210.dat -C 12800
    stmt = gvars.inscmd + """ """ + defs.my_schema + """.pd182 select * from """ + gvars.g_schema_cmureg + """.big210a;"""
    output = _dci.cmdexec(stmt)

    stmt = """select count(*) from """ + defs.my_schema + """.pd182;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '12800')
    
    # purgedata the table to other catalog.
    stmt = """purgedata """ + defs.my_schema + """.pd182;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from """ + defs.my_schema + """.pd182;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """drop table """ + defs.my_schema + """.pd182;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #                   End of test case purgedata182
    _testmgr.testcase_end(desc)

