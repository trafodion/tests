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
    
def test001(desc="""Joins Set 11"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from t2
where (44 = (c + d))
) T1(a_l)
left join (
Select d
from t5
where (62 < 28)
) T2(d_r)
on (d_r = 15)
) T1
union all
select e, c
from (
Select e, c, d
from t1
where ((c - 85) < ((91 - c) - e))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t4
where (d < 31)
) T1
union all
select e, b
from (
Select e, b, d
from t4
where (d = (60 * 18))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, e_r
from (
Select a_l, e_r
from (
Select a, b, d
from t5
where (32 < (c * a))
) T1(a_l, b_l, d_l)
left join (
select e
from (
Select e, c, b
from t5
where ((16 * 85) < 13)
) T1
union all
select c
from (
Select c
from t5
where ((((59 - c) - 70) * (66 - d)) > 87)
) T2
) T2(e_r)
on (a_l > 0)
) T1
union all
select c, b
from (
Select c, b
from t5
where (c < (a * c))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_r_r
from (
Select a_l, b_r_r, d_l_r, b_l_r
from (
Select a, b, d
from t5
where (69 = c)
) T1(a_l, b_l, d_l)
inner join (
Select b_l, d_l, b_r
from (
Select b, d
from t3
where (e < 88)
) T1(b_l, d_l)
left join (
Select b
from t4
where ((59 - d) > 89)
) T2(b_r)
on (36 = 31)
) T2(b_l_r, d_l_r, b_r_r)
on (54 > ((b_l_r + 35) + b_r_r))
) T1
union all
select a, b
from (
Select a, b
from t5
where (e = (((c * (a + (e + 20))) + b) + 63))
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
from t4
where ((99 - ((e - 52) * c)) = (e * 4))
) T1
union all
select b
from (
Select b, d
from t1
where (((d * 55) * a) < a)
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
select d_l, e_r
from (
Select d_l, e_r, a_r, d_r
from (
Select a, b, d
from t5
where (((61 - 40) + 84) > b)
) T1(a_l, b_l, d_l)
left join (
Select e, a, d
from t1
where (16 > ((44 * e) + 92))
) T2(e_r, a_r, d_r)
on (d_r = 67)
) T1
union all
select e, b
from (
Select e, b
from t4
where (e = (e * (0 * 84)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t1
where ((c * d) > a)
) T1
union all
select b
from (
Select b
from t4
where (a = 52)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t1
where (72 = a)
) T1
union all
select a, d
from (
Select a, d
from t2
where (8 = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t4
where (c < (50 - 18))
) T1
union all
select e, a
from (
Select e, a, b
from t4
where (a = 90)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, e_r, b_r
from (
Select d_l, e_r, b_r
from (
Select c, d
from t1
where (78 > 10)
) T1(c_l, d_l)
inner join (
Select e, b
from t5
where (10 = 62)
) T2(e_r, b_r)
on (d_l < 25)
) T1
union all
select c, b, d
from (
Select c, b, d
from t1
where ((d * e) < 94)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t1
where (27 = c)
) T1
union all
select a_l, b_r_r
from (
select a_l, b_r_r
from (
Select a_l, b_r_r, e_l_r, a_r_r
from (
Select c, a, d
from t1
where (39 > 68)
) T1(c_l, a_l, d_l)
left join (
Select e_l, a_r, b_r
from (
Select e
from t1
where (47 < e)
) T1(e_l)
left join (
select a, b
from (
Select a, b
from t1
where ((45 - 86) < c)
) T1
union all
select d_l_l, a_r
from (
Select d_l_l, a_r
from (
Select c_l, d_l, d_r
from (
Select c, d
from t3
where ((d + b) = 44)
) T1(c_l, d_l)
left join (
Select e, a, b, d
from t3
where (57 = e)
) T2(e_r, a_r, b_r, d_r)
on (d_r > 64)
) T1(c_l_l, d_l_l, d_r_l)
inner join (
Select a
from t5
where (e < ((a - 79) + a))
) T2(a_r)
on (d_l_l > 23)
) T2
) T2(a_r, b_r)
on ((6 - 53) = ((11 * (84 * a_r)) + ((3 - 11) + a_r)))
) T2(e_l_r, a_r_r, b_r_r)
on ((b_r_r + 74) = e_l_r)
) T1
union all
select a, b
from (
Select a, b
from t5
where (42 < 0)
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
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, c_r, a_r
from (
Select a_l, c_r, a_r
from (
Select a, b, d
from t3
where (67 < (d * b))
) T1(a_l, b_l, d_l)
inner join (
Select e, c, a
from t4
where (37 = 85)
) T2(e_r, c_r, a_r)
on (a_r > (a_r + (30 + a_r)))
) T1
union all
select c_l, b_l, c_l_r_r
from (
Select c_l, b_l, c_l_r_r, e_l_r
from (
Select c, a, b
from t3
where ((d * e) > 46)
) T1(c_l, a_l, b_l)
full join (
Select e_l, c_l, c_l_r, e_r_r
from (
Select e, c, a, b
from t1
where (83 < 7)
) T1(e_l, c_l, a_l, b_l)
full join (
Select c_l, e_r
from (
Select e, c
from t5
where (a = d)
) T1(e_l, c_l)
inner join (
Select e
from t2
where (b = c)
) T2(e_r)
on (45 > 68)
) T2(c_l_r, e_r_r)
on (43 = e_r_r)
) T2(e_l_r, c_l_r, c_l_r_r, e_r_r_r)
on (98 < c_l_r_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (a = (32 - e))
) T1
union all
select c
from (
Select c, a, d
from t2
where (53 < b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, d
from (
Select a, d
from t5
where ((b + d) < (((50 - e) - 91) - a))
) T1
union all
select a, b
from (
select a, b
from (
Select a, b
from t5
where (66 < 14)
) T1
union all
select d_r_l, d_l_l
from (
Select d_r_l, d_l_l, e_r
from (
Select d_l, d_r
from (
Select d
from t2
where (4 > 19)
) T1(d_l)
inner join (
Select c, b, d
from t4
where (((c - d) - 71) = a)
) T2(c_r, b_r, d_r)
on (d_r < 93)
) T1(d_l_l, d_r_l)
full join (
Select e
from t2
where (98 = 32)
) T2(e_r)
on (48 > (70 + d_r_l))
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
select a, b, d
from (
Select a, b, d
from t2
where (a < (33 * (a + 18)))
) T1
union all
select c, a, d
from (
Select c, a, d
from t5
where (((a - 96) - (4 * c)) < 20)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, b, d
from t1
where (44 < ((13 + ((e + c) - c)) - 94))
) T1
union all
select b
from (
Select b
from t2
where ((d - d) < 21)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l
from (
select e_l, a_l
from (
Select e_l, a_l, c_r_l_l_r
from (
Select e, a
from t4
where (d < e)
) T1(e_l, a_l)
left join (
Select d_r_l, c_r_l_l, b_r
from (
Select c_r_l, c_r, d_r
from (
Select c_l_l, c_r
from (
Select c_l, d_r
from (
Select c, b
from t1
where (a > 60)
) T1(c_l, b_l)
full join (
Select d
from t1
where (c = 47)
) T2(d_r)
on (18 = (c_l - d_r))
) T1(c_l_l, d_r_l)
left join (
Select e, c
from t3
where (71 = 77)
) T2(e_r, c_r)
on (72 = (c_r - (95 * 61)))
) T1(c_l_l_l, c_r_l)
full join (
Select c, d
from t5
where (d = (38 - 95))
) T2(c_r, d_r)
on (c_r > c_r)
) T1(c_r_l_l, c_r_l, d_r_l)
inner join (
Select a, b, d
from t5
where (57 = 27)
) T2(a_r, b_r, d_r)
on (43 = c_r_l_l)
) T2(d_r_l_r, c_r_l_l_r, b_r_r)
on (62 < e_l)
) T1
union all
select e_l, c_l_r
from (
Select e_l, c_l_r
from (
select e
from (
select e
from (
select e
from (
Select e
from t2
where (d = e)
) T1
union all
select e
from (
Select e, c, b
from t4
where (29 = (38 - c))
) T2
) T1
union all
select c
from (
Select c, a, d
from t3
where (36 < b)
) T2
) T1
union all
select e
from (
Select e, d
from t3
where (86 > 13)
) T2
) T1(e_l)
left join (
Select c_l, b_r
from (
select c
from (
Select c
from t3
where (42 > d)
) T1
union all
select a
from (
Select a, b
from t3
where (95 = d)
) T2
) T1(c_l)
left join (
Select c, a, b, d
from t1
where (e > d)
) T2(c_r, a_r, b_r, d_r)
on (22 < c_l)
) T2(c_l_r, b_r_r)
on (c_l_r < 8)
) T2
) T1
union all
select c, a
from (
Select c, a, d
from t5
where ((96 - 10) = a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, c_l, d_l, c_r
from (
Select e, c, d
from t3
where ((c + a) < 34)
) T1(e_l, c_l, d_l)
left join (
Select c, b
from t5
where (62 = 58)
) T2(c_r, b_r)
on (77 = c_l)
) T1
union all
select c
from (
Select c
from t3
where (82 = ((a + 94) + 18))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l
from (
select d_l
from (
select d_l
from (
Select d_l, e_r
from (
Select b, d
from t4
where (54 = 48)
) T1(b_l, d_l)
full join (
Select e, d
from t3
where (a = 81)
) T2(e_r, d_r)
on ((e_r * 51) = (d_l + e_r))
) T1
union all
select c
from (
Select c
from t3
where (e < 8)
) T2
) T1
union all
select e_r_l
from (
Select e_r_l, a_r
from (
Select e_l, e_r
from (
Select e, d
from t4
where (e < b)
) T1(e_l, d_l)
left join (
Select e
from t5
where (b < d)
) T2(e_r)
on (11 < 72)
) T1(e_l_l, e_r_l)
left join (
Select e, a
from t1
where (a > 70)
) T2(e_r, a_r)
on (5 = 0)
) T2
) T1
union all
select a
from (
Select a, d
from t5
where (((e - 61) - 83) < (41 * c))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e
from t5
where ((a - (7 * 49)) < e)
) T1
union all
select a_r_l
from (
Select a_r_l, d_l_l, c_r, b_r
from (
Select d_l, a_r
from (
Select d
from t1
where (b > d)
) T1(d_l)
full join (
Select a
from t4
where (44 < (c + (68 + a)))
) T2(a_r)
on (23 = 57)
) T1(d_l_l, a_r_l)
left join (
Select e, c, b
from t2
where ((a * c) = (81 - 41))
) T2(e_r, c_r, b_r)
on (92 = d_l_l)
) T2
) T1
union all
select e
from (
select e, a, b
from (
Select e, a, b
from t2
where (53 < 51)
) T1
union all
select e, c, b
from (
Select e, c, b
from t3
where (80 > b)
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
    _dci.expect_file(output, defs.test_dir + """/Test11exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

