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
    
def test001(desc="""Joins Set 25"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e, c
from (
select e, c
from (
Select e, c
from t3
where (b = (27 * (35 * a)))
) T1
union all
select e, b
from (
Select e, b
from t4
where (7 > 49)
) T2
) T1
union all
select a, b
from (
Select a, b
from t1
where (a = 52)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, b, d
from t5
where (c < 8)
) T1
union all
select a
from (
select a
from (
Select a, b
from t1
where (d = d)
) T1
union all
select e_l
from (
select e_l
from (
Select e_l, c_l_l_r, a_r_r, c_r_r
from (
Select e, a
from t3
where (d = d)
) T1(e_l, a_l)
inner join (
Select c_l_l, c_r, a_r
from (
Select c_l, d_l, d_r_r, d_l_r
from (
Select c, d
from t2
where (b = 40)
) T1(c_l, d_l)
left join (
Select e_l, d_l, c_r, d_r
from (
Select e, d
from t3
where ((49 - (c - ((74 + d) - 27))) = c)
) T1(e_l, d_l)
inner join (
Select c, b, d
from t3
where (98 < d)
) T2(c_r, b_r, d_r)
on (e_l > 37)
) T2(e_l_r, d_l_r, c_r_r, d_r_r)
on (75 = ((d_l_r + 56) - d_l))
) T1(c_l_l, d_l_l, d_r_r_l, d_l_r_l)
left join (
select c, a, d
from (
Select c, a, d
from t4
where (a = 67)
) T1
union all
select e_l, c_l, a_r
from (
Select e_l, c_l, a_r
from (
select e, c
from (
Select e, c, b
from t1
where (d = 6)
) T1
union all
select a, b
from (
Select a, b
from t4
where (46 = (e - c))
) T2
) T1(e_l, c_l)
inner join (
Select c, a, b, d
from t1
where (e < 92)
) T2(c_r, a_r, b_r, d_r)
on (42 > ((2 + (57 - a_r)) - 79))
) T2
) T2(c_r, a_r, d_r)
on (97 < c_l_l)
) T2(c_l_l_r, c_r_r, a_r_r)
on (19 = e_l)
) T1
union all
select a
from (
Select a
from t4
where (67 = c)
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
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t1
where (b > 23)
) T1
union all
select c
from (
Select c, a, d
from t3
where (c = 46)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, d
from t4
where (((75 + e) + 14) = 41)
) T1
union all
select e, c
from (
Select e, c
from t3
where (a = e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t4
where (e = (64 * c))
) T1
union all
select e, c
from (
Select e, c, b
from t3
where (45 > 87)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t1
where (96 = 84)
) T1
union all
select e_l_l
from (
Select e_l_l, d_r_l, c_r_l, e_r
from (
Select e_l, c_r, d_r
from (
Select e, a
from t3
where (((95 + (78 - ((b - b) + 11))) * (d + b)) = 80)
) T1(e_l, a_l)
left join (
Select c, d
from t2
where (a > 60)
) T2(c_r, d_r)
on (d_r < c_r)
) T1(e_l_l, c_r_l, d_r_l)
left join (
select e
from (
select e
from (
Select e
from t3
where (79 = 39)
) T1
union all
select a
from (
Select a
from t4
where ((d * d) = 72)
) T2
) T1
union all
select a_l
from (
select a_l, a_r
from (
Select a_l, a_r
from (
Select a
from t5
where ((e - c) = a)
) T1(a_l)
left join (
Select e, a
from t5
where (b < b)
) T2(e_r, a_r)
on (a_l < a_r)
) T1
union all
select b_l, d_l
from (
Select b_l, d_l, a_r, b_r
from (
Select b, d
from t5
where ((29 + ((c + b) + a)) > 59)
) T1(b_l, d_l)
left join (
Select c, a, b
from t4
where ((79 + d) = b)
) T2(c_r, a_r, b_r)
on (45 > d_l)
) T2
) T2
) T2(e_r)
on (e_l_l < 14)
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
select a, d
from (
Select a, d
from t5
where (3 < e)
) T1
union all
select c, a
from (
Select c, a, b
from t4
where ((e * b) = (a - 16))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, b
from t1
where (b = 3)
) T1
union all
select a, b
from (
Select a, b
from t2
where (0 > 42)
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
select e
from (
Select e, d
from t2
where ((72 * a) > (c + b))
) T1
union all
select e
from (
Select e
from t1
where (b > 14)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, b
from (
Select c, a, b
from t1
where (e < (11 * a))
) T1
union all
select e_l, b_l, c_r
from (
Select e_l, b_l, c_r, b_r, d_r
from (
Select e, b
from t3
where ((a - 10) < e)
) T1(e_l, b_l)
left join (
Select c, b, d
from t4
where (33 = 99)
) T2(c_r, b_r, d_r)
on (c_r = (8 * b_r))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, b
from (
Select c, a, b, d
from t4
where (52 > 8)
) T1
union all
select c, a, d
from (
Select c, a, d
from t4
where (e < 57)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t3
where (32 > (45 * (e * a)))
) T1
union all
select b
from (
select b
from (
Select b
from t5
where (34 > b)
) T1
union all
select d
from (
Select d
from t1
where ((e - (c - 57)) < c)
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
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t3
where (49 < b)
) T1
union all
select c_l, a_r
from (
Select c_l, a_r
from (
Select c
from t2
where (49 < ((e + a) + (b - (54 - 21))))
) T1(c_l)
full join (
Select a
from t5
where (b = b)
) T2(a_r)
on (a_r > (a_r + 65))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b, d
from (
Select a, b, d
from t4
where (90 = (d + 33))
) T1
union all
select e, a, b
from (
Select e, a, b
from t2
where (d = b)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t2
where (60 = c)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, e_r, a_r, b_r
from (
Select e, c, d
from t1
where ((33 - (10 * 28)) < 91)
) T1(e_l, c_l, d_l)
inner join (
Select e, a, b
from t3
where (c < c)
) T2(e_r, a_r, b_r)
on (c_l < ((19 - c_l) - d_l))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t2
where (42 = c)
) T1
union all
select a, d
from (
Select a, d
from t3
where (10 = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, c_l, e_l_l_l_r_r, b_l_r
from (
Select e, c
from t5
where (58 = c)
) T1(e_l, c_l)
inner join (
Select c_l, b_l, e_l_l_l_r
from (
Select c, b
from t2
where (c < 39)
) T1(c_l, b_l)
left join (
Select e_l_l_l, b_r
from (
select e_l_l
from (
Select e_l_l, c_r
from (
Select e_l, c_l, d_l, b_r, d_r
from (
Select e, c, d
from t4
where (10 < ((a * 90) * 32))
) T1(e_l, c_l, d_l)
left join (
select b, d
from (
Select b, d
from t2
where (e = b)
) T1
union all
select e, a
from (
Select e, a
from t5
where (21 = 33)
) T2
) T2(b_r, d_r)
on ((c_l * e_l) > c_l)
) T1(e_l_l, c_l_l, d_l_l, b_r_l, d_r_l)
full join (
Select c, a, b
from t5
where (d > 32)
) T2(c_r, a_r, b_r)
on (e_l_l > e_l_l)
) T1
union all
select b
from (
select b
from (
Select b
from t1
where (32 > e)
) T1
union all
select d
from (
Select d
from t2
where (d = 5)
) T2
) T2
) T1(e_l_l_l)
full join (
Select b
from t3
where ((12 * ((27 * (a - 80)) * 5)) = 8)
) T2(b_r)
on (36 = 84)
) T2(e_l_l_l_r, b_r_r)
on (53 < b_l)
) T2(c_l_r, b_l_r, e_l_l_l_r_r)
on (e_l = e_l_l_l_r_r)
) T1
union all
select b
from (
Select b
from t5
where (a > 46)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t5
where (91 = 31)
) T1
union all
select c_l, a_r_r_r
from (
Select c_l, a_r_r_r
from (
Select c
from t5
where (a = 28)
) T1(c_l)
left join (
Select c_l, a_r_r
from (
Select c
from t3
where ((77 - e) = 28)
) T1(c_l)
full join (
Select e_l, a_r
from (
Select e
from t3
where (33 < (d + 40))
) T1(e_l)
left join (
select c, a
from (
Select c, a
from t2
where (26 > 34)
) T1
union all
select a, b
from (
Select a, b
from t4
where (a > b)
) T2
) T2(c_r, a_r)
on ((e_l * e_l) = (59 + e_l))
) T2(e_l_r, a_r_r)
on (c_l < 5)
) T2(c_l_r, a_r_r_r)
on (61 < ((a_r_r_r - (84 - ((c_l * c_l) - (a_r_r_r - 22)))) + a_r_r_r))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t1
where (41 < b)
) T1
union all
select c
from (
select c
from (
Select c, a, d
from t1
where (32 < (74 + 41))
) T1
union all
select e
from (
select e
from (
Select e
from t1
where ((c * 42) < (a - 7))
) T1
union all
select e
from (
Select e, c, b
from t5
where (d > 91)
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
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, c_l_r_r_l, c_r
from (
select e_l_l, c_l_r_r_l, c_r
from (
Select e_l_l, c_l_r_r_l, c_r
from (
Select e_l, c_l_r_r, e_l_r_r
from (
Select e
from t4
where (b > a)
) T1(e_l)
left join (
Select c_l, a_l, c_l_r, e_l_r, c_r_r
from (
Select c, a
from t5
where ((d * (41 - 41)) > (((40 + c) * a) - 74))
) T1(c_l, a_l)
inner join (
Select e_l, c_l, c_r
from (
Select e, c, b
from t3
where (a > b)
) T1(e_l, c_l, b_l)
left join (
Select c
from t4
where (68 = 13)
) T2(c_r)
on (e_l = (c_l * e_l))
) T2(e_l_r, c_l_r, c_r_r)
on (51 = 69)
) T2(c_l_r, a_l_r, c_l_r_r, e_l_r_r, c_r_r_r)
on (83 = e_l_r_r)
) T1(e_l_l, c_l_r_r_l, e_l_r_r_l)
left join (
Select c
from t3
where (61 = e)
) T2(c_r)
on (((e_l_l * 58) + 73) = (c_r - e_l_l))
) T1
union all
select b_l_r_l_l, d_r_l, d_r
from (
Select b_l_r_l_l, d_r_l, d_r
from (
Select b_l_r_l, c_r, a_r, d_r
from (
Select c_l, b_l, d_l, c_l_r_r, b_l_r
from (
Select c, b, d
from t4
where (c > d)
) T1(c_l, b_l, d_l)
inner join (
Select b_l, c_l_r, e_l_r
from (
Select a, b, d
from t2
where (69 = 69)
) T1(a_l, b_l, d_l)
left join (
Select e_l, c_l, a_l, c_r
from (
Select e, c, a
from t4
where (d > (61 + (c * 83)))
) T1(e_l, c_l, a_l)
inner join (
Select c, a, b
from t2
where (((31 * (65 * a)) - a) = e)
) T2(c_r, a_r, b_r)
on (((25 + 35) + e_l) < 50)
) T2(e_l_r, c_l_r, a_l_r, c_r_r)
on (c_l_r > c_l_r)
) T2(b_l_r, c_l_r_r, e_l_r_r)
on (13 = 28)
) T1(c_l_l, b_l_l, d_l_l, c_l_r_r_l, b_l_r_l)
left join (
Select e, c, a, d
from t3
where (29 > 29)
) T2(e_r, c_r, a_r, d_r)
on (28 < b_l_r_l)
) T1(b_l_r_l_l, c_r_l, a_r_l, d_r_l)
inner join (
select d
from (
select d
from (
Select d
from t4
where (5 < 51)
) T1
union all
select c_l
from (
Select c_l, e_r
from (
select c
from (
Select c, a
from t1
where (c = 33)
) T1
union all
select c
from (
Select c
from t1
where (47 < 92)
) T2
) T1(c_l)
inner join (
select e, a
from (
Select e, a, b
from t1
where (60 = 96)
) T1
union all
select a_l, c_l_r
from (
select a_l, c_l_r
from (
Select a_l, c_l_r
from (
Select a
from t5
where (b > 52)
) T1(a_l)
left join (
select c_l
from (
Select c_l, a_l, b_r_r, c_r_l_r
from (
Select c, a
from t3
where ((76 - (c + (e - e))) > (e * 91))
) T1(c_l, a_l)
left join (
Select a_l_l, c_r_l, c_r, b_r
from (
Select a_l, c_r
from (
Select a
from t4
where ((81 - d) = 20)
) T1(a_l)
full join (
Select c
from t5
where (c = 62)
) T2(c_r)
on (c_r = c_r)
) T1(a_l_l, c_r_l)
left join (
Select c, a, b
from t3
where (((d * e) - (e + (27 * 57))) < 41)
) T2(c_r, a_r, b_r)
on (19 = 84)
) T2(a_l_l_r, c_r_l_r, c_r_r, b_r_r)
on (c_l > c_l)
) T1
union all
select e
from (
select e
from (
Select e
from t5
where ((58 * 63) > 61)
) T1
union all
select c_l
from (
select c_l, a_l
from (
Select c_l, a_l, b_l, d_r_r, e_r_r
from (
Select c, a, b, d
from t5
where (a = b)
) T1(c_l, a_l, b_l, d_l)
inner join (
Select d_l_l, e_r, d_r
from (
Select d_l, e_r
from (
Select a, d
from t4
where (98 = 29)
) T1(a_l, d_l)
left join (
Select e, d
from t3
where (74 > 79)
) T2(e_r, d_r)
on (d_l = 29)
) T1(d_l_l, e_r_l)
inner join (
Select e, d
from t2
where (63 < 35)
) T2(e_r, d_r)
on (e_r < d_l_l)
) T2(d_l_l_r, e_r_r, d_r_r)
on (56 = a_l)
) T1
union all
select a, d
from (
Select a, d
from t1
where ((((55 - e) + c) + 26) = 31)
) T2
) T2
) T2
) T2(c_l_r)
on ((34 + 39) = 78)
) T1
union all
select a, b
from (
Select a, b, d
from t2
where (87 > 4)
) T2
) T2
) T2(e_r, a_r)
on (e_r = (8 * 22))
) T2
) T1
union all
select e_l
from (
Select e_l, c_l, c_r
from (
Select e, c
from t1
where ((81 - b) = 66)
) T1(e_l, c_l)
left join (
Select c, a, b, d
from t5
where (55 = 14)
) T2(c_r, a_r, b_r, d_r)
on (77 = ((19 * (12 * (c_r + c_r))) - 53))
) T2
) T2(d_r)
on (b_l_r_l_l = 88)
) T2
) T1
union all
select c, a, b
from (
Select c, a, b
from t2
where (19 < 99)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test25exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

