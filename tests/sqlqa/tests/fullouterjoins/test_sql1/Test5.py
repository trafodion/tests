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

#****************************************
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='Joins Set 5'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, b
from t2
where (19 < 16)
) T1
union all
select b
from (
select b
from (
Select b
from t4
where (a < d)
) T1
union all
select e
from (
Select e, c
from t4
where (30 = 98)
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
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s1')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, a_l, d_l, d_r
from (
Select e, a, d
from t4
where (b < a)
) T1(e_l, a_l, d_l)
inner join (
Select a, d
from t1
where (c > 3)
) T2(a_r, d_r)
on (36 > 5)
) T1
union all
select c
from (
Select c
from t3
where (8 = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t5
where (56 = c)
) T1
union all
select e
from (
Select e, a, d
from t2
where (28 = 68)
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
select e, c
from (
Select e, c, a
from t3
where (8 = 21)
) T1
union all
select b_l_l, c_l_r
from (
Select b_l_l, c_l_r
from (
select b_l
from (
Select b_l, c_r, a_r, b_r
from (
Select b
from t2
where ((d * b) > 88)
) T1(b_l)
left join (
Select c, a, b
from t5
where ((d * c) = (d * 97))
) T2(c_r, a_r, b_r)
on (((50 + b_l) * 2) = 25)
) T1
union all
select c
from (
Select c
from t1
where (c > a)
) T2
) T1(b_l_l)
full join (
select c_l, d_r
from (
Select c_l, d_r
from (
Select c, a, b
from t4
where (37 = 79)
) T1(c_l, a_l, b_l)
left join (
Select d
from t1
where (50 = 2)
) T2(d_r)
on ((c_l + (d_r - d_r)) > 2)
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, e_r
from (
Select e, c, b
from t3
where (c > 26)
) T1(e_l, c_l, b_l)
left join (
Select e, a, b
from t5
where ((2 + 11) = b)
) T2(e_r, a_r, b_r)
on (e_r = 22)
) T2
) T2(c_l_r, d_r_r)
on (b_l_l > 77)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t4
where (a < 52)
) T1
union all
select c_l, d_l_r_r
from (
Select c_l, d_l_r_r
from (
Select e, c, a
from t1
where (e = 67)
) T1(e_l, c_l, a_l)
full join (
Select c_l_l, d_l_r
from (
Select c_l, a_l, e_r, c_r, a_r
from (
Select c, a
from t1
where ((87 * 43) < b)
) T1(c_l, a_l)
left join (
Select e, c, a
from t1
where (13 < e)
) T2(e_r, c_r, a_r)
on (20 = (90 * a_r))
) T1(c_l_l, a_l_l, e_r_l, c_r_l, a_r_l)
full join (
select d_l, a_r
from (
Select d_l, a_r, d_r
from (
Select d
from t1
where (80 = 73)
) T1(d_l)
inner join (
Select c, a, d
from t5
where (e = 96)
) T2(c_r, a_r, d_r)
on (a_r < d_r)
) T1
union all
select b_r_l, e_r_l
from (
select b_r_l, e_r_l
from (
Select b_r_l, e_r_l, e_r
from (
Select e_l_l, b_l_l, e_r, b_r
from (
Select e_l, b_l, b_r
from (
Select e, b
from t5
where (d = e)
) T1(e_l, b_l)
full join (
select b
from (
Select b
from t1
where (b = c)
) T1
union all
select b_l_l
from (
Select b_l_l, d_l_l, e_r
from (
Select b_l, d_l, d_r_r
from (
Select b, d
from t1
where (55 = 80)
) T1(b_l, d_l)
left join (
Select d_l, d_r
from (
Select b, d
from t2
where ((e + 34) = 85)
) T1(b_l, d_l)
left join (
Select d
from t5
where (c = b)
) T2(d_r)
on (26 = d_l)
) T2(d_l_r, d_r_r)
on (b_l = 15)
) T1(b_l_l, d_l_l, d_r_r_l)
left join (
Select e
from t4
where (a < a)
) T2(e_r)
on (b_l_l = 79)
) T2
) T2(b_r)
on (42 < (95 - e_l))
) T1(e_l_l, b_l_l, b_r_l)
left join (
Select e, b
from t5
where (((73 + d) * d) = 48)
) T2(e_r, b_r)
on (e_r = ((25 * e_r) + (e_l_l - 2)))
) T1(e_l_l_l, b_l_l_l, e_r_l, b_r_l)
left join (
Select e
from t3
where (((33 * 24) - 55) = e)
) T2(e_r)
on (e_r < (e_r_l + 85))
) T1
union all
select c, d
from (
Select c, d
from t2
where (35 > e)
) T2
) T2
) T2(d_l_r, a_r_r)
on (d_l_r = 9)
) T2(c_l_l_r, d_l_r_r)
on (24 < ((55 + 11) - (d_l_r_r * c_l)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a, b
from t5
where (59 < (a - 61))
) T1
union all
select c, a
from (
Select c, a
from t5
where (a = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t1
where (((90 - d) + 9) = e)
) T1
union all
select b
from (
Select b
from t3
where (91 = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t2
where (a < 93)
) T1
union all
select b_l
from (
select b_l, e_r
from (
Select b_l, e_r, c_r
from (
Select b
from t1
where (e = d)
) T1(b_l)
inner join (
Select e, c, b
from t5
where ((c - a) < c)
) T2(e_r, c_r, b_r)
on (28 < (e_r - 5))
) T1
union all
select e, d
from (
Select e, d
from t1
where ((e - 46) = 40)
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
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s8')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t1
where (4 = c)
) T1
union all
select a_l, b_l
from (
Select a_l, b_l, d_l, c_r
from (
Select a, b, d
from t4
where (0 < d)
) T1(a_l, b_l, d_l)
inner join (
Select c, d
from t5
where (c > 71)
) T2(c_r, d_r)
on ((((b_l - 95) - 70) * a_l) < a_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t2
where ((44 + (c - d)) > 35)
) T1
union all
select d
from (
select d
from (
Select d
from t4
where (d = 31)
) T1
union all
select a
from (
Select a, b
from t1
where (b = (((a - 74) * 41) * b))
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
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_r
from (
Select a_l, b_r
from (
Select c, a, b, d
from t3
where (5 = e)
) T1(c_l, a_l, b_l, d_l)
inner join (
Select b
from t3
where (a < b)
) T2(b_r)
on (b_r < a_l)
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, d_l, a_r
from (
Select e, a, b, d
from t5
where (56 > 14)
) T1(e_l, a_l, b_l, d_l)
full join (
Select a
from t5
where (d > d)
) T2(a_r)
on (a_r = e_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_r_r
from (
Select a_l, b_r_r, e_l_r
from (
Select a
from t2
where (e = 46)
) T1(a_l)
inner join (
Select e_l, b_r
from (
select e
from (
Select e, b
from t4
where (43 = 62)
) T1
union all
select a
from (
select a
from (
select a
from (
Select a
from t1
where (d > (d + d))
) T1
union all
select e_l_l
from (
Select e_l_l, c_l_r_r_l, c_r, a_r, b_r
from (
Select e_l, c_l_r_r
from (
select e
from (
Select e
from t4
where (b > (a * e))
) T1
union all
select c
from (
select c
from (
Select c
from t5
where (d = (e - a))
) T1
union all
select d
from (
Select d
from t5
where (48 = (b * (((36 - d) - (96 + a)) * b)))
) T2
) T2
) T1(e_l)
left join (
Select c_l, a_l_r, c_l_r
from (
Select c, d
from t1
where ((c - (e * 2)) < b)
) T1(c_l, d_l)
full join (
Select c_l, a_l, d_r
from (
Select c, a
from t5
where (e = 11)
) T1(c_l, a_l)
full join (
Select c, d
from t3
where (93 = 16)
) T2(c_r, d_r)
on (c_l = d_r)
) T2(c_l_r, a_l_r, d_r_r)
on (((93 + 14) + (5 - (c_l - c_l))) > a_l_r)
) T2(c_l_r, a_l_r_r, c_l_r_r)
on (c_l_r_r < e_l)
) T1(e_l_l, c_l_r_r_l)
left join (
Select c, a, b
from t3
where (((50 * d) - (9 * 76)) > e)
) T2(c_r, a_r, b_r)
on (21 = 37)
) T2
) T1
union all
select e
from (
Select e
from t4
where (((b + 70) * a) > 93)
) T2
) T2
) T1(e_l)
inner join (
Select a, b
from t3
where ((87 * 5) > (82 + 8))
) T2(a_r, b_r)
on (b_r = 72)
) T2(e_l_r, b_r_r)
on (a_l = e_l_r)
) T1
union all
select a, d
from (
Select a, d
from t5
where (e > d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t4
where (76 = (10 + (23 - e)))
) T1
union all
select d_l, a_r
from (
Select d_l, a_r
from (
Select d
from t3
where (91 < (d + 1))
) T1(d_l)
left join (
Select a, d
from t4
where ((b - (49 - (97 * 15))) = 0)
) T2(a_r, d_r)
on (((((86 * d_l) + ((99 * (a_r * a_r)) + (42 - a_r))) - (2 - d_l)) + 36) = (94 + 20))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, d
from (
Select a, d
from t2
where (d = (a * (c * (d + c))))
) T1
union all
select e, c
from (
Select e, c
from t3
where (d = (a + 13))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t3
where (a = 7)
) T1
union all
select a_l_l, d_r_l_l_r
from (
Select a_l_l, d_r_l_l_r, d_r_r
from (
Select e_l, a_l, a_l_r
from (
Select e, a, d
from t4
where (e < (e * 36))
) T1(e_l, a_l, d_l)
left join (
select a_l
from (
select a_l
from (
Select a_l, c_r
from (
Select a
from t5
where (a > 33)
) T1(a_l)
left join (
Select e, c, a
from t4
where (a > c)
) T2(e_r, c_r, a_r)
on (c_r = (17 + 13))
) T1
union all
select a
from (
Select a
from t2
where (d = 19)
) T2
) T1
union all
select c
from (
Select c, b, d
from t1
where (e > 45)
) T2
) T2(a_l_r)
on (82 = a_l_r)
) T1(e_l_l, a_l_l, a_l_r_l)
left join (
Select d_r_l_l, e_r, d_r
from (
Select a_l_l, d_r_l, b_l_r
from (
Select a_l, d_r
from (
Select a
from t5
where (87 > 94)
) T1(a_l)
left join (
Select a, b, d
from t3
where (c = 7)
) T2(a_r, b_r, d_r)
on (47 > 59)
) T1(a_l_l, d_r_l)
full join (
Select b_l, a_l_r_r
from (
Select a, b
from t1
where (b = 99)
) T1(a_l, b_l)
left join (
select a_l, a_l_r
from (
Select a_l, a_l_r
from (
Select a
from t2
where (d > 70)
) T1(a_l)
inner join (
Select a_l, b_l_r_r_r, e_l_l_r
from (
Select e, a, b, d
from t1
where (((49 + (97 * b)) - e) = 45)
) T1(e_l, a_l, b_l, d_l)
full join (
Select e_l_l, b_l_r_r
from (
Select e_l, a_r, b_r
from (
Select e
from t4
where (3 < (a - a))
) T1(e_l)
inner join (
Select c, a, b
from t2
where (a = e)
) T2(c_r, a_r, b_r)
on (70 < e_l)
) T1(e_l_l, a_r_l, b_r_l)
inner join (
Select a_l, e_r_r, b_l_r
from (
Select a
from t1
where (b < d)
) T1(a_l)
left join (
Select b_l, e_r
from (
Select e, b
from t5
where (47 < (c + c))
) T1(e_l, b_l)
full join (
Select e, c, d
from t2
where (d = 14)
) T2(e_r, c_r, d_r)
on (e_r = e_r)
) T2(b_l_r, e_r_r)
on (e_r_r > 95)
) T2(a_l_r, e_r_r_r, b_l_r_r)
on (99 > e_l_l)
) T2(e_l_l_r, b_l_r_r_r)
on (a_l < 27)
) T2(a_l_r, b_l_r_r_r_r, e_l_l_r_r)
on (a_l < a_l_r)
) T1
union all
select e, b
from (
Select e, b, d
from t4
where (17 < 4)
) T2
) T2(a_l_r, a_l_r_r)
on (37 < (87 + 66))
) T2(b_l_r, a_l_r_r_r)
on (b_l_r > 67)
) T1(a_l_l_l, d_r_l_l, b_l_r_l)
left join (
Select e, a, d
from t1
where (19 > b)
) T2(e_r, a_r, d_r)
on (17 = d_r)
) T2(d_r_l_l_r, e_r_r, d_r_r)
on (77 = a_l_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b
from t2
where ((c + c) = 61)
) T1
union all
select d
from (
Select d
from t4
where (22 = (d * ((90 - e) + c)))
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
select d
from (
select d
from (
Select d
from t1
where ((64 - 1) = 58)
) T1
union all
select e
from (
Select e
from t4
where (b < 77)
) T2
) T1
union all
select c
from (
Select c, a
from t2
where (c > 58)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t3
where (72 = c)
) T1
union all
select c_l, e_r
from (
Select c_l, e_r, c_r, b_r
from (
Select c, a
from t3
where (e = 44)
) T1(c_l, a_l)
left join (
select e, c, b
from (
Select e, c, b
from t4
where (35 = ((74 - d) + 58))
) T1
union all
select e, a, b
from (
Select e, a, b
from t4
where (c < b)
) T2
) T2(e_r, c_r, b_r)
on (29 = b_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, b, d
from t3
where (b = e)
) T1
union all
select c, a
from (
Select c, a
from t2
where (a = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_r_l, d_r
from (
Select a_l_r_l, d_r
from (
Select b_l, a_l_r
from (
Select b
from t3
where (a < b)
) T1(b_l)
left join (
Select a_l, d_l, e_r
from (
Select a, d
from t1
where ((8 + 20) < 14)
) T1(a_l, d_l)
left join (
Select e, d
from t4
where (2 = (a * (e * 88)))
) T2(e_r, d_r)
on (41 = 46)
) T2(a_l_r, d_l_r, e_r_r)
on (b_l = (57 - b_l))
) T1(b_l_l, a_l_r_l)
inner join (
Select b, d
from t2
where (a > (b * d))
) T2(b_r, d_r)
on (73 < ((d_r - 31) - 77))
) T1
union all
select a_l, e_r
from (
Select a_l, e_r, a_r
from (
select a
from (
Select a
from t3
where (98 = 36)
) T1
union all
select c
from (
Select c, a
from t4
where (c > 60)
) T2
) T1(a_l)
left join (
Select e, a
from t4
where ((c * (((32 - 86) * 67) - 41)) > c)
) T2(e_r, a_r)
on (a_l < a_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test05exp""", 'a1s20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #************************************
    
    _testmgr.testcase_end(desc)

