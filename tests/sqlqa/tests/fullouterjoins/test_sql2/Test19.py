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
    
def test001(desc="""Joins Set 19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select e_l, c_l
from (
Select e_l, c_l, c_r_r, b_l_r
from (
Select e, c
from t1
where (35 > (c + 52))
) T1(e_l, c_l)
left join (
select b_l, c_r
from (
select b_l, c_r
from (
Select b_l, c_r, b_r, d_r
from (
Select b
from t1
where (2 = 48)
) T1(b_l)
left join (
Select c, b, d
from t3
where (c = (86 * 49))
) T2(c_r, b_r, d_r)
on (49 = 57)
) T1
union all
select e_l, b_r
from (
Select e_l, b_r
from (
select e
from (
Select e, d
from t1
where (12 = c)
) T1
union all
select b
from (
select b
from (
Select b, d
from t4
where (b = a)
) T1
union all
select e
from (
Select e
from t2
where (a > a)
) T2
) T2
) T1(e_l)
left join (
Select a, b
from t2
where ((c - c) < 46)
) T2(a_r, b_r)
on ((28 + (38 - 58)) = 90)
) T2
) T1
union all
select c_l, b_r_r_l_r
from (
Select c_l, b_r_r_l_r
from (
Select e, c, b
from t2
where (e > (53 - c))
) T1(e_l, c_l, b_l)
inner join (
Select a_r_r_l, b_r_r_l, d_l_l, a_r
from (
Select d_l, b_r_r, a_r_r
from (
select c, d
from (
Select c, d
from t5
where (b = c)
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, d_r
from (
Select e, a
from t2
where (23 < c)
) T1(e_l, a_l)
left join (
Select b, d
from t3
where (e > 44)
) T2(b_r, d_r)
on (a_l = 79)
) T2
) T1(c_l, d_l)
left join (
Select c_l, a_r, b_r
from (
Select c
from t2
where (56 = (1 + a))
) T1(c_l)
full join (
Select a, b
from t3
where ((c + e) < 73)
) T2(a_r, b_r)
on (c_l > ((61 * 1) - b_r))
) T2(c_l_r, a_r_r, b_r_r)
on (48 < 77)
) T1(d_l_l, b_r_r_l, a_r_r_l)
inner join (
select a
from (
Select a, b
from t1
where (b = (23 - e))
) T1
union all
select e
from (
Select e
from t1
where (((45 - (53 * (c * c))) + c) = a)
) T2
) T2(a_r)
on (73 > 48)
) T2(a_r_r_l_r, b_r_r_l_r, d_l_l_r, a_r_r)
on (c_l > c_l)
) T2
) T2(b_l_r, c_r_r)
on (42 = b_l_r)
) T1
union all
select e, d
from (
Select e, d
from t4
where (88 = 16)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
select c, d
from (
Select c, d
from t4
where (25 < 7)
) T1
union all
select b_l, d_l
from (
Select b_l, d_l, b_r
from (
Select a, b, d
from t4
where (c = 80)
) T1(a_l, b_l, d_l)
left join (
Select b
from t4
where ((29 + d) = d)
) T2(b_r)
on ((24 * (37 - d_l)) < (49 - 14))
) T2
) T1
union all
select e, b
from (
Select e, b, d
from t1
where (b > 88)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
select c
from (
Select c
from t3
where (90 = c)
) T1
union all
select a
from (
Select a, b, d
from t4
where (68 = (90 - (b * (29 + b))))
) T2
) T1
union all
select d_l
from (
Select d_l, d_r_r
from (
select b, d
from (
Select b, d
from t1
where (c > (89 + 34))
) T1
union all
select c_l, a_r
from (
Select c_l, a_r, b_r
from (
Select c, d
from t5
where (40 = d)
) T1(c_l, d_l)
left join (
Select a, b
from t5
where (74 > 9)
) T2(a_r, b_r)
on (39 = 81)
) T2
) T1(b_l, d_l)
left join (
Select a_l_l, a_r_l, a_r, b_r, d_r
from (
Select a_l, a_r
from (
Select a, d
from t5
where (42 > 99)
) T1(a_l, d_l)
left join (
Select a
from t4
where (b > e)
) T2(a_r)
on (a_l > 71)
) T1(a_l_l, a_r_l)
left join (
Select c, a, b, d
from t5
where (50 = e)
) T2(c_r, a_r, b_r, d_r)
on (37 > 42)
) T2(a_l_l_r, a_r_l_r, a_r_r, b_r_r, d_r_r)
on (d_r_r = d_l)
) T2
) T1
union all
select e
from (
select e, b
from (
Select e, b
from t5
where (40 = 40)
) T1
union all
select c, b
from (
Select c, b
from t4
where (24 < e)
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
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t3
where (a < c)
) T1
union all
select d_r_l, a_r_l
from (
Select d_r_l, a_r_l, e_r
from (
Select c_l, a_l, a_r, d_r
from (
Select c, a
from t5
where ((49 + 32) = (4 + 1))
) T1(c_l, a_l)
full join (
Select c, a, d
from t4
where (59 = c)
) T2(c_r, a_r, d_r)
on (c_l = d_r)
) T1(c_l_l, a_l_l, a_r_l, d_r_l)
inner join (
Select e
from t1
where (86 > 99)
) T2(e_r)
on (90 = (4 + 83))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_l, d_l_l_r
from (
Select e_l, b_l, d_l_l_r, a_r_r_r
from (
Select e, b, d
from t1
where (52 > 5)
) T1(e_l, b_l, d_l)
left join (
Select b_l_l, d_l_l, a_r_r
from (
Select b_l, d_l, e_r_r
from (
Select b, d
from t1
where (d = (a * (60 * (a + 31))))
) T1(b_l, d_l)
inner join (
Select e_l, e_r
from (
Select e
from t5
where (b > 70)
) T1(e_l)
inner join (
Select e
from t2
where (26 > a)
) T2(e_r)
on (31 < 94)
) T2(e_l_r, e_r_r)
on (b_l = d_l)
) T1(b_l_l, d_l_l, e_r_r_l)
left join (
Select c_l_l, c_r_r_l, a_r, b_r
from (
Select c_l, b_r_r, c_r_r
from (
select e, c
from (
Select e, c
from t4
where ((49 - a) = b)
) T1
union all
select e, d
from (
Select e, d
from t3
where ((61 - 10) < (90 - d))
) T2
) T1(e_l, c_l)
left join (
Select e_l, c_r, b_r
from (
Select e
from t2
where (d < e)
) T1(e_l)
left join (
Select c, a, b, d
from t1
where (a = b)
) T2(c_r, a_r, b_r, d_r)
on (b_r = 92)
) T2(e_l_r, c_r_r, b_r_r)
on (98 < c_l)
) T1(c_l_l, b_r_r_l, c_r_r_l)
left join (
Select c, a, b
from t2
where (((61 * 88) - a) = (e + (b + (c * 72))))
) T2(c_r, a_r, b_r)
on ((b_r - (a_r - 33)) = 70)
) T2(c_l_l_r, c_r_r_l_r, a_r_r, b_r_r)
on (d_l_l > (d_l_l - (b_l_l + a_r_r)))
) T2(b_l_l_r, d_l_l_r, a_r_r_r)
on (73 > 58)
) T1
union all
select e, b, d
from (
Select e, b, d
from t5
where ((d - a) > d)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    ##expectfile $test_dir/Test19exp a1s5
    #execute s1;
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t2
where (e > 0)
) T1
union all
select e
from (
Select e, c, a
from t3
where (24 > 30)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t1
where ((b * b) = 40)
) T1
union all
select c_l_l, c_r
from (
Select c_l_l, c_r, d_r
from (
Select c_l, a_l, e_l_r
from (
Select c, a
from t2
where (b = ((e + d) * d))
) T1(c_l, a_l)
left join (
select e_l
from (
Select e_l, c_l, c_r
from (
Select e, c, a
from t5
where (a = (c + c))
) T1(e_l, c_l, a_l)
left join (
Select c
from t3
where ((((94 - 71) * c) + e) = e)
) T2(c_r)
on (c_r = (63 + (43 + (c_r - 4))))
) T1
union all
select e
from (
select e
from (
Select e
from t5
where ((65 - (87 * d)) > c)
) T1
union all
select c
from (
Select c, d
from t4
where (72 = 12)
) T2
) T2
) T2(e_l_r)
on (e_l_r < e_l_r)
) T1(c_l_l, a_l_l, e_l_r_l)
inner join (
Select c, d
from t2
where ((54 * (33 * 97)) > 11)
) T2(c_r, d_r)
on (c_r = c_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, a_r_r
from (
Select e_l, a_r_r
from (
select e
from (
Select e
from t3
where (d = 53)
) T1
union all
select e_l
from (
Select e_l, b_l, e_r, d_r
from (
Select e, b
from t2
where (70 = 2)
) T1(e_l, b_l)
inner join (
Select e, d
from t1
where ((31 * 62) < 92)
) T2(e_r, d_r)
on (e_r > e_l)
) T2
) T1(e_l)
left join (
Select c_l, d_l, a_r
from (
Select e, c, d
from t5
where (c < (84 - 9))
) T1(e_l, c_l, d_l)
inner join (
Select a
from t5
where (62 < e)
) T2(a_r)
on (73 = ((d_l - a_r) + 81))
) T2(c_l_r, d_l_r, a_r_r)
on (14 < a_r_r)
) T1
union all
select b, d
from (
Select b, d
from t1
where (b = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a
from t2
where (3 = a)
) T1
union all
select c
from (
Select c
from t3
where (78 > 7)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t2
where (d > 65)
) T1
union all
select a, b
from (
Select a, b, d
from t3
where ((d - 56) = 5)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, b_l
from (
Select a_l, b_l, e_r, c_r, b_r
from (
Select c, a, b
from t5
where (65 = 49)
) T1(c_l, a_l, b_l)
full join (
Select e, c, b
from t5
where (a < 17)
) T2(e_r, c_r, b_r)
on (c_r = 23)
) T1
union all
select e, b
from (
Select e, b
from t4
where (b > 8)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b
from t1
where (72 = b)
) T1
union all
select e, c, a
from (
Select e, c, a, d
from t2
where (c < b)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l_l_l, c_l_r_r_r_r_l, b_r
from (
Select c_l_l_l, c_l_r_r_r_r_l, b_r
from (
Select c_l_l, c_r_l_r_r, c_l_r_r_r_r
from (
Select c_l, a_l_r
from (
Select e, c, a, b
from t1
where (17 = (11 - 96))
) T1(e_l, c_l, a_l, b_l)
full join (
select c_l, a_l
from (
Select c_l, a_l, b_r
from (
Select c, a
from t5
where (e < 25)
) T1(c_l, a_l)
inner join (
Select b
from t4
where (a = b)
) T2(b_r)
on ((50 + ((22 - ((92 - c_l) - (((a_l + a_l) + a_l) - 65))) + (67 * a_l))) = 62)
) T1
union all
select c, a
from (
Select c, a
from t4
where (50 > a)
) T2
) T2(c_l_r, a_l_r)
on (71 < c_l)
) T1(c_l_l, a_l_r_l)
inner join (
Select a_l, c_r_l_r, c_l_r_r_r, e_l_l_r
from (
Select e, c, a
from t2
where (27 < 98)
) T1(e_l, c_l, a_l)
full join (
Select e_l_l, c_r_l, c_l_r_r, a_r_r_r
from (
Select e_l, c_r
from (
Select e
from t2
where ((b - 98) = b)
) T1(e_l)
inner join (
Select c, d
from t4
where (d = 49)
) T2(c_r, d_r)
on (84 = 74)
) T1(e_l_l, c_r_l)
inner join (
Select a_l_l, c_l_r, a_r_r
from (
select a_l
from (
Select a_l, d_r_r_r, d_l_r
from (
Select a, b, d
from t1
where (40 < 92)
) T1(a_l, b_l, d_l)
left join (
Select d_l, a_l_r, d_r_r
from (
Select d
from t3
where (b = 22)
) T1(d_l)
full join (
Select a_l, d_r
from (
Select a
from t2
where ((23 - 31) > 78)
) T1(a_l)
full join (
Select d
from t2
where (2 > 60)
) T2(d_r)
on (75 = 53)
) T2(a_l_r, d_r_r)
on (d_l = a_l_r)
) T2(d_l_r, a_l_r_r, d_r_r_r)
on (51 < ((d_l_r * a_l) - 81))
) T1
union all
select a
from (
Select a
from t5
where (a < 28)
) T2
) T1(a_l_l)
inner join (
Select c_l, a_r
from (
select c
from (
Select c, a, b
from t1
where (a = d)
) T1
union all
select a
from (
Select a
from t5
where (c = d)
) T2
) T1(c_l)
inner join (
select a
from (
Select a
from t5
where (b = (48 * d))
) T1
union all
select e_l
from (
Select e_l, b_r_r
from (
Select e
from t1
where (a < e)
) T1(e_l)
full join (
Select a_l, d_l, a_r, b_r
from (
Select e, c, a, d
from t2
where (d > b)
) T1(e_l, c_l, a_l, d_l)
left join (
Select c, a, b
from t5
where (e < (10 * d))
) T2(c_r, a_r, b_r)
on (7 > 94)
) T2(a_l_r, d_l_r, a_r_r, b_r_r)
on (b_r_r > (b_r_r - 10))
) T2
) T2(a_r)
on (c_l < a_r)
) T2(c_l_r, a_r_r)
on (a_l_l = a_r_r)
) T2(a_l_l_r, c_l_r_r, a_r_r_r)
on (68 = 9)
) T2(e_l_l_r, c_r_l_r, c_l_r_r_r, a_r_r_r_r)
on (e_l_l_r = 37)
) T2(a_l_r, c_r_l_r_r, c_l_r_r_r_r, e_l_l_r_r)
on (27 < c_r_l_r_r)
) T1(c_l_l_l, c_r_l_r_r_l, c_l_r_r_r_r_l)
full join (
Select a, b, d
from t2
where (95 < e)
) T2(a_r, b_r, d_r)
on (c_l_r_r_r_r_l = c_l_l_l)
) T1
union all
select b_l, e_r, c_r
from (
Select b_l, e_r, c_r
from (
Select c, b
from t5
where (63 = (43 * 19))
) T1(c_l, b_l)
left join (
Select e, c, d
from t5
where (b = 95)
) T2(e_r, c_r, d_r)
on (e_r < e_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t4
where (54 = 30)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a, d
from t1
where ((84 - (a - b)) = 10)
) T1
union all
select b, d
from (
Select b, d
from t3
where (73 = 79)
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
select a, b
from (
Select a, b, d
from t2
where (b < c)
) T1
union all
select d_l, b_r
from (
Select d_l, b_r
from (
Select c, a, d
from t1
where ((16 - 3) = a)
) T1(c_l, a_l, d_l)
inner join (
select b
from (
Select b
from t2
where (d = d)
) T1
union all
select c_r_l
from (
select c_r_l, d_l_l
from (
Select c_r_l, d_l_l, e_l_r_r_r, e_l_l_r
from (
Select d_l, c_r
from (
select d
from (
Select d
from t5
where (d > e)
) T1
union all
select e_l
from (
Select e_l, b_l, d_l, a_r, d_r
from (
Select e, b, d
from t5
where (4 < b)
) T1(e_l, b_l, d_l)
inner join (
Select a, d
from t2
where (8 = 30)
) T2(a_r, d_r)
on (b_l = d_l)
) T2
) T1(d_l)
left join (
Select c, a
from t2
where (68 > e)
) T2(c_r, a_r)
on (c_r = d_l)
) T1(d_l_l, c_r_l)
left join (
Select e_l_l, e_l_r_r
from (
Select e_l, b_l_r_r, a_r_l_r, e_r_r_r
from (
Select e, c
from t1
where (33 > c)
) T1(e_l, c_l)
full join (
Select a_r_l, e_r_r, b_l_r
from (
Select a_l_l, d_r_l, d_l_l, e_r, c_r, a_r
from (
Select a_l, d_l, d_r
from (
Select e, a, d
from t2
where (98 = e)
) T1(e_l, a_l, d_l)
left join (
Select d
from t4
where (d = 79)
) T2(d_r)
on (99 = d_r)
) T1(a_l_l, d_l_l, d_r_l)
inner join (
Select e, c, a, b
from t4
where (39 = 16)
) T2(e_r, c_r, a_r, b_r)
on ((d_l_l + a_l_l) = c_r)
) T1(a_l_l_l, d_r_l_l, d_l_l_l, e_r_l, c_r_l, a_r_l)
full join (
Select b_l, e_r
from (
select b
from (
Select b
from t2
where (c = b)
) T1
union all
select a_l
from (
Select a_l, b_l, d_l_l_r, a_r_r
from (
Select a, b
from t3
where (c = 91)
) T1(a_l, b_l)
left join (
Select e_l_l, c_r_l, d_l_l, a_r
from (
Select e_l, a_l, d_l, c_r
from (
Select e, a, d
from t5
where ((86 - (58 - (a * (70 + e)))) > 4)
) T1(e_l, a_l, d_l)
left join (
Select c, a, b, d
from t1
where (45 = 4)
) T2(c_r, a_r, b_r, d_r)
on (e_l > a_l)
) T1(e_l_l, a_l_l, d_l_l, c_r_l)
full join (
Select c, a
from t5
where (1 = (e * ((a * 19) + d)))
) T2(c_r, a_r)
on (e_l_l = (53 - 71))
) T2(e_l_l_r, c_r_l_r, d_l_l_r, a_r_r)
on (51 < a_r_r)
) T2
) T1(b_l)
inner join (
Select e
from t3
where ((c - 47) < c)
) T2(e_r)
on (72 = b_l)
) T2(b_l_r, e_r_r)
on (a_r_l = (e_r_r + ((84 * (30 - (a_r_l + (((((e_r_r * e_r_r) - a_r_l) * a_r_l) + a_r_l) + 3)))) + e_r_r)))
) T2(a_r_l_r, e_r_r_r, b_l_r_r)
on (40 < a_r_l_r)
) T1(e_l_l, b_l_r_r_l, a_r_l_r_l, e_r_r_r_l)
left join (
Select c_l, e_l_r, d_r_r
from (
Select c
from t5
where (92 = a)
) T1(c_l)
left join (
Select e_l, d_l, d_r
from (
Select e, d
from t1
where (((97 + c) - (a + e)) = b)
) T1(e_l, d_l)
full join (
Select c, d
from t4
where ((35 - e) < (49 + b))
) T2(c_r, d_r)
on ((e_l * d_r) < d_r)
) T2(e_l_r, d_l_r, d_r_r)
on (c_l = e_l_r)
) T2(c_l_r, e_l_r_r, d_r_r_r)
on (e_l_l > 46)
) T2(e_l_l_r, e_l_r_r_r)
on (48 < 15)
) T1
union all
select c, a
from (
Select c, a
from t4
where (4 < (b * 67))
) T2
) T2
) T2(b_r)
on ((b_r + d_l) = 42)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, a, b
from t5
where (a = 2)
) T1
union all
select c, a
from (
Select c, a
from t3
where ((((b * d) + a) + 88) > b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_l_r_r
from (
Select e_l, b_l_r_r, b_l_r
from (
Select e, c
from t2
where (52 = (d * 63))
) T1(e_l, c_l)
left join (
Select b_l, a_l_r_r, b_l_r
from (
Select c, b
from t3
where (66 < ((((a - (b - b)) * d) * 92) * (b - d)))
) T1(c_l, b_l)
full join (
Select a_l, b_l, a_l_r
from (
Select a, b
from t1
where (41 = (16 * a))
) T1(a_l, b_l)
full join (
Select a_l, e_r_r, b_l_r
from (
select a
from (
Select a
from t1
where (75 = 71)
) T1
union all
select b
from (
Select b, d
from t4
where (47 = 23)
) T2
) T1(a_l)
left join (
Select b_l, e_r
from (
select a, b
from (
Select a, b
from t5
where ((a - (c + ((18 * d) - 6))) = 34)
) T1
union all
select c, a
from (
Select c, a, b
from t5
where (17 = d)
) T2
) T1(a_l, b_l)
full join (
Select e
from t3
where (a = 64)
) T2(e_r)
on (73 = e_r)
) T2(b_l_r, e_r_r)
on (73 = e_r_r)
) T2(a_l_r, e_r_r_r, b_l_r_r)
on (9 = (((61 - 18) * a_l) * a_l))
) T2(a_l_r, b_l_r, a_l_r_r)
on (b_l_r = a_l_r_r)
) T2(b_l_r, a_l_r_r_r, b_l_r_r)
on ((9 + 74) < 21)
) T1
union all
select c, a
from (
Select c, a
from t5
where (45 < 64)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t3
where ((a * (((99 * 77) * a) * (e - d))) = c)
) T1
union all
select b_l, e_r
from (
Select b_l, e_r, d_r
from (
Select e, b
from t5
where (90 = (16 - b))
) T1(e_l, b_l)
full join (
Select e, a, d
from t3
where (((77 - 18) + 80) = 96)
) T2(e_r, a_r, d_r)
on ((95 * b_l) = e_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_r_r, e_r_l_r
from (
Select e_l, b_r_r, e_r_l_r, e_l_l_r
from (
Select e
from t4
where (c = d)
) T1(e_l)
inner join (
Select e_l_l, e_r_l, b_r
from (
select e_l, b_l, e_r, d_r
from (
Select e_l, b_l, e_r, d_r
from (
Select e, b
from t2
where (e = 14)
) T1(e_l, b_l)
left join (
Select e, a, b, d
from t5
where (c < 47)
) T2(e_r, a_r, b_r, d_r)
on (e_l < 50)
) T1
union all
select b_l_r_r_l, c_l_l, d_r_r_r_l, e_r
from (
Select b_l_r_r_l, c_l_l, d_r_r_r_l, e_r, a_r
from (
Select e_l, c_l, b_l_r_r, d_r_r_r, b_l_r
from (
Select e, c
from t1
where (49 = b)
) T1(e_l, c_l)
full join (
Select b_l, d_r_r, b_l_r
from (
Select e, c, b
from t4
where (67 = (b + (47 - c)))
) T1(e_l, c_l, b_l)
left join (
Select b_l, d_r
from (
Select c, a, b
from t5
where ((e * d) = c)
) T1(c_l, a_l, b_l)
inner join (
Select d
from t4
where (d > ((a + 99) + 7))
) T2(d_r)
on (34 > (((89 + 34) - 65) + b_l))
) T2(b_l_r, d_r_r)
on (d_r_r > b_l)
) T2(b_l_r, d_r_r_r, b_l_r_r)
on (10 = c_l)
) T1(e_l_l, c_l_l, b_l_r_r_l, d_r_r_r_l, b_l_r_l)
full join (
select e, a, d
from (
Select e, a, d
from t4
where (d > e)
) T1
union all
select e, a, b
from (
Select e, a, b, d
from t1
where (70 = 0)
) T2
) T2(e_r, a_r, d_r)
on (91 = (83 - d_r_r_r_l))
) T2
) T1(e_l_l, b_l_l, e_r_l, d_r_l)
left join (
Select c, b
from t5
where (d > e)
) T2(c_r, b_r)
on (e_r_l < e_r_l)
) T2(e_l_l_r, e_r_l_r, b_r_r)
on (e_l > e_r_l_r)
) T1
union all
select d_l, c_r, d_r
from (
Select d_l, c_r, d_r
from (
Select d
from t4
where (9 = (33 - (a - a)))
) T1(d_l)
left join (
Select c, d
from t2
where (b = 47)
) T2(c_r, d_r)
on (c_r = c_r)
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
select e, c
from (
Select e, c, a
from t4
where (((b + (99 - (45 * 68))) + b) > (a * 67))
) T1
union all
select a_l, b_l
from (
select a_l, b_l
from (
Select a_l, b_l, a_r
from (
Select e, a, b
from t2
where (73 = a)
) T1(e_l, a_l, b_l)
full join (
Select a
from t1
where (59 > b)
) T2(a_r)
on (75 < 1)
) T1
union all
select b, d
from (
Select b, d
from t3
where (e < 41)
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
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

