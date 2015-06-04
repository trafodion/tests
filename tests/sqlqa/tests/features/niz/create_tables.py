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
    
def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table niz000 
(
seqno	integer		not null	not droppable,    

smin1	smallint	signed		default null,
smin2	smallint	unsigned	default null,    

inte1	integer		signed		default null,
inte2	integer		unsigned	default null,    

lint1	largeint			default null,
lint2	largeint			default null,    

nume1	numeric(7)	unsigned	default null,
nume2	numeric(9,3)	unsigned	default null,
nume3	numeric(18)	signed		default null,
nume4	numeric(18,15)	signed		default null,    

deci1	decimal(3)	unsigned	default null,
deci2	decimal(18,0)	signed		default null,
deci3	decimal(18,9)	signed		default null,    

pict1	pic s9(18)	comp		default null,
pict2	pic sv9(2)	comp		default null,
pict3	pic s9(13)v9(5)			default null,
pict4	pic 9(3)v9(6)			default null,    

flot1	float (12)			default null,
flot2	float (52)			default null,    

real1	real				default null,
real2	real				default null,    

dblp1	double precision		default null,
dblp2	double precision		default null,    

primary key (seqno)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smin_idx on niz000(smin1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index inte_idx on niz000(inte1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index lint_idx on niz000(lint1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index nume_idx on niz000(nume1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index deci_idx on niz000(deci1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index pict_idx on niz000(pict1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index flot_idx on niz000(flot1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index real_idx on niz000(real1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index dblp_idx on niz000(dblp1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #Zeroes
    stmt = """insert into niz000 values
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #Ones
    stmt = """insert into niz000 values
(2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .1, 1, 1, 1, 1, 1, 1, 1, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #NULLs
    stmt = """insert into niz000 (seqno) values (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #Minimum Values
    stmt = """insert into niz000 values
(
4,    

-32768,
0,    

-2147483648,
1,    

-9223372036854775808,
2,    

3,
4,
-999999999999999999,
-999.999999999999999,    

5,
-999999999999999999,
-999999999.999999999,    

-999999999999999999,
-0.99,
-9999999999999.99999,
6.000001,    

7.000000000001,
-2.2250738585072014e-308,    

-1.17549435e-38,
8,    

-2.2250738585072014e-308,
9
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #Maximum Values
    stmt = """insert into niz000 values
(
5,    

32767,
0,    

2147483647,
1,    

9223372036854775807,
-2,    

3,
4,
999999999999999999,
999.999999999999999,    

5,
999999999999999999,
999999999.999999999,    

999999999999999999,
0.99,
9999999999999.99999,
6.000001,    

7.000000000001,
1.7976931348623157e+308,    

3.40282347e+38,
8,    

1.7976931348623157e+308,
9
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #First Set Of Other Values
    stmt = """insert into niz000 values
(
6,    

-459,
7892,    

-992348,
293847923,    

701291928791,
9809876586,    

5622901,
23990.78,
-129980,
-46.012979798,    

804,
-62352342342,
-8768889.1200454,    

-1283498234923749,
0.65,
-7870234.00126,
786.124598,    

11897.9998877656,
898889.00000997,    

5.89100,
555.23,    

10045.157e+8,
-6120.00945e-21
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #Second Set Of Other Values
    stmt = """insert into niz000 values
(
7,    

2834,
443,    

-90,
450,    

4545990,
11,    

102245,
77.923,
-670,
831.44553,    

21,
60778,
-486.929,    

-8798799000,
0.13,
34007.00387,
506.55209,    

-99082.007,
6712009.22,    

-3.1417,
10.39e-1,    

30887.333e+10,
-445e-25
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'nizs000')
    
    stmt = """update statistics for table niz000 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table temp_niz000 like niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into temp_niz000 
(
seqno,
smin1,
smin2,
inte1,
inte2,
lint1,
lint2,
nume1,
nume2,
nume3,
nume4,
deci1,
deci2,
deci3,
pict1,
pict2,
pict3,
pict4,
flot1,
flot2,
real1,
real2,
dblp1,
dblp2
)
(
select	seqno,
smin1,
smin2,
inte1,
inte2,
lint1,
lint2,
nume1,
nume2,
nume3,
nume4,
deci1,
deci2,
deci3,
pict1,
pict2,
pict3,
pict4,
flot1,
flot2,
real1,
real2,
dblp1,
dblp2
from niz000 
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 7)
    
    stmt = """select count(*) from temp_niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'nizs001')
    
    stmt = """create table niz001 like niz000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index smin_mc_idx on niz001(smin1, smin2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index inte_mc_idx on niz001(inte1, inte2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index lint_mc_idx on niz001(lint1, lint2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index nume_mc_idx on niz001(nume1, nume2, nume3, nume4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index deci_mc_idx on niz001(deci1, deci2, deci3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index pict_mc_idx on niz001(pict1, pict2, pict3, pict4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index flot_mc_idx on niz001(flot1, flot2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index real_mc_idx on niz001(real1, real2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index dblp_mc_idx on niz001(dblp1, dblp2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into niz001 values
(
1,    

34,
44,    

123,
789,    

99809,
99909,    

1223311,
12.333,
9899898979,
11.098080980,    

23,
123134534534,
98797.8768688,    

-4435,
-0.39,
-121213434.111,
345.8879,    

-1.2250E-28,
0.834673734574,    

9.223e18,
-1.79e-2,    

-0.00092746,
-2.225E-38
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz001 values
(
2,    

24923,
9992,    

-2147484,
9,    

847201,
5098,    

8365290,
12.333,
8998979,
444.238,    

3,
789729834,
669.02983487,    

9928,
0.96,
12345678.1234,
797.799,    

-7.9098700456e-1,
-0.7986750064688,    

0.11,
-0.7129,    

2.222197264,
4.0876e-5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz001 values
(
3,    

108,
81,    

925,
1351,    

923749823,
-615240,    

81230,
119900.22,
7019239,
308.1274,    

111,
6092340,
501293.5553,    

8394230423,
0.01,
12111.0980,
405.0001,    

0.128349234,
312.9999989e-5,    

0.0008745245,
-0.1007,    

0.309e+3,
100
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz001 values
(
4,    

25065,
10117,    

-2146436,
2149,    

924696833,
-510233,    

9669831,
119924.886,
9915917197,
763.463480980000001,    

137,
123930356708,
600760.462003670,    

8394235916,
0.58,
-108855644.88960,
158.687000,    

-6.62637770560000000E-001,
3.91287280941999936E-002,    

9.22299985216877440E+018,
-8.31499980762600960E-001,    

3.11221269804000000E+002,
1.00000040876000000E+002
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz001 values
(
5,    

12532,
5058,    

-1073218,
1074,    

462348416,
-255116,    

4834915,
59962.443,
4957958598,
381.731740490000250,    

68,
61965178354,
300380.231001835,    

4197117958,
0.29,
-54427822.44480,
426.843503,    

-3.31318885280000000E-001,
1.95643640470999968E-002,    

4.61149992608438720E+018,
-4.15749993640929472E-001,    

1.55610634902000000E+002,
5.00000204380000128E+001
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from niz001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/nexp000""", 'nizs002')
    
    stmt = """update statistics for table niz001 on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view niz_vw_000 as
select
n0.seqno,    

n0.smin1,
n1.smin2,    

n0.inte1,
n1.inte2,    

n0.lint1,
n1.lint2,    

n0.nume1,
n1.nume2,
n0.nume3,
n1.nume4,    

n0.deci1,
n1.deci2,
n0.deci3,    

n0.pict1,
n1.pict2,
n0.pict3,
n1.pict4,    

n0.flot1,
n1.flot2,    

n0.real1,
n1.real2,    

n0.dblp1,
n1.dblp2    

from  niz000 n0 inner join niz001 n1
on n0.seqno = n1.seqno;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view niz_vw_001 as
select
count(*) as cnt,
NULLIFZERO (avg (niz000.inte1 + niz001.inte2)) as niz_avg    

from niz000, niz001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view niz_vw_002 as
select	n0.seqno,    

n0.smin1,
n1.smin2,    

n0.inte1,
n1.inte2,    

n0.lint1,
n1.lint2,    

n0.nume1,
n1.nume2,
n0.nume3,
n1.nume4,    

n0.deci1,
n1.deci2,
n0.deci3,    

n0.pict1,
n1.pict2,
n0.pict3,
n1.pict4,    

n0.flot1,
n1.flot2,    

n0.real1,
n1.real2,    

n0.dblp1,
n1.dblp2    

from niz000 n0, niz001 n1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view niz_vw_003 as
select	n0.seqno as n0sq,    

NULLIFZERO (n0.smin1) as n0s1,
NULLIFZERO (n1.smin2) as n1s2,    

NULLIFZERO (n0.inte1) as n0i1,
NULLIFZERO (n1.inte2) as n1i2,    

NULLIFZERO (n0.lint1) as n0l1,
NULLIFZERO (n1.lint2) as n1l2,    

NULLIFZERO (n0.nume1) as n0n1,
NULLIFZERO (n1.nume2) as n1n2,
NULLIFZERO (n0.nume3) as n0n3,
NULLIFZERO (n1.nume4) as n1n4,    

NULLIFZERO (n0.deci1) as n0d1,
NULLIFZERO (n1.deci2) as n1d2,
NULLIFZERO (n0.deci3) as n0d3,    

NULLIFZERO (n0.pict1) as n0p1,
NULLIFZERO (n1.pict2) as n1p2,
NULLIFZERO (n0.pict3) as n0p3,
NULLIFZERO (n1.pict4) as n1p4,    

NULLIFZERO (n0.flot1) as n0f1,
NULLIFZERO (n1.flot2) as n1f2,    

NULLIFZERO (n0.real1) as n0r1,
NULLIFZERO (n1.real2) as n1r2,    

NULLIFZERO (n0.dblp1) as n0dp1,
NULLIFZERO (n1.dblp2) as n0dp2    

from niz000 n0, niz001 n1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table niz002 
(
seqno	integer		not null
not droppable,    

char1	char (25)	default null,
char2	varchar (25)	character set ucs2
default null,    

date1	date		default null,
tims1	timestamp	default null,    

primary key (seqno)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into niz002 values
(
1,    

'HP',
_ucs2'Cupertino',    

date '07/24/2001',
timestamp '2001-03-01 11:56:43.300000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz002 values
(
2,    

'Tandem',
_ucs2'Austin',    

date '03/12/2002',
timestamp '2002-12-05 03:33:51.300000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz002 values
(
3,    

'Compaq',
_ucs2'Bay Area',    

date '04/12/2003',
timestamp '2003-09-03 00:00:34.000000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz002 values
(
4,    

'HP-IT',
_ucs2'San Jose',    

date '12/24/2004',
timestamp '2004-07-05 23:59:59.100000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz002 values
(
5,    

'RTSD',
_ucs2'CAC',    

date '05/07/2005',
timestamp '2005-01-07 09:46:29.300000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into niz002 values
(
6,    

NULL,
_ucs2'',    

date '05/07/2006',
timestamp '2006-05-06 16:40:00.000000'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    _testmgr.testcase_end(desc)

