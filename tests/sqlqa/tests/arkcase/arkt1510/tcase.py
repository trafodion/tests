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
    
def test001(desc="""a00"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA00
    #  Description:        Create the table for the use in the test
    #			cases.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    
    # Create LOG file
    
    stmt = """drop table OPTABLE;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table OPTABLE 
(  p1  largeint 		not null
, u1  smallint 		unsigned
, zi1 smallint 		not null
, f1  double precision
, n1  numeric (4,2)    unsigned no default not null
, d1  decimal (4,2)    unsigned no default not null
, t1  date	       not null
, c1  char
, p2  integer 		not null
, u2  integer 		unsigned
, zi2 integer 		signed no default not null
, f2  real	        not null
, n2  numeric (6,3) 	unsigned
, d2  decimal (6,3)	signed no default not null
, t2  time
, c2  char(2)
, p3  smallint 		signed no default not null
, u3  largeint
, zi3 largeint 		signed no default not null
, f3  float		no default not null
, n3  numeric (12,4) 	signed no default not null
, d3  decimal (12,4)
, t3  interval hour to second
, c3  char(3)
, z   char (8)
, psv pic s9v9(3) 	no default not null
, p9c pic 9v9(2) comp
, ps9 pic s9(5) 	no default not null
, psc pic s9(1) comp
, f4  float
, f5  real 		no default not null
, b1  double precision	no default not null
, b2  double precision
, primary key (t1) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idxp1 on OPTABLE (b1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # Commented out until DDL supported  location $data1;
    
    stmt = """create unique index unidx on OPTABLE (p1, p2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values (
0, 0,  -32768,  -.7394723453, 10.79,  10, date '1959-12-31',  'a' ,
-2147484,   9,   9,   0.9,   9,   9, time '23:59:59', 'aa',
9, 200,  -1, 0.10120, 11.9,  null, null, null, null,
-0.1123, 0.99, -99999, -9, .314159260, -1.175E-18,
-1.2250E-28, 0.05
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
9.223e18,  10,  32767,  0.00971, 10,  10, date '1960-11-01', 'a'  ,
10, 10, 214748366, -1.17e-18, 10, 10, time '00:00:00', 'aa', -2418,
5678236,  -4928761,  -0.10859,  10,  -2.222197264,
interval '00:00:00' hour to second, 'aaa', 'Row01',
0.356, 1.99, 99999, 9, -2.225E-8, 3.402E-8,
1.7976E-3, -0.05
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10, 32766, -32766, -1.79e-2, 1.01, 2.99, date '1974-05-24', 'a',
-3829135, 847201, 23.0008347231, -.123009, 10, 10, time '00:00:15',
'aa', 0, 20, 0, -.00092746, 36.02, 20,
interval '00:00:15' hour to second, 'aab', 'Row02',
0.997, 0.11, 12345, 8, -.3876, -3.402E-3,
-1.7976E-3, -2.225E-38
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
193, 24923, 9992, -0.9999999, 1.1, 22.03, date '1900-12-01', 'a'  ,
-2.14588, 78246, 8, 0.82304903,  3.33,  10, time '00:00:30', 'aa' ,
30, 18234, 3, -0.333330, -0.000392, 12353298.1999,
interval '00:00:30' hour to second, 'aac', 'Row03',
-.019, 0.58, 4598, 7, .9789, -0.58793,
0.045, -0.045
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
9999, 33392, -19234, -0.0003726, 2.1, 1.9, date '1981-08-21', 'a',
2083292, 83652920, -19283745, 0.983720007, 208.3, 2,
time '00:00:45', 'ab' ,
1, 182734, 42, 0.948, 3, 87, interval '00:00:45' hour to second,
'aba', 'Row04', 0.866, .50, 75849, 6, .8345, -.9999999,
-0.71414, -.60
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
10328, 75, 78, 0.8700123, 3.0, 34.29, date '2960-03-22',  'a'  ,
-58339, 38412, -38413, 0.2000974, 444.238, 2.0, time '00:01:00',
'ab', -12390, -9335202, -109, -.853, 12345678.1234, 0,
interval '00:01:00' hour to second, 'abb', 'Row05',
0.037, 1.06, 83936, 5, -.7129, 0.834673734574,
7.9098700456e-23, -7.9098700456e-1
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
3, 201, 1, -1,  10, 25.73, date '1925-09-12',  'a'  ,
836, 2, -2, -.5,  1.3,  20, time '00:01:15', 'ab' ,
11, 28, 322, .111003, -12345678.1234, -1.3,
interval '00:01:15' hour to second, 'abc', 'Row06',
0.298, 1.17, 76546, 4, -0.6958, -0.7986750064688,
-.0976952543975, 0.0976952543975
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
1, 2,  3, -0.1, 0.27, 8.2, date '1963-03-01',  'a'  ,
82, 0, 0, -.10834562, 6.003, 60.006, time '00:01:30', 'ac' ,
0, 1, 1, -1.0, 333.02, 666.09, interval '00:01:30' hour to second,
'aca', 'Row07',
0.309, 0.01, 52076, 3, 0.57308, -0.98633667800,
-0.008754335, 0.008754335
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into OPTABLE values (
25, 83, 19, 0.2787124838, 8.000, 7.23, date '1926-02-17', 'a'  ,
16, 30, 3088, -.300072823,  9.003, 3, time '00:01:45', 'ac' ,
20, 0, 20, -.20008436, 20, 20, interval '00:01:45' hour to second,
'acb', 'Row08', -0.1007, .05, 42770, 2, 4.0876e-5, -1,
0.0008745245, -0.0008745245
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update statistics for table OPTABLE on every column;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA01
    #  Description:        Tests for SQL, use of ACOS function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ACOS function syntax:
    # ACOS{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 0.344;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, f1, AcOs(f1), f3, acOs(aCoS(f3) / 199), SQRT(Acos(?p)),
CEILING(ACOS(0)), ACOS(ASIN(f2) / 3), ACOS(TANH(f4))
from OPTABLE 
where ACOS(f3 / 9999999) < PI() and
SIGN(ACOS(f3)) between 0 and 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    stmt = """select z, f4, f5, psv, FLOOR(POWER(ACOS(psv), 2)),
FLOOR(EXP(ACOS(psv))),
ACOS(ABS(f4)), RADIANS(ACOS(f5)),
ACOS(b1), ACOS(SIN(b2)), ACOS(.5 * 2 / 10),
ACOS(8.1 / 99.37 * 100000 / 80000)
from OPTABLE 
where t3, c2 is not null
group by z, f5, f4, psv, b1, b2
having ACOS(f4) < 1
order by f5, f4, psv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    stmt = """select z, ACOS(LOG(?p) + 1) - SIN(37 * PI() /180),
ACOS(COS(f2)), ACOS(COSH(f3) / 10),
ACOS(TAN(?p)), ACOS(CAST('.14' as float)),
CASE ACOS(0.5)
when 30 then acos(30 * PI() / 180)
when 45 then asin(45 * PI() / 180)
when 90 then atan(90 * PI() / 180)
else ACOS(LOG10(.5))
END,
ACOS(f3 / 100) * COSH(0.6668 * 2) / 2,
4 - ACOS(b1) * TAN(TANH(u3)),
ACOS(b2 / 10) / ASIN(b2 / 2e1)
from OPTABLE 
where ACOS(DEGREES(f3) / 100) =
(select ACOS(DEGREES(f3) / 100)
from OPTABLE 
where acos(degrees(f3) / 100) < 1 and
ACOS(b2 / 10) not IN (30, 40, 60, 90));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    stmt = """alter table OPTABLE 
add check (acos(f1) < 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into OPTABLE values(
1,  0,  100,  acos(-.5),  10,  10, date '1960-01-01',  'a'  ,
.566,  0.14147,  -.1,  -1,  0,  0, time '00:02:00', 'au' ,
0,  -.335,  .66688,  .7668,  .419,  0.554, null, 'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, -1, ACOS(.05), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = ACOS(.05)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, p9c, ACOS(AVG(p9c) / 2), ACOS(SUM(psc) / 180), psc,
acos(0.9999), acos(-0.99999), acos(1), acos(-1)
from OPTABLE 
where TRIM(z) >= 'Row07'
group by z, p9c, psc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """delete from OPTABLE 
where LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1
on ACOS(vv.f4 * 0.1) = ACOS(t1.f4 / 10)
and ACOS(COS(vv.f5)) = ACOS(COS(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    stmt = """select c3, ACOS(TANH(b1)), SQRT(ACOS(b2))
from OPTABLE 
union
select trim(t1.z), t1.b2, ACOS(t1.b2 / 100)
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
ACOS(asin(t1.b2 * .008)) = ACOS(asin(vv.b2 * .008))
left join voptbl v on
ACOS(vv.psv) = ACOS(v.psv);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA02
    #  Description:        Tests for SQL, use of ASIN function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ASIN function syntax:
    # ASIN{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 0.134;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, f1, Asin(f1), f3, AsiN(AsIn(f3 /100) / 2),
SQRT(aSIN(?p)),
CEILING(ASIN(0)), f1, asIN(ACOS(f1) / 10),
f4, f5, psv, FLOOR(POWER(ASIN(psv), 2)),
FLOOR(EXP(ASIN(psv))),
ASIN(ABS(f4)), RADIANS(ASIN(f5))
from OPTABLE 
where ASIN(f3 / 100) < PI() and
SIGN(ASIN(f3 / 100)) between 0 and 8 and
psv > -9.9
group by z, f1, f3, f5, f4, psv, zi1, u1, u3
having ASIN(f4) > 0
order by f5, f4, psv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    
    stmt = """select z, ASIN(b2 / 60),
ASIN(ACOS(zi1 * (-.00102e-2)) / 2),
ASIN(1 - 0.3332), ASIN(-1.873E-4 * 2.485E3)
from OPTABLE 
where t3 is not null and
c2 is not null and
ASIN(DEGREeS(f3) * 10e-3) =
(select ASIN(DEGREeS(f3) * 10e-3)
from OPTABLE 
where asin(f4) < -0.77);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    
    stmt = """select z, ASIN(LOG10(?p)) / SIN(145 * PI() / 180),
ASIN(COS(f5)), ASIN(SIN(f5)), ASIN(COSH(f4) * 0.01), f5, f4,
CASE
when asin(f5) > 0 then sin(0.14147)
when asin(f5) < 0 then cos(-0.14147)
when asin(f5) = 0 then asin(0.14147)
else ASIN(LOG10(.5))
END,
n3, ASIN(n3 * 50e-10) * COSH(0.6668) / 2
from OPTABLE 
where ASIN(TAN(b2) / 100) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    
    stmt = """select z, ASIN(TAN(?p)), ASIN(ATAN(CAST('0.314' as float))),
f2, ACOS(f2 / 100) / ASIN(f2 * (-0.001)),
asin(TAN(n1) / 15),
-3.1 / ASIN(TAN(b2) / 555) * ASIN(TAN(u3 * .00001) / 10)
from OPTABLE 
where ASIN(b2 * pi() / 180) not IN (30, 40, 60, 90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    
    stmt = """alter table OPTABLE 
add check (asin(f1) < 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into OPTABLE values(
1,  0,  100,  Asin(-.5),  10,  10, date '1960-12-01',  'a'  ,
3,  3,  3,  3,  3,  3, time '00:02:00', 'ac' ,
3,  3,  3,  3,  3,  3, interval '00:10:30' hour to second,
'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, -.09, ACOS(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = ASIN(.05)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # AR Added order by
    stmt = """select z, zi2 * 11e-10, ASIN(AVG(zi2 * 11e-10)),
ASIN(SUM(psc) / 180), asin(1), asin(-1)
from OPTABLE 
where TRIM(z) > 'Row07' and
ASIN(f4) < 180
group by z, zi2, psc order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    
    stmt = """delete from OPTABLE 
where f4 = ASIN(.05) and
LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1
on ASIN(vv.f4) = ASIN(t1.f4)
and ASIN(SIN(vv.f5)) = ASIN(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """select c3, ASIN(TANH(b1)), SQRT(abs(SIN(b2)))
from OPTABLE 
union all
select trim(vv.z), vv.b2, ASIN(vv.b2)
from voptbl vv
left join voptbl1 v1 on
v1.z = vv.z and
ASIN(v1.b2 * 0.0005225) = ASIN(vv.b2 * 0.0005225)
right join voptbl v  on
v.z >= v1.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """select c3, ASIN(TANH(b1)), SQRT(abs(ASIN(b2 / 100)))
from OPTABLE 
union
select t1.c2, t1.b2, ASIN(t1.b2)
from OPTABLE t1
inner join voptbl1 on
t1.z = voptbl1.z and
ASIN(t1.b2) = ASIN(voptbl1.b2)
left join voptbl on
ASIN(voptbl1.psv) = ASIN(voptbl.psv)
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA03
    #  Description:        Tests for SQL, use of ATAN function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ATAN function syntax:
    # ATAN{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 0.9887;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, p2, aTAN(p2), Atan(ATAN(psv)), SQRT(ATAN(?p)),
CEILING(ATAN(0)), ATAN(ACOS(f2)), atAn(TANH(f4)),
ATAN(0.00478 * 72300 / -0.038)
from OPTABLE 
where ataN(f3) < PI() and
SIGN(ATAN(f3)) between -1 and 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    
    stmt = """select z, f4, f5, psv, FLOOR(POWER(ATAN(psv), 2)),
FLOOR(power(ATAN(psv), 2)),
ATAN(ABS(f4)), RADIANS(ATAN(f5))
from OPTABLE 
where t3 is not null and
c2 is not null
group by z, f5, f4, psv
having ATAN(f4) > 0
order by 1 asc, 2 desc, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    
    stmt = """select z, ATAN(LOG10(?p)) + PI()  / SIN(145 * PI() / 180),
f5, ATAN(COS(f5)), ATAN(SIN(f5)),
ATAN(CAST(pi() as double precision)),
CASE
when atan(f5) > 0 then atan(99999.1239999)
when atan(f5) < 0 then tan(90 * PI() / 180)
else ATAN(LOG10(.5))
END,
n3, ATAN(n3 - 1) * COSH(0.6668) / 2,
9.27 - ATAN(TANH(d2)) * ATAN(TAN(p3 / 100))
from OPTABLE 
where ATAN(DEGREeS(f3)) =
(select ATAN(DEGREeS(f3))
from OPTABLE 
where RADIANS(f5) > 1.4e-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    
    stmt = """insert into OPTABLE values(
1,  0,  100,  atan(-.5),  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, null, ACOS(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select p9c, b2, c3, f4 from OPTABLE order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    
    stmt = """update OPTABLE set f4 = ATAN(.05)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select p9c, b2, c3, f4
from OPTABLE 
where TRIM(z) > 'Row07' and
ATAN(f4) < 180
group by c3, p9c, b2, f4
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    
    stmt = """delete from OPTABLE 
where LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select p9c, b2, c3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where	trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    
    stmt = """create view voptbl1 as
select t1.z, t1.b2, vv.psv
from voptbl vv left join OPTABLE t1
on ATAN(vv.f4) = ATAN(t1.f4)
and ATAN(SIN(vv.f5)) = ATAN(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    
    stmt = """select rtrim(ltrim(v.c2)), v.b2, ATAN(v.b2)
from voptbl v
left join voptbl1 vv on
v.z = vv.z and
ATAN(v.b2) = ATAN(vv.b2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    
    stmt = """select z, ATAN(TANH(b1)), SQRT(abs(ATAN(b2)))
from OPTABLE 
union all
select rtrim(ltrim(v.c2)), v.b2, ATAN(v.b2)
from voptbl v
left join voptbl1 vv on
v.z = vv.z and
ATAN(v.b2) = ATAN(vv.b2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    
    stmt = """select z, c3, ATAN(TANH(b1)), SQRT(abs(ATAN(b2)))
from OPTABLE 
union
select t1.z, t1.c2, t1.b2, ASIN(t1.b2)
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
ATAN(t1.b2 + 9.999999) = ATAN(vv.b2 + 9.999999)
left join voptbl v on
ATAN(v.psv) = ATAN(vv.psv)
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    
    stmt = """select v.z, atan(v.b2)
from voptbl v
left join voptbl1 vv on
v.z = vv.z and
atan(v.b2) = atan(vv.b2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA04
    #  Description:        Tests for SQL, use of COS function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # COS function syntax:
    # COS{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p -1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, d1, Cos(d1), psc, CoS(cOS(psc)), SQRT(COS(?p)),
CEILING(COS(sinh(0))), COS(ACOS(f2)), p2, COS(TANH(p2))
from OPTABLE 
where COS(f2) < PI() and
SIGN(COS(f3)) = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    
    stmt = """select z, f4, f5, psv, FLOOR(POWER(COS(psv), 2)),
EXP(COS(psv)),
COS(ABS(f4)), RADIANS(COS(f5)),
COS(45 * 3.1415926 / 180), COS(SIN(45 * PI() / 180)),
b1, b2, COS(b1 + 256 - b2 / 100)
from OPTABLE 
where t3 is null and
c2 is not null
group by z, f4, f5, psv, b1, b2
having COS(f4) > 0
order by f4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    
    stmt = """select z, COS(sin(TAN(?p))), cosh(cos(CAST('.14' as float))),
COS(LOG10(abs(f1)) + PI() / SIN(145 * PI() / 180)),
CASE COS(0.5)
when 30 then 30 * PI() / 180
when 45 then 45 * PI() / 180
when 90 then 90 * PI() / 180
else COS(LOG10(.5))
END,
COS(COS(0.2 + 0.6 - 0.3)) + .002 * 10,
1.12 - COS(ACOS(d2 / 100 * 11e-2)) * TAN(ASIN(psv))
from OPTABLE 
where Cos(f3) =
(select COS(f3)
from OPTABLE 
where RADIANS(f5) > 1.1e-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    
    stmt = """prepare p from
insert into OPTABLE values(
1,  0,  100,  cos(-.5),  10,  10, date '1960-09-01',  'a'  ,
3,  3,  3,  3,  3,  3, time '00:02:00', 'ac' ,
3,  3,  3,  3,  3,  3, interval '00:10:30' hour to second,
'acc', 'Row09',
-9.9, COS(0.022E-3), -5342, 4, -.09, ACOS(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = COS(.5)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, c1, f1, psc, COS(f1 + ASIN(SUM(psc) / 180)),
cos(262), cos(261), cos(-262), cos(-261)
from OPTABLE 
where TRIM(z) > 'Row07' and
COS(f4) < 180
group by z, c1, f1, psc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    
    stmt = """delete from OPTABLE 
where f4 = COS(.5) and
LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c2, c3 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    
    stmt = """create view voptbl1 as
select vv.z, vv.c1, vv.b2
from voptbl vv left join OPTABLE t1 on
COS(vv.f4) = COS(t1.f4) and
COS(SIN(vv.f5)) = COS(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """select z, COS(TANH(b1)), SQRT(abs(COS(b2)))
from OPTABLE 
union all
select v.z, v.b2, COS(v.b2)
from voptbl v
left join voptbl1 vv on
v.z = vv.z and
COS(v.b2 * 10e-5) = SIN(vv.b2 * 10e-5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    stmt = """select z, ASIN(TANH(b1)), SQRT(abs(ASIN(b2 * -1.1e-2)))
from OPTABLE 
union
select t1.z, t1.b2, COS(COsh(t1.b2 / 3 * 7))
from OPTABLE t1
inner join voptbl1 on
t1.z = voptbl1.z and
COS(SIN(t1.b2)) = COS(SIN(voptbl1.b2))
left join voptbl on
COS(voptbl.b2) = COS(voptbl1.b2)
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    
    stmt = """drop table d1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """CREATE TABLE d1 (i1 INT UNSIGNED
, i2 INT UNSIGNED
, i3 INT UNSIGNED
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT INTO d1 VALUES (  11 ,  21 ,  61);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO d1 VALUES (  31 ,  41 ,  51);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT INTO d1 VALUES (  51 ,  61 ,   1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SELECT i2 FROM d1 
WHERE i2 in ( VALUES( cos(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT i2 FROM d1 
WHERE i2 in ( VALUES( cos(1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """SELECT i2 FROM d1 
WHERE i2 in ( VALUES( sin(cos(1)+2)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA05
    #  Description:        Tests for SQL, use of COSH function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # COSH function syntax:
    # COSH{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, f2, COSH(f2), COSH(COSH(p9c)), SQRT(COSH(?p)),
CEILING(COSH(0)), COSH(ACOS(f2)), COSH(TANH(f4)),
COSH(ABS(f4)), RADIANS(COSH(f5))
from OPTABLE 
where COSH(f3) < PI() and
SIGN(COSH(f3)) = 1
group by z, u2, p9c, f2, f4, f5
having COSH(f4) > 0
order by f2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    stmt = """select z, COSH(45 * 3.1415926 / 180), COSH(SINH(45 * PI() / 180)),
b1, b2, COSH(b1 - b2 / 100),
psv, FLOOR(POWER(COSH(psv), 2)),
FLOOR(EXP(COSH(psv)))
from OPTABLE 
where t3 is null and
c2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    
    stmt = """select z, Cosh(LOG10(?p) + PI()),
COSH(COS(f5)), COSH(SIN(f5)), COS(COSH(f4)),
COSH(TAN(?p)),
CASE
when cosh(f1) = 0 then 0
when cosh(f1) < 0 then -1
when cosh(f1) > 1 then 1111111111
else COSH(LOG10(10))
END,
COSH(SIN(0.2 + 0.6 - 0.3)) - TANH(COSH(0.6666666666)),
4 - COSH(SINH(f3)) * TAN(f3)
from OPTABLE 
where COSH(DEGREeS(f3)) =
(select coSh(DEGREeS(f3))
from OPTABLE 
where SINH(f3) < -.99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    
    stmt = """alter table OPTABLE 
add constraint c1 check (cosh(f1) < 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values(
1,  0,  100,  cosH(-.5),  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, null, ACOS(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select z, f4, c1, COSH(f1)
from OPTABLE 
where TRIM(z) > 'Row07' and
(COSH(f4) is null or
COSH(f4) is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    
    stmt = """update OPTABLE set f4 = COSH(.5)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, f4, c1, COSH(f1)
from OPTABLE 
where TRIM(z) > 'Row07' and
(COSH(f4) is null or
COSH(f4) is not null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    stmt = """delete from OPTABLE 
where LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, f4, c1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv. b2, vv.psv
from voptbl vv left join OPTABLE t1 on
COSH(vv.f4) = COSH(t1.f4) and
COSH(SIN(vv.f5)) = COSH(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    
    stmt = """select c3, COSH(TANH(b1)), SQRT(COSH(b2))
from OPTABLE 
union all
select v.c1, v.b2, COSH(v.b2)
from voptbl v
left join voptbl1 on
v.z = voptbl1.z and
COSH(v.b1) = SINH(voptbl1.b1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    
    stmt = """select z, c3, COSH(TANH(b1)), SQRT(COSH(b2))
from OPTABLE 
union
select t1.z, t1.c1, t1.b2, COSH(t1.b2)
from OPTABLE t1
inner join voptbl1 on
t1.z = voptbl1.z and
ASIN(t1.b2 / 2000) = ASIN(voptbl1.b2 / 2000)
left join voptbl on
COSH(voptbl.psv) = COSH(voptbl1.psv)
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    
    stmt = """alter table OPTABLE 
drop constraint c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test007(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA06
    #  Description:        Tests for SQL, use of SIN function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SIN function syntax:
    # SIN{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.1415;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, b2, n2, SIN(b2), SIN(SIN(n2)), SQRT(SIN(?p)),
CEILING(SIN(0)), SIN(ACOS(f2)), SIN(TANH(f4))
from OPTABLE 
where SIN(f3) < PI() and
SIGN(SIN(f3)) = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    
    stmt = """select z, AVG(FLOOR(POWER(SIN(psv), 2))),
MAX(ceiling(EXP(SIN(psv)))),
SIN(ABS(f4)), RADIANS(COS(f5)),
SIN(123 * 3.1415926 / 180),
COS(SIN(45 * PI() / 180)),
SIN(b1 + 256 - b2 / 100),
SIN(ACOS(CAST('.14' as float) * pi() / 180)),
SIN(TANH(zi3 * pi())) / ASIN(d2 * 5e-4)
from OPTABLE 
where f4 > 0 and
t3 is not null
group by z, zi3, d2, f4, f5, psv, b1, b2
having SIN(f4) > 0
order by 1 asc, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    
    stmt = """select z, SIN(power(TAN(?p), 2) / 4000),
CASE
when sin(f4) > 1 then 100
when sin(f4) < -1 then -111
when sin(f4) = 0 then 999
else SIN(LOG10(.5))
END,
SIN(TANH(0.2 + 0.6 - 0.3) - TAN(-3.44E-2)),
f5, 99.81 * SIN(SINH(f5)),
SIN(LOG10(?p) + PI() / SIN(145 * PI() / 180)),
sin(COS(f5)), COS(SIN(f5)), SIN(COSH(f4))
from OPTABLE 
where sIN(sinh(f3)) =
(select SiN(sinh(f3))
from OPTABLE 
where	sinh(f3) < -.99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    
    stmt = """prepare p from
insert into OPTABLE values(
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, SIN(90 * pi() / 180), -5342, 4, null,
SIN(120 * pi() / 180), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = SIN(.5)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select f4, SIN(AVG(f1)), ASIN(SUM(psc) / 180),
sin(262), sin(261), sin(-262), sin(-261)
from OPTABLE 
where TRIM(z) > 'Row07' and
SIN(f4) < 180
group by f4, c1, f1, psc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    
    stmt = """delete from OPTABLE 
where SIN(f5) <> 9.61760009961632290E-001 and
LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select c1, c2, c3 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    
    stmt = """create view voptbl1 as
select vv.c1, vv.f4, vv.f5, vv.b2, vv.z, vv.ps9, vv.psv
from voptbl vv left join OPTABLE t1 on
SIN(vv.f4) = SIN(t1.f4) and
cos(siN(vv.f5)) = COS(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    
    stmt = """select z, c1, SIN(TANH(f4)), SQRT(abs(SIN(b2)))
from OPTABLE 
union all
select v1.z, v1.c3, sin(tanh(v1.f4)), sqrt(abs(sin(v1.b2)))
from voptbl v1
left join voptbl1 vv on
vv.z = v1.z and
SIN(vv.b2) = sin(v1.b2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    
    stmt = """select z, c3, ASIN(TANH(b1)), SQRT(abs(ASIN(b2  / 999999)))
from OPTABLE 
union
select t1.z, t1.c1, t1.b2, SIN(t1.b2 * 2)
from OPTABLE t1
inner join voptbl1 on
t1.z = voptbl1.z and
SIN(t1.b2 * PI() + 55.6) =
SIN(voptbl1.b2 * PI() + 55.6)
left join voptbl on
SIN(voptbl1.psv - COS(voptbl1.ps9  * 15e-7)) =
SIN(voptbl.psv - COS(voptbl.ps9  * 15e-7))
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test008(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA07
    #  Description:        Tests for SQL, use of SINH function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SINH function syntax:
    # SINH{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, psc, SINH(psc), SINH(SINH(f3)), SQRT(SINH(?p)),
CEILING(SINH(0)), SINH(ACOS(f2)), SINH(TANH(f4))
from OPTABLE 
where SINH(f3) < PI() and
SIGN(SINH(f3)) = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    
    stmt = """select z, SINH(45 * 3.1415926 / 180),
SINH(sInH(88 * PI() / 180)),
SINH(f2 / 1e9),
FLOOR(POWER(SINH(psv), 2)),
f4, SINH(ABS(f4)),
f5, RADIANS(SINH(f5)),
EXP(SINH(psv))
from OPTABLE 
where t3, c2 is not null
group by z, f2, b1, b2, f5, psv, f4
having Sinh(f4) > 0
order by f5, f4, 3 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    
    stmt = """select z, SINH(FLOOR(psv * 100) / SIN(145 * PI() / 180) / 10),
SINH(COS(f5)), SINH(SIN(f5)),
SINh(COSH(f4))
from OPTABLE 
where SINH(cos(f3)) =
(select SINH(cos(f3))
from OPTABLE 
where sinh(f3) < -.99);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    
    stmt = """select z, SINH(TAN(?p)), sinh(CAST('3.14' as float)),
CASE
when sinh(d2) > 1 then sinh(1)
when sinh(d2) < 0 then sinh(-1)
when sinh(d2) = 0 then sinh(0)
else SINH(log(.5))
END,
SINH(ACOS(0.2 + 0.6 - 0.3)) - 4.209,
9845.001 * SINH(COSH(d2 / 100)) / ATAN(SIN(f3)),
SINH(ATAN(zi3)) / ASIN(d2 / 650)
from OPTABLE 
where SINH(d2) not IN (30, 40, 60, 90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    
    stmt = """alter table OPTABLE 
add constraint c7 check (sinh(f1) < 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values(
1,  0,  100,  sinh(-.5),  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, null, ACOS(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = SINH(.05)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select f4, c1, SINH(f1),
SINH(SUM(psc) / 180)
from OPTABLE 
where TRIM(z) > 'Row07'
group by f4, c1, f1, psc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    
    stmt = """delete from OPTABLE 
where f4 = sinH(0.05) and
trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select c1, c2, c3, t3, f4
from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    
    stmt = """create view voptbl1 as
select vv.c2, vv.t1, vv.z, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
SINH(vv.f4) = sinh(t1.f4) and
SINH(cosh(vv.f5)) = sinh(cosh(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select c2, t1, b1, b2, psv
from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    
    stmt = """select z, c2, SINH(TANH(b1)), SINH(b2)
from OPTABLE 
union all
select v1.z, v1.c2, sinh(tanh(v1.b1)), SINH(v1.b2)
from voptbl v1
left join voptbl1 on
v1.z = voptbl1.z and
SINH(v1.b2) = sinh(voptbl1.b1)
right join voptbl v2 on
v2.z = voptbl1.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    stmt = """alter table OPTABLE 
drop constraint c7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test009(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA08
    #  Description:        Tests for SQL, use of TAN function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # TAN function syntax:
    # TAN{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, TAN(d1), SIN(SIN(f2)), SQRT(TAN(?p)),
CEILING(TAN(0)), TAN(ACOS(f2)), TAN(TANH(f4))
from OPTABLE 
where TAN(f3) < PI() and
SIGN(TAN(f3)) = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    
    stmt = """select z, f4, f5, psv, FLOOR(POWER(TAN(psv), 2)),
FLOOR(EXP(TAN(psv))),
TAN(ABS(f4)), RADIANS(TANH(f5)),
TAN(TANH(45 * PI() / 180))
from OPTABLE 
where t3, c2 is not null and
TAN(d2 / 100) between -0.1 and 0.5
group by z, f4, f5, psv
having TAN(f4) > 0
order by 1 asc, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    
    stmt = """prepare p from
select TAN(45 * 3.1415926 / 180), TAN(TANH(45 * PI() / 180)),
b1, b2, TAN(b1 + 256 - b2 / 100), t3
from OPTABLE 
where t3 is null and
c2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    
    stmt = """select z, TAN(power(TAN(?p), 2)), TAN(CAST('3.14' as float)),
CASE TAN(0.5)
when 30 then 30 * PI() / 180
when 45 then 45 * PI() / 180
when 90 then 90 * PI() / 180
else TAN(LOG10(.5))
END,
TAN(SIN(0.2 + 0.6 - 0.3)) / SIN(TAN(psc)) - SIN(COS(f4)),
7.2E+3 * TAN(COs(d2 / 100)) * TAN(ATAN(u3)) + 100,
TAN(COS(f5)), TAN(ATAN(f5)), TAN(TANH(f1))
from OPTABLE 
where TAN(ceiling(f3)) =
(select TAN(ceiling(f3))
from OPTABLE 
where ceiling(f3) < 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    
    stmt = """prepare p from
insert into OPTABLE values(
1.223e18,  0, 767,  TAN(90 * pi() / 180),
1, 1, date '1960-02-01', 'b'  ,
10, 10, 21486, -1.27e-18, 43, 23, time '00:12:00', 'as', -2418,
786,  -49761,  -0.159,  10,  -2.27264,
interval '00:33:33' hour to second, 'aaz', 'Row09',
0.36, 0.9, 1999, 9, -2.5E-8, 3.02E-8,
1.76E-3, -0.5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = TAN(.05)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select c1, f4,
tan(262), tan(259), tan(-262), tan(-259)
from OPTABLE 
where TRIM(z) > 'Row07' and
TAN(f4) < 180;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    
    # Added this query to test the number < 263, > -263.
    stmt = """select tan( 262.9999999999999999999999999999999999),
tan(-262.99999999999999)
from OPTABLE 
where trim(z) = 'Row07';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6a')
    
    stmt = """delete from OPTABLE 
where f4 = tan(.05) and
LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select c1, f5, f4 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.c1
from voptbl vv left join OPTABLE t1 on
Tan(vv.f4) = ATAN(t1.f4) and
tAN(SIN(vv.f5)) = TaN(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select c1 from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s9')
    
    stmt = """select z, c1, TAN(TANH(b1)), SQRT(abs(TAN(b2)))
from OPTABLE 
union all
select v.z, v.c3, v.b2, TAN(v.b2)
from voptbl v
left join voptbl1 on
v.z = voptbl1.z and
TAN(COs(v.b2)) = ATAN(COs(voptbl1.b1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s10')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test010(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA09
    #  Description:        Tests for SQL, use of TANH function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # TANH function syntax:
    # TANH{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p -3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, TANH(f1), TANH(COSH(f3)), SQRT(abs(TANH(?p))),
CEILING(TANH(0)), TANH(ACOS(f2)), TANH(TANH(f4))
from OPTABLE 
where TANH(f3) < PI() and
SIGN(TANH(f3)) = 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    
    stmt = """select z, FLOOR(POWER(TANH(psv), 2)),
FLOOR(EXP(TANH(psv))),
TANH(ABS(f4)), DEGREES(TANH(f5)),
TANH(b1 + 256 - b2 / 100),
TANH(SINH(45 * PI() / 180))
from OPTABLE 
where t3 is not null
group by z, psv, f4, f5, b1, b2
having TANH(f4) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    
    stmt = """select z, TANH(LOG10(abs(cast(?p as float)))) + PI() / SIN(145 * PI() / 180),
TANH(COS(f5)), TANH(SIN(f5)), TANH(COSH(f4)),
f5, f4
from OPTABLE 
where TANH(f3) =
(select TANH(f3)
from OPTABLE 
where tanh(f5) < -.75 and
tanh(f5) > -.76);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    stmt = """select z, TANH(power(TAN(?p), 2)), TANH(CAST('3.14' as float)),
CASE TANH(0.5)
when 30 then 30 * PI() / 180
when 45 then 45 * PI() / 180
when 90 then 90 * PI() / 180
else TANH(LOG10(.5))
END,
398.4505E-5 / TANH(COS(0.2 + 0.6 - 0.3)),
3.1E-3 * TANH(sin(ps9 * 11e-5)) / 05.37 - TANH(ATAN(u3))
from OPTABLE 
where TANH(f3) =
(select TANH(f3)
from OPTABLE 
where tanh(f3) < -.761) and
TANH(d2) not IN (30, 40, 60, 90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    
    stmt = """insert into OPTABLE values(
1.23e18,  1, 77,  TANh(90 * pi() / 180),
1, 0, date '1960-02-11', 'b'  ,
10, 10, 21486, -1.2e-18, 4, 3, time '01:12:00', 'a1', -218,
761,  -4261,  -0.159,  1,  -2.22764,
interval '00:36:33' hour to second, 'abz', 'Row09',
0.333, 0.9, 129, 9, -2.55E-8, 3.022E-8,
1.766E-3, -0.8
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = tAnH(.05)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select c1, f4
from OPTABLE 
where TRIM(z) > 'Row07';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    
    stmt = """delete from OPTABLE 
where f4 = TANH(0.05) and
LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.c1
from voptbl vv left join OPTABLE t1 on
TANH(vv.f4) = TANH(t1.f4) and
TANH(SIN(vv.f5)) = TANH(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    
    stmt = """select z, c, b1 from (
select t1.z, t1.c2, MIN(TANH(SINH(t1.b1)))
from OPTABLE t1
group by t1.z, t1.c2, t1.b1
union all
select v1.z, v2.z, SUM(TANH(v1.b1))
from voptbl v1
left join voptbl1 vv on
v1.z = vv.z and
TANH(v1.b2) = TANH(vv.b1)
right join voptbl v2 on
vv.z = v2.z
group by v1.z, v2.z, v1.b1)
x(z, c, b1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test011(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA10
    #  Description:        Tests for SQL, use of ATAN2 function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ATAN2 function syntax:
    # ATAN2{(<float-exp1>, <float-exp2>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, psv, p9c, ATAN2(psc, p9c), zi3, f5,
ATAN2(ATAN2(zi3, f4), f5),
SQRT(ATAN2(?p, f4)), CEILING(ATAN2(0, 1)),
ATAN2(ACOS(f2), SIN(f2)),
ATAN2(TANH(f4), .3)
from OPTABLE 
where ATAN2(f3, 0) < PI() and
SIGN(ATAN2(f3, .2)) > .314159
group by z, f4, f5, f2, psv, psc, p9c, zi3
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    
    stmt = """prepare p from
select z, FLOOR(POWER(ATAN2(psv, .743), 2)),
psv, FLOOR(EXP(ATAN2(psv, 123124153254.9999999))),
ATAN2(ABS(f4), 540.01),
RADIANS(ATAN2(f5, psv))
from OPTABLE 
where t3 is null and
c2 is not null
group by z, psv, f4, f5
having ATAN2(f4, 0) > 0
order by psv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    
    stmt = """select z, ATAN2(LOG10(?p), ?p) + PI() - FLOOR(psv * 100) / SIN(145 * PI() / 180),
ATAN2(COS(f5), -32.4), ATAN2(SIN(f5), -99.99),
ATAN2(COSH(f4), 100)
from OPTABLE 
where aTAn2(f3, 0) =
(select ATAN2(f3, 0)
from OPTABLE 
where atan2(f5, pi()) > 0.11)
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    
    stmt = """select z, ATAN2(TAN(?p), 2), ATAN2(CAST('3.14' as float), 10),
CASE
when ATAN2(0.5, ps9) > 1 then atan2(sinh(ps9 * 10e-6), 1)
when ATAN2(0.5, ps9) < 0 then atan2(cosh(ps9 * 20e-5), -1)
when ATAN2(0.5, ps9) = 0 then atan2(90 * PI() / 180, 0)
else ATAN2(.5, ps9)
END,
ATAN2(8.1 / 99.37 * 100000, LOG10(500000.999999)),
ATAN2(Cos(f2), 8.203E-2),
ATAN2(tanh(d2) + 8.203E-2, ATAN2(u3, ATAN(zi3)))
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    
    stmt = """prepare p from
insert into OPTABLE values(
1.223e18,  0, 767,  aTAN2(90 * pi() / 180, sin(pi())),
1, 1, date '1960-02-01', 'b'  ,
10, 10, 21486, -1.27e-18, 43, 23, time '00:12:00', 'as', -2418,
786,  -49761,  -0.159,  10,  -2.27264,
interval '00:33:33' hour to second, 'aaz', 'Row09',
0.36, 0.9, 1999, 9, -2.5E-8, 3.02E-8,
1.76E-3, -0.5
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    
    stmt = """update OPTABLE set f4 = ATAN2(.05, -0.0005)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # AR added order by
    stmt = """select z, f4, ATAN2(AVG(f1), SUM(f4))
from OPTABLE 
where TRIM(z) > 'Row07'
group by z, f4, f1 order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    
    stmt = """delete from OPTABLE 
where f4 = ATAN2(.05, -0.0005) and
LTRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.c1
from voptbl vv left join OPTABLE t1 on
ATAN2(vv.f4, -150) = ATAN2(t1.f4, -150) and
ATAN2(SIN(vv.f5), -99999) =
ATAN2(SIN(t1.f5), -99999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    
    stmt = """select z, TANH(b1), ATAN2(TANH(b1), ?p)
from OPTABLE 
union all
select trim(v1.z), v1.b2, ATAN2(v1.b2, -100000)
from voptbl v1
left join voptbl1 vv1 on
v1.z = vv1.z and
ATAN2(v1.b2, PI()) = ATAN2(vv1.b2, PI())
right join voptbl v2 on
v2.z >= vv1.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test012(desc="""a11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA11
    #  Description:        Tests for SQL, use of DEGREES function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # DEGREES function syntax:
    # DEGREES{(<numeric-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, DEGREES(-.00159), sinh(DEGREES(90 * pi() / 180)),
DEGREES(1839 * pi() / 180 + 1009 / 500),
DEGREES(-9342.764134) / cosh(DEGREES(0.5)) -?p,
CASE trim(z)
WHEN 'Row01' THEN DEGREES(0.5)
WHEN 'Row02' THEN DEGREES(-0.5)
WHEN 'Row04' THEN Degrees(0.66668)
WHEN 'Row06' THEN DEGRees(-0.7071067)
WHEN 'Row07' THEN DegREES(TAN(1 - 0.246446))
WHEN 'Row08' THEN DEGREES(COS(-0.866825))
ELSE  DEGREES(SIN(-1))
END
from OPTABLE 
where DEGREES(zi1) < 1000 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    
    stmt = """select z, f1, SIGN(DEGREES(f1) / ATAN2(f1, 100 - 350)),
DEGREES(ACOS(f3)) * DEGREES(COS(SIN(ABS(-0.707106781186)))),
DEGREES(SQRT(abs(TANH(-.3333333333)))),
degrees(radians(degrees(radians(f1)))), degrees(0000)
from OPTABLE 
group by z, f1, f3, p1
having DEGREES(p1) > 180
order by f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    
    stmt = """select z, zi1, DEGREES(CAST('-9.873265e+13' as largeint)),
DEGREES(CAST(psc as smallint)),
CASE
WHEN DEGREES(zi1) < 0 THEN RADIANS(zi1)
WHEN DEGREES(zi1) > 0 THEN DEGREES(-0.666667)
ELSE DEGREES(TANH(pi()) - 1)
END,
CEILING(DEGREES(zi1)), FLOOR(DEGREES(zi1)),
POWER(2, DEGREES(f3))
from OPTABLE 
where DEGREES(zi1) > 0 and
z is not null
group by z, zi1, psc, f3
order by z, zi1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    
    stmt = """prepare p from
insert into OPTABLE values (
9.23e8,  1,  3767,  0,  1,  11, date '1966-11-01', 'a'  ,
10, 10, 21366, -1.17e8, 10, 10, time '00:00:00', 'aa' ,
-2418, 6786,  -4761,  DEGREES(SIN(-261)),  10,  -2.64,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.356, 1.99, 99, 9, -2.225E-8, 3.402E8,
1.7976E-3, DEGREES(-0.0000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    
    stmt = """update OPTABLE set u1 = DEGREES(abs(TANH(-0.7078)))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = cast(DEGREES(abs(TANH(-0.7078))) as smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select z, DEGREES(LOG(n1) + ?p), DEGREES(LOG10(u1 * 13)),
DEGREES(EXP(n1)),
char(cast(abs(DEGREES(f3)) as integer)),
f2
from OPTABLE 
where SQRT(DEGREES(abs(f2))) = (
select SQRT(DEGREES(abs(f2)))
from OPTABLE 
where f2 > 0.9) and
u1 <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    
    stmt = """create view voptbl1 as
select vv.z, vv.f4, vv.b1, vv.b2, vv.psv, vv.c3
from voptbl vv left join OPTABLE t1 on
DEGREES(Atan(vv.f4)) = DEGREES(Atan(t1.f4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    stmt = """select t1.z, t1.c1, t1.b2,
DEGREES(ACOS(TANH(t1.b1) * 5E-6)),
SQRT(DEGREES(abs(RADIANS(DEGREES(RADIANS(t1.b2))))))
from OPTABLE t1
union all
select v1.z, v1.c3, v1.psv, v1.b1,
DEGREES(DEGREES(atan2(v1.psv, v1.psv)))
from voptbl v1
left join voptbl1 vv on
v1.z = vv.z and
DEGREES(RADIANS(v1.b2)) =
DEGREES(RADIANS(vv.b2)) and
vv.z > 'Row05'
right join voptbl v2 on
v2.z >= vv.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s9')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test013(desc="""a12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA12
    #  Description:        Tests for SQL, use of RADIANS function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RADIANS function syntax:
    # RADIANS{(<numeric-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, RADIANS(-.00159), atan(radians(580 * pi() / 180)),
RADIANS(1839 * pi() / 180 + 1009 / 500),
RADIANS(-9342.764134) / degrees(0.5) * RADIANS(-.66666668),
CASE trim(z)
WHEN 'Row01' THEN RADIANS(0.5)
WHEN 'Row02' THEN RADIANS(-0.5)
WHEN 'Row04' THEN RADIANS(0.66668)
WHEN 'Row06' THEN raDians(-0.7071067)
WHEN 'Row07' THEN RAdiaNs(TAN(1 - 0.246446))
WHEN 'Row08' THEN RADIANS(COS(-0.866825))
ELSE  RADIANS(SIN(-?p))
END
from OPTABLE 
where RADIANS(zi1) < 1000 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    
    stmt = """select z, f1, SIGN(RADIANS(f1) / ATAN2(f1, 100 - 350)),
f3,
RADIANS(ACOS(f3)) * RADIANS(COS(SIN(ABS(-0.707106781186)))),
RADIANS(SQRT(TANH(abs(-.3333333333)))),
radians(000)
from OPTABLE 
group by z, f1, f3, p1
having RADIANS(p1) between -0.15 and 180
order by f1, f3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    
    stmt = """select z, zi1, RADIANS(CAST('-9.873265e+3' as largeint)),
RADIANS(CAST(ps9 as double precision)),
CASE
WHEN RADIANS(zi1) < 0 THEN DEGREES(zi1)
WHEN radians(zi1) > 0 THEN RADIANS(-0.666667)
ELSE RADIANS(TANH(pi()) - 1)
END,
CEILING(radians(zi1)), FLOOR(radians(zi1)),
POWER(2, RADIANS(f4))
from OPTABLE 
where RADIANS(zi1) > 0 and
z is not null
group by z, zi1, ps9, f4
order by z, zi1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    
    stmt = """insert into OPTABLE values (
9.223e1,  10,  37,  10,  10,  10, date '1996-01-01', 'a'  ,
10, 10, 8366, -1.17e18, 10, 10, time '00:00:00', 'aa' , -2418,
236,  -4928,  RADIANS(-800),  10,  -2.22214,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.356, 1.99, 99, 9, -2.225E-30, 3.402E3,
1.7976E-3, RADIANS(-0.000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    
    stmt = """update OPTABLE set u1 =
RADIANS(cast(TANH(0.7078) as double precision))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select z, RADIANS(LOG(n1 + 10000)), radians(LOG10(u1) * ?p),
RADIANS(EXP(d1)), radians(d3),
f2
from OPTABLE 
where RADIANS(degrees(f2)) = (
select RADIANS(DEGREES(f2))
from OPTABLE 
where f2 > 0.9) and
u1 <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, c2, t1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    
    stmt = """create view voptbl1 as
select vv.z, t1.c3, t1.t1, vv.b2, vv.c2, t1.psv
from voptbl vv left join OPTABLE t1 on
DEGREES(RADIANS(vv.f4)) = DEGREES(RADIANS(t1.f4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, t1 from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    
    stmt = """select z, c1, RADIANS(TANH(b1) / PI() + ?p),
SQRT(RADIANS(TAN(b2) + LOG(27) * 33))
from OPTABLE 
union
select t1.z, t1.c1, RADIANS(TANH(t1.b1) / PI() + ?p),
SQRT(RADIANS(TAN(t1.b2) + LOG(27) * 33))
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
RADIANS(t1.b2 - LOG10(37) * 19) =
RADIANS(vv.b2 - LOG10(37) * 19)
left join voptbl v on
RADIANS(PI() / vv.psv) =
RADIANS(3.14159265359 / v.psv)
order by c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test014(desc="""a13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA13
    #  Description:        Tests for SQL, use of ABS() function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # abs function syntax:
    # abs{(<numeric-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, abs(-.00159), cosh(abs(580 * pi() / 180)),
abs(1839 * pi() / 180 + 1009 / 500), sqrt(abs(-0.00000007)),
abs(-9342.764134) / abs(0.5) * DEGREES(-.66666668) - abs(-?p),
CASE trim(z)
WHEN 'Row01' THEN abs(0.5)
WHEN 'Row02' THEN abs(-0.5)
WHEN 'Row04' THEN abs(0.66668)
WHEN 'Row06' THEN abs(-0.7071067)
WHEN 'Row07' THEN abs(TAN(1 - 0.246446))
WHEN 'Row08' THEN abs(COS(-0.866825))
ELSE  abs(SIN(-1))
END
from OPTABLE 
where abs(zi1) < 1000 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    
    stmt = """select z, f1, SIGN(abs(f1) / ATAN2(f1, 350)),
abs(ACOS(f2)) * abs(COS(SIN(ABS(-0.707106781186)))),
SQRT(abs(TANH(-.3333333333))),
abs(00), abs(-00)
from OPTABLE 
group by z, f1, f2, p1
having aBs(p1) > 180
order by z desc, f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    
    stmt = """select z, zi1, Abs(CAST('-9.873265e+10' as largeint)),
abS(CAST(ps9 as double precision)),
CASE
WHEN abs(zi1) < 0 THEN abs(zi1)
WHEN abs(zi1) > 0 THEN DEGREES(-0.666667)
ELSE abs(TANH(pi() - 1))
END,
CEILING(abs(zi1)), abs(FLOOR(DEGREES(zi1))),
POWER(2, abs(f1))
from OPTABLE 
where abs(zi1) > 17 and
z is not null
group by z, f1, zi1, ps9
order by z, zi1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    
    stmt = """insert into OPTABLE values (
9.23e8,  1,  767,  0,  1,  0, date '1900-01-01', 'a'  ,
10, 10, 66, -1.17e18, 1, 1, time '00:00:00', 'aa' , -218,
56,  -761,  abs(SIN(-8)),  10,  -2.2224,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.36, .99, 999, 9, -2.25E-3, 3.0E3,
1.7E-3, abs(-0.000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    
    stmt = """update OPTABLE set u1 = abs(00000000)
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select z, abs(LOG(n1) + ?p), abs(LOG10(u1 * 13)),
abs(EXP(f1)), f2
from OPTABLE 
where SQRT(abs(f2)) = (
select SQRT(abs(f2))
from OPTABLE 
where f2 > 0.9) and
u1 <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    
    stmt = """create view voptbl1 as
select t1.z, t1.c2, t1.t1, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
abs(degrees(vv.f4)) = abs(DEGREES(t1.f4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c2, t1 from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    
    stmt = """select c3, abs(TANH(b1) / PI() + ?p),
SQRT(abs(TAN(b2) + LOG(27) * 33))
from OPTABLE 
union
select TRIM(t1.z), t1.b2,
abs(TAN(t1.b2 + POWER(t1.b2, 2) / 100))
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
abs(COs(t1.b2 - LOG10(37) * 19)) =
abs(COs(vv.b2 - LOG10(37) * 19))
left join voptbl v on
abs(PI() / vv.psv) =
abs(3.14159265359 / v.psv)
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test015(desc="""a14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA14
    #  Description:        Tests for SQL, use of CEILING function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # CEILING function syntax:
    # CEILING{(<numeric-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, CEILING(-.00159E+15),
CEILING(radians(580 * pi() / 180)),
CEILING(1839 * pi() / 180 + 1009 / TANH(-30)),
CEILING(-9342.764134) / degrees(0.5) * RADIANS(-.66666668),
CASE trim(z)
WHEN 'Row01' THEN CEILING(0.5)
WHEN 'Row02' THEN CEILING(-0.5)
WHEN 'Row04' THEN CEILING(0.66668)
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN CEILING(TAN(1 - 0.246446))
WHEN 'Row08' THEN CEILING(COS(-0.866825))
ELSE  MAX(CEILING(SIN(-?p)))
END
from OPTABLE 
where CEILING(b1) in
(1.0, -1.7976E3, -2.2250E-8) and
d3, z is not null and
floor(b1) between -1 and 17
group by z
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    
    stmt = """select z, f1, SIGN(CEILING(f1)),
CEILING(f3) * RADIANS(COS(SIN(ABS(-0.707106781186)))),
Ceiling(ACOS(f3)),
RADIANS(SQRT(abs(TANH(-.3333333333)))),
ceiling(radians(-000))
from OPTABLE 
group by z, f1, f3, p1
having CEILING(p1) > 180
order by z, f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    
    stmt = """select z, zi1, CEILING(CAST('-9.873265e+2' as largeint)),
CEILING(CAST(ps9 as real)),
CASE
WHEN CeiLing(zi1) < 0 THEN DEGREES(zi1)
WHEN radians(zi1) > 0 THEN CEILING(-0.666667)
ELSE CEILING(TANH(pi()) - 1)
END,
CEILING(CEILING(radians(zi1))),
FLOOR(CEILING(DEGREES(zi1))),
POWER(2, CEILING(f4))
from OPTABLE 
where CEILING(zi1) > 0 and
z is not null
group by z, zi1, ps9, f4
order by z, zi1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    
    stmt = """prepare p from
insert into OPTABLE values (
9.23e8,  1,  767,  0,  1,  0, date '1872-01-01', 'a'  ,
10, 10, 66, -1.17e18, 1, 1, time '00:00:00', 'aa' , -218,
56,  -761,  abs(ceiling(-8.6)),  10,  -2.2224,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.36, .99, 999, 9, -2.25E-3, 3.0E3,
1.7E-3, abs(-0.000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    
    stmt = """update OPTABLE set u1 = CEILING(TANH(-0.7078))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = CEILING(TANH(-0.7078));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select z, SUM(CEILING(LOG(n1 + 10000))),
DEGREES(CEILING(LOG10(u1) * ?p)),
CEILING(EXP(MIN(n2))), CEILING(LOG(d3)),
CEILING(DEGREES(d3)),
CEILING(?p)
from OPTABLE 
where SQRT(CEILING(f2)) = (
select SQRT(CEILING(f2))
from OPTABLE 
where f2 > 0.9) and
u1 <> 0 and
d3 > 0
group by z, n1, u1, p1, d3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, f1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s7')
    
    stmt = """create view voptbl1 as
select vv.z, vv.c2, vv.t1, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
DEGREES(CEILING(vv.f4)) = DEGREES(CEILING(t1.f4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c2, t1 from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s8')
    
    stmt = """select c3, b1, CEILING(DEGREES(TANH(RADIANS(b1) * 5E-6))),
SQRT(CEILING(b2))
from OPTABLE 
union all
select trim(v1.z), v1.psv, CEILING(v1.psv),
SQRT(CEILING(v1.b2))
from voptbl v1
left join voptbl1 on
v1.z = voptbl1.z and
CEILING(Cosh(v1.b2)) = CEILING(Cosh(voptbl1.b2)) and
v1.z > 'Row05'
right join voptbl v2 on
v2.z >= voptbl1.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s9')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test016(desc="""a15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA15
    #  Description:        Tests for SQL, use of FLOOR function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # FLOOR function syntax:
    # FLOOR{(<numeric-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare p from
select z, FLOOR(-.00159E+15),
FLOOR(radians(580 * pi() / 180)),
FLOOR(1839 * pi() / 180 + 1009 / TANH(500)),
FLOOR(-9342.764134) / degrees(0.5) * FLOOR(RADIANS(-.66666668)),
CASE trim(z)
WHEN 'Row01' THEN FLOOR(0.5)
WHEN 'Row02' THEN FLOOR(-0.5)
WHEN 'Row04' THEN FLOOR(0.66668)
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN FLOOR(TAN(1 - 0.246446))
WHEN 'Row08' THEN FLOOR(COS(-0.866825))
ELSE  Floor(SIN(-?p))
END
from OPTABLE 
where flOOR(zi1) < 1000 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    
    stmt = """select z, SIGN(FLOOR(f1) / ATAN2(f1, 350)),
FLOor(ACOS(f3)) * RADIANS(COS(SIN(ABS(-0.707106781186)))),
RADIANS(SQRT(TANH(33333.33333))),
ceiling(-000.00001)
from OPTABLE 
group by z, f1, b1, f3
having FLoOR(b1) between -999.999 and -1
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    
    stmt = """select z, zi1, FLOOR(CAST('-9.873265e+2' as largeint)),
FLOOR(CAST(f2 as smallint)),
CASE
WHEN FLOOR(zi1) < 0 THEN ceiling(zi1)
WHEN radians(zi1) > 0 THEN FLOOR(-0.666667)
ELSE FLOOR(TANH(pi()) - 1)
END,
FLOOR(CEILING(radians(zi1))), FLOOR(DEGREES(ceiling(zi1))),
POWER(2, FLOOR(psv))
from OPTABLE 
where FLOOR(zi1) > 0 and
z is not null
group by z, zi1, f2, psv
order by z, zi1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    
    stmt = """prepare p from
insert into OPTABLE values (
9.23e8,  1,  3767,  0,  1,  11, date '1996-11-01', 'a'  ,
10, 10, 21366, -1.17e8, 10, 10, time '00:00:00', 'aa' ,
-2418, 6786,  -4761,  floor(SIN(-21)),  10,  -2.64,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.356, 1.99, 99, 9, -2.225E-8, 3.402E8,
1.7976E-3, DEGREES(-0.0000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    
    stmt = """update OPTABLE set u1 = FLOOR(TANH(0.7078))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = FLOOR(TANH(0.7078));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """select z, FLOOR(LOG(n1 + 10000)), DEGREES(CEILING(LOG10(u1) * ?p)),
FLOOR(EXP(f1)), floor(LOG(abs(f3))),
FLOOR(DEGREES(d3)),
FLOOR(?p)
from OPTABLE 
where SQRT(FLOOR(abs(radians(degrees(f2))))) = (
select SQRT(FLOOR(abs(RADIANS(DEGREES(f2)))))
from OPTABLE 
where f2 > 0.9) and
u1 <> 0 and
d3 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.c3, vv.t1, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
DEGREES(FLOOR(vv.f4)) = DEGREES(floor(t1.f4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s9')
    
    stmt = """select c3, FLOOR(TANH(b1) / PI() + ?p),
SQRT(FLOOR(TAN(b2) + LOG(27) * 33))
from OPTABLE 
union
select TRIM(t1.z), t1.b2,
FLOOR(TAN(t1.b2 + POWER(t1.b2, 2) / 100))
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
FLOOR(t1.b2 - LOG10(37) * 19) =
FLOOR(vv.b2 - LOG10(37) * 19)
left join voptbl v1 on
FLOOR(PI() / vv.psv) = FLOOR(3.14159265359 / v1.psv)
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s10')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test017(desc="""a16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA16
    #  Description:        Tests for SQL, use of EXP function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # EXP function syntax:
    # EXP{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, EXP(-.00159E+5), exp(?p),
EXP(radians(580 * pi() / 180)),
EXP(19 * pi() / 180 + 109 / TANH(503)),
EXP(-94.7) / degrees(0.5) * RADIANS(-.66666668),
CASE rtrim(z)
WHEN 'Row01' THEN EXP(0.5)
WHEN 'Row02' THEN EXP(-0.5)
WHEN 'Row04' THEN EXP(0.66668)
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN EXP(TAN(1 - 0.246446))
WHEN 'Row08' THEN ExP(COS(-0.866825))
ELSE  Exp(SIN(-?p))
END
from OPTABLE 
where eXP(b1) between 1 and 4 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    
    stmt = """select z, SIGN(EXP(f1) / ATAN2(f1, 35)),
EXP(ACOS(f3)) * exp(COS(SIN(ABS(-0.707106781186)))),
exp(SQRT(TANH(3333333333))),
exp(-000.0000)
from OPTABLE 
where p1 < 150
group by z, f1, f3, p1
having EXP(p1) > 180
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    
    stmt = """select z, EXP(CAST('-9.875e-3' as largeint)),
EXP(CAST(f4 as real)),
CASE
WHEN EXP(zi1/1000) < 0 THEN exp(zi1/1000)
WHEN exp(zi1/1000) > 0 THEN EXP(-0.666667)
ELSE EXP(TANH(pi()) - 1)
END,
EXP(CEILING(radians(zi1))),
EXP(FLOOR(CEILING(DEGREES(f2)))),
POWER(12, EXP(f1))
from OPTABLE 
where zi1 < 79 and
EXP(zi1/1000) > 0 and
z is not null
group by z, zi1, f1, f2, f4
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    
    stmt = """alter table OPTABLE 
add check (exp(f1) > 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values(
1.223e18,  0, 767,  aTAN2(90 * pi() / 180, sin(pi())),
1, 1, date '1960-02-01', 'b'  ,
10, 10, 21486, -1.27e-18, 43, 23, time '00:12:00', 'as', -2418,
786,  -49761,  -0.159,  exp(-81),  -2.27264,
interval '00:33:33' hour to second, 'aaz', 'Row09',
0.36, 0.9, 1999, 9, -2.5E-8, 3.02E-8,
1.76E-3, abs(exp(-0.5))
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    
    stmt = """update OPTABLE set u1 = EXP(TANH(-0.7078))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, u1, t1 from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = cast(EXP(TANH(-0.7078)) as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select z, u1
from OPTABLE 
where z > 'Row03';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    
    stmt = """select trim(z),
exp(99.99),
exp(-99.9999),
exp(0.000001),
exp(-0.0000001)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s6')
    
    stmt = """select z, EXP(LOG(n1 + 10000)), exp(CEILING(LOG10(u1) * ?p)),
EXP(EXP(f1)), exp(LOG(d3)),
EXP(DEGREES(p9c)),
EXP(?p)
from OPTABLE 
where EXP(radians(degrees(f2))) = (
select EXP(RADIANS(DEGREES(f2)))
from OPTABLE 
where f2 > 0.9) and
u1 <> 0 and
d3 > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s7')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, t1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.psv, vv.c2, vv.t1
from voptbl vv left join OPTABLE t1 on
DEGREES(EXP(vv.f4)) = DEGREES(exp(t1.f4));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c2, t1 from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s9')
    
    stmt = """select c3, EXP(TANH(b1) / PI() + ?p),
SQRT(EXP(TAN(b2) + LOG(27) * 33))
from OPTABLE 
union
select TRIM(t1.z), t1.b2,
EXP(TAN(t1.b2 + POWER(t1.b2, 2) / 100))
from OPTABLE t1
inner join voptbl1 on
t1.z = voptbl1.z and
EXP(t1.b2 - LOG10(37) * 19) =
EXP(voptbl1.b2 - LOG10(37) * 19)
left join voptbl on
EXP(PI() / voptbl1.psv) =
EXP(3.14159265359 / voptbl.psv)
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s10')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test018(desc="""a17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA17
    #  Description:        Tests for SQL, use of LOG function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LOG function syntax:
    # LOG{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, LOG(.00159E+15), LOG(?p),
max(LOG(radians(580 * pi() / 180))),
LOG(1839 * pi() / 180 + 009 / ATAN2(500, -30)),
LOG(9342.764134) / degrees(0.5) * RADIANS(-.66666668),
CASE trim(z)
WHEN 'Row01' THEN LOG(abs(f1))
WHEN 'Row02' THEN LOG(abs(log(abs(f1))))
WHEN 'Row04' THEN LOG(f2 + 555777)
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN LOG(TAN(1 - 0.246446))
WHEN 'Row08' THEN LOG(COS(-0.866825))
ELSE  LOG(SIN(-?p))
END
from OPTABLE 
where u1 <> 0 and
LOG(u1) is not null and
d3, z is not null
group by z, f1, f2, u1
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    
    # Following query generates non-deterministic behavior depends on how the
    # compiler eveluate the predicate expression. Please see the detail on
    # QC 1491
    # rewrite the query so it won't evaluate the u2<>0 and log(abs(u2)) at the
    # same
    stmt = """create volatile table a17_volt1
(z char(8), u2 integer unsigned,exp1 float, exp2 float, exp3 float) no partition
as select z, u2, SIGN(LOG(abs(f1)) / TANh(f1) + 100 - 350),
LOG(abs(ACOS(f4))) * lOg(COS(SIN(ABS(-0.76781186)))),
log(SQRT(abs(TANH(f2))))
from OPTABLE 
where u2 <> 0
group by z, f1, f2, f4, u2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 8)
    
    #select z, SIGN(LOG(abs(f1)) / TANh(f1) + 100 - 350),
    #       LOG(abs(ACOS(f4))) * lOg(COS(SIN(ABS(-0.76781186)))),
    #       log(SQRT(abs(TANH(f2))))
    #  from optable
    # where u2 <> 0
    # group by z, f1, f2, f4, u2
    #having loG(abs(u2)) between -1 and 18
    # order by z desc;
    stmt = """select z,exp1,exp2,exp3 from a17_volt1 where log(abs(u2)) between -1 and 18 order by z desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    
    stmt = """drop volatile table a17_volt1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create volatile table a17_volt2
(z char(8), u1 smallint unsigned,exp1 float,exp2 float,exp3 float,exp4 float, exp5 float,
exp6 float) no partition
as
select z, u1, LOG(CAST(pi() as largeint)),
LOG(abs(CAST(ps9 as double precision))),
CASE
WHEN LOG(abs(zi1)) < 1 THEN SUM(log(abs(zi1)))
WHEN exp(zi1/1000) > 0 THEN LOG(0.666667)
ELSE LOG(abs(TANH(pi()) - 1))
END,
LOG(CEILING(abs(radians(zi1)))),
log(FLOOR(DEGREES(abs(zi1)))),
POWER(2, LOG(pi()))
from OPTABLE 
where zi1 < 78 and
u1 <> 0 and
z is not null
group by z, ps9, zi1, u1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    #select z, LOG(CAST(pi() as largeint)),
    #       LOG(abs(CAST(ps9 as double precision))),
    #       CASE
    #	  WHEN LOG(abs(zi1)) < 1 THEN SUM(log(abs(zi1)))
    #	  WHEN exp(zi1/1000) > 0 THEN LOG(0.666667)
    #	  ELSE LOG(abs(TANH(pi()) - 1))
    #       END,
    #       LOG(CEILING(abs(radians(zi1)))),
    #       log(FLOOR(DEGREES(abs(zi1)))),
    #       POWER(2, LOG(pi()))
    #  from optable
    # where zi1 < 78 and
    #       u1 <> 0 and
    #       LOG(u1) > 0 and
    #       z is not null
    # group by z, ps9, zi1, u1
    # order by z;
    stmt = """select z,exp1,exp2,exp3,exp4,exp5,exp6 from a17_volt2 where LOG(u1) > 0  order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    
    stmt = """drop volatile table a17_volt2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into OPTABLE values(
1,  0,  log(100),  acos(-.5),  10,  10, date '1960-01-01',  'a'  ,
.566,  0.14147,  -.1,  -1,  0,  0, time '00:02:00', 'au' ,
0,  -.335,  .66688,  .7668,  .419,  0.554, null, 'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, -1, ACOS(.05), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select z, p1, u1, zi1, t1 from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s3')
    
    stmt = """update OPTABLE set u1 = LOG(exp(5.78))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = cast(LOG(exp(5.78)) as integer);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select z, u1, t1 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    
    stmt = """select trim(z), u1,
log(99999.999),
log(0.0000001)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s6')
    
    stmt = """select z, LOG(LOG(n1 + 10000)), log(LOG10(abs(f2)) / ?p * (-1)),
LOG(EXP(n1)), exp(LOG(abs(f3))),
LOG(?p)
from OPTABLE 
where LOG(sqrt(abs(f2))) = (
select LOG(sqrt(abs(f2)))
from OPTABLE 
where f2 > 0.9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, b1, b2, c2 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.c3, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
DEGREES(LOG(abs(vv.f4))) = DEGREES(log(abs(t1.f4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    
    stmt = """select c3, LOG(abs(DEGREES(sinh(RADIANS(b1) * 5E-6)))),
SQRT(abs(LOG(abs(b2))))
from OPTABLE 
union all
select trim(v1.z), v1.psv, LOG(abs(v1.psv))
from voptbl v1
left join voptbl1 vv on
v1.z = vv.z and
LOG(abs(v1.b2)) = log(abs(vv.b2)) and
vv.z > 'Row05'
right join voptbl v2 on
v2.z >= vv.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s10')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test019(desc="""a18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA18
    #  Description:        Tests for SQL, use of LOG10 function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LOG10 function syntax:
    # LOG10{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, LOG10(.00159E+15), LOG10(?p),
LOG10(sinh(radians(580))),
LOG10(1839 * pi() / 180 + 1.009 / ATAN(-30)),
LOG10(9342.764134) / RADIANS(-.66666668),
CASE trim(z)
WHEN 'Row01' THEN LOG10(0.5)
WHEN 'Row02' THEN LOG10(abs(f2))
WHEN 'Row04' THEN LOG10(0.66668)
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN LOG10(TAN(1 - 0.246446))
WHEN 'Row08' THEN LOG10(COS(-0.866825))
ELSE  LOG10(SINH(?p))
END
from OPTABLE 
where LOG10(abs(f1)) is not null and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s0')
    
    stmt = """select z, LOG10(abs(f1 / ATAN(f1) + 100 - 350)),
LOG10(abs(ACOS(f2) * log(ASIN(ABS(-0.707106781186))))),
LOG10(abs(power(ACOS(f2), 13))),
log10(SQRT(abs(f2)))
from OPTABLE 
group by z, f1, f2
having LOG10(abs(f1)) > -1.8
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s1')
    
    stmt = """select z, LOG10(CAST(pi() as largeint)),
LOG10(abs(CAST(ps9 as integer))),
CASE
WHEN LOG10(abs(zi1)) < 0 THEN log(abs(zi1))
WHEN exp(zi1/1000) > 0 THEN LOG10(0.666667)
ELSE LOG10(abs(TANH(pi()) - 1))
END,
LOG10(abs(CEILING(zi1))), FLOOR(log10(abs(DEGREES(zi1)))),
POWER(2, LOG10(abs(zi1)))
from OPTABLE 
where zi1 < 78 and
LOG10(abs(zi1)) > 0 and
z is not null
group by z, zi1, ps9
order by z, 2, 3, 4, 5, 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s2')
    
    stmt = """alter table OPTABLE 
add check (log10(f1) > 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into OPTABLE values (
9.23e8,  1,  3767,  0,  1,  11, date '1916-11-01', 'a'  ,
10, 10, 21366, -1.17e8, 10, 10, time '00:00:00', 'aa' ,
-2418, 6786,  -4761,  log10(21),  10,  -2.64,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.356, 1.99, 99, 9, -2.225E-8, 3.402E8,
1.7976E-3, DEGREES(-0.0000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select z, f1, b2, f3, t1 from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s4')
    
    stmt = """update OPTABLE set f1 = LOG10(TANH(5.998))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, f1, t1 from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s5')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
f1 = LOG10(TANH(5.998));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select z, LOG10(abs(LOG(abs(f2)))), CEILING(LOG10(abs(f2)) * ?p),
log10(abs(LOG10(abs(f2))))
from OPTABLE 
where cos(Log10(abs(f2))) = (
select cos(lOG10(abs(f2)))
from OPTABLE 
where f2 > 0.9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s6')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, f2, b2, psv from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s7')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.psv, vv.t1
from voptbl vv left join OPTABLE t1 on
DEGREES(LOG10(abs(vv.f4))) =
DEGREES(log10(abs(t1.f4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, t1, psv from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s8')
    
    stmt = """select c3, LOG10(abs(sin(RADIANS(b1) / PI()))),
SQRT(abs(LOG10(abs(f2))))
from OPTABLE 
union
select trim(v1.z), v1.psv, LOG10(abs(v1.psv))
from voptbl v1
left join voptbl1 vv1 on
v1.z = vv1.z and
LOg10(cosh(vv1.b2)) = log10(COSH(v1.b2)) and
v1.z > 'Row05'
right join voptbl v2 on
v2.z >= vv1.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a18exp""", 'a18s9')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test020(desc="""a19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA19
    #  Description:        Tests for SQL, use of PI() function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # PI() function syntax:
    # PI()
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, PI() * (.00159E+15) / LOG(?p),
PI() - (asin(radians(30))),
PI() * (1839 * pi() - acos(-30 * PI() / 180)),
PI() / degrees(0.5) * RADIANS(-.66666668),
trim(both ' ' from z) || ' for PI function. ',
CASE trim(z)
WHEN 'Row01' THEN SIN(10) * PI() / 180
WHEN 'Row02' THEN SIN(20) * PI() / 180
WHEN 'Row04' THEN SIN(40) * PI() / 180
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN TAN(1 - 0.246446)
WHEN 'Row08' THEN COS(-0.866825)
ELSE  PI() * SIN(?p) / 180
END
from OPTABLE 
where PI() <> p1 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s0')
    
    stmt = """select z, PI() * (f1) / ATAN(f1),
PI() - (ACOS(f2)) * log10(abs(COS(SIN(-0.707106781186)))),
PI() / (power(ACOS(f2), 13)),
PI() + (SQRT(TANH(.714114))),
EXP(log10(PI()))
from OPTABLE 
group by z, f1, f2, p1
having PI() * p1 > 18
order by z desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s1')
    
    stmt = """select z, CAST(PI() as largeint),
CAST(ps9 * log10(PI()) as double precision),
CASE
WHEN PI() / zi1 < 0 THEN log10(abs(zi1))
WHEN exp(zi1) > 0 THEN PI()
ELSE PI() - (cosh(pi()) - 1)
END,
CEILING(radians(PI())), FLOOR(DEGREES(PI())),
POWER(2, PI())
from OPTABLE 
where zi1 < 78 and
power(PI(), 3) >= b1 and
z is not null
group by z, zi1, ps9
order by z asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s2')
    
    stmt = """insert into OPTABLE values (
9.23e8,  1,  3767,  0,  1,  11, date '1916-11-01', 'a',
10, 10, 21366, -1.17e8, 10, 10, time '00:00:00', 'aa',
-2418, 6786,  -4761,  pi(),  10,  -2.64,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.356, 1.99, 99, 9, -2.225E-8, 3.402E8,
1.7976E-3, DEGREES(-0.0000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s3')
    
    stmt = """update OPTABLE set u1 = PI() + TANH(-0.7078)
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, u1, t1 from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s4')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = cast(PI() + TANH(-0.7078) as largeint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select z, tanh(PI()) * (LOG(n1 / pi())),
DEGREES(CEILING(u1 * pi())),
exp(Pi()) * (EXP(f4)),
power(pI(), 2)
from OPTABLE 
where PI() - (radians(degrees(f2))) = (
select PI() - (RADIANS(DEGREES(f2)))
from OPTABLE 
where f2 > 0.9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s5')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, t1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s6')
    
    stmt = """create view voptbl1 as
select vv.z, vv.c3, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
DEGREES(PI()) = DEGREES(pi());"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, psv from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s7')
    
    stmt = """select c3, PI() * (TANH(b1) / PI() + ?p),
SQRT(PI() ** (TAN(b2) + LOG(27) * 33))
from OPTABLE 
union
select TRIM(t1.z), t1.b2,
PI() - (TAN(t1.b2 + POWER(t1.b2, 2) / 100))
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
sinh(t1.b2 - LOG10(37) * 19 / pi()) =
sinh(vv.b2 - LOG10(37) * 19 / pi())
left join voptbl v on
v.psv * pI() = v.psv / 3.14159265359
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a19exp""", 'a19s8')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test021(desc="""a20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA20
    #  Description:        Tests for SQL, use of SQRT function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SQRT function syntax:
    # SQRT{(<float-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, avg(SQRT(ABS(-.00159E+15))), SQRT(?p),
SQRT(radians(580 * pi() / 180)),
SQRT(1839 * pi()),
SQRT(9342.764134 / sin(0.5) * RADIANS(11.66666668)),
CASE trim(z)
WHEN 'Row01' THEN SQRT(0.5)
WHEN 'Row02' THEN SQRT(0.2)
WHEN 'Row04' THEN SQRT(0.66668)
WHEN 'Row06' THEN radians(-0.7071067)
WHEN 'Row07' THEN SQRT(TAN(1 - 0.246446))
WHEN 'Row08' THEN SQRT(COS(-0.866825))
ELSE  SQRT(ABS(SIN(-?p)))
END
from OPTABLE 
where SQRT(abs(b1)) not in
(1.7976E-3, 1.7976E3, 2.2250E-38) and
d3, z is not null or
sqrt(abs(b1)) between 0.002 and 0.23e+5
group by z, b1
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s0')
    
    stmt = """select z, SQRT(abs(ATAN2(f1, f2))),
SQRT(abs(ACOS(f3))) * exp(log(ABS(-0.707106781186))),
SQRT(power(ACOS(f1), f4)),
exp(SQRT(abs(sinh(f1))))
from OPTABLE 
group by z, f1, f2, f3, f4, p1
having SQRT(p1) > 180
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s1')
    
    stmt = """prepare p from
select z, SQRT(abs(CAST('-9.85e+2' as largeint))),
CASE
WHEN zi1 <= -1 THEN sqrt(zi1 * (-2))
WHEN zi1 > 0 THEN SQRT(zi1)
ELSE SQRT(abs(TANH(pi()) - 1))
END,
max(SQRT(abs(CEILING(radians(zi1))))),
sqrt(abs(FLOOR(DEGREES(zi1)))),
POWER(2, SQRT(abs(zi1)))
from OPTABLE 
where SQRT(abs(zi1)) > 0 and
z is not null
group by z, zi1
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s3')
    
    stmt = """insert into OPTABLE values (
9.23e8,  1,  3767,  0,  1,  11, date '1916-11-01', 'a',
10, 10, 21366, -1.17e8, 10, 10, time '00:00:00', 'aa',
-2418, 6786,  -4761,  sqrt(pi()),  10,  -2.64,
interval '00:00:00' hour to second, 'aaa', 'Row09',
0.356, 1.99, 99, 9, -2.225E-8, 3.402E8,
1.7976E-3, DEGREES(-0.0000)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s4')
    
    stmt = """update OPTABLE set u1 = SQRT(TANH(1))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s5')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
u1 = cast(SQRT(TANH(1)) as smallint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select trim(z),
sqrt(99999999999999999.999999999),
sqrt(0.0000000000000000000000001),
sqrt(0)
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s6')
    
    stmt = """select z, SQRT(abs(LOG(n1 * PI()))),
DEGREES(sqrt(abs(LOG10(abs(f4) * ?p)))),
SQRT(sQRt(abs(p1))),
SQRT(?p)
from OPTABLE 
where SQRT(Sqrt(abs(asin(radians(f2))))) = (
select sQRT(SQRT(abs(asin(RADIANS(f2)))))
from OPTABLE 
where f2 > 0.9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s7')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, c3, t1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.t1, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
DEGREES(SQRT(abs(vv.f4))) =
DEGREES(sqrt(abs(t1.f4)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, t1, psv from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s9')
    
    stmt = """select c3, SQRT(abs(DEGREES(cosh(RADIANS(b1))))),
SQRT(SQRT(abs(b2 / abs(-2))))
from OPTABLE 
union all
select trim(v1.z), v1.psv, SQRT(v1.psv + 10)
from voptbl v1
left join voptbl1 vv on
v1.z = vv.z and
SQRT(power(v1.b2, 2)) =
sqrt(power(vv.b2, 2)) and
v1.z > 'Row05'
right join voptbl v2 on
v2.z >= vv.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a20exp""", 'a20s10')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test022(desc="""a21"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA21
    #  Description:        Tests for SQL, use of POWER function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # POWER function syntax:
    # POWER{(<float-exp1>, <float-exp2>)}
    
    # Create LOG file
    
    stmt = """set param ?p  3.4;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, max(POWER(ceiling(psc), floor(p9c))),
power(avg(power(zi3, 4)), 0.5 * 4),
SQRT(abs(POWER(f4, ?p1))),
CEILING(power(0, 99999999999999999999)),
POWER(ACOS(f2), 2), power(TANH(f4), 3)
from OPTABLE 
where POWER(f3, 0) < PI() and
POWER(f3, 2) < 3.14159
group by z, psc, f4, f2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s0')
    
    stmt = """select z, psv, FLOOR(POWER(POWER(psv, 2), 2)),
FLOOR(EXP(POWER(psv, 3))),
POWER(ceiling(ABS(f4)), 2),
RADIANS(power(f5, 1))
from OPTABLE 
where t3 is null and
c2 is not null
group by z, f5, f4, psv
having POWER(f4, 0) > 0
order by 1 asc, 2 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s1')
    
    stmt = """select z, POWER(LOG10(?p), ?p1) + PI() / SIN(145 * PI() / 180),
POWER(COS(f5), 2),
POWER(COSH(f4), 1)
from OPTABLE 
where POWER(DEGREES(f3), 0) =
(select POWER(DEGREES(f3), 0)
from OPTABLE 
where RADIANS(f5) > 0.01);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s2')
    
    stmt = """select z, POWER(TAN(?p), 2), power(CAST('3.14' as float), 10),
CASE POWER(0.5, 2)
when 1.5 then 1.5 * PI() / 180
when 0.5 then 0.5 * PI() / 180
when .25 then .25 * PI() / 180
else POWER(.5, 3)
END,
POWER(8.1 / 99.37 * 100000, LOG10(500000.999999)),
POWER(d2, 200E-2),
POWER(d2, 0) + 8.203E-2 * ATAN2(u3, ATAN(zi3)),
POWER(u3, ceiling(ATAN(zi3)))
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s3')
    
    stmt = """select z, POWER(TAN(?p), 2),
POWER(ASIN(CAST('.14' as float)), 4),
POWER(d2, 10), ATAN2(-1 / 2, 5),
TANH(COS(f3)) * POWER(SINH(d2), ceiling(f1)),
POWER(SINH(d2), floor(f1))
from OPTABLE 
where Power(d2, 3) > 3 and
d2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s4')
    
    stmt = """alter table OPTABLE 
add check (power(f1, 2) <> 0.25);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into OPTABLE values(
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, POWER(0.2, 8), -5342, 4, null, ASIN(.5), 76.373, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select cast(z as char(10)), power(sqrt(p1), 2), sqrt((u1 ** 2))
from OPTABLE 
group by z, p1, u1
having z in (values ('Row09'));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s4a')
    
    stmt = """update OPTABLE set f4 = POWER(.05, ?p1)
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select trim(z), POWER(avg(COS(f1)), floor(AVG(f4))),
CASE
WHEN power(zi1, 2) < 0 THEN powER(zi1, 2)
WHEN pOWer(zi1, 2) > 0 THEN zi1 ** zi1
ELSE Power(999, 2)
END,
POWER(AVG(psc) / 180, -3), f4
from OPTABLE 
where TRIM(z) > 'Row07' and
POWER(f4, -2) * 100 > 180
group by z, zi1, f1, f4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s5')
    
    stmt = """delete from OPTABLE 
where rtrim(LTRIM(z)) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select z, f4, t1 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s6')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, psv, c3, t1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s7')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.f4, vv.psv
from voptbl vv left join OPTABLE t1 on
power(vv.f4, -30) = POWER(t1.f4, -30) and
POWER(SIN(vv.f5), -9) = POWER(SIN(t1.f5), -9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, f4, psv from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s8')
    
    stmt = """select z, POWER(TANH(b1) / PI() + ?p1, 1),
SQRT(power(33, SIN(f3)))
from OPTABLE 
union
select TRIM(t1.z), t1.b2,
POWER(t1.b2 + POWER(t1.b2, 2) / 100, ceiling(2.447e-2))
from OPTABLE t1
inner join voptbl1 vv on
t1.z = vv.z and
POWER(t1.b2 - LOG10(37) * 19, 5) =
POWER(vv.b2 - LOG10(37) * 19, 5)
left join voptbl v1 on
POWER(PI() / v1.psv,
ceiling(abs(vv.b1 * -1.17E-23))) =
POWER(3.14159265359 / v1.psv,
ceiling(abs(vv.b1 * -1.17E-23)))
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a21exp""", 'a21s9')
    
    # Added following query for testing.
    stmt = """select z, power(-1, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 9)
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test023(desc="""a22"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA22
    #  Description:        Tests for SQL, use of <numeric-exp> **
    #			<integer-exp> function in the select list.
    #                      This is a positive test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # Create LOG file
    
    stmt = """set param ?p  3.4;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, ceiling(psc) ** floor(p9c),
(zi1 ** 4) ** floor(f5),
power(SQRT(abs(f4 ** ?p1)), CEILING(.15 ** 9)),
ACOS(f2) ** 2, ATAN2(TANH(f4), 3)
from OPTABLE 
where abs(f3) ** (f2) < PI() and
f3 ** 3 > -1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s0')
    
    stmt = """select z, FlOOR((psv ** 2) ** 2),
FLooR(EXp(psv ** 3)),
Ceiling(ABS(f4) ** 2),
Radians(f5 ** 1)
from OPTABLE 
where t3 is null and
c2 is not null
group by z, f4, f5, psv
having f4 ** 0 >= 0
order by z desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s1')
    
    stmt = """prepare p from
select z, LOG10(?p) ** ?p1 + PI() / SIN(145),
0 ** COS(f5),
COSH(f4) ** 15
from OPTABLE 
where f3 ** 0 =
(select f3 ** 0
from OPTABLE 
where RADIANS(f5) between 5.9e-10 and 1.4e-2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """select seq_num, operator, total_cost
from table (explain (null, 'P'));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute p;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s3')
    
    stmt = """select z, sinh(TAN(?p)) ** 2, CAST('3.14' as float) ** 10,
CASE 0.5 ** 2
when 1.5 then 1.5 * PI() / 180
when 0.5 then 0.5 * PI() / 180
when .25 then .25 * PI() / 180
else .2 ** 3
END,
(8.1 / 99.37 * 100000) ** (LOG10(420.999)),
COS(f2) ** 200E-2,
COSH(d2) ** (-2) + 8.203E-2 * ATAN2(u3, ATAN(zi3)),
u3 ** ceiling(ATAN(zi3))
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s4')
    
    stmt = """select z, acos(TAN(?p)) ** 5,
ASIN(CAST('-.827' as float) ** 4),
d2 ** 10,
COS(COS(f3)) * (SINH(d2) ** TANH(f1)),
sqrt(abs(SINH(d2) ** floor(f1)))
from OPTABLE 
where d2 ** 3 between -0.03 and 1.22e+23  and
d2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s5')
    
    stmt = """insert into OPTABLE values(
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, 0.2 ** 8, -5342, 4, null, ASIN(.5) ** 3, 76.373, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set f4 = .05 ** ?p1
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select trim(z), AVG(f1) ** floor(AVG(f4)),
CASE
WHEN zi1 ** 2 < 0 THEN power(zi1, 2)
WHEN zi1 ** 2 > 0 THEN zi1 ** zi1
ELSE 999 ** 2
END,
AVG(psc) / 180 ** -3, f1, f4, zi1
from OPTABLE 
where TRIM(z) > 'Row07' and
f4 ** (-2) * 100 > 180
group by z, f1, f4, zi1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s6')
    
    stmt = """delete from OPTABLE 
where f4 <> (.05 ** 5) * 0.05 and
rtrim(LTRIM(z)) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select z, f4 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s7')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.f4, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
vv.f4 ** -10 = t1.f4 ** -10 and
SIN(vv.f5) ** (-9) = SIN(t1.f5) ** -9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, f4 from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s9')
    
    stmt = """select c3, power(TANH(b1), 2)  ** ?p, SQRT(ABS(ps9 / 100) ** ?p)
from OPTABLE 
union all
select v1.z, v1.b2, v1.b2 ** -1
from voptbl v1
left join voptbl1 vv1 on
v1.z = vv1.z and
degrees(v1.b2) ** floor(PI()) =
degrees(vv1.b2) ** floor(PI())
right join voptbl v2 on
v2.z >= vv1.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a22exp""", 'a22s10')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  -------------------------------
    #   Close the Log file
    #  ---------------------------------
    
    _testmgr.testcase_end(desc)

def test024(desc="""a23"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA23
    #  Description:        Tests for SQL, use of RAND function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RAND function syntax:
    # RAND{(<integer-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p  3.4;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, RAND(159), rand(?p1),
floor(rand(1839) * pi() / 180 + 1009 / TANH(-30)),
RAND(9342) / degrees(0.5) * RADIANS(-.66666668),
CASE trim(z)
WHEN 'Row01' THEN RAND(100)
WHEN 'Row02' THEN RAND(0)
WHEN 'Row04' THEN RAND(400)
WHEN 'Row06' THEN rand()
WHEN 'Row07' THEN floor(TAN(1 - 0.246446))
WHEN 'Row08' THEN RAND(9)
ELSE  RAND()
END
from OPTABLE 
where p1 < 15000 and
RAND(p1) > 999999 and
d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select f1, SIGN(RAND(abs(p2)) / ATAN(f1) + 100 - 350),
ceiling(rand(13) ** acos(f3)),
SQRT(rand(4)),
rand(000)
from OPTABLE 
group by f1, f3, p2
having p2 < 15000
order by f1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select z,
CAST(rand(abs(p2)) as float),
CASE
WHEN RAND(u1) < 0 THEN
rand(0000000)
WHEN rand(u1) > 0 THEN
RAND(555)
ELSE RAND(123456789)
END,
FLOOr(CeILING(DEGREES(Rand(abs(zi1)))))
from OPTABLE 
where power(RAND(1), 1) > 0 and
z is null
group by z, p2, u1, zi1
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """insert into OPTABLE values(
10,  10,  10,  10,  10,  10, date '1360-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  rand(30),  30,  30, null, 'acc', 'Row09',
-9.9, 0.2 ** 8, -5342, 4, null, ASIN(.5) ** 3, 76.373, null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select z, u1, f3  from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """select trim(z),
rand(999999999),
rand(01),
rand() - rand(), rand() + rand(),
rand() / rand(), rand() * rand()
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a23exp""", 'a23s5')
    
    # Function is rand() currently is not supported
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.psc, vv.u2
from voptbl vv left join OPTABLE t1 on
DEGREES(RAND(abs(vv.zi1))) = DEGREES(rand(abs(t1.zi1)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select z, psc from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """select c3, SQRT(RAND(u2)),
rand(rand(u2))
from OPTABLE 
union all
select v1.z, RAND(v1.u2), v1.u2
from voptbl v1
left join voptbl1 vv1 on
v1.z = vv1.z and
RAND(v1.u2) = rand(vv1.u2) and
rtrim(ltrim(vv1.z)) > 'Row05'
right join voptbl v2 on
v2.z >= vv1.z
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test025(desc="""a24"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA24
    #  Description:        Tests for SQL, use of SIGN function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SIGN function syntax:
    # SIGN{(<integer-exp>)}
    
    # Create LOG file
    
    stmt = """set param ?p  3.4;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, SIGN(-.00159E+15), sign(rand(?p1)),
SIGN(degrees(580 * pi() / 180)),
SIGN(floor(1839 * pi() / TANH(-30))),
SIGN(-9342.764134e23) / degrees(0.5) * RADIANS(-.66666668),
CASE trim(z)
WHEN 'Row01' THEN SIGN(100)
WHEN 'Row02' THEN SIGN(-200)
WHEN 'Row04' THEN SIGN(400)
WHEN 'Row06' THEN sign(radians(-0.7071067))
WHEN 'Row07' THEN SIGN(floor(TAN(1 - 0.246446)))
WHEN 'Row08' THEN SIGN(COS(-0.866825) * 239)
ELSE  SIGN(?p1)
END
from OPTABLE 
where SIGN(p1), d3, z is not null
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select z, SIGN(SIGN(p1) / ATAN(f1) + 100 - 350),
SIGN(floor(ACOS(f2)) * exp(COS(SIN(ABS(-0.707106781186))))),
SIGN(ceiling(power(ACOS(f3), 13))),
rand(sign(SQRT(4))),
char(sign(000))
from OPTABLE 
group by z, u1, f1, f2, f3, p1
having SIGN(p1) = 0
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select z, SIGN(CAST(9 ** ?p as largeint)),
CASE
WHEN SIgN(u1) < 0 THEN rand(u1)
WHEN sIGn(u1) > 0 THEN sIGN(-0.666667e17)
ELSE Sign(-9999999e24)
END,
SIGN(CEILING(radians(zi1))),
sign(FLOOR(CEILING(DEGREES(zi1)))),
POWER(2, SIGN(u3))
from OPTABLE 
where SIGN(1) > 0 and
z is null
group by z, zi1, u1, u3
order by z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """alter table OPTABLE 
add check (sign(f1) = 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into OPTABLE values(
1,  0,  100,  sign(-.5275),  10,  10, date '0060-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, ACOS(0.022E-3), -5342, 4, null, ACOS(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select z, f1, t1 from OPTABLE 
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s4')
    
    stmt = """update OPTABLE set p1 = SIGN(TANH(-0.7078))
where trim(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select z, p1, t1 from OPTABLE 
where trim(z) > 'Row08';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s5')
    
    stmt = """delete from OPTABLE 
where trim(z) = 'Row09' and
p1 = SIGN(TANH(-0.7078));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select trim(z),
sign(99999999999999999.99999999999999999999),
sign(-99999999999999999.99999999999999999999),
sign(0.000000000000000000001),
sign(-0.0000000000000000000000000000001),
sign(cast(z as integer))
from OPTABLE 
where z is null
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s6')
    
    stmt = """select z, SIGN(floor(LOG(n1 + 10000))),
DEGREES(CEILING(p1 * ?p)),
SIGN(ceiling(EXP(f1))),
SIGN(floor(?p))
from OPTABLE 
where SQRT(SIGN(ceiling(radians(degrees(f2))))) = (
select SQRT(SIGN(ceiling(RADIANS(DEGREES(f2)))))
from OPTABLE 
where f2 between -.2 and -.111)
order by z desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s7')
    
    stmt = """create view voptbl as
select *
from OPTABLE 
where trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, t1 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s8')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
DEGReeS(SIgN(vv.zi1)) = DEGREES(sign(t1.zi1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, b1, b2, psv from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s9')
    
    stmt = """select c3, SIGn(floOr(DEGREES(taNH(raDIANS(b1) * 5E-6)))),
sign(sign(u2))
from OPTABLE 
union all
select v1.z, v1.psv, SIGN(v1.psc)
from voptbl v1
left join voptbl1 vv1 on
v1.z = vv1.z and
SIGN(ceiling(v1.b2)) =
sign(ceiling(vv1.b2)) and
rtrim(ltrim(vv1.z)) > 'Row03'
right join voptbl v2 on
v2.z = vv1.z
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a24exp""", 'a24s10')
    
    # -------------------------------
    # Clearn up section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test026(desc="""a26"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testA26
    #  Description:        Tests for SQL, use of MOD function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # MOD function syntax:
    # MOD{(<integer-exp1>, <integer-exp2>)}
    
    # Create LOG file
    
    stmt = """set param ?p  3.4;"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?p1 5;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z,
max(MOD(cast(ceiling(psc) as integer),
cast(3.5 as integer))),
mod(cast(min(floor(p9c)) as largeint), 2),
mod(cast(floor(avg(mod(zi3, 4))) as integer), 4),
SQRT(MOD(cast(atan(p1) as int), ?p1)),
CEILING(power(0, 99999999999999999999)),
MOD(p2, 2), ATAN2(TANH(f4), 3)
from OPTABLE 
where MOD(p3, 330) < PI()
group by z, psc, p9c, zi3, p1, p2, f4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s0')
    
    stmt = """select z, zi2, FLOOR(power(mod(ps9, 2), 2)),
FLOOR(EXP(MOD(psc, 3))),
max(ceiling(MOD(ABS(u2), 2)))
from OPTABLE 
where t3 is null and
c2 is not null
group by z, zi2, f4, f5, ps9, psc
having MOD(zi2, 11990) > 0
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s1')
    
    stmt = """select z,
LOG10(mod(cast(?p1 as smallint),
cast(FLOOR(psv * 100) as largeint))),
MOD(300, ?p),
MOD(cast(ceiling(COSH(f4)) as int), 1)
from OPTABLE 
where MOD(cast(ceiling(f3) as smallint), 10) =
(select MOD(cast(ceiling(f3) as smallint), 10)
from OPTABLE 
where RADIANS(f5) > 0.003) order  by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s2')
    
    stmt = """select MOD(MOD(cast(TAN(?p1) * 2e+5 as integer), 2), 2),
power(CAST('3.14' as float), 10),
CASE MOD(10, 2)
when 1.5 then 1.5 * PI() / 180
when 5   then 5 * PI() / 180
when .25 then .25 * PI() / 180
else MOD(5, 3)
END,
MOD(8, cast(LOG10(500000.999999) * 5e+7 as largeint)),
MOD(u3, cast(ceiling(ATAN(zi3)) as largeint))
from OPTABLE 
where Power(d2, 3) > 3000 and
d2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s3')
    
    stmt = """alter table OPTABLE 
add check (p1 <> mod(90, 2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into OPTABLE values(
10,  10,  10,  10,  10,  10, date '1960-01-01',  'a'  ,
30,  30,  30,  30,  30,  30, time '00:02:00', 'ac' ,
30,  30,  30,  30,  30,  30, null, 'acc', 'Row09',
-9.9, MOD(2, cast(?p1 as integer)), -5342, 4, null,
ASIN(.5), 76.373, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """update OPTABLE set p1 = MOD(5, cast(?p1 as integer))
where TRIM(z) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select trim(z),
CASE
WHEN Mod(zi1, 2) < 0 THEN mOd(zi1, 2)
WHEN mOD(zi1, 2) > 0 THEN mod(zi1, zi1)
ELSE MoD(999, 2)
END
from OPTABLE 
where TRIM(z) > 'Row07' and
MOD(1, -2) * 100 < 180;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s5')
    
    stmt = """delete from OPTABLE 
where p1 = MOD(5, 5) and
rtrim(LTRIM(z)) = 'Row09';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """select count(*)
from OPTABLE 
where z > 'Row04';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s6')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where	trim(z) > 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select z, f4, f5 from voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s7')
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.psv
from voptbl vv left join OPTABLE t1 on
power(vv.f4, -5) = POWER(t1.f4, -5) and
ceiling(SIN(vv.f5)) =
ceiling(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*) from voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s8')
    
    stmt = """select t.c3, MOD(cast(TANH(t.b1) / PI() + ?p1 as largeint), 1)
from OPTABLE t
union
select TRIM(t1.z),
MOD(cast(t1.b2 + POWER(t1.b2, 2) * 100 as integer),
cast(ceiling(2.447e-2) as smallint))
from OPTABLE t1
inner join voptbl1 vv1 on
t1.z = vv1.z and
MOD(cast(COSH(t1.b2 - LOG10(37)) as integer), 5) =
MOD(cast(COSH(vv1.b2 - LOG10(37)) as integer), 5)
left join voptbl v1 on
MOD(cast(PI() / vv1.psv * 1.2e+5 as largeint),
cast(ceiling(abs(vv1.b1 * -1.17E-23)) as largeint)) =
MOD(cast(3.14159265359 / v1.psv * 1.2e+5 as largeint),
cast(ceiling(abs(v1.d1 * -1.17E-23)) as largeint))
order by c3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a26exp""", 'a26s9')
    
    # -------------------------------
    # Cleanup section
    # -------------------------------
    
    stmt = """DROP VIEW  voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """DROP VIEW  voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test027(desc="""n01.temp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN01
    #  Description:        Tests for SQL, use of ACOS function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ACOS function syntax:
    # ACOS{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select ACOS() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ACOS, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select Acos(( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select acos)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select acos(()) fromoptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  float-exp used more than once
    
    stmt = """select ACOS(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ACOS(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled ACOS
    
    # error different in SQ and NSK
    stmt = """select ACPS(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misspelled table name
    
    stmt = """select ACOS(.05) from optaleb;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  Misplaced ACOS
    
    stmt = """select f4
from OPTABLE 
group by ACOS(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by ACOS(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  ACOS used twice
    
    stmt = """select ACOS ACOS(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select ACOSACOS(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select ACOS(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ACOS(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ACOS(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ACOS(t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ACOS('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ACOS(-1.000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select ACOS(-1.00000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01.tempexp""", 'n01.temps19')
    
    stmt = """select ACOS(-1.00000000000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01.tempexp""", 'n01.temps20')
    
    stmt = """select ACOS(-1.0000000000000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n01.tempexp""", 'n01.temps21')
    
    stmt = """select ACOS(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select ACOS(-3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select ACOS(3.4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select acos(1.1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select acos(-1.1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    #  float-exp is null
    
    stmt = """select ACOS(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid caculation for float-exp
    
    stmt = """select ACOS(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ACOS(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select ACOS(.1 + null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    # error different in SQ and NSK
    stmt = """select acospi() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # Added following four queries for testing division by a 0.
    stmt = """select 5 / 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select f2 / 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select t2 / 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select z / 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    _testmgr.testcase_end(desc)

def test028(desc="""n02.temp"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN02
    #  Description:        Tests for SQL, use of ASIN function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ASIN function syntax:
    # ASIN{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select ASIN() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASIN, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select Asin(( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select asin)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select asin(()) fromoptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  float-exp used more than once
    
    stmt = """select ASIN(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASIN(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled ASIN
    # error different in SQ and NSK
    stmt = """select ASIM(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced ASIN
    
    stmt = """select f4
from OPTABLE 
group by ASIN(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by ASIN(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  ASIN used twice
    
    stmt = """select ASIN ASIN(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select ASINASIN(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select ASIN(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ASIN(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASIN(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ASIN(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ASIN('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ASIN(-1.0000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select Asin(-1.00000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02.tempexp""", 'n02.temps18')
    
    stmt = """select Asin(-1.00000000000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02.tempexp""", 'n02.temps19')
    
    stmt = """select Asin(-1.0000000000000000000000001) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n02.tempexp""", 'n02.temps20')
    
    stmt = """select ASIN(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select ASIN(-3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select ASIN(3.4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    #  Invalid caculation for float-exp
    
    stmt = """select ASIN(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ASIN(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select asin(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select ASIN(.1 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select asin 30 * pi() / 180 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  This query hangs when subquery returns more than one row.
    
    stmt = """select f2 from OPTABLE 
where ASIN(DEGREeS(f3) * 10e-3) =
(select ASIN(DEGREeS(f3) * 10e-3)
from OPTABLE 
where RADIANS(f5) < 180);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    _testmgr.testcase_end(desc)

def test029(desc="""n03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN03
    #  Description:        Tests for SQL, use of ATAN function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ATAN function syntax:
    # ATAN{(<float-exp>)}
    
    #  float-exp not used
    
    stmt = """select ATAN() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select Atan(( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select atan)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select atan(()) fromoptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  float-exp used more than once
    
    stmt = """select ATAN(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled ATAN
    # error different in SQ and NSK
    stmt = """select ARAS(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced ATAN
    
    stmt = """select f4
from OPTABLE 
group by ATAN(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by ATAN(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  ATAN used twice
    
    stmt = """select ATAN ATAN(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select ATANATAN(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select ATAN(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ATAN(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ATAN(t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ATAN('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select ATAN(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n03exp""", 'n03s17')
    
    #  Invalid caculation for float-exp
    
    stmt = """select ATAN(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select atan(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select ATAN(null + 0.002) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test030(desc="""n04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN04
    #  Description:        Tests for SQL, use of COS function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # COS function syntax:
    # COS{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select COS() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COS, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select Cos(( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select cos)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select cos(()) fromoptable;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  float-exp used more than once
    
    stmt = """select COS(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COS(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled COS
    # error different in SQ and NSK
    stmt = """select COOS(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced COS
    
    stmt = """select f4
from OPTABLE 
group by COS(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by COS(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  COS used twice
    
    stmt = """select COS COS(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select COSCOS(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select COS(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select COS(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COS(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select COS(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select COS('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select cos(263) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n04exp""", 'n04s17')
    
    stmt = """select cos(265) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n04exp""", 'n04s18')
    
    stmt = """select cos(-263) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n04exp""", 'n04s19')
    
    stmt = """select cos(-264) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n04exp""", 'n04s20')
    
    stmt = """select COS(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n04exp""", 'n04s21')
    
    #  Invalid caculation for float-exp
    
    stmt = """select COS(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COS(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select cos(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select COS($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test031(desc="""n05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN05
    #  Description:        Tests for SQL, use of COSH function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # COSH function syntax:
    # COSH{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select COSH() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COSH, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  float-exp used more than once
    
    stmt = """select COSH(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COSH(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled COSH
    
    # error different in SQ and NSK
    stmt = """select COSJ(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced COSH
    
    stmt = """select f4
from OPTABLE 
group by COSH(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by COSH(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  COSH used twice
    
    stmt = """select COSH COS(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select COSHCOSH(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select COSH(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select COSH(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COSH(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select COSH(t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select COSH('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select COSH(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select COSH(778) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select COSH(711) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select COSH(-711) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select COSH(-720) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    #  Invalid caculation for float-exp
    
    stmt = """select COSH(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select COSH(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select cosh(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select COSH($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test032(desc="""n06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN06
    #  Description:        Tests for SQL, use of SIN function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SIN function syntax:
    # SIN{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select SIN() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIN, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  float-exp used more than once
    
    stmt = """select SIN(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIN(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled SIN
    
    # error different in SQ and NSK
    stmt = """select SSIN(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced SIN
    
    stmt = """select f4
from OPTABLE 
group by SIN(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by SIN(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SIN used twice
    
    stmt = """select SIN SIN(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select SINSIN(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select SIN(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SIN(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIN(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SIN(t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SIN('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select sin(263) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s14')
    
    stmt = """select sin(264) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s15')
    
    stmt = """select sin(-263) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s16')
    
    stmt = """select sin(-266) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s17')
    
    stmt = """select SIN(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n06exp""", 'n06s18')
    
    #  Invalid caculation for float-exp
    
    stmt = """select SIN(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIN(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select sin(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select SIN($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test033(desc="""n07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN08
    #  Description:        Tests for SQL, use of SINH function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SINH function syntax:
    # SINH{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select SINH() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SINH, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  float-exp used more than once
    
    stmt = """select SINH(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SINH(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled SINH
    
    # error different in SQ and NSK
    stmt = """select COSJ(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced SINH
    
    stmt = """select f4
from OPTABLE 
group by SINH(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by SINH(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  SINH used twice
    
    stmt = """select SINH SINH(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select SINHSINH(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select SINH(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SINH(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SINH(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SINH(t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SINH('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SINH(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select SINH(711) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select SINH(7129) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    #$err_msg 8428 "SINH"
    stmt = """select SINH(-711) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s14c')
    
    #$err_msg 8428 "SINH"
    stmt = """select SINH(-712) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n07exp""", 'n07s14d')
    
    #  Invalid caculation for float-exp
    
    stmt = """select SINH(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SINH(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select sinh(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select SINH($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test034(desc="""n08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN08
    #  Description:        Tests for SQL, use of TAN function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # TAN function syntax:
    # TAN{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select TAN() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TAN, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  float-exp used more than once
    
    stmt = """select TAN(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TAN(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled TAN
    
    # error different in SQ and NSK
    stmt = """select STAN(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced TAN
    
    stmt = """select f4
from OPTABLE 
group by TAN(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by TAN(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  TAN used twice
    
    stmt = """select TAN TAN(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select TANTAN(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select TAN(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select TAN(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TAN(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select TAN(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select TAN('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select tan(263) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s14')
    
    stmt = """select tan(264) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s15')
    
    # Changed from -273 to -263, which is the minimum limit for TAN.
    stmt = """select tan(-263) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s16')
    
    stmt = """select tan(-269) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s17')
    
    stmt = """select TAN(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s18')
    
    #  Invalid caculation for float-exp
    
    stmt = """select TAN(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TAN(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select tan(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select TAN($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # Added this query for testing.
    stmt = """select tan(-262.999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n08exp""", 'n08s23')
    
    _testmgr.testcase_end(desc)

def test035(desc="""n09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN09
    #  Description:        Tests for SQL, use of TANH function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # TANH function syntax:
    # TANH{(<float-exp>)}
    
    # Create LOG file
    
    #  float-exp not used
    
    stmt = """select TANH() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TANH, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  float-exp used more than once
    
    stmt = """select TANH(f4, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TANH(f5 f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled TANH
    
    # error different in SQ and NSK
    stmt = """select TANG(b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced TANH
    
    stmt = """select f4
from OPTABLE 
group by TANH(f4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by TANH(f5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  TANH used twice
    
    stmt = """select TANH TANH(f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select TANHTANH(f5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp
    
    stmt = """select TANH(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select TANH(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')

    stmt = """select TANH(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select TANH(t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select TANH('abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select TANH(999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n09exp""", 'n09s14')
    
    stmt = """select tanh(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid caculation for float-exp
    
    stmt = """select TANH(0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select TANH(.1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select TANH($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """create view voptbl as
select * from OPTABLE 
where trim(z) < 'Row05';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view voptbl1 as
select vv.z, vv.b1, vv.b2, vv.c1
from voptbl vv left join OPTABLE t1 on
TANH(vv.f4) = TANH(t1.f4) and
TANH(SIN(vv.f5)) = TANH(SIN(t1.f5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select v1.z, v1.c3, v1.b2, SUM(TANH(v1.b2))
from voptbl v1
right join voptbl1 v2 on
v1.z = v2.z;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4021')
    
    stmt = """drop view voptbl1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop view voptbl;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test036(desc="""n10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN10
    #  Description:        Tests for SQL, use of ATAN2 function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ATAN2 function syntax:
    # ATAN2{(<float-exp1>, <float-exp2>)}
    
    # Create LOG file
    
    #  float-exp1, float-exp2, or both not used
    
    stmt = """select atan2(f1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(f1, ) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(), z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  float-exp1, or float-exp2 used more than once
    
    stmt = """select ATAN2(f4 f1, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(f4, b1 b2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(f5, f4, b1, b2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(psv p9c, psc, f3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled ATAN2
    
    # error different in SQ and NSK
    stmt = """select ATAN3(b1, b2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select ATAN1(b1, b1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced ATAN2
    
    stmt = """select f4
from OPTABLE 
group by ATAN2(f4, 9999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by ATAN2(f5, -99999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  ATAN2 used twice
    
    stmt = """select ATAN2 ATAN2(f4, pi()) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select ATAN2ATAN2(f5, ABS(-1234556)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid float-exp1
    
    stmt = """select ATAN2(a, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ATAN2(%, 1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(z, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select ATAN2(t3, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select ATAN2('abcdefg', 3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select ATAN2(999999999999999999999999999999, -44) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n10exp""", 'n10s20')
    
    stmt = """select ATAN2(t1, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select ATAN2(1.23.34, .3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2('01/09/1903', 988) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select atan2(null, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid float-exp2
    
    stmt = """select ATAN2(0, a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select ATAN2(.01, %) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(-.987654321, z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select ATAN2(-1.0, t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select ATAN2(pi(), 'abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select ATAN2(-1292343, c3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select ATAN2(999, 1.23.34) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(988, '01/09/1903') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select ATAN2(9, 99999999999999999999999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n10exp""", 'n10s33')
    
    stmt = """select ATAN2(2, '07/31/1998 12:00:39.1234') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select atan2(2, null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid caculation for float-exp1, float-exp2, or both
    
    stmt = """select ATAN2(0.5 * #, 1234567890) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(.1 / z, 0987676554342) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select ATAN2($ / null, -1.22) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(1234567890, 0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(09876564, .1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select ATAN2(-1.22, $ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(1234567890 - null, 0.5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(09876564 + null, .1 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select ATAN2(-1.22 * null, $ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select ATAN2(t1, t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    _testmgr.testcase_end(desc)

def test037(desc="""n11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN11
    #  Description:        Tests for SQL, use of DEGREES function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # DEGRESS function syntax:
    # DEGRESS{(<numeric-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select DEGREES() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select DEGREES from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select DEGREES( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    # error different in SQ and NSK
    stmt = """select DEGRESS(f1, psc) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select DEGREES(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select DEGREES(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled DEGREES
    
    # error different in SQ and NSK
    stmt = """select DEGRESS(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misspelled table name
    
    stmt = """select DEGREES(p1) from opreble;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    #  DEGREES typed in more than once
    
    stmt = """select DEGREES DEGREES(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select DEGREESDEGREES(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select DEGREES(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select DEGREES(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select DEGREES(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select DEGREES('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select DEGREES(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select DEGREES(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select DEGREES('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select DEGREES(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select DEGREES(9999999999999999999999999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n11exp""", 'n11s18')
    
    stmt = """select degrees(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select degrees(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select degrees(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test038(desc="""n12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN12
    #  Description:        Tests for SQL, use of RADIANS function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RADIANS function syntax:
    # RADIANS{(<numeric-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select RADIANS() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RADIANS from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RADIANS( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select RADIANS(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RADIANS(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RADIANS(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled RADIANS
    
    # error different in SQ and NSK
    stmt = """select RAIDIANS(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  RADIANS typed in more than once
    
    stmt = """select RADIANS RADIANS(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select RADIANSRADIANS(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select RADIANS(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RADIANS(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select RADIANS(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select RADIANS('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select RADIANS(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RADIANS(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RADIANS('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select RADIANS(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RADIANS(9999999999999999999999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n12exp""", 'n12s17')
    
    stmt = """select radians(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select radians(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select radians(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test039(desc="""n13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN13
    #  Description:        Tests for SQL, use of ABS() function
    #                      in the select list.  This is a positive
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # ABS function syntax:
    # ABS{(<numeric-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select abs() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select abs from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select abs( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select abs(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select abs(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select abs(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled abs
    
    # error different in SQ and NSK
    stmt = """select AVS(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  abs typed in more than once
    
    stmt = """select abs ABS(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select absABS(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select abs(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select abs(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select abs(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select abs('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select abs(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select abs(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select abs('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select abs(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select abs(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select abs(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select abs(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test040(desc="""n14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN14
    #  Description:        Tests for SQL, use of CEILING function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # CEILING function syntax:
    # CEILING{(<numeric-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select CEILING() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CEILING from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select CEILING( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select CEILING(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CEILING(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CEILING(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled CEILING
    
    # error different in SQ and NSK
    stmt = """select ceiiling(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  CEILING typed in more than once
    
    stmt = """select CEILING ceiling(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select CEILINGceiling(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select CEILING(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select CEILING(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CEILING(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CEILING('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CEILING(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CEILING(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select CEILING('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select CEILING(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select CEILING(9999999999999999999999999999999999999.999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n14exp""", 'n14s17')
    
    stmt = """select ceiling(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select ceiling(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select ceiling(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test041(desc="""n15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN15
    #  Description:        Tests for SQL, use of FLOOR function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # FLOOR function syntax:
    # FLOOR{(<numeric-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select FLOOR() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select FLOOR from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select FLOOR( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select FLOOR(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select FLOOR(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select FLOOR(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled FLOOR
    
    # error different in SQ and NSK
    stmt = """select flooor(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  FLOOR typed in more than once
    
    stmt = """select FLOOR floor(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select FLOORfloor(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select FLOOR(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select FLOOR(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select FLOOR(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select FLOOR('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select FLOOR(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select FLOOR(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select FLOOR('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select FLOOR(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select FLOOR(-99999999999999999999999999999999999.999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n15exp""", 'n15s17')
    
    stmt = """select floor(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select floor(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select floor(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test042(desc="""n16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN16
    #  Description:        Tests for SQL, use of EXP function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # EXP function syntax:
    # EXP{(<float-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select EXP() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select EXP from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select EXP( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select EXP(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select EXP(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select EXP(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled EXP
    
    # error different in SQ and NSK
    stmt = """select exxp(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  EXP typed in more than once
    
    stmt = """select EXP exp(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select EXPexp(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select EXP(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select EXP(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select EXP(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select EXP('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select EXP(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select EXP(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select EXP('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select EXP(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #$err_msg 8428 "EXP"
    stmt = """select EXP(-99999999999999999999999999999999.9999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n16exp""", 'n16s17')
    
    #$err_msg 8428 "EXP"
    stmt = """select EXP(999999999999999999999999999999999.99999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n16exp""", 'n16s18')
    
    stmt = """select EXP(278) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n16exp""", 'n16s18a')
    
    stmt = """select EXP(279) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n16exp""", 'n16s18b')
    
    stmt = """select exp(5.72000000000000064E+002) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n16exp""", 'n16s18c')
    
    stmt = """select exp(null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select exp(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select exp(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test043(desc="""n17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN17
    #  Description:        Tests for SQL, use of LOG function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LOG function syntax:
    # LOG{(<float-log>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select LOG() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LOG( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select LOG(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled LOG
    
    # error different in SQ and NSK
    stmt = """select lof(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  LOG typed in more than once
    
    stmt = """select LOG log(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select LOGlog(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select LOG(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LOG(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LOG(0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select LOG(-1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select log(-0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select LOG(-9999999999999999999999999999999999.9999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select LOG(9999999999999999999999999999999999.99999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n17exp""", 'n17s18')
    
    stmt = """select log(NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select log(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select log(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test044(desc="""n18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN18
    #  Description:        Tests for SQL, use of LOG10 function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # LOG10 function syntax:
    # LOG10{(<float-log10>)}
    
    # Create LOG18 file
    
    #  numeric-exp not used
    
    stmt = """select LOG10() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG10 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LOG10( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select LOG10(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG10(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG10(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled LOG10
    
    # error different in SQ and NSK
    stmt = """select log20(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  LOG10 typed in more than once
    
    stmt = """select LOG10 log10(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    # error different in SQ and NSK
    stmt = """select LOG10log10(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select LOG10(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LOG10(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG10(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG10('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG10(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG10(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select LOG10('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select LOG10(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select LOG10(-9999999999999999999999999999999.9999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select LOG10(99999999999999999999999999999999.99999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n18exp""", 'n18s18')
    
    stmt = """select log10(NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select log10(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select log10(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select log10988 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    _testmgr.testcase_end(desc)

def test045(desc="""n19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN19
    #  Description:        Tests for SQL, use of PI function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # PI function syntax:
    # PI()
    
    # Create PI file
    
    #  parenthese not used
    
    stmt = """select PI) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select PI( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled PI
    
    #error different in SQ and NSK
    stmt = """select pe() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  PI typed in more than once
    
    stmt = """select PI pi() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #error different in SQ and NSK
    stmt = """select PIpi() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  parenthese contains extra data
    
    stmt = """select PI(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(-9999999999999999999999999999999999999.9999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select PI(9999999999999999999999999999999999999.99999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select pi(NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select pi(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select pi(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select pi(pi()) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select pi(0.3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    _testmgr.testcase_end(desc)

def test046(desc="""n20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN20
    #  Description:        Tests for SQL, use of SQRT function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SQRT function syntax:
    # SQRT{(<float-sqrt>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select SQRT() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SQRT from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SQRT( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select SQRT(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SQRT(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SQRT(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled SQRT
    
    #error different in SQ and NSK
    stmt = """select sqtr(100) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  SQRT typed in more than once
    
    stmt = """select SQRT sqrt(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #error different in SQ and NSK
    stmt = """select SQRTsqrt(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select SQRT(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SQRT(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SQRT(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SQRT('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SQRT(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SQRT(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SQRT('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4045')
    
    stmt = """select SQRT(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select sqrt(-100) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select SQRT(-999999999999999999999999999999999.9999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select SQRT(999999999999999999999999999999999.99999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n20exp""", 'n20s19')
    
    stmt = """select sqrt(NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select sqrt(78 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select sqrt(99.012 - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test047(desc="""n21"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN21
    #  Description:        Tests for SQL, use of POWER function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # POWER function syntax:
    # POWER{(<numeric-exp>, <integer-exp>)}
    
    # Create LOG file
    
    #  numeric-exp, integer-exp, or both not used
    
    stmt = """select power(2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(f1, ) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(), z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  numeric-exp, or integer-exp used more than once
    
    stmt = """select POWER(f4 f1, p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(f4, p1 u2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(f5, f4, p1, u2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(psv p9c, zi1, u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled POWER
    
    #error different in SQ and NSK
    stmt = """select poower(b1, -2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #error different in SQ and NSK
    stmt = """select powerr(b1, p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced POWER
    
    stmt = """select f4
from OPTABLE 
group by POWER(f4, 99999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by POWER(f5, -9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  POWER used twice
    
    stmt = """select POWER power(f4, pi()) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #error different in SQ and NSK
    stmt = """select POWERpower(f5, ABS(-1234556)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select POWER(a, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select POWER(%, 1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(z, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select POWER(t3, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select POWER('abcdefg', 3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select POWER(999999999999999999999999999999, -44) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select POWER(t1, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select POWER(1.23.34, .3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER('01/09/1903', 988) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select POWER(t3, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    #  Invalid integer-exp
    
    stmt = """select POWER(0, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select POWER(0, a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select POWER(.01, %) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(-.987654321, z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select POWER(-1.0, t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select POWER(pi(), 'abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select POWER(-1292343, c3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select POWER(999, 1.23.34) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(988, '01/09/1903') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select POWER(99999999999999999999999999999999999, t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select POWER(2, '07/31/1998 12:00:39.1234') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    #  numeric-exp, integer-exp, or both is null
    
    stmt = """select POWER(null, 3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select POWER(3.1415, null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select POWER(null, NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid caculation for numeric-exp, integer-exp, or both
    
    stmt = """select POWER(0.5 * #, 123) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(.1 / z, 02) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select POWER($ / null, -1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(12567890, 5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(09876564, 100 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select POWER(-1.22, $ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(1234567890 - null, 5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(09876564 + null, 41 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select POWER(-1.22 * null, $ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(t1, t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    #  This is non-supported feature, should get error message:
    
    stmt = """select power(-9, -2.2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select power(-9, 2.2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select power(0, -2.2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select power(-323, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n21exp""", 'n21s51')
    
    _testmgr.testcase_end(desc)

def test048(desc="""n22"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN22
    #  Description:        Tests for SQL, use of <numeric-exp> **
    #			<integer-exp> function in the select list.
    #                      This is a negative test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    #
    # Create LOG file
    
    #  numeric-exp, integer-exp, or both not used
    
    stmt = """select ** 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select f1 **  from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select **, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp, or integer-exp used more than once
    
    stmt = """select f4 f1 ** p1 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select f4 ** p1u2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select f5 ** f4 p1 u2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select POWER(psv p9c **  zi1 u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid ** operator
    
    stmt = """select 5 *& 2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select 2 (* 4 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select 4 *2 2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select 3 *a 2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misplaced exponentiation expression
    
    stmt = """select f4
from OPTABLE 
group by f4 ** 99;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by f5 ** -9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Invalid numeric-exp
    
    stmt = """select a ** 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select % ** 1 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select z ** 2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select t3 ** 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select 'abcdefg' ** 3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select 9999999999999999999999999999999999.9999999999999 ** (-44)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select t1 ** 2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select 1.23.34 ** 3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select '01/09/1903' ** 9 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select t3 ** 2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    #  Invalid integer-exp
    
    stmt = """select 0 ** 0 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select 0 ** a from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select .01 ** % from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select (-.987654321) ** z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select (-1.0) ** t3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select pi() ** 'abcdefg' from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select (-1292343) ** c3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select 999 ** 1.23.34 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select 98 ** '01/09/1903' from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select 9 ** t3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    stmt = """select 2 ** '07/31/1998 12:00:39.1234' from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4052')
    
    #  numeric-exp, integer-exp, or both is null
    
    stmt = """select null ** 3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select 3.1415 ** null from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select null ** NULL from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    #  Invalid caculation for numeric-exp, integer-exp, or both
    
    stmt = """select (0.5 * #) ** 123) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select (.1 / z) ** 02 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select ($ / null) ** -1 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select 12567890.001 ** (5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select 9876564.33 ** (100 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select -1.22 ** ($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select (1234567890 - null) ** (5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select (09876564 + null) ** (41 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select (-1.22 * null) ** ($ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select t1 ** t2 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4059')
    
    stmt = """select 0 ** 1 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n22exp""", 'n22s46')
    
    stmt = """select 0 ** (-1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select -999 ** 999.999 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    stmt = """select -111 ** .111111 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8428')
    
    _testmgr.testcase_end(desc)

def test049(desc="""n23"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN23
    #  Description:        Tests for SQL, use of RAND function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # RAND function syntax:
    # RAND{(<float-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select RAND) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RAND from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select RAND( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select rand(( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select RAND(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RAND(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RAND(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled RAND
    
    #error different in SQ and NSK
    stmt = """select ramd(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select RANDOMNUM(93) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  RAND typed in more than once
    
    stmt = """select RAND rand(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RANDrand(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select RAND(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RAND(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select RAND('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND(-99999999999999999999999999999999.9999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RAND(99999999999999999999999999999999.99999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select Rand(-10) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select RanD(1.999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select rand(-.00159E+15) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select rand(NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select rand(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    stmt = """select rand(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4313')
    
    _testmgr.testcase_end(desc)

def test050(desc="""n24"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN24
    #  Description:        Tests for SQL, use of SIGN function
    #                      in the select list.  This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # SIGN function syntax:
    # SIGN{(<float-exp>)}
    
    # Create LOG file
    
    #  numeric-exp not used
    
    stmt = """select SIGN() from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIGN from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SIGN( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select sign*( from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  numeric-exp used more than once
    
    stmt = """select SIGN(f1, psc) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIGN(u1, psv, 99) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIGN(f3 f4) from optabel;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled SIGN
    
    stmt = """select sing(p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  SIGN typed in more than once
    
    stmt = """select SIGN sign(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIGNsign(u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid numeric-exp
    
    stmt = """select SIGN(a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select SIGN(z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select SIGN(t1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select SIGN('07/31/1998 11:43:13.1234 a.m.') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select SIGN(%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIGN(#%) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select SIGN('this is a string, wrong') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4041')
    
    stmt = """select SIGN(ABCDEFG) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select sign(NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4099')
    
    stmt = """select sign(ps9 * null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select sign(psv - null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    _testmgr.testcase_end(desc)

def test051(desc="""n26"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     testN26
    #  Description:        Tests for SQL, use of MOD function
    #                      in the select list. This is a negative
    #                      test.
    #  Test case inputs:
    #  Test case outputs:
    #  Expected Results:   (provide a high-level description)
    #
    # =================== End Test Case Header  ===================
    # MOD function syntax:
    # MOD{(<integer-exp1>, <integer-exp2>)}
    
    # Create LOG file
    
    #  integer-exp1, integer-exp2, or both not used
    
    stmt = """select MOD(, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(f1, ) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select mod(f2, f4) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(), z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD, z from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    #  integer-exp1, or integer-exp2 used more than once
    
    stmt = """select MOD(f4 f1, p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(f4, p1 u2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(f5, f4, p1, u2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(psv p9c, zi1, u3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  Misspelled MOD
    
    stmt = """select mood(p1, -2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select mmod(p1, p1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Misplaced MOD
    
    stmt = """select f4
from OPTABLE 
group by MOD(u2, 99999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4197')
    
    stmt = """select f5
from OPTABLE 
order by MOD(zi2, -9999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    #  MOD used twice
    
    stmt = """select MOD mod(zi3, 7) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MODMod(zi1, ABS(-1234556)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #  Invalid integer-exp1
    
    stmt = """select MOD(a, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select MOD(%, 1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(z, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(t3, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD('abcdefg', 3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(9999999999999999.99999999999999, -44) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select mod(99999999999999999999, 99999999999999999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3037')
    
    stmt = """select MOD(t1, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(1.23.34, .3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD('01/09/1903', 988) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(p9c, 2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    #  Added this query to test number with a scale.
    stmt = """select MOD(9.23432, 5) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    #  Invalid integer-exp2
    
    stmt = """select MOD(0, a) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4001')
    
    stmt = """select MOD(1, %) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(987654321, z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select mod(9812314, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select MOD(1, t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select mod(100, cast(-1 as largeint)) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/n26exp""", 'n26s31')
    
    stmt = """select MOD(p1, 'abcdefg') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(zi3, c3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(999, 1.23.34) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(u2, '01/09/1903') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select mod(u2, 0) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    stmt = """select MOD(999, t3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select MOD(2, '07/31/1998 12:00:39.1234') from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    stmt = """select mod(2, 8.1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select mod(3, 1.1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    stmt = """select mod(2, 9999999999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3037')
    
    #  Added this query to test number with a scale.
    stmt = """select mod(2, 9.99999999999999) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    #  integer-exp1, integer-exp2, or both is null
    
    stmt = """select MOD(null, 3) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select MOD(zi3, null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    stmt = """select MOD(null, NULL) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4097')
    
    # Added this query to test number with a scale.
    stmt = """select MOD(2.343, 9.4373) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4047')
    
    #  Invalid caculation for integer-exp1, integer-exp2, or both
    
    stmt = """select MOD(5 * #, 123) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(1 / z, 02) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select MOD($ / null, -1) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(12567890, 5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(zi2, 100 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4034')
    
    stmt = """select MOD(22, $ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(u3 - null, 5 * #) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(09876564 + null, 41 / z) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4098')
    
    stmt = """select MOD(p1 * null, $ / null) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '15001')
    
    stmt = """select MOD(t1, t2) from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4046')
    
    _testmgr.testcase_end(desc)

