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
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)

    # testA01, testA02, testA03, testA04    
   
    stmt = """create table tbl1 (
last_name            varchar(10) default null -- Default is null.
, first_name           varchar(10)
, dept_num             numeric(4,0)
, salary               numeric(8,0)
, marital_status       varchar(1)
)
;"""
    output = _dci.cmdexec(stmt)
    
    # From testA01.
    stmt = """insert into tbl1 values
('clark', 'dinah', 9000, 37000.00, '3');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl1 values
('crinar', 'jessica', 3500, 39500.00, '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl1 values
('green', 'roger', 9000, 175500.00, '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl1 values
('howard', 'jerry', 1000, 65000.00, '1');"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # testA03, testA04
    stmt = """create table tbl2 (
last_name            varchar(10)
, first_name           varchar(10)
, dept_num             numeric(4,0)
, salary               numeric(8,0)
, marital_status       varchar(1)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tbl2 values
('zann', 'kathy', 2000, 80000.00, '1');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl2 values
('velcro', 'judy', 4000, 40000.00, '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl2 values
('jones', 'gail', 5000, 90000.00, '3');"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # In A01 this was called tbl2 -- change there!
    # testA03, testA04
    stmt = """create table tbl3 (
l_name               varchar(10)
, f_name               varchar(10)
, mar_status           varchar(1)
) ;"""
    output = _dci.cmdexec(stmt)
    
    # From testA01.
    stmt = """insert into tbl3 values ('clark', 'dinah',  '3');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl3 values ('crinar', 'jessica',  '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl3 values ('howard', 'jerry',  '1');"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    stmt = """create table tbl4 (
l_name               varchar(10)
, f_name               varchar(10)
, mar_status           varchar(1)
) ;"""
    output = _dci.cmdexec(stmt)
    
    # testA04 has instead:
    # Populating the table tbl4
    stmt = """insert into tbl4 values ('attili', 'sailaja', '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl4 values ('atluri', 'satish', '1');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl4 values ('chari', 'murli', '3');"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # In testA05 - testA03, testA08
    stmt = """create table tbl5 (
last_name            varchar(10)
, first_name           varchar(10)
, dept_num             numeric(4,0)
, salary               numeric(8,0)
, marital_status       varchar(1)
) ;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------------
    # Populating the table tbl5
    # (1998-01-03) Changes Roger Green's dept to 9000
    # so that we have a duplicate value.
    stmt = """insert into tbl5 values
('clark',  'dinah',  9000, 37000.00, '3');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl5 values
('crinar', 'jessica',8000, 39500.00, '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl5 values
('green',  'roger',  9000, 175500.00, '2');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl5 values
('howard', 'jerry',  4000, 65000.00, '1');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl5 values
('zann',   'kathy',  3000, 80000.00, '1');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tbl5 values
('velcro', 'judy',   2000, 40000.00, '3');"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------------
    # Create empty table for testA02.
    stmt = """create table tA02
(
l_name varchar(10),
f_name varchar(10)
)
;"""
    output = _dci.cmdexec(stmt)
    # ---------------------------------
    # Creating a grouped view
    
    stmt = """create view grpview
(l_name, f_name, d_num, min_sal, max_sal, avg_sal)
as (select last_name, first_name, dept_num
, min(salary), max(salary)
, cast(avg(salary) as numeric(9,2))
from tbl5
where marital_status = '1'
group by last_name, first_name, dept_num
having dept_num = 4000 or dept_num = 3000
);"""
    output = _dci.cmdexec(stmt)
    
