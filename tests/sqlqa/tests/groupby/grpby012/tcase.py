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
    
def test001(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select * from table (querycache());"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select plan_id from table (explain (null,'%')) group by plan_id;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select module_name from table (explain('grp_cat.grp_sch.emp','%')) group by module_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8809')
    
    stmt = """select statement_name from table (explain (null,'S%')) group by statement_name;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '8017')
    
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
   
    stmt = """select optimization_level from table (querycache()) group by optimization_level;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
      _dci.expect_selected_msg(output, 0)
    elif hpdci.tgtTR():
      _dci.expect_error_msg(output, '15001')
 
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """select * from table (querycacheentries());"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
      _dci.expect_selected_msg(output, 0)
    elif hpdci.tgtTR():
      _dci.expect_error_msg(output, '15001')
    
    stmt = """select plan_id from table (querycacheentries()) group by plan_id;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
      _dci.expect_selected_msg(output, 0)
    elif hpdci.tgtTR():
      _dci.expect_error_msg(output, '15001')
    
    stmt = """select optimization_level from table (querycacheentries()) group by optimization_level;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
      _dci.expect_selected_msg(output, 0)
    elif hpdci.tgtTR():
      _dci.expect_error_msg(output, '15001')
    
    stmt = """select num_hits from table (querycacheentries()) group by num_hits;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
      _dci.expect_selected_msg(output, 0)
    elif hpdci.tgtTR():
      _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

