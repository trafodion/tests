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
    
def test001(desc="""Joins Set 12"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, b
from (
Select e, a, b
from t2
where (45 = d)
) T1
union all
select e, c, a
from (
Select e, c, a
from t5
where ((26 + 77) = a)
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
select a, b
from (
Select a, b
from t4
where (17 > 74)
) T1
union all
select e, b
from (
Select e, b
from t2
where ((a + c) > ((28 - a) + (57 + 14)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b, d
from t5
where ((17 * 17) = b)
) T1
union all
select e
from (
select e
from (
Select e
from t2
where (d > e)
) T1
union all
select a_l
from (
Select a_l, d_l, b_r
from (
Select a, b, d
from t3
where (a = d)
) T1(a_l, b_l, d_l)
full join (
Select c, b
from t1
where (24 > ((89 + 69) * d))
) T2(c_r, b_r)
on (24 > 41)
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
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, b
from t4
where (15 = e)
) T1
union all
select b
from (
Select b
from t4
where (52 = 95)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
select a, b
from (
Select a, b
from t4
where (84 > 93)
) T1
union all
select c, d
from (
Select c, d
from t2
where (a = 95)
) T2
) T1
union all
select e, b
from (
Select e, b
from t4
where (b < 32)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, d
from t3
where (44 = 66)
) T1
union all
select e
from (
Select e
from t3
where ((52 + e) = b)
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
select e, b, d
from (
Select e, b, d
from t3
where (c > c)
) T1
union all
select b_l, d_l, e_l_r
from (
select b_l, d_l, e_l_r, e_r_r_r
from (
Select b_l, d_l, e_l_r, e_r_r_r, b_l_r
from (
Select a, b, d
from t1
where (d = (d + e))
) T1(a_l, b_l, d_l)
left join (
Select e_l, b_l, e_r_r
from (
Select e, b
from t5
where (2 = (d + e))
) T1(e_l, b_l)
left join (
Select c_l, e_r
from (
Select c
from t1
where ((a * d) = 89)
) T1(c_l)
inner join (
Select e
from t2
where ((26 * ((a - d) - d)) = a)
) T2(e_r)
on (c_l = c_l)
) T2(c_l_r, e_r_r)
on (e_l > (((23 - 34) - (((b_l + 97) + e_l) + 50)) + e_r_r))
) T2(e_l_r, b_l_r, e_r_r_r)
on (b_l > ((52 + b_l) + 95))
) T1
union all
select a_l_l, a_r_l, b_r_r, d_r_r
from (
Select a_l_l, a_r_l, b_r_r, d_r_r
from (
Select a_l, c_r, a_r, b_r
from (
Select a
from t5
where (d = a)
) T1(a_l)
left join (
Select c, a, b
from t4
where (b = 77)
) T2(c_r, a_r, b_r)
on (28 = 37)
) T1(a_l_l, c_r_l, a_r_l, b_r_l)
inner join (
Select e_l, b_r, d_r
from (
Select e, c, a
from t1
where (((b * d) - b) = e)
) T1(e_l, c_l, a_l)
inner join (
Select b, d
from t1
where (c = a)
) T2(b_r, d_r)
on (d_r > 31)
) T2(e_l_r, b_r_r, d_r_r)
on (60 > a_l_l)
) T2
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, e_r
from (
select c_l, e_r
from (
Select c_l, e_r
from (
Select c, a
from t3
where (e > e)
) T1(c_l, a_l)
full join (
Select e
from t2
where ((44 + d) < c)
) T2(e_r)
on (22 = ((5 + 56) * 27))
) T1
union all
select e, a
from (
Select e, a, d
from t4
where (d = e)
) T2
) T1
union all
select c, a
from (
Select c, a
from t1
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
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a
from (
Select e, c, a
from t3
where (a < c)
) T1
union all
select a, b, d
from (
Select a, b, d
from t1
where ((0 * 53) > 45)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_l, b_r
from (
Select e_l, a_l, b_r
from (
Select e, c, a
from t1
where (a = (96 + (b * c)))
) T1(e_l, c_l, a_l)
inner join (
Select b
from t5
where (74 < d)
) T2(b_r)
on (b_r = 97)
) T1
union all
select e_l, a_l, b_l
from (
select e_l, a_l, b_l
from (
Select e_l, a_l, b_l, e_r, a_r, d_r
from (
Select e, a, b
from t2
where (c = 66)
) T1(e_l, a_l, b_l)
full join (
Select e, c, a, d
from t4
where (38 = c)
) T2(e_r, c_r, a_r, d_r)
on ((23 + (6 + 11)) > e_r)
) T1
union all
select c_l, e_r, a_r
from (
Select c_l, e_r, a_r
from (
Select c
from t3
where (d > 23)
) T1(c_l)
left join (
Select e, a, b
from t5
where (d = (c * 23))
) T2(e_r, a_r, b_r)
on (51 = c_l)
) T2
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, d_r
from (
Select e_l, d_r
from (
Select e
from t5
where (a = 37)
) T1(e_l)
inner join (
Select b, d
from t4
where (a > a)
) T2(b_r, d_r)
on (d_r = 52)
) T1
union all
select b, d
from (
Select b, d
from t5
where (b = 7)
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
select a, b
from (
Select a, b
from t2
where (d = d)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a, b
from t3
where (b < d)
) T1
union all
select e, a
from (
Select e, a
from t2
where (e < 94)
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
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t2
where (16 > b)
) T1
union all
select c
from (
Select c, b
from t2
where (d < (e + a))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, c_r
from (
Select c_l, c_r
from (
Select e, c, d
from t1
where (a < (39 + 91))
) T1(e_l, c_l, d_l)
inner join (
select c
from (
Select c
from t4
where ((70 - e) = 61)
) T1
union all
select e_r_l
from (
Select e_r_l, b_l_l_r, a_r_r, b_r_l_r
from (
select d_r_l, e_r
from (
Select d_r_l, e_r, b_r
from (
Select c_r_l, a_r, d_r
from (
Select c_l, c_r
from (
Select c, a, d
from t3
where (d = (c * a))
) T1(c_l, a_l, d_l)
inner join (
Select c
from t3
where (((75 - b) + (((67 - d) - d) - (b * 90))) > e)
) T2(c_r)
on (15 = 63)
) T1(c_l_l, c_r_l)
inner join (
Select a, b, d
from t3
where (a > e)
) T2(a_r, b_r, d_r)
on (d_r > 11)
) T1(c_r_l_l, a_r_l, d_r_l)
full join (
Select e, c, b
from t1
where ((d - ((b * (13 * 51)) - (84 - b))) < b)
) T2(e_r, c_r, b_r)
on (d_r_l = b_r)
) T1
union all
select d_l, e_r
from (
Select d_l, e_r
from (
Select d
from t4
where (d > 34)
) T1(d_l)
left join (
Select e, d
from t2
where (d < (c - ((b + c) - (c * (b - d)))))
) T2(e_r, d_r)
on ((68 - e_r) = e_r)
) T2
) T1(d_r_l_l, e_r_l)
left join (
Select b_r_l, b_l_l, a_r
from (
select b_l, c_r, b_r
from (
Select b_l, c_r, b_r
from (
select b
from (
Select b
from t2
where (24 > 0)
) T1
union all
select a
from (
select a, b
from (
Select a, b
from t1
where (94 > c)
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, b_l, a_r
from (
Select c, a, b
from t3
where (c < a)
) T1(c_l, a_l, b_l)
left join (
Select a, b
from t3
where (63 < 16)
) T2(a_r, b_r)
on ((90 + 95) > 9)
) T2
) T2
) T1(b_l)
left join (
Select c, b
from t1
where (2 = e)
) T2(c_r, b_r)
on (48 = ((c_r * 6) + 1))
) T1
union all
select c_r_r_l, c_l_r_l_l, a_r_r_r_r_r
from (
Select c_r_r_l, c_l_r_l_l, a_r_r_r_r_r, a_r_l_l_r
from (
select c_l_r_l, c_r_r
from (
Select c_l_r_l, c_r_r
from (
Select d_l_l, b_r_r, c_l_r
from (
Select a_l, d_l, e_r_r
from (
Select a, d
from t3
where (74 = e)
) T1(a_l, d_l)
full join (
Select a_l, e_r
from (
Select a
from t2
where (b < 87)
) T1(a_l)
inner join (
Select e, c, d
from t5
where (51 = (c - b))
) T2(e_r, c_r, d_r)
on (((a_l - 69) + (e_r + a_l)) < (97 + (e_r + 12)))
) T2(a_l_r, e_r_r)
on (6 = 1)
) T1(a_l_l, d_l_l, e_r_r_l)
left join (
Select c_l, b_l, b_r
from (
Select c, a, b
from t1
where (b < 44)
) T1(c_l, a_l, b_l)
inner join (
Select b
from t1
where ((e + c) = c)
) T2(b_r)
on (c_l = ((29 - c_l) * 80))
) T2(c_l_r, b_l_r, b_r_r)
on (b_r_r = d_l_l)
) T1(d_l_l_l, b_r_r_l, c_l_r_l)
inner join (
Select c_l, a_l, b_l, c_r, d_r
from (
Select e, c, a, b
from t2
where (c = e)
) T1(e_l, c_l, a_l, b_l)
inner join (
Select c, d
from t2
where (35 = e)
) T2(c_r, d_r)
on (83 < b_l)
) T2(c_l_r, a_l_r, b_l_r, c_r_r, d_r_r)
on (c_l_r_l = 52)
) T1
union all
select d_l, b_r_r
from (
Select d_l, b_r_r, b_l_l_r
from (
Select d
from t2
where (41 > d)
) T1(d_l)
left join (
Select b_l_l, b_r
from (
Select e_l, b_l, c_r, d_r
from (
Select e, b
from t3
where (37 = (75 * 18))
) T1(e_l, b_l)
full join (
Select c, d
from t3
where (45 = 31)
) T2(c_r, d_r)
on (d_r > b_l)
) T1(e_l_l, b_l_l, c_r_l, d_r_l)
left join (
Select b, d
from t3
where (a > d)
) T2(b_r, d_r)
on ((6 - (48 - (b_r + (b_l_l + 20)))) = 55)
) T2(b_l_l_r, b_r_r)
on (b_l_l_r = b_r_r)
) T2
) T1(c_l_r_l_l, c_r_r_l)
full join (
Select a_r_l_l, a_r_r_r_r, e_l_r
from (
Select a_r_l, e_r_l, a_r_l_r_r, c_l_r
from (
Select e_l, d_l, e_r, a_r
from (
Select e, b, d
from t3
where (80 = b)
) T1(e_l, b_l, d_l)
left join (
Select e, a
from t2
where (c < 47)
) T2(e_r, a_r)
on (d_l > a_r)
) T1(e_l_l, d_l_l, e_r_l, a_r_l)
full join (
Select c_l, a_r_l_r
from (
Select c, a, b
from t3
where (e = b)
) T1(c_l, a_l, b_l)
left join (
Select c_l_l, a_r_l, c_r, d_r
from (
Select c_l, a_l, a_r, d_r
from (
Select c, a
from t4
where ((c - e) < b)
) T1(c_l, a_l)
full join (
Select a, d
from t4
where (75 < ((e - b) - e))
) T2(a_r, d_r)
on (a_l < a_r)
) T1(c_l_l, a_l_l, a_r_l, d_r_l)
left join (
Select c, b, d
from t4
where (71 = (e * a))
) T2(c_r, b_r, d_r)
on (d_r = c_l_l)
) T2(c_l_l_r, a_r_l_r, c_r_r, d_r_r)
on (31 < a_r_l_r)
) T2(c_l_r, a_r_l_r_r)
on (c_l_r = 8)
) T1(a_r_l_l, e_r_l_l, a_r_l_r_r_l, c_l_r_l)
left join (
Select e_l, a_r_r_r
from (
select e
from (
Select e, c
from t4
where (d = d)
) T1
union all
select a
from (
Select a
from t5
where (b < 4)
) T2
) T1(e_l)
inner join (
Select c_l, a_r_r, d_l_r
from (
Select c
from t2
where (47 = 55)
) T1(c_l)
inner join (
Select d_l, a_r
from (
Select c, a, d
from t3
where (a = (31 * (47 - 79)))
) T1(c_l, a_l, d_l)
inner join (
select a
from (
Select a
from t5
where (90 > a)
) T1
union all
select a_l
from (
Select a_l, e_r
from (
Select e, a
from t5
where (4 < 46)
) T1(e_l, a_l)
left join (
Select e, c
from t5
where (47 = 40)
) T2(e_r, c_r)
on (56 = 16)
) T2
) T2(a_r)
on (33 = 31)
) T2(d_l_r, a_r_r)
on ((69 - d_l_r) = 64)
) T2(c_l_r, a_r_r_r, d_l_r_r)
on (a_r_r_r = e_l)
) T2(e_l_r, a_r_r_r_r)
on ((63 * a_r_l_l) = a_r_r_r_r)
) T2(a_r_l_l_r, a_r_r_r_r_r, e_l_r_r)
on (93 > c_l_r_l_l)
) T2
) T1(b_l_l, c_r_l, b_r_l)
left join (
Select a, b
from t1
where (64 = b)
) T2(a_r, b_r)
on (b_r_l < b_r_l)
) T2(b_r_l_r, b_l_l_r, a_r_r)
on (b_l_l_r = a_r_r)
) T2
) T2(c_r)
on (c_r = c_l)
) T1
union all
select a, b
from (
Select a, b, d
from t5
where (75 < c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, d
from t3
where (c > 44)
) T1
union all
select c, a
from (
Select c, a
from t2
where ((b * b) > 14)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t4
where ((73 - c) = (a * (87 + 9)))
) T1
union all
select b, d
from (
Select b, d
from t4
where ((43 - a) = 27)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, d
from (
Select e, c, d
from t5
where (e = e)
) T1
union all
select e, c, a
from (
Select e, c, a
from t1
where (83 = (28 + 38))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t2
where (a < (d * b))
) T1
union all
select c
from (
Select c, a, b, d
from t1
where (b < 37)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_l, e_l_r_l, e_r
from (
Select a_l_l, e_l_r_l, e_r, a_r
from (
Select a_l, e_l_r
from (
Select a
from t4
where (0 > a)
) T1(a_l)
inner join (
Select e_l, c_l, b_l, e_r, d_r
from (
Select e, c, b
from t2
where (d = (a * 8))
) T1(e_l, c_l, b_l)
left join (
Select e, c, d
from t5
where (84 = ((14 * a) * 34))
) T2(e_r, c_r, d_r)
on (d_r < d_r)
) T2(e_l_r, c_l_r, b_l_r, e_r_r, d_r_r)
on (e_l_r < e_l_r)
) T1(a_l_l, e_l_r_l)
full join (
Select e, a
from t5
where (47 = e)
) T2(e_r, a_r)
on (20 = 16)
) T1
union all
select e, a, b
from (
Select e, a, b
from t5
where (a < 62)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_r_l_l
from (
Select a_r_l_l, e_r_r_l, c_r
from (
Select e_l_l, a_r_l, b_r_l_r, c_r_l_r, e_r_r
from (
Select e_l, d_l, a_r
from (
Select e, d
from t1
where (14 = a)
) T1(e_l, d_l)
left join (
Select e, a
from t4
where (a < (17 * a))
) T2(e_r, a_r)
on (22 = 75)
) T1(e_l_l, d_l_l, a_r_l)
full join (
Select b_r_l, c_r_l, e_r
from (
Select c_l, c_r, b_r
from (
select c
from (
Select c, a, b, d
from t3
where (b < (c * ((54 + d) + d)))
) T1
union all
select b
from (
Select b
from t4
where (d > e)
) T2
) T1(c_l)
left join (
Select c, b
from t5
where (d = 43)
) T2(c_r, b_r)
on (30 = ((b_r - 77) * (c_r - b_r)))
) T1(c_l_l, c_r_l, b_r_l)
left join (
Select e
from t2
where ((a + e) > a)
) T2(e_r)
on ((5 * (e_r - (41 - b_r_l))) = b_r_l)
) T2(b_r_l_r, c_r_l_r, e_r_r)
on ((e_r_r * 26) > e_r_r)
) T1(e_l_l_l, a_r_l_l, b_r_l_r_l, c_r_l_r_l, e_r_r_l)
left join (
Select e, c
from t1
where ((24 * a) = 73)
) T2(e_r, c_r)
on (10 = (e_r_r_l * (90 + 86)))
) T1
union all
select b
from (
Select b
from t3
where (28 = 62)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test12exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

