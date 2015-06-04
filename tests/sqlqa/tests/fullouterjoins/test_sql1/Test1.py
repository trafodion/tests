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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='union tests'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a
from t3
where (33 < (75 + b))
) T1
union all
select c
from (
Select c
from t3
where (e = 21)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s1')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
select e, a
from (
Select e, a
from t5
where (b > 22)
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, d_l, e_r_r
from (
Select e, b, d
from t4
where (c = d)
) T1(e_l, b_l, d_l)
left join (
select b_l, e_r, a_r
from (
Select b_l, e_r, a_r
from (
Select c, b, d
from t5
where (37 < b)
) T1(c_l, b_l, d_l)
full join (
Select e, c, a
from t2
where ((75 + 60) = c)
) T2(e_r, c_r, a_r)
on (b_l = 32)
) T1
union all
select e_l, d_l, e_r_l_r
from (
Select e_l, d_l, e_r_l_r, b_r_l_r
from (
Select e, d
from t5
where (e = (65 - e))
) T1(e_l, d_l)
left join (
Select b_r_l, e_l_l, e_r_l, c_r_r, d_l_r
from (
Select e_l, e_r, b_r
from (
Select e
from t1
where (a > 63)
) T1(e_l)
left join (
Select e, c, b
from t4
where (e = e)
) T2(e_r, c_r, b_r)
on (22 = e_l)
) T1(e_l_l, e_r_l, b_r_l)
left join (
Select a_l, d_l, e_r, c_r
from (
Select c, a, b, d
from t4
where (31 = b)
) T1(c_l, a_l, b_l, d_l)
left join (
Select e, c
from t4
where (d = d)
) T2(e_r, c_r)
on (34 < a_l)
) T2(a_l_r, d_l_r, e_r_r, c_r_r)
on (64 = 89)
) T2(b_r_l_r, e_l_l_r, e_r_l_r, c_r_r_r, d_l_r_r)
on ((38 - d_l) = 1)
) T2
) T2(b_l_r, e_r_r, a_r_r)
on (98 > 53)
) T2
) T1
union all
select e, a
from (
Select e, a
from t5
where (70 > c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t4
where (b < 42)
) T1
union all
select c_l
from (
Select c_l, c_r, d_r
from (
Select c
from t2
where (((e * (e - 73)) - 26) = (b - c))
) T1(c_l)
full join (
Select c, d
from t5
where (d < a)
) T2(c_r, d_r)
on ((30 - 52) = c_r)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t4
where (12 = 82)
) T1
union all
select e
from (
Select e, d
from t4
where (d = 70)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
select a
from (
Select a
from t3
where (87 < 74)
) T1
union all
select e
from (
Select e, c, b
from t2
where (10 < (a + 9))
) T2
) T1
union all
select e
from (
Select e, d
from t1
where (a > (62 + b))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (30 < 1)
) T1
union all
select e
from (
Select e, d
from t1
where (a < 97)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b
from t1
where (a = (86 - b))
) T1
union all
select c
from (
select c
from (
Select c, d
from t4
where (71 = 55)
) T1
union all
select a
from (
Select a
from t4
where (((45 - c) + 50) = 75)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t3
where (14 = d)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a
from t5
where (32 = e)
) T1
union all
select b_l, d_l
from (
select b_l, d_l
from (
Select b_l, d_l, e_r, b_r
from (
Select b, d
from t2
where (78 < (87 - 88))
) T1(b_l, d_l)
left join (
Select e, b
from t1
where (d < c)
) T2(e_r, b_r)
on ((4 - (d_l + ((b_r * 48) - e_r))) = b_r)
) T1
union all
select a_l, a_l_r
from (
Select a_l, a_l_r
from (
Select e, c, a
from t1
where (b < 72)
) T1(e_l, c_l, a_l)
inner join (
select a_l
from (
Select a_l, a_r
from (
Select c, a, b
from t3
where (23 = c)
) T1(c_l, a_l, b_l)
inner join (
Select a
from t2
where (a = (57 + ((50 * e) * e)))
) T2(a_r)
on ((a_l * (38 * (((69 + a_r) + (a_r * a_r)) * a_r))) = 23)
) T1
union all
select c
from (
Select c
from t4
where (d < 44)
) T2
) T2(a_l_r)
on (a_l_r = ((43 + 65) - 9))
) T2
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l
from (
select e_l_l
from (
select e_l_l, a_r, b_r
from (
Select e_l_l, a_r, b_r
from (
Select e_l, c_r
from (
Select e, c
from t5
where (c = (53 - a))
) T1(e_l, c_l)
left join (
Select c, d
from t2
where (40 = (e - 59))
) T2(c_r, d_r)
on ((2 * 18) < e_l)
) T1(e_l_l, c_r_l)
full join (
Select a, b
from t1
where (d = ((10 - (90 * 77)) + 64))
) T2(a_r, b_r)
on ((e_l_l + e_l_l) = (36 - 95))
) T1
union all
select e, b, d
from (
Select e, b, d
from t4
where ((e - 24) > c)
) T2
) T1
union all
select c
from (
Select c
from t2
where (47 > a)
) T2
) T1
union all
select d_l
from (
Select d_l, c_l_l_r, e_r_r
from (
Select d
from t1
where (c < 90)
) T1(d_l)
inner join (
Select c_l_l, d_r_l, e_r
from (
Select c_l, c_r, d_r
from (
Select c
from t4
where (80 < 98)
) T1(c_l)
left join (
Select c, d
from t4
where (e > a)
) T2(c_r, d_r)
on (c_l > d_r)
) T1(c_l_l, c_r_l, d_r_l)
inner join (
Select e
from t2
where (e = e)
) T2(e_r)
on (((c_l_l * 39) + (d_r_l * 37)) < 76)
) T2(c_l_l_r, d_r_l_r, e_r_r)
on (e_r_r = 16)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, e_r
from (
Select b_l, e_r, a_r
from (
select e, b
from (
Select e, b
from t1
where (46 < a)
) T1
union all
select c, a
from (
Select c, a, b, d
from t2
where (89 = ((d * (12 + 73)) + e))
) T2
) T1(e_l, b_l)
left join (
Select e, a
from t2
where (e < (75 * (1 * 0)))
) T2(e_r, a_r)
on (55 < 60)
) T1
union all
select e, a
from (
Select e, a
from t3
where (d = b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, a, b
from t3
where (62 = d)
) T1
union all
select d
from (
Select d
from t4
where (22 < (b + e))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t4
where (95 = b)
) T1
union all
select c
from (
Select c, a
from t5
where (c = ((64 * 56) * (42 - 26)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t2
where (b > d)
) T1
union all
select a, b
from (
Select a, b, d
from t4
where (46 < (c + (90 - b)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
select a, d
from (
Select a, d
from t1
where (0 > d)
) T1
union all
select c_l, d_l_l_r
from (
Select c_l, d_l_l_r
from (
Select c, d
from t5
where ((((47 + 39) + 67) - 33) = 82)
) T1(c_l, d_l)
left join (
Select a_r_r_l, d_l_l, e_r
from (
Select a_l, d_l, a_r_r, a_r_l_r
from (
Select c, a, b, d
from t4
where (e = e)
) T1(c_l, a_l, b_l, d_l)
left join (
select a_r_l, a_r
from (
select a_r_l, a_r
from (
Select a_r_l, a_r
from (
Select c_l, a_r, b_r
from (
Select c
from t1
where (e > c)
) T1(c_l)
inner join (
Select a, b, d
from t2
where ((((d * 53) * c) * a) < d)
) T2(a_r, b_r, d_r)
on (b_r < c_l)
) T1(c_l_l, a_r_l, b_r_l)
full join (
Select c, a
from t4
where (e < d)
) T2(c_r, a_r)
on ((28 + 57) = 47)
) T1
union all
select c, b
from (
Select c, b
from t2
where ((e - 67) > d)
) T2
) T1
union all
select c, b
from (
Select c, b
from t3
where (5 > a)
) T2
) T2(a_r_l_r, a_r_r)
on ((d_l + 26) = a_r_l_r)
) T1(a_l_l, d_l_l, a_r_r_l, a_r_l_r_l)
left join (
Select e
from t1
where (d > d)
) T2(e_r)
on (e_r > 86)
) T2(a_r_r_l_r, d_l_l_r, e_r_r)
on (d_l_l_r > c_l)
) T2
) T1
union all
select c
from (
Select c
from t5
where (18 < d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s714')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l
from (
Select e_l, a_l, e_r
from (
Select e, a, d
from t1
where ((64 * a) = 20)
) T1(e_l, a_l, d_l)
left join (
Select e, b
from t5
where (71 < d)
) T2(e_r, b_r)
on (23 = (72 - a_l))
) T1
union all
select e, c
from (
select e, c
from (
Select e, c
from t1
where (((15 * a) + c) = c)
) T1
union all
select c_r_l, e_r
from (
Select c_r_l, e_r, c_r, d_r
from (
Select e_l, c_r
from (
Select e, c
from t2
where (e = c)
) T1(e_l, c_l)
left join (
Select e, c
from t5
where (e = 90)
) T2(e_r, c_r)
on ((65 - 77) < c_r)
) T1(e_l_l, c_r_l)
left join (
Select e, c, b, d
from t5
where (a = c)
) T2(e_r, c_r, b_r, d_r)
on (c_r_l = (c_r_l + c_r))
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (a > 28)
) T1
union all
select e
from (
Select e, c, a, d
from t1
where (d > c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t4
where (e < 45)
) T1
union all
select b_l, b_r
from (
Select b_l, b_r, d_r
from (
select e, b, d
from (
Select e, b, d
from t2
where (c = a)
) T1
union all
select e, c, d
from (
Select e, c, d
from t4
where (85 < 37)
) T2
) T1(e_l, b_l, d_l)
inner join (
Select b, d
from t1
where (e = c)
) T2(b_r, d_r)
on (51 = 75)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t5
where (45 = ((((63 - c) * a) * ((((e * 96) * 6) + d) + 98)) - (88 * 60)))
) T1
union all
select b_r_l, c_l_l_l
from (
Select b_r_l, c_l_l_l, e_r, c_r
from (
Select c_l_l, b_r
from (
Select c_l, a_l, b_l, e_r, a_r
from (
Select e, c, a, b
from t3
where (61 < d)
) T1(e_l, c_l, a_l, b_l)
left join (
Select e, a, d
from t5
where (a > b)
) T2(e_r, a_r, d_r)
on (a_r = c_l)
) T1(c_l_l, a_l_l, b_l_l, e_r_l, a_r_l)
full join (
Select b
from t2
where (18 = 51)
) T2(b_r)
on (c_l_l = c_l_l)
) T1(c_l_l_l, b_r_l)
full join (
Select e, c, d
from t5
where (d = a)
) T2(e_r, c_r, d_r)
on (e_r = b_r_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, a_r
from (
Select e_l_l, a_r
from (
Select e_l, b_l, c_r, d_r
from (
Select e, b
from t5
where (50 > b)
) T1(e_l, b_l)
inner join (
select c, b, d
from (
Select c, b, d
from t1
where (d = d)
) T1
union all
select b_l, e_r, c_r
from (
Select b_l, e_r, c_r, a_r
from (
Select e, b, d
from t2
where (a = e)
) T1(e_l, b_l, d_l)
full join (
Select e, c, a
from t3
where ((67 + (43 - a)) = (b + 66))
) T2(e_r, c_r, a_r)
on (a_r < a_r)
) T2
) T2(c_r, b_r, d_r)
on (22 > b_l)
) T1(e_l_l, b_l_l, c_r_l, d_r_l)
full join (
Select a
from t5
where (86 = e)
) T2(a_r)
on (e_l_l < a_r)
) T1
union all
select a_l, b_l
from (
select a_l, b_l, d_l, c_r
from (
Select a_l, b_l, d_l, c_r, a_r
from (
Select a, b, d
from t3
where (e = 19)
) T1(a_l, b_l, d_l)
full join (
Select e, c, a
from t2
where (68 > a)
) T2(e_r, c_r, a_r)
on (28 < a_l)
) T1
union all
select c_l, b_l, c_r, b_r
from (
Select c_l, b_l, c_r, b_r
from (
Select e, c, b
from t1
where (82 = 31)
) T1(e_l, c_l, b_l)
left join (
Select c, a, b
from t2
where (77 = 75)
) T2(c_r, a_r, b_r)
on (67 < (69 - c_r))
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test01exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b
from t3
where (e > e)
) T1
union all
select e, b, d
from (
Select e, b, d
from t2
where (e = 73)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

