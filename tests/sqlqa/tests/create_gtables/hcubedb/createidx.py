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
    
def test001(desc='create indexes'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # stmt = """control query default pos_num_of_partns '1';"""
    # output = _dci.cmdexec(stmt)
    stmt = """create index ix6b on t6(b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix6c on t6(c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix7b on t7(b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix7c on t7(c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix8b on t8(b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix8c on t8(c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix9b on t9(b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix9c on t9(c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix10b on t10(b) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ix10c on t10(c) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stmt = """control query default pos_num_of_partns '4';"""
    # output = _dci.cmdexec(stmt)
    stmt = """create index ixcube1d on cube1(d)
attribute extent (30, 30), maxextents 400
hash partition
no populate
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ixcube1e on cube1(e)
attribute extent (30, 30), maxextents 400
hash partition
no populate
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create index ixcube1f on cube1(f)
attribute extent (30, 30), maxextents 400
hash partition
no populate
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """populate index ixcube1d on cube1;"""
    output = _dci.cmdexec(stmt)
    stmt = """populate index ixcube1e on cube1;"""
    output = _dci.cmdexec(stmt)
    stmt = """populate index ixcube1f on cube1;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

