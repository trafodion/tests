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
    
def test001(desc="""Joins Set 26"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e_l, c_r, d_r
from (
Select e_l, c_r, d_r
from (
Select e, a
from t2
where (27 = c)
) T1(e_l, a_l)
full join (
Select c, d
from t1
where (57 = a)
) T2(c_r, d_r)
on (10 = 32)
) T1
union all
select e, c, b
from (
Select e, c, b
from t3
where (68 = 63)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, d
from t5
where ((a * b) < (e + b))
) T1
union all
select e, d
from (
Select e, d
from t1
where (e > (d * (9 + c)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t4
where (32 > a)
) T1
union all
select b, d
from (
Select b, d
from t5
where (((d + a) + 11) = ((58 + (b - 47)) + b))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t4
where (((e + 92) + (a * (((82 + ((b + 83) * 69)) - (53 * d)) - 35))) = 83)
) T1
union all
select b
from (
Select b
from t5
where ((((92 * (b + c)) - 50) + 94) = b)
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
select a, b
from (
Select a, b
from t2
where ((65 - a) < d)
) T1
union all
select e, c
from (
Select e, c, b
from t2
where (d = e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, d
from (
Select c, a, d
from t5
where (a < b)
) T1
union all
select e, c, a
from (
Select e, c, a
from t1
where (65 > a)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a
from (
Select e, c, a
from t3
where ((3 + e) = (e * a))
) T1
union all
select e, a, d
from (
Select e, a, d
from t2
where ((31 * b) < 55)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t4
where (93 > 39)
) T1
union all
select e, b
from (
Select e, b
from t5
where (16 < a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (16 < b)
) T1
union all
select a_l
from (
Select a_l, b_r_r_r
from (
Select a
from t4
where (((86 * d) * (19 - 85)) = 27)
) T1(a_l)
left join (
Select a_l_l, b_r_r, c_r_r, b_l_r
from (
select a_l
from (
select a_l, b_l, d_l_r
from (
Select a_l, b_l, d_l_r
from (
Select e, a, b, d
from t2
where (a = 36)
) T1(e_l, a_l, b_l, d_l)
left join (
Select a_l, d_l, e_r
from (
Select a, d
from t5
where (51 < d)
) T1(a_l, d_l)
left join (
Select e, b, d
from t1
where (43 = d)
) T2(e_r, b_r, d_r)
on (5 > e_r)
) T2(a_l_r, d_l_r, e_r_r)
on ((a_l + b_l) = d_l_r)
) T1
union all
select e_l, a_l, d_r
from (
Select e_l, a_l, d_r
from (
Select e, c, a, b
from t1
where (93 = d)
) T1(e_l, c_l, a_l, b_l)
inner join (
Select d
from t1
where (47 < c)
) T2(d_r)
on (69 = a_l)
) T2
) T1
union all
select d
from (
Select d
from t4
where (b = d)
) T2
) T1(a_l_l)
inner join (
Select c_l, b_l, c_r, b_r, d_r
from (
Select c, b
from t3
where (c = d)
) T1(c_l, b_l)
inner join (
Select c, b, d
from t1
where ((37 - 17) = a)
) T2(c_r, b_r, d_r)
on (c_r > 50)
) T2(c_l_r, b_l_r, c_r_r, b_r_r, d_r_r)
on (6 = 27)
) T2(a_l_l_r, b_r_r_r, c_r_r_r, b_l_r_r)
on (55 < 58)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where (67 = b)
) T1
union all
select a
from (
Select a
from t5
where ((25 * 30) = c)
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
select e, a, b
from (
Select e, a, b
from t1
where (e < 35)
) T1
union all
select b_l, d_l, c_r
from (
Select b_l, d_l, c_r
from (
Select b, d
from t4
where ((56 * (b - a)) = a)
) T1(b_l, d_l)
full join (
Select c, d
from t3
where (3 = 37)
) T2(c_r, d_r)
on ((81 - 49) = d_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t3
where (41 > a)
) T1
union all
select c
from (
select c, a, b
from (
Select c, a, b
from t3
where (e > 37)
) T1
union all
select c, a, d
from (
Select c, a, d
from t3
where (21 < 93)
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
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, d
from t1
where (7 > c)
) T1
union all
select a_l, e_r
from (
select a_l, e_r
from (
Select a_l, e_r
from (
Select a, d
from t4
where (29 > d)
) T1(a_l, d_l)
left join (
Select e
from t4
where (((((((a + e) - 7) - b) + b) - d) * 68) = e)
) T2(e_r)
on (a_l > a_l)
) T1
union all
select e, c
from (
Select e, c, b
from t4
where (((10 + b) - (a + e)) = d)
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
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t1
where (b > (99 * e))
) T1
union all
select e
from (
select e, c, d
from (
Select e, c, d
from t2
where (34 > 66)
) T1
union all
select a, b, d
from (
Select a, b, d
from t4
where (b < c)
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
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, b
from t3
where (((11 + c) * d) > 28)
) T1
union all
select e
from (
Select e
from t2
where (d < 92)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
select c, a, b
from (
Select c, a, b, d
from t4
where (e > 42)
) T1
union all
select e, c, b
from (
select e, c, b
from (
Select e, c, b, d
from t5
where (89 = d)
) T1
union all
select a_l_l, c_r_l, e_l_r
from (
Select a_l_l, c_r_l, e_l_r
from (
Select a_l, c_r
from (
Select a
from t5
where (14 > 10)
) T1(a_l)
left join (
Select c, a, d
from t4
where ((10 - c) = (57 * a))
) T2(c_r, a_r, d_r)
on (((35 - (((86 - a_l) + ((a_l * a_l) + 62)) * (c_r + 48))) + 64) = a_l)
) T1(a_l_l, c_r_l)
left join (
Select e_l, b_r
from (
Select e, b, d
from t4
where (c < c)
) T1(e_l, b_l, d_l)
left join (
Select b
from t3
where (e < 84)
) T2(b_r)
on (93 < b_r)
) T2(e_l_r, b_r_r)
on (a_l_l = (75 - c_r_l))
) T2
) T2
) T1
union all
select a_l, d_l
from (
select a_l, d_l
from (
Select a_l, d_l, e_r
from (
Select a, d
from t3
where (49 = (9 - (e + 86)))
) T1(a_l, d_l)
left join (
Select e, b, d
from t4
where ((c - 19) = b)
) T2(e_r, b_r, d_r)
on (a_l = 45)
) T1
union all
select e, b
from (
Select e, b
from t5
where (8 = 91)
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
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t4
where (((75 - 94) * (22 + 25)) = c)
) T1
union all
select a
from (
Select a
from t3
where ((a * (d - e)) = 13)
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
select e, a
from (
Select e, a, b
from t5
where (((48 * c) + 72) = (a * (15 * 68)))
) T1
union all
select a, b
from (
Select a, b
from t1
where (64 > e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t1
where (39 = 50)
) T1
union all
select e
from (
Select e, b, d
from t5
where ((c - 24) = b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where ((71 - e) = d)
) T1
union all
select e
from (
Select e, a, b
from t2
where (b = (25 * b))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test26exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #******************************************
    _testmgr.testcase_end(desc)

