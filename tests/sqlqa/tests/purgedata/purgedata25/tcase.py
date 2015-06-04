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
    
    stmt = """CQD HIST_MISSING_STATS_WARNING_LEVEL '0';"""
    output = _dci.cmdexec(stmt)
    #
    #                Purgedata 25
    #
    #   Purgedata from SQL TPCD tables
def test001(desc="""Purgedata from SQL TPCD tables."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """purgedata """ + defs.my_schema + """.customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.\"PART\";"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.nation;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """purgedata """ + defs.my_schema + """.region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from """ + defs.my_schema + """.customer;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.orders;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.part;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.partsupp;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.supplier;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.lineitem;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.nation;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """select count(*) from """ + defs.my_schema + """.region;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '0')
    
    stmt = """drop table """ + defs.my_schema + """.customer;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.orders;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.part;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.partsupp;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.supplier;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.lineitem;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.nation;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.region;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

