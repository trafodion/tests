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
    
def test001(desc="""Joins Set 18"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e_l, b_l, b_l_r
from (
Select e_l, b_l, b_l_r
from (
Select e, b, d
from t2
where (b < 55)
) T1(e_l, b_l, d_l)
left join (
select e_l, b_l
from (
Select e_l, b_l, e_l_r_r_r_r_r, c_l_r_r, e_l_r_r_r, c_r_l_r
from (
Select e, b, d
from t3
where ((a + e) > 12)
) T1(e_l, b_l, d_l)
left join (
Select c_r_l, c_l_r, e_l_r_r_r_r, e_l_r_r
from (
Select a_l, b_l, c_r
from (
select a, b
from (
Select a, b
from t3
where (66 > 0)
) T1
union all
select c, a
from (
Select c, a
from t3
where ((96 - d) < 25)
) T2
) T1(a_l, b_l)
left join (
Select c
from t5
where (91 > 20)
) T2(c_r)
on (a_l = 44)
) T1(a_l_l, b_l_l, c_r_l)
inner join (
Select c_l, e_l_r, e_l_r_r_r
from (
Select e, c, a
from t1
where ((93 + 74) = 65)
) T1(e_l, c_l, a_l)
left join (
Select e_l, e_l_r_r
from (
Select e
from t4
where ((c - 66) = 69)
) T1(e_l)
left join (
Select d_l_l, e_r_l, e_l_r, a_r_r
from (
Select d_l, e_r, a_r, b_r
from (
Select d
from t1
where (b = d)
) T1(d_l)
left join (
Select e, a, b
from t2
where (34 = e)
) T2(e_r, a_r, b_r)
on (1 > d_l)
) T1(d_l_l, e_r_l, a_r_l, b_r_l)
full join (
Select e_l, a_r
from (
Select e
from t4
where (c = 38)
) T1(e_l)
inner join (
Select c, a
from t3
where (77 = 98)
) T2(c_r, a_r)
on (47 > a_r)
) T2(e_l_r, a_r_r)
on ((4 + 62) = 43)
) T2(d_l_l_r, e_r_l_r, e_l_r_r, a_r_r_r)
on (e_l < 32)
) T2(e_l_r, e_l_r_r_r)
on (e_l_r_r_r < (c_l * 76))
) T2(c_l_r, e_l_r_r, e_l_r_r_r_r)
on (7 > c_l_r)
) T2(c_r_l_r, c_l_r_r, e_l_r_r_r_r_r, e_l_r_r_r)
on (((12 * 71) * 7) = e_l)
) T1
union all
select e, c
from (
Select e, c
from t2
where (c > (79 + 31))
) T2
) T2(e_l_r, b_l_r)
on (89 < b_l)
) T1
union all
select e, a, d
from (
Select e, a, d
from t4
where (93 < 7)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_r_l_l, b_r, d_r
from (
Select b_r_l_l, b_r, d_r
from (
Select b_r_l, e_r
from (
Select e_l, a_l, b_r
from (
select e, a
from (
Select e, a, d
from t5
where (c < a)
) T1
union all
select a, b
from (
Select a, b
from t3
where (b = 73)
) T2
) T1(e_l, a_l)
inner join (
Select b, d
from t5
where (66 = e)
) T2(b_r, d_r)
on (e_l < a_l)
) T1(e_l_l, a_l_l, b_r_l)
full join (
Select e, c, a
from t1
where ((d - 54) = 74)
) T2(e_r, c_r, a_r)
on (b_r_l < 49)
) T1(b_r_l_l, e_r_l)
left join (
Select a, b, d
from t2
where (1 > 8)
) T2(a_r, b_r, d_r)
on ((2 - 1) < (b_r + 71))
) T1
union all
select c_l, b_l, a_r
from (
Select c_l, b_l, a_r
from (
Select c, a, b
from t1
where (21 < 88)
) T1(c_l, a_l, b_l)
full join (
Select a
from t1
where (d = 5)
) T2(a_r)
on ((42 - 83) = 99)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, e_r
from (
Select d_l, e_r, c_r
from (
Select d
from t5
where (((20 * 13) * 58) > d)
) T1(d_l)
left join (
Select e, c
from t4
where (d > 92)
) T2(e_r, c_r)
on ((60 - 25) < 63)
) T1
union all
select d_r_l, e_r
from (
select d_r_l, e_r
from (
Select d_r_l, e_r
from (
Select c_l, a_r, d_r
from (
select c
from (
Select c
from t4
where (a = 7)
) T1
union all
select b
from (
Select b
from t1
where ((((3 - (e + e)) - b) * e) = b)
) T2
) T1(c_l)
full join (
Select a, d
from t4
where (c = b)
) T2(a_r, d_r)
on (d_r = ((a_r - 20) * c_l))
) T1(c_l_l, a_r_l, d_r_l)
full join (
select e, c
from (
Select e, c, a
from t5
where (c = (c + (21 + (28 * (82 * 86)))))
) T1
union all
select c, a
from (
select c, a
from (
Select c, a
from t2
where ((e - b) > 86)
) T1
union all
select c, a
from (
Select c, a
from t5
where (97 = e)
) T2
) T2
) T2(e_r, c_r)
on ((e_r * (d_r_l + (33 + 36))) = (91 - 0))
) T1
union all
select e_l, c_l_r
from (
select e_l, c_l_r
from (
Select e_l, c_l_r, b_r_r_r
from (
select e
from (
select e
from (
Select e
from t3
where (a = (55 + a))
) T1
union all
select b
from (
Select b
from t5
where (a > c)
) T2
) T1
union all
select c_l_l
from (
Select c_l_l, e_l_l, d_l_r
from (
select e_l, c_l
from (
Select e_l, c_l, a_r
from (
Select e, c
from t3
where (a = 35)
) T1(e_l, c_l)
left join (
select a
from (
Select a
from t4
where (89 > 21)
) T1
union all
select a
from (
Select a, d
from t4
where ((c - 13) < c)
) T2
) T2(a_r)
on (((a_r * a_r) * (e_l + c_l)) < 88)
) T1
union all
select e_l, c_l_l_r_r_r_r
from (
Select e_l, c_l_l_r_r_r_r
from (
Select e, a, d
from t3
where (0 = d)
) T1(e_l, a_l, d_l)
full join (
Select d_l, c_l_l_r_r_r
from (
Select d
from t5
where (c = 71)
) T1(d_l)
left join (
Select c_l, e_l_r, c_l_l_r_r
from (
Select c, d
from t3
where (b > (55 * 74))
) T1(c_l, d_l)
inner join (
select e_l, c_l_l_r
from (
select e_l, c_l_l_r, e_l_r_r_r, e_r_l_r
from (
Select e_l, c_l_l_r, e_l_r_r_r, e_r_l_r
from (
Select e, b
from t3
where (40 > 23)
) T1(e_l, b_l)
left join (
Select c_l_l, e_r_l, a_l_r, e_l_r_r
from (
Select c_l, e_r, b_r, d_r
from (
Select c, a
from t3
where (d = 86)
) T1(c_l, a_l)
left join (
Select e, a, b, d
from t4
where (d > a)
) T2(e_r, a_r, b_r, d_r)
on (44 = (89 - b_r))
) T1(c_l_l, e_r_l, b_r_l, d_r_l)
inner join (
Select a_l, b_l, e_l_r, a_r_r
from (
Select a, b
from t5
where (d < d)
) T1(a_l, b_l)
full join (
Select e_l, a_r
from (
Select e
from t4
where (e = 9)
) T1(e_l)
left join (
select a
from (
Select a, d
from t5
where (a < a)
) T1
union all
select b
from (
Select b
from t1
where ((d + 16) < 31)
) T2
) T2(a_r)
on (((a_r - e_l) + 70) = a_r)
) T2(e_l_r, a_r_r)
on (23 > a_l)
) T2(a_l_r, b_l_r, e_l_r_r, a_r_r_r)
on (1 = (49 + (e_l_r_r - e_l_r_r)))
) T2(c_l_l_r, e_r_l_r, a_l_r_r, e_l_r_r_r)
on (((e_r_l_r + 36) + c_l_l_r) < (e_l * 29))
) T1
union all
select e, c, a, b
from (
Select e, c, a, b
from t4
where (60 = d)
) T2
) T1
union all
select e, b
from (
select e, b
from (
Select e, b
from t3
where (a < a)
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, c_l_r_r, e_r_r_r_r_r, b_r_l_r_r_l_r
from (
Select c, a
from t3
where (d > a)
) T1(c_l, a_l)
full join (
Select b_l_r_l, b_r_l_r_r_l, c_l_l, c_l_r, e_r_r_r_r
from (
Select e_l, c_l, b_r_l_r_r, b_l_r
from (
Select e, c
from t3
where (e = 35)
) T1(e_l, c_l)
left join (
select b_l, b_r_l_r
from (
Select b_l, b_r_l_r, a_l_l_r
from (
Select b
from t2
where (3 < e)
) T1(b_l)
left join (
Select a_l_l, b_r_l, c_r
from (
Select a_l, b_r
from (
Select a, d
from t3
where ((76 * 19) = (88 * b))
) T1(a_l, d_l)
left join (
Select b
from t3
where (e > 2)
) T2(b_r)
on ((((30 * a_l) + a_l) + (68 * 58)) < 41)
) T1(a_l_l, b_r_l)
full join (
Select c
from t1
where (a > c)
) T2(c_r)
on (91 = b_r_l)
) T2(a_l_l_r, b_r_l_r, c_r_r)
on (a_l_l_r = b_l)
) T1
union all
select e, c
from (
Select e, c
from t3
where ((52 - 71) < b)
) T2
) T2(b_l_r, b_r_l_r_r)
on (16 = b_l_r)
) T1(e_l_l, c_l_l, b_r_l_r_r_l, b_l_r_l)
left join (
Select c_l, e_r_r_r
from (
Select c
from t5
where (27 = c)
) T1(c_l)
inner join (
Select e_l, e_l_r, e_r_r
from (
Select e
from t3
where ((71 * a) = d)
) T1(e_l)
left join (
Select e_l, e_r, a_r
from (
Select e
from t4
where ((d * 61) = 72)
) T1(e_l)
left join (
select e, a
from (
select e, a
from (
Select e, a, d
from t4
where ((66 * 39) < 49)
) T1
union all
select e, a
from (
Select e, a
from t5
where ((79 - 40) > (52 - 41))
) T2
) T1
union all
select e, c
from (
Select e, c, d
from t1
where (a > 79)
) T2
) T2(e_r, a_r)
on (e_r > (a_r + 52))
) T2(e_l_r, e_r_r, a_r_r)
on (e_r_r > 68)
) T2(e_l_r, e_l_r_r, e_r_r_r)
on (e_r_r_r < (e_r_r_r + 19))
) T2(c_l_r, e_r_r_r_r)
on (b_r_l_r_r_l < 49)
) T2(b_l_r_l_r, b_r_l_r_r_l_r, c_l_l_r, c_l_r_r, e_r_r_r_r_r)
on (72 < c_l)
) T2
) T2
) T2(e_l_r, c_l_l_r_r)
on (29 = 60)
) T2(c_l_r, e_l_r_r, c_l_l_r_r_r)
on (16 = c_l_l_r_r_r)
) T2(d_l_r, c_l_l_r_r_r_r)
on (e_l < e_l)
) T2
) T1(e_l_l, c_l_l)
inner join (
Select d_l, d_l_r, e_r_r
from (
Select d
from t5
where (48 < 35)
) T1(d_l)
left join (
Select d_l, e_r, a_r
from (
Select d
from t5
where (b = 70)
) T1(d_l)
left join (
Select e, a
from t4
where (b < a)
) T2(e_r, a_r)
on (56 = a_r)
) T2(d_l_r, e_r_r, a_r_r)
on (d_l_r = (d_l_r + (d_l_r - 75)))
) T2(d_l_r, d_l_r_r, e_r_r_r)
on (31 > 87)
) T2
) T1(e_l)
full join (
Select c_l, b_r_r
from (
Select c
from t1
where (47 = 22)
) T1(c_l)
full join (
Select e_l, c_l, d_l, b_r
from (
Select e, c, d
from t1
where (27 = 12)
) T1(e_l, c_l, d_l)
full join (
Select b
from t5
where (e < ((97 - a) * c))
) T2(b_r)
on (c_l < ((b_r - (c_l * e_l)) * (86 + 72)))
) T2(e_l_r, c_l_r, d_l_r, b_r_r)
on (8 > c_l)
) T2(c_l_r, b_r_r_r)
on ((52 * b_r_r_r) > (31 + c_l_r))
) T1
union all
select b, d
from (
Select b, d
from t2
where (88 < e)
) T2
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_r_l, c_r_l, a_r
from (
Select a_r_l, c_r_l, a_r, b_r, d_r
from (
Select a_l, c_r, a_r
from (
Select e, a
from t1
where (57 > 97)
) T1(e_l, a_l)
full join (
Select c, a
from t4
where (d = (37 - 5))
) T2(c_r, a_r)
on (c_r = 98)
) T1(a_l_l, c_r_l, a_r_l)
inner join (
select a, b, d
from (
Select a, b, d
from t1
where (e > 87)
) T1
union all
select e_l, d_l, a_r
from (
Select e_l, d_l, a_r
from (
select e, c, d
from (
Select e, c, d
from t4
where (5 = e)
) T1
union all
select e, c, a
from (
Select e, c, a, d
from t5
where ((c - 76) < c)
) T2
) T1(e_l, c_l, d_l)
left join (
Select c, a
from t2
where (64 = a)
) T2(c_r, a_r)
on (a_r = a_r)
) T2
) T2(a_r, b_r, d_r)
on ((66 * (b_r + 40)) > 22)
) T1
union all
select e, c, a
from (
select e, c, a
from (
Select e, c, a
from t2
where (85 = 89)
) T1
union all
select e, c, d
from (
select e, c, d
from (
Select e, c, d
from t4
where (2 = c)
) T1
union all
select e, c, b
from (
Select e, c, b
from t4
where (38 > 14)
) T2
) T2
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, b, d
from t1
where (a = a)
) T1
union all
select c_l, d_r
from (
Select c_l, d_r
from (
Select e, c, d
from t1
where (d > 26)
) T1(e_l, c_l, d_l)
full join (
Select b, d
from t2
where ((7 - (e + a)) = (57 + d))
) T2(b_r, d_r)
on ((12 * 31) = 0)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t2
where (91 < d)
) T1
union all
select e, c
from (
Select e, c, a, d
from t2
where (77 > (1 * 58))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
select a_l
from (
Select a_l, d_r
from (
Select a
from t2
where (64 < d)
) T1(a_l)
left join (
Select d
from t1
where (((c - c) * (6 * a)) = a)
) T2(d_r)
on (a_l = 81)
) T1
union all
select c
from (
Select c
from t3
where ((98 * 92) > b)
) T2
) T1
union all
select d
from (
select d
from (
Select d
from t5
where (e = d)
) T1
union all
select e
from (
select e
from (
select e, c
from (
Select e, c, b, d
from t4
where (d > (10 - (c - a)))
) T1
union all
select e, a
from (
Select e, a
from t3
where (64 > a)
) T2
) T1
union all
select e
from (
Select e
from t2
where (d = (54 * b))
) T2
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
Select e, d
from t4
where (1 = e)
) T1
union all
select b_l_l, e_r_l
from (
Select b_l_l, e_r_l, b_r
from (
Select b_l, e_r
from (
Select e, b
from t2
where (56 = a)
) T1(e_l, b_l)
inner join (
Select e
from t5
where (d = e)
) T2(e_r)
on (86 < 36)
) T1(b_l_l, e_r_l)
left join (
Select a, b
from t2
where (b = (18 - b))
) T2(a_r, b_r)
on (b_l_l < 5)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_r_l, c_r_l_l, a_r, d_r
from (
Select b_r_l, c_r_l_l, a_r, d_r
from (
Select c_l_l, c_r_l, b_r, d_r
from (
select c_l, c_r
from (
Select c_l, c_r
from (
Select c, d
from t4
where ((68 * a) = c)
) T1(c_l, d_l)
full join (
Select c
from t2
where (98 = d)
) T2(c_r)
on (c_l = c_r)
) T1
union all
select c, b
from (
Select c, b, d
from t1
where (((57 - 94) + 89) < 60)
) T2
) T1(c_l_l, c_r_l)
left join (
Select b, d
from t1
where (13 < b)
) T2(b_r, d_r)
on (b_r = (57 + (35 * 8)))
) T1(c_l_l_l, c_r_l_l, b_r_l, d_r_l)
left join (
Select a, b, d
from t5
where (c > a)
) T2(a_r, b_r, d_r)
on (47 = 46)
) T1
union all
select e, c, b, d
from (
Select e, c, b, d
from t4
where (a = a)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (62 > d)
) T1
union all
select c
from (
Select c, a
from t2
where ((69 - (94 - 16)) = (22 + 43))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, b, d
from t4
where (a > (c - d))
) T1
union all
select c, d
from (
Select c, d
from t3
where (d < c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l_l, b_r_l
from (
Select a_l_l, b_r_l, a_r
from (
Select e_l, a_l, b_r
from (
Select e, a
from t4
where (46 = d)
) T1(e_l, a_l)
full join (
select b
from (
Select b
from t1
where (d = (14 - d))
) T1
union all
select e_l
from (
select e_l
from (
Select e_l, a_l, c_r_r, b_l_r
from (
select e, c, a
from (
Select e, c, a
from t2
where (97 = 35)
) T1
union all
select a, b, d
from (
Select a, b, d
from t1
where (e > 10)
) T2
) T1(e_l, c_l, a_l)
left join (
select b_l, c_r, a_r
from (
Select b_l, c_r, a_r
from (
Select e, b
from t3
where ((71 - d) = (b - 87))
) T1(e_l, b_l)
inner join (
Select c, a
from t3
where (93 > 84)
) T2(c_r, a_r)
on ((c_r * 12) > 96)
) T1
union all
select c_l, c_r, d_r
from (
Select c_l, c_r, d_r
from (
Select c
from t5
where (55 < (b - 87))
) T1(c_l)
inner join (
Select c, d
from t1
where (e = c)
) T2(c_r, d_r)
on (d_r = 71)
) T2
) T2(b_l_r, c_r_r, a_r_r)
on (11 = b_l_r)
) T1
union all
select c
from (
Select c
from t3
where (a < a)
) T2
) T2
) T2(b_r)
on (a_l = 11)
) T1(e_l_l, a_l_l, b_r_l)
full join (
Select a, b
from t4
where (6 = b)
) T2(a_r, b_r)
on ((b_r_l * 72) > b_r_l)
) T1
union all
select a_l, a_r
from (
Select a_l, a_r
from (
Select a
from t4
where (3 < (a - b))
) T1(a_l)
inner join (
select a
from (
Select a
from t2
where (95 = 65)
) T1
union all
select c_l
from (
Select c_l, e_r, a_r, b_r
from (
Select c
from t5
where (c > a)
) T1(c_l)
inner join (
Select e, a, b
from t3
where (26 = 40)
) T2(e_r, a_r, b_r)
on (74 = a_r)
) T2
) T2(a_r)
on (15 < (a_r * 5))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
select e_l
from (
Select e_l, c_l, c_l_l_r, a_r_r, b_r_l_r
from (
select e, c
from (
Select e, c, b
from t2
where (13 > b)
) T1
union all
select e_l, b_r
from (
Select e_l, b_r
from (
Select e
from t3
where (b < d)
) T1(e_l)
inner join (
Select a, b, d
from t5
where (29 = 26)
) T2(a_r, b_r, d_r)
on (34 = e_l)
) T2
) T1(e_l, c_l)
left join (
Select b_r_l, c_l_l, e_r, a_r
from (
Select c_l, d_l, e_r, b_r
from (
Select c, a, d
from t4
where (50 = 57)
) T1(c_l, a_l, d_l)
left join (
Select e, b
from t1
where (e > a)
) T2(e_r, b_r)
on (c_l = b_r)
) T1(c_l_l, d_l_l, e_r_l, b_r_l)
inner join (
Select e, c, a, b
from t3
where (24 = c)
) T2(e_r, c_r, a_r, b_r)
on (32 > 51)
) T2(b_r_l_r, c_l_l_r, e_r_r, a_r_r)
on (e_l > 15)
) T1
union all
select e
from (
select e
from (
Select e
from t2
where (e > (a + a))
) T1
union all
select b
from (
Select b
from t1
where (80 < 75)
) T2
) T2
) T1
union all
select b
from (
Select b, d
from t4
where (9 < c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a, b
from t3
where (d = 95)
) T1
union all
select c, b
from (
Select c, b
from t1
where (90 = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b
from t1
where (62 > (b * d))
) T1
union all
select b
from (
Select b
from t1
where (b < 10)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t1
where ((b + b) = e)
) T1
union all
select e
from (
Select e, b
from t2
where (b = 95)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, e_r
from (
Select b_l, e_r
from (
Select b
from t1
where (((((0 * (e + (84 + c))) - 86) + 12) - c) < b)
) T1(b_l)
left join (
Select e
from t1
where (51 = a)
) T2(e_r)
on ((24 + (b_l * ((((e_r + (28 + 45)) + e_r) * (40 + 50)) - 43))) < e_r)
) T1
union all
select e, c
from (
Select e, c, a, d
from t4
where (b > (c - e))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
select a
from (
Select a, d
from t1
where (e = 17)
) T1
union all
select e
from (
select e
from (
Select e, c, b, d
from t3
where (44 = ((b * 15) + (16 + c)))
) T1
union all
select c
from (
Select c
from t4
where (e = 7)
) T2
) T2
) T1
union all
select c
from (
select c
from (
Select c, a
from t1
where (25 < c)
) T1
union all
select b
from (
Select b
from t5
where ((e - c) = 14)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t1
where (15 = 18)
) T1
union all
select e, c
from (
Select e, c, a, b
from t5
where ((c - 53) > 20)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t2
where (b < c)
) T1
union all
select c_l
from (
Select c_l, e_r
from (
Select e, c, a
from t3
where (72 = b)
) T1(e_l, c_l, a_l)
full join (
Select e, c, a, d
from t2
where (b = a)
) T2(e_r, c_r, a_r, d_r)
on (e_r > 47)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f'  s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test18exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

