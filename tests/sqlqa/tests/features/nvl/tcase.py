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
    
def test001(desc="""A01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A01
    #  Description:        The NVL function testing,
    #                          Select NVL(NULL, 2) from (values(1)) x(a)
    #                            -- Should return 2
    #                          Select NVL(1, 2) from (values(1)) x(a)
    #                            -- Should return 1
    #                      This is a positive test on table optable and views.
    #
    # =================== End Test Case Header  ===================
    
    ##expectfile ${test_dir}/a01exp a01s0
    stmt = """select nvl(cast(null as char(1)), c2), nvl(cast(null as decimal(5)), d1)
from OPTABLE order by 1,2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectfile ${test_dir}/a01exp a01s1
    stmt = """select NVL(n3, (SELECT n3 from voptbl 
where vc1 = '~!#$%^&')),
t1, d2, n3, trim(z), vc1
from  OPTABLE 
where t1 < date '1980-12-30'
order by vc1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectfile ${test_dir}/a01exp a01s1a
    stmt = """select NVL(n3, (SELECT n3 from voptbl 
where vc1 = '~!#$%^&')),
t1, d2, n3, trim(z), vc1
from  OPTABLE 
where nvl((select hire_date from emp 
where hire_date > date '1977-05-02' and hire_date is not null),
(select v.t1 from voptbl v
where v.t1 < date '1980-12-30' and
v.t1 in (date '1900-12-01',
date '2006-06-17',
date '3030-06-15')
group by v.t1))
is not null
order by z, vc1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectfile ${test_dir}/a01exp a01s1a
    stmt = """select NVL(n3, (SELECT n3 from voptbl 
where vc1 = '~!#$%^&')),
t1, d2, n3, trim(z), vc1
from  OPTABLE 
where nvl((select hire_date from emp 
where hire_date > date '1977-05-02' and hire_date is not null),
(select v.t1 from voptbl v
group by v.t1
having v.t1 < date '1980-12-30' and
v.t1 in (date '1900-12-01',
date '2006-06-17',
date '3030-06-15')))
is not null
order by z, vc1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    ##expectfile ${test_dir}/a01exp a01s2
    stmt = """select NVL('~!#$%^&', (SELECT c3 from voptbl 
where vc1 = '~!#$%^&')),
NVL(0, (SELECT zi2 from voptbl 
where vc1 = '~!#$%^&')),
t1, d2, n3, vc1
from OPTABLE 
where t1 < date '1980-12-30';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select vc1, b2, f2,
NVL((select b2 from voptbl where b2 is null),
(select ACOS(COS(f2))
from voptbl where f2 > 8.55E-1 and f2 < 9.0E-01))
from OPTABLE 
where vc1 in ('\$vcR1~', '~!#$%^&', '\$vcZERO~')
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)

    stmt = """select vc1, b2, f2,
NVL((select b2 from voptbl where b2 is null),
(select ACOS(COS(f2))
from voptbl where f2 > 8.55E-1 and f2 < 9.0E-01))
from OPTABLE 
group by vc1, b2, f2
having nvl(vc1, (select last_name from emp 
group by last_name
having last_name in ('LName B', 'LName C', 'LName last')))
in ('\$vcR1~', '~!#$%^&', '\$vcZERO~')
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
 
    stmt = """select vc1, f2,
