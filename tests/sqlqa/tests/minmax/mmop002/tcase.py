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

import data1
import data2
import data3
import data4
import data5
from ...lib import hpdci
import defs

_testmgr = None
_testlist = []
_dci = None

#  testtype functional

#  #######################################
#  ###########   Testcase A0   ###########
#  #######################################

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='min max simple query indexed column'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge
    
    #  10/30/03 EL  Changed to MX datetime data type format.
    
    stmt = """create table tab1
(
IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH not null not droppable,
Flt_1            FLOAT,
Int_1            INT,
VarCh_1          VARCHAR(5),
Yr_Dy_1          DATE,
Numer_1          NUMERIC(9, 0) SIGNED,
primary key( IntvlYr_Mn_1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table tab2
(
IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH not null not droppable,
Flt_1            FLOAT,
Int_1            INT,
VarCh_1          VARCHAR(5),
Yr_Dy_1          DATE,
Numer_1          NUMERIC(9, 0) SIGNED,
primary key(IntvlYr_Mn_1)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab3
(
IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH not null not droppable,
Flt_1            FLOAT,
Int_1            INT,
VarCh_1          VARCHAR(5),
Yr_Dy_1          DATE,
Numer_1          NUMERIC(9, 0) SIGNED,
primary key(IntvlYr_Mn_1)
);"""
    output = _dci.cmdexec(stmt)
    
    data1._init(_testmgr)
    data2._init(_testmgr)
    data3._init(_testmgr)
    data4._init(_testmgr)
    data5._init(_testmgr)
    
    stmt = """create index idx1 on tab1
( Flt_1, IntvlYr_Mn_1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idx2 on tab1
(IntvlYr_Mn_1,  Flt_1 desc);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idx3 on tab2
(IntvlYr_Mn_1,  Flt_1 desc);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idx4 on tab2
(Flt_1 desc);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idx5 on tab3
( Flt_1, IntvlYr_Mn_1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare XX from
select min(t1.IntvlYr_Mn_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select min(t1.IntvlYr_Mn_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s2b')
    
    # control query shape cut;
    stmt = """prepare XX from
