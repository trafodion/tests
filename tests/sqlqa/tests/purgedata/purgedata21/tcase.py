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

#
#                       PURGEDATA21
#
#    A1: Purgedata from a multi-partitioned SQL table.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""PURGEDATA from multi-partitioned SQL table."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21016;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21064;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """PURGEDATA """ + defs.my_schema + """.pd21210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + defs.my_schema + """.pd21001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21016;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21064;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """select * from """ + defs.my_schema + """.pd21210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop table """ + defs.my_schema + """.pd21001;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21002;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21004;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21008;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21016;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21032;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21064;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21128;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd21210;"""
    output = _dci.cmdexec(stmt)
    
    #                   End of test case PURGEDATA21
    _testmgr.testcase_end(desc)

