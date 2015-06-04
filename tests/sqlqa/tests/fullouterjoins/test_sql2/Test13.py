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
    
def test001(desc="""Join Tests Set 13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t5
where (92 = a)
) T1
union all
select e, c
from (
Select e, c, d
from t2
where (71 < 46)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, d
from (
Select e, a, d
from t4
where (e = 80)
) T1
union all
select e_l, e_l_r, e_r_r
from (
Select e_l, e_l_r, e_r_r
from (
Select e, c
from t2
where (e = a)
) T1(e_l, c_l)
inner join (
Select e_l, c_l, e_r
from (
Select e, c, d
from t4
where (((87 - (b * 46)) * 74) = 79)
) T1(e_l, c_l, d_l)
left join (
Select e
from t5
where (a = 89)
) T2(e_r)
on (e_l > ((56 - (64 - c_l)) * c_l))
) T2(e_l_r, c_l_r, e_r_r)
on ((e_l_r - (29 * e_l_r)) > e_l_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c
from t3
where ((((66 - 49) - (84 + 71)) * 12) < (92 * d))
) T1
union all
select c
from (
Select c, a, d
from t1
where ((71 * 10) < ((d - 48) * a))
) T2
) T1
union all
select b
from (
Select b, d
from t1
where (95 < 57)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b, d
from (
Select a, b, d
from t2
where (e > 34)
) T1
union all
select e_l, c_r, d_r
from (
Select e_l, c_r, d_r
from (
Select e
from t4
where (94 = d)
) T1(e_l)
inner join (
Select c, b, d
from t3
where (38 = (19 + b))
) T2(c_r, b_r, d_r)
on (19 > e_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, b_r
from (
select c_l, b_r
from (
Select c_l, b_r
from (
select c, b
from (
Select c, b
from t4
where (4 > ((d + b) * c))
) T1
union all
select c, b
from (
Select c, b
from t2
where ((88 + b) < a)
) T2
) T1(c_l, b_l)
inner join (
Select b
from t3
where (73 > c)
) T2(b_r)
on (b_r = 78)
) T1
union all
select e, d
from (
Select e, d
from t1
where (a > 62)
) T2
) T1
union all
select b_r_r_l, a_r
from (
Select b_r_r_l, a_r, d_r
from (
select e_l, b_r_r
from (
Select e_l, b_r_r
from (
Select e
from t5
where (60 < a)
) T1(e_l)
full join (
Select d_l, b_r
from (
Select d
from t2
where (c < 39)
) T1(d_l)
full join (
Select e, a, b
from t2
where (48 = (d + 76))
) T2(e_r, a_r, b_r)
on (d_l < b_r)
) T2(d_l_r, b_r_r)
on (b_r_r = 92)
) T1
union all
select e_l, a_r
from (
Select e_l, a_r
from (
Select e
from t2
where (a < b)
) T1(e_l)
left join (
Select a
from t3
where (56 > c)
) T2(a_r)
on (e_l = a_r)
) T2
) T1(e_l_l, b_r_r_l)
inner join (
Select a, d
from t3
where (d = a)
) T2(a_r, d_r)
on ((99 - d_r) = 30)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, d_r
from (
Select c_l, d_r
from (
Select c, b, d
from t2
where (d = (a + c))
) T1(c_l, b_l, d_l)
full join (
Select d
from t3
where (10 < 98)
) T2(d_r)
on (28 = 32)
) T1
union all
select e, a
from (
Select e, a
from t1
where (e < 98)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t2
where (((e - (92 * (69 * 92))) - b) > (56 * b))
) T1
union all
select c_l_l
from (
Select c_l_l, a_r_l, d_r
from (
Select c_l, a_r
from (
Select c
from t4
where (e = 29)
) T1(c_l)
inner join (
Select a
from t2
where (c < 80)
) T2(a_r)
on (25 = c_l)
) T1(c_l_l, a_r_l)
inner join (
Select d
from t5
where ((b - b) < 64)
) T2(d_r)
on (a_r_l < 32)
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
select e, b
from (
select e, b
from (
Select e, b, d
from t4
where (b > e)
) T1
union all
select a_l, c_r
from (
Select a_l, c_r
from (
Select a
from t2
where (b < b)
) T1(a_l)
full join (
Select e, c, d
from t1
where (28 = ((a * a) - 3))
) T2(e_r, c_r, d_r)
on (40 = a_l)
) T2
) T1
union all
select a, d
from (
Select a, d
from t1
where (b < 70)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b
from t1
where (e < d)
) T1
union all
select d
from (
Select d
from t5
where (a > 23)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, e_r
from (
Select a_l, e_r
from (
Select a, d
from t1
where (d = 33)
) T1(a_l, d_l)
full join (
select e, b
from (
Select e, b
from t1
where (37 < (b + 4))
) T1
union all
select e, a
from (
Select e, a, b
from t2
where (78 = 5)
) T2
) T2(e_r, b_r)
on (e_r < 28)
) T1
union all
select e, b
from (
Select e, b
from t5
where (c < c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, a_r
from (
Select d_l, a_r
from (
Select e, d
from t5
where (49 = 38)
) T1(e_l, d_l)
left join (
Select a, b
from t2
where (28 = b)
) T2(a_r, b_r)
on (d_l = a_r)
) T1
union all
select e_l, d_r
from (
select e_l, d_r
from (
Select e_l, d_r
from (
Select e, a
from t3
where (e < c)
) T1(e_l, a_l)
left join (
Select d
from t3
where ((13 + 62) < (c + a))
) T2(d_r)
on (9 = 57)
) T1
union all
select c, b
from (
select c, b
from (
Select c, b
from t3
where (b = d)
) T1
union all
select a_l, d_l_l_r
from (
Select a_l, d_l_l_r, c_r_r
from (
Select a
from t4
where (88 > c)
) T1(a_l)
left join (
Select d_r_l, d_l_l, c_r
from (
Select d_l, d_r
from (
Select e, a, d
from t4
where (35 = 21)
) T1(e_l, a_l, d_l)
full join (
Select d
from t5
where (a > d)
) T2(d_r)
on (92 < d_r)
) T1(d_l_l, d_r_l)
full join (
Select e, c, a, d
from t2
where (83 < (5 + b))
) T2(e_r, c_r, a_r, d_r)
on ((95 - 5) = ((d_l_l * d_r_l) + c_r))
) T2(d_r_l_r, d_l_l_r, c_r_r)
on (38 > (16 + 38))
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
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e, c, d
from (
Select e, c, d
from t2
where (d = 68)
) T1
union all
select e, c, d
from (
Select e, c, d
from t1
where (81 = c)
) T2
) T1
union all
select c
from (
Select c
from t5
where (a > 1)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t3
where (d = 57)
) T1
union all
select b_l_l, d_l_l_r_r
from (
Select b_l_l, d_l_l_r_r, b_r_r_r_r, d_r_l_r
from (
select b_l, a_r, b_r
from (
Select b_l, a_r, b_r
from (
Select b, d
from t5
where (c < e)
) T1(b_l, d_l)
left join (
Select c, a, b
from t1
where (28 > 14)
) T2(c_r, a_r, b_r)
on (b_r < b_r)
) T1
union all
select e, a, b
from (
Select e, a, b
from t3
where (a < b)
) T2
) T1(b_l_l, a_r_l, b_r_l)
left join (
Select d_r_l, d_l_l_r, b_r_r_r
from (
Select e_l, b_l, e_r, a_r, d_r
from (
select e, b
from (
Select e, b
from t2
where ((((48 * a) * d) - b) < b)
) T1
union all
select a_l, d_r
from (
Select a_l, d_r
from (
Select a, d
from t5
where (21 > 73)
) T1(a_l, d_l)
full join (
Select d
from t3
where (a = e)
) T2(d_r)
on (82 = 83)
) T2
) T1(e_l, b_l)
full join (
Select e, a, d
from t4
where (18 = c)
) T2(e_r, a_r, d_r)
on (15 > d_r)
) T1(e_l_l, b_l_l, e_r_l, a_r_l, d_r_l)
left join (
Select a_l_r_l, d_l_l, b_r_r
from (
Select d_l, a_l_r
from (
Select d
from t5
where (45 < b)
) T1(d_l)
left join (
select a_l
from (
Select a_l, b_l, d_l, d_r_r
from (
Select a, b, d
from t1
where (b = (c - b))
) T1(a_l, b_l, d_l)
full join (
Select c_l, d_l, c_r, d_r
from (
Select c, a, d
from t4
where (((a * (91 * (97 + (b - 35)))) - c) = b)
) T1(c_l, a_l, d_l)
inner join (
Select c, d
from t4
where (e = 58)
) T2(c_r, d_r)
on ((88 - c_r) < 54)
) T2(c_l_r, d_l_r, c_r_r, d_r_r)
on (a_l > 54)
) T1
union all
select b
from (
Select b
from t3
where ((24 - (26 - 33)) = d)
) T2
) T2(a_l_r)
on (38 < 25)
) T1(d_l_l, a_l_r_l)
left join (
Select b_l, a_r, b_r
from (
Select b
from t2
where (d = 55)
) T1(b_l)
left join (
Select a, b
from t2
where (34 = b)
) T2(a_r, b_r)
on (b_r = (a_r + (a_r - 48)))
) T2(b_l_r, a_r_r, b_r_r)
on (63 > b_r_r)
) T2(a_l_r_l_r, d_l_l_r, b_r_r_r)
on (b_r_r_r < (7 - d_r_l))
) T2(d_r_l_r, d_l_l_r_r, b_r_r_r_r)
on (58 = d_l_l_r_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b, d
from t3
where ((((a + 9) - a) * (a * e)) = 23)
) T1
union all
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r
from (
Select c, a
from t3
where (e = a)
) T1(c_l, a_l)
full join (
select e
from (
Select e, c
from t2
where (68 > c)
) T1
union all
select a
from (
Select a
from t4
where (4 > c)
) T2
) T2(e_r)
on (c_l < (35 + 41))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t4
where (a = 36)
) T1
union all
select d
from (
Select d
from t1
where ((c - c) = ((93 + ((b + 34) + (e - e))) * 57))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, d
from (
Select e, c, d
from t4
where (14 = 67)
) T1
union all
select e_l_l, c_r_l, c_r
from (
Select e_l_l, c_r_l, c_r
from (
Select e_l, c_l, c_r
from (
select e, c
from (
Select e, c
from t5
where (76 = 83)
) T1
union all
select e, c
from (
Select e, c, b
from t5
where (94 = 7)
) T2
) T1(e_l, c_l)
full join (
Select c
from t2
where (a < 9)
) T2(c_r)
on ((c_r * 67) < c_l)
) T1(e_l_l, c_l_l, c_r_l)
full join (
Select c
from t2
where (e > 38)
) T2(c_r)
on (59 > c_r_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b, d
from t5
where (d = 93)
) T1
union all
select e
from (
Select e
from t2
where ((79 * (c - c)) < 10)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, a_l
from (
Select c_l, a_l, a_r
from (
Select c, a, d
from t1
where (63 = 83)
) T1(c_l, a_l, d_l)
left join (
Select a
from t2
where (a = ((55 * c) + (a * 92)))
) T2(a_r)
on (a_l = 39)
) T1
union all
select c, a
from (
Select c, a
from t1
where (e > (76 * 98))
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
select c, a, d
from (
Select c, a, d
from t4
where (45 = a)
) T1
union all
select c, b, d
from (
Select c, b, d
from t4
where (58 = (c * a))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t4
where ((67 + (c - d)) < 26)
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, c_r
from (
Select e, c
from t3
where (68 > d)
) T1(e_l, c_l)
left join (
Select c
from t4
where (25 > 33)
) T2(c_r)
on (c_r < 69)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

