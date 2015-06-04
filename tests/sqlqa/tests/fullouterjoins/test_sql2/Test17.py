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
    
def test001(desc="""Joins Set 17"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l_l_l, d_r_l, c_r_r_r
from (
select c_l_l_l, d_r_l, c_r_r_r
from (
Select c_l_l_l, d_r_l, c_r_r_r
from (
Select c_l_l, e_r, d_r
from (
Select c_l, a_r
from (
Select c
from t3
where ((30 * 8) < 85)
) T1(c_l)
left join (
Select a
from t2
where ((38 + d) = c)
) T2(a_r)
on (c_l = c_l)
) T1(c_l_l, a_r_l)
inner join (
select e, d
from (
Select e, d
from t5
where (d = 74)
) T1
union all
select c, a
from (
Select c, a, b
from t2
where ((d - (10 + 17)) = d)
) T2
) T2(e_r, d_r)
on ((92 * c_l_l) = d_r)
) T1(c_l_l_l, e_r_l, d_r_l)
left join (
Select d_r_l, c_r_l, c_r_r
from (
Select e_l, c_r, d_r
from (
Select e
from t5
where (b > a)
) T1(e_l)
full join (
Select c, d
from t5
where (73 > 79)
) T2(c_r, d_r)
on (e_l > d_r)
) T1(e_l_l, c_r_l, d_r_l)
inner join (
Select d_l, c_r
from (
select d
from (
Select d
from t1
where (a < ((c - 13) + e))
) T1
union all
select a
from (
Select a, b
from t1
where (43 = 77)
) T2
) T1(d_l)
left join (
select c
from (
Select c, d
from t2
where (e < 45)
) T1
union all
select a
from (
Select a
from t3
where (18 < 87)
) T2
) T2(c_r)
on (c_r = d_l)
) T2(d_l_r, c_r_r)
on (72 > 23)
) T2(d_r_l_r, c_r_l_r, c_r_r_r)
on (c_l_l_l > 10)
) T1
union all
select e, c, a
from (
Select e, c, a
from t3
where (e < b)
) T2
) T1
union all
select e, c, d
from (
Select e, c, d
from t4
where (e = d)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l
from (
Select b_l, c_l_r_r
from (
Select b
from t4
where (92 = b)
) T1(b_l)
left join (
Select c_l, c_l_r
from (
select c
from (
select c
from (
Select c, d
from t4
where (b = 96)
) T1
union all
select a
from (
Select a
from t5
where (7 > 8)
) T2
) T1
union all
select c
from (
select c
from (
Select c
from t4
where (c = d)
) T1
union all
select e_l
from (
Select e_l, c_l, d_r
from (
Select e, c
from t3
where (96 > a)
) T1(e_l, c_l)
left join (
select b, d
from (
Select b, d
from t1
where (0 > e)
) T1
union all
select a_l, b_l
from (
Select a_l, b_l, d_l, e_l_r, d_r_l_r_r, b_l_r
from (
Select e, a, b, d
from t2
where (7 = 18)
) T1(e_l, a_l, b_l, d_l)
left join (
Select e_l, b_l, b_r_r_r, d_r_l_r
from (
Select e, b
from t5
where (a < e)
) T1(e_l, b_l)
left join (
Select d_r_l, b_r_r
from (
Select e_l, d_l, d_r
from (
Select e, a, b, d
from t1
where (7 < d)
) T1(e_l, a_l, b_l, d_l)
left join (
Select d
from t4
where (51 > 15)
) T2(d_r)
on (d_r = d_r)
) T1(e_l_l, d_l_l, d_r_l)
full join (
Select e_l, b_r
from (
Select e
from t5
where (d = 3)
) T1(e_l)
left join (
Select b
from t2
where (b < (b * 85))
) T2(b_r)
on (e_l < (b_r + e_l))
) T2(e_l_r, b_r_r)
on ((d_r_l - (d_r_l + d_r_l)) > 61)
) T2(d_r_l_r, b_r_r_r)
on ((e_l * 73) = 28)
) T2(e_l_r, b_l_r, b_r_r_r_r, d_r_l_r_r)
on (e_l_r = 56)
) T2
) T2(b_r, d_r)
on (c_l = 42)
) T2
) T2
) T1(c_l)
inner join (
Select c_l, e_r
from (
Select c, a, d
from t1
where (c < a)
) T1(c_l, a_l, d_l)
inner join (
Select e
from t5
where (a = (e + d))
) T2(e_r)
on ((c_l * e_r) > e_r)
) T2(c_l_r, e_r_r)
on (72 < 64)
) T2(c_l_r, c_l_r_r)
on (74 > 6)
) T1
union all
select d
from (
Select d
from t3
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
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t3
where (c = 88)
) T1
union all
select c
from (
select c, b, d
from (
Select c, b, d
from t2
where (d = e)
) T1
union all
select b_l, e_r, b_r
from (
Select b_l, e_r, b_r
from (
Select b
from t3
where (d > e)
) T1(b_l)
left join (
Select e, b, d
from t3
where ((19 + 29) < d)
) T2(e_r, b_r, d_r)
on (e_r < (47 + b_l))
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
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t2
where (8 = (c * (c - 82)))
) T1
union all
select e
from (
Select e
from t1
where (96 < 42)
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
Select e, a, b, d
from t3
where (40 = 27)
) T1
union all
select b, d
from (
Select b, d
from t3
where (b = (32 * d))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b
from t5
where (e = e)
) T1
union all
select e, c, a
from (
Select e, c, a
from t1
where (7 < 97)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t3
where ((72 + e) = ((85 + 9) + e))
) T1    

union all
select e, c
from (
Select e, c, a, b
from t2
where (23 > 90)
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
from t5
where (a < (b - d))
) T1
union all
select c_l_l_l
from (
select c_l_l_l
from (
Select c_l_l_l, a_r_l, b_r
from (
Select c_l_l, a_r, d_r
from (
Select c_l, b_l_l_r, b_r_l_r
from (
Select c
from t5
where ((38 * (b - (c + b))) = 59)
) T1(c_l)
full join (
Select b_r_l, b_l_l, b_r
from (
Select b_l, b_r, d_r
from (
Select c, b, d
from t2
where (e < 73)
) T1(c_l, b_l, d_l)
inner join (
Select b, d
from t2
where (42 > d)
) T2(b_r, d_r)
on (b_r = d_r)
) T1(b_l_l, b_r_l, d_r_l)
left join (
Select b
from t2
where (55 = (c - 48))
) T2(b_r)
on (85 > ((52 + 1) - b_r_l))
) T2(b_r_l_r, b_l_l_r, b_r_r)
on (b_l_l_r > b_r_l_r)
) T1(c_l_l, b_l_l_r_l, b_r_l_r_l)
left join (
Select c, a, d
from t4
where (d = 63)
) T2(c_r, a_r, d_r)
on (a_r = (c_l_l + (a_r * (d_r - d_r))))
) T1(c_l_l_l, a_r_l, d_r_l)
full join (
Select c, b
from t4
where (31 = 42)
) T2(c_r, b_r)
on (c_l_l_l > 43)
) T1
union all
select c
from (
Select c
from t4
where (89 > e)
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
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, e_r
from (
Select a_l, e_r, c_r, a_r
from (
Select a, d
from t1
where (b = b)
) T1(a_l, d_l)
left join (
Select e, c, a
from t2
where (9 = 13)
) T2(e_r, c_r, a_r)
on (65 > 66)
) T1
union all
select c, b
from (
Select c, b
from t1
where (c = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t1
where (15 > c)
) T1
union all
select a
from (
Select a, b
from t5
where (65 = (a - 32))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l
from (
Select e_l, c_l, c_l_r
from (
Select e, c, a
from t3
where (b > c)
) T1(e_l, c_l, a_l)
full join (
select c_l, a_l, b_l, a_r_r
from (
Select c_l, a_l, b_l, a_r_r
from (
Select c, a, b, d
from t2
where (47 < 87)
) T1(c_l, a_l, b_l, d_l)
full join (
Select a_l, a_r
from (
Select a
from t5
where ((b + b) = a)
) T1(a_l)
inner join (
Select a, d
from t1
where (54 > d)
) T2(a_r, d_r)
on (69 = a_l)
) T2(a_l_r, a_r_r)
on (19 = ((a_l - b_l) + a_l))
) T1
union all
select c, a, b, d
from (
Select c, a, b, d
from t1
where (c = d)
) T2
) T2(c_l_r, a_l_r, b_l_r, a_r_r_r)
on (8 = c_l)
) T1
union all
select e, d
from (
Select e, d
from t3
where (e < e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t5
where (a < a)
) T1
union all
select e, b
from (
Select e, b
from t2
where (a = (36 - (5 + (35 + 23))))
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
select c, b, d
from (
Select c, b, d
from t3
where (99 > 36)
) T1
union all
select a, b, d
from (
Select a, b, d
from t5
where (a = d)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t2
where (48 > a)
) T1
union all
select b
from (
Select b
from t4
where ((((83 + 55) * 68) - (((b * 52) * b) + b)) = 76)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e, a
from t1
where (c > 17)
) T1
union all
select e
from (
select e
from (
Select e, c
from t2
where (20 = 47)
) T1
union all
select b
from (
Select b
from t1
where ((20 * 42) = 25)
) T2
) T2
) T1
union all
select c_l_l
from (
Select c_l_l, c_r, a_r
from (
Select c_l, b_l, e_l_r, d_l_r
from (
Select c, b
from t5
where (93 = 65)
) T1(c_l, b_l)
left join (
Select e_l, d_l, d_r
from (
Select e, b, d
from t2
where (b > 24)
) T1(e_l, b_l, d_l)
full join (
Select d
from t2
where (c > e)
) T2(d_r)
on ((24 - 93) > d_r)
) T2(e_l_r, d_l_r, d_r_r)
on (c_l = b_l)
) T1(c_l_l, b_l_l, e_l_r_l, d_l_r_l)
inner join (
Select c, a
from t5
where (32 = a)
) T2(c_r, a_r)
on (90 = c_r)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t4
where (a > 32)
) T1
union all
select c, a
from (
Select c, a
from t1
where (52 = (85 * c))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, b
from (
Select c, a, b, d
from t5
where (60 = e)
) T1
union all
select b_l_l_l_l_l, a_r_l, a_r
from (
Select b_l_l_l_l_l, a_r_l, a_r
from (
Select b_l_l_l_l, e_r_l_l_l, a_r, b_r
from (
Select d_r_l, b_l_l_l, e_r_l_l, d_r
from (
Select c_r_l, b_l_l, e_r_l, d_r
from (
Select b_l, e_r, c_r
from (
Select b
from t3
where ((e - (48 - ((31 + 28) - 26))) = 69)
) T1(b_l)
left join (
Select e, c
from t4
where (a > (a + 71))
) T2(e_r, c_r)
on (96 = 37)
) T1(b_l_l, e_r_l, c_r_l)
full join (
Select d
from t2
where (b > (25 - d))
) T2(d_r)
on (e_r_l > 44)
) T1(c_r_l_l, b_l_l_l, e_r_l_l, d_r_l)
left join (
Select d
from t1
where (c = b)
) T2(d_r)
on (e_r_l_l = d_r_l)
) T1(d_r_l_l, b_l_l_l_l, e_r_l_l_l, d_r_l)
inner join (
select a, b
from (
Select a, b
from t3
where ((c + 55) < e)
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, e_r_l_r, c_r_r
from (
Select c, a
from t4
where ((60 * 11) = (94 + (2 * (48 - e))))
) T1(c_l, a_l)
full join (
Select b_r_l, e_r_l, c_r
from (
Select d_l, e_r, b_r
from (
Select d
from t4
where ((e * 53) = a)
) T1(d_l)
left join (
Select e, b
from t2
where (b = 81)
) T2(e_r, b_r)
on (90 < b_r)
) T1(d_l_l, e_r_l, b_r_l)
full join (
Select c, d
from t3
where ((39 + 66) = (a + (55 + ((51 - d) + ((0 - ((a + 11) + (33 + d))) * 88)))))
) T2(c_r, d_r)
on (31 = b_r_l)
) T2(b_r_l_r, e_r_l_r, c_r_r)
on (64 > 68)
) T2
) T2(a_r, b_r)
on (23 = 16)
) T1(b_l_l_l_l_l, e_r_l_l_l_l, a_r_l, b_r_l)
left join (
Select a
from t1
where (17 < 4)
) T2(a_r)
on ((78 - (27 - (77 * 52))) > a_r_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_r_r_l
from (
select d_r_r_l
from (
Select d_r_r_l, d_l_l, b_r
from (
Select d_l, d_r_r, b_l_r
from (
Select d
from t1
where (37 = e)
) T1(d_l)
left join (
select b_l, d_r
from (
Select b_l, d_r
from (
select b
from (
Select b, d
from t3
where (17 = 26)
) T1
union all
select e
from (
select e
from (
Select e, a, d
from t2
where (14 = b)
) T1
union all
select d
from (
Select d
from t2
where ((c - (76 * 24)) > 25)
) T2
) T2
) T1(b_l)
left join (
Select e, c, d
from t3
where (62 = 24)
) T2(e_r, c_r, d_r)
on (d_r = d_r)
) T1
union all
select e, d
from (
Select e, d
from t4
where (86 < e)
) T2
) T2(b_l_r, d_r_r)
on (((d_l + (86 + 6)) + d_r_r) < (13 + (65 - (69 * (d_l * 77)))))
) T1(d_l_l, d_r_r_l, b_l_r_l)
left join (
Select b
from t4
where (e < (b - c))
) T2(b_r)
on (74 > d_r_r_l)
) T1
union all
select e
from (
Select e
from t5
where (d = c)
) T2
) T1
union all
select e_l
from (
Select e_l, e_l_r, d_r_r, c_r_r
from (
select e
from (
Select e, b, d
from t2
where (11 > d)
) T1
union all
select e
from (
Select e
from t5
where (((20 * c) - (23 + 60)) = 52)
) T2
) T1(e_l)
left join (
Select e_l, e_r, c_r, d_r
from (
Select e, c, b
from t5
where (b > 86)
) T1(e_l, c_l, b_l)
left join (
Select e, c, d
from t3
where (58 = (c * e))
) T2(e_r, c_r, d_r)
on (21 < (31 + c_r))
) T2(e_l_r, e_r_r, c_r_r, d_r_r)
on (e_l_r = e_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
select e, a
from (
Select e, a, b
from t5
where (15 < 78)
) T1
union all
select b, d
from (
Select b, d
from t2
where (d = (e - 71))
) T2
) T1
union all
select c_l, a_l
from (
select c_l, a_l
from (
Select c_l, a_l, b_l, a_l_r
from (
Select c, a, b
from t2
where (b > e)
) T1(c_l, a_l, b_l)
left join (
Select a_l, d_l, c_r
from (
Select a, d
from t3
where ((a * 9) = 38)
) T1(a_l, d_l)
inner join (
Select c
from t3
where (b = a)
) T2(c_r)
on (d_l = 95)
) T2(a_l_r, d_l_r, c_r_r)
on (22 = 63)
) T1
union all
select e, a
from (
select e, a
from (
Select e, a, b
from t3
where ((11 + a) < d)
) T1
union all
select e, a
from (
Select e, a
from t5
where (63 = 87)
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
    _dci.expect_file(output, defs.test_dir + """/Test17exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, d_l, c_r
from (
Select a_l, d_l, c_r, d_r
from (
Select a, b, d
from t1
where (6 < 2)
) T1(a_l, b_l, d_l)
left join (
Select c, a, d
from t3
where (e < c)
) T2(c_r, a_r, d_r)
on (c_r > d_l)
) T1
union all
select e, c, d
from (
Select e, c, d
from t3
where ((47 + d) < d)
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
    
    _testmgr.testcase_end(desc)

