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
    # set up: create the tables and load the data for the extract tests
    
    # testA01
    stmt = """create table extr01 (
dt date,
tm time,
ts timestamp
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwextr01 
as select * from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into extr01 values (
date '1997-02-27',
time '10:30:54',
timestamp '1997-02-27:10:30:54.123'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr01 values (
date '1999-12-31',
null,
timestamp '1999-12-31:23:59:59.999999'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr01 values (
date '2000-01-01',
time '00:00:00',
timestamp '2000-01-01:00:00:00.00'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA02
    stmt = """create table extr02 (
iy INTERVAL YEAR,
iym INTERVAL YEAR TO MONTH,
im INTERVAL MONTH,
id INTERVAL DAY
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwextr02 
as select * from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into extr02 values (
INTERVAL '97' YEAR,
INTERVAL '97-02' YEAR TO MONTH,
INTERVAL '22' MONTH,
INTERVAL '27' DAY
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr02 values (
INTERVAL '00' YEAR,
INTERVAL '00-01' YEAR TO MONTH,
INTERVAL '01' MONTH,
INTERVAL '01' DAY
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr02 values (
INTERVAL '99' YEAR,
INTERVAL '05-10' YEAR TO MONTH,
INTERVAL '12' MONTH,
INTERVAL '31' DAY
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #     INTERVAL '99-12' YEAR TO MONTH,	XXXXXX crashes on \lilith
    
    # testA03
    stmt = """create table extr03 (
idh INTERVAL DAY TO HOUR,
idm INTERVAL DAY TO MINUTE,
ids INTERVAL DAY TO SECOND
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwextr03 as
select * from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into extr03 values (
INTERVAL '13:23' DAY TO HOUR,
INTERVAL '15:12:30' DAY TO MINUTE,
INTERVAL '25:01:45:09.00' DAY TO SECOND
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr03 values (
INTERVAL '01:01' DAY TO HOUR,
INTERVAL '31:23:59' DAY TO MINUTE,
INTERVAL '13:11:05:59.999999' DAY TO SECOND
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr03 values (
null,
INTERVAL '00:00:00' DAY TO MINUTE,
INTERVAL '00:00:00:00.0000' DAY TO SECOND
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA04
    stmt = """create table extr04 (
ih INTERVAL HOUR,
ihm INTERVAL HOUR TO MINUTE,
ihs INTERVAL HOUR TO SECOND
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwextr04 as
select * from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into extr04 values (
INTERVAL '48' HOUR,
null,
INTERVAL '23:59:59' HOUR TO SECOND
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr04 values (
INTERVAL '00' HOUR,
INTERVAL '00:00' HOUR TO MINUTE,
INTERVAL '00:00:00' HOUR TO SECOND
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr04 values (
INTERVAL '19' HOUR,
INTERVAL '01:19' HOUR TO MINUTE,
INTERVAL '17:55:07' HOUR TO SECOND
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # testA05
    stmt = """create table extr05 (
im  INTERVAL MINUTE,
ims INTERVAL MINUTE TO SECOND,
isec  INTERVAL SECOND
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create view vwextr05 as
select * from extr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into extr05 values (
INTERVAL '99' MINUTE,
INTERVAL '00:00' MINUTE TO SECOND,
null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """insert into extr05 values (
INTERVAL '99' MINUTE,
INTERVAL '59:59' MINUTE TO SECOND,
null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    #     INTERVAL '59.999' SECOND		XXXXXX crashes
    
    stmt = """insert into extr05 values (
INTERVAL '30' MINUTE,
INTERVAL '18:27' MINUTE TO SECOND,
null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA01
    # johnc
    # 1997-02-27
    # EXTRACT tests:  DATE, TIME, and TIMESTAMP data types
    # contents:
    # 	1. check the table data
    # 	2. simple extract of table datetime elements
    # 	3. check the view data
    # 	4. simple extract of view datetime elements
    #
    #
    #  1. check the table data
    
    stmt = """select * from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #  expect 3 rows with the following values:
    #  	DT          TM        TS
    #  	----------  --------  --------------------------
    #
    #     1997-02-27  10:30:54  1997-02-27 10:30:54.123000
    #     1999-12-31         ?  1999-12-31 23:59:59.999999
    #     2000-01-01  00:00:00  2000-01-01 00:00:00.000000
    
    # -----------------------------------------------
    
    #  2. simple extract of table datetime elements
    stmt = """select extract (year from dt)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #  expect 3 rows with the following values:
    #       1997
    #       1999
    #       2000
    
    stmt = """select extract (month from dt)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #  expect 3 rows with the following values:
    #          2
    #         12
    #          1
    
    stmt = """select extract (day from dt)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #  expect 3 rows with the following values:
    #         27
    #         31
    #          1
    
    stmt = """select extract (hour from tm)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #  expect 3 rows with the following values:
    #         10
    #          ?
    #          0
    
    stmt = """select extract (minute from tm)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #  expect 3 rows with the following values:
    #         30
    #          ?
    #          0
    
    stmt = """select extract (second from tm)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #  expect 3 rows with the following values:
    #         54
    #          ?
    #          0
    
    stmt = """select extract (year from ts)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    #  expect 3 rows with the following values:
    #       1997
    #       1999
    #       2000
    
    stmt = """select extract (month from ts)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #  expect 3 rows with the following values:
    #          2
    #         12
    #          1
    
    stmt = """select extract (day from ts)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #  expect 3 rows with the following values:
    #         27
    #         31
    #          1
    
    stmt = """select extract (hour from ts)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #  expect 3 rows with the following values:
    #         10
    #         23
    #          0
    
    stmt = """select extract (minute from ts)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    #  expect 3 rows with the following values:
    #         30
    #         59
    #          0
    
    stmt = """select extract (second from ts)
from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    #  expect 3 rows with the following values:
    #       54.123000
    #       59.999999
    #        0.000000
    #
    #
    #  3. check the view data
    
    stmt = """select * from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s13')
    #     expect 3 rows with the following values:
    #     DT          TM        TS
    #     ----------  --------  --------------------------
    #
    #     1997-02-27  10:30:54  1997-02-27 10:30:54.123000
    #     1999-12-31         ?  1999-12-31 23:59:59.999999
    #     2000-01-01  00:00:00  2000-01-01 00:00:00.000000
    
    # -----------------------------------------------
    
    #  4. simple extract of view datetime elements
    stmt = """select extract (year from dt)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s14')
    #  expect 3 rows with the following values:
    #       1997
    #       1999
    #       2000
    
    stmt = """select extract (month from dt)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s15')
    #  expect 3 rows with the following values:
    #          2
    #         12
    #          1
    
    stmt = """select extract (day from dt)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s16')
    #  expect 3 rows with the following values:
    #         27
    #         31
    #          1
    
    stmt = """select extract (hour from tm)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s17')
    #  expect 3 rows with the following values:
    #         10
    #          ?
    #          0
    
    stmt = """select extract (minute from tm)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s18')
    #  expect 3 rows with the following values:
    #         30
    #          ?
    #          0
    
    stmt = """select extract (second from tm)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s19')
    #  expect 3 rows with the following values:
    #         54
    #          ?
    #          0
    
    stmt = """select extract (year from ts)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s20')
    #  expect 3 rows with the following values:
    #       1997
    #       1999
    #       2000
    
    stmt = """select extract (month from ts)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s21')
    #  expect 3 rows with the following values:
    #          2
    #         12
    #          1
    
    stmt = """select extract (day from ts)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s22')
    #  expect 3 rows with the following values:
    #         27
    #         31
    #          1
    
    stmt = """select extract (hour from ts)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s23')
    #  expect 3 rows with the following values:
    #         10
    #         23
    #          0
    
    stmt = """select extract (minute from ts)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s24')
    #  expect 3 rows with the following values:
    #         30
    #         59
    #          0
    
    stmt = """select extract (second from ts)
from vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s25')
    
    _testmgr.testcase_end(desc)

def test003(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA02
    # johnc
    # 1997-02-27
    # EXTRACT tests:  INTERVAL YEAR, INTERVAL YEAR TO MONTH,
    #		   INTERVAL MONTH, and INTERVAL DAY data types
    # contents:
    # 	 1. check the table data
    # 	 2. simple extract of the table interval elements
    # 	 3. check the view data
    # 	 4. simple extract of the view interval elements
    #
    #
    #  1. check the table data
    
    stmt = """select * from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #  expect 3 rows with the following values:
    #  	IY   IYM     IM   ID
    #  	---  ------  ---  ---
    #  	 97   97-02   22   27
    #  	  0    0-01    1    1
    #  	 99    5-10   12   31
    
    #
    #  2. simple extract of the table interval elements
    stmt = """select extract (year from iy)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  expect 3 rows with the following values:
    #         97
    #          0
    #         99
    
    stmt = """select extract (year from iym)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    #  expect 3 rows with the following values:
    #         97
    #          0
    #          5
    
    stmt = """select extract (month from iym)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #  expect 3 rows with the following values:
    #          2
    #          1
    #         10
    
    stmt = """select extract (month from im)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #  expect 3 rows with the following values:
    #         22
    #          1
    #         12
    
    stmt = """select extract (day from id)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #  expect 3 rows with the following values:
    #         27
    #          1
    #         31
    #
    #
    #  3. check the view data
    #
    stmt = """select * from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #  expect 3 rows with the following values:
    #  	IY   IYM     IM   ID
    #  	---  ------  ---  ---
    #  	 97   97-02   22   27
    #  	  0    0-01    1    1
    #  	 99    5-10   12   31
    #
    #
    #  4. simple extract of the view interval elements
    #
    stmt = """select extract (year from iy)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    #  expect 3 rows with the following values:
    #         97
    #          0
    #         99
    
    stmt = """select extract (year from iym)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    #  expect 3 rows with the following values:
    #         97
    #          0
    #          5
    
    stmt = """select extract (month from iym)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #  expect 3 rows with the following values:
    #          2
    #          1
    #         10
    
    stmt = """select extract (month from im)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    #  expect 3 rows with the following values:
    #         22
    #          1
    #         12
    
    stmt = """select extract (day from id)
from vwextr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s11')
    
    _testmgr.testcase_end(desc)

def test004(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA03
    # johnc
    # 1997-02-27
    # EXTRACT tests: INTERVAL DAY TO HOUR, INTERVAL DAY TO MINUTE,
    #		  INTERVAL DAY TO SECOND data types
    # contents:
    # 	1. check the table data
    # 	2. simple extract of the table interval elements
    # 	3. check the view data
    # 	4. simple extract of the view interval elements
    #
    #
    #  1. check the table data
    #
    
    stmt = """select * from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #  expect 3 rows with the following values:
    #  	IDH     IDM        IDS
    #  	------  ---------  -------------------
    #  	 13 23   15 12:30   25 01:45:09
    #  	  1 01   31 23:59    0 00:00:01
    #  	     ?    0 00:00   13 11:05:59.999999
    #
    #
    #  2. simple extract of the table interval elements
    #
    stmt = """select extract (day from idh)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #  expect 3 rows with the following values:
    #         13
    #          1
    #          ?
    
    stmt = """select extract (hour from idh)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  expect 3 rows with the following values:
    #         23
    #          1
    #          ?
    
    stmt = """select extract (day from idm)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    #  expect 3 rows with the following values:
    #         15
    #         31
    #          0
    
    stmt = """select extract (hour from idm)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    #  expect 3 rows with the following values:
    #         12
    #         23
    #          0
    
    stmt = """select extract (minute from idm)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    #  expect 3 rows with the following values:
    #         30
    #         59
    #          0
    
    stmt = """select extract (day from ids)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #  expect 3 rows with the following values:
    #         25
    #          0
    #         13
    
    stmt = """select extract (hour from ids)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s7')
    #  expect 3 rows with the following values:
    #          1
    #          0
    #         11
    
    stmt = """select extract (minute from ids)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s8')
    #  expect 3 rows with the following values:
    #         45
    #          0
    #          5
    
    stmt = """select extract (second from ids)
from extr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s9')
    #  expect 3 rows with the following values:
    #          9
    #          1
    #         59.999999
    #
    #
    #  3. check the view data
    #
    stmt = """select * from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #  expect 3 rows with the following values:
    #  	IDH     IDM        IDS
    #  	------  ---------  -------------------
    #  	 13 23   15 12:30   25 01:45:09
    #  	  1 01   31 23:59    0 00:00:01
    #  	     ?    0 00:00   13 11:05:59.999999
    #
    #
    #  4. simple extract of the view interval elements
    #
    stmt = """select extract (day from idh)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s11')
    #  expect 3 rows with the following values:
    #         13
    #          1
    #          ?
    
    stmt = """select extract (hour from idh)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s12')
    #  expect 3 rows with the following values:
    #         23
    #          1
    #          ?
    
    stmt = """select extract (day from idm)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s13')
    #  expect 3 rows with the following values:
    #         15
    #         31
    #          0
    
    stmt = """select extract (hour from idm)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s14')
    #  expect 3 rows with the following values:
    #         12
    #         23
    #          0
    
    stmt = """select extract (minute from idm)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s15')
    #  expect 3 rows with the following values:
    #         30
    #         59
    #          0
    
    stmt = """select extract (day from ids)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s16')
    #  expect 3 rows with the following values:
    #         25
    #          0
    #         13
    
    stmt = """select extract (hour from ids)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s17')
    #  expect 3 rows with the following values:
    #          1
    #          0
    #         11
    
    stmt = """select extract (minute from ids)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s18')
    #  expect 3 rows with the following values:
    #         45
    #          0
    #          5
    
    stmt = """select extract (second from ids)
from vwextr03;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s19')
    
    _testmgr.testcase_end(desc)

def test005(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA04
    # johnc
    # 1997-02-27
    # EXTRACT tests:  INTERVAL HOUR, INTERVAL HOUR TO MINUTE
    #		   and INTERVAL HOUR TO SECOND data types
    # contents:
    # 	1. check the table data
    # 	2. simple extract of the table interval elements
    # 	3. check the view data
    # 	4. simple extract of the view interval elements
    #
    #
    #  1. check the table data
    #
    
    stmt = """select * from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    #  expect 3 rows with the following values:
    #  	IH   IHM     IHS
    #  	---  ------  ----------------
    #  	 48       ?   23:59:59.999999
    #  	  0    0:00    0:00:00
    #  	 19    1:19   17:55:07.333000
    #
    #
    #  2. simple extract of the table interval elements
    #
    stmt = """select extract (hour from ih)
from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #  expect 3 rows with the following values:
    #         48
    #          0
    #         19
    
    stmt = """select extract (hour from ihm)
from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    #  expect 3 rows with the following values:
    #          ?
    #          0
    #          1
    
    stmt = """select extract (minute from ihm)
from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    #  expect 3 rows with the following values:
    #          ?
    #          0
    #         19
    
    stmt = """select extract (hour from ihs)
from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #  expect 3 rows with the following values:
    #         23
    #          0
    #         17
    
    stmt = """select extract (minute from ihs)
from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    #  expect 3 rows with the following values:
    #         59
    #          0
    #         55
    
    stmt = """select extract (second from ihs)
from extr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #  expect 3 rows with the following values:
    #         59.999999
    #          0
    #          7.333000
    #
    #
    #  1. check the view data
    #
    stmt = """select * from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #  expect 3 rows with the following values:
    #  	IH   IHM     IHS
    #  	---  ------  ----------------
    #  	 48       ?   23:59:59.999999
    #  	  0    0:00    0:00:00
    #  	 19    1:19   17:55:07.333000
    #
    #
    #  2. simple extract of the view interval elements
    #
    stmt = """select extract (hour from ih)
from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    #  expect 3 rows with the following values:
    #         48
    #          0
    #         19
    
    stmt = """select extract (hour from ihm)
from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s9')
    #  expect 3 rows with the following values:
    #          ?
    #          0
    #          1
    
    stmt = """select extract (minute from ihm)
from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s10')
    #  expect 3 rows with the following values:
    #          ?
    #          0
    #         19
    
    stmt = """select extract (hour from ihs)
from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s11')
    #  expect 3 rows with the following values:
    #         23
    #          0
    #         17
    
    stmt = """select extract (minute from ihs)
from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s12')
    #  expect 3 rows with the following values:
    #         59
    #          0
    #         55
    
    stmt = """select extract (second from ihs)
from vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s13')
    
    _testmgr.testcase_end(desc)

def test006(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA05
    # johnc
    # 1997-02-27
    # EXTRACT tests: INTERVAL MINUTE, INTERVAL MINUTE TO SECOND
    #                and INTERVAL SECOND data types
    
    # contents:
    # 	1. check the table data
    # 	2. simple extract of the table interval elements
    # 	3. check the view data
    # 	4. simple extract of the view interval elements
    #
    #
    #  1. check the table data
    #
    
    stmt = """select * from extr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #  expect 3 rows with the following values:
    #
    #
    #  2. simple extract of the table interval elements
    #
    stmt = """select extract (minute from im)
from extr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #  expect 3 rows with the following values:
    
    stmt = """select extract (minute from ims)
from extr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #  expect 3 rows with the following values:
    
    stmt = """select extract (second from ims)
from extr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #  expect 3 rows with the following values:
    
    stmt = """select extract (second from isec)
from extr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    
    _testmgr.testcase_end(desc)

def test007(desc="""a06"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA06
    # johnc
    # 1997-02-27
    # EXTRACT tests:  arithmetic operators with EXTRACT on
    #                 INTERVAL YEAR, INTERVAL YEAR TO MONTH,
    #                 INTERVAL MONTH, and INTERVAL DAY data types
    # uses table extr02 which was built for testA02
    # contents:
    #       1. insert an extra row & check the table data
    #       2. extract + extract of the table interval elements
    #       3. extract of the table interval elements + integer
    #       4. extract - extract of the table interval elements
    #       5. extract of the table interval elements - integer
    #       6. extract / extract of the table interval elements
    #       7. extract of the table interval elements / integer
    #       8. extract * extract of the table interval elements
    #       9. extract of the table interval elements * integer
    #	10. extract / extract where 2nd extract is zero
    #
    #
    # 1. insert an extra row with some NULLS & check the table data
    
    stmt = """insert into extr02 values (
null,
null,
null,
INTERVAL '99' DAY
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #  expect 4 rows with the following values:
    #  IY   IYM     IM   ID
    #  ---  ------  ---  ---
    #
    #   97   97-02   22   27
    #    0    0-01    1    1
    #   99    5-10   12   31
    #    ?       ?    ?   99
    
    #  2. extract + extract of the table interval elements
    #
    stmt = """select extract (year from iy) + extract (month from im)
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #     119
    #       1
    #     111
    #       ?
    
    #  3. extract of the table interval elements + integer
    stmt = """select extract (year from iy) + 123
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #     220
    #     123
    #     222
    #       ?
    
    #  4. extract - extract of the table interval elements
    stmt = """select extract (year from iy) - extract (month from im)
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #      75
    #      -1
    #      87
    #       ?
    
    #  5. extract of the table interval elements - integer
    stmt = """select extract (year from iy) - 33
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #      64
    #     -33
    #      66
    #       ?
    
    #  6. extract / extract of the table interval elements
    stmt = """select extract (year from iy) / extract (month from iym)
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #  	  48.50
    #  	   0.00
    #  	   9.90
    #             ?
    
    #  7. extract of the table interval elements / integer
    stmt = """select extract (year from iy) / 12
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #        8.08
    #        0.00
    #        8.25
    #           ?
    
    #  8. extract * extract of the table interval elements
    stmt = """select extract (year from iy) * extract (month from iym)
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #  	   194
    #  	     0
    #  	   990
    #           ?
    
    #  9. extract of the table interval elements * integer
    stmt = """select extract (year from iy) * 150
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    # -     from vwextr02;		XXXXXX crashes
    #  expect 4 rows with the following values:
    #           14550
    #               0
    #           14850
    #               ?
    
    #  10. extract / extract where 2nd extract is zero
    #  negative test: divide by zero
    ##expectfile ${test_dir}/a06exp a06s9
    stmt = """select extract (year from iy) / extract (year from iym)
from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8419')
    
    _testmgr.testcase_end(desc)

def test008(desc="""a07"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA07
    # johnc
    # 1997-02-28
    # EXTRACT tests:  EXTRACT in a where clause with = <> > >= < <= operators
    # contents:
    #       1. check the table data
    #       2. extract = extract in a where clause
    # 	 3. extract = integer in a where clause
    # 	 4. extract <> extract in a where clause
    # 	 5. extract <> integer in a where clause
    # 	 6. extract > extract in a where clause
    # 	 7. extract > integer in a where clause
    # 	 8. extract >= extract in a where clause
    # 	 9. extract >= integer in a where clause
    # 	10. extract < extract in a where clause
    # 	11. extract < integer in a where clause
    # 	12. extract <= extract in a where clause
    # 	13. extract <= integer in a where clause
    #
    #
    #  1. check the table data
    
    stmt = """select * from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    #  expect 4 rows with the following values:
    #  IY   IYM     IM   ID
    #  ---  ------  ---  ---
    #
    #   97   97-02   22   27
    #    0    0-01    1    1
    #   99    5-10   12   31
    #    ?       ?    ?   99
    #
    #
    #  2. extract = extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) = extract (year from iym);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    #  expect a count of 2
    
    #  3. extract = integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    #  expect a count of 1
    
    #  4. extract <> extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) <> extract (year from iym);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    #  expect a count of 1
    
    #  5. extract <> integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) <> 97;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    #  expect a count of 3
    
    #  6. extract > extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) > extract (day from id);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    #  expect a count of 2
    
    #  7. extract > integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) > 97;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #  expect a count of 1
    
    #  8. extract >= extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) >= extract (year from iym);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #  expect a count of 3
    
    #  9. extract >= integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) >= 97;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    #  expect a count of 2
    
    #  10. extract < extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) < extract (year from iym);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s9')
    #  expect a count of 0
    
    #  11. extract < integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) < 97;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s10')
    #  expect a count of 1
    
    #  12. extract <= extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) <= extract (year from iy);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s11')
    #  expect a count of 3
    
    #  13. extract <= integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) <= 97;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s12')
    
    _testmgr.testcase_end(desc)

def test009(desc="""a08"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA08
    # johnc
    # 1997-03-03
    # EXTRACT tests:  EXTRACT in a where clause with arithmetic operators
    # contents:
    #       1. check the table data
    #       2. extract - extract in a where clause
    #       3. extract - integer in a where clause
    #       4. extract + extract in a where clause
    #       5. extract + integer in a where clause
    #       6. extract / extract in a where clause
    #       7. extract / integer in a where clause
    #       8. extract * extract in a where clause
    #       9. extract * integer in a where clause
    #
    #
    #  1. check the table data
    
    stmt = """select * from extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    #  expect 4 rows with the following values:
    #  IY   IYM     IM   ID
    #  ---  ------  ---  ---
    #
    #   97   97-02   22   27
    #    0    0-01    1    1
    #   99    5-10   12   31
    #    ?       ?    ?   99
    #
    #
    #  2. extract - extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) - extract (year from iym) = 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    #  expect a count of 2
    
    #  3. extract - integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) - 97 = 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    #  expect a count of 1
    
    #  4. extract + extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) + extract (year from iym) > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    #  expect a count of 2
    
    #  5. extract + integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) + 3 > 100;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    #  expect a count of 1
    
    #  6. extract / extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) / extract (day from id) >= 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    #  expect a count of 2
    
    #  7. extract / integer in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) / 3 = 33;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #  expect a count of 1
    
    #  8. extract * extract in a where clause
    stmt = """select count(*) from extr02 
where extract (year from iy) * extract (year from iym) > 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #  expect a count of 2
    
    #  9. extract * integer in a where clause
    stmt = """select count(*) from extr02 
where extract (month from im) * 5 >= 0
and   extract (month from im) * 5 <= 60;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    _testmgr.testcase_end(desc)

def test010(desc="""a09"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA09
    # johnc
    # 1997-03-04
    # EXTRACT tests:  EXTRACT in a where clause with BETWEEN & NOT BETWEEN
    # contents:
    #       1. check the table data
    # 	 2. extract BETWEEN extract AND integer in a where clause
    # 	 3. extract NOT BETWEEN extract AND integer in a where clause
    #
    #
    #  1. check the table data
    
    stmt = """select * from extr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    #  expect 3 rows with the following values:
    #       DT          TM        TS
    #       ----------  --------  --------------------------
    #
    #     1997-02-27  10:30:54  1997-02-27 10:30:54.123000
    #     1999-12-31         ?  1999-12-31 23:59:59.999999
    #     2000-01-01  00:00:00  2000-01-01 00:00:00.000000
    
    # -----------------------------------------------
    #
    #  2. extract BETWEEN extract AND integer in a where clause
    stmt = """select count(*) from extr01 
where extract (year from dt) BETWEEN extract (year from ts)
AND 2000;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    #  expect a count of 3
    
    #  3. extract NOT BETWEEN extract AND integer in a where clause
    stmt = """select count(*) from extr01 
where extract (year from ts) NOT BETWEEN extract (year from dt)
AND 1999;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    
    _testmgr.testcase_end(desc)

def test011(desc="""a10"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # testA10
    # johnc
    # 1997-02-27
    # clean up for the EXTRACT tests
    #
    
    stmt = """drop view vwextr01;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table extr01 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view vwextr02 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table extr02;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view vwextr03 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table extr03 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view vwextr04;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table extr04 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop view vwextr05;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table extr05 cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

