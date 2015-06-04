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

# ==================   Begin Test Case Header   ==================
#
#  Test case name:     volt5
#
#      To test if the first column
#	of a VOLATILE TABLE becomes the default STORE BY key
#	when not explicitly specified.
#
#      Example:
#              create volatile table a
#		(
#			i	int,
#			j	int
#		);
#
#		would result in ...
#
#CREATE VOLATILE TABLE A
#(
#  I                                INT NO DEFAULT -- NOT NULL NOT DROPPABLE
#, J                                INT DEFAULT NULL
#, CONSTRAINT
#    CAT_WM_16.
#    VOLATILE_SCHEMA_11507105521201820280227986817DEFAULT_MXCI_USER0000000001.
#    A_177285786_4662 PRIMARY KEY (I ASC) NOT DROPPABLE
#, CONSTRAINT
#    CAT_WM_16.
#    VOLATILE_SCHEMA_11507105521201820280227986817DEFAULT_MXCI_USER0000000001.
#    A_531775786_4662 CHECK
#    (CAT_WM_16.
#    VOLATILE_SCHEMA_11507105521201820280227986817DEFAULT_MXCI_USER0000000001.
#    A.I IS NOT NULL) NOT DROPPABLE
#)
#LOCATION \WALLY6.$W61100.ZSDDG5R9.SK5KGG00
#NAME WALLY6_W61100_ZSDDG5R9_SK5KGG00
#STORE BY (I ASC)
#;
#  Revision History:
#      06/27/06       Created.
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
    
