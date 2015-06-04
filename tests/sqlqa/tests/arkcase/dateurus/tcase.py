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
    
def test001(desc="""US and European DATE formats with INSERTS, UPDATES, and DELETES"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test001
    # johncl
    # 03/24/97
    # Test US and European DATE formats with INSERTS, UPDATES, and DELETES
    #
    # (1) INSERTs
    # Std format
    
    stmt = """insert into tbl001 values (date '1927-08-06');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl001 values (date '1997-01-30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # US format
    stmt = """insert into tbl001 values (date '06/12/1995');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl001 values (date '10/10/1994');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Euro format
    stmt = """insert into tbl001 values (date '20.02.1992');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl001 values (date '19.11.1993');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tbl001 order by dt desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    #  expect 6 rows with the following values in this order:
    #  	1997-01-30
    #  	1995-06-12
    #  	1994-10-10
    #  	1993-11-19
    #  	1992-02-20
    #  	1927-08-06
    
    #  (2) SELECTs
    #  Std format
    stmt = """select * from tbl001 where dt = date '1997-01-30';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #  expect 1 row with the requested date
    
    #  US format
    stmt = """select * from tbl001 where dt = date '10/10/1994';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s2')
    #  expect 1 row with the requested date
    
    #  Euro format
    stmt = """select * from tbl001 where dt = date '19.11.1993';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    # expect 1 row with the requested date
    
    # (3) UPDATEs with mixed formats
    # Std format + US format
    stmt = """update tbl001 set dt = date '1927-08-06' where dt = date '01/30/1997';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # US format + Euro format
    stmt = """update tbl001 set dt = date '06/12/1995' where dt = date '10.10.1994';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # Euro format + Std format
    stmt = """update tbl001 set dt = date '20.02.1992' where dt = date '1993-11-19';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tbl001 order by dt asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    # expect 6 rows with the following values in this order:
    # 	1927-08-06
    # 	1927-08-06
    # 	1992-02-20
    # 	1992-02-20
    # 	1995-06-12
    # 	1995-06-12
    
    # (4) DELETEs
    # Std format
    stmt = """delete from tbl001 where dt = date '1927-08-06';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    # US format
    stmt = """delete from tbl001 where dt = date '06/12/1995';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    # Euro format
    stmt = """delete from tbl001 where dt = date '20.02.1992';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select count (*) from tbl001;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    _testmgr.testcase_end(desc)

def test002(desc="""US and European TIME formats with INSERTS, UPDATES, and DELETES"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test002
    # johncl
    # 03/24/97
    # Test US and European TIME formats with INSERTS, UPDATES, and DELETES
    #
    # (1) INSERTs
    # Std & Euro format are the same
    
    stmt = """insert into tbl002 values (time '13:05:24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl002 values (time '01:25:45');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # US Format
    stmt = """insert into tbl002 values (time '10:40:05 AM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl002 values (time '11:02:55 PM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tbl002 order by tm desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #  expect 4 rows with the following values in this order:
    #  	23:02:55
    #  	13:05:24
    #  	10:40:05
    #  	01:25:45
    #
    #  (2) SELECTs
    #  Std & Euro format
    stmt = """select tm from tbl002 where tm = time '13:05:24';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s1')
    #  expect 1 row with the requested time value
    
    #  US format
    stmt = """select tm from tbl002 where tm = time '11:02:55 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s2')
    # expect 1 row with the requested time value
    
    # (3) UPDATEs with mixed formats
    # Std/Euro format + US format
    stmt = """update tbl002 set tm = time '13:05:24'
where tm = time '01:25:45 AM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # US format + Std/Euro format
    stmt = """update tbl002 set tm = time '10:40:05 AM'
where tm = time '23:02:55';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tbl002 order by tm asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    # expect 4 rows with the following values in this order:
    # 	10:40:05
    # 	10:40:05
    # 	13:05:24
    # 	13:05:24
    
    # (4) DELETEs
    # Std/Euro format
    stmt = """delete from tbl002 where tm = time '13:05:24';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    # US format
    stmt = """delete from tbl002 where tm = time '10:40:05 AM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select count (*) from tbl002;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    
    _testmgr.testcase_end(desc)

def test003(desc="""US and European TIMESTAMP formats with INSERTS, UPDATES, and DELETES"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # test003
    # johncl
    # 03/24/97
    # Test US and European TIMESTAMP formats with INSERTS, UPDATES, and DELETES
    #
    # (1) INSERTs
    # Std format
    
    stmt = """insert into tbl003 values (timestamp '1927-08-06:13:45:23.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl003 values (timestamp '1997-01-30:04:18:00.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # US format
    stmt = """insert into tbl003 values (timestamp '06/12/1995 11:06:56.000 PM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl003 values (timestamp '10/10/1994 09:50:15.000 AM');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # Euro format
    stmt = """insert into tbl003 values (timestamp '20.02.1992 01.24.59.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into tbl003 values (timestamp '19.11.1993 19.35.08.000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from tbl003 order by ts desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s0')
    #  expect 6 rows with the following values in this order:
    #  	1997-01-30 04:18:00.000000
    #  	1995-06-12 23:06:56.000000
    #  	1994-10-10 09:50:15.000000
    #  	1993-11-19 19:35:08.000000
    #  	1992-02-20 01:24;59.000000
    #       1927-08-06 13:45:23.000000
    #
    #  (2) SELECTs
    #  Std format
    stmt = """select * from tbl003 where ts = timestamp '1997-01-30:04:18:00.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s1')
    #  expect 1 row with the requested timestamp
    
    #  US format
    stmt = """select * from tbl003 where ts = timestamp '10/10/1994 09:50:15.000 AM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #  expect 1 row with the requested timestamp
    
    #  Euro format
    stmt = """select * from tbl003 where ts = timestamp '19.11.1993 19.35.08.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s3')
    # expect 1 row with the requested timestamp
    
    # (3) UPDATEs with mixed formats
    # Std format + US format
    stmt = """update tbl003 set ts = timestamp '1927-08-06 13:45:23.000'
where ts = timestamp '01/30/1997 04:18:00.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # US format + Euro format
    stmt = """update tbl003 set ts = timestamp '06/12/1995 11:06:56.000 PM'
where ts = timestamp '10.10.1994 09.50.15.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    # Euro format + Std format
    stmt = """update tbl003 set ts = timestamp '20.02.1992 01.24.59.000'
where ts = timestamp '1993-11-19 19:35:08.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from tbl003 order by ts asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s4')
    # expect 6 rows with the following values in this order:
    # 	1927-08-06 13:45:23.000000
    # 	1927-08-06 13:45:23.000000
    # 	1992-02-20 01:24;59.000000
    # 	1992-02-20 01:24;59.000000
    # 	1995-06-12 23:06:56.000000
    # 	1995-06-12 23:06:56.000000
    
    # (4) DELETEs
    # Std format
    stmt = """delete from tbl003 where ts = timestamp '1927-08-06 13:45:23.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    # US format
    stmt = """delete from tbl003 where ts = timestamp '06/12/1995 11:06:56.000 PM';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    # Euro format
    stmt = """delete from tbl003 where ts = timestamp '20.02.1992 01.24.59.000';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 2)
    
    stmt = """select count (*) from tbl003;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s5')
    
    _testmgr.testcase_end(desc)