NVL((select ACOS(COS(f2))
from voptbl 
where f2 > 8.55E-1 and f2 < 9.0E-01
group by vc1, f2
having vc1 in ('\$vcR1~', '\$vcR3~')),
(select ACOS(COS(f2)) from voptbl 
where trim(z) is null))
from OPTABLE 
group by vc1, f2
having vc1 in ('\$vcR1~', '~!#$%^&', '\$vcZERO~')
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 3)
    
    stmt = """select NVL((select ACOS(COS(psc))
from voptbl v
where v.psc > 7.99 and v.psc < 9
group by v.vc1, v.psc
having v.vc1 in ('\$vcR1~', '\$vcR3~')),
(select ACOS(COS(f2)) from voptbl 
where trim(z) is null))
from OPTABLE 
group by vc1
having vc1 in ('\$vcR1~', '~!#$%^&', '\$vcZERO~')
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4a')
    
    stmt = """select NVL((select ACOS(COS(psc))
from voptbl V
where v.psc > 7 and v.psc < 9
group by vc1, psc
having nvl(vc1, vc1) in ('\$vcR1~', '\$vcR3~')),
(select ACOS(COS(f2)) from voptbl 
where trim(z) is null))
from OPTABLE 
group by vc1
having vc1 in ('\$vcR1~', '~!#$%^&', '\$vcZERO~')
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '4007')
    
    stmt = """select z, NVL(p1, p1) NNULLp1, NVL('n', 'N') NULLANULL,
NVL(b2, 109.99109) B2V,
NVL((select c1 from OPTABLE where c1 is null), 'C1-NULL') C1N,
NVL((select u1 from OPTABLE where u1 is null), 12345) U1V,
NVL((select d1 from OPTABLE where d1 is null), 99.12) D1V
from voptbl 
where trim(z) > 'Row07';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    
    stmt = """select vv.vc1,
NVL(vv.z, vv.vc1) CHARVALUE,
NVL(vv.b2, vv.b1) FLOATVALUE,
v.vc1,
NVL(v.z, v.vc1) CHARVALUE,
NVL(v.b2, v.b1) FLOATVALUE
from voptbl1 vv, voptbl v
group by vv.vc1, vv.z, vv.b1, vv.b2,
v.vc1, v.z, v.b1, v.b2
order by vv.vc1, 2, 3, v.vc1, 5, 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 49)
    
    stmt = """select t.z, NVL(v.z, v.vc1), NVL(t.c1, v.c1),
NVL(v.vc1, t.c3),
NVL(substring(t.z from 5 for 1), trim(v.z))
from OPTABLE t, voptbl1 v
group by t.z, v.z, v.vc1, t.c1, v.c1, t.c3
having trim(t.z) in ('NULLS', 'ZEROS', 'null')
order by 1, 2, 3, 4, 5;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 14)
    
    stmt = """select t.vc1, t.d3, v.n3, sum(nvl(t.d3, v.n3)), avg(nvl(t.d3, v.n3))
from OPTABLE t, voptbl v
group by t.vc1, t.d3, v.n3
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select vc1, c3, nvl(c3, 'ABC'), n3, u2
from OPTABLE 
where vc1 = (select NVL(v.vc1, (select v2.vc1
from voptbl v2
where v2.vc1 = '\$vcR4~'))
from voptbl v, voptbl1 vv)
group by vc1, c3, n3, u2
order by 1, 2, 3, 4;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """set param ?p 3.4;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select z, nvl(c1, c1),
nvl(d3, mod(cast(floor(avg(mod(zi3, 4))) as integer), 4)),
nvl(n2,
abs(-9342.764134) / abs(0.5) * DEGREES(-.66666668) - abs(-?p))
from OPTABLE 
group by z, c1, d3, n2
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    
    stmt = """select u2, nvl(nullifzero(u2), 9999999)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11')
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """update OPTABLE set u3 = nvl((select nullifzero(dept_num)
from emp 
where dept_num = 0),
(select nullifzero(dept_num)
from emp 
where dept_num = 0));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    stmt = """select u3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11a')
    
    stmt = """update OPTABLE set u3 =
nvl((select nullifzero(dept_num)
from emp 
where dept_num = 0),
(select nvl(nullifzero(dept_num), 001)
from emp 
group by dept_num
having dept_num in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    stmt = """select u3 from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s11b')
    
    ##expect any *6 row(s) selected*
    stmt = """select first_name, last_name, ASCII(RIGHT(first_name, 8)),
REPLACE(first_name, 'R', RIGHT(first_name, 9)),
hire_date, last_name,
case
when nvl(cast(null as pic x(2)), (RIGHT(last_name, 7))) = 'RY'
then nvl(cast(null as pic x(50)), 'last name is JERRY')
when nvl(first_name, last_name) > 'JERRY'
then RIGHT(last_name, 8)
else nvl(cast(null as varchar(3)),RIGHT(first_name, 10))
end
from emp 
where RIGHT(last_name, 7) > 'JE'
group by first_name, last_name, hire_date
order by first_name asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    ##expect any *6 row(s) selected*
    stmt = """select first_name, last_name, ASCII(RIGHT(first_name, 8)),
