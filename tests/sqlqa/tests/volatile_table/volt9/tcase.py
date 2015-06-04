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
#  Test case name:     volt9
#  Description :  Volatile table enhancements in R2.3 SP2
#  Negative test: Turn off the cqd volatile_table_find_suitable_key
#  Revision History:
#      08/01/08       Created.
#
# =================== End Test Case Header  =================================
#
# CQD volatile_table_find_suitable_key is ON by setup. Select the suitable key.

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

) attribute extent 256;"""
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
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1 values
(2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .1, 1, 1, 1, 1, 1, 1, 1, 1,'One','One');"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1 (lint1, lint2) values (null, null);"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into d1 (lint1, lint2) values (-9223372036854775808, null);"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *--- 2 row(s) inserted.*
    stmt = """insert into d1 (lint1) values (-9223372036854775808), (-9223372036854775808);"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """select count(*) from d1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s1""")
    
    # Turn off the CQD volatile_table_find_suitable_key
    # The first column is the primary key.
    _testmgr.testcase_end(desc)

def test002(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """control query default volatile_table_find_suitable_key 'OFF';"""
    output = _dci.cmdexec(stmt)
    
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
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by seqno
    stmt = """showddl d2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by smin1
    stmt = """showddl d3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table d9
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
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stored by deci1
    stmt = """showddl d9;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
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
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table d17
(
real1   real            not null        not droppable,
real2   real            not null        not droppable,    

flot1   float (12)              default null,
flot2   float (52)              default null,    

dblp1   double precision        default null,
dblp2   double precision        default null    

) attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # ==================   Begin Test Case Header   ==============================
    #  CTAS having CQD volatile_table_find_suitable_key turn off
    _testmgr.testcase_end(desc)

def test003(desc=""""""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """control query default volatile_table_find_suitable_key 'OFF';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default POS 'OFF';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table d4
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
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl d4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d4 values
(0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0', '1234567890123', 0, 0, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 values
(1, 1, 1, 1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, '1', 'we are united', 1, 1, 12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 (pict4, vchar1) values (3, 'Happy time!');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d4 (pict4) values (128.928321), (128.928321);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s4""")
    
    ##expectfile ${test_dir}/a01exp a01s4e
    stmt = """create volatile table vd4 as select * from d4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    stmt = """create table d8
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
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl d8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d8 values
(0, 0, date'2000-01-01', time'00:00:00', timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, 'adieu', '1234567890123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8 values
(1, 1, date'2005-12-31', time'00:00:00', timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, 'amour', 'we are united');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d8 (char1) values (null), ('adieu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    
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
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s8""")
    
    ##expectfile ${test_dir}/a01exp a01s4e
    stmt = """create volatile table vd8 as select * from d8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8421')
    
    stmt = """create table d15a
(
bignum1 numeric(128,6)   signed 	not null,
bignum2 numeric(128,6)   unsigned 	default null,
bignum3 numeric(123)     unsigned 	default null
)
attribute extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl d15a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into  d15a values
(12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into  d15a values
(12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
12345678979747742740242403545805835208428428308588353838538538538545454545454545454538538538538538538538535353123456789012.345678,
123456789797477427402424035458058352084284283085883538385385385385454545454545454545385385385385385385385353531234567890123
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from d15a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", """a01s15a""")
    
    ##expectfile ${test_dir}/a01exp a01s15e
    stmt = """create volatile table vd15a as select * from d15a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    # _dci.expect_error_msg(output, '8102')
    
    _testmgr.testcase_end(desc)

