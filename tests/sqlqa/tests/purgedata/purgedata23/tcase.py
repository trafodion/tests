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
#                       PURGEDATA23
#
#    A1: Purgedata from SQL tables with both views.
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""PURGEDATA from partitioned SQL table with views."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #updated: 05/20/2008: R3 doesn't support partition level purgedata ('where' clause not supported)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23016;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23064;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """PURGEDATA """ + defs.my_schema + """.pd23210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from """ + defs.my_schema + """.pd23001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23016;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23032;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23064;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23128;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select * from """ + defs.my_schema + """.pd23210;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """drop view """ + defs.my_schema + """.pd23001v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23002v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23004v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23008v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23016v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23032v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23064v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23128v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view """ + defs.my_schema + """.pd23210v1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table """ + defs.my_schema + """.pd23001;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23002;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23004;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23008;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23016;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23032;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23064;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23128;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table """ + defs.my_schema + """.pd23210;"""
    output = _dci.cmdexec(stmt)
    
    #                   End of test case PURGEDATA23
    _testmgr.testcase_end(desc)

