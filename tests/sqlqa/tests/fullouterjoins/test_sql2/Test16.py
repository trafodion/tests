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
    
def test001(desc="""Joins Set 16"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t1
where (31 = d)
) T1
union all
select a_l, b_r_r_r
from (
select a_l, b_r_r_r
from (
Select a_l, b_r_r_r
from (
Select a
from t1
where (e < 17)
) T1(a_l)
left join (
Select a_l, b_r_r, d_l_r
from (
select a, b
from (
Select a, b, d
from t2
where (((b + (c - (1 - (57 * (78 * c))))) + c) = a)
) T1
union all
select e, d
from (
Select e, d
from t4
where (88 = 8)
) T2
) T1(a_l, b_l)
full join (
Select b_l, d_l, a_r, b_r, d_r
from (
Select b, d
from t4
where (a < 48)
) T1(b_l, d_l)
inner join (
Select c, a, b, d
from t3
where (a > d)
) T2(c_r, a_r, b_r, d_r)
on (5 = 4)
) T2(b_l_r, d_l_r, a_r_r, b_r_r, d_r_r)
on (74 > d_l_r)
) T2(a_l_r, b_r_r_r, d_l_r_r)
on (79 = ((b_r_r_r + 75) + (a_l * a_l)))
) T1
union all
select c, a
from (
Select c, a, b, d
from t4
where (d > 14)
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
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, d_r
from (
Select b_l, d_r
from (
Select c, b
from t4
where (92 = b)
) T1(c_l, b_l)
left join (
Select c, b, d
from t5
where (81 < e)
) T2(c_r, b_r, d_r)
on ((d_r - (9 - (90 * d_r))) > b_l)
) T1
union all
select e, d
from (
Select e, d
from t1
where ((e * 26) = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t2
where ((((7 * (7 * 83)) * d) - 25) = 84)
) T1
union all
select e, d
from (
Select e, d
from t2
where ((97 + 96) > b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t2
where (24 < 95)
) T1
union all
select d_l
from (
select d_l, d_r
from (
Select d_l, d_r
from (
Select c, a, d
from t1
where (((64 + b) - d) > 56)
) T1(c_l, a_l, d_l)
inner join (
select d
from (
Select d
from t2
where (e > 9)
) T1
union all
select b_l
from (
Select b_l, d_l, b_r
from (
Select b, d
from t1
where ((b - 45) = (63 * 73))
) T1(b_l, d_l)
inner join (
Select b
from t3
where ((e + 3) > 53)
) T2(b_r)
on (2 = 82)
) T2
) T2(d_r)
on (d_l = d_r)
) T1
union all
select e, c
from (
Select e, c, d
from t2
where (d > (a + 55))
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
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, b
from t4
where (92 > 23)
) T1
union all
select c, a
from (
Select c, a
from t4
where ((b - d) < 93)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
select a, b
from (
Select a, b, d
from t3
where (b < e)
) T1
union all
select c_l, a_l
from (
select c_l, a_l
from (
Select c_l, a_l, c_r
from (
select c, a
from (
Select c, a
from t4
where (b = d)
) T1
union all
select e, a
from (
Select e, a, b
from t4
where (a = (8 + 7))
) T2
) T1(c_l, a_l)
inner join (
Select e, c, a, d
from t4
where (39 = (82 - (c + (e * 95))))
) T2(e_r, c_r, a_r, d_r)
on (a_l = (58 - (c_l + 28)))
) T1
union all
select e, a
from (
Select e, a
from t5
where (b = (((e + 44) * b) + b))
) T2
) T2
) T1
union all
select d_l, c_r
from (
Select d_l, c_r
from (
Select d
from t4
where ((24 * (c * e)) = (1 * c))
) T1(d_l)
left join (
Select c
from t2
where ((a * ((a + d) - (22 - b))) > c)
) T2(c_r)
on (68 > 68)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t2
where (d > (50 - c))
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, c_r_r, b_l_r
from (
Select c, b
from t1
where ((d * (b * b)) = 65)
) T1(c_l, b_l)
left join (
Select b_l, c_r
from (
Select b
from t4
where (71 = 47)
) T1(b_l)
full join (
Select c
from t2
where (e = a)
) T2(c_r)
on (c_r > b_l)
) T2(b_l_r, c_r_r)
on (b_l > b_l_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_r_l
from (
Select b_r_l, e_r, a_r
from (
Select e_l_l, e_r_l, e_r, b_r
from (
Select e_l, e_r
from (
Select e
from t5
where (94 = c)
) T1(e_l)
left join (
Select e
from t3
where (c = e)
) T2(e_r)
on (e_r > (e_l * 30))
) T1(e_l_l, e_r_l)
inner join (
Select e, b
from t5
where (59 > (99 + a))
) T2(e_r, b_r)
on (35 = 49)
) T1(e_l_l_l, e_r_l_l, e_r_l, b_r_l)
inner join (
Select e, a, b
from t3
where ((91 + (30 - (49 + e))) = c)
) T2(e_r, a_r, b_r)
on (((b_r_l * b_r_l) * 39) = (b_r_l - 25))
) T1
union all
select c
from (
Select c
from t4
where ((((a - 64) + a) * (77 + (2 - 83))) = 30)
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
from t4
where (41 < (b * ((d - 44) + 66)))
) T1
union all
select c
from (
Select c
from t4
where (c > 63)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l_l
from (
Select b_l_l, c_l_r
from (
select b_l, d_l
from (
Select b_l, d_l, a_r
from (
Select a, b, d
from t2
where (16 = 18)
) T1(a_l, b_l, d_l)
left join (
Select a
from t2
where (a > 99)
) T2(a_r)
on (13 < b_l)
) T1
union all
select a, b
from (
Select a, b
from t5
where (e > b)
) T2
) T1(b_l_l, d_l_l)
left join (
Select c_l, b_r, d_r
from (
Select c, d
from t4
where (74 < 16)
) T1(c_l, d_l)
left join (
Select e, a, b, d
from t2
where (15 = e)
) T2(e_r, a_r, b_r, d_r)
on (46 > (b_r * 95))
) T2(c_l_r, b_r_r, d_r_r)
on (68 = 86)
) T1
union all
select d
from (
Select d
from t5
where (4 = 87)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t2
where (48 > a)
) T1
union all
select d_l
from (
Select d_l, b_r
from (
Select d
from t2
where (e = 50)
) T1(d_l)
left join (
Select c, b
from t5
where (23 = b)
) T2(c_r, b_r)
on (45 = 89)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t4
where (((b + e) * 39) < a)
) T1
union all
select d_l_l_l, c_r_r_l
from (
Select d_l_l_l, c_r_r_l, c_r, a_r, b_r
from (
Select c_r_l, b_l_l, d_l_l, c_r_r
from (
Select c_l, b_l, d_l, c_r
from (
Select c, a, b, d
from t5
where (59 < c)
) T1(c_l, a_l, b_l, d_l)
full join (
select c
from (
Select c
from t2
where (d = 34)
) T1
union all
select c
from (
Select c, b
from t3
where (c = 14)
) T2
) T2(c_r)
on (d_l = 81)
) T1(c_l_l, b_l_l, d_l_l, c_r_l)
full join (
Select a_l, d_l, c_r
from (
Select c, a, d
from t2
where (c > (b * 87))
) T1(c_l, a_l, d_l)
left join (
select c
from (
Select c
from t4
where ((e + (95 - e)) < 32)
) T1
union all
select c_l_l
from (
Select c_l_l, a_l_l_r_l, b_l_l, a_l_l_r
from (
Select c_l, b_l, a_l_l_r
from (
Select c, b
from t2
where (a < (((e * b) - 63) + e))
) T1(c_l, b_l)
inner join (
select a_l_l
from (
Select a_l_l, e_l_l, e_r_l, a_r
from (
Select e_l, a_l, e_r
from (
Select e, c, a, d
from t2
where ((d * c) = e)
) T1(e_l, c_l, a_l, d_l)
left join (
Select e
from t5
where ((27 * 50) = c)
) T2(e_r)
on (e_r = 61)
) T1(e_l_l, a_l_l, e_r_l)
left join (
Select a
from t5
where (e = a)
) T2(a_r)
on (89 < 7)
) T1
union all
select e
from (
Select e
from t3
where (14 > e)
) T2
) T2(a_l_l_r)
on (49 < a_l_l_r)
) T1(c_l_l, b_l_l, a_l_l_r_l)
left join (
Select a_l_l, b_r
from (
Select a_l, a_r
from (
Select a
from t4
where (b = d)
) T1(a_l)
full join (
Select a
from t4
where (a < c)
) T2(a_r)
on (a_l = (32 - 98))
) T1(a_l_l, a_r_l)
full join (
select b
from (
Select b
from t3
where (60 > ((40 + ((e + 7) * 88)) * (30 - c)))
) T1
union all
select b
from (
Select b
from t4
where (d > 55)
) T2
) T2(b_r)
on (9 > (a_l_l * a_l_l))
) T2(a_l_l_r, b_r_r)
on (a_l_l_r_l > 2)
) T2
) T2(c_r)
on ((c_r - d_l) > 3)
) T2(a_l_r, d_l_r, c_r_r)
on (59 < b_l_l)
) T1(c_r_l_l, b_l_l_l, d_l_l_l, c_r_r_l)
left join (
Select e, c, a, b
from t5
where (35 < 41)
) T2(e_r, c_r, a_r, b_r)
on (b_r < c_r_r_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b
from t2
where (d > 50)
) T1
union all
select d
from (
Select d
from t3
where (38 > e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_r_l
from (
Select e_l_r_l, d_r_r
from (
Select c_l, d_l, e_l_r
from (
Select c, a, d
from t2
where (74 = (a * e))
) T1(c_l, a_l, d_l)
inner join (
Select e_l, c_r, d_r
from (
Select e
from t3
where ((17 + 1) = d)
) T1(e_l)
full join (
Select e, c, d
from t5
where (2 = (48 * (d - (e + c))))
) T2(e_r, c_r, d_r)
on (e_l = 97)
) T2(e_l_r, c_r_r, d_r_r)
on ((42 * (e_l_r * (13 + 1))) < d_l)
) T1(c_l_l, d_l_l, e_l_r_l)
full join (
Select c_l, b_l, d_r
from (
Select c, b
from t4
where (a > d)
) T1(c_l, b_l)
left join (
Select d
from t2
where (1 < 75)
) T2(d_r)
on (b_l < 42)
) T2(c_l_r, b_l_r, d_r_r)
on ((e_l_r_l + 47) < d_r_r)
) T1
union all
select a
from (
Select a
from t2
where (d > 18)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t1
where (77 < 40)
) T1
union all
select e
from (
Select e, c
from t4
where (19 = ((84 + (d + 26)) + e))
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
select c_l, d_r_r
from (
Select c_l, d_r_r
from (
Select c
from t1
where (51 = ((a * 18) * e))
) T1(c_l)
left join (
Select a_l_l, c_r_l, e_r_l, c_r, d_r
from (
Select a_l, e_r, c_r, a_r
from (
Select a
from t2
where (38 = c)
) T1(a_l)
left join (
Select e, c, a
from t1
where (84 = (a + 89))
) T2(e_r, c_r, a_r)
on (78 = 67)
) T1(a_l_l, e_r_l, c_r_l, a_r_l)
full join (
Select c, d
from t1
where (c = 20)
) T2(c_r, d_r)
on ((92 - d_r) > a_l_l)
) T2(a_l_l_r, c_r_l_r, e_r_l_r, c_r_r, d_r_r)
on (c_l = c_l)
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, e_r, c_r, d_r
from (
Select c, a
from t5
where ((d + a) = b)
) T1(c_l, a_l)
left join (
Select e, c, a, d
from t3
where (c < 20)
) T2(e_r, c_r, a_r, d_r)
on (27 = c_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b, d
from t5
where (e > a)
) T1
union all
select c, a
from (
Select c, a
from t3
where (a = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t5
where (b > 39)
) T1
union all
select e, d
from (
Select e, d
from t3
where (c < b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, b_l_r
from (
Select b_l, b_l_r
from (
Select e, b
from t3
where (c = (54 + d))
) T1(e_l, b_l)
full join (
select b_l
from (
Select b_l, a_r, d_r
from (
select e, a, b
from (
Select e, a, b
from t1
where (d < e)
) T1
union all
select c_l, a_l, a_r
from (
Select c_l, a_l, a_r
from (
Select c, a
from t3
where (51 > 49)
) T1(c_l, a_l)
full join (
Select a
from t3
where (45 > 96)
) T2(a_r)
on (39 = 71)
) T2
) T1(e_l, a_l, b_l)
full join (
Select c, a, d
from t3
where (a = c)
) T2(c_r, a_r, d_r)
on (0 = b_l)
) T1
union all
select b
from (
Select b
from t1
where (76 = 63)
) T2
) T2(b_l_r)
on (52 = 89)
) T1
union all
select e, c
from (
Select e, c, a
from t3
where (60 < 42)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t5
where (51 > 25)
) T1
union all
select c_l
from (
Select c_l, a_l, b_r
from (
Select c, a
from t5
where ((58 * e) = c)
) T1(c_l, a_l)
left join (
Select b
from t3
where (1 > 85)
) T2(b_r)
on ((a_l - 7) > (b_r + 40))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test16exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

