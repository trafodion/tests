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
    
def test001(desc="""Joins Set 20"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select b
from (
Select b, d
from t5
where (18 = (40 - (73 - c)))
) T1
union all
select b
from (
Select b
from t2
where (12 > (b * 62))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, b
from t2
where (65 > 8)
) T1
union all
select a
from (
Select a
from t4
where (c = 99)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, b
from t2
where ((e + 16) > 76)
) T1
union all
select e
from (
Select e
from t5
where (b < (63 * c))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, b
from (
Select c, a, b
from t2
where ((e - e) > a)
) T1
union all
select a, b, d
from (
Select a, b, d
from t3
where (6 < c)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t1
where (b = a)
) T1
union all
select e
from (
Select e, c
from t3
where ((62 * d) = (c * 29))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a, b
from t2
where (e = 65)
) T1
union all
select e, b
from (
select e, b
from (
Select e, b
from t1
where (b = c)
) T1
union all
select c, a
from (
Select c, a, d
from t1
where (b > e)
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
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, b_r, d_r
from (
Select c_l, b_r, d_r
from (
Select c
from t5
where ((e - 88) = 50)
) T1(c_l)
left join (
Select a, b, d
from t1
where (b < 51)
) T2(a_r, b_r, d_r)
on ((c_l - 55) = (84 + 15))
) T1
union all
select e_l, a_l, e_r
from (
Select e_l, a_l, e_r
from (
Select e, a
from t1
where ((c + (e + b)) = c)
) T1(e_l, a_l)
left join (
select e
from (
Select e, c
from t1
where ((a * 7) < (20 * b))
) T1
union all
select b
from (
Select b
from t3
where (70 = b)
) T2
) T2(e_r)
on ((a_l + e_r) > e_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, c_l_l_r
from (
Select b_l, c_l_l_r, e_r_r
from (
Select a, b, d
from t2
where (5 > b)
) T1(a_l, b_l, d_l)
left join (
Select c_l_l, e_r
from (
select c_l
from (
select c_l, a_r
from (
select c_l, a_r
from (
Select c_l, a_r, b_r
from (
Select c
from t1
where (79 = 98)
) T1(c_l)
full join (
Select e, c, a, b
from t1
where (70 > a)
) T2(e_r, c_r, a_r, b_r)
on (a_r = a_r)
) T1
union all
select d_l_l_l, d_r
from (
Select d_l_l_l, d_r
from (
Select c_r_l, d_l_l, e_r, a_r
from (
Select e_l, d_l, e_r, c_r
from (
Select e, d
from t2
where (23 = b)
) T1(e_l, d_l)
inner join (
Select e, c, d
from t3
where (45 > 28)
) T2(e_r, c_r, d_r)
on (c_r = e_l)
) T1(e_l_l, d_l_l, e_r_l, c_r_l)
full join (
Select e, a
from t4
where (45 > d)
) T2(e_r, a_r)
on (16 < e_r)
) T1(c_r_l_l, d_l_l_l, e_r_l, a_r_l)
left join (
Select c, b, d
from t4
where (85 = 8)
) T2(c_r, b_r, d_r)
on (d_l_l_l = d_l_l_l)
) T2
) T1
union all
select a_l_l, b_l_l
from (
Select a_l_l, b_l_l, e_r
from (
Select a_l, b_l, e_r
from (
Select a, b
from t1
where (b = 73)
) T1(a_l, b_l)
full join (
Select e, a
from t3
where (a < d)
) T2(e_r, a_r)
on (41 = (a_l * a_l))
) T1(a_l_l, b_l_l, e_r_l)
inner join (
select e
from (
Select e, c, b, d
from t4
where (c = (c - (43 * d)))
) T1
union all
select b
from (
Select b
from t3
where (a < 6)
) T2
) T2(e_r)
on (b_l_l < a_l_l)
) T2
) T1
union all
select c
from (
Select c
from t1
where (c = a)
) T2
) T1(c_l_l)
inner join (
Select e, d
from t5
where (78 = a)
) T2(e_r, d_r)
on (e_r = e_r)
) T2(c_l_l_r, e_r_r)
on (93 < 19)
) T1
union all
select e, b
from (
Select e, b
from t4
where (75 < 81)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t2
where (c > c)
) T1
union all
select a_l_l, c_l_l
from (
select a_l_l, c_l_l, e_l_l
from (
Select a_l_l, c_l_l, e_l_l, c_r
from (
Select e_l, c_l, a_l, c_r
from (
Select e, c, a, d
from t1
where (48 = b)
) T1(e_l, c_l, a_l, d_l)
left join (
Select c
from t4
where (c = b)
) T2(c_r)
on (e_l > c_l)
) T1(e_l_l, c_l_l, a_l_l, c_r_l)
left join (
Select c, a
from t1
where (46 = 41)
) T2(c_r, a_r)
on (11 < 68)
) T1
union all
select c_l, c_l_r_r, e_l_r
from (
Select c_l, c_l_r_r, e_l_r
from (
select e, c
from (
Select e, c
from t1
where (76 = 98)
) T1
union all
select e, d
from (
Select e, d
from t2
where ((27 + c) > 7)
) T2
) T1(e_l, c_l)
inner join (
Select e_l, a_l_r, c_l_r
from (
Select e
from t5
where ((1 - 16) = (88 * b))
) T1(e_l)
inner join (
select c_l, a_l, a_r, d_r
from (
Select c_l, a_l, a_r, d_r
from (
Select e, c, a
from t5
where (75 < 33)
) T1(e_l, c_l, a_l)
left join (
Select e, a, d
from t3
where ((58 * c) = a)
) T2(e_r, a_r, d_r)
on ((1 + c_l) = a_l)
) T1
union all
select e, c, a, b
from (
Select e, c, a, b
from t1
where (20 = (a + e))
) T2
) T2(c_l_r, a_l_r, a_r_r, d_r_r)
on (16 = a_l_r)
) T2(e_l_r, a_l_r_r, c_l_r_r)
on (29 > e_l_r)
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
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, e_r
from (
Select c_l, e_r
from (
Select c
from t1
where (82 > c)
) T1(c_l)
full join (
Select e, a
from t1
where (12 = d)
) T2(e_r, a_r)
on (c_l > e_r)
) T1
union all
select a_l, e_r
from (
Select a_l, e_r
from (
Select a
from t1
where (b > 96)
) T1(a_l)
inner join (
select e
from (
Select e, a
from t2
where (70 = a)
) T1
union all
select c
from (
select c
from (
Select c
from t5
where (e > ((e - b) - 18))
) T1
union all
select c
from (
Select c, a
from t1
where ((((a + 83) + (e * 25)) - e) = 92)
) T2
) T2
) T2(e_r)
on ((51 - (19 - a_l)) > 89)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t4
where (b = c)
) T1
union all
select e
from (
Select e, d
from t3
where ((42 + c) < (78 - b))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t1
where (36 < (d + e))
) T1
union all
select c_l_l, d_l_l
from (
Select c_l_l, d_l_l, b_r_r, d_l_r
from (
Select e_l, c_l, d_l, d_r
from (
Select e, c, d
from t4
where (d < 56)
) T1(e_l, c_l, d_l)
full join (
Select d
from t2
where (d = c)
) T2(d_r)
on (d_l > 73)
) T1(e_l_l, c_l_l, d_l_l, d_r_l)
left join (
Select d_l, b_r
from (
Select e, d
from t1
where (e = 92)
) T1(e_l, d_l)
inner join (
select b
from (
Select b
from t2
where (37 > 2)
) T1
union all
select d
from (
Select d
from t2
where (90 > 72)
) T2
) T2(b_r)
on (91 = 95)
) T2(d_l_r, b_r_r)
on ((57 - (d_l_l + 82)) = 96)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, b
from t5
where (b > d)
) T1
union all
select c, d
from (
Select c, d
from t5
where (e < 5)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t2
where (52 = e)
) T1
union all
select a_l, d_l
from (
Select a_l, d_l, e_l_r_r
from (
Select a, d
from t4
where (18 = e)
) T1(a_l, d_l)
left join (
Select e_l, a_l_r, e_l_r
from (
select e
from (
Select e, c
from t1
where (b > c)
) T1
union all
select c
from (
Select c
from t4
where (a = e)
) T2
) T1(e_l)
full join (
Select e_l, a_l, c_r
from (
Select e, a
from t5
where (30 = 63)
) T1(e_l, a_l)
full join (
select c
from (
Select c, a, b
from t1
where (b = a)
) T1
union all
select b
from (
Select b
from t3
where (b = d)
) T2
) T2(c_r)
on ((a_l * c_r) > (28 * c_r))
) T2(e_l_r, a_l_r, c_r_r)
on (17 = (8 - a_l_r))
) T2(e_l_r, a_l_r_r, e_l_r_r)
on (a_l > a_l)
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
select c_l_l, b_l_l
from (
Select c_l_l, b_l_l, c_r
from (
select c_l, b_l
from (
Select c_l, b_l, c_l_r_r_r, d_l_r_r
from (
select c, b
from (
Select c, b, d
from t4
where (21 > c)
) T1
union all
select e, c
from (
Select e, c
from t2
where (58 = (d + (b * b)))
) T2
) T1(c_l, b_l)
left join (
Select e_l, d_l, c_l_r_r, d_l_r
from (
Select e, d
from t5
where (c = 47)
) T1(e_l, d_l)
left join (
Select b_l, d_l, c_l_r, b_r_r
from (
Select b, d
from t5
where (50 > 95)
) T1(b_l, d_l)
left join (
Select c_l, b_r
from (
select e, c
from (
select e, c
from (
Select e, c
from t3
where (46 = c)
) T1
union all
select c_l, c_r
from (
Select c_l, c_r, b_r
from (
Select c, a, b
from t1
where ((b * c) = e)
) T1(c_l, a_l, b_l)
left join (
Select c, b
from t1
where ((87 + (33 + 74)) < 31)
) T2(c_r, b_r)
on (77 < b_r)
) T2
) T1
union all
select e, c
from (
Select e, c, a
from t2
where (b = c)
) T2
) T1(e_l, c_l)
left join (
Select b
from t3
where ((d + c) > 2)
) T2(b_r)
on ((62 * 41) = 60)
) T2(c_l_r, b_r_r)
on (21 = d_l)
) T2(b_l_r, d_l_r, c_l_r_r, b_r_r_r)
on (91 = c_l_r_r)
) T2(e_l_r, d_l_r, c_l_r_r_r, d_l_r_r)
on (b_l = d_l_r_r)
) T1
union all
select e, c
from (
Select e, c
from t5
where (b = 42)
) T2
) T1(c_l_l, b_l_l)
left join (
Select c
from t1
where (e = 19)
) T2(c_r)
on (c_l_l > c_r)
) T1
union all
select c, b
from (
select c, b
from (
Select c, b
from t3
where (e = 87)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, e_r
from (
Select e, c, d
from t3
where (a = 88)
) T1(e_l, c_l, d_l)
inner join (
Select e, b, d
from t3
where ((16 + b) < (86 - a))
) T2(e_r, b_r, d_r)
on (50 < 59)
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
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
Select a_l, d_l, e_r, c_r, a_r, b_r
from (
Select a, d
from t5
where (5 > (42 - 76))
) T1(a_l, d_l)
full join (
Select e, c, a, b
from t2
where (2 = 85)
) T2(e_r, c_r, a_r, b_r)
on ((((a_r * 60) * b_r) - 72) = (17 + (d_l * d_l)))
) T1
union all
select d
from (
Select d
from t5
where ((b * 58) = 83)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t3
where (89 > (b + 50))
) T1
union all
select e
from (
Select e, d
from t2
where ((88 * 44) = (b - 40))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_r_l, b_l_r
from (
Select c_r_l, b_l_r
from (
Select a_l, c_r
from (
Select a
from t1
where (d > c)
) T1(a_l)
left join (
Select c
from t5
where (47 = 98)
) T2(c_r)
on ((58 + (36 * 82)) > 94)
) T1(a_l_l, c_r_l)
left join (
Select b_l, b_r, d_r
from (
Select c, b
from t3
where (26 = (95 - d))
) T1(c_l, b_l)
full join (
Select b, d
from t5
where (b = (b + 93))
) T2(b_r, d_r)
on (b_l > (b_r * b_l))
) T2(b_l_r, b_r_r, d_r_r)
on (10 = 81)
) T1
union all
select e, c
from (
Select e, c, b, d
from t2
where (81 = 2)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l, c_r
from (
Select e_l, a_l, c_r, b_r
from (
Select e, a
from t3
where ((a * 27) = c)
) T1(e_l, a_l)
full join (
Select c, a, b
from t3
where (e = c)
) T2(c_r, a_r, b_r)
on (4 < c_r)
) T1
union all
select a_l, b_l, a_r
from (
Select a_l, b_l, a_r
from (
Select a, b
from t2
where (c = 28)
) T1(a_l, b_l)
full join (
Select a
from t4
where (87 > (23 + 58))
) T2(a_r)
on (b_l > 34)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b, d
from (
Select e, b, d
from t4
where (81 = 49)
) T1
union all
select c, b, d
from (
Select c, b, d
from t3
where (c > 73)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test20exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #************************************************
    
    _testmgr.testcase_end(desc)

