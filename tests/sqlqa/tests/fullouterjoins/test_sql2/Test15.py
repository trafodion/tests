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
    
def test001(desc="""Joins Set 15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, a
from t2
where ((a * (((31 - 42) + 18) * (62 * a))) = 21)
) T1
union all
select c
from (
Select c
from t2
where (c = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c
from t4
where (51 > (67 - c))
) T1
union all
select a_l_r_l
from (
Select a_l_r_l, a_r_r_l, b_l_l, d_r
from (
Select e_l, b_l, a_l_r, a_r_r
from (
Select e, b
from t3
where ((86 + 19) = (b * d))
) T1(e_l, b_l)
left join (
Select a_l, a_r
from (
select a
from (
Select a
from t4
where (a = a)
) T1
union all
select c
from (
Select c, d
from t1
where (b < c)
) T2
) T1(a_l)
left join (
Select a
from t5
where ((((59 * (e + c)) - d) * 99) < d)
) T2(a_r)
on ((79 - a_l) = 93)
) T2(a_l_r, a_r_r)
on ((((b_l * (68 * 55)) + (54 + a_l_r)) * 69) > b_l)
) T1(e_l_l, b_l_l, a_l_r_l, a_r_r_l)
full join (
Select d
from t5
where ((11 + 95) > 6)
) T2(d_r)
on (10 = 99)
) T2
) T1
union all
select c
from (
Select c, a
from t2
where (59 > a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, c_r
from (
select e
from (
Select e
from t2
where (33 = (e - a))
) T1
union all
select c
from (
Select c, d
from t4
where (d > 12)
) T2
) T1(e_l)
left join (
Select c
from t5
where (44 = (35 - d))
) T2(c_r)
on (e_l = 54)
) T1
union all
select a
from (
Select a
from t2
where (13 < (e - ((c * 21) - d)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b
from t4
where (89 < e)
) T1
union all
select b
from (
Select b
from t1
where (1 < 81)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t4
where (e = e)
) T1
union all
select c, d
from (
Select c, d
from t5
where (b = (b * b))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, a_r
from (
Select d_l, a_r
from (
Select c, a, d
from t3
where (e = e)
) T1(c_l, a_l, d_l)
inner join (
Select a
from t4
where (a > c)
) T2(a_r)
on (37 = a_r)
) T1
union all
select a, b
from (
Select a, b
from t3
where (27 < (c * d))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b
from t2
where (c = d)
) T1
union all
select d
from (
Select d
from t1
where (1 > e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, d
from (
Select e, a, d
from t2
where (d < b)
) T1
union all
select b_l, d_l, e_r_r
from (
Select b_l, d_l, e_r_r
from (
Select b, d
from t1
where (62 = a)
) T1(b_l, d_l)
inner join (
Select c_l, e_r, c_r
from (
Select c, a
from t4
where (d > e)
) T1(c_l, a_l)
left join (
Select e, c
from t3
where ((66 + (b + e)) = 68)
) T2(e_r, c_r)
on (c_r = e_r)
) T2(c_l_r, e_r_r, c_r_r)
on (e_r_r = (11 - (9 - d_l)))
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
select e
from (
Select e
from t5
where (d = b)
) T1
union all
select e
from (
Select e, c, b
from t1
where (69 = (c * 54))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t3
where (c = (c - 61))
) T1
union all
select b_l, d_l
from (
Select b_l, d_l, c_l_r, d_l_r
from (
Select b, d
from t2
where (93 < 72)
) T1(b_l, d_l)
left join (
Select c_l, d_l, d_r
from (
Select c, d
from t4
where (d > b)
) T1(c_l, d_l)
inner join (
Select d
from t2
where (14 > 29)
) T2(d_r)
on (c_l = d_l)
) T2(c_l_r, d_l_r, d_r_r)
on (c_l_r > 21)
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
select e_l
from (
Select e_l, c_l, a_l, a_r
from (
select e, c, a
from (
Select e, c, a, b
from t1
where (c > ((25 - e) * 5))
) T1
union all
select a_l, e_l_r, d_r_r
from (
Select a_l, e_l_r, d_r_r
from (
Select a
from t5
where (88 = (42 + (a - 66)))
) T1(a_l)
full join (
Select e_l, c_r, d_r
from (
select e
from (
Select e, c, d
from t4
where (((68 + e) * 3) = 55)
) T1
union all
select c
from (
Select c
from t2
where (83 < d)
) T2
) T1(e_l)
left join (
Select e, c, d
from t1
where (92 < b)
) T2(e_r, c_r, d_r)
on (e_l = (3 * 10))
) T2(e_l_r, c_r_r, d_r_r)
on (93 < (40 - d_r_r))
) T2
) T1(e_l, c_l, a_l)
full join (
Select a, b
from t5
where (64 > d)
) T2(a_r, b_r)
on (c_l = 49)
) T1
union all
select d
from (
Select d
from t4
where ((91 * b) = 98)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t1
where (13 = 34)
) T1
union all
select e, c
from (
select e, c, a, b
from (
Select e, c, a, b
from t1
where (c = 80)
) T1
union all
select e_l, b_l, a_r, b_r
from (
Select e_l, b_l, a_r, b_r
from (
Select e, b
from t1
where (32 > 74)
) T1(e_l, b_l)
inner join (
Select a, b
from t2
where (78 = d)
) T2(a_r, b_r)
on (10 = a_r)
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
select c_l, b_r
from (
Select c_l, b_r
from (
Select c
from t3
where (43 = b)
) T1(c_l)
left join (
Select b
from t4
where (55 > 23)
) T2(b_r)
on (b_r = (39 - (62 - b_r)))
) T1
union all
select c, b
from (
Select c, b
from t4
where ((55 - 73) > e)
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
select b_r_r_l, c_r_l_r, c_r_r, e_r_r
from (
Select b_r_r_l, c_r_l_r, c_r_r, e_r_r, e_l_l_r
from (
Select d_l, b_r_r
from (
Select c, d
from t4
where ((38 * (e + b)) = (84 * 44))
) T1(c_l, d_l)
left join (
Select c_l, b_l, b_r
from (
Select c, b
from t3
where (22 < 45)
) T1(c_l, b_l)
inner join (
Select b
from t3
where ((14 + e) < 33)
) T2(b_r)
on (98 > c_l)
) T2(c_l_r, b_l_r, b_r_r)
on (d_l < (d_l - b_r_r))
) T1(d_l_l, b_r_r_l)
left join (
Select e_l_l, c_r_l, e_r, c_r
from (
Select e_l, c_r
from (
Select e
from t4
where ((b * c) < 22)
) T1(e_l)
full join (
Select c
from t3
where (e = b)
) T2(c_r)
on (48 > c_r)
) T1(e_l_l, c_r_l)
inner join (
Select e, c
from t3
where (54 > (a - b))
) T2(e_r, c_r)
on (51 > c_r_l)
) T2(e_l_l_r, c_r_l_r, e_r_r, c_r_r)
on ((e_l_l_r * e_r_r) > 16)
) T1
union all
select b_r_l, d_l_l, c_r, d_r
from (
Select b_r_l, d_l_l, c_r, d_r
from (
Select a_l, b_l, d_l, b_r
from (
Select a, b, d
from t2
where ((44 + 45) = 53)
) T1(a_l, b_l, d_l)
left join (
Select a, b
from t5
where (b > a)
) T2(a_r, b_r)
on (b_l = (68 - ((17 + d_l) * a_l)))
) T1(a_l_l, b_l_l, d_l_l, b_r_l)
full join (
Select e, c, d
from t5
where (89 = d)
) T2(e_r, c_r, d_r)
on (c_r = d_r)
) T2
order by 1, 2, 3, 4
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
select a_r_l_l
from (
Select a_r_l_l, e_r, c_r
from (
select a_r_l
from (
select a_r_l
from (
select a_r_l, d_l_l
from (
Select a_r_l, d_l_l, a_r
from (
Select d_l, e_r, c_r, a_r
from (
Select c, b, d
from t1
where (b < (65 * c))
) T1(c_l, b_l, d_l)
full join (
Select e, c, a, d
from t1
where ((b * 72) = (c + (a - d)))
) T2(e_r, c_r, a_r, d_r)
on (d_l > (d_l * e_r))
) T1(d_l_l, e_r_l, c_r_l, a_r_l)
left join (
Select a
from t5
where ((84 * (e - 52)) = 5)
) T2(a_r)
on (23 = a_r_l)
) T1
union all
select b, d
from (
Select b, d
from t2
where (78 > 21)
) T2
) T1
union all
select c
from (
Select c
from t1
where (36 < 86)
) T2
) T1
union all
select d_l
from (
Select d_l, e_r_r
from (
Select d
from t2
where ((c * 64) = 78)
) T1(d_l)
left join (
Select b_l, e_r, d_r
from (
Select e, c, b
from t4
where (e > a)
) T1(e_l, c_l, b_l)
left join (
Select e, a, d
from t2
where ((d * e) = e)
) T2(e_r, a_r, d_r)
on (39 < 66)
) T2(b_l_r, e_r_r, d_r_r)
on ((d_l + (25 * (64 + d_l))) = e_r_r)
) T2
) T1(a_r_l_l)
left join (
Select e, c
from t3
where (b > 49)
) T2(e_r, c_r)
on (a_r_l_l = e_r)
) T1
union all
select a
from (
select a
from (
Select a
from t2
where (d = b)
) T1
union all
select e
from (
Select e, c
from t4
where (e > 31)
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
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b, d
from t3
where (20 > e)
) T1
union all
select e
from (
Select e
from t4
where (a < e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t4
where (d = c)
) T1
union all
select c
from (
Select c
from t1
where ((66 - d) < c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b
from t2
where (d > 64)
) T1
union all
select d
from (
Select d
from t1
where (b = 96)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_l, a_r
from (
Select e_l, b_l, a_r, d_r
from (
Select e, b
from t5
where (d > 71)
) T1(e_l, b_l)
left join (
Select c, a, d
from t4
where (82 < 62)
) T2(c_r, a_r, d_r)
on (25 < 23)
) T1
union all
select c_l, a_l_r, d_r_r
from (
Select c_l, a_l_r, d_r_r
from (
Select c
from t5
where (20 < b)
) T1(c_l)
inner join (
Select a_l, d_l, e_r, d_r
from (
Select c, a, d
from t5
where ((36 * 46) = 53)
) T1(c_l, a_l, d_l)
left join (
Select e, b, d
from t1
where (d = 36)
) T2(e_r, b_r, d_r)
on (d_r > e_r)
) T2(a_l_r, d_l_r, e_r_r, d_r_r)
on (a_l_r > 88)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t1
where (98 > ((c - b) + d))
) T1
union all
select e
from (
Select e, c
from t1
where (14 > 44)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

