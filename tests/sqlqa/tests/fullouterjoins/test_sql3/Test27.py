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
    
def test001(desc="""Joins Set 27"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select c_l_l
from (
Select c_l_l, d_r_l, c_r
from (
Select c_l, c_r, d_r
from (
Select e, c
from t3
where (d = (e - c))
) T1(e_l, c_l)
left join (
Select c, d
from t4
where (83 = b)
) T2(c_r, d_r)
on (d_r < 12)
) T1(c_l_l, c_r_l, d_r_l)
full join (
select c
from (
Select c
from t5
where (b > 12)
) T1
union all
select a
from (
Select a, b, d
from t3
where (a > 73)
) T2
) T2(c_r)
on (76 = (78 - c_r))
) T1
union all
select c
from (
Select c
from t2
where (80 = b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, d
from (
Select e, a, d
from t4
where (e < 52)
) T1
union all
select c_l, b_r_r, c_r_r
from (
Select c_l, b_r_r, c_r_r
from (
Select c
from t2
where (52 = b)
) T1(c_l)
inner join (
Select e_l, c_r, b_r
from (
select e
from (
Select e
from t5
where (11 = 5)
) T1
union all
select c
from (
Select c, b
from t3
where (((61 + (86 + (d * 32))) * (b - e)) > 96)
) T2
) T1(e_l)
full join (
Select c, a, b
from t4
where (((e * 88) + 0) = 51)
) T2(c_r, a_r, b_r)
on (61 < 91)
) T2(e_l_r, c_r_r, b_r_r)
on (9 = b_r_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (73 = (d + d))
) T1
union all
select e
from (
Select e, b
from t1
where ((e - 34) < e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, d
from t4
where (36 < (e - e))
) T1
union all
select d_l_l
from (
select d_l_l
from (
Select d_l_l, c_r, d_r
from (
Select d_l, a_r
from (
Select d
from t4
where ((47 + 59) > a)
) T1(d_l)
full join (
Select a, b, d
from t2
where (95 = d)
) T2(a_r, b_r, d_r)
on ((a_r + (d_l + d_l)) = d_l)
) T1(d_l_l, a_r_l)
inner join (
Select c, d
from t5
where (77 > d)
) T2(c_r, d_r)
on (c_r = 7)
) T1
union all
select c
from (
Select c
from t5
where (b = 40)
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
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, b, d
from t5
where (38 = (b * d))
) T1
union all
select a
from (
Select a
from t2
where ((c * a) = 45)
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
select a_l, d_l, a_r_r
from (
Select a_l, d_l, a_r_r, b_l_r
from (
Select a, d
from t3
where (12 < c)
) T1(a_l, d_l)
inner join (
Select b_l, a_r
from (
select b
from (
Select b
from t3
where (15 = 11)
) T1
union all
select e
from (
Select e, b
from t3
where ((9 - c) > 69)
) T2
) T1(b_l)
inner join (
Select e, a, d
from t3
where (d > 65)
) T2(e_r, a_r, d_r)
on (41 = 61)
) T2(b_l_r, a_r_r)
on (b_l_r = 46)
) T1
union all
select e, c, b
from (
Select e, c, b
from t3
where ((a * b) > (a * b))
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
select a_l_l
from (
select a_l_l, c_r
from (
Select a_l_l, c_r
from (
Select e_l, a_l, d_r_l_r
from (
Select e, c, a
from t5
where (d < 69)
) T1(e_l, c_l, a_l)
left join (
select d_r_l, a_r
from (
Select d_r_l, a_r
from (
Select a_l, c_r, d_r
from (
Select a
from t4
where (c = c)
) T1(a_l)
full join (
Select e, c, a, d
from t1
where (e < 85)
) T2(e_r, c_r, a_r, d_r)
on (d_r > (11 + a_l))
) T1(a_l_l, c_r_l, d_r_l)
inner join (
Select a, b
from t4
where ((d * c) = c)
) T2(a_r, b_r)
on ((88 + (a_r - 24)) > 14)
) T1
union all
select e, c
from (
Select e, c
from t3
where (23 < (10 + d))
) T2
) T2(d_r_l_r, a_r_r)
on (44 > e_l)
) T1(e_l_l, a_l_l, d_r_l_r_l)
left join (
Select c, d
from t4
where (a < (d + 91))
) T2(c_r, d_r)
on (21 = 95)
) T1
union all
select e, a
from (
Select e, a, d
from t4
where ((52 * c) = 59)
) T2
) T1
union all
select a
from (
Select a
from t2
where (b = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l_l
from (
Select b_l_l, a_r_r, d_l_r
from (
Select b_l, c_r
from (
Select b
from t2
where (e = 4)
) T1(b_l)
left join (
select c, a
from (
Select c, a
from t2
where (d = d)
) T1
union all
select e, a
from (
Select e, a
from t1
where (b < (98 - 24))
) T2
) T2(c_r, a_r)
on (58 = (28 + 60))
) T1(b_l_l, c_r_l)
full join (
Select d_l, a_r
from (
Select d
from t2
where (44 = (74 + 93))
) T1(d_l)
left join (
Select a, d
from t2
where (21 = c)
) T2(a_r, d_r)
on (67 < ((d_l * 15) + (d_l * a_r)))
) T2(d_l_r, a_r_r)
on ((b_l_l + 22) > a_r_r)
) T1
union all
select c
from (
Select c
from t2
where (93 > 21)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l
from (
Select c_l, b_l, e_l_r, a_r_r
from (
Select c, b
from t3
where (36 > e)
) T1(c_l, b_l)
left join (
Select e_l, a_r
from (
Select e, d
from t4
where (68 < 87)
) T1(e_l, d_l)
full join (
Select c, a, b
from t2
where (25 > d)
) T2(c_r, a_r, b_r)
on (65 = 80)
) T2(e_l_r, a_r_r)
on (c_l < c_l)
) T1
union all
select a
from (
Select a
from t2
where (a > d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, b
from t1
where ((b - (e - b)) = e)
) T1
union all
select e
from (
Select e
from t2
where (41 = (b * (0 - a)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, d
from t4
where (d > c)
) T1
union all
select d
from (
Select d
from t2
where (72 < 77)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_r_r
from (
select e_l, c_r_r
from (
Select e_l, c_r_r, d_l_r
from (
Select e
from t4
where ((((c + (c + (a * 40))) - b) * 73) = d)
) T1(e_l)
inner join (
select d_l, c_r
from (
Select d_l, c_r
from (
Select e, d
from t5
where (50 = (c - e))
) T1(e_l, d_l)
inner join (
Select c
from t5
where ((57 * e) > (((76 + 50) * (b - 81)) + 17))
) T2(c_r)
on (d_l = 76)
) T1
union all
select e_l, d_l
from (
Select e_l, d_l, c_r
from (
select e, d
from (
Select e, d
from t5
where (74 < d)
) T1
union all
select e, a
from (
Select e, a, b, d
from t2
where ((b * b) = c)
) T2
) T1(e_l, d_l)
left join (
Select c
from t2
where (49 = 15)
) T2(c_r)
on (24 < 75)
) T2
) T2(d_l_r, c_r_r)
on (91 = 86)
) T1
union all
select c, a
from (
Select c, a
from t2
where (46 > c)
) T2
) T1
union all
select e_l, a_l
from (
Select e_l, a_l, a_r
from (
Select e, a, d
from t3
where (76 > ((d - 87) + 12))
) T1(e_l, a_l, d_l)
inner join (
Select a
from t4
where (b = 37)
) T2(a_r)
on ((0 * 27) = e_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, d
from (
Select e, c, d
from t2
where (80 = c)
) T1
union all
select a, b, d
from (
Select a, b, d
from t5
where (17 = 71)
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
select e, a, b
from (
Select e, a, b, d
from t1
where (65 > c)
) T1
union all
select c_l, a_l, b_r
from (
Select c_l, a_l, b_r
from (
select c, a
from (
Select c, a, b
from t2
where (((66 + 56) - c) = 43)
) T1
union all
select a, d
from (
Select a, d
from t1
where ((39 - 5) = 69)
) T2
) T1(c_l, a_l)
inner join (
Select b
from t2
where (43 > (85 - (d * e)))
) T2(b_r)
on (a_l = b_r)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b, d
from t1
where (24 = 37)
) T1
union all
select a
from (
Select a
from t5
where (68 < b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t1
where (a > b)
) T1
union all
select e, c
from (
Select e, c, b
from t5
where (a > ((20 + 72) + c))
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
select e_l, a_l, d_l, d_r
from (
Select e_l, a_l, d_l, d_r
from (
Select e, c, a, d
from t4
where (53 = 1)
) T1(e_l, c_l, a_l, d_l)
inner join (
Select e, c, d
from t5
where (30 < e)
) T2(e_r, c_r, d_r)
on (15 = ((49 - (90 - d_r)) - d_l))
) T1
union all
select e, a, b, d
from (
Select e, a, b, d
from t3
where (51 > e)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e, a, d
from (
Select e, a, d
from t2
where (d > (a + ((b * c) + (73 - b))))
) T1
union all
select e, a, b
from (
Select e, a, b
from t3
where (5 = (83 * (d + (84 - 47))))
) T2
) T1
union all
select e
from (
select e
from (
Select e
from t5
where (14 = d)
) T1
union all
select c
from (
Select c, b, d
from t1
where (73 = c)
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
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, a_r_l, e_l_r
from (
Select e_l_l, a_r_l, e_l_r
from (
Select e_l, a_r
from (
Select e
from t1
where (5 < 5)
) T1(e_l)
full join (
Select a
from t1
where (66 > (11 * (45 - (a * a))))
) T2(a_r)
on (14 = e_l)
) T1(e_l_l, a_r_l)
left join (
Select e_l, e_r
from (
Select e, a
from t4
where (14 > a)
) T1(e_l, a_l)
left join (
Select e, c, b, d
from t2
where (c = (67 * ((95 + 62) * 56)))
) T2(e_r, c_r, b_r, d_r)
on ((e_r + e_r) = 93)
) T2(e_l_r, e_r_r)
on (25 > 7)
) T1
union all
select c, a, b
from (
Select c, a, b
from t4
where (a > (78 * 11))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l_r_r
from (
Select e_l, c_l_r_r, a_l_r_r, e_l_r, a_r_r_r
from (
select e, b
from (
Select e, b
from t2
where (70 < 31)
) T1
union all
select e, a
from (
Select e, a
from t1
where (a = d)
) T2
) T1(e_l, b_l)
inner join (
Select e_l, a_l_r, c_l_r, a_r_r
from (
Select e, d
from t5
where (3 > (5 - 24))
) T1(e_l, d_l)
left join (
Select c_l, a_l, e_r, a_r
from (
Select c, a
from t5
where (26 < 15)
) T1(c_l, a_l)
full join (
Select e, a, b
from t5
where (b < 43)
) T2(e_r, a_r, b_r)
on (87 > 9)
) T2(c_l_r, a_l_r, e_r_r, a_r_r)
on (93 = a_l_r)
) T2(e_l_r, a_l_r_r, c_l_r_r, a_r_r_r)
on ((34 + 28) = (a_r_r_r * (((2 + a_l_r_r) - (c_l_r_r + 60)) * 62)))
) T1
union all
select c, d
from (
Select c, d
from t5
where (86 = a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

