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

# ==================   Begin Test Case Header   ==============================
#
#  Test case name:     volt7
#  Description :  Volatile table enhancements in R2.3 SP2
#  Using a suitable key as a primary key if it's not defined in create table.
#  Allowing duplicate and null values to be used in partitioning and store by clause.
#  Revision History:
#      08/01/08       Created.
#

# =================== End Test Case Header  =================================
#  Nullable primary key
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
    
    stmt = """create volatile table d1
(
seqno   integer         		default null,    

smin1   smallint        signed          default null,
smin2   smallint        unsigned        default null,    

inte1   integer                 	default null,    

nume2   numeric(9,3)    unsigned        default null,
nume3   numeric(18)     signed          default null,    

deci1   decimal(18,9)           	default null,    

flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict1   pic s9(18)      comp            default null,
pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null,    

primary key(seqno)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # primary key can be null
    stmt = """showddl d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d1 values
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d1 (seqno) values (4), (12324);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d1 (seqno, pict1) values (null, -999999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d1 (
seqno,
smin1,
smin2,
inte1,
nume2,
nume3,
deci1,
flot1,
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict1,
pict2,
pict3,
pict4,
bignum1
)
values
(
70892,    

-32768,
32768,    

-2147483648,    

99999.999,
-999999999999999999,    

-9999999.99999,    

7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-999999999999999999,
-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d1
values (
6,    

7892,
32768,    

2937923,    

23990.78,
999999999999999999,    

786.12598,    

11897.9998877656,    

898889.00000997,    

555.23,    

date'2000-04-12',    

time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'123',
'nothing is ok',    

999999999999999999,
0.99,
9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s1""")
    
    # ==================   Begin Test Case Header   ==============================
    #  Nullable primary key (droppable)
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d2
(
seqno   integer                         default null,    

smin1   smallint        signed          default null,
smin2   smallint        unsigned        default null,    

inte1   integer                 	default null,    

nume2   numeric(9,3)    unsigned        default null,
nume3   numeric(18)     signed          default null,    

deci1   decimal(18,9)           	default null,    

flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict1   pic s9(18)      comp            default null,
pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null,    

primary key(seqno) droppable
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # primary key can be null and droppable
    stmt = """showddl d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d2 values
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d2 (seqno) values (4), (89234);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d2 (seqno, pict1) values (null, -999999999999999999);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into  d2 (
seqno,
smin1,
smin2,
inte1,
nume2,
nume3,
deci1,
flot1,
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict1,
pict2,
pict3,
pict4,
bignum1
)
values
(
92938,    

-32768,
32768,    

-2147483648,    

99999.999,
-999999999999999999,    

-9999999.99999,    

7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-999999999999999999,
-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s2""")
    
    # ==================   Begin Test Case Header   ==============================
    #  Nullable store by key
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d3
(
seqno   integer                         ,    

smin1   smallint        signed          default null,
smin2   smallint        unsigned        default null,    

inte1   integer                 	default null,    

nume2   numeric(9,3)    unsigned        default null,
nume3   numeric(18)     signed          default null,    

deci1   decimal(18,9)           	default null,    

flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict1   pic s9(18)      comp            default null,
pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null    

) store by(seqno)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by key can be null
    stmt = """showddl d3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d3 values
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d3 (seqno) values (4), (4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d3 (seqno) values (null), (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
 
    stmt = """insert into  d3 (seqno, pict1) values (272898, -999999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d3 (
seqno,
smin1,
smin2,
inte1,
nume2,
nume3,
deci1,
flot1,
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict1,
pict2,
pict3,
pict4,
bignum1
)
values
(
27891,    

-32768,
32768,    

-2147483648,    

99999.999,
-999999999999999999,    

-9999999.99999,    

7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-999999999999999999,
-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s3""")
    
    _testmgr.testcase_end(desc)

def test004(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d4
(
time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

vchar1	varchar(13)			default null,    

primary key(time1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # store by time1
    stmt = """showddl d4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d4 values
(time'23:00:53', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month,'1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d4 values
(null, timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month,'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 (time1) values (time'23:12:53');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 (time1, vchar1) values (time'11:12:53', 'au revoir !!!');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 (
time1,
tims1,
intv1,
vchar1
)
values
(
time'09:43:53',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s4""")
    
    _testmgr.testcase_end(desc)

def test005(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d5
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,
vchar1	varchar(13)			default null,    

pict1   pic s9(18)      comp            default null,
pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null    

) store by(bignum1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl d5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d5 (bignum1, pict1) values (98342178979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678, -999999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d5 (
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict1,
pict2,
pict3,
pict4,
bignum1
)
values
(
-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-999999999999999999,
-0.99,
-9999999999999.99999,
6.000001,    

98342178979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d5
values (
898889.00000997,    

555.23,    

date'2000-04-12',    

time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'123',
'nothing is ok',    

999999999999999999,
0.99,
9999999999999.99999,
6.000001,    

null    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s5""")
    
    # ==================   Begin Test Case Header   ==============================
    #  Nullable unique key
    _testmgr.testcase_end(desc)

def test006(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d6
(
real1   real                            default null,    

dblp1   double precision        	default null,    

date1   date                            default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)       		, -- unique,
vchar1	varchar(13)			default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by char1
    stmt = """showddl d6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6 values
(0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, null, '1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6 values
(1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, 'spring', 'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6 (
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1
)
values
(
-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'united',    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s6""")
    
    # ==================   Begin Test Case Header   ==============================
    #  USER specified clauses will disable auto-selection of keys - primary key specified
    _testmgr.testcase_end(desc)

def test007(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d7a
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

bignum1 numeric(128,6)   	 	not null,
bignum2 numeric(128,6)   		not null,    

primary key (bignum2)
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by bignum2
    stmt = """showddl d7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d7a values
(0, 0, 98765432179747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d7a values
(1, 1, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.123456, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.654321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d7a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s7a""")
    
    stmt = """create volatile table d7b
(
smin1   smallint        unsigned          not null,
smin2   smallint        signed        default null,    

inte1   integer         signed          not null,
inte2   integer         unsigned        default null,    

primary key (smin2)
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    
    # stored by smin2
    stmt = """showddl d7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into d7b values(12, 0, -2147483648, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d7b values(53, null, 718732, 3890832);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into d7b values(53, -2134, -12838931, 3890832);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d7b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s7b""")
    
    # ==================   Begin Test Case Header   ==============================
    #  USER specified clauses will disable auto-selection of keys - store by specified
    _testmgr.testcase_end(desc)

def test008(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d8a
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

vchar1	varchar(13)			default null,
vchar2	varchar(8)		  	not null
) store by (vchar1)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by vchar1
    stmt = """showddl d8a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d8a values(0, 0, null, 'mon dieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8a values(-1, -1, 'we are united', 'mon dieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8a (
real1,
dblp1,
vchar1,
vchar2
)
values
(
-2.2250738585072014,    

-1.17549435e-38,    

'we are united',
'golfing!'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8a
values (
898889.00000997,    

555.23,    

'nothing is ok',
'non-null'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d8a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s8a""")
    
    stmt = """create volatile table d8b
(
intv1   interval year to month  	not null,
iday1   interval day to second          default null,    

vchar1	varchar(13)			default null
) store by (iday1)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by iday1
    stmt = """showddl d8b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d8b values
(interval'01-01'year to month, interval '22:12:00:00.000001' day to second(6), '1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8b values
(interval'99-02'year to month, interval '00:00:00:00.000001' day to second(6), 'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d8b (intv1, vchar1) values (interval'99-02'year to month, 'au revoir !!!');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8b (
intv1,
iday1,
vchar1
)
values
(
interval'03-02'year to month,
interval '22:12:00:00.000001' day to second(6),    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8b
values (
interval'06-11'year to month,
interval '11:12:00:00.000001' day to second(6),    

'fresh product'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from d8b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s8b""")
    
    _testmgr.testcase_end(desc)

def test009(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d9a
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	not null,
date2   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

vchar1	varchar(13)			default null    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by date2
    stmt = """showddl d9a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9a values
(0, 0, date'2000-01-01', date'2020-12-01',time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month,'1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9a values
(1, 1, date'2005-12-31', date'1992-01-23',time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month,'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9a (date1, date2, real1) values (date'1992-01-23', null, -2.2250738585072014);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9a (
real1,
dblp1,
date1,
time1,
tims1,
intv1,
vchar1
)
values
(
-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9a
values (
898889.00000997,    

555.23,    

date'2005-12-31',
null,    

time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'nothing is ok'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d9a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s9a""")
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d9b
(
nume1   numeric(9,3)       unsigned        not null,
nume2   numeric(18)          signed        not null,
nume3   numeric(7,2)       unsigned        not null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null
);"""
    output = _dci.cmdexec(stmt)
    
    # stored by nume3
    stmt = """showddl d9b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9b values
(0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9b values
(322212.589, 123456, 9.183842000001, 67.000000456001, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d9b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s9b""")
    
    _testmgr.testcase_end(desc)