REPLACE(first_name, 'R', RIGHT(first_name, 9)),
hire_date, last_name,
case
when nvl(cast (nullifzero(cast(null as float
)
)
as varchar(1)
),    

(RIGHT(last_name, 7)))  = 'RY'
then nvl(cast(null as pic x(50)), 'last name is JERRY')
when nvl(first_name, last_name) > 'JERRY'
then RIGHT(last_name, 8)
else nvl(cast(null as varchar(3)),RIGHT(first_name, 10))
end
from emp 
where RIGHT(last_name, 7) > 'JE'
group by first_name, last_name, hire_date
order by first_name asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s12')
    
    stmt = """prepare s from
select (select vc1 from voptbl group by vc1)
from OPTABLE;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """execute s;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8401')
    
    stmt = """rollback work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""A02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     A02
    #  Description:        The NVL function testing,
    #                          Select NVL(NULL, 2) from (values(1)) x(a)
    #                            -- Should return 2
    #                          Select NVL(1, 2) from (values(1)) x(a)
    #                            -- Should return 1
    #                      This is a positive test on joined tables and views.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expectfile ${test_dir}/a02exp a02s0
    stmt = """insert into playt3 
(binary_signed, binary_32_u, binary_64_s, small_int, medium_int)
(select 99,
nvl(n2, d2),
123456789012345.333,
nvl(u1, (select v.u1 from voptbl v
where u1 is null)),
nvl(u2, u2)
from OPTABLE 
where vc1 = '\$vcRNULL~'
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    ##expectfile ${test_dir}/a02exp a02s1
    stmt = """insert into emp 
(first_name, last_name, dept_num, salary,
marital_status, hire_date, start_time)
(select nvl((select trim(vc1) from OPTABLE 
where vc1 = '\$vcRNULL~'), trim(vc1)),
nvl(c1, c3),
nvl(ps9, (select cast(v.ps9 / 3 as numeric(4,0)) from voptbl v
where v.ps9 = 12345)),
cast(nvl(n1, (select small_int from playt3 
where medium_int is null and
small_int = 0))
as numeric(8,2)),
123,
nvl((select
cast(cast(substring(cast(d_t_m_e as char(26)), 1, 10) as char(10)) as date)
from DAYTAB 
where cast(d_t_m_e as varchar(26)) in
('0001-12-13 00:00:00.000000', '0001-12-13 00:00:00.000001'))
, t1),
nvl((select d_t_m_e from DAYTAB 
where d_t_m_e = timestamp '1901-05-10 15:19:59.300000'),
(select d_t_m_e from DAYTAB 
where d_t_m_e = timestamp '1999-12-31 23:59:59.999999'))
from OPTABLE 
where ps9 = 4598);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    ##expectfile ${test_dir}/a02exp a02s2
    stmt = """select hire_date,
nvl(cast(hire_date as char(11)),
concat(concat(char(ASCII(first_name)), '.'), last_name))
first_name, last_name
from emp 
where hire_date = (select hire_date
from emp 
where ASCII(first_name) = 106)
group by hire_date, last_name, first_name
order by 2 asc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """update emp set
hire_date = (select cast(nvl(
(select td from play_tabA),
(select td from play_tabB 
where tt = timestamp '2006-05-08 15:05:59.400000'
)
)
as date
)
from play_tabA 
),
marital_status = (select(nvl( (select n2 from OPTABLE where n2 is null),
999
)
)
from voptbl where n2 is null
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """select *
from emp 
order by first_name, last_name, dept_num, salary,
marital_status, hire_date, start_time;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select nvl(cast(hire_date as char(10)), max(INSERT(last_name, 5, 2, 'max'))),
last_name,
nvl(cast(hire_date as char(10)), min(INSERT(last_name, 1, 2, 'mm'))),
hire_date
from emp 
where last_name not in
(select nvl(cast(hire_date as varchar(10)), last_name)
from emp 
where REPEAT(first_name, 2) like 'HOWARD%OWARD%')
group by hire_date, last_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """set param ?u 99.12;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update OPTABLE set vc1 =
(select(nvl(
(select last_name
from emp 
where hire_date is not null and
first_name = 'FName B'
),
(select m_n from DAYTAB 
where d_n = 'Friday')
)
)
from emp 
where first_name = 'FName B')    

, b1 = (select(nvl((select salary
from emp 
where salary is null and
first_name = 'First Name')
, ?u)
)
from emp 
where first_name = 'FName B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    stmt = """update OPTABLE set vc1 =
(select(nvl(
(select last_name
from emp 
where hire_date is not null and
first_name = 'FName B'
),
(select m_n from DAYTAB 
where d_n = 'Friday')
)
)
from emp 
where first_name = 'FName B')    

, b1 = (select(nvl((select salary
from emp 
where salary is null and
first_name = 'First Name')
, (?u - 0.12 * 1 + 0.12))
)
from emp 
where first_name = 'FName B');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 11)
    
    stmt = """select z, vc1, b1 from OPTABLE order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s7')
    
    stmt = """set param ?s 'NVL';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select nvl((select cast(max(salary) as varchar(12))
from emp 
where last_name = 'JERRY')
, (select LPAD(first_name, 1, SUBSTRING(last_name from 1 for 10))
from emp 
where last_name = 'JERRY')),
nvl((select cast(start_time as pic x(12))
from emp 
where start_time is null and salary is not null)
, (select REPLACE(first_name, 'E', LPAD(first_name, 0, '$'))
from emp 
where last_name = 'JERRY')),
nvl((select cast(start_time as pic x(12))
from emp 
where start_time is null and salary is not null)
, (select INSERT('what is your first name', 9, ASCII('our'), 'A')
from emp 
where last_name = 'JERRY'))
from emp 
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s8')
    
    stmt = """select nvl((select upper(cast(salary as varchar(12)))
from emp 
where last_name = 'JERRY')
, (select distinct(trim(last_name)) from emp 
where last_name in ('JERRY', 'ME', 'haha'))),
nvl((select upper(cast(salary as varchar(12)))
from emp 
where last_name = 'JERRY'),
cast(?s as pic x(5))),
nvl(cast(hire_date as varchar(10)), cast(?s as pic x(15)))
from emp 
group by last_name, hire_date
order by 1, 2, 3;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s9')
    
    stmt = """set param ?date '9999-12-31';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update emp 
