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
import defs

_testmgr = None
_testlist = []
_dci = None

# ==================   Begin Test Case Header   ==============================
#
#  Test case name:     volt6
#  Description :  Volatile table enhancements in R2.3 SP2
#  Using a suitable key as a primary key if the primary key is not specified in create table.
#  Allowing duplicate values and null values to be used in the primary key.
#  Revision History:
#      08/01/08       Created.
#

# =================== End Test Case Header  =================================
#  Volatile table with the suitable key as a largeint (nullable).
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d1
(
seqno   integer         	        default null,    

smin1   smallint        signed          default null,
smin2   smallint        unsigned        default null,    

inte1   integer         signed          default null,
inte2   integer         unsigned        default null,    

lint1   largeint        	        default null,
lint2   largeint        		default null,    

nume1   numeric(7)      unsigned        default null,
nume2   numeric(9,3)    unsigned        default null,
nume3   numeric(18)     signed          default null,
nume4   numeric(18,15)  signed          default null,    

deci1   decimal(3)      unsigned        default null,
deci2   decimal(18,0)   signed          default null,
deci3   decimal(18,9)   signed          default null,    

pict1   pic s9(18)      comp            default null,
pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

flot1   float (12)                      default null,
flot2   float (52)                      default null,    

real1   real                            default null,
real2   real                            default null,    

dblp1   double precision                default null,
dblp2   double precision                default null,    

char1   char (12)                       default null,
char2   varchar (30)            upshift default null    

) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by lint1
    stmt = """showddl d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1 values
(null, 0, 0, 0, 0, null, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Zero','Zero');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
 
    stmt = """insert into d1 values
