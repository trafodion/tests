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

import table1
from ...lib import hpdci
import defs

_testmgr = None
_testlist = []
_dci = None

#  testtype functional

#  #######################################
#  ###########   Testcase A0   ###########
#  #######################################

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='min max, primary key partitioned table distributed on different systems'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table table1
(
Int_1            INT SIGNED not null not droppable,
Large_2          LARGEINT not null,
Flt_1            FLOAT,
Ch_1             CHAR(10),
primary key( Int_1)
) number of partitions 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #partition
    #(
    #    add first key 0        location ${w_catalog1},
    #    add first key 50000000 location ${w_catalog2}
    #);
    
    stmt = """create index idx1 on table1
(Large_2 desc, Int_1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create unique index idx2 on table1
(Int_1, Large_2);"""
    output = _dci.cmdexec(stmt)
    
    table1._init(_testmgr)
    
    stmt = """update statistics for table table1 ON (Int_1);"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    
    ##expectplan ${test_dir}/a0exp a0s0
    stmt = """prepare XX from
select  min(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s2b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s4')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s4b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s5
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s6')
    
    # control query shape groupby(exchange(scan));
    
    stmt = """select  min(Large_2) + 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s6')
    
    ##expectplan ${test_dir}/a0exp a0s5b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s6b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s7
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s8')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s7b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s8b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s9
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s10')
    
    # control query shape groupby(exchange(scan));
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s11
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s12')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s11b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s12b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s13
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s14')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s13b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s14b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s15
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s16')
    
    # control query shape groupby(exchange(scan));
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s17
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s18')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s17b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s18b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s19
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s20')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s19b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a0exp""", 'a0s20b')
    
    # control query shape cut;
    
    #  #######################################
    #  ###########   Testcase A1   ###########
    #  #######################################
    
    _testmgr.testcase_end(desc)

def test002(desc='min max , primary key non-partitioned remote table'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table table1 cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table1
(
Int_1            INT SIGNED not null not droppable,
Large_2          LARGEINT,
Flt_1            FLOAT,
Ch_1             CHAR(10),
primary key(Int_1)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create index idx1
on table1 (Large_2 desc, Int_1);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index idx2
on table1 (Int_1, Large_2);"""
    output = _dci.cmdexec(stmt)
    
    table1._init(_testmgr)
    
    #set showshape on;
    
    stmt = """prepare XX from
select  min(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s2b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s4')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s4b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s5
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s6')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s5b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s6b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s7
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s8')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s7b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s8b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s9
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s10')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s9b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s10b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s11
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s12')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s11b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s12b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s13
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s14')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s13b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s14b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s15
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s16')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s15b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s16b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s17
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s18')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s17b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s18b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s19
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s20')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a1exp a1s19b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a1exp""", 'a1s20b')
    
    # control query shape cut;
    
    #  #######################################
    #  ###########   Testcase A2   ###########
    #  #######################################
    
    _testmgr.testcase_end(desc)

def test003(desc='min max , primary key partitioned local table'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table1
(
Int_1            INT SIGNED not null not droppable,
Large_2          LARGEINT,
Flt_1            FLOAT,
Ch_1             CHAR(10),
primary key(Int_1)
) number of partitions 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #partition
    #(
    #     add first key 0 location ${w_catalog1}
    #);
    
    stmt = """create index idx1
on table1 (Large_2 desc, Int_1);"""
    output = _dci.cmdexec(stmt)
    stmt = """create index idx2
on table1 (Int_1, Large_2);"""
    output = _dci.cmdexec(stmt)
    
    table1._init(_testmgr)
    
    #set showshape on;
    
    stmt = """prepare XX from
select  min(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s2b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s4')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Int_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s4b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s5
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s6')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s5b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s6b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s7
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s8')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s7b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s8b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s9
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s10')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s9b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s10b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s11
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s12')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s11b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s12b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s13
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s14')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s13b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s14b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s15
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s16')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s15b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s16b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s17
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s18')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s17b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s18b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s19
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s20')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a2exp a2s19b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a2exp""", 'a2s20b')
    
    # control query shape cut;
    
    #  #######################################
    #  ###########   Testcase A3   ###########
    #  #######################################
    
    _testmgr.testcase_end(desc)

def test004(desc='view, min max , primary key partitioned local table'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table1
(
Int_1            INT SIGNED not null not droppable,
Large_2          LARGEINT,
Flt_1            FLOAT,
Ch_1             CHAR(10),
primary key(Int_1)
) number of partitions 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #partition
    #(
    #    add first key 0 location ${w_catalog1}
    #);
    
    stmt = """create index idx1
on table1 (Large_2 desc, Int_1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idx2
on table1 (Int_1, Large_2);"""
    output = _dci.cmdexec(stmt)
    
    table1._init(_testmgr)
    
    #set showshape on;
    
    stmt = """create view vw1 (c1)
as select  min(Int_1) from table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare XX from
select  *
from vw1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a3exp a3s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a3exp""", 'a3s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  *
from vw1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a3exp a3s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a3exp""", 'a3s2b')
    
    # control query shape cut;
    
    stmt = """create view vw2 (vc1)
as select max(Int_1) from table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare XX from
select  *
from vw2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a3exp a3s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a3exp""", 'a3s4')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  *
from vw2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a3exp a3s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a3exp""", 'a3s4b')
    
    # control query shape cut;
    
    #  #######################################
    #  ###########   Testcase A4   ###########
    #  #######################################
    
    _testmgr.testcase_end(desc)

def test005(desc='min max , primary key partitioned local table, group by'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """drop view vw1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vw2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table table1
(
Int_1            INT SIGNED not null not droppable,
Large_2          LARGEINT,
Flt_1            FLOAT,
Ch_1             CHAR(10),
primary key(Int_1)
) number of partitions 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #partition
    #(
    #    add first key 0 location ${w_catalog1}
    #);
    
    stmt = """create index idx1
on table1 (Large_2 desc, Int_1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idx2
on table1 (Int_1, Large_2);"""
    output = _dci.cmdexec(stmt)
    
    table1._init(_testmgr)
    
    #set showshape on;
    
    stmt = """prepare XX from
select  min(Int_1)
from table1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s2')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Int_1)
from table1
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s2b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Int_1)
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s4')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Int_1)
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s4b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s5
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s6')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2) + 2
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s5b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s6b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s7
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s8')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) * 2
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s7b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s8b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa'
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s9
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s10')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Ch_1='xoa'
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s9b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s10b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa'
group by Large_2
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s11
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s12')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)
from table1 where Ch_1<'xoa'
group by Large_2
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s11b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s12b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s13
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s14')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  min(Large_2)
from table1 where Int_1=701753639
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s13b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s14b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s15
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s16')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2) + 1000000.0
from table1 where Int_1<=701753639
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s15b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s16b')
    
    # control query shape cut;
    
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s17
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s18')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0
from table1 where Int_1<>701753639
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    ##expectplan ${test_dir}/a4exp a4s17b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s18b')
    
    # control query shape cut;
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a4exp a4s19
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s20')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
select  max(Large_2)+1000000.0, max(Int_1)
from table1
group by Large_2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    ##expectplan ${test_dir}/a4exp a4s19b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a4exp""", 'a4s20b')
    
    # control query shape cut;
    
    stmt = """drop view vw2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop view vw1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table table1;"""
    output = _dci.cmdexec(stmt)
    
    #                  End of test case mmop001
    _testmgr.testcase_end(desc)

