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
    
def test001(desc="""Joins Set 21"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t3
where (64 = a)
) T1
union all
select b, d
from (
Select b, d
from t5
where (((a * 28) + 22) = b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t1
where (d < 94)
) T1
union all
select e, c
from (
select e, c, a
from (
select e, c, a
from (
select e, c, a
from (
Select e, c, a
from t2
where ((25 - (a * 11)) = a)
) T1
union all
select c, b, d
from (
Select c, b, d
from t5
where (d > (6 * (91 - c)))
) T2
) T1
union all
select e, a, d
from (
Select e, a, d
from t1
where (d = c)
) T2
) T1
union all
select b_l, d_l, e_r
from (
Select b_l, d_l, e_r, b_r
from (
Select b, d
from t4
where (4 = ((7 + e) + (e - 71)))
) T1(b_l, d_l)
full join (
Select e, c, b
from t2
where (d < 43)
) T2(e_r, c_r, b_r)
on (e_r = 32)
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
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b, d
from t2
where ((c * d) > (19 + 35))
) T1
union all
select e, b
from (
Select e, b
from t2
where ((a + 44) < (c - d))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t1
where (a = 41)
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select b
from t1
where ((11 + 14) < 62)
) T1(b_l)
left join (
Select a
from t1
where ((b * (57 - (29 * 69))) = (d + 71))
) T2(a_r)
on (b_l > 2)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e
from t4
where (b < c)
) T1
union all
select b_l
from (
Select b_l, d_l, c_r
from (
Select c, b, d
from t1
where (((74 * d) - c) < (b - 20))
) T1(c_l, b_l, d_l)
left join (
Select c
from t1
where ((e - b) < c)
) T2(c_r)
on (13 < 85)
) T2
) T1
union all
select c
from (
Select c, d
from t1
where ((c * 58) < (87 - b))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, d
from (
Select a, d
from t2
where (d = 57)
) T1
union all
select e, c
from (
select e, c, a
from (
Select e, c, a, d
from t2
where (75 = 1)
) T1
union all
select b_r_l, d_l_l, d_r
from (
Select b_r_l, d_l_l, d_r
from (
select d_l, b_r
from (
Select d_l, b_r, d_r
from (
Select d
from t1
where ((58 + a) = a)
) T1(d_l)
left join (
select b, d
from (
Select b, d
from t2
where (e < e)
) T1
union all
select c_l, c_r
from (
Select c_l, c_r
from (
Select c
from t2
where (0 < (((d + 20) + b) - e))
) T1(c_l)
left join (
Select c
from t1
where (82 = 56)
) T2(c_r)
on (c_l = 43)
) T2
) T2(b_r, d_r)
on (d_l = (90 * b_r))
) T1
union all
select c, d
from (
Select c, d
from t3
where (a > ((31 + a) * 98))
) T2
) T1(d_l_l, b_r_l)
full join (
Select c, b, d
from t4
where (38 > b)
) T2(c_r, b_r, d_r)
on (80 = 34)
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
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b
from t5
where (26 > 45)
) T1
union all
select a, b
from (
Select a, b
from t4
where (a = 46)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t4
where (c = d)
) T1
union all
select d_r_l_l
from (
Select d_r_l_l, e_l_r
from (
select d_r_l
from (
select d_r_l, e_l_l_l
from (
Select d_r_l, e_l_l_l, a_r
from (
Select e_l_l, b_r_r_l, d_r
from (
Select e_l, b_l, a_l_r, b_r_r
from (
Select e, a, b, d
from t2
where (68 = 71)
) T1(e_l, a_l, b_l, d_l)
inner join (
Select a_l, b_r
from (
Select a
from t1
where (c = c)
) T1(a_l)
left join (
Select b
from t5
where (26 = a)
) T2(b_r)
on (b_r < b_r)
) T2(a_l_r, b_r_r)
on (34 > 58)
) T1(e_l_l, b_l_l, a_l_r_l, b_r_r_l)
left join (
Select d
from t4
where (8 > e)
) T2(d_r)
on (60 > 42)
) T1(e_l_l_l, b_r_r_l_l, d_r_l)
left join (
Select a
from t5
where (c < a)
) T2(a_r)
on (4 < 90)
) T1
union all
select d_l, b_r
from (
Select d_l, b_r
from (
Select a, d
from t3
where (99 < 57)
) T1(a_l, d_l)
left join (
Select b
from t5
where (b > e)
) T2(b_r)
on (d_l = b_r)
) T2
) T1
union all
select e
from (
Select e
from t3
where ((((40 * a) + a) * (b * 53)) = c)
) T2
) T1(d_r_l_l)
left join (
Select e_l, d_r
from (
Select e
from t2
where (53 < 21)
) T1(e_l)
full join (
Select c, d
from t1
where (13 = 40)
) T2(c_r, d_r)
on ((86 * (26 + e_l)) > 7)
) T2(e_l_r, d_r_r)
on (((57 - e_l_r) * 97) > ((d_r_l_l + (42 - e_l_r)) + d_r_l_l))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l, a_l_r
from (
Select a_l, a_l_r
from (
Select a
from t1
where (84 = b)
) T1(a_l)
inner join (
Select a_l, e_r
from (
Select c, a, b
from t1
where (c < 88)
) T1(c_l, a_l, b_l)
full join (
select e
from (
Select e
from t5
where (a = b)
) T1
union all
select a
from (
Select a
from t1
where (c < c)
) T2
) T2(e_r)
on ((4 - 36) < e_r)
) T2(a_l_r, e_r_r)
on (a_l < a_l_r)
) T1
union all
select b, d
from (
Select b, d
from t2
where (8 = (a + d))
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
select a_l, b_r
from (
Select a_l, b_r
from (
Select a
from t4
where (74 = b)
) T1(a_l)
left join (
Select e, a, b
from t2
where (e = 74)
) T2(e_r, a_r, b_r)
on (a_l < b_r)
) T1
union all
select c, a
from (
Select c, a, b
from t1
where ((52 + 6) < 2)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, c_l, e_r
from (
Select e, c, b
from t4
where (c < 42)
) T1(e_l, c_l, b_l)
full join (
Select e
from t1
where (((34 - c) - (84 + 51)) < 83)
) T2(e_r)
on (e_r = 5)
) T1
union all
select c
from (
Select c
from t3
where (18 > 57)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l
from (
Select e_l, c_l, a_l, b_r, d_r
from (
Select e, c, a
from t1
where (e < a)
) T1(e_l, c_l, a_l)
inner join (
select b, d
from (
Select b, d
from t5
where (76 < (69 * 99))
) T1
union all
select c, b
from (
select c, b, d
from (
Select c, b, d
from t2
where ((64 * 87) > 75)
) T1
union all
select e_l_r_l, e_l_r, c_r_r
from (
Select e_l_r_l, e_l_r, c_r_r
from (
Select d_r_l_l, e_l_r
from (
Select d_r_l, c_r
from (
Select e_l, c_r, d_r
from (
select e
from (
Select e, c, a
from t2
where (e < (((71 + a) - 80) + 79))
) T1
union all
select e
from (
Select e
from t1
where (51 > (a + 62))
) T2
) T1(e_l)
inner join (
Select c, d
from t1
where (e = 2)
) T2(c_r, d_r)
on ((d_r * 63) > 75)
) T1(e_l_l, c_r_l, d_r_l)
full join (
Select c
from t3
where ((b + d) = (d - 77))
) T2(c_r)
on (70 = d_r_l)
) T1(d_r_l_l, c_r_l)
left join (
Select e_l, c_l, e_r
from (
Select e, c, d
from t2
where (87 < (b + a))
) T1(e_l, c_l, d_l)
full join (
Select e
from t3
where (15 < (78 + (b - ((b - 50) * 23))))
) T2(e_r)
on (99 = 73)
) T2(e_l_r, c_l_r, e_r_r)
on (e_l_r < 69)
) T1(d_r_l_l_l, e_l_r_l)
full join (
Select e_l, c_r
from (
Select e
from t2
where (0 > 96)
) T1(e_l)
full join (
Select c
from t1
where (e = 36)
) T2(c_r)
on ((21 - c_r) = c_r)
) T2(e_l_r, c_r_r)
on ((e_l_r * c_r_r) < 66)
) T2
) T2
) T2(b_r, d_r)
on ((71 + 9) < 89)
) T1
union all
select e, b
from (
Select e, b
from t3
where (94 = d)
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
select e, d
from (
Select e, d
from t2
where (62 = (c + (18 * (a * 30))))
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, a_r, b_r
from (
select c, b
from (
Select c, b
from t1
where (c > (d + 56))
) T1
union all
select a_r_r_l, b_l_l
from (
Select a_r_r_l, b_l_l, d_r_r_r, d_l_r
from (
Select b_l, d_l, a_l_r, a_r_r
from (
Select c, b, d
from t4
where ((c + ((80 * d) * 97)) = 92)
) T1(c_l, b_l, d_l)
left join (
Select a_l, a_r, d_r
from (
Select a
from t5
where (c = (63 - (e - 9)))
) T1(a_l)
left join (
Select e, a, d
from t1
where (75 > d)
) T2(e_r, a_r, d_r)
on (86 = a_r)
) T2(a_l_r, a_r_r, d_r_r)
on ((a_r_r - 99) > 88)
) T1(b_l_l, d_l_l, a_l_r_l, a_r_r_l)
full join (
Select c_l, d_l, d_r_r
from (
Select c, a, d
from t1
where (e = d)
) T1(c_l, a_l, d_l)
left join (
Select e_l, b_l, e_r, d_r
from (
Select e, b
from t4
where (((46 - a) * 50) > 32)
) T1(e_l, b_l)
left join (
Select e, d
from t4
where (((96 - 43) * (32 - e)) < d)
) T2(e_r, d_r)
on (e_r = b_l)
) T2(e_l_r, b_l_r, e_r_r, d_r_r)
on (d_l < 34)
) T2(c_l_r, d_l_r, d_r_r_r)
on (a_r_r_l < b_l_l)
) T2
) T1(c_l, b_l)
inner join (
Select a, b
from t1
where (a < ((b * c) - d))
) T2(a_r, b_r)
on ((b_l + 20) = 19)
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
Select e, a
from t3
where (d = (98 * (b - (13 * c))))
) T1
union all
select d
from (
Select d
from t4
where (59 = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, d
from (
select e, d
from (
Select e, d
from t3
where (c = 99)
) T1
union all
select e, a
from (
Select e, a, d
from t5
where (78 < 21)
) T2
) T1
union all
select e, c
from (
Select e, c, a
from t1
where (((95 + (24 - 23)) * ((99 - 93) + b)) > 87)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t3
where ((99 - 29) = 36)
) T1
union all
select c
from (
Select c, a, d
from t3
where (77 > (63 - 73))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
select b, d
from (
Select b, d
from t5
where (a < 14)
) T1
union all
select a_l, b_r
from (
Select a_l, b_r
from (
Select e, a
from t2
where (((a * 29) - 41) = a)
) T1(e_l, a_l)
left join (
Select c, b
from t1
where (69 = d)
) T2(c_r, b_r)
on (b_r < 1)
) T2
) T1
union all
select c, d
from (
Select c, d
from t1
where (9 = (d * 76))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where ((c - a) = 44)
) T1
union all
select c
from (
Select c, a
from t2
where (87 = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
Select a_l, e_r_l_r
from (
Select a, b, d
from t4
where (99 < 42)
) T1(a_l, b_l, d_l)
left join (
Select e_l_l, e_r_l, c_r
from (
Select e_l, e_r
from (
Select e, b
from t5
where (21 < 0)
) T1(e_l, b_l)
left join (
Select e
from t3
where (98 = (98 + d))
) T2(e_r)
on ((e_r + 85) > (88 * 95))
) T1(e_l_l, e_r_l)
full join (
Select c
from t4
where (78 > 36)
) T2(c_r)
on (c_r < e_l_l)
) T2(e_l_l_r, e_r_l_r, c_r_r)
on (((29 + 30) * a_l) = a_l)
) T1
union all
select a
from (
Select a
from t1
where (c > (42 + c))
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
select e, c, b
from (
Select e, c, b
from t1
where (c = a)
) T1
union all
select c, a, d
from (
Select c, a, d
from t4
where (57 < a)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #******************************************
    _testmgr.testcase_end(desc)

