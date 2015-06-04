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
    
def test001(desc="""Joins Set 14"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (b = 62)
) T1
union all
select c
from (
Select c
from t1
where (b < ((88 - 52) + (29 * (20 + 53))))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b
from t1
where (c = (80 + 16))
) T1
union all
select e, c, d
from (
Select e, c, d
from t4
where (66 > 98)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (43 < e)
) T1
union all
select a_l
from (
Select a_l, d_l, b_l_r, e_r_r
from (
Select a, d
from t2
where (18 > 31)
) T1(a_l, d_l)
inner join (
Select b_l, e_r
from (
Select b
from t4
where (33 > (39 + 4))
) T1(b_l)
full join (
Select e
from t1
where (d = a)
) T2(e_r)
on (e_r > 23)
) T2(b_l_r, e_r_r)
on (a_l > e_r_r)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t3
where (73 = 10)
) T1
union all
select c, b
from (
Select c, b
from t5
where (78 < 92)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b, d
from (
Select e, b, d
from t3
where (c = 96)
) T1
union all
select e, c, a
from (
Select e, c, a, b
from t2
where (87 > c)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, c_r
from (
Select d_l, c_r
from (
Select d
from t5
where ((97 - d) = e)
) T1(d_l)
left join (
Select c
from t4
where (b = 9)
) T2(c_r)
on (77 > 91)
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select a, b
from t3
where (14 = a)
) T1(a_l, b_l)
full join (
Select a
from t4
where (c < 64)
) T2(a_r)
on (a_r = a_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t3
where (a > 63)
) T1
union all
select e
from (
select e, c, b
from (
Select e, c, b
from t5
where ((c + 44) < (18 - (c + 43)))
) T1
union all
select a_l_l, b_r_l, c_r
from (
select a_l_l, b_r_l, c_r
from (
Select a_l_l, b_r_l, c_r
from (
Select a_l, b_r
from (
Select c, a
from t4
where (66 = 92)
) T1(c_l, a_l)
left join (
Select b
from t2
where (e = a)
) T2(b_r)
on ((95 * (5 * 75)) = 32)
) T1(a_l_l, b_r_l)
left join (
Select c, a
from t4
where (28 = c)
) T2(c_r, a_r)
on (26 < b_r_l)
) T1
union all
select e_l, e_r, b_r
from (
Select e_l, e_r, b_r
from (
Select e
from t1
where (a < b)
) T1(e_l)
left join (
Select e, b
from t2
where (a = 73)
) T2(e_r, b_r)
on (b_r = (e_l - (e_l * b_r)))
) T2
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
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l
from (
Select d_l, b_r
from (
Select e, d
from t5
where ((97 * 99) > (29 * d))
) T1(e_l, d_l)
inner join (
Select b
from t5
where ((e - b) < (43 * 42))
) T2(b_r)
on (42 > 15)
) T1
union all
select c
from (
Select c
from t3
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
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, d_l, c_r, b_r
from (
Select a_l, d_l, c_r, b_r
from (
Select a, d
from t5
where (b < 60)
) T1(a_l, d_l)
inner join (
Select e, c, b
from t2
where ((12 + 92) < (c - b))
) T2(e_r, c_r, b_r)
on ((33 * a_l) = (84 * (a_l * (c_r + a_l))))
) T1
union all
select c_r_l, b_l_l, c_r, b_r
from (
Select c_r_l, b_l_l, c_r, b_r
from (
Select b_l, c_r, a_r
from (
Select b
from t3
where (d < 6)
) T1(b_l)
full join (
Select c, a
from t1
where ((95 * 85) < 91)
) T2(c_r, a_r)
on (b_l < 33)
) T1(b_l_l, c_r_l, a_r_l)
left join (
Select c, a, b
from t2
where (58 < (60 + 2))
) T2(c_r, a_r, b_r)
on (c_r = 86)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t1
where ((a - 52) < a)
) T1
union all
select e, a
from (
Select e, a
from t1
where ((e * a) = b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t2
where (88 = (b - b))
) T1
union all
select e
from (
Select e, a, d
from t2
where (d < 67)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t1
where (a = a)
) T1
union all
select e
from (
Select e, b, d
from t4
where ((e * e) < c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t4
where (53 = 3)
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, d
from t5
where (((34 - 74) * 59) < (e - b))
) T1
union all
select a, d
from (
Select a, d
from t3
where (13 > (c + e))
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
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where ((75 - (87 + a)) = b)
) T1
union all
select a_l_l
from (
Select a_l_l, c_l_l, a_r_l, b_l_l, c_r
from (
Select c_l, a_l, b_l, c_r, a_r
from (
Select c, a, b
from t2
where (60 = e)
) T1(c_l, a_l, b_l)
left join (
Select c, a
from t1
where (35 < (69 - 84))
) T2(c_r, a_r)
on (a_r = a_l)
) T1(c_l_l, a_l_l, b_l_l, c_r_l, a_r_l)
inner join (
Select c, a
from t5
where (47 < 47)
) T2(c_r, a_r)
on (a_r_l = b_l_l)
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
Select a, b
from t1
where (b = b)
) T1
union all
select b
from (
Select b
from t2
where (e < 42)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t4
where ((d - 40) > c)
) T1
union all
select a_l, e_r
from (
Select a_l, e_r, b_r
from (
select e, c, a
from (
Select e, c, a
from t4
where (c = (52 + (a + 2)))
) T1
union all
select a_l_r_l, c_r, a_r
from (
Select a_l_r_l, c_r, a_r, b_r
from (
Select e_r_l, a_l_r
from (
Select e_l, b_l, e_r, a_r
from (
select e, b
from (
Select e, b, d
from t3
where (a = (22 - 46))
) T1
union all
select a, b
from (
Select a, b
from t1
where (a = (89 - a))
) T2
) T1(e_l, b_l)
inner join (
select e, a
from (
Select e, a, d
from t5
where (e = ((e + b) + b))
) T1
union all
select c, a
from (
Select c, a
from t1
where (2 > a)
) T2
) T2(e_r, a_r)
on ((e_r - a_r) = 54)
) T1(e_l_l, b_l_l, e_r_l, a_r_l)
inner join (
Select a_l, c_r
from (
Select c, a, d
from t1
where (8 = c)
) T1(c_l, a_l, d_l)
full join (
Select e, c, a, d
from t5
where (19 = e)
) T2(e_r, c_r, a_r, d_r)
on (((a_l * 94) + c_r) = c_r)
) T2(a_l_r, c_r_r)
on (77 = a_l_r)
) T1(e_r_l_l, a_l_r_l)
full join (
Select c, a, b
from t4
where (48 < d)
) T2(c_r, a_r, b_r)
on (43 = a_r)
) T2
) T1(e_l, c_l, a_l)
left join (
Select e, c, b
from t5
where ((a - 65) < 72)
) T2(e_r, c_r, b_r)
on (79 = 39)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t1
where (d = 0)
) T1
union all
select e_l
from (
Select e_l, a_r
from (
Select e, c
from t1
where (9 = e)
) T1(e_l, c_l)
left join (
Select a
from t5
where (47 < 99)
) T2(a_r)
on (89 > e_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, d
from t4
where (a < 25)
) T1
union all
select e
from (
Select e
from t1
where (79 = (a + e))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_r_r
from (
Select e_l, a_r_r
from (
Select e, b, d
from t4
where (e = d)
) T1(e_l, b_l, d_l)
left join (
select e_r_l, a_r, b_r
from (
Select e_r_l, a_r, b_r
from (
Select b_l, e_r
from (
Select b
from t1
where (b < c)
) T1(b_l)
left join (
Select e
from t3
where (b > 53)
) T2(e_r)
on (b_l = 34)
) T1(b_l_l, e_r_l)
left join (
Select a, b, d
from t3
where ((4 + a) = 66)
) T2(a_r, b_r, d_r)
on (44 = (b_r - (b_r + e_r_l)))
) T1
union all
select e, a, b
from (
Select e, a, b, d
from t2
where (29 > (e + 45))
) T2
) T2(e_r_l_r, a_r_r, b_r_r)
on (((54 + e_l) + e_l) = 91)
) T1
union all
select e, c
from (
Select e, c, b
from t5
where (c = (59 - d))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t5
where (b = 12)
) T1
union all
select c_l, e_r
from (
Select c_l, e_r, d_r
from (
Select e, c, d
from t3
where (d = a)
) T1(e_l, c_l, d_l)
left join (
Select e, d
from t4
where (72 < 3)
) T2(e_r, d_r)
on (58 > (67 + 13))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test14exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

