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
    
def test001(desc="""set up for the timeprec datetime precision tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test000.sql
    # jclear
    # set up for the timeprec datetime precision tests
    #
    # test001
    
    stmt = """create table tdeflt (tm time) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tm0 (tm time (0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tm1 (tm time (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tm6 (tm time (6)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test002
    stmt = """create table tsdeflt (ts timestamp) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ts0 (ts timestamp (0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ts1 (ts timestamp (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table ts6 (ts timestamp (6)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test003
    stmt = """create table tyear (
ivdeflt     interval year,
iv1         interval year (1),
iv10        interval year (10),
ivmax       interval year (18)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test004
    stmt = """create table ydefmon 
(iv interval year to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table y1mon 
(iv interval year (1) to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table y16mon 
(iv interval year (16) to month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test005
    stmt = """create table tmon (
mdeflt interval month) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tmon1 (
m1 interval month (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tmon2 (
m2 interval month (2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tmon18 (
m18 interval month (18)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test006
    stmt = """create table tday (
iv interval day) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tday1 (
iv interval day (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tday2 (
iv interval day (2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tday18 (
iv interval day (18)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test007
    stmt = """create table ddefhr 
(iv interval day to hour) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table d1hr 
(iv interval day (1) to hour) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table d16hr 
(iv interval day (16) to hour) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test008
    stmt = """create table dmdef (
iv interval day to minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table dm1 (
iv interval day (1) to minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table d14m (
iv interval day (14) to minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test009
    stmt = """create table dsdef (
iv interval day to second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table d0s (
iv interval day to second (0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table d1s (
iv interval day (1) to second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table d7s (
iv interval day (7) to second (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test010
    stmt = """create table thour (
iv interval hour) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table thour1 (
iv interval hour (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table thour2 (
iv interval hour (5)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table thour18 (
iv interval hour (18)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test011
    stmt = """create table hmdef (
iv interval hour to minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table h1m (
iv interval hour (1) to minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table h16m (
iv interval hour (16) to minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test012
    stmt = """create table hsdef (
iv interval hour to second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table h0s (
iv interval hour to second (0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table h1s (
iv interval hour (1) to second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table h8s (
iv interval hour (8) to second (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test013
    stmt = """create table tmin (
iv interval minute) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tmin1 (
iv interval minute (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tmin2 (
iv interval minute (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tmin18 (
iv interval minute (18)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test014
    
    stmt = """create table msdef (
iv interval minute to second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table m0s (
iv interval minute to second (0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table m1s (
iv interval minute (1) to second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table m13s (
iv interval minute (13) to second (3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test015
    stmt = """create table tsec (
iv interval second) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tsec1 (
iv interval second (1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tsec12 (
iv interval second (12)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test016
    
    stmt = """create table tn0sec1 (
iv interval second (1, 0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tn0sec18 (
iv interval second (18, 0)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # test017
    
    stmt = """create table tsec13 (
iv interval second (1, 3)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tsec21 (
iv interval second (2, 1)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """create table tsec162 (
iv interval second (16, 2)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Test the precision of TIME datatypes with INSERT, UPDATE, & DELETE"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test001
    # jclear
    # 1997-03-25
    # test the precision of TIME datatypes with INSERT, UPDATE, & DELETE
    #
    
    stmt = """insert into tdeflt values (time '01:25:35 PM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tdeflt values (time '01:25:35');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tdeflt values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select tm from tdeflt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    # expect 3 rows with the following values:
    # 	13:25:35
    # 	01:25:35
    # 	       ?
    
    stmt = """insert into tm0 values (time '11:12:13');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm0 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm0 values (time '02:22:32 PM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm0 values (time '02:22:32');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select tm from tm0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    # expect 4 rows with the following values:
    # 	11:12:13
    # 	       ?
    # 	14:22:32
    # 	02:22:32
    
    stmt = """insert into tm1 values (time '14:15:16.7');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm1 values (time '05:15:45.9 pm');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm1 values (time '05:15:45.9 aM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select tm from tm1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    # expect 4 rows with the following values:
    # 	14:15:16.7
    # 	         ?
    # 	17:15:45.9
    # 	05:15:45.9
    
    stmt = """insert into tm6 values (time '01:02:03.456789 Pm');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm6 values (NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tm6 values (time '01:02:03.456789');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select tm from tm6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    # expect 3 rows with the following values:
    # 	13:02:03.456789
    # 	              ?
    # 	01:02:03.456789
    
    stmt = """UPDATE tdeflt set tm = time '01:25:35'
where tm = time '13:25:35';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tm0 set tm = time '02:22:32'
where tm = time '14:22:32';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tm1 set tm = time '05:15:45.9 am'
where tm = time '05:15:45.9 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tm6 set tm = time '01:02:03.456789 am'
where tm = time '01:02:03.456789 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tdeflt order by tm asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #  expect 3 rows with the following values in this order:
    #       01:25:35
    #       01:25:35
    #              ?
    
    stmt = """select * from tm0 order by tm desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    #  expect 4 rows with the following values in this order:
    #  	       ?
    #  	11:12:13
    #  	02:22:32
    #  	02:22:32
    
    stmt = """select * from tm1 order by tm;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s6')
    #  expect 4 rows with the following values in this order:
    #  	05:15:45.9
    #  	05:15:45.9
    #  	14:15:16.7
    #  	         ?
    
    stmt = """select * from tm6 order by tm;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    # expect 4 rows with the following values in this order:
    # 	01:02:03.456789
    # 	01:02:03.456789
    # 	              ?
    
    stmt = """DELETE from tdeflt where tm = time '01:25:35 AM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """DELETE from tm0 where tm is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from tm1 where tm = time '05:15:45.9 am'
or tm = time '02:15:16.7 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from tm6 where tm = time '01:02:03.456789 am';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select * from tdeflt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #  expect 1 row with a NULL
    
    stmt = """select * from tm0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    #  expect 1 row with a NULL
    
    stmt = """select * from tm1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    #  expect 1 row with a NULL
    
    stmt = """select * from tm6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Test the precision of TIMESTAMP datatypes with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  UPDATE, & DELETE
    # test002
    # test the precision of TIMESTAMP datatypes with INSERT, UPDATE, & DELETE
    # using Standard, US, and European formats
    #
    #
    
    stmt = """INSERT into tsdeflt values (timestamp '03/25/1997 01:25:35 PM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsdeflt values (timestamp '1997-03-25:01:25:35');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsdeflt values (NULL);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select ts from tsdeflt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    # expect 3 rows with the following values:
    # 	1997-03-25 13:25:35.000000
    # 	1997-03-25 01:25:35.000000
    # 	                         ?
    
    stmt = """INSERT into ts0 values (timestamp '2000-01-01:11:12:13');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts0 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts0 values (timestamp '12/31/1999 02:22:32 PM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts0 values (timestamp '1999-12-31:02:22:32');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select ts from ts0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    # expect 4 rows with the following values:
    # 	2000-01-01 11:12:13
    # 	                  ?
    # 	1999-12-31 14:22:32
    # 	1999-12-31 02:22:32
    
    stmt = """INSERT into ts1 values (timestamp '1995-12-29:14:15:16.7');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts1 values (timestamp '12/25/1997 05:15:45.9 pm');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts1 values (timestamp '12/25/1997 05:15:45.9 aM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select ts from ts1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    # expect 4 rows with the following values:
    # 	1995-12-29 14:15:16.7
    # 	                    ?
    # 	1997-12-25 17:15:45.9
    # 	1997-12-25 05:15:45.9
    
    stmt = """INSERT into ts6 values (timestamp '01/02/0003 04:05:06.123456 Pm');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts6 values (timestamp '0003-01-02:04:05:06.123456');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ts6 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select ts from ts6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    # expect 3 rows with the following values:
    # 	0003-01-02 16:05:06.123456
    # 	0003-01-02 04:05:06.123456
    # 	                         ?
    
    stmt = """UPDATE tsdeflt set ts = timestamp '1997-03-25:13:25:35'
where ts = timestamp '03/25/1997 01:25:35 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE ts0 set ts = ts - interval '1' day
where ts = timestamp '2000-01-01:11:12:13';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE ts1 set ts = timestamp '12/25/1997 05:15:45.9 Am'
where ts = timestamp '1997-12-25:17:15:45.9';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE ts6 set ts = timestamp '01/02/0003 04:05:06.123456 PM'
where ts = timestamp '0003-01-02:04:05:06.123456';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select ts from tsdeflt order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    #  expect 3 rows with the following values in this order:
    #  	1997-03-25 01:25:35.000000
    #  	1997-03-25 13:25:35.000000
    #     			         ?
    
    stmt = """select ts from ts0 order by ts asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    #  expect 4 rows with the following values in this order:
    #     1999-12-31 02:22:32
    #     1999-12-31 11:12:13
    #     1999-12-31 14:22:32
    #     		        ?
    
    stmt = """select ts from ts1 order by ts desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s6')
    #  expect 4 rows with the following values in this order:
    #                         ?
    #     1997-12-25 05:15:45.9
    #     1997-12-25 05:15:45.9
    #     1995-12-29 14:15:16.7
    
    stmt = """select ts from ts6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    # expect 3 rows with the following values in any order:
    #    0003-01-02 16:05:06.123456
    #    0003-01-02 16:05:06.123456
    #                             ?
    
    stmt = """DELETE from tsdeflt where ts = timestamp '03/25/1997 01:25:35 PM'
or ts = timestamp '03/25/1997 01:25:35 am';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """DELETE from ts0 where ts < timestamp '2000-01-01:00:00:00';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from ts1 where ts is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from ts6 where ts = timestamp '01/02/0003 04:05:06.123456 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select count (*) from tsdeflt where ts is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    # expect count of 1
    
    stmt = """select * from ts0 where ts is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    #  expect count of 0
    
    stmt = """select * from ts1 order by ts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    #  expect 1 row containing a null
    
    stmt = """select * from ts6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s10')
    
    _testmgr.testcase_end(desc)

def test004(desc="""Test the precision of INTERVAL YEAR(n) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # UPDATE, & DELETE
    # test003
    # jclear
    # 1997-03-26
    # Test the precision of INTERVAL YEAR(n) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 1 to 18 figures, default is 2
    #
    
    stmt = """create table t1year (
ivdeflt     interval year,
iv1         interval year (1),
iv10        interval year (10),
ivmax       interval year (18)
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """INSERT into t1year values (
interval '97' year,
interval '7' year (1),
interval '1234567890' year (10),
interval '123456789123456789' year (18)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into t1year values (
- interval '99' year,
- interval '9' year (1),
- interval '9876543210' year (10),
- interval '987654321987654321' year (18)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into t1year values (
interval '00' year,
interval '0' year (1),
interval '0000000000' year (10),
interval '000000000000000000' year (18)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into t1year values (null, null, null, null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from t1year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    # expect 4 rows with the following values:
    #      97    7   1234567890   123456789123456789
    #     -99   -9  -9876543210  -987654321987654321
    #       0    0            0                    0
    #       ?    ?            ?                    ?
    
    stmt = """UPDATE t1year set iv1 = interval '0' year (1)
where ivmax is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """UPDATE t1year set iv10 = interval '9876543210' year (10)
where iv1 = interval '0' year (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """select * from t1year 
where iv10 > interval '666' year (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #      where iv10 > cast (666 as interval year (3));	XXXXXX
    # expect 3 rows with the following values:
    #      97    7   1234567890   123456789123456789
    #       0    0   9876543210                    0
    #       ?    0            ?                    ?
    
    stmt = """DELETE from t1year 
where ivdeflt = interval '97' year
or ivdeflt >= interval '0' year
or ivmax is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    # -     where ivdeflt = interval '0' year (1) + cast (97 as interval year)  XXXX
    
    stmt = """select count (*) from t1year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    # expect count of 1
    
    stmt = """drop table t1year cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Test the precision of INTERVAL YEAR(n) TO MONTH with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test004
    # jclear
    # 1997-03-26
    # Test the precision of INTERVAL YEAR(n) TO MONTH with INSERT, UPDATE, & DELETE
    # Specs allow a YEAR range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the MONTH can only be 0 to 11.
    #
    
    stmt = """INSERT into ydefmon values (interval '97-03' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ydefmon values (interval '00-00' year to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ydefmon values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from ydefmon;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s0')
    # expect 2 rows with the following values:
    # 	 97-03
    # 	  0-00
    # 	     ?
    
    stmt = """INSERT into y1mon values (interval '7-11' year (1) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into y1mon values (interval '0-00' year (1) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into y1mon values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from y1mon;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    # expect 2 rows with the following values:
    #     7-11
    #     0-00
    # 	  ?
    
    stmt = """INSERT into y16mon values (
interval '1234567890123456-11' year (16) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into y16mon values (
interval '0000000000000000-00' year (16) to month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into y16mon values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from y16mon;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s2')
    # expect 2 rows with the following values:
    #     1234567890123456-11
    #                    0-00
    #                       ?
    
    stmt = """UPDATE ydefmon set iv = interval '99' year
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE y1mon set iv = interval '9-01' year (1) to month
where iv <= interval '0' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE y16mon set iv = interval '9876543210987654-11' year (16) to month
where iv <= interval '0000000000000000-00' year (16) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from ydefmon 
where iv < interval '666' year (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s3')
    # -     where iv < cast (666 as interval year (3));	XXXXXX
    #  expect 3 rows with the following values:
    #      97-03
    #       0-00
    #      99-00
    
    stmt = """select * from y1mon 
where iv > interval '108' month (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    # -     where iv > cast (108 as interval month (3));	XXXXXX
    #  expect 1 row with the following value:
    #  	 9-01
    
    stmt = """select * from y16mon 
where iv > interval '8888888888888888-10' year (16) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s5')
    # expect 1 row with the following value:
    # 	 9876543210987654-11
    
    stmt = """DELETE from ydefmon where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from y1mon 
where iv BETWEEN interval '0' year (1) AND interval '10' year;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """DELETE from y16mon 
where iv >= interval '1234567890-01' year (10) to month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select count (*) from ydefmon;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s6')
    #  expect count of 0
    stmt = """select count (*) from y1mon where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    #  expect count of 1
    stmt = """select count (*) from y16mon where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s8')
    
    _testmgr.testcase_end(desc)

def test006(desc="""Test the precision of INTERVAL MONTH(n) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # UPDATE, & DELETE
    # test005
    # jclear
    # 1997-03-26
    # Test the precision of INTERVAL MONTH(n) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    #
    
    stmt = """INSERT into tmon   values (interval '03' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon1  values (interval '3' month (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon2  values (interval '23' month (2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon18 values (interval '123456789012345678' month (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tmon   values (interval '00' month);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon1  values (interval '0' month (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon2  values (interval '00' month (2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon18 values (interval '000000000000000000' month (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tmon   values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon1  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon2  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmon18 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tmon;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    #  expect 3 rows with the following values:
    #  	     3
    #  	     0
    #  	     ?
    
    stmt = """select * from tmon1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    #  expect 3 rows with the following values:
    #          3
    #          0
    #  	   ?
    
    stmt = """select * from tmon2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    #  expect 3 rows with the following values:
    #      23
    #       0
    #       ?
    
    stmt = """select * from tmon18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    # expect 3 rows with the following values:
    #     123456789012345678
    #                      0
    #                      ?
    
    stmt = """UPDATE tmon set mdeflt = interval '99' month
where mdeflt < interval '1' month (1) or mdeflt is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE tmon1 set m1 = interval '9' month
where m1 < interval '1' month (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  UPDATE tmon2 set m2 = cast (33 * 3 as interval month) XXXXXX
    stmt = """UPDATE tmon2 set m2 = interval '99' month
where m2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE tmon18 set m18 = interval '99' month
where m18 < interval '1' month (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tmon 
where mdeflt > interval '2' month (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s4')
    # -     where mdeflt > cast (2 as interval month (1));	XXXXXX
    #  expect 3 rows with the following values:
    #  	     3
    #  	    99
    #  	    99
    
    stmt = """select * from tmon1 
where m1 >= interval '3' month (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    # -     where m1 >= cast (3 as interval month (1));	XXXXXX
    #  expect 2 rows with the following values:
    #          3
    #          9
    
    stmt = """select * from tmon2 
where m2 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    #  expect 2 rows with the following values:
    #         99
    #         99
    
    stmt = """select * from tmon18 
where m18 >= interval '00' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s7')
    #      where m18 >= cast (0 as interval month (1));	XXXXXX
    # expect 2 rows with the following values:
    #     123456789012345678
    #                     99
    
    stmt = """DELETE from tmon 
where mdeflt = interval '99' month
or mdeflt = interval '03' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    #      where mdeflt = interval '00' month + cast (99 as interval month) XXXXXX
    
    stmt = """DELETE from tmon1 
where m1 = interval '3' month (1)
or m1 = interval '9' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #      where m1 = interval '00' month + cast (3 as interval month(1))	XXXXXX
    
    stmt = """DELETE from tmon2 
where m2 = interval '99' month;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #      where m2 = interval '09' month + cast (90 as interval month);	XXXXXX
    
    stmt = """DELETE from tmon18 
where m18 between interval '00' month
and interval '123456789012345678' month (18);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    # - and interval '00' month + cast (123456789012345678 as interval month(18)); XXXXXX
    
    stmt = """select count (*) from tmon;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #  expect count of 0
    stmt = """select count (*) from tmon1 where m1 is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    #  expect count of 0
    stmt = """select count (*) from tmon2 where m2 is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    #  expect count of 1
    stmt = """select count (*) from tmon18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s11')
    
    _testmgr.testcase_end(desc)

def test007(desc="""Test the precision of INTERVAL DAY(n) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # UPDATE, & DELETE
    # test006
    # jclear
    # 1997-03-27
    # Test the precision of INTERVAL DAY(n) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    #
    stmt = """INSERT into tday   values (interval -'03' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday1  values (interval '3' day (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday2  values (interval -'23' day (2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday18 values (interval '123456789012345678' day (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tday   values (interval '99' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday1  values (interval -'9' day (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday2  values (interval '10' day (2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday18 values (interval -'987654321987654321' day (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tday   values (interval '00' day);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday1  values (interval '0' day (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday2  values (interval '00' day (2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday18 values (interval '000000000000000000' day (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tday   values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday1  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday2  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tday18 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from tday;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s0')
    #  expect 4 rows with the following values:
    #  	   -03
    #  	    99
    #  	     0
    #  	     ?
    
    stmt = """select iv from tday1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s1')
    #  expect 4 rows with the following values:
    #          3
    #         -9
    #          0
    #          ?
    
    stmt = """select iv from tday2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s2')
    #  expect 4 rows with the following values:
    #     -23
    #       0
    #      10
    #       ?
    
    stmt = """select iv from tday18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s3')
    # expect 3 rows with the following values:
    #     123456789012345678
    #    -987654321987654321
    #                      0
    #                      ?
    
    stmt = """UPDATE tday set iv = interval '99' day
where iv between interval '0' day (1) and interval '10' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tday1 set iv = interval '9' day (1)
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tday2 set iv = interval '99' day
where iv < interval '1' day (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE tday18 set iv = interval '99' day
where iv = interval '0' day (1) or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """select iv from tday 
where iv < interval '100' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s4')
    # -     where iv < cast (100 as interval day (3));	XXXXXX
    #  expect 3 rows with the following values:
    #  	   -03
    #  	    99
    #  	    99
    
    stmt = """select iv from tday1 
where iv >= interval '0' day (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s5')
    # -     where iv >= cast (0 as interval day (1));	XXXXXX
    #  expect 3 rows with the following values:
    #          3
    #          0
    #          9
    
    stmt = """select iv from tday2 
where iv > interval '10' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s6')
    # -     where iv > cast (10 as interval day);	XXXXXX
    #  expect 2 rows with the following values:
    #         99
    #         99
    
    stmt = """select iv from tday18 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s7')
    # expect 4 rows with the following values:
    #     123456789012345678
    #    -987654321987654321
    #                     99
    #                     99
    
    stmt = """DELETE from tday 
where iv = interval '99' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    #      where iv = interval '00' day + cast (99 as interval day);	XXXXXX
    stmt = """DELETE from tday 
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    stmt = """DELETE from tday1 
where iv >= interval '00' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """DELETE from tday2 
where iv = interval '99' day
or iv <= interval '23' day or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #      where iv = interval '09' day + cast (90 as interval day)	XXXXXX
    
    stmt = """DELETE from tday18 
where iv >= interval '123456789012345678' day (18)
or iv < interval '100' day(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    # -        where iv >= interval '00' day +
    # -         cast (123456789012345678 as interval day(18)) XXXXX
    
    stmt = """select count (*) from tday;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s8')
    #  expect count of 1
    stmt = """select count (*) from tday1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s9')
    #  expect count of 1
    stmt = """select count (*) from tday2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s10')
    #  expect count of 0
    stmt = """select count (*) from tday18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a06exp""", 'a06s11')
    
    _testmgr.testcase_end(desc)

def test008(desc="""Test the precision of INTERVAL DAY(n) TO HOUR with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test007
    # jclear
    # 1997-03-27
    # Test the precision of INTERVAL DAY(n) TO HOUR with INSERT, UPDATE, & DELETE
    # Specs allow a DAY range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the HOUR can only be 0 to 23
    #
    stmt = """INSERT into ddefhr values (interval '99:23' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ddefhr values (interval '00:00' day to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into ddefhr values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from ddefhr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s0')
    # expect 2 rows with the following values:
    # 	 99 23
    # 	  0 00
    # 	     ?
    
    stmt = """INSERT into d1hr values (interval '7:11' day (1) to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d1hr values (interval '0:00' day (1) to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d1hr values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from d1hr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s1')
    # expect 2 rows with the following values:
    #     7 11
    #     0 00
    #        ?
    
    stmt = """INSERT into d16hr values (
interval '1234567890123456:23' day (16) to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d16hr values (
interval '0000000000000000:00' day (16) to hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d16hr values (
null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from d16hr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s2')
    # expect 2 rows with the following values:
    #     1234567890123456 23
    #                    0 00
    #                       ?
    
    stmt = """UPDATE ddefhr set iv = interval '99' day
where iv <= interval '0' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE d1hr set iv = interval '9:01' day (1) to hour
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE d16hr set iv = interval '9876543210987654:11' day (16) to hour
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select iv from ddefhr 
where iv > interval '0' day (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s3')
    # -     where iv > cast (0 as interval day);	XXXXXX
    #  expect 2 rows with the following values:
    #      99 23
    #      99 00
    
    stmt = """select iv from d1hr 
where iv > interval '180' hour (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s4')
    # -     where iv > cast (180 as interval hour (3));	XXXXXX
    #  expect 2 row with the following value:
    #  	 9 01
    #  	 9 01
    
    stmt = """select iv from d16hr 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s5')
    # expect 3 rows with the following value:
    # 	 1234567890123456 23
    # 	                0 00
    # 	 9876543210987654 11
    
    stmt = """DELETE from ddefhr 
where iv BETWEEN interval '0' day (1) AND interval '100' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """DELETE from d1hr 
where iv < interval '10' day or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from d16hr 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """select count (*) from ddefhr where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s6')
    #  expect count of 0
    stmt = """select count (*) from d1hr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s7')
    #  expect count of 0
    stmt = """select count (*) from d16hr;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a07exp""", 'a07s8')
    
    _testmgr.testcase_end(desc)

def test009(desc="""Test the precision of INTERVAL DAY(n) TO MINUTE with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test008
    # jclear
    # 1997-03-28
    # Test the precision of INTERVAL DAY(n) TO MINUTE with INSERT, UPDATE, & DELETE
    # Specs allow a DAY range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the HOUR can only be 0 to 23, MINUTE is 0 - 59
    #
    stmt = """INSERT into dmdef values (interval '99:23:59' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dmdef values (interval '00:00:00' day to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dmdef values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from dmdef;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s0')
    # expect 3 rows with the following values:
    # 	 99 23:59
    # 	  0 00:00
    # 	        ?
    
    stmt = """INSERT into dm1 values (interval '1:22:33' day (1) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dm1 values (interval '0:00:00' day (1) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dm1 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from dm1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s1')
    # expect 3 rows with the following values:
    # 	 1 22:33
    # 	 0 00:00
    # 	       ?
    
    stmt = """INSERT into d14m values (
interval '12345678901234:23:59' day (14) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d14m values (
interval '00000000000000:00:00' day (14) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d14m values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from d14m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s2')
    # expect 3 rows with the following values:
    # 	 12345678901234 23:59
    # 	              0 00:00
    # 	                    ?
    
    stmt = """UPDATE dmdef set iv = interval '99' day
where iv <= interval '0' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE dm1 set iv = interval '9:01:01' day (1) to minute
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE d14m set iv = interval '98765432109876:11:59' day (14) to minute
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select iv from dmdef 
where iv > interval '0' day (1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s3')
    # -     where iv > cast (0 as interval day);	XXXXXX
    #  expect 2 rows with the following values:
    #  	 99 23:59
    #  	 99 00:00
    
    stmt = """select iv from dm1 
where iv > interval '180' minute (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s4')
    # -     where iv > cast (180 as interval minute (3));	XXXXXX
    #  expect 2 rows both with the following value:
    #  	 9 01:01
    
    stmt = """select iv from d14m 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s5')
    # expect 3 rows with the following value:
    # 	 12345678901234 23:59
    # 	              0 00:00
    # 	 98765432109876 11:59
    
    stmt = """DELETE from dmdef 
where iv BETWEEN interval '0' day (1) AND interval '100' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    stmt = """DELETE from dm1 
where iv < interval '10' day or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from d14m 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    
    stmt = """select count (*) from dmdef where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s6')
    #  expect count of 0
    stmt = """select count (*) from dm1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s7')
    #  expect count of 0
    stmt = """select count (*) from d14m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a08exp""", 'a08s8')
    
    _testmgr.testcase_end(desc)

def test010(desc="""Test the precision of INTERVAL DAY(n) TO SECOND with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test009
    # jclear
    # 1997-03-31
    # Test the precision of INTERVAL DAY(n) TO SECOND with INSERT, UPDATE, & DELETE
    # Specs allow a DAY range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the SECOND can be 0 - 59 with up to 6 decimal figures.
    #
    stmt = """INSERT into dsdef values (interval '99:23:59:59.999999' day to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dsdef values (interval '01:01:01:01.000001' day to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dsdef values (interval '00:00:00:00.000000' day to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into dsdef values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from dsdef;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s0')
    # expect 4 rows with the following values:
    # 	 99 23:59:59.999999
    # 	  1 01:01:01.000001
    # 	  0 00:00:00.000000
    # 	                  ?
    
    stmt = """INSERT into d0s values (interval '99:23:59:59' day to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d0s values (interval '01:01:01:01' day to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d0s values (interval '00:00:00:00' day to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d0s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from d0s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s1')
    # expect 4 rows with the following values:
    # 	 99 23:59:59
    # 	  1 01:01:01
    # 	  0 00:00:00
    # 	           ?
    
    stmt = """INSERT into d1s values (interval '0:12:34:56' day (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d1s values (interval '9:23:59:59' day (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d1s values (interval '0:00:00:00' day (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d1s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from d1s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s2')
    # expect 4 rows with the following values:
    # 	 0 12:34:56.000000
    # 	 9 23:59:59.000000
    # 	 0 00:00:00.000000
    # 	                 ?
    
    stmt = """INSERT into d7s values (
interval '1234567:23:59:59.999' day (7) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d7s values (
interval '0000001:01:01:01.001' day (7) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d7s values (
interval '0000000:00:00:00.000' day (7) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into d7s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from d7s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s3')
    # expect 4 rows with the following values:
    # 	 1234567 23:59:59.999
    # 	       1 01:01:01.001
    # 	       0 00:00:00.000
    # 	                    ?
    
    stmt = """UPDATE dsdef set iv = interval '99' day
where iv <= interval '0' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE d0s set iv = interval '11:22:33:44' day to second (0)
where iv = interval '0' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE d1s set iv = interval '9:01:01:01.123456' day (1) to second (6)
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """UPDATE d7s set iv = interval '9876543:23:59:59.999' day (7) to second (3)
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select iv from dsdef 
where iv > interval '0' day (1)
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s4')
    # -     where iv > cast (0 as interval day)	XXXXXX
    #  expect 3 rows with the following values:
    #  	  1 01:01:01.000001
    #  	 99 00:00:00.000000
    #  	 99 23:59:59.999999
    
    stmt = """select iv from d0s 
where iv <= interval '100' day (3)
order by iv desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s5')
    # -     where iv <= cast (100 as interval day (3))	XXXXXX
    #  expect 3 rows with the following values:
    #  	 99 23:59:59
    #  	 11 22:33:44
    #  	  1 01:01:01
    
    stmt = """select iv from d1s 
where iv > interval '217' hour (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s6')
    # -     where iv > cast (217 as interval hour (3));	XXXXXX
    #  expect 3 rows all with the following value:
    #  	 9 01:01:01.123456
    
    stmt = """select iv from d7s 
where iv is not null
order by iv asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s7')
    # expect 4 rows with the following value in this order:
    # 	       0 00:00:00.000
    # 	       1 01:01:01.001
    # 	 1234567 23:59:59.999
    # 	 9876543 23:59:59.999
    
    stmt = """DELETE from dsdef 
where iv BETWEEN interval '0' day (1) AND interval '100' day (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from d0s 
where iv > interval '1' day;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from d1s 
where iv < interval '10' day or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """DELETE from d7s 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """select count (*) from dsdef where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s8')
    #  expect count of 0
    stmt = """select count (*) from d0s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s9')
    #  expect count of 1
    stmt = """select count (*) from d1s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s10')
    #  expect count of 0
    stmt = """select count (*) from d7s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a09exp""", 'a09s11')
    
    _testmgr.testcase_end(desc)

def test011(desc="""Test the precision of INTERVAL HOUR(n) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # UPDATE, & DELETE
    # test010
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL HOUR(n) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    #
    
    stmt = """INSERT into thour   values (interval '03' hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour1  values (interval '3' hour (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour2  values (interval '12345' hour (5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour18 values (interval '123456789012345678' hour (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into thour   values (interval '00' hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour1  values (interval '0' hour (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour2  values (interval '00000' hour (5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour18 values (interval '000000000000000000' hour (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into thour   values (interval '01' hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour1  values (interval '1' hour (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour2  values (interval '00001' hour (5));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour18 values (interval '000000000000000001' hour (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into thour   values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour1  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour2  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into thour18 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from thour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s0')
    #  expect 4 rows with the following values:
    #  	     3
    #  	     0
    #  	     1
    #  	     ?
    
    stmt = """select iv from thour1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s1')
    #  expect 4 rows with the following values:
    #          3
    #          0
    #          1
    #          ?
    
    stmt = """select iv from thour2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s2')
    #  expect 4 rows with the following values:
    #  	 12345
    #  	     0
    #  	     1
    #  	     ?
    
    stmt = """select iv from thour18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s3')
    # expect 4 rows with the following values:
    #     123456789012345678
    #                      0
    #                      1
    #                      ?
    
    stmt = """UPDATE thour set iv = interval '99' hour
where iv between interval '0' hour (1) and interval '10' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """UPDATE thour1 set iv = interval '9' hour
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE thour2 set iv = interval '99' hour
where iv not between interval '1' hour (1)
and interval '100000' hour (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE thour18 set iv = interval '999999999999999999' hour (18)
where iv = interval '0' hour (1) or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """select iv from thour 
where iv < interval '100' hour (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s4')
    # -     where iv < cast (100 as interval hour (3));	XXXXXX
    #  expect 3 rows all with the following value:
    #  	    99
    
    stmt = """select * from thour1 
where iv >= interval '0' hour (1)
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s5')
    # -     where iv >= cast (0 as interval hour (1));	XXXXXX
    #  expect 4 rows with the following values in this order:
    #          0
    #          1
    #          3
    #          9
    
    stmt = """select iv from thour2 
where iv > interval '00' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s6')
    # -     where iv > cast (00 as interval hour);	XXXXXX
    #  expect 3 rows with the following values:
    #  	 12345
    #  	    99
    #  	     1
    
    stmt = """select distinct iv from thour18 
where iv is not null
order by iv desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s7')
    # expect 3 rows with the following values:
    # 	 999999999999999999
    # 	 123456789012345678
    # 	                  1
    
    stmt = """DELETE from thour 
where iv = interval '99' hour or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #      where iv = interval '00' hour + cast (99 as interval hour)	XXXXXX
    #      or iv is null;		XXXXXX
    
    stmt = """DELETE from thour1 
where iv >= interval '00' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """DELETE from thour2 
where iv >= interval '99' hour
or iv <= interval '23' hour or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #      where iv >= interval '09' hour + cast (90 as interval hour)	XXXXXX
    
    stmt = """DELETE from thour18 
where iv >= interval '123456789012345678' hour (18)
or iv < interval '100' hour(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    # -     where iv >= interval '00' hour +
    # -                 cast (123456789012345678 as interval hour(18))	XXXXXX
    
    stmt = """select count (*) from thour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s8')
    #  expect count of 0
    stmt = """select count (*) from thour1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s9')
    #  expect count of 0
    stmt = """select count (*) from thour2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s10')
    #  expect count of 0
    stmt = """select count (*) from thour18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a10exp""", 'a10s11')
    
    _testmgr.testcase_end(desc)

def test012(desc="""Test the precision of INTERVAL HOUR(n) TO MINUTE with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test011
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL HOUR(n) TO MINUTE with INSERT, UPDATE, & DELETE
    # Specs allow a HOUR range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the MINUTE can only be 0 - 59
    #
    stmt = """INSERT into hmdef values (interval '23:59' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into hmdef values (interval '01:01' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into hmdef values (interval '00:00' hour to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into hmdef values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from hmdef;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s0')
    # expect 4 rows with the following values:
    # 	 23:59
    # 	  1:01
    # 	  0:00
    # 	     ?
    
    stmt = """INSERT into h1m values (interval '1:23' hour (1) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h1m values (interval '1:01' hour (1) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h1m values (interval '0:00' hour (1) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h1m values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from h1m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s1')
    # expect 4 rows with the following values:
    #     1:23
    #     1:01
    #     0:00
    #        ?
    
    stmt = """INSERT into h16m values (
interval '1234567890123456:59' hour (16) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h16m values (
interval '0000000000000000:00' hour (16) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h16m values (
interval '0000000000000001:01' hour (16) to minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h16m values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from h16m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s2')
    # expect 4 rows with the following values:
    #     1234567890123456:59
    #                    0:00
    #                    1:01
    #                       ?
    
    stmt = """UPDATE hmdef set iv = interval '99' hour
where iv <= interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE h1m set iv = interval '9:59' hour (1) to minute
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """UPDATE h16m set iv = interval '9876543210987654:59' hour (16) to minute
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select iv from hmdef 
where iv > interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s3')
    #  expect 3 rows with the following values:
    #      23:59
    #       1:01
    #      99:00
    
    stmt = """select iv from h1m 
where iv >= interval '599' minute (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s4')
    #  expect 3 rows all with the following value:
    #  	 9:59
    
    stmt = """select * from h16m 
where iv is not null
order by iv asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s5')
    # expect 4 rows with the following value:
    #                    0:00
    #                    1:01
    #     1234567890123456:59
    #     9876543210987654:59
    
    stmt = """DELETE from hmdef 
where iv BETWEEN interval '1' hour (1) AND interval '100' hour (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from h1m 
where iv < interval '10' hour or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """DELETE from h16m 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """select count (*) from hmdef where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s6')
    #  expect count of 0
    stmt = """select count (*) from h1m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s7')
    #  expect count of 0
    stmt = """select count (*) from h16m;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a11exp""", 'a11s8')
    
    _testmgr.testcase_end(desc)

def test013(desc="""Test the precision of INTERVAL HOUR(n) TO SECOND with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test012
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL HOUR(n) TO SECOND with INSERT, UPDATE, & DELETE
    # Specs allow a HOUR range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the MINUTE can be 0 - 59,
    # the SECOND can be 0 - 59 with up to 6 decimal figures.
    #
    stmt = """INSERT into hsdef values (interval '23:59:59.999999' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into hsdef values (interval '01:01:01.000001' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into hsdef values (interval '00:00:00.000000' hour to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into hsdef values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from hsdef;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s0')
    # expect 4 rows with the following values:
    # 	 23:59:59.999999
    # 	  1:01:01.000001
    # 	  0:00:00.000000
    # 	               ?
    
    stmt = """INSERT into h0s values (interval '99:59:59' hour to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h0s values (interval '01:01:01' hour to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h0s values (interval '00:00:00' hour to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h0s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from h0s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s1')
    # expect 4 rows with the following values:
    #     99:59:59
    #      1:01:01
    #      0:00:00
    #            ?
    
    stmt = """INSERT into h1s values (interval '2:34:56' hour (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h1s values (interval '9:59:59' hour (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h1s values (interval '0:00:00' hour (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h1s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from h1s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s2')
    # expect 4 rows with the following values:
    #     2:34:56.000000
    #     9:59:59.000000
    #     0:00:00.000000
    #                  ?
    
    stmt = """INSERT into h8s values (
interval '12345678:59:59.999' hour (8) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h8s values (
interval '00000001:01:01.001' hour (8) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h8s values (
interval '00000000:00:00.000' hour (8) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into h8s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from h8s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s3')
    # expect 4 rows with the following values:
    #     12345678:59:59.999
    #            1:01:01.001
    #            0:00:00.000
    #                      ?
    
    #  XXXXXX false error for hour values over 7
    #  INSERT into h18s values (
    #      interval '123456789012345678:59:59.999999' hour (18) to second);
    #  INSERT into h18s values (
    #      interval '000000000000000001:01:01.000001' hour (18) to second);
    #  INSERT into h18s values (
    #      interval '000000000000000000:00:00.000000' hour (18) to second);
    #  INSERT into h18s values (null);
    #
    #  select iv from h18s;
    #  -- expect 4 rows with the following values:
    #  --     123456789012345678:59:59.999999
    #  --                      1:01:01.000001
    #  --                      0:00:00.000000
    #  --                                   ?
    
    stmt = """UPDATE hsdef set iv = interval '99' hour
where iv <= interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE h0s set iv = interval '22:33:44' hour to second (0)
where iv = interval '0' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE h1s set iv = interval '9:01:01.123456' hour (1) to second (6)
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """UPDATE h8s set iv = interval '98765432:59:59.999' hour (8) to second (3)
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # - UPDATE h18s set iv = interval '987654321098765432:11:12:13' hour (18) to second XXXXXX
    # -    where iv is null;		XXXXXX
    
    stmt = """select iv from hsdef 
where iv > interval '1' hour
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s4')
    #  expect 3 rows with the following values:
    #       1:01:01.000001
    #      23:59:59.999999
    #      99:00:00.000000
    
    stmt = """select * from h0s 
where iv <= interval '100' hour (3)
order by iv asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s5')
    #  expect 3 rows with the following values:
    #       1:01:01
    #      22:33:44
    #      99:59:59
    
    stmt = """select iv from h1s 
where iv > interval '540' minute (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s6')
    #  expect 3 rows all with the following value:
    #  	  9:01:01.123456
    
    stmt = """select iv from h8s 
where iv is not null
order by iv asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s7')
    # expect 1 rows with the following value in this order:
    #            0:00:00.000
    #            1:01:01.001
    #     12345678:59:59.999
    #     98765432:59:59.999
    
    #  select iv from h18s
    #      where iv is not null;
    #  -- expect 3 rows with the following values:
    
    stmt = """DELETE from hsdef 
where iv BETWEEN interval '0' hour (1) AND interval '100' hour (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from h0s 
where iv > interval '1' hour;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from h1s 
where iv < interval '10' hour or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """DELETE from h8s 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    # - DELETE from h18s			XXXXXX
    # -     where iv is not null;
    
    stmt = """select count (*) from hsdef where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s8')
    #  expect count of 0
    stmt = """select count (*) from h0s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s9')
    #  expect count of 1
    stmt = """select count (*) from h1s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s10')
    #  expect count of 0
    stmt = """select count (*) from h8s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a12exp""", 'a12s11')
    
    _testmgr.testcase_end(desc)

def test014(desc="""Test the precision of INTERVAL MINUTE(n) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  UPDATE, & DELETE
    # test013
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL MINUTE(n) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    #
    
    stmt = """INSERT into tmin   values (interval '03' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin1  values (interval '3' minute (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin2  values (interval '345' minute (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin18 values (
interval '123456789012345678' minute (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tmin   values (interval '00' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin1  values (interval '0' minute (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin2  values (interval '000' minute (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin18 values (
interval '000000000000000000' minute (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tmin   values (interval '01' minute);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin1  values (interval '1' minute (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin2  values (interval '001' minute (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin18 values (
interval '000000000000000001' minute (18));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tmin   values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin1  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin2  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tmin18 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from tmin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s0')
    #  expect 4 rows with the following values:
    #  	     3
    #  	     0
    #  	     1
    #  	     ?
    
    stmt = """select iv from tmin1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s1')
    #  expect 4 rows with the following values:
    #          3
    #          0
    #          1
    #          ?
    
    stmt = """select iv from tmin2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s2')
    #  expect 4 rows with the following values:
    #  	   345
    #  	     0
    #  	     1
    #  	     ?
    
    stmt = """select iv from tmin18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s3')
    # expect 4 rows with the following values:
    #     123456789012345678
    #                      0
    #                      1
    #                      ?
    
    stmt = """UPDATE tmin set iv = interval '99' minute
where iv between interval '0' minute (1) and interval '10' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """UPDATE tmin1 set iv = interval '9' minute
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tmin2 set iv = interval '99' minute
where iv not between interval '1' minute (1)
and interval '100000' minute (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tmin18 set iv = interval '999999999999999999' minute (18)
where iv = interval '0' minute (1) or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """select iv from tmin 
where iv < interval '100' minute (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s4')
    # -     where iv < cast (100 as interval minute (3));	XXXXXX
    #  expect 3 rows all with the following value:
    #  	    99
    
    stmt = """select * from tmin1 
where iv >= interval '0' minute (1)
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s5')
    # -     where iv >= cast (0 as interval minute (1));	XXXXXX
    #  expect 4 rows with the following values in this order:
    #          0
    #          1
    #          3
    #          9
    
    stmt = """select iv from tmin2 
where iv > interval '00' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s6')
    # -     where iv > cast (00 as interval minute);	XXXXXX
    #  expect 3 rows with the following values:
    #  	   345
    #  	    99
    #  	     1
    
    stmt = """select distinct iv from tmin18 
where iv is not null
order by iv desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s7')
    # expect 4 rows with the following values:
    # 	 999999999999999999
    # 	 123456789012345678
    # 	                  1
    
    stmt = """DELETE from tmin 
where iv = interval '99' minute or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #      where iv = interval '00' minute + cast (99 as interval minute)	XXXXXX
    #      or iv is null;		XXXXXX
    
    stmt = """DELETE from tmin1 
where iv >= interval '00' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """DELETE from tmin2 
where iv >= interval '99' minute
or iv <= interval '23' minute or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #      where iv >= interval '09' minute + cast (90 as interval minute)	XXXXXX
    
    stmt = """DELETE from tmin18 
where iv >= interval '123456789012345678' minute (18)
or iv < interval '100' minute(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    # -     where iv >= interval '00' minute +
    # -                 cast (123456789012345678 as interval minute(18))	XXXXXX
    
    stmt = """select count (*) from tmin;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s8')
    #  expect count of 0
    stmt = """select count (*) from tmin1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s9')
    #  expect count of 0
    stmt = """select count (*) from tmin2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s10')
    #  expect count of 0
    stmt = """select count (*) from tmin18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a13exp""", 'a13s11')
    
    _testmgr.testcase_end(desc)

def test015(desc="""Test the precision of INTERVAL MINUTE(n) TO SECOND with"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  INSERT, UPDATE, & DELETE
    # test014
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL MINUTE(n) TO SECOND with INSERT, UPDATE, & DELETE
    # Specs allow a MINUTE range of (unsigned) 1 to 18 figures, default is 2,
    # the values for the SECOND can be 0 - 59 with up to 6 decimal figures.
    #
    stmt = """INSERT into msdef values (interval '99:59.999999' minute to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into msdef values (interval '01:01.000001' minute to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into msdef values (interval '00:00.000000' minute to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into msdef values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from msdef;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s0')
    # expect 4 rows with the following values:
    # 	 99:59.999999
    # 	  1:01.000001
    # 	  0:00.000000
    # 	            ?
    
    stmt = """INSERT into m0s values (interval '99:59' minute to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m0s values (interval '01:01' minute to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m0s values (interval '00:00' minute to second (0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m0s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from m0s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s1')
    # expect 4 rows with the following values:
    #     99:59
    #      1:01
    #      0:00
    #         ?
    
    stmt = """INSERT into m1s values (interval '4:56' minute (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m1s values (interval '9:59' minute (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m1s values (interval '0:00' minute (1) to second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m1s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from m1s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s2')
    # expect 4 rows with the following values:
    #     2:34:56.000000
    #     9:59:59.000000
    #     0:00:00.000000
    #                  ?
    
    stmt = """INSERT into m13s values (
interval '1234567890123:59.999' minute (13) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m13s values (
interval '0000000000001:01.001' minute (13) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m13s values (
interval '0000000000000:00.000' minute (13) to second (3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into m13s values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from m13s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s3')
    # expect 4 rows with the following values:
    #     1234567890123:59.999
    #                 1:01.001
    #                 0:00.000
    #                        ?
    
    stmt = """UPDATE msdef set iv = interval '99' minute
where iv <= interval '0' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE m0s set iv = interval '33:44' minute to second (0)
where iv = interval '0' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE m1s set iv = interval '9:01.123456' minute (1) to second (6)
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 3)
    stmt = """UPDATE m13s set iv = interval '9876543210987:59.999' minute (13) to second (3)
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select iv from msdef 
where iv > interval '1' minute
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s4')
    #  expect 3 rows with the following values:
    #       1:01.000001
    #      99:00.000000
    #      99:59.999999
    
    stmt = """select * from m0s 
where iv <= interval '100' minute (3)
order by iv asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s5')
    #  expect 3 rows with the following values:
    #       1:01
    #      33:44
    #      99:59
    
    stmt = """select iv from m1s 
where iv > interval '540' second (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s6')
    #  expect 3 rows all with the following value:
    #  	  9:01.123456
    
    stmt = """select iv from m13s 
where iv is not null
order by iv asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s7')
    # expect 4 rows with the following value in this order:
    #                 0:00.000
    #                 1:01.001
    #     1234567890123:59.999
    #     9876543210987:59.999
    
    stmt = """DELETE from msdef 
where iv BETWEEN interval '1' minute (1) AND interval '100' minute (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from m0s 
where iv > interval '1' minute;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """DELETE from m1s 
where iv < interval '10' minute or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    stmt = """DELETE from m13s 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """select count (*) from msdef where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s8')
    #  expect count of 0
    stmt = """select count (*) from m0s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s9')
    #  expect count of 1
    stmt = """select count (*) from m1s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s10')
    #  expect count of 0
    stmt = """select count (*) from m13s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a14exp""", 'a14s11')
    
    _testmgr.testcase_end(desc)

def test016(desc="""Test the precision of INTERVAL SECOND(n) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #   UPDATE, & DELETE
    # test015
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL SECOND(n) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    #
    stmt = """INSERT into tsec   values (interval '99' second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec1  values (interval '9' second (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec12  values (interval '123456789012' second (12));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  INSERT into tsec18 values (
    #      interval '123456789012345678' second (18)); XXXXXX
    
    stmt = """INSERT into tsec   values (interval '00' second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec1  values (interval '0' second (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec12  values (interval '000000000000' second (12));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  INSERT into tsec18 values (
    #      interval '000000000000000000' second (18));	XXXXXX
    
    stmt = """INSERT into tsec   values (interval '01' second);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec1  values (interval '1' second (1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec12  values (interval '000000000001' second (12));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  INSERT into tsec18 values (
    #      interval '000000000000000001' second (18));	XXXXXX
    
    stmt = """INSERT into tsec   values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec1  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec12  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # - INSERT into tsec18 values (null);	XXXXXX
    
    stmt = """select iv from tsec;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s0')
    #  expect 4 rows with the following values:
    #  	 99.000000
    #  	  0.000000
    #  	  1.000000
    #  	         ?
    
    stmt = """select iv from tsec1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s1')
    #  expect 4 rows with the following values:
    #      9.000000
    #      0.000000
    #      1.000000
    #             ?
    
    stmt = """select iv from tsec12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s2')
    # expect 4 rows with the following values:
    #     123456789012.000000
    #                0.000000
    #                1.000000
    #                       ?
    
    #  select iv from tsec18;		XXXXXX
    # expect 4 rows with the following values:
    #     123456789012345678.000000
    #                      0.000000
    #                      1.000000
    #                             ?
    
    stmt = """UPDATE tsec set iv = interval '99' second
where iv between interval '0' second (1) and interval '10' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE tsec1 set iv = interval '9' second
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tsec12 set iv = interval '999999999999' second (12)
where iv between interval '1' second (1)
and interval '100000' second (6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # - UPDATE tsec18 set iv = interval '999999999999999999' second (18)  XXXXXX
    # -     where iv = interval '0' second (1) or iv is null;
    
    stmt = """select iv from tsec 
where iv < interval '100' second (3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s3')
    # -     where iv < cast (100 as interval second (3));	XXXXXX
    #  expect 3 rows all with the following value:
    #  	    99.000000
    
    stmt = """select * from tsec1 
where iv >= interval '0' second (1)
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s4')
    # -     where iv >= cast (0 as interval second (1));	XXXXXX
    #  expect 4 rows with the following values in this order:
    #      0.000000
    #      1.000000
    #      9.000000
    #      9.000000
    
    stmt = """select iv from tsec12 
where iv >= interval '00' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s5')
    #      where iv > cast (00 as interval second);	XXXXXX
    # expect 3 rows with the following values:
    #     123456789012.000000
    #                0.000000
    #     999999999999.000000
    
    #  select distinct iv from tsec18		XXXXXX
    #      where iv is not null
    #          order by iv desc;
    # expect 3 rows with the following values:
    
    stmt = """DELETE from tsec 
where iv = interval '99' second or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    #      where iv = interval '00' second + cast (99 as interval second)	XXXXXX
    #      or iv is null;		XXXXXX
    
    stmt = """DELETE from tsec1 
where iv >= interval '00' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """DELETE from tsec12 
where iv >= interval '99' second
or iv <= interval '00' second or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    # -     where iv >= interval '09' second + cast (90 as interval second)	XXXXXX
    
    # - DELETE from tsec18
    # -     where iv >= interval '123456789012345678' second (18)
    # -        or iv < interval '100' second(3);
    
    stmt = """select count (*) from tsec;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s6')
    #  expect count of 0
    stmt = """select count (*) from tsec1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s7')
    #  expect count of 0
    stmt = """select count (*) from tsec12;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a15exp""", 'a15s8')
    
    _testmgr.testcase_end(desc)

def test017(desc="""Test the precision of INTERVAL SECOND(n,0) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  UPDATE, & DELETE
    # test016
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL SECOND(n,0) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    # and a precision of 1 - 6, default is 6.
    #
    
    stmt = """INSERT into tn0sec1  values (interval '9' second (1, 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tn0sec18 values (
interval '123456789012345678' second (18, 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tn0sec1  values (interval '0' second (1, 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tn0sec18 values (
interval '000000000000000000' second (18, 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tn0sec1  values (interval '1' second (1, 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tn0sec18 values (
interval '000000000000000001' second (18, 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """INSERT into tn0sec1  values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tn0sec18 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select iv from tn0sec1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s0')
    #  expect 4 rows with the following values:
    #  	 9
    #  	 0
    #  	 1
    #  	 ?
    
    stmt = """select iv from tn0sec18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s1')
    # expect 4 rows with the following values:
    #     123456789012345678
    #                      0
    #                      1
    #                      ?
    
    stmt = """UPDATE tn0sec1 set iv = interval '9' second (1, 0)
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tn0sec18 set iv = interval '999999999999999999' second (18, 0)
where iv = interval '0' second (1, 0) or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    
    stmt = """select * from tn0sec1 
where iv >= interval '0' second (1, 0)
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s2')
    #  expect 4 rows with the following values in this order:
    #      0
    #      1
    #      9
    #      9
    
    stmt = """select distinct iv from tn0sec18 
where iv is not null
order by iv desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s3')
    # expect 3 rows with the following values:
    #     999999999999999999
    #     123456789012345678
    #                      1
    
    stmt = """DELETE from tn0sec1 
where iv >= interval '0' second (1, 0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """DELETE from tn0sec18 
where iv >= interval '123456789012345678' second (18, 0)
or iv < interval '100' second(3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """select count (*) from tn0sec1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s4')
    #  expect count of 0
    stmt = """select count (*) from tn0sec18;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a16exp""", 'a16s5')
    
    _testmgr.testcase_end(desc)

def test018(desc="""Test the precision of INTERVAL SECOND(n,f) with INSERT,"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  UPDATE, & DELETE
    # test017
    # jclear
    # 1997-04-01
    # Test the precision of INTERVAL SECOND(n,f) with INSERT, UPDATE, & DELETE
    # Specs allow a range of (unsigned) 2 to 18 figures, default is 2,
    #
    stmt = """INSERT into tsec13 values (interval '9.999' second (1, 3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec21 values (interval '99.9' second (2, 1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec162 values (
interval '9999999999999999.99' second (16, 2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  INSERT into tsec182 values (
    #      interval '123456789012345678.12' second (18, 2));	XXXXXX
    
    stmt = """INSERT into tsec13 values (interval '0.000' second (1, 3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec21 values (interval '00.0' second (2, 1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec162 values (
interval '0000000000000000.00' second (16, 2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  INSERT into tsec182 values (
    #      interval '000000000000000000.00' second (18, 2));	XXXXXX
    
    stmt = """INSERT into tsec13 values (interval '1.001' second (1, 3));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec21 values (interval '01.1' second (2, 1));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec162 values (
interval '0000000000000001.01' second (16, 2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  INSERT into tsec182 values (
    #      interval '000000000000000001.01' second (18, 2));	XXXXXX
    
    stmt = """INSERT into tsec13 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec21 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT into tsec162 values (null);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # - INSERT into tsec182 values (null);
    
    stmt = """select iv from tsec13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s0')
    #  expect 4 rows with the following values:
    # 	 9.999
    # 	 0.000
    # 	 1.001
    # 	     ?
    
    stmt = """select iv from tsec21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s1')
    #  expect 4 rows with the following values:
    #      99.9
    #       0.0
    #       1.1
    #         ?
    
    stmt = """select iv from tsec162;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s2')
    # expect 4 rows with the following values:
    #     9999999999999999.99
    #                    0.00
    #                    1.01
    #                       ?
    
    #  select iv from tsec182;		XXXXXX
    # expect 4 rows with the following values:
    #  --      123456789012345678.12
    #  --      000000000000000000.00
    #  --      000000000000000001.01
    #  --                          ?
    
    stmt = """UPDATE tsec13 set iv = interval '9.999' second (1, 3)
where iv between interval '0.000' second (1, 3)
and interval '2.000' second (1, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """UPDATE tsec21 set iv = interval '12.3' second (2, 1)
where iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """UPDATE tsec162 set iv = interval '9999999999999999.99' second (16, 2)
where iv between interval '0' second (1)
and interval '1.01' second (1, 2);"""
    output = _dci.cmdexec(stmt)
    # FIXME _dci.expect_updated_msg(output, 2)
    # - UPDATE tsec182 set iv = interval '999999999999999999' second (18)  XXXXXX
    # -     where iv = interval '0' second (1) or iv is null;
    
    stmt = """select iv from tsec13 
where iv < interval '10.0' second (2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s4')
    # -     where iv < cast (100 as interval second (3));	XXXXXX
    #  expect 3 rows all with the following value:
    #  	    9.999
    
    stmt = """select * from tsec21 
where iv >= interval '00.0' second (2, 1)
order by iv;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s5')
    #  expect 4 rows with the following values in this order:
    #       0.0
    #       1.1
    #      12.3
    #      99.9
    
    stmt = """select distinct iv from tsec162 
where iv >= interval '00' second;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8411')
    # expect 1 row with the following value:
    #     9999999999999999.99
    
    #  select distinct iv from tsec182		XXXXXX
    #      where iv is not null
    #          order by iv desc;
    # expect 3 rows with the following values:
    
    stmt = """DELETE from tsec13 
where iv = interval '9.999' second (1 ,3) or iv is null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """DELETE from tsec21 
where iv is not null;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)
    
    stmt = """DELETE from tsec162 
where iv = interval '9999999999999999.99' second (16, 2)
or iv is null;"""
    output = _dci.cmdexec(stmt)
    # FIXME _dci.expect_deleted_msg(output, 1)
    
    # - DELETE from tsec182
    # -     where iv >= interval '123456789012345678.12' second (18, 2)	XXXXXX
    # -        or iv < interval '100' second(3);
    
    stmt = """select count (*) from tsec13;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s7')
    #  expect count of 0
    stmt = """select count (*) from tsec21;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s8')
    #  expect count of 0
    stmt = """select count (*) from tsec162;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a17exp""", 'a17s9')
    
    _testmgr.testcase_end(desc)

