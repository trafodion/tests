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
    
def test001(desc='min , primary key'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #expect purge
    
    stmt = """create table table1
(
Ch_1             CHAR(10) not null,
Dec_1            DECIMAL(9, 0) SIGNED,
IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH,
IntvlHr_Mi_2     INTERVAL HOUR(2) TO MINUTE,
Int_1            INT ,
Int_2            INT ,
primary key( Ch_1)
) number of partitions 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #partition(
    #    add first key 'aaa' location ${w_catalog1},
    #    add first key 'ppp' location ${w_catalog2}
    #);
    
    stmt = """create index idx1 on table1
(Dec_1 desc, Ch_1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create index idx2 on table1
(Ch_1, Dec_1) ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab2
(
Ch_1             CHAR(10),
Dec_1            DECIMAL(9, 0) SIGNED,
IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH,
IntvlHr_Mi_2     INTERVAL HOUR(2) TO MINUTE,
Int_1            INT UNSIGNED not null not droppable ,
Int_2            INT UNSIGNED    

) no partition;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tab3
(
Ch_1             CHAR(10)
) no partition;"""
    output = _dci.cmdexec(stmt)
    
    table1._init(_testmgr)
    
    stmt = """update statistics for table table1 ON (Int_1);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into tab2 select * from table1;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into tab3 select Ch_1 from table1;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    stmt = """prepare XX from
select  min(Ch_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1bb
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare XX from
insert into tab3
select  min(Ch_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
insert into tab3
select  min(Ch_1)
from table1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s1b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # control query shape cut;
    
    stmt = """prepare XX from
update tab2 set Dec_1 = Dec_1 + 1
where Ch_1 >
(select  min(Ch_1)
from table1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s3
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
update tab2 set Dec_1 = Dec_1 + 1
where Ch_1 >  (select  min(Ch_1)
from table1)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    ##expectplan ${test_dir}/a0exp a0s3b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 0)
    
    # control query shape cut;
    stmt = """prepare XX from
insert into   tab2
select  *
from table1
where Ch_1 > (select min(t1.Ch_1) from table1 t1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan ${test_dir}/a0exp a0s5
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    # #expectfile $test_dir/a0exp a0s6
    # depends on plan or access order, different errors may return
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
insert into   tab2
select  *
from table1
where Ch_1 > (select min(t1.Ch_1) from table1 t1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """;"""
    output = _dci.cmdexec(stmt)
    
    ##expectplan ${test_dir}/a0exp a0s5b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/a0exp a0s6b
    # depends on plan or access order, different errors may return
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # control query shape cut;
    
    stmt = """prepare XX from
update  tab2 set
Ch_1 = 'kYaOFJfcma',
Dec_1 = 223228343,
IntvlYr_Mn_1 = INTERVAL '83-8' YEAR(2) TO MONTH,
IntvlHr_Mi_2 = INTERVAL '5:39' HOUR(2) TO MINUTE,
Int_1 = 2012282033,
Int_2 = 1615915
where  Ch_1 > (select min(t1.C1) from table1 t1)
and Ch_1 <(select max(t2.Ch_1) from table1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    
    ##expectplan ${test_dir}/a0exp a0s7
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
update  tab2 set
Ch_1 = 'kYaOFJfcma',
Dec_1 = 223228343,
IntvlYr_Mn_1 = INTERVAL '83-8' YEAR(2) TO MONTH,
IntvlHr_Mi_2 = INTERVAL '5:39' HOUR(2) TO MINUTE,
Int_1 = 2012282033,
Int_2 = 1615915
where  Ch_1 > (select min(t1.C1) from table1 t1)
and Ch_1 <(select max(t2.Ch_1) from table1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4003')
    
    ##expectplan ${test_dir}/a0exp a0s7b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    
    # control query shape cut;
    
    stmt = """prepare XX from
delete from  tab2
where  Ch_1 > (select min(t1.C1) from table1 t1)
and Ch_1 <(select max(t2,Ch_1) from table1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3129')
    
    ##expectplan ${test_dir}/a0exp a0s9
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    
    # control query shape groupby(exchange(scan));
    stmt = """prepare XX from
delete from  tab2
where  Ch_1 > (select min(t1.C1) from table1 t1)
and Ch_1 <(select max(t2.Ch_1) from table1 t2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8822')
    
    ##expectplan ${test_dir}/a0exp a0s9b
    stmt = """explain options 'f' XX;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute XX;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '29431')
    
    # control query shape cut;
    
    #                  End of test case mmop003
    
    _testmgr.testcase_end(desc)

