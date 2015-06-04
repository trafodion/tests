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
#  Description:        Create Table with [NOT] ENFORCED constraint.
#
#  Purpose:
#
#
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
    
def test001(desc="""Verify that NOT ENFORCED constraints are used for join elimination."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # join should be eliminated in this query
    stmt = """prepare s from select a1ne from t1ne,t2ne where fk1ne2ne=pk2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2NE*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # t2ne should be marked as an extra-hub table in this query
    stmt = """prepare s from select a1ne,a2ne from t1ne,t2ne where fk1ne2ne=pk2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2NE')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Test effect of ELIMINATE_REDUNDANT_JOINS 'MINIMUM'."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    # Setting CQD to 'MINIMUM' should prevent NOT ENFORCED constraints from being
    # used for join elimination/extra-hub marking.
    
    # change setting of ELIMINATE_REDUNDANT_JOINS.
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS 'MINIMUM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # join should not be eliminated
    stmt = """prepare s from select a1ne from t1ne,t2ne where fk1ne2ne=pk2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, '_scan*T2')
    
    # T2NE should be present, and not marked as extra-hub
    stmt = """prepare s from select a1ne,a2ne from t1ne,t2ne where fk1ne2ne=pk2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1NE')
    _dci.expect_any_substr(output, 'scan*.T2NE')
    _dci.expect_selected_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # Constraints explicitly marked ENFORCED should not be affected by this
    # CQD setting.
    
    # enforced constraint should cause redundant table to be eliminated
    stmt = """prepare s from select a1e from t1e,t2e where fk1e2e=pk2e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # enforced constraint should cause extra-hub table to be marked
    stmt = """prepare s from select a1e,a2e from t1e,t2e where fk1e2e=pk2e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1E')
    _dci.expect_selected_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2E')
    _dci.expect_selected_msg(output)
    
    # Restore original setting for ELIMINATE_REDUNDANT_JOINS.
    stmt = """control query default ELIMINATE_REDUNDANT_JOINS reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""Verify that NOT ENFORCED constraints are not enforced"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # insert rows into table referenced by unenforced constraint
    stmt = """insert into t2ne values(10, 1), (11, 2), (12, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # add rows to referencing table that match rows just inserted
    stmt = """insert into t1ne(pk1ne, fk1ne2ne) values(1, 10), (2, 11), (3, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # add row to referencing table that does not match; should get no error
    stmt = """insert into t1ne(pk1ne, fk1ne2ne) values (4, -47);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # delete a referenced row; no error
    stmt = """delete from t2ne where pk2ne=10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # change pk of a referenced row; no error
    stmt = """update t2ne set pk2ne=111 where pk2ne=11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # change fk to a value that does not match a row in referenced table; no error
    stmt = """update t1ne set fk1ne2ne=88 where fk1ne2ne=12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # restore table contents
    stmt = """delete from t1ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from t2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Check redundant joins when ENFORCED explicitly specified."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """prepare s from select a1e from t1e,t2e where fk1e2e=pk2e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2E*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s from select a1e,a2e from t1e,t2e where fk1e2e=pk2e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1E')
    _dci.expect_selected_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2E')
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Verify that RI is still maintained even when not enforced"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """drop table t2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1059')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Verify that SHOWDDL shows the unenforced RI constraint"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """showddl t1ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'FOREIGN KEY')
    _dci.expect_any_substr(output, 'FK1NE2NE')
    _dci.expect_any_substr(output, 'NOT ENFORCED')
    
    _testmgr.testcase_end(desc)

def test007(desc="""Verify that there is no change in RI behavior when ENFORCED"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # insert 3 rows into referenced table, and 3 matching rows in referencing table
    stmt = """insert into t2e values(10, 1), (11, 2), (12, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into t1e(pk1e, fk1e2e) values(1, 10), (2, 11), (3, 12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # insert non-matching row in referencing table; should fail
    stmt = """insert into t1e(pk1e, fk1e2e) values (4, -47);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    # delete referenced row from referenced table; should fail
    stmt = """delete from t2e where pk2e=10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    # update pk of referenced row to non-referenced value; should fail
    stmt = """update t2e set pk2e=111 where pk2e=11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    # update fk to a non-pk value; should fail
    stmt = """update t1e set fk1e2e=88 where fk1e2e=12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    # restore table contents
    stmt = """delete from t1e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from t2e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""Verify that index is created for RI constraint only when enforced"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """showddl t1e;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'system created index')
    _dci.expect_any_substr(output, 'FK1E2E ASC')
    
    stmt = """showddl t1ne;"""
    output = _dci.cmdexec(stmt)
    # _dci.unexpect_any_substr(output, 'system created index')
    _dci.unexpect_any_substr(output, 'FK1E2E ASC')
    
    _testmgr.testcase_end(desc)

def test009(desc="""Use a referential action with NOT ENFORCED; allowed, but meaningless"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table t1ner
(
pk1ner int not null not droppable primary key,
fk1ner2ne int references t2ne on update restrict on delete restrict not enforced,
a1ner int
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')
    _dci.expect_complete_msg(output)
    
    stmt = """showddl t1ner;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'FOREIGN KEY')
    _dci.expect_any_substr(output, 'FK1NER2NE')
    _dci.expect_any_substr(output, 'NOT ENFORCED')
    
    # make sure not enforced
    stmt = """insert into t1ner values(1,-4,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # make sure join elimination performed
    stmt = """prepare s from select a1ner from t1ner,t2ne where fk1ner2ne=pk2ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2NE*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # remove table created for this testcase
    stmt = """drop table t1ner;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""Use of [NOT] ENFORCED on non-RI constraints."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # make sure NOT ENFORCED isn't allowed for primary key constraints
    stmt = """create table terr(i int not null not droppable primary key not enforced);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3244')
    
    # illegal use of NOT ENFORCED on a NOT NULL constraint
    stmt = """create table terr(i int not null not droppable primary key,
j int not null not enforced);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3244')
    
    # invalid use of NOT ENFORCED in a table constraint
    stmt = """create table terr(i int not null not droppable primary key,
check(i>0) not enforced);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3244')
    
    # make sure gratuitous use of ENFORCED on a non-referential constraint doesn't affect it
    stmt = """create table terr(i int not null not droppable primary key check(i>0) enforced);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into terr values(0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    stmt = """drop table terr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""Duplicate RI constraint with different enforced attribute."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # add 2nd RI constraint on same column to same primary key with NOT ENFORCED,
    # make sure original one is not affected
    stmt = """alter table t1e add constraint ri_dup foreign key(fk1e2e) references t2e not enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t1e values(555, 555, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    _dci.unexpect_any_substr(output, 'RI_DUP')
    stmt = """alter table t1e drop constraint ri_dup;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """insert into t1e values(555, 555, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    _testmgr.testcase_end(desc)

