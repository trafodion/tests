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
    
def test001(desc='Joins Set 6'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t5
where (d < ((e + 13) - ((b + c) * 31)))
) T1
union all
select e, a
from (
Select e, a
from t4
where (9 < (b * 57))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s1')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t4
where (b = (e + e))
) T1
union all
select d_r_l
from (
Select d_r_l, b_l_l, e_r, a_r, b_r
from (
select a_l, b_l, d_r
from (
Select a_l, b_l, d_r
from (
Select a, b
from t4
where (e < 25)
) T1(a_l, b_l)
full join (
Select d
from t4
where ((a + d) > 30)
) T2(d_r)
on (87 = 46)
) T1
union all
select a_l_l, e_r_l, d_r
from (
Select a_l_l, e_r_l, d_r
from (
Select a_l, e_r
from (
Select c, a, d
from t3
where (5 = ((50 * 50) + 51))
) T1(c_l, a_l, d_l)
left join (
Select e, b, d
from t5
where (b = 3)
) T2(e_r, b_r, d_r)
on (a_l < (8 + e_r))
) T1(a_l_l, e_r_l)
left join (
Select e, b, d
from t1
where (34 = b)
) T2(e_r, b_r, d_r)
on (7 < 17)
) T2
) T1(a_l_l, b_l_l, d_r_l)
left join (
Select e, a, b, d
from t4
where (83 < 72)
) T2(e_r, a_r, b_r, d_r)
on (b_l_l = 48)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t5
where (b < d)
) T1
union all
select e_l
from (
Select e_l, a_l, e_r, c_r
from (
Select e, a
from t4
where (e = 78)
) T1(e_l, a_l)
left join (
Select e, c
from t5
where (47 = (e * 60))
) T2(e_r, c_r)
on ((57 * e_l) = a_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t3
where ((c * d) > 20)
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
select b
from (
Select b
from t2
where (14 < d)
) T1
union all
select a_l
from (
Select a_l, b_r
from (
Select a
from t1
where (53 > 93)
) T1(a_l)
inner join (
Select b
from t5
where (d = d)
) T2(b_r)
on (90 < b_r)
) T2
) T1(b_l)
inner join (
Select a
from t3
where (c = b)
) T2(a_r)
on (a_r = ((((95 * b_l) - 26) * a_r) * (((b_l * 53) + a_r) * 96)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l
from (
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r, c_r
from (
Select e, c, a, b
from t3
where (e = d)
) T1(e_l, c_l, a_l, b_l)
left join (
Select e, c, b
from t5
where (35 = d)
) T2(e_r, c_r, b_r)
on (a_l = 99)
) T1
union all
select c, a, b
from (
Select c, a, b
from t4
where (10 < c)
) T2
) T1
union all
select d
from (
select d
from (
Select d
from t5
where (32 = 5)
) T1
union all
select a_l_l
from (
Select a_l_l, b_l_r_r, c_l_r, b_l_r
from (
Select a_l, b_r_r
from (
Select a
from t1
where ((e * ((5 * 75) * c)) = 43)
) T1(a_l)
full join (
Select d_l, b_r
from (
Select c, d
from t3
where (d > c)
) T1(c_l, d_l)
left join (
Select b
from t5
where (53 < c)
) T2(b_r)
on (7 < 54)
) T2(d_l_r, b_r_r)
on (64 > a_l)
) T1(a_l_l, b_r_r_l)
left join (
Select c_l, b_l, b_l_r
from (
Select c, b
from t1
where (c < c)
) T1(c_l, b_l)
full join (
Select a_l, b_l, e_r, b_r, d_r
from (
Select e, a, b
from t3
where (13 = 71)
) T1(e_l, a_l, b_l)
full join (
Select e, b, d
from t1
where (((((b + 36) + 95) * (42 * c)) - c) < a)
) T2(e_r, b_r, d_r)
on (52 = 9)
) T2(a_l_r, b_l_r, e_r_r, b_r_r, d_r_r)
on ((73 - b_l_r) > c_l)
) T2(c_l_r, b_l_r, b_l_r_r)
on (93 = a_l_l)
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
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, b_l, c_r_r
from (
Select c_l, b_l, c_r_r
from (
Select c, a, b
from t1
where (e > a)
) T1(c_l, a_l, b_l)
left join (
Select e_l, c_r
from (
Select e
from t4
where (e = c)
) T1(e_l)
full join (
Select c
from t4
where (c = (e - (e + 40)))
) T2(c_r)
on (e_l = 1)
) T2(e_l_r, c_r_r)
on (78 > ((c_l * 76) + b_l))
) T1
union all
select e, c, a
from (
Select e, c, a, d
from t4
where (e = 84)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s6')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b, d
from t5
where (a = 84)
) T1
union all
select d_l, b_r_r
from (
Select d_l, b_r_r
from (
Select c, b, d
from t2
where (76 < (59 + 20))
) T1(c_l, b_l, d_l)
full join (
Select c_l, d_l, c_r, b_r
from (
Select c, d
from t2
where (e < (60 * (66 - a)))
) T1(c_l, d_l)
left join (
Select c, b
from t4
where (d < 34)
) T2(c_r, b_r)
on (14 = 97)
) T2(c_l_r, d_l_r, c_r_r, b_r_r)
on (b_r_r < 70)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l
from (
Select b_l, b_l_r
from (
Select e, b
from t2
where (c > 34)
) T1(e_l, b_l)
left join (
Select b_l, d_r_l_l_r, e_l_r_r
from (
select b
from (
Select b
from t1
where (62 < a)
) T1
union all
select a_l
from (
Select a_l, c_r, b_r
from (
Select a, b, d
from t1
where (b > ((35 - 2) + d))
) T1(a_l, b_l, d_l)
left join (
Select c, b
from t1
where ((33 * 74) > c)
) T2(c_r, b_r)
on (5 < 92)
) T2
) T1(b_l)
left join (
Select d_r_l_l, e_l_r
from (
Select d_r_l, c_r_l_l, a_l_r, d_l_r
from (
Select a_l_l, e_l_l, a_r_l, c_r_l, d_r
from (
Select e_l, c_l, a_l, c_r, a_r
from (
Select e, c, a
from t4
where (95 = (e * b))
) T1(e_l, c_l, a_l)
left join (
Select c, a, d
from t4
where (c = b)
) T2(c_r, a_r, d_r)
on (a_r > 59)
) T1(e_l_l, c_l_l, a_l_l, c_r_l, a_r_l)
inner join (
select c, d
from (
Select c, d
from t4
where (58 > (c + 12))
) T1
union all
select c, a
from (
Select c, a, b
from t2
where ((89 - a) = b)
) T2
) T2(c_r, d_r)
on (e_l_l = 46)
) T1(a_l_l_l, e_l_l_l, a_r_l_l, c_r_l_l, d_r_l)
left join (
Select a_l, d_l, a_r
from (
Select e, a, d
from t4
where ((b + 2) < 69)
) T1(e_l, a_l, d_l)
inner join (
Select c, a, d
from t4
where ((10 * e) = d)
) T2(c_r, a_r, d_r)
on (d_l = (22 + 50))
) T2(a_l_r, d_l_r, a_r_r)
on (59 > d_l_r)
) T1(d_r_l_l, c_r_l_l_l, a_l_r_l, d_l_r_l)
left join (
Select e_l, a_l, c_l_r_r
from (
Select e, a, b
from t3
where (30 < 34)
) T1(e_l, a_l, b_l)
inner join (
Select d_l, c_l_r
from (
Select d
from t1
where (9 < (89 - (a - d)))
) T1(d_l)
full join (
Select c_l, e_r
from (
Select c
from t5
where (b > 30)
) T1(c_l)
inner join (
Select e
from t2
where ((a * 68) = 4)
) T2(e_r)
on (17 > (45 + 98))
) T2(c_l_r, e_r_r)
on (c_l_r > c_l_r)
) T2(d_l_r, c_l_r_r)
on (41 < 12)
) T2(e_l_r, a_l_r, c_l_r_r_r)
on (89 = 94)
) T2(d_r_l_l_r, e_l_r_r)
on (59 = 69)
) T2(b_l_r, d_r_l_l_r_r, e_l_r_r_r)
on (b_l_r < b_l_r)
) T1
union all
select e
from (
Select e
from t2
where (d = c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s8')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t4
where ((((40 + 71) + (d - c)) + 93) = b)
) T1
union all
select c, d
from (
Select c, d
from t1
where (e > 57)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s9')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t1
where (((38 - 65) + d) = 0)
) T1
union all
select e_l, b_l
from (
Select e_l, b_l, e_l_r, a_r_r
from (
select e, b
from (
Select e, b
from t2
where ((97 - e) = 97)
) T1
union all
select d_l, d_r
from (
Select d_l, d_r
from (
Select e, a, b, d
from t4
where (b < (79 - d))
) T1(e_l, a_l, b_l, d_l)
inner join (
Select d
from t4
where (60 = (e - 26))
) T2(d_r)
on (d_r < d_r)
) T2
) T1(e_l, b_l)
left join (
select e_l, a_l, a_r, b_r
from (
Select e_l, a_l, a_r, b_r
from (
Select e, c, a
from t3
where (69 = ((4 - (99 - e)) * c))
) T1(e_l, c_l, a_l)
left join (
Select e, a, b
from t2
where (74 = 54)
) T2(e_r, a_r, b_r)
on ((e_l + a_r) < 39)
) T1
union all
select e, c, b, d
from (
Select e, c, b, d
from t2
where ((26 * 60) < c)
) T2
) T2(e_l_r, a_l_r, a_r_r, b_r_r)
on (66 > (92 - 13))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s10')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, d_r_l, a_r
from (
Select e_l_l, d_r_l, a_r
from (
Select e_l, d_l, d_r
from (
Select e, b, d
from t3
where (c = 92)
) T1(e_l, b_l, d_l)
left join (
Select e, d
from t1
where (17 = c)
) T2(e_r, d_r)
on (97 = e_l)
) T1(e_l_l, d_l_l, d_r_l)
inner join (
Select a
from t2
where (d = e)
) T2(a_r)
on (76 = 19)
) T1
union all
select e_l, d_l, e_r
from (
Select e_l, d_l, e_r, c_r, b_r
from (
Select e, d
from t5
where (e < 67)
) T1(e_l, d_l)
left join (
Select e, c, b
from t4
where (83 = 34)
) T2(e_r, c_r, b_r)
on (53 > c_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t4
where (40 < c)
) T1
union all
select e, c
from (
Select e, c, a
from t3
where (((43 + (d + 11)) * 62) > b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_r
from (
Select a_l, b_r
from (
Select a
from t4
where (27 > d)
) T1(a_l)
inner join (
Select e, b, d
from t4
where (e > 8)
) T2(e_r, b_r, d_r)
on (b_r < b_r)
) T1
union all
select c, a
from (
Select c, a
from t4
where (12 > d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s13')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t1
where (c > (e - (b + c)))
) T1
union all
select c
from (
select c
from (
Select c
from t2
where (a = e)
) T1
union all
select e_l
from (
Select e_l, a_l, a_r_r
from (
Select e, a
from t1
where (((a + (c - b)) - 2) = 60)
) T1(e_l, a_l)
full join (
Select c_l, a_r
from (
Select c
from t4
where (59 = 82)
) T1(c_l)
left join (
Select a
from t5
where (((e * 45) + 68) > e)
) T2(a_r)
on (3 < 44)
) T2(c_l_r, a_r_r)
on (e_l > e_l)
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
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c, a, d
from t5
where (3 > d)
) T1
union all
select c
from (
Select c
from t2
where (79 < 67)
) T2
) T1
union all
select e
from (
Select e, c, a
from t2
where (d = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s15')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t1
where (d > a)
) T1
union all
select e_l, a_r
from (
Select e_l, a_r, b_r
from (
select e
from (
Select e
from t4
where (c = c)
) T1
union all
select b
from (
Select b
from t5
where (b = 34)
) T2
) T1(e_l)
left join (
Select c, a, b
from t4
where ((b - 95) < e)
) T2(c_r, a_r, b_r)
on (b_r > (55 - b_r))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l
from (
Select d_l, b_r, d_r
from (
Select d
from t1
where (77 > b)
) T1(d_l)
left join (
Select e, a, b, d
from t1
where (a = 68)
) T2(e_r, a_r, b_r, d_r)
on (d_r > 80)
) T1
union all
select c
from (
Select c
from t2
where (23 = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_r_l, a_r_l
from (
select d_r_l, a_r_l
from (
Select d_r_l, a_r_l, c_r, a_r
from (
Select d_l, a_r, d_r
from (
Select c, b, d
from t5
where (80 = 69)
) T1(c_l, b_l, d_l)
full join (
Select a, d
from t4
where (67 = (d * b))
) T2(a_r, d_r)
on ((17 * (a_r + ((d_r - (d_r - 14)) - a_r))) < d_r)
) T1(d_l_l, a_r_l, d_r_l)
inner join (
Select c, a, b
from t3
where (a < 23)
) T2(c_r, a_r, b_r)
on (a_r_l = d_r_l)
) T1
union all
select e_l, c_r
from (
Select e_l, c_r
from (
Select e
from t1
where (73 = (b + 99))
) T1(e_l)
left join (
select e, c
from (
Select e, c
from t5
where (a > c)
) T1
union all
select e, d
from (
Select e, d
from t4
where (a = 21)
) T2
) T2(e_r, c_r)
on (e_l < 78)
) T2
) T1
union all
select a, b
from (
Select a, b
from t2
where (59 < (7 * c))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t2
where (21 > 94)
) T1
union all
select a_l_l, b_l_l
from (
select a_l_l, b_l_l, e_r_l
from (
Select a_l_l, b_l_l, e_r_l, e_r
from (
Select a_l, b_l, e_r
from (
Select e, a, b
from t1
where (((28 + 48) + 39) > (67 + 37))
) T1(e_l, a_l, b_l)
inner join (
Select e
from t3
where (d > c)
) T2(e_r)
on (54 < (e_r * 12))
) T1(a_l_l, b_l_l, e_r_l)
full join (
Select e, c, a
from t2
where ((44 * 75) > 75)
) T2(e_r, c_r, a_r)
on (e_r_l = 84)
) T1
union all
select e, b, d
from (
Select e, b, d
from t4
where (38 = 64)
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
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s19')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, a, b, d
from t3
where (34 < ((71 * 39) - d))
) T1
union all
select e
from (
select e
from (
Select e
from t2
where (45 = 43)
) T1
union all
select b
from (
Select b
from t2
where (c > e)
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
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", 'a1s20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #**************************************
    
    _testmgr.testcase_end(desc)

