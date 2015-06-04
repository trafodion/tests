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
    
def test001(desc='Joins Set 8'):
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
Select e
from t2
where ((c - 34) > 68)
) T1
union all
select c_r_l_l
from (
Select c_r_l_l, e_r_l, a_r_r, d_l_r
from (
Select c_r_l, e_r
from (
Select e_r_l_l, a_r_l, c_r, d_r
from (
Select e_r_l, a_r
from (
Select a_l, e_r, a_r
from (
Select a
from t3
where (91 = 48)
) T1(a_l)
left join (
Select e, a, d
from t2
where (a > (c + 92))
) T2(e_r, a_r, d_r)
on (74 > e_r)
) T1(a_l_l, e_r_l, a_r_l)
full join (
Select c, a, b
from t4
where (b < e)
) T2(c_r, a_r, b_r)
on (e_r_l < a_r)
) T1(e_r_l_l, a_r_l)
left join (
Select c, d
from t2
where (d = b)
) T2(c_r, d_r)
on (3 = c_r)
) T1(e_r_l_l_l, a_r_l_l, c_r_l, d_r_l)
full join (
Select e
from t5
where (63 = a)
) T2(e_r)
on (67 < 46)
) T1(c_r_l_l, e_r_l)
left join (
Select d_l, a_r
from (
Select d
from t2
where (50 = 30)
) T1(d_l)
left join (
Select c, a, b
from t1
where (b > (e + ((66 + 98) + 96)))
) T2(c_r, a_r, b_r)
on (9 = (a_r - d_l))
) T2(d_l_r, a_r_r)
on (36 = a_r_r)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s1')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, a, d
from t5
where (((d + c) + e) > 3)
) T1
union all
select c
from (
Select c
from t1
where ((c - 65) > 72)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s2')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l, a_l_l_l_r, c_r_r
from (
Select e_l, a_l, a_l_l_l_r, c_r_r
from (
select e, a
from (
Select e, a, b, d
from t1
where (b > c)
) T1
union all
select c, d
from (
Select c, d
from t3
where (32 = 77)
) T2
) T1(e_l, a_l)
inner join (
Select a_l_l_l, e_r, c_r
from (
Select a_l_l, c_r_r_r_l, d_r
from (
Select a_l, c_r_r_r
from (
select e, a, b
from (
Select e, a, b
from t1
where (d = 65)
) T1
union all
select b_l, e_l_r, c_r_r_r
from (
Select b_l, e_l_r, c_r_r_r
from (
Select b
from t4
where (((b - a) - c) = a)
) T1(b_l)
inner join (
Select e_l, a_l_r, d_r_r, c_r_r
from (
Select e, b
from t5
where (c = 89)
) T1(e_l, b_l)
left join (
Select a_l, c_r, d_r
from (
select a
from (
Select a, b
from t5
where (d > c)
) T1
union all
select e
from (
Select e
from t5
where (e = (b * (6 + 6)))
) T2
) T1(a_l)
left join (
Select c, d
from t3
where (59 < e)
) T2(c_r, d_r)
on (d_r < a_l)
) T2(a_l_r, c_r_r, d_r_r)
on (a_l_r = (85 * c_r_r))
) T2(e_l_r, a_l_r_r, d_r_r_r, c_r_r_r)
on ((b_l * c_r_r_r) = b_l)
) T2
) T1(e_l, a_l, b_l)
left join (
Select b_l, d_l, c_r_r
from (
Select b, d
from t1
where (((8 + 6) - (39 * c)) = 11)
) T1(b_l, d_l)
left join (
Select d_l, c_r, a_r
from (
Select d
from t2
where (68 > 45)
) T1(d_l)
left join (
Select c, a
from t5
where (84 = c)
) T2(c_r, a_r)
on (33 > c_r)
) T2(d_l_r, c_r_r, a_r_r)
on (c_r_r = 18)
) T2(b_l_r, d_l_r, c_r_r_r)
on (93 < a_l)
) T1(a_l_l, c_r_r_r_l)
full join (
Select b, d
from t3
where ((a + 13) = 83)
) T2(b_r, d_r)
on (d_r = c_r_r_r_l)
) T1(a_l_l_l, c_r_r_r_l_l, d_r_l)
left join (
Select e, c
from t4
where ((97 + 73) > (a * (a * b)))
) T2(e_r, c_r)
on (e_r > (a_l_l_l - a_l_l_l))
) T2(a_l_l_l_r, e_r_r, c_r_r)
on ((e_l * a_l_l_l_r) = c_r_r)
) T1
union all
select e_r_l, b_l_l, e_l_l_l_r, b_r_r
from (
Select e_r_l, b_l_l, e_l_l_l_r, b_r_r, a_r_r
from (
Select b_l, e_r
from (
Select b
from t1
where (84 > 2)
) T1(b_l)
left join (
Select e
from t3
where (51 = (63 + e))
) T2(e_r)
on (((39 - 70) + ((9 * (82 * (68 - 84))) + e_r)) = 19)
) T1(b_l_l, e_r_l)
left join (
Select e_l_l_l, a_r, b_r
from (
Select e_l_l, b_r_l_r_l, b_r
from (
Select e_l, e_r_l_r, b_r_l_r
from (
Select e, a
from t5
where (b > 62)
) T1(e_l, a_l)
left join (
Select b_r_l, e_r_l, e_l_r, a_r_r
from (
Select e_l, c_l, e_r, b_r
from (
Select e, c, d
from t5
where (b = 41)
) T1(e_l, c_l, d_l)
inner join (
Select e, a, b
from t1
where (a = (60 - (a - c)))
) T2(e_r, a_r, b_r)
on (86 < e_r)
) T1(e_l_l, c_l_l, e_r_l, b_r_l)
left join (
Select e_l, c_r, a_r
from (
Select e, c
from t5
where (c < (b - 50))
) T1(e_l, c_l)
inner join (
Select c, a
from t4
where (71 > d)
) T2(c_r, a_r)
on (81 < c_r)
) T2(e_l_r, c_r_r, a_r_r)
on (37 = a_r_r)
) T2(b_r_l_r, e_r_l_r, e_l_r_r, a_r_r_r)
on ((e_r_l_r - 63) > ((3 + b_r_l_r) * 2))
) T1(e_l_l, e_r_l_r_l, b_r_l_r_l)
full join (
select b
from (
Select b
from t1
where (b > ((34 - d) + 28))
) T1
union all
select e_l
from (
Select e_l, e_r, c_r
from (
Select e
from t5
where (34 > 83)
) T1(e_l)
full join (
Select e, c
from t1
where (92 > 68)
) T2(e_r, c_r)
on (32 = 90)
) T2
) T2(b_r)
on ((b_r_l_r_l - 20) = (45 * 49))
) T1(e_l_l_l, b_r_l_r_l_l, b_r_l)
inner join (
Select a, b
from t1
where (e = 33)
) T2(a_r, b_r)
on (a_r = b_r)
) T2(e_l_l_l_r, a_r_r, b_r_r)
on (e_l_l_l_r = 77)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s3')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_r_r_l_r, e_r_r_l_r
from (
Select e_l, b_r_r_l_r, e_r_r_l_r
from (
Select e, a, b
from t1
where (b = b)
) T1(e_l, a_l, b_l)
full join (
Select b_r_r_l, e_r_r_l, e_r, b_r
from (
Select e_l, c_l, b_r_r, e_l_r, e_r_r
from (
Select e, c
from t1
where (52 = (((b * 2) - b) + (58 * 98)))
) T1(e_l, c_l)
inner join (
Select e_l, e_r, b_r
from (
Select e
from t2
where (e < 46)
) T1(e_l)
left join (
Select e, c, b
from t2
where (2 = c)
) T2(e_r, c_r, b_r)
on (e_l = (93 - 80))
) T2(e_l_r, e_r_r, b_r_r)
on (51 > e_r_r)
) T1(e_l_l, c_l_l, b_r_r_l, e_l_r_l, e_r_r_l)
left join (
Select e, b
from t2
where (43 < d)
) T2(e_r, b_r)
on (e_r = 38)
) T2(b_r_r_l_r, e_r_r_l_r, e_r_r, b_r_r)
on (16 = b_r_r_l_r)
) T1
union all
select c, a, b
from (
select c, a, b
from (
Select c, a, b
from t2
where (25 > (10 - 9))
) T1
union all
select e_l, d_l, a_l_r
from (
Select e_l, d_l, a_l_r, d_l_r
from (
Select e, a, d
from t3
where ((77 + 54) < a)
) T1(e_l, a_l, d_l)
inner join (
Select a_l, d_l, a_r
from (
Select a, d
from t1
where (74 < a)
) T1(a_l, d_l)
left join (
Select c, a
from t3
where (b < (a - d))
) T2(c_r, a_r)
on ((a_l - (11 - ((17 * a_l) * 92))) > 19)
) T2(a_l_r, d_l_r, a_r_r)
on (e_l < e_l)
) T2
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s4')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b, d
from t3
where (d < 99)
) T1
union all
select d
from (
Select d
from t4
where (c < a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s5')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, a_r, d_r
from (
Select b_l, a_r, d_r
from (
Select b
from t5
where (28 = (c - 1))
) T1(b_l)
left join (
Select c, a, d
from t3
where (d = e)
) T2(c_r, a_r, d_r)
on (a_r > d_r)
) T1
union all
select e, c, a
from (
Select e, c, a
from t3
where (c = 95)
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
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, e_r
from (
Select e, c, a
from t3
where ((82 - 65) = 83)
) T1(e_l, c_l, a_l)
left join (
Select e
from t2
where ((67 + (b * e)) < 42)
) T2(e_r)
on (e_l = e_r)
) T1
union all
select e
from (
select e
from (
select e
from (
Select e, c
from t5
where ((a + c) < 15)
) T1
union all
select c
from (
Select c
from t1
where (e > 46)
) T2
) T1
union all
select c_l
from (
Select c_l, d_l_r
from (
select c
from (
select c
from (
Select c
from t2
where (80 < (10 * d))
) T1
union all
select b
from (
Select b
from t2
where (25 = 9)
) T2
) T1
union all
select c
from (
select c, b
from (
Select c, b
from t4
where (b > ((a + 69) + e))
) T1
union all
select e, a
from (
Select e, a, b
from t4
where ((15 * b) = a)
) T2
) T2
) T1(c_l)
left join (
Select c_l, d_l, c_r, b_r
from (
Select c, d
from t3
where ((37 - ((b - e) * 88)) < 6)
) T1(c_l, d_l)
full join (
Select c, b, d
from t1
where (((16 - 48) - a) = e)
) T2(c_r, b_r, d_r)
on (10 = 83)
) T2(c_l_r, d_l_r, c_r_r, b_r_r)
on (20 = c_l)
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
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s7')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t3
where (a < b)
) T1
union all
select e, b
from (
Select e, b
from t4
where (79 < e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s8')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a
from (
Select e, c, a
from t3
where (46 = e)
) T1
union all
select e, b, d
from (
Select e, b, d
from t3
where (84 < 83)
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
    
    stmt = """prepare s1 from
select c
from (
Select c, a
from t1
where ((17 * b) = ((b - 37) - e))
) T1
union all
select c
from (
select c
from (
Select c
from t5
where ((b + 6) = b)
) T1
union all
select e_r_r_r_l_l
from (
Select e_r_r_r_l_l, a_l_l_l, a_l_r, a_r_r_r, b_l_l_r_r
from (
Select a_l_l, e_r_r_r_l, d_r_l_r
from (
Select c_l, a_l, e_r_r_r, d_l_r
from (
Select c, a
from t3
where (d > d)
) T1(c_l, a_l)
inner join (
select d_l, e_r_r
from (
Select d_l, e_r_r
from (
Select e, a, d
from t1
where (e = e)
) T1(e_l, a_l, d_l)
left join (
Select c_l, e_r, a_r
from (
Select c
from t2
where (38 > b)
) T1(c_l)
full join (
Select e, a
from t1
where (a < b)
) T2(e_r, a_r)
on (c_l > e_r)
) T2(c_l_r, e_r_r, a_r_r)
on (d_l > (d_l + d_l))
) T1
union all
select e, b
from (
Select e, b
from t5
where (2 = 29)
) T2
) T2(d_l_r, e_r_r_r)
on (83 < 31)
) T1(c_l_l, a_l_l, e_r_r_r_l, d_l_r_l)
left join (
Select c_l_l, d_r_l, e_l_r
from (
Select c_l, d_r
from (
Select c
from t1
where ((e - 8) = 10)
) T1(c_l)
full join (
Select a, b, d
from t5
where ((a + c) = b)
) T2(a_r, b_r, d_r)
on (d_r > 17)
) T1(c_l_l, d_r_l)
inner join (
select e_l
from (
Select e_l, d_l, a_r, b_r
from (
Select e, d
from t2
where (11 > b)
) T1(e_l, d_l)
full join (
Select a, b
from t4
where (b > (d - a))
) T2(a_r, b_r)
on (59 < 63)
) T1
union all
select a
from (
Select a
from t2
where (c = 21)
) T2
) T2(e_l_r)
on (c_l_l < d_r_l)
) T2(c_l_l_r, d_r_l_r, e_l_r_r)
on (3 = 17)
) T1(a_l_l_l, e_r_r_r_l_l, d_r_l_r_l)
inner join (
Select a_l, b_l, b_l_l_r, a_r_r
from (
Select e, a, b
from t5
where (d = b)
) T1(e_l, a_l, b_l)
full join (
Select b_l_l, c_r, a_r
from (
select b_l, e_r
from (
Select b_l, e_r
from (
Select b
from t2
where (e = 44)
) T1(b_l)
left join (
Select e, c
from t4
where (c = 16)
) T2(e_r, c_r)
on ((68 - b_l) = 31)
) T1
union all
select e, a
from (
Select e, a, b
from t4
where (6 > 74)
) T2
) T1(b_l_l, e_r_l)
full join (
Select c, a
from t2
where (4 < 12)
) T2(c_r, a_r)
on (b_l_l = 41)
) T2(b_l_l_r, c_r_r, a_r_r)
on (51 < (23 + a_l))
) T2(a_l_r, b_l_r, b_l_l_r_r, a_r_r_r)
on (79 = 12)
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
select e
from (
Select e
from t1
where (54 = d)
) T1
union all
select c
from (
Select c
from t1
where (45 > a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s11')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t3
where (e > b)
) T1
union all
select e, b
from (
Select e, b, d
from t5
where ((49 - 87) = 19)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s12')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t1
where (31 = 62)
) T1
union all
select e
from (
Select e, a, b
from t1
where (d = 89)
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
select c
from (
Select c, a, b
from t5
where (61 > (b - ((d * ((b + b) + (38 - a))) * (d - 43))))
) T1
union all
select c
from (
select c
from (
select c, a
from (
Select c, a, d
from t4
where (d < b)
) T1
union all
select a, d
from (
Select a, d
from t1
where (51 > e)
) T2
) T1
union all
select d
from (
Select d
from t4
where (d = e)
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
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s14')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t4
where (e = (33 * 9))
) T1
union all
select a
from (
Select a
from t1
where (19 = 76)
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
select c
from (
Select c, a, b
from t2
where ((47 - (45 - 71)) < ((a - 85) * 97))
) T1
union all
select e
from (
Select e
from t2
where ((22 - (e + 2)) = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s16')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b, d
from t3
where (73 = 79)
) T1
union all
select a
from (
Select a
from t2
where (32 = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s17')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t4
where (e = 58)
) T1
union all
select b, d
from (
Select b, d
from t3
where (78 > (d - ((53 * 37) - d)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1s18')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (b > c)
) T1
union all
select a
from (
Select a, d
from t1
where (69 < 33)
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
Select a
from t1
where (87 = c)
) T1
union all
select e
from (
Select e, a
from t1
where (41 = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test08exp""", 'a1si20')
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    #*************************************************
    _testmgr.testcase_end(desc)

