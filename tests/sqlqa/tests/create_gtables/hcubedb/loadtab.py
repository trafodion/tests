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
    
def test001(desc='load tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # insert 10 rows into t0
    stmt = """insert into t0 values (0,0,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (2,2,2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (3,3,3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (4,4,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (5,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (6,6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (7,7,7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (8,8,8);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into t0 values (9,9,9);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # t1, t2, t3, t4, t5, t11, t12, are 10 rows similar to t10
    stmt = gvars.inscmd + """ t1 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t2 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t3 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t4 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t5 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t11 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t12 select * from t0;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # t6, t66, t7 are 100 rows
    stmt = gvars.inscmd + """ t6 select t1.a+10*t2.a,t1.a,t2.a from t1,t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t66 select t1.a+10*t2.a,t1.a,t2.a from t1,t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    stmt = gvars.inscmd + """ t7 select t1.a+10*t2.a,t1.a,t2.a from t1,t2;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # t8 is 1000 rows
    stmt = gvars.inscmd + """ t8 select t6.a+100*t1.a,t6.a,t1.a from t1,t6;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # t9 is 10000 rows
    stmt = gvars.inscmd + """ t9 select t8.a+1000*t1.a,t8.a,t1.a from t1,t8;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # t10 is 100000 rows
    stmt = gvars.inscmd + """ t10 select t8.a+1000*t6.a,t8.a,t6.a from t6,t8;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # cube1 is 100000 row (change t8.a < 100 if you want more rows)
    stmt = gvars.inscmd + """ cube1 select t1.a, t6.a, t8.a, t1.a, t6.a, t8.a, 'some text'
from t1, t6, t8 where t8.a < 100;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # cube2 is 1 million row, 500000 in each insert.
    stmt = gvars.inscmd + """ cube2
select t6.a, t1.a, t8.a, t1.a, t6.a, t8.a, 'some text'
from t1, t6, t8
where t6.a < 50;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube2
select t6.a, t1.a, t8.a, t1.a, t6.a, t8.a, 'some text'
from t1, t6, t8
where t6.a >= 50;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # cube3 is 10 million row
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a < 5;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 5
and
t6.a < 10;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 10
and
t6.a < 15;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 15
and
t6.a < 20;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 20
and
t6.a < 25;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 25
and
t6.a < 30;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 30
and
t6.a < 35;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 35
and
t6.a < 40;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 40
and
t6.a < 45;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 45
and
t6.a < 50;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 50
and
t6.a < 55;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 55
and
t6.a < 60;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 60
and
t6.a < 65;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 65
and
t6.a < 70;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 70
and
t6.a < 75;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 75
and
t6.a < 80;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 80
and
t6.a < 85;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 85
and
t6.a < 90;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 90
and
t6.a < 95;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube3
select t6.a, t2.a, t1.a, t8.a,  t6.a+ (t2.a*100)+ (t1.a*1000), t6.a+(t2.b*100)+(t1.a*1000)+(t8.a*10000), 'some text'
from  t1, t2, t6, t8
where t6.a >= 95;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # transpose does all of insert under single transaction
    # on small systems, this can pin TMF audit
    # on any system, it can cause long backout when there is an error
    # breaking up upsert using load into 10M row chunks
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 0 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)

    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 1 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
 
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 2 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 3 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 4 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 5 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 6 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 7 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 8 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    stmt = gvars.inscmd + """ cube4
select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
,x1+x2*10+x3*100+x4*1000+x5*10000
,x1+x2*10+x3*100
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
from (values(1)) t
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5
transpose 0,1,2,3,4,5,6,7,8,9 as x6
transpose 0,1,2,3,4,5,6,7,8,9 as x7
transpose 9 as x8
;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_error_msg(output)
    
    # likewise break up insert for even larger cube5, not automatically done
    # this is still 100M row chunks, so beware of audit trail problems
    
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 0 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 1 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 2 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 3 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 4 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 5 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 6 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 7 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 8 as x9
    #;
    #upsert using load into cube5
    #select  x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000
    #       ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000
    #         ,x1+x2*10+x3*100+x4*1000+x5*10000+x6*100000+x7*1000000+x8*10000000+x9*100000000
    #from (values(1)) t
    #transpose 0,1,2,3,4,5,6,7,8,9 as x1
    #transpose 0,1,2,3,4,5,6,7,8,9 as x2
    #transpose 0,1,2,3,4,5,6,7,8,9 as x3
    #transpose 0,1,2,3,4,5,6,7,8,9 as x4
    #transpose 0,1,2,3,4,5,6,7,8,9 as x5
    #transpose 0,1,2,3,4,5,6,7,8,9 as x6
    #transpose 0,1,2,3,4,5,6,7,8,9 as x7
    #transpose 0,1,2,3,4,5,6,7,8,9 as x8
    #transpose 9 as x9
    #;
    
    _testmgr.testcase_end(desc)

