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

#this cqd should be gone for new version of foj
#control query default comp_bool_199 'on';
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """control query default COMP_FLOAT_8 '5';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default COMP_FLOAT_9 '5';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default EXE_DIAGNOSTIC_EVENTS 'ON';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE CASH01A
(
ITEM_NBR                         INT NOT NULL
, STORE_NBR                        DECIMAL(9, 5) NOT NULL
, WHSE_NBR                         SMALLINT
, ON_HAND_QTY                      INT NOT NULL
, PRIMARY KEY (ITEM_NBR, STORE_NBR) NOT DROPPABLE
)
HASH2 PARTITION
STORE BY (ITEM_NBR ASC, STORE_NBR ASC)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """control query default GROUP_BY_USING_ORDINAL 'all';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table wm000
(
seqno	integer		not null	not droppable,    

smin1	smallint		default null,    

inte1	integer			default null,    

lint1	largeint		default null,    

nume1	numeric(9,3)		default null,    

deci1	decimal(18,9)		default null,    

pict1	pic s9(13)v9(5)		default null,    

flot1	float (52)		default null,    

real1	real			default null,    

dblp1	double precision	default null,    

char1	char (12)		default null,    

vchr1	varchar (12)		default null,    

primary key (seqno)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index smin_idx on wm000(smin1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index inte_idx on wm000(inte1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index lint_idx on wm000(lint1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index nume_idx on wm000(nume1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index deci_idx on wm000(deci1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index pict_idx on wm000(pict1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index flot_idx on wm000(flot1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index real_idx on wm000(real1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index dblp_idx on wm000(dblp1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index char_idx on wm000(char1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index vchr_idx on wm000(vchr1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table wm001 like wm000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view wm_vw_000 as
select
n0.seqno as n0sq,    

n0.smin1 as n0s1,    

n0.inte1 as n0i1,    

n0.lint1 as n0l1,    

n0.nume1 as n0n1,    

n0.deci1 as n0d1,    

n0.pict1 as n0p1,    

n0.flot1 as n0f1,    

n0.real1 as n0r1,    

n0.dblp1 as n0dp1,    

n0.char1 as n0c1,    

n0.vchr1 as n0v1    

from 	wm000 n0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view wm_vw_001 as
select
n1.seqno as n1sq,    

n1.smin1 as n1s1,    

n1.inte1 as n1i1,    

n1.lint1 as n1l1,    

n1.nume1 as n1n1,    

n1.deci1 as n1d1,    

n1.pict1 as n1p1,    

n1.flot1 as n1f1,    

n1.real1 as n1r1,    

n1.dblp1 as n1dp1,    

n1.char1 as n1c1,    

n1.vchr1 as n1v1    

from 	wm001 n1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into CASH01A
select C1*10+C2, C2, 3, 4 from (values(1)) as x
transpose 0,1,2,3,4,5,6,7,8 as C1
transpose 0,1,2,3,4,5,6,7,8 as C2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000 values
(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '0', '0');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000 values
(2, 1, 1, 1, 1, 1, 1, 1, 1, 1, '1', '1');"""
    output = _dci.cmdexec(stmt)
   
    # can't use upsert if you are not inserting all columns 
    stmt = """insert into WM000 (seqno) values (3);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000
values
(
4,    

-32768,    

-2147483648,    

-923720368547588,    

-99999.999,    

-999999.99999999,    

-9999999.99999,    

7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

'1',    

'11'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000 values
(
5,    

32767,    

2147483647,    

923720368547587,    

999999.999,    

9999999.999999999,    

99999999.99999,    

6.000001,    

4509.000000001,    

3.40282347e+38,    

'12',    

'112'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000 values
(
6,    

7892,    

293847923,    

9809876586,    

23990.78,    

8769.1200454,    

786.12598,    

11897.9998877656,    

898889.00000997,    

555.23,    

'123',    

'1123'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000 values
(
7,    

2834,    

450,    

4545990,    

831.44553,    

486.929,    

506.55209,    

99.082007,    

10.39e-1,    

308.87333e+2,    

'1234',    

'11234'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM000 values
(
8,    

123,    

789,    

99809,    

12.333,    

9897.8768688,    

12434.111,    

345.8879,    

-1.2250E-2,    

0.834673734574,    

'12345',    

'112345'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(1, 1, 2, 2, 2, 2, 2, 2, 2, 2, '2', '2');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(2, 1, 3, 3, 3, 3, 3, 3, 3, 3, '3', '3');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(
3,    

24923,    

9,    

847201,    

444.238,    

669.02983487,    

797.799,    

-7.9098700456e-1,    

0.11,    

2.222197264,    

'54321',    

'554321'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(
4,    

-32768,    

-2147483648,    

-923720368547588,    

-99999.999,    

-999999.99999999,    

-9999999.99999,    

7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

'1',    

'11'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(
5,    

25065,    

2149,    

510233,    

763.463,    

137,    

158.687000,    

3.91287280941999936E-002,    

8.31499980762600960E-001,    

3.11221269804000000E+002,    

'321',    

'3321'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(
6,    

7892,    

293847923,    

9809876586,    

23990.78,    

8769.1200454,    

786.12598,    

11897.9998877656,    

898889.00000997,    

555.23,    

'123',    

'1123'
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM001 values
(
12,    

9374,    

3298,    

8928,    

88790.78,    

9769.1254,    

876.12598,    

1897.8766,    

988898.09097,    

955.23,    

'523',    

'9123'
);"""
    output = _dci.cmdexec(stmt)
    # extra tables set up
    
    stmt = """create table wm003 like wm000; -- one value"""
    output = _dci.cmdexec(stmt)
    stmt = """create table wm004 like wm001; -- nullvalue"""
    output = _dci.cmdexec(stmt)
    stmt = """create table emp00 like wm004; -- empty"""
    output = _dci.cmdexec(stmt)
    stmt = """create table emp01 like wm004; -- empty"""
    output = _dci.cmdexec(stmt)
    stmt = """create table wm005 like wm000; -- one value"""
    output = _dci.cmdexec(stmt)
    stmt = """create table tab006 ( a int not null primary key);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into WM003 values
(1, 1, 0, 0, 0, 0, 0, 0, 0, 0, '0', '0');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into WM005 values
(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '0', '0');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab006 values
(0);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view wm_vw_003 as
select
n0.seqno as n0sq,    

n0.smin1 as n0s1,    

n0.inte1 as n0i1,    

n0.lint1 as n0l1,    

n0.nume1 as n0n1,    

n0.deci1 as n0d1,    

n0.pict1 as n0p1,    

n0.flot1 as n0f1,    

n0.real1 as n0r1,    

n0.dblp1 as n0dp1,    

n0.char1 as n0c1,    

n0.vchr1 as n0v1    

from 	wm003 n0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view wm_vw_004 as
select
n1.seqno as n1sq,    

n1.smin1 as n1s1,    

n1.inte1 as n1i1,    

n1.lint1 as n1l1,    

n1.nume1 as n1n1,    

n1.deci1 as n1d1,    

n1.pict1 as n1p1,    

n1.flot1 as n1f1,    

n1.real1 as n1r1,    

n1.dblp1 as n1dp1,    

n1.char1 as n1c1,    

n1.vchr1 as n1v1    

from 	wm004 n1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view wm_vw_005 as
select
n0.seqno as n0sq,    

n0.smin1 as n0s1,    

n0.inte1 as n0i1,    

n0.lint1 as n0l1,    

n0.nume1 as n0n1,    

n0.deci1 as n0d1,    

n0.pict1 as n0p1,    

n0.flot1 as n0f1,    

n0.real1 as n0r1,    

n0.dblp1 as n0dp1,    

n0.char1 as n0c1,    

n0.vchr1 as n0v1    

from 	wm005 n0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view wm_vw_tab006 as
select
a as a
from 	tab006 n0;"""
    output = _dci.cmdexec(stmt)
    
    # NULL and EMPTY tables
    
    stmt = """create table tbl_null_000
(
seqno	integer		not null	,    

smin1	smallint		default null,    

inte1	integer			default null,    

lint1	bigint		default null,    

nume1	numeric(9,3)		default null,    

deci1	decimal(18,9)		default null,    

pict1	float	default null,    

flot1	float (52)		default null,    

real1	real			default null,    

dblp1	double precision	default null,    

char1	char (12)		default null,    

vchr1	varchar (12)		default null,    

primary key (seqno)
) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tbl_null_001 like tbl_null_000;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tbl_null_000 values
(1, null, null, null, null, null, null, null, null, null, null, null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tbl_null_001 values
(1, null, null, null, null, null, null, null, null, null, null, null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tbl_null_001 values
(2, null, null, null, null, null, null, null, null, null, null, null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vw_null_000 as
select
n0.seqno as n0sq,    

n0.smin1 as n0s1,    

n0.inte1 as n0i1,    

n0.lint1 as n0l1,    

n0.nume1 as n0n1,    

n0.deci1 as n0d1,    

n0.pict1 as n0p1,    

n0.flot1 as n0f1,    

n0.real1 as n0r1,    

n0.dblp1 as n0dp1,    

n0.char1 as n0c1,    

n0.vchr1 as n0v1    

from 	tbl_null_000 n0;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create view vw_null_001 as
select
n1.seqno as n1sq,    

n1.smin1 as n1s1,    

n1.inte1 as n1i1,    

n1.lint1 as n1l1,    

n1.nume1 as n1n1,    

n1.deci1 as n1d1,    

n1.pict1 as n1p1,    

n1.flot1 as n1f1,    

n1.real1 as n1r1,    

n1.dblp1 as n1dp1,    

n1.char1 as n1c1,    

n1.vchr1 as n1v1    

from 	tbl_null_001  n1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table CASH01A on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table wm000 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table wm001 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table wm003 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table wm004 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table wm005 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table tab006 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table tbl_null_000 on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table tbl_null_001 on every column sample;"""
    output = _dci.cmdexec(stmt)
    