(2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .1, 1, 1, 1, 1, 1, 1, 1, 1,'One','One');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1 (lint1, lint2) values (null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
 
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1 (lint1, lint2) values (-9223372036854775808, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
 
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into d1 (lint1) values (-9223372036854775808), (-9223372036854775808);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
 
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1
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
dblp2,
char1,
char2
)
values
(
null,    

-32768,
0,    

-2147483648,
1,    

null,
-9223372036854775808,    

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
9,    

'HP',
'Compaq'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
   
    stmt = """select count(*) from d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as an integer
    _testmgr.testcase_end(desc)

def test002(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d2
(
seqno   integer         		default null,    

smin1   smallint        signed          default null,
smin2   smallint        unsigned        default null,    

inte1   integer                 	default null,    

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

pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by seqno
    stmt = """showddl d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d2 values
(1, 0, 0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d2 (seqno, vchar1) values (3, 'celebration');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d2 (seqno) values (4), (4);"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d2 (seqno) values (4), (4);"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d2 (seqno) values (null), (null);"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d2 (seqno, vchar1) values (null, 'A new year');"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d2 (
seqno,
smin1,
smin2,
inte1,
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
pict2,
pict3,
pict4,
bignum1
)
values
(
null,    

-32768,
32768,    

-2147483648,    

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

-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into  d2
values (
6,    

7892,
32768,    

2937923,    

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

0.99,
9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a small integer
    _testmgr.testcase_end(desc)

def test003(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d3
(
smin1   smallint        signed          default null,
smin2   smallint        unsigned        default null,    

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

pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by smin2 (unsigned preceded over signed)
    stmt = """showddl d3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d3 values
(1, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d3 (smin2, vchar1) values (null, 'Spring time');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d3 (smin2) values (null), (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)

    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d3 (smin1, smin2) values (null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d3 (
smin1,
smin2,
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
pict2,
pict3,
pict4,
bignum1
)
values
(
32767,
32766,    

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

-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d3
values (
7892,
32768,    

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

0.99,
9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a decimal value
    _testmgr.testcase_end(desc)

def test004(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d4
(
deci1   decimal(18,9)           	default null,
deci2   decimal(18,0)   signed          default null,    

flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by pict4 (decimal)
    stmt = """showddl d4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s1b
    stmt = """insert into  d4 values
(0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s1b
    stmt = """insert into  d4 values
(1, 1, 1, 1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, '1', 'we are united', 1, 1, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d4 (pict4, vchar1) values (3, 'Happy time!');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d4 (pict4) values (128.928321), (128.928321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d4 (deci1, pict4) values (null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d4 (pict4, tims1) values (null, timestamp'2012-06-23 21:34:01.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 (
deci1,
deci2,
flot1,
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict3,
pict4,
bignum1
)
values
(
-9999999.99999,
128928321128928321,    

7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4
values (
99999.999,
null,    

11897.9998877656,    

898889.00000997,    

555.23,    

date'2000-04-12',    

time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'123',
'nothing is ok',    

9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    
    stmt = """create volatile table d4a
(
deci1   decimal(18,9)           	default null,
deci2   decimal(18,0)   signed          default null,    

flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict3   pic s9(13)v9(5)                 default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by deci1
    stmt = """showddl d4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d4a values
(0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4a values
(1, 1, 1, 1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, '1', 'we are united', 1, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4a (deci1, vchar1) values (3, 'Happy time!');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d4a (deci1) values (128.928321), (128.928321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d4a (deci1, pict3) values (null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d4a (deci1, tims1) values (null, timestamp'2012-06-23 21:34:01.000000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d4a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4a')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a numeric value
    _testmgr.testcase_end(desc)

def test005(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table d5
(
nume2   numeric(9,3)    unsigned        default null,
nume3   numeric(18)     signed        default null,    

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

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by nume3
    stmt = """showddl d5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d5 values
(0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d5 (nume3, pict1) values (3, -999999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d5 (nume3) values (128928.321), (128928.321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    stmt = """insert into  d5 (nume2, nume3) values (128928.321, 128928321128928321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d5 (nume2, nume3) values (null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d5 (nume3, pict1) values (null, -999999999999999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d5 (
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
99999.999,    

null,    

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
    
    stmt = """insert into  d5
values (
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
    
    stmt = """select count(*) from d5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    ##expectfile ${test_dir}/b01exp b01s5a1
    stmt = """create volatile table d5a
(
nume2   numeric(9,3)    unsigned        default null,    

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

pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by nume2
    stmt = """showddl d5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d5a values
(0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d5a (nume2, flot1) values (3, 19939);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d5a (nume2) values (128928.321), (128928.321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d5a (nume2) values (128928.321), (128928.321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d5a (nume2) values (null), (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d5a (
nume2,
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
pict2,
pict3,
pict4,
bignum1
)
values
(
null,    

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

-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d5a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5a')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a numeric value
    _testmgr.testcase_end(desc)

def test006(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expectfile ${test_dir}/b01exp b01s6
    stmt = """create volatile table d6
(
flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict2   pic sv9(2)      comp            default null,
pict3   pic s9(13)v9(5)                 default null,
pict4   pic 9(3)v9(6)                   default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    
    # stored by pict2 (numeric)
    stmt = """showddl d6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6 values
(0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, 'Olympics', '1234567890123', 0, 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 4 row(s) inserted.*
    stmt = """insert into  d6 (pict2) values (-0.71939020), (-0.94938), (null), (-0.94938);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6 (
flot1,
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict2,
pict3,
pict4,
bignum1
)
values
(
7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-0.99,
-9999999999999.99999,
6.000001,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    
    ##expect any *--- SQL operation complete.*
    ##expectfile ${test_dir}/b01exp b01s6
    stmt = """create volatile table d6a
(
flot1   float (52)              	default null,    

real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,    

vchar1	varchar(13)			default null,    

pict3   pic s9(13)v9(5)                 default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    
    # stored by pict3 (numeric)
    stmt = """showddl d6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6a values
(0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, 'Olympics', '1234567890123', 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d6a (pict3) values (-0.94938), (null) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d6a (
flot1,
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
pict3,
bignum1
)
values
(
7.000000000001,    

-2.2250738585072014,    

-1.17549435e-38,    

date'2006-06-15',    

time'17:55:45',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'1',    

'we are united',    

-0.94938,    

12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d6a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6a')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a bignum value
    _testmgr.testcase_end(desc)

def test007(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d7
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,
vchar1	varchar(13)			default null,    

bignum1 numeric(128,6)   signed 	default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by bignum1
    stmt = """showddl d7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d7 values
(0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d7 values
(1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, '1', 'we are united', 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d7 (bignum1, time1) values (98342178979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678, time'13:32:20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d7 (bignum1) values (null), (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d7 (
real1,
dblp1,
date1,
time1,
tims1,
intv1,
char1,
vchar1,
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

98342178979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a char value
    _testmgr.testcase_end(desc)

def test008(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d8
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

char1   char (12)               	default null,
vchar1	varchar(13)			default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by char1
    stmt = """showddl d8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d8 values
(0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, 'adieu', '1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d8 values
(1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, 'amour', 'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d8 (char1) values (null), ('adieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d8 (
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

'au revoir',    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d8
values (
898889.00000997,    

555.23,    

date'2000-04-12',    

time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

null,
'nothing is ok'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a date value
    _testmgr.testcase_end(desc)

def test009(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    # stored by date1
    stmt = """create volatile table d9
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

vchar1	varchar(13)			default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by date1
    stmt = """showddl d9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9 values
(0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month,'1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9 values
(1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month,'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9 (date1, real1) values (null, -2.2250738585072014);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d9 (
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
    stmt = """insert into  d9
values (
898889.00000997,    

555.23,    

date'2005-12-31',    

time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'nothing is ok'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a time value
    _testmgr.testcase_end(desc)

def test010(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expectfile ${test_dir}/b01exp b01s10
    stmt = """create volatile table d10
(
time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

vchar1	varchar(13)			default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by time1
    ##expectfile ${test_dir}/b01exp b01s10
    stmt = """showddl d10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d10 values
(time'23:00:53', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month,'1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d10 values
(time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month,'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d10 (time1, vchar1) values (null, 'au revoir !');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d10 (
time1,
tims1,
intv1,
vchar1
)
values
(
time'23:00:53',    

timestamp'2006-06-23 17:56:59.300439',    

interval'06-06' year to month,    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d10
values (
time'00:21:30',    

timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'nothing is ok'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d10;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a timestamp value
    _testmgr.testcase_end(desc)

def test011(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expectfile ${test_dir}/b01exp b01s11
    stmt = """create volatile table d11
(
tims1   timestamp               	default null,    

intv1   interval year to month  	default null,    

vchar1	varchar(13)			default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by tims1
    stmt = """showddl d11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d11 values
(timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month,'1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d11 values
(timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month,'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d11 (tims1, vchar1) values (null, 'au revoir !');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d11 (
tims1,
intv1,
vchar1
)
values
(
timestamp'2000-06-23 01:01:01.000000',    

interval'06-06' year to month,    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d11
values (
timestamp'1999-01-01 02:11:33.100439',    

interval'06-11'year to month,    

'nothing is ok'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d11;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a interval value
    _testmgr.testcase_end(desc)

def test012(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expectfile ${test_dir}/b01exp b01s12
    stmt = """create volatile table d12
(
intv1   interval year to month  	default null,
iday1   interval day to second          default null,    

vchar1	varchar(13)			default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by intv1
    stmt = """showddl d12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d12 values
(interval'01-01'year to month, interval '22:12:00:00.000001' day to second(6), '1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d12 values
(interval'99-02'year to month, interval '00:00:00:00.000001' day to second(6), 'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d12 (intv1, vchar1) values (interval'99-02'year to month, 'au revoir !!!');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d12 (
intv1,
iday1,
vchar1
)
values
(
null,
interval '22:12:00:00.000001' day to second(6),    

'we are united'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d12
values (
interval'06-11'year to month,
interval '11:12:00:00.000001' day to second(6),    

'nothing is ok'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """select count(*) from d12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as a varchar value
    _testmgr.testcase_end(desc)

def test013(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d13
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

vchar1	varchar(13)			default null,
vchar2	varchar(8)		  	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by vchar1
    stmt = """showddl d13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d13 values(0, 0, null, 'mon dieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d13 values(-1, -1, 'we are united', 'mon dieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into  d13 (vchar1) values ('we are united'), (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d13 (
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
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d13
values (
898889.00000997,    

555.23,    

'nothing is ok',
null    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from d13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as not null preceding over null col.
    _testmgr.testcase_end(desc)

def test014(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d14
(
real1   real                    	default null,    

dblp1   double precision        	default null,    

vchar1	varchar(13)			default null,
vchar2	varchar(8)		  	not null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by vchar2
    stmt = """showddl d14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d14 values(0, 0, null, 'mon dieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d14 values(-1, -1, 'we are united', 'mon dieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d14 (
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
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d14
values (
898889.00000997,    

555.23,    

'nothing is ok',
'non-null'    

);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d14;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    
    # ==================   Begin Test Case Header   ==============================
    #  Volatile table with the suitable key as an unsigned over signed value.
    _testmgr.testcase_end(desc)

def test015(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expectfile ${test_dir}/b01exp b01s15
    stmt = """create volatile table d15
(
smin1   smallint        signed          not null,
smin2   smallint        unsigned        default null,    

inte1   integer         signed          not null,
inte2   integer         unsigned        default null    

)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by inte2
    stmt = """showddl d15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d15 values(12, 0, -2147483648, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d15 values(-53, null, 718732, 3890832);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d15 values(-53, null, -12838931, 3890832);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d15;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    
    ##expectfile ${test_dir}/b01exp b01s15a
    stmt = """create volatile table d15a
(
bignum1 numeric(128,6)   signed 	not null,
bignum2 numeric(128,6)   unsigned 	default null,
bignum3 numeric(123)     unsigned 	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by bignum2
    stmt = """showddl d15a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d15a values
(12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d15a values
(12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
123456789797477427402424035458058352084284283085883538385385385385454545454545454545385385385385385385385353531234567890123
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d15a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15a')
    
    # ==================   Begin Test Case Header   ==============================
    #  All the preceded datatypes are the same type.  First column is the suitable key
    _testmgr.testcase_end(desc)

def test016(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d16a
(
real1   real                    	default null,
real2	real				default null,
real3	real				default null,
real4	real				default null,    

dblp1   double precision        	default null,    

date1   date                    	default null,
date2   date                    	default null,
date3   date                    	default null,
date4   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by date1
    stmt = """showddl d16a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d16a values
(0, 0, 0, 0, 0, date'2000-01-01', date'2021-01-01', date'2011-03-01', date'2030-12-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d16a values
(-2.2250738585072014, 1, -2.2250738585072014, 1, 1, date'2005-12-31', null, null, null, time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d16a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16a')
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table d16b
(
flot1   float (12)                      not null,
flot2   float (12)                      not null,
flot3   float (12)                      not null,
flot4   float (12)                      not null,    

dblp1   double precision        	default null,    

time1   time                    	default null,
time2   time                    	default null,
time3  	time                    	default null,
time4   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by time1
    stmt = """showddl d16b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d16b values
(0, 0, 0, 0, 0, time'00:00:00', time'00:00:00', time'21:33:00', time'15:00:32', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d16b values
(7.000000000001, 122.00000892512, 9.183842000001, 67.000000456001, 1, time'00:00:00', time'13:54:43', null, null, timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """select count(*) from d16b;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16b')
    
    ##expectfile ${test_dir}/b01exp b01s16c
    stmt = """create volatile table d16c
(
nume1   numeric(9,3)       unsigned        not null,
nume2   numeric(9,3)       unsigned        not null,
nume3   numeric(9,3)       unsigned        not null,    

dblp1   double precision        	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by nume1
    stmt = """showddl d16c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d16c values
(0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d16c values
(322212.589, 123.456, 9.183842000001, 67.000000456001, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/a01exp a01s16c
    stmt = """select count(*) from d16c;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16c')
    
    ##expectfile ${test_dir}/b01exp b01s16d
    stmt = """create volatile table d16d
(
bignum1 numeric(128,6)   signed 	default null,
bignum2 numeric(128,6)   signed 	default null,
bignum3 numeric(128,6)   signed 	default null,    

date1   date                    	default null,    

time1   time                    	default null,    

tims1   timestamp               	default null,    

intv1   interval year to month  	default null
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by bignum1
    stmt = """showddl d16d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into  d16d values
(null, null, null, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into  d16d values
(12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d16d;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16d')
    
    # ==================   Begin Test Case Header   ==============================
    #  All the datatypes are not qualified as a suitable key.
    _testmgr.testcase_end(desc)

def test017(desc=''):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #control query default POS 'OFF';
    
    ##expectfile ${test_dir}/b01exp b01s17
    stmt = """create volatile table d17
(
real1   real            not null        not droppable,
real2   real            not null        not droppable,    

flot1   float (12)              default null,
flot2   float (52)              default null,    

dblp1   double precision        default null,
dblp2   double precision        default null    

) max table size 256
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # SYSKEY with no partition
    stmt = """showddl d17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d17 values(0, 0, 0, 0, 0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d17 values(1, 1, 1, 1, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d17 values( -1.17549435e-38,
8,    

7.000000000001,
-2.2250738585072014e-308,    

-2.2250738585072014e-308,
9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/a01exp a01s17
    stmt = """select count(*) from d17;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    
    ##expectfile ${test_dir}/b01exp b01s17a
    stmt = """create volatile table d17a
(
real1   real            			     ,
real2   real            not null        not droppable,    

flot1   float (12)              default null,
flot2   float (52)              default null,    

dblp1   double precision        default null,
dblp2   double precision        default null    

) max table size 256
no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # SYSKEY with no partition
    stmt = """showddl d17a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d17a values(0, 0, 0, 0, 0, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d17a values(null, 1, 1, 1, null, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expectfile ${test_dir}/b01exp b01s0b
    stmt = """insert into d17a values( -1.17549435e-38,
8,    

7.000000000001,
-2.2250738585072014e-308,    

-2.2250738585072014e-308,
9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d17a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17a')
    
    _testmgr.testcase_end(desc)

