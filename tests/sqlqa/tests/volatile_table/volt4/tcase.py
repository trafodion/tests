# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

# To test if clustering key is automatically forced with options
# NOT NULL & NOT DROPPABLE when it is not explicitly specified
#
#      Example:
#              create table a
#              (
#              	i 	int,
#              	j	int,
#		primary key (i)
#		);
#
#		should get transformed to
#
#		create table a
#		(
#			i 	int 	NOT NULL NOT DROPPABLE,
#			j	int,
#		primary key (i)
#		);

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
    
    stmt = """create volatile table wm000
(
seqno	smallint		default null,
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
primary key (smin1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm001
(
seqno	smallint		default null,
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
primary key (inte1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm002
(
seqno	smallint		default null,
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
primary key (lint1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm003
(
seqno	smallint		default null,
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
primary key (nume1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm004
(
seqno	smallint		default null,
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
primary key (deci1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm005
(
seqno	smallint		default null,
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
primary key (pict1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm006
(
seqno	smallint		default null,
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
primary key (flot1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
 
    stmt = """create volatile table wm007
(
seqno	smallint		default null,
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
primary key (flot1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm008
(
seqno	smallint		default null,
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
primary key (real1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm009
(
seqno	smallint		default null,
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
primary key (dblp1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm010
(
seqno	smallint		default null,
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
primary key (date1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm011
(
seqno	smallint		default null,
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
primary key (time1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm012
(
seqno	smallint		default null,
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
primary key (tims1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm013
(
seqno	smallint		default null,
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
primary key (intv1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm014
(
seqno	smallint		default null,
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
primary key (char1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm015
(
seqno	smallint		default null,
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
primary key (smin1, inte1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm016
(
seqno	smallint		default null,
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
primary key (lint1, nume1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm017
(
seqno	smallint		default null,
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
primary key (deci1, pict1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm018
(
seqno	smallint		default null,
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
primary key (flot1, real1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm019
(
seqno	smallint		default null,
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
primary key (dblp1, date1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm020
(
seqno	smallint		default null,
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
primary key (time1, tims1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table wm021
(
seqno	smallint		default null,
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
primary key (intv1, char1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile index smin_idx on wm000(smin1) attributes extent 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- SQL operation failed with errors.*
    stmt = """create view wm_vw_000 as select seqno, smin1, lint1, deci1, flot1, dblp1, time1, intv1 from wm000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4082')
    
    stmt = """insert into WM000 values
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, date'2000-01-01', time'00:00:00',
timestamp'2000-06-23 01:01:01.000000', interval'01-01'year to month, '0');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values
(2, 1, 1, 1, 1, 1, 1, 1, 1, 1, date'1999-12-31', time'00:00:00',
timestamp'1999-01-01 00:00:00.000000', interval'99-02'year to month, '1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 (seqno, intv1, char1) values (3, interval'01-02'year to month, '9090909');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date'2006-06-15',    
time'17:55:45',    
timestamp'2006-06-23 17:56:59.300439',    
interval'06-06'year to month,    
'1' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '2005-07-24',    
time '07:35:54',    
timestamp '2005-12-24 09:21:11.234039',    
interval '06-07'year to month,    
'12' );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '2000-04-12',    
time '00:21:30',    
timestamp '1999-01-01 02:11:33.100439',    
interval '06-11'year to month,    
'123');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '2005-10-20',    
time '13:49:58',    
timestamp '2005-11-12 19:30:12.500993',    
interval '01-01'year to month,    
'1234');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '2006-06-14',    
time '05:55:55',    
timestamp '2005-06-23 06:44:21.000000',    
interval '99-03'year to month,    
'12345');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values
(9, 2, 2, 2, 2, 2, 2, 2, 2, 2, date '2002-11-11', time '23:00:00',
timestamp '2000-09-23 09:03:51.459920', interval '21-01'year to month, '1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values
(10, 3, 3, 3, 3, 3, 3, 3, 3, 3, date '2003-12-12', time '13:13:12',
timestamp '2000-12-24 02:03:51.459920', interval '19-07'year to month, '3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '2002-03-01',    
time '23:59:59',    
timestamp '1975-07-24 00:00:00.000000',    
interval '96-07'year to month,    
'54321');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '1976-04-12',    
time '10:55:45',    
timestamp '2001-06-23 17:56:59.300439',    
interval '01-03'year to month,    
'4321');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '2006-06-15',    
time '17:55:45',    
timestamp '2000-06-23 17:56:59.300439',    
interval '00-06'year to month,    
'321');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into WM000 values (
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
date '1999-06-30',    
time '17:55:45',    
timestamp '1992-06-23 17:56:59.300439',    
interval '09-10'year to month,    
'21');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*) from wm000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '14')
    
    stmt = """select count(*) from wm000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, '14')
    
    stmt = """create volatile table WM022
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (smin1, smin2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM001
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (smin1, smin2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM002
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (inte1, inte2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *--- SQL operation complete.*
    stmt = """create volatile table NWM003
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (lint1, flot1, real1, dblp1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM004
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (nume2, nume1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM005
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (deci2, deci1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM006
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (pict1, pict2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM007
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (char1, vchr1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM008
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (char2, vchr2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM009
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (date1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM010
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (time1, tims1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM011
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (time2, tims2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM012
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv00)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM013
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv01)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM014
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv02)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM015
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv03)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM016
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv04)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM017
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv05)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM018
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv06)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM019
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv07)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM020
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv08)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM021
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv09)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM022
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv10)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM023
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv11)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM024
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv12)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM025
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv13)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM026
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv14)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM027
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv15)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM028
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv16)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM029
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv17)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM030
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv18)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """create table NWM001
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint        not null        not droppable,
smin2   smallint unsigned  not null     not droppable,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (smin1, smin2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM002
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer         not null        not droppable,
inte2   integer unsigned not null       not droppable,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (inte1, inte2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM003
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint        not null        not droppable,   

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)      not null        not droppable,    

real1   real            not null        not droppable,    

dblp1   double precision  not null      not droppable,   

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (lint1, flot1, real1, dblp1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1120')
        _dci.expect_error_msg(output, '1029')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)
    
    stmt = """create table NWM004
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3) not null           not droppable,
nume2   numeric(9,3) unsigned  not null not droppable,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (nume2, nume1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM005
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9) not null          not droppable,
deci2   decimal (5,0) unsigned not null not droppable,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (deci2, deci1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM006
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5) not null        not droppable,
pict2   pic s9(13)v9(5) comp not null   not droppable,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (pict1, pict2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM007
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12) not null              not droppable,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12) not null           not droppable,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (char1, vchr1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM008
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
not null not droppable,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
not null not droppable,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (char2, vchr2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM009
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date        not null            not droppable,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (date1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM010
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time     not null               not droppable,
time2   time(5)                         default null,    

tims1   timestamp not null               not droppable,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (time1, tims1)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM011
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5) not null                not droppable,    

tims1   timestamp                       default null,
tims2   timestamp(3) not null           not droppable,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (time2, tims2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM012
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year    not null       not droppable,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv00)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM013
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year  not null not droppable,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv01)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM014
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month not null not droppable,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv02)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM015
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month  not null        not droppable,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv03)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM016
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month not null not droppable,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv04)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM017
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day   not null         not droppable,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv05)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM018
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day not null not droppable,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv06)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM019
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour not null not droppable,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv07)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM020
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute not null not droppable,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv08)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM021
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second not null not droppable,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv09)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM022
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour  not null         not droppable,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv10)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM023
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour not null not droppable,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv11)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM024
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute not null not droppable,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv12)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM025
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second not null not droppable,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv13)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM026
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute    not null     not droppable,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv14)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM027
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute not null not droppable,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv15)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM028
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second not null not droppable,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (intv16)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM029
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second  not null       not droppable,
intv18  interval second (6) to second   default null,    

primary key (intv17)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM030
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second not null not droppable,    

primary key (intv18)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
   
    # should see error, object already exists. 
    stmt = """create table NWM001
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (smin1, smin2)
) max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """create volatile table NWM031
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (smin1, inte2)
) no partition
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table NWM031
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint        not null        not droppable,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned not null       not droppable,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (smin1, inte2)
) no partition
max table size 256;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create volatile table NWM032
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint                        default null,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (lint1)
)
range partition by (lint1)
(
add first key 1    location """ + gvars.g_disc7 + """ name Rng_1,
add first key 1000 location """ + gvars.g_disc8 + """ name Rng_2,
add first key 2908 location """ + gvars.g_disc9 + """ name Rng_3
)
max table size 256;"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output, '1199')
 
    stmt = """create table NWM032
(
seqno   integer         not null        not droppable,
grpid   integer         not null        not droppable,    

smin1   smallint                        default null,
smin2   smallint unsigned               default null,    

inte1   integer                         default null,
inte2   integer unsigned                default null,    

lint1   largeint  not null              not droppable,    

nume1   numeric(9,3)                    default null,
nume2   numeric(9,3) unsigned           default null,    

deci1   decimal(18,9)                   default null,
deci2   decimal (5,0) unsigned          default null,    

pict1   pic s9(13)v9(5)                 default null,
pict2   pic s9(13)v9(5) comp            default null,    

flot1   float (36)                      default null,    

real1   real                            default null,    

dblp1   double precision                default null,    

char1   char (12)                       default null,
char2   char (12)                       character set ucs2
default null,    

vchr1   varchar (12)                    default null,
vchr2   varchar (12)                    character set ucs2
default null,    

date1   date                            default null,    

time1   time                            default null,
time2   time(5)                         default null,    

tims1   timestamp                       default null,
tims2   timestamp(3)                    default null,    

intv00  interval year                   default null,
intv01  interval year (18) to year      default null,
intv02  interval year (16) to month     default null,    

intv03  interval month                  default null,
intv04  interval month (15) to month    default null,    

intv05  interval day                    default null,
intv06  interval day (14) to day        default null,
intv07  interval day (13) to hour       default null,
intv08  interval day (12) to minute     default null,
intv09  interval day (7) to second      default null,    

intv10  interval hour                   default null,
intv11  interval hour (11) to hour      default null,
intv12  interval hour (9) to minute     default null,
intv13  interval hour (8) to second     default null,    

intv14  interval minute                 default null,
intv15  interval minute (7) to minute   default null,
intv16  interval minute to second       default null,
intv17  interval second                 default null,
intv18  interval second (6) to second   default null,    

primary key (lint1)
)
range partition by (lint1)
(
add first key 1    location """ + gvars.g_disc7 + """ name Rng_1,
add first key 1000 location """ + gvars.g_disc8 + """ name Rng_2,
add first key 2908 location """ + gvars.g_disc9 + """ name Rng_3
);"""
    output = _dci.cmdexec(stmt)
    if hpdci.tgtSQ():
        _dci.expect_complete_msg(output)
    elif hpdci.tgtTR():
        _dci.expect_error_msg(output, '1199')
    
    _testmgr.testcase_end(desc)

