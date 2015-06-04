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
import defs

_testmgr = None
_testlist = []
_dci = None

# =================  Begin Test Case Header  ==================
#
#  Description:        Plan comparisons using ENFORCED/NOT ENFORCED RI constraints.
#
#  Purpose:            Verify absence of inlined subtrees for maintaining
#                      referential integrity when the RI constraint is
#                      unenforced.
#
# =================== End Test Case Header  ===================

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Delete from primary key table of enforced constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from delete from tplan_pk_e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*TPLAN_FK_E')
    
    _testmgr.testcase_end(desc)

def test002(desc="""Delete from primary key table of unenforced constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from delete from tplan_pk_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, '_scan')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Update primary key table of enforced constraint, changing key values"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from update tplan_pk_e set pk=?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*TPLAN_FK_E')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Update primary key table of unenforced constraint, changing key values"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """prepare s from update tplan_pk_ne set pk=?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, '_scan')
    
    _testmgr.testcase_end(desc)

def test005(desc="""Insert or update foreign key table of enforced constraint, setting fk values"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s_ins from insert into tplan_fk_e values(1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare s_upd from update tplan_fk_e set fk=?;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s_ins;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan')
    _dci.expect_any_substr(output, 'TPLAN_PK_E')
    stmt = """explain options 'f' s_upd;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Insert or update foreign key table of unenforced constraint, setting fk values"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """prepare s_ins from insert into tplan_fk_ne values(1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare s_upd from update tplan_fk_ne set fk=?;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s_ins;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, '_scan_unique')
    stmt = """explain options 'f' s_upd;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc="""Update primary key of referencing table of enforced constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # This causes delete/reinsert of the row (because PK value determines physical
    # location), along with the attendant RI checks.
    stmt = """prepare s from update tplan_fk_e set pk=?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'nested_join')
    
    _testmgr.testcase_end(desc)

def test008(desc="""Update primary key of referencing table of unenforced constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # This causes delete/reinsert of the row (because PK value determines physical
    # location), but should trigger no RI checks because the RI constraint is not
    # enforced.
    stmt = """prepare s from update tplan_fk_ne set pk=?;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    #TRAF _dci.unexpect_any_substr(output, 'nested_join')
    
    _testmgr.testcase_end(desc)

