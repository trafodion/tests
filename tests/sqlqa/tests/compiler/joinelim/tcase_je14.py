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
#  Description:        ALTER TABLE with [NOT] ENFORCED constraint.
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
    
def test001(desc="""Add unenforced RI constraint and make sure it behaves as expected."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """alter table t1alt add constraint ne foreign key(fk1alt2alt) references t2alt not enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')
    _dci.expect_complete_msg(output)
    
    # add data that violates the constraint
    stmt = """insert into t2alt values(1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into t1alt(pk1alt, fk1alt2alt) values(1,-1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # ensure that the constraint is used for join elimination
    stmt = """prepare s from select a1alt from t1alt,t2alt where fk1alt2alt=pk2alt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #unexpect any *_scan*T2ALT*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    
    # ensure that the constraint is used for extra-hub marking
    stmt = """prepare s from select a1alt, a2alt from t1alt,t2alt where fk1alt2alt=pk2alt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T2ALT')
    
    # remove the constraint created for this testcase
    stmt = """alter table t1alt drop constraint ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Drop/add to try to make constraint enforced when not consistent"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # first create the RI constraint as NOT ENFORCED
    stmt = """alter table t1alt add constraint ne foreign key(fk1alt2alt) references t2alt not enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')
    _dci.expect_complete_msg(output)
    
    # now drop the constraint
    stmt = """alter table t1alt drop constraint ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # add it back as ENFORCED; should fail validity check
    stmt = """alter table t1alt add constraint ne foreign key(fk1alt2alt) references t2alt enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1143')
    
    # try same add without ENFORCED keyword; should get same failure
    stmt = """alter table t1alt add constraint ne foreign key(fk1alt2alt) references t2alt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1143')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Add multi-column unenforced RI constraint and make sure it behaves as expected."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # add a multi-col unenforced referential constraint
    stmt = """alter table t1alt add constraint ne_m4 foreign key(fk4a,fk4b,fk4c) references m4 not enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')
    _dci.expect_complete_msg(output)
    
    # insert data that violates the unenforced constraint
    stmt = """insert into t1alt(pk1alt,fk4a,fk4b,fk4c) values(2,98,99,100);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into m4 values(98,99,100, 'm4:98/99/100');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    # ensure that the constraint is used for join elimination
    stmt = """prepare s from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    #unexpect any *_scan*M4*
    stmt = """explain options 'f' s;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1ALT')
    _dci.expect_selected_msg(output)
    
    # ensure that the constraint is used for extra-hub marking
    stmt = """prepare s from select a1alt, v4 from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute hub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.T1ALT')
    _dci.expect_selected_msg(output)
    stmt = """execute extrahub;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, 'scan*.M4')
    _dci.expect_selected_msg(output)
    
    # delete referenced row, no error
    stmt = """delete from m4 where pk4a=98;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # remove the constraint created for this testcase
    stmt = """alter table t1alt drop constraint ne_m4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""Verify that adding an unenforced RI constraint affects similarity check for query caching."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # prepare statement used to check for use of cached plan
    stmt = """prepare IsCachedPlanUsed from
select distinct 'Cached plan used'
from table(explain(NULL,?)) x
where plan_id
= (select distinct plan_id from table(explain(NULL,?)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # turn query cache on
    stmt = """control query default QUERY_CACHE '4096';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # prepare same query twice with different statement ids, make sure same plan used
    stmt = """prepare s  from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare sx from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute isCachedPlanUsed using 'S', 'SX';"""
    output = _dci.cmdexec(stmt)
    
    # add the unenforced RI constraint, and prepare the same statement again with the sx statement id
    stmt = """alter table t1alt add constraint ne_m4 foreign key(fk4a,fk4b,fk4c) references m4 not enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')
    _dci.expect_complete_msg(output)
    stmt = """prepare sx from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # this time, the cached plan should have been invalidated
    stmt = """execute isCachedPlanUsed using 'S', 'SX';"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'Cached plan used')
    
    # turn query caching back off, which is the standard mode for our tests
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # remove the constraint created for this testcase
    stmt = """alter table t1alt drop constraint ne_m4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Verify that dropping an unenforced RI constraint affects similarity check for query caching."""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # prepare statement used to check for use of cached plan
    stmt = """prepare IsCachedPlanUsed from
select distinct 'Cached plan used'
from table(explain(NULL,?)) x
where plan_id
= (select distinct plan_id from table(explain(NULL,?)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # add a multi-col unenforced referential constraint
    stmt = """alter table t1alt add constraint ne_m4 foreign key(fk4a,fk4b,fk4c) references m4 not enforced;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')
    _dci.expect_complete_msg(output)
    
    # turn query cache on
    stmt = """control query default QUERY_CACHE '4096';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default QUERY_CACHE reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # prepare same query twice with different statement ids, make sure same plan used
    stmt = """prepare s  from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """prepare sx from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute isCachedPlanUsed using 'S', 'SX';"""
    output = _dci.cmdexec(stmt)
    
    # remove the RI constraint, and prepare the statement again with the sx statement id
    stmt = """alter table t1alt drop constraint ne_m4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """prepare sx from select a1alt from t1alt,m4 where fk4a=pk4a and fk4b=pk4b and fk4c=pk4c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    # this time, the cached plan should have been invalidated
    stmt = """execute isCachedPlanUsed using 'S', 'SX';"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, 'Cached plan used')
    
    # turn query caching back off, which is the standard mode for our tests
    stmt = """control query default QUERY_CACHE '0';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