set hire_date = cast((select cast(nvl(t1, cast(?date as date)) as date)
from voptbl 
where t2 is null) as date);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 12)
    
    stmt = """select first_name, last_name, hire_date,
nvl(cast(start_time as char(32)), 'TBD')
from emp 
order by 1, 2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """rollback;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # stmt = """begin work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    stmt = """insert into play_likeA 
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl((select t1 from OPTABLE 
where t1 in (date '1981-08-21', date '2006-05-16')),
date '2006-05-08'),
nvl((select start_time
from emp 
where start_time = timestamp '1977-05-02 08:12:00.110000'),
timestamp '2006-05-08 15:05:59.400000'),
nvl((select intv_hs from play_tabA 
where intv_hs is null),
interval '05:25:00.000001' hour to second),
nvl((select intv_md from play_tabA 
where intv_hs is null),
interval '55-09' year to month),
nvl((select intv_y2 from play_tabA),
interval '55' year(2)),
nvl((select intv_h2 from play_tabA),
interval '11' hour));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    # #expect any *Subquery returns no row, null value is returned.*
    # fixed in QCD-5 0712
    stmt = """insert into play_tabB 
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl((select td
from play_tabA 
where td is null),
date '2006-05-08'),
nvl((select tt
from play_tabA 
where tt is null),
timestamp '2006-05-08 15:05:59.400000'),
nvl((select intv_hs
from play_likeA 
where intv_hs is null),
interval '05:15:38.777777' hour to second),
nvl(interval '08-10' year to month,
interval '03-07' year to month),
nvl((select intv_y2
from play_tabA 
where intv_y2 = interval '55' year(2)),
interval '88' year(2)),
nvl(interval '03' hour, interval '11' hour));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from play_likeA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """select * from play_tabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """set param ?td '2000-12-31';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?tt '2006-05-08 12:00:00.123456';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i_hs '09:09:00.123456';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i_md '09-09';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i_y2 '33';"""
    output = _dci.cmdexec(stmt)
    stmt = """set param ?i_h2 '96';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into play_tabB 
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(cast(null as date), cast(?td as date)),
nvl(cast(null as timestamp), cast(?tt as timestamp)),
nvl(cast(null as interval hour to second),
cast(?i_hs as interval hour to second)),
nvl(cast(null as interval year to month),
cast(?i_md as interval year to month)),
nvl(cast(null as interval year(2)),
cast(?i_y2 as interval year(2))),
nvl(cast(null as interval hour),
cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select td, tt, intv_hs, intv_md, intv_y2, intv_h2
from play_tabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """insert into play_tabB 
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(cast(null as date), cast(?td as date)),
nvl(cast(null as timestamp), cast(?tt as timestamp)),
nvl(cast(null as interval hour to second),
(select intv_hs
from play_tabA 
where cast(intv_hs as char(5)) = '05-15')),
nvl(cast(null as interval year to month),
cast(?i_md as interval year to month)),
nvl(cast(null as interval year(2)),
cast(?i_y2 as interval year(2))),
nvl(cast(null as interval hour),
cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select td, tt, intv_hs, intv_md, intv_y2, intv_h2
from play_tabB 
order by 1, 2, 3, 4, 5, 6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """insert into play_tabB 
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(cast(null as date), cast(?td as date)),
nvl(cast(null as timestamp), cast(?tt as timestamp)),
nvl(cast(null as interval hour to second),
(select intv_hs
from play_tabA 
where cast(intv_hs as char(5)) = '99-99')),
nvl(cast(null as interval year to month),
cast(?i_md as interval year to month)),
nvl(cast(null as interval year(2)),
cast(?i_y2 as interval year(2))),
nvl(cast(null as interval hour),
cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select count(*)
from play_tabB;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s15')
    
    stmt = """create view emp_view (first_name, last_name, dept_num,
salary, marital_status, hire_date, start_time) as
(select first_name, last_name,
nvl((select p3 from optable
where p3 = -12390), 333),
salary,
13,
nvl(cast(null as date), hire_date),
start_time
from emp);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from emp_view;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    # stmt = """rollback;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""N01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     N01
    #  Description:        The is a NVL function negative test.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """select nvl(p1, t1), nvl(salary, (select t3 from OPTABLE))
from voptbl_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(start_time, hire_date)
from emp_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(start_time, last_name)
from emp_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl((select t2 from OPTABLE), last_name)
from emp_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select first_name, last_name, hire_date
from emp_ne
where nvl(first_name, last_name) = 'b987654321'
group by first_name, last_name, hire_date
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select first_name, last_name, nvl(hire_date, date '2006-05-08')
from emp_ne
where nvl(salary, last_name) = 'b987654321'
group by first_name, last_name
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(start_time, timestamp '0901-01-01 01:59:50.400000')
from emp_ne
group by start_time
having start_time in (nvl(start_time, null));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(start_time, timestamp '0901-01-01 01:59:50.400000')
from emp_ne
group by nvl(start_time, null))
having start_time in ('09/23/1908 12:34:00.067222');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(d3, t3) from voptbl_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(trim(z), t3) from voptbl_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    ##expect any *4049*
    stmt = """select nvl(trim(z), psc) from voptbl_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(td, tt) from play_tabA_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select td, nvl(intv_hs, intv_h2) from play_tabA_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select td, nvl(td, intv_y2) from play_tabA_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into play_tabA_ne
(td, intv_hs, intv_md, intv_y2, intv_h2)
values (date '2666-12-01',
nvl(0, (select t2 from OPTABLE 
where trim(z) = '$vcZERO~')),
interval '11-11' year to month,
interval '11' year(2),
interval '11' hour);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """update play_tabB_ne
set td = (select nvl('ops', tt) from play_tabA);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """delete from play_tabB_ne
where td = (select nvl('p90', psc) from voptbl);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into play_tabB_ne
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(date '2006-05-17', cast(?td as date)),
nvl(timestamp '2006-05-17 10:02:01.000006',
cast(tt as timestamp)),
nvl(interval '10:02.000000' hour to second,
cast(?i_hs as interval hour to second)),
nvl(interval '06-06' year to month, ?i_md),
nvl(interval '00' year(4),
cast(?i_y2 as interval year(2)),
nvl(inteval '00' hour, cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into play_tabB_ne
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(date '2006-05-17', cast(?td as date)),
nvl(timestamp '2006-05-17 10:02:01.000006',
cast(?tt as timestamp)),
nvl(interval '10:02:00.000000' hour to second,
cast(?i_hs as interval hour to second)),
nvl(interval '06-06' year to month,
cast(?i_md as interval hour to second)),
nvl(interval '00' year(4),
cast(?i_y2 as interval year(2))),
nvl(interval '00' hour(2), cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into play_tabB_ne
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(null, cast(?td as date)),
nvl(null, cast(tt as timestamp)),
nvl(null, cast(?i_hs as interval hour to second)),
vnl(null, cast(?i_md as interval hour to second),
nvl(null, cast(?i_y2 as interval year(2)),
nvl(null, cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into play_tabB_ne
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(date '2006-05-17', cast(?td as date)),
nvl(timestamp '2006-05-17 10:02:01.000006',
cast(?tt as timestamp)),
nvl(interval '10:02:00.000000' hour to second,
cast(?i_hs as interval hour to second)),
nvl(interval '06-06' year to month,
cast(?i_y2 as interval year to month)),
nvl(null, cast(?i_y2 as interval year(2))),
nlv(interval '00' hour(2), cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """insert into play_tabB_ne
(td, tt, intv_hs, intv_md, intv_y2, intv_h2)
values (nvl(null, cast(?td as date)),
nvl(null, cast(tt as timestamp)),
nvl(null, cast(?i_hs as interval hour to second)),
nvl(null, cast(?i_md as interval hour to second),
lnv(null, cast(?i_y2 as interval year(2)),
nvl(null, cast(?i_h2 as interval hour)));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    ##expectfile ${test_dir}/a04exp a04s5
    stmt = """select substring(SPACE(cast(ascii(
REPEAT(UPPER(first_name), 5)) / 10 as integer)), 1, 14),
first_name,
last_name, CHAR(ascii(REPEAT(last_name, 10))),
min(REPEAT(REPEAT(first_name, 5), 2)),
case
when REPEAT(UPSHIFT(last_name), 2) = 'JERRYJERRY'
then 'last name is JERRY'
when REPEAT(UCASE(last_name), 3) > 'JERRYJERRY'
then (select nvl(c2) from OPTABLE)
else 'who are you?'
end
from emp_ne
group by last_name, first_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(99.6, 33.9, 100) from optable_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(123) from optable_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(aaa) from optable_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(, 'aaa') from optable_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl('aaa',) from optable_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """select nvl(12345,) from optable_ne;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

