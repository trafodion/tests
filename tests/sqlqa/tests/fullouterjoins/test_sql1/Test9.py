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

#************************************************
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='Joins Set 9'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #************************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select c, b, d
from (
Select c, b, d
from t1
where (6 = 15)
) T1
union all
select e, a, d
from (
Select e, a, d
from t3
where (a < c)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s1')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t5
where (a = a)
) T1
union all
select e, c
from (
Select e, c
from t5
where (d < 49)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t1
where ((((37 * d) + e) + a) > (22 * 72))
) T1
union all
select b, d
from (
Select b, d
from t5
where (c = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_l
from (
Select a_l, b_l, e_r_r
from (
Select a, b
from t5
where (a > 25)
) T1(a_l, b_l)
inner join (
Select e_l, d_l, e_r
from (
Select e, d
from t4
where (b = 22)
) T1(e_l, d_l)
inner join (
Select e, c, b
from t3
where (4 = a)
) T2(e_r, c_r, b_r)
on (e_r > e_r)
) T2(e_l_r, d_l_r, e_r_r)
on (e_r_r = b_l)
) T1
union all
select e, b
from (
Select e, b
from t1
where ((54 - (12 + 56)) > 71)
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
select c, a
from (
Select c, a
from t3
where (22 = 5)
) T1
union all
select e, a
from (
Select e, a, b
from t4
where (9 = ((96 + (67 * (b * c))) + d))
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
select e, c
from (
Select e, c, a, b
from t3
where ((b - 93) > a)
) T1
union all
select a, d
from (
Select a, d
from t2
where (c = 4)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, d
from (
Select e, a, d
from t1
where (38 = (a + 1))
) T1
union all
select c_l, a_l, c_r
from (
Select c_l, a_l, c_r, b_r
from (
Select e, c, a, b
from t5
where (19 = 41)
) T1(e_l, c_l, a_l, b_l)
left join (
Select c, b
from t4
where (60 < 94)
) T2(c_r, b_r)
on ((((6 * (b_r * 68)) + 58) + 16) < 49)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l
from (
select c_l
from (
Select c_l, d_l, e_r
from (
Select e, c, d
from t2
where (d = 12)
) T1(e_l, c_l, d_l)
inner join (
Select e, b
from t1
where (a = (99 - 96))
) T2(e_r, b_r)
on ((c_l + 7) = (0 * (d_l + c_l)))
) T1
union all
select d
from (
Select d
from t3
where (2 = ((b + a) - e))
) T2
) T1
union all
select d_l
from (
Select d_l, a_r_r_r
from (
Select e, c, d
from t4
where (d = 46)
) T1(e_l, c_l, d_l)
left join (
Select b_r_l, e_l_l, e_l_r, a_r_r
from (
Select e_l, b_r
from (
Select e, b
from t2
where (c = c)
) T1(e_l, b_l)
left join (
Select b
from t5
where ((b * (e - (e * c))) = b)
) T2(b_r)
on (22 < ((8 * b_r) + e_l))
) T1(e_l_l, b_r_l)
full join (
select e_l, d_l, a_r
from (
Select e_l, d_l, a_r
from (
Select e, b, d
from t5
where (d = ((a - 53) + c))
) T1(e_l, b_l, d_l)
left join (
Select a
from t2
where (91 < 44)
) T2(a_r)
on ((77 + a_r) < d_l)
) T1
union all
select c, a, d
from (
Select c, a, d
from t4
where (61 > 24)
) T2
) T2(e_l_r, d_l_r, a_r_r)
on ((e_l_l + 11) = e_l_r)
) T2(b_r_l_r, e_l_l_r, e_l_r_r, a_r_r_r)
on ((21 + (a_r_r_r * (a_r_r_r + (a_r_r_r * d_l)))) = a_r_r_r)
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
select e
from (
Select e
from t4
where ((c * e) = b)
) T1
union all
select d
from (
Select d
from t4
where (81 = 70)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, a, d
from t2
where (e = 22)
) T1
union all
select e, a
from (
Select e, a
from t3
where (56 = ((12 * 8) - e))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t3
where (d = d)
) T1
union all
select e, b
from (
Select e, b
from t3
where (7 = (63 + b))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t2
where (91 = d)
) T1
union all
select c
from (
Select c
from t1
where (d < 60)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t4
where (5 < 97)
) T1
union all
select c_l, b_l_r_l_l_r
from (
Select c_l, b_l_r_l_l_r, a_r_l_r
from (
Select c
from t2
where (93 = 80)
) T1(c_l)
full join (
select b_l_r_l_l, a_r_l
from (
select b_l_r_l_l, a_r_l
from (
Select b_l_r_l_l, a_r_l, b_r_r, d_l_r
from (
Select b_l_r_l, c_l_l, a_r
from (
Select c_l, b_l_r
from (
Select e, c, a, d
from t1
where (c < c)
) T1(e_l, c_l, a_l, d_l)
left join (
Select b_l, a_r, b_r
from (
Select b
from t1
where (a > 68)
) T1(b_l)
left join (
Select e, a, b, d
from t1
where (8 = (d * 60))
) T2(e_r, a_r, b_r, d_r)
on ((22 * b_l) = (86 - 76))
) T2(b_l_r, a_r_r, b_r_r)
on (c_l = 98)
) T1(c_l_l, b_l_r_l)
inner join (
Select e, a
from t5
where (94 = b)
) T2(e_r, a_r)
on (72 < a_r)
) T1(b_l_r_l_l, c_l_l_l, a_r_l)
left join (
Select d_l, b_r, d_r
from (
Select d
from t1
where (61 = 4)
) T1(d_l)
inner join (
Select c, a, b, d
from t3
where (43 < e)
) T2(c_r, a_r, b_r, d_r)
on (b_r = 12)
) T2(d_l_r, b_r_r, d_r_r)
on (68 = 35)
) T1
union all
select c, b
from (
Select c, b
from t1
where (47 > 8)
) T2
) T1
union all
select b, d
from (
Select b, d
from t3
where (28 = c)
) T2
) T2(b_l_r_l_l_r, a_r_l_r)
on (50 = 64)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t3
where (e > (81 + a))
) T1
union all
select e, c
from (
Select e, c, d
from t3
where (58 < 10)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, d
from (
Select a, d
from t2
where (32 > 2)
) T1
union all
select b_l, d_r_r
from (
Select b_l, d_r_r, e_l_r
from (
Select b
from t3
where (50 = e)
) T1(b_l)
left join (
Select e_l, e_r, d_r
from (
Select e
from t3
where (53 < c)
) T1(e_l)
left join (
Select e, a, d
from t3
where (92 = 7)
) T2(e_r, a_r, d_r)
on (d_r < e_l)
) T2(e_l_r, e_r_r, d_r_r)
on (28 > (b_l - (25 + 89)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l
from (
Select b_l, c_r, a_r, b_r
from (
Select c, b
from t3
where ((a + 78) < b)
) T1(c_l, b_l)
full join (
select c, a, b
from (
Select c, a, b
from t5
where (94 > 59)
) T1
union all
select c, a, b
from (
Select c, a, b
from t1
where (52 > (37 - 33))
) T2
) T2(c_r, a_r, b_r)
on (69 = (72 * (b_r + b_r)))
) T1
union all
select b
from (
Select b
from t3
where (b = (a * 77))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t4
where (b = 10)
) T1
union all
select c_l
from (
Select c_l, e_r, a_r
from (
Select c, a, b
from t1
where (82 > 47)
) T1(c_l, a_l, b_l)
full join (
select e, a
from (
Select e, a
from t2
where (96 < e)
) T1
union all
select e, a
from (
Select e, a
from t1
where ((23 + 72) > (75 - b))
) T2
) T2(e_r, a_r)
on (96 = 78)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t2
where (87 < 0)
) T1
union all
select b
from (
Select b
from t4
where (28 < 1)
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
select c_l
from (
select c_l
from (
Select c_l, a_l, e_r, d_r
from (
select c, a
from (
Select c, a, b
from t3
where (5 < (37 + d))
) T1
union all
select e, d
from (
Select e, d
from t5
where (e < e)
) T2
) T1(c_l, a_l)
left join (
Select e, b, d
from t2
where (e = (84 - (65 - a)))
) T2(e_r, b_r, d_r)
on (73 < 39)
) T1
union all
select a
from (
select a
from (
Select a, b
from t2
where (b < 28)
) T1
union all
select b
from (
Select b
from t5
where (d < 68)
) T2
) T2
) T1
union all
select c
from (
Select c, b
from t1
where (a < c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a
from (
Select e, c, a, b
from t5
where (d = a)
) T1
union all
select e, a, b
from (
Select e, a, b
from t2
where (d < b)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test09exp""", 'a1s20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

