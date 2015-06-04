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
    
def test001(desc="""Joins Set 28"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select c, a
from (
Select c, a, d
from t3
where (90 = 56)
) T1
union all
select a_l, d_r
from (
select a_l, d_r
from (
Select a_l, d_r
from (
select c, a, b
from (
Select c, a, b
from t3
where (b < (c * 63))
) T1
union all
select e, b, d
from (
Select e, b, d
from t4
where (89 > c)
) T2
) T1(c_l, a_l, b_l)
full join (
Select d
from t1
where ((95 * 60) = (a + c))
) T2(d_r)
on (5 = 2)
) T1
union all
select e, a
from (
Select e, a
from t1
where (c < (e * a))
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a, d
from (
Select e, c, a, d
from t2
where (43 > 19)
) T1
union all
select c, a, b, d
from (
Select c, a, b, d
from t4
where (((34 - c) * b) = 0)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t2
where (c < 78)
) T1
union all
select c
from (
Select c, b
from t1
where (a = b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
select d
from (
select d
from (
Select d
from t4
where (33 = 71)
) T1
union all
select e
from (
Select e, b
from t5
where (73 < 23)
) T2
) T1
union all
select a
from (
Select a, d
from t3
where (3 = e)
) T2
) T1
union all
select c_l
from (
Select c_l, d_l, c_r, d_r
from (
Select c, d
from t3
where (d < e)
) T1(c_l, d_l)
full join (
Select c, d
from t4
where ((e * c) > 17)
) T2(c_r, d_r)
on ((31 + 16) = d_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
select e, a
from (
Select e, a
from t1
where (e = 1)
) T1
union all
select b_l_l_l, c_r_l_l
from (
Select b_l_l_l, c_r_l_l, c_r_l, e_r, d_r
from (
Select c_r_l, b_l_l, c_r
from (
Select c_l, b_l, d_l, e_r, c_r
from (
Select c, b, d
from t2
where (((65 + d) + 97) < b)
) T1(c_l, b_l, d_l)
left join (
Select e, c, b
from t5
where (e < 70)
) T2(e_r, c_r, b_r)
on (e_r > c_r)
) T1(c_l_l, b_l_l, d_l_l, e_r_l, c_r_l)
full join (
Select c
from t5
where ((95 - 98) < d)
) T2(c_r)
on (b_l_l < 50)
) T1(c_r_l_l, b_l_l_l, c_r_l)
left join (
Select e, a, d
from t5
where ((c + (25 * d)) = c)
) T2(e_r, a_r, d_r)
on (20 > 19)
) T2
) T1
union all
select c, a
from (
Select c, a
from t5
where ((74 + e) < (a + (d + e)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c
from t5
where (((4 * e) + 95) > 85)
) T1
union all
select e
from (
Select e, d
from t4
where (43 = 82)
) T2
) T1
union all
select e
from (
Select e, b
from t4
where (d = (56 - 84))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_r_l, e_r
from (
Select b_r_l, e_r, d_r
from (
Select e_r_r_l, d_l_r_l, b_r
from (
Select a_l, c_l_r, e_r_r, d_l_r
from (
Select a, d
from t2
where ((d - b) < 96)
) T1(a_l, d_l)
inner join (
Select c_l, d_l, e_r, d_r
from (
Select c, d
from t3
where (d < (e + d))
) T1(c_l, d_l)
left join (
Select e, d
from t2
where ((47 + c) > 70)
) T2(e_r, d_r)
on ((98 * 30) = 36)
) T2(c_l_r, d_l_r, e_r_r, d_r_r)
on (98 = 97)
) T1(a_l_l, c_l_r_l, e_r_r_l, d_l_r_l)
left join (
Select b, d
from t2
where (66 < c)
) T2(b_r, d_r)
on ((12 + b_r) = d_l_r_l)
) T1(e_r_r_l_l, d_l_r_l_l, b_r_l)
left join (
Select e, c, d
from t2
where (88 = 48)
) T2(e_r, c_r, d_r)
on (93 = 19)
) T1
union all
select b, d
from (
Select b, d
from t1
where ((89 * a) = 79)
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
select d
from (
Select d
from t1
where (7 > 38)
) T1
union all
select e
from (
Select e, b
from t4
where (e = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, a
from t1
where (1 = 53)
) T1
union all
select a
from (
Select a
from t2
where (14 = b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, b_l
from (
Select c_l, b_l, c_r
from (
Select c, b
from t2
where (19 > 68)
) T1(c_l, b_l)
left join (
Select c
from t1
where (8 = b)
) T2(c_r)
on (b_l < 46)
) T1
union all
select a, b
from (
Select a, b
from t5
where (44 = 92)
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
select a_l_l, d_r_l, a_r
from (
Select a_l_l, d_r_l, a_r, d_r
from (
Select a_l, d_l, c_r, a_r, d_r
from (
Select a, d
from t4
where (c = 45)
) T1(a_l, d_l)
inner join (
Select c, a, d
from t5
where ((d + e) = (((d - 38) - b) - b))
) T2(c_r, a_r, d_r)
on (a_r = a_r)
) T1(a_l_l, d_l_l, c_r_l, a_r_l, d_r_l)
left join (
Select e, a, d
from t5
where ((b - (b - a)) > 71)
) T2(e_r, a_r, d_r)
on (d_r = (72 * d_r_l))
) T1
union all
select e, b, d
from (
Select e, b, d
from t4
where ((a - 73) = (68 + ((63 - c) - (60 - 44))))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t2
where (42 = d)
) T1
union all
select b_l, e_r
from (
Select b_l, e_r, d_r
from (
Select b
from t5
where (b < 47)
) T1(b_l)
full join (
Select e, d
from t1
where (45 < 36)
) T2(e_r, d_r)
on (58 < b_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_r_l, c_l_l
from (
Select b_r_l, c_l_l, c_r_r
from (
Select c_l, b_r
from (
Select c, a, b, d
from t2
where (d = d)
) T1(c_l, a_l, b_l, d_l)
full join (
Select b
from t4
where (71 = 17)
) T2(b_r)
on (56 = 38)
) T1(c_l_l, b_r_l)
left join (
Select d_l_l, c_r, d_r
from (
Select d_l, c_r
from (
Select d
from t2
where (26 = (93 + 0))
) T1(d_l)
full join (
Select c, b
from t1
where (e > 75)
) T2(c_r, b_r)
on (((d_l + d_l) + 3) = c_r)
) T1(d_l_l, c_r_l)
left join (
Select c, b, d
from t3
where ((38 * 55) = a)
) T2(c_r, b_r, d_r)
on (67 = 60)
) T2(d_l_l_r, c_r_r, d_r_r)
on (((b_r_l * c_r_r) + ((c_l_l + b_r_l) * (c_r_r - 52))) = c_l_l)
) T1
union all
select e, b
from (
Select e, b
from t3
where ((82 - 89) < d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a, b
from t4
where (a < e)
) T1
union all
select b_l, d_r
from (
Select b_l, d_r
from (
Select c, b
from t4
where (44 > c)
) T1(c_l, b_l)
left join (
Select d
from t2
where (24 < 0)
) T2(d_r)
on (b_l > b_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, d_l, d_r
from (
Select b_l, d_l, d_r
from (
Select c, b, d
from t3
where (76 > d)
) T1(c_l, b_l, d_l)
left join (
select d
from (
select d
from (
select d
from (
Select d
from t2
where (8 < 85)
) T1
union all
select c
from (
Select c, a, b, d
from t2
where (d = c)
) T2
) T1
union all
select c_l
from (
Select c_l, c_r, a_r
from (
Select c
from t4
where (18 = 49)
) T1(c_l)
inner join (
select c, a
from (
Select c, a
from t5
where (22 > (29 + (e - a)))
) T1
union all
select e, c
from (
Select e, c, a
from t4
where (c > d)
) T2
) T2(c_r, a_r)
on (c_l = c_r)
) T2
) T1
union all
select e
from (
Select e, a
from t4
where (d < 64)
) T2
) T2(d_r)
on ((15 + d_r) = (90 * ((d_l - (83 - d_r)) - 47)))
) T1
union all
select e_l, c_l, e_r
from (
Select e_l, c_l, e_r, a_r
from (
select e, c
from (
Select e, c
from t4
where (a = b)
) T1
union all
select a_l_l, d_r_l
from (
Select a_l_l, d_r_l, e_l_r, a_r_r
from (
Select e_l, a_l, d_r
from (
Select e, a, b
from t1
where (65 > d)
) T1(e_l, a_l, b_l)
left join (
Select a, d
from t4
where ((e - b) > a)
) T2(a_r, d_r)
on ((d_r + a_l) > 96)
) T1(e_l_l, a_l_l, d_r_l)
full join (
Select e_l, c_r, a_r
from (
Select e, d
from t1
where (98 = b)
) T1(e_l, d_l)
left join (
Select c, a
from t3
where ((b - a) > 84)
) T2(c_r, a_r)
on (e_l = a_r)
) T2(e_l_r, c_r_r, a_r_r)
on (e_l_r = a_l_l)
) T2
) T1(e_l, c_l)
left join (
Select e, a
from t3
where (e = c)
) T2(e_r, a_r)
on (e_l < 53)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_l
from (
Select a_l_l, e_r_l, d_r
from (
Select a_l, e_r
from (
Select a, b, d
from t3
where (((a * d) - e) > e)
) T1(a_l, b_l, d_l)
left join (
Select e, a
from t3
where (((51 * (b * 61)) + d) > b)
) T2(e_r, a_r)
on (29 > 46)
) T1(a_l_l, e_r_l)
left join (
Select a, d
from t2
where (68 < (28 - e))
) T2(a_r, d_r)
on (88 > 49)
) T1
union all
select e
from (
Select e
from t5
where ((e - 87) < 76)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b
from t5
where (d = (a + 70))
) T1
union all
select a_l, b_l, c_r
from (
Select a_l, b_l, c_r
from (
Select a, b
from t2
where (61 = b)
) T1(a_l, b_l)
full join (
Select c, a, d
from t3
where (d = a)
) T2(c_r, a_r, d_r)
on (b_l < 2)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
select d
from (
Select d
from t4
where (58 > e)
) T1
union all
select e
from (
Select e
from t2
where (d < (9 + e))
) T2
) T1
union all
select c
from (
Select c
from t3
where (a = 0)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t5
where (43 = (19 + (85 + 32)))
) T1
union all
select c_l
from (
Select c_l, b_l, c_r
from (
Select c, b
from t1
where ((b + a) > 76)
) T1(c_l, b_l)
left join (
select c
from (
select c
from (
Select c
from t5
where (e = d)
) T1
union all
select a
from (
Select a, b
from t5
where (30 > 72)
) T2
) T1
union all
select e_l
from (
Select e_l, a_l, d_r_r, b_l_r
from (
Select e, a
from t2
where (96 = c)
) T1(e_l, a_l)
inner join (
Select b_l, d_r
from (
Select a, b, d
from t4
where (((65 - c) + (d - 22)) > c)
) T1(a_l, b_l, d_l)
full join (
Select d
from t5
where (20 > 30)
) T2(d_r)
on (21 > 9)
) T2(b_l_r, d_r_r)
on (17 = e_l)
) T2
) T2(c_r)
on ((b_l * c_r) = c_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, d
from t2
where (96 > 73)
) T1
union all
select d
from (
Select d
from t4
where (b > 62)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #*******************************************
    
    _testmgr.testcase_end(desc)