select min(t1.IntvlYr_Mn_1)
from tab1 t1 left join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s4')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select min(t1.IntvlYr_Mn_1)
from tab1 t1 left join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s4b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(t1.IntvlYr_Mn_1)
from tab1 t1 right join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1 and t1.Int_1 > 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s5
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s6')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(t1.IntvlYr_Mn_1)
from tab1 t1 right join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1 and t1.Int_1 > 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s5b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s6b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(t1.IntvlYr_Mn_1)
from tab1 t1 cross join tab2 t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s7
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s8')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(t1.IntvlYr_Mn_1)
from tab1 t1 cross join tab2 t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s7b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s8b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select min(t2.IntvlYr_Mn_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s9
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s10')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select min(t2.IntvlYr_Mn_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s9b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s10b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(t2.IntvlYr_Mn_1)
from tab1 t1 left join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s11
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s12')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(t2.IntvlYr_Mn_1)
from tab1 t1 left join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan ${test_dir}/a0exp a0s11b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s12b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(t2.IntvlYr_Mn_1)
from tab1 t1 right join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1 and t2.Int_1 < 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s13
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s14')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(t2.IntvlYr_Mn_1)
from tab1 t1 right join tab2 t2
on t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1 and t2.Int_1 < 500;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s13b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s14b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(t2.IntvlYr_Mn_1)
from tab1 t1 cross join tab2 t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s15
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s16')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(t2.IntvlYr_Mn_1)
from tab1 t1 cross join tab2 t2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s15b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s16b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select min(t1.Flt_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s17
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s18')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select min(t1.Flt_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s17b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s18b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select t1.IntvlYr_Mn_1
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1
and t2.IntvlYr_Mn_1 <>
(select min(t3.IntvlYr_Mn_1) from tab1 t3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s19
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select t1.IntvlYr_Mn_1
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1
and t2.IntvlYr_Mn_1 <>
(select min(t3.IntvlYr_Mn_1) from tab1 t3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s19b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(t1.IntvlYr_Mn_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1
and t2.IntvlYr_Mn_1 <>
(select min(t3.IntvlYr_Mn_1) from tab3 t3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s21
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s22')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(t1.IntvlYr_Mn_1)
from tab1 t1, tab2 t2
where t1.IntvlYr_Mn_1 = t2.IntvlYr_Mn_1
and t2.IntvlYr_Mn_1 <>
(select min(t3.IntvlYr_Mn_1) from tab3 t3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s21b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s22b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select IntvlYr_Mn_1 + (select max(IntvlYr_Mn_1) from tab1)
from tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s23
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s24')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select IntvlYr_Mn_1 + (select max(IntvlYr_Mn_1) from tab1)
from tab1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s23b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s24b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(IntvlYr_Mn_1)
from tab1
where IntvlYr_Mn_1 < (select max(t2.IntvlYr_Mn_1) from tab1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s25
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s26')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(IntvlYr_Mn_1)
from tab1
where IntvlYr_Mn_1 < (select max(t2.IntvlYr_Mn_1) from tab1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s25b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s26b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select max(Flt_1)
from tab1
where IntvlYr_Mn_1 < (select max(t2.IntvlYr_Mn_1) from tab1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s27
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s28')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select max(Flt_1)
from tab1
where IntvlYr_Mn_1 < (select max(t2.IntvlYr_Mn_1) from tab1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s27b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s28b')
    
    # control query shape cut;
    
    _testmgr.testcase_end(desc)

def test002(desc='combation test'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table sailor
(
sid              INT UNSIGNED not null not droppable,
sname            CHAR(10),
rating           INT UNSIGNED,
age              REAL,
primary key( sid)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table boats
(
bid              INT UNSIGNED not null not droppable,
bname            CHAR(10),
color            CHAR(10),
primary key( bid)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table reserves
(
sid              INT UNSIGNED not null not droppable,
bid              INT UNSIGNED not null not droppable,
rday             DATE not null not droppable,
rname            CHAR(10),
primary key( sid, bid, rday)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into sailor
values
(22, 'dustin', 7, 45.0),
(28, 'yuppy',  9, 35.0),
(31, 'lubber', 8, 55.5),
(36, 'lubber', 6, 36.0),
(44, 'guppy',  5, 35.0),
(58, 'rusty', 10, 35.0)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into reserves
values
(28, 103, date '1996-12-04', 'guppy'),
(28, 103, date '1996-11-03', 'yuppy'),
(31, 101, date '1996-10-10', 'dustin'),
(31, 102, date '1996-10-12', 'lubber'),
(31, 101, date '1996-10-11', 'lubber'),
(58, 103, date '1996-11-12', 'dustin')
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into boats
values
(101, 'Salsa', 'Red'),
(102, 'Picante', 'Scarlet'),
(103, 'Pinto', 'Brown')
;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    
    stmt = """prepare XX from
select  S.sname
from sailor S
where S.rating = (select MAX(S2.rating) from sailor S2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan ${test_dir}/a1exp a1s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  S.sname
from sailor S
where S.rating = (select MAX(S2.rating) from sailor S2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan ${test_dir}/a1exp a1s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s2b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  S.sid, min(R.rday)
from sailor S, reserves R, boats B
where S.sid = R.sid and R.bid = B.bid and B.color = 'red' and
S.rating = (select max(S2.rating) from sailor S2)
group by S.sid
having count(*) > 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  S.sid, min(R.rday)
from sailor S, reserves R, boats B
where S.sid = R.sid and R.bid = B.bid and B.color = 'red' and
S.rating = (select max(S2.rating) from sailor S2)
group by S.sid
having count(*) > 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # control query shape cut;
    
    #                  End of test case mmop002
    
    _testmgr.testcase_end(desc)