def test001(desc='a00'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create volatile table wm000
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
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm001
(
smin1   smallint                default null,
seqno   integer         not null        not droppable,
inte1   integer                 default null,
lint1   largeint                default null,
nume1   numeric(9,3)            default null,
deci1   decimal(18,9)           default null,
pict1   pic s9(13)v9(5)         default null,
flot1   float (52)              default null,
real1   real                    default null,
dblp1   double precision        default null,
date1   date                    default null,
time1   time                    default null,
tims1   timestamp               default null,
intv1   interval year to month  default null,
char1   char (12)               default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm002
(
inte1   integer		not null	not droppable,
seqno   integer         not null        not droppable,
smin1   smallint                default null,
lint1   largeint                default null,
nume1   numeric(9,3)            default null,
deci1   decimal(18,9)           default null,
pict1   pic s9(13)v9(5)         default null,
flot1   float (52)              default null,
real1   real                    default null,
dblp1   double precision        default null,
date1   date                    default null,
time1   time                    default null,
tims1   timestamp               default null,
intv1   interval year to month  default null,
char1   char (12)               default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm003
(
lint1   largeint                default null,
seqno   integer         not null        not droppable,
smin1   smallint                default null,
inte1   integer                 default null,
nume1   numeric(9,3)            default null,
deci1   decimal(18,9)           default null,
pict1   pic s9(13)v9(5)         default null,
flot1   float (52)              default null,
real1   real                    default null,
dblp1   double precision        default null,
date1   date                    default null,
time1   time                    default null,
tims1   timestamp               default null,
intv1   interval year to month  default null,
char1   char (12)               default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm004
(
nume1	numeric(9,3)	not null	not droppable,
seqno	integer		not null	not droppable,
smin1	smallint		default null,
inte1	integer			default null,
lint1	largeint		default null,
deci1	decimal(18,9)		default null,
pict1	pic s9(13)v9(5)		default null,
flot1	float (52)		default null,
real1	real			default null,
dblp1	double precision	default null,
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm005
(
deci1	decimal(18,9)		default null,
seqno	integer		not null	not droppable,
smin1	smallint		default null,
inte1	integer			default null,
lint1	largeint		default null,
nume1	numeric(9,3)		default null,
pict1	pic s9(13)v9(5)		default null,
flot1	float (52)		default null,
real1	real			default null,
dblp1	double precision	default null,
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm006
(
pict1	pic s9(13)v9(5)	not null	not droppable,
seqno	integer		not null	not droppable,
smin1	smallint		default null,
inte1	integer			default null,
lint1	largeint		default null,
nume1	numeric(9,3)		default null,
deci1	decimal(18,9)		default null,
flot1	float (52)		default null,
real1	real			default null,
dblp1	double precision	default null,
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *ERROR[1120]*
    ##expect any *ERROR[1029]*
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table wm007
(
flot1	float (52)		default null,
seqno	integer		not null	not droppable,
smin1	smallint		default null,
inte1	integer			default null,
lint1	largeint		default null,
nume1	numeric(9,3)		default null,
deci1	decimal(18,9)		default null,
pict1	pic s9(13)v9(5)		default null,
real1	real			default null,
dblp1	double precision	default null,
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *ERROR[1120]*
    ##expect any *ERROR[1029]*
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table wm008
(
real1	real		not null	not droppable,
seqno	integer		not null	not droppable,
smin1	smallint		default null,
inte1	integer			default null,
lint1	largeint		default null,
nume1	numeric(9,3)		default null,
deci1	decimal(18,9)		default null,
pict1	pic s9(13)v9(5)		default null,
flot1	float (52)		default null,
dblp1	double precision	default null,
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *ERROR[1120]*
    ##expect any *ERROR[1029]*
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table wm009
(
dblp1	double precision	default null,
seqno	integer		not null	not droppable,
smin1	smallint		default null,
inte1	integer			default null,
lint1	largeint		default null,
nume1	numeric(9,3)		default null,
deci1	decimal(18,9)		default null,
pict1	pic s9(13)v9(5)		default null,
flot1	float (52)		default null,
real1	real			default null,
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm010
(
date1	date		not null	not droppable,
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
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm011
(
time1	time			default null,
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
date1	date			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm012
(
tims1	timestamp	not null	not droppable,
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
date1	date			default null,
time1	time			default null,
intv1	interval year to month	default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm013
(
intv1	interval year to month	default null,
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
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
char1	char (12)		default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm014
(
char1	char (12)	not null	not droppable,
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
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- SQL operation failed with errors.*
    stmt = """create volatile table wm015
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
date1	date			default null,
time1	time			default null,
tims1	timestamp		default null,
intv1	interval year to month	default null,
char1	char (12)		default null,
primary key (seqno, inte1, nume1, pict1, real1, date1, tims1, char1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    # TRAF: TRAF does not have the restriction of not allowing flat datatype
    # in partitioning key anymore.
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    stmt = """insert into WM000 values
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00',
timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM001 values
(2, 1, 1, 1, 1, 1, 1, 1, 1, 1, date'1999-12-31', time'00:00:00',
timestamp'1999-01-01 00:00:00.000000', interval'99-02' year to month, '1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM002 (inte1, seqno) values (12345, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM003
values
(
-923720368547588,
4,
-32768,
-2147483648,
-99999.999,
-999999.99999999,
-9999999.99999,
7.000000000001,
-2.2250738585072014,
-1.17549435e-38,
date'2006-06-15',
time'17:55:45',
timestamp'2006-06-23 17:56:59.300439',
interval'06-06'year to month,
'1'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM004 values
(
999999.999,
5,
32767,
2147483647,
923720368547587,
9999999.999999999,
99999999.99999,
6.000001,
4509.000000001,
3.40282347e+38,
date'2005-07-24',
time'07:35:54',
timestamp'2005-12-24 09:21:11.234039',
interval'06-07'year to month,
'12'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM005 values
(
8769.1200454,
6,
7892,
293847923,
9809876586,
23990.78,
786.12598,
11897.9998877656,
898889.00000997,
555.23,
date'2000-04-12',
time'00:21:30',
timestamp'1999-01-01 02:11:33.100439',
interval'06-11' year to month,
'123'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM006 values
(
506.55209,
7,
2834,
450,
4545990,
831.44553,
486.929,
99.082007,
10.39e-1,
308.87333e+2,
date'2005-10-20',
time'13:49:58',
timestamp'2005-11-12 19:30:12.500993',
interval'01-01'year to month,
'1234'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *ERROR[4082]*
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into WM007 values
(
345.8879,
8,
123,
789,
99809,
12.333,
9897.8768688,
12434.111,
-1.2250E-2,
0.834673734574,
date'2006-06-14',
time'05:55:55',
timestamp'2005-06-23 06:44:21.000000',
interval'99-03'year to month,
'12345'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *ERROR[4082]*
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into WM008 values
(9, 2, 2, 2, 2, 2, 2, 2, 2, 2, date'2002-11-11', time'23:00:00',
timestamp'2000-09-23 09:03:51.459920', interval'21-01'year to month, '1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    ##expect any *ERROR[4082]*
    stmt = """insert into WM009 values
(10, 3, 3, 3, 3, 3, 3, 3, 3, 3, date'2003-12-12', time'13:13:12',
timestamp'2000-12-24 02:03:51.459920', interval'19-07'year to month, '3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM010 values
(
date'2002-03-01',
11,
24923,
9,
847201,
444.238,
669.02983487,
797.799,
-7.9098700456e-1,
0.11,
2.222197264,
time'23:59:59',
timestamp'1975-07-24 00:00:00.000000',
interval'96-07'year to month,
'54321'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM011 values
(
time'10:55:45',
12,
108,
925,
61524,
308.274,
51293.5553,
405.0001,
0.128349234,
0.0008745245,
100,
date'1976-04-12',
timestamp'2001-06-23 17:56:59.300439',
interval'01-03'year to month,
'4321'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM012 values
(
timestamp'2000-06-23 17:56:59.300439',
13,
25065,
2149,
510233,
763.463,
137,
158.687000,
3.91287280941999936E-002,
8.31499980762600960E-001,
3.11221269804000000E+002,
date'2006-06-15',
time'17:55:45',
interval'00-06'year to month,
'321'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM013 values
(
interval'09-10'year to month,
14,
5058,
1074,
25116,
59962.443,
381.7314925,
338.231835,
1.95643640470999968E+001,
4.61149992608438720E+02,
5.00000204380000128E+001,
date'1999-06-30',
time'17:55:45',
timestamp'1992-06-23 17:56:59.300439',
'21'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM014 values
(
'12',
15,
9058,
2074,
67916,
95962.443,
831.7314925,
988.231835,
195.643640470999968E+001,
1.61149992608438720E+02,
9.00000204380000128E+001,
date'2001-06-30',
time'19:55:45',
timestamp'1972-06-23 17:56:59.300439',
interval'12-10'year to month
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    ##expect any *--- 1 row(s) inserted.*
    stmt = """insert into WM015 values
(
16,
9058,
2074,
67916,
95962.443,
831.7314925,
988.231835,
195.643640470999968E+001,
1.61149992608438720E+02,
9.00000204380000128E+001,
date'2001-06-30',
time'19:55:45',
timestamp'1972-06-23 17:56:59.300439',
interval'12-10' year to month,
'12'
);"""
    output = _dci.cmdexec(stmt)
    # TRAF: TRAF does not have the restriction of not allowing flat datatype
    # in partitioning key anymore.
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    elif hpdci.tgtTR():
        _dci.expect_inserted_msg(output, 1)
 
    stmt = """select	count (*)
from	wm000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a000')
    
    stmt = """select	count (*)
from	wm001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a001')
    
    stmt = """select	count (*)
from	wm002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a002')
    
    stmt = """select	count (*)
from	wm003;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a003')
    
    stmt = """select	count (*)
from	wm004;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a004')
    
    stmt = """select	count (*)
from	wm005;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a005')
    
    stmt = """select	count (*)
from	wm006;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a006')
    
    ##expect any *ERROR[4082]*
    stmt = """select	count (*)
from	wm007;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a007')
    
    ##expect any *ERROR[4082]*
    stmt = """select	count (*)
from	wm008;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a008')
    
    ##expect any *ERROR[4082]*
    stmt = """select	count (*)
from	wm009;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a009')
    
    stmt = """select	count (*)
from	wm010;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a010')
    
    stmt = """select	count (*)
from	wm011;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a011')
    
    stmt = """select	count (*)
from	wm012;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a012')
    
    stmt = """select	count (*)
from	wm013;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a013')
    
    stmt = """select	count (*)
from	wm014;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a014')
    
    ##expectfile ${test_dir}/a00exp a015
    stmt = """select	count (*)
from	wm015;"""
    output = _dci.cmdexec(stmt)
    # TRAF: TRAF does not have the restriction of not allowing flat datatype
    # in partitioning key anymore.
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '4082')
    elif hpdci.tgtTR():
        _dci.expect_selected_msg(output, 1)

    stmt = """select	a.inte1,
b.date1
from	wm000 a FULL OUTER JOIN wm014 b
on a.seqno = b.seqno
order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a00exp""", 'a016')
    
    _testmgr.testcase_end(desc)

