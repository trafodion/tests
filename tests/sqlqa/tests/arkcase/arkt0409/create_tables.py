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
    
    stmt = """drop view v1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view v2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view v3;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table tab1;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table tab1 
(tab1_pk integer not null,
tab1_nn integer not null,
tab1_na integer,
primary key (tab1_pk));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table tab2;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table tab2 
(tab2_pk integer not null,
tab2_nn integer not null,
tab2_na integer,
primary key (tab2_pk));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table tab3;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table tab3 
(tab3_pk integer not null,
tab3_nn integer not null,
tab3_na integer,
primary key (tab3_pk));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table oj1;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table oj1 (a integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table oj2;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table oj2 (b integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view v1 (a, b) as
select tab2_pk, tab3_pk
from tab2, tab3 
where tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view v2 (a, b) as
select tab2_pk, tab3_pk
from tab2 inner join
 tab3 
on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view v3 (a, b) as
select tab2_pk, tab3_pk
from tab2 left join
 tab3 
on tab2_pk = tab3_pk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table zztemp;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table zztemp 
(zzc1 integer not null, zzc2 integer not null) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table zztemp2;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table zztemp2 
(zzc1 integer, zzc2 integer) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
