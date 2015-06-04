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
    
def test001(desc="""Joins Set 39"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
Select e, a, b
from p2
where (((a + 6) > 91) AND ((56 - b) > (d - 77)))
) T1(e_l, a_l, b_l)
left join (
Select c, a, d
from p4
where (58 = (b - 0))
) T2(c_r, a_r, d_r)
on ((35 + a_r) > 7)
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
Select a_l, d_l, c_r, b_r, d_r
from (
Select c, a, d
from p4
where ((32 = c) AND ((e = e) AND (((d - 62) * 53) > e)))
) T1(c_l, a_l, d_l)
left join (
Select c, b, d
from p1
where (85 > b)
) T2(c_r, b_r, d_r)
on (((d_l + (67 - (d_l - c_r))) = b_r) OR (d_r < (b_r - a_l)))
order by 1, 2, 3, 4, 5
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
Select c_l, a_l, c_r, a_r
from (
select c, a
from (
select c, a
from (
Select c, a, d
from p1
where (a = 65)
) T1
union all
select a_l, e_r
from (
Select a_l, e_r
from (
Select a
from p2
where (c = 0)
) T1(a_l)
left join (
Select e, a, b
from p3
where (b = b)
) T2(e_r, a_r, b_r)
on (63 = e_r)
) T2
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select c, a, b
from p5
where ((((((95 * 92) - c) - b) - 7) + d) = 88)
) T1(c_l, a_l, b_l)
left join (
Select a
from p5
where ((4 < 33) OR (((d - c) < b) OR ((e - b) = 46)))
) T2(a_r)
on (57 < 24)
) T2
) T1(c_l, a_l)
left join (
Select e, c, a
from p1
where (63 > a)
) T2(e_r, c_r, a_r)
on ((a_r > 67) AND (a_l > 77))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r
from (
Select e, a
from p1
where (e = 48)
) T1(e_l, a_l)
left join (
select b
from (
Select b
from p5
where (85 < 83)
) T1
union all
select a_l
from (
Select a_l, a_r_r, d_r_l_r
from (
Select a
from p3
where ((c - 83) = 95)
) T1(a_l)
left join (
Select d_r_l, a_r
from (
Select c_r_l, c_r, d_r
from (
Select e_l, b_l, c_r
from (
Select e, b, d
from p5
where (77 < 25)
) T1(e_l, b_l, d_l)
left join (
Select c
from p2
where (a > c)
) T2(c_r)
on ((c_r = c_r) OR ((b_l + c_r) > c_r))
) T1(e_l_l, b_l_l, c_r_l)
left join (
Select c, d
from p3
where ((49 = d) AND (e = e))
) T2(c_r, d_r)
on ((23 < d_r) OR ((c_r = c_r) OR ((d_r > c_r_l) OR ((c_r = c_r_l) AND (57 > (c_r + c_r))))))
) T1(c_r_l_l, c_r_l, d_r_l)
left join (
Select a
from p3
where ((b < 83) AND ((b < (13 * 22)) AND (48 = b)))
) T2(a_r)
on ((51 + a_r) = 17)
) T2(d_r_l_r, a_r_r)
on (64 > 41)
) T2
) T2(b_r)
on (87 = (a_l * (96 - b_r)))
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
Select e_l, d_l, a_r
from (
Select e, d
from p4
where (60 = 61)
) T1(e_l, d_l)
full join (
Select a
from p5
where ((99 > 77) AND (a < b))
) T2(a_r)
on ((e_l = ((a_r - 61) - 23)) AND ((d_l = (d_l + 4)) AND (d_l = 91)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, c_r, b_r
from (
Select d_l, c_r, b_r
from (
Select d
from p3
where (b > 4)
) T1(d_l)
left join (
Select c, b
from p3
where ((e = a) OR ((21 < 47) OR (79 < 87)))
) T2(c_r, b_r)
on (54 < c_r)
) T1(d_l_l, c_r_l, b_r_l)
left join (
Select c, b
from p4
where (b = d)
) T2(c_r, b_r)
on (b_r_l = b_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r, c_r
from (
Select b
from p2
where (58 = b)
) T1(b_l)
full join (
Select e, c
from p4
where ((22 = b) OR (14 > (71 + e)))
) T2(e_r, c_r)
on ((15 = 41) OR (c_r = c_r))
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
Select b_l, d_r_r, a_r_r
from (
Select e, b
from p2
where (a > 66)
) T1(e_l, b_l)
inner join (
Select a_l, a_r, d_r
from (
Select e, c, a, b
from p1
where ((78 = 91) OR (52 = 45))
) T1(e_l, c_l, a_l, b_l)
left join (
Select e, a, d
from p2
where (93 < 78)
) T2(e_r, a_r, d_r)
on ((d_r > a_l) OR (((((a_r * 39) + a_l) * (d_r + d_r)) = 47) OR (49 = 40)))
) T2(a_l_r, a_r_r, d_r_r)
on (a_r_r = 44)
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
Select a_l, e_r, c_r
from (
Select a
from p4
where (87 = 29)
) T1(a_l)
full join (
select e, c
from (
Select e, c
from p4
where (e < d)
) T1
union all
select c, d
from (
Select c, d
from p1
where (d > (a * b))
) T2
) T2(e_r, c_r)
on (38 = 59)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, a_r, d_r
from (
Select a, d
from p1
where (45 > d)
) T1(a_l, d_l)
inner join (
Select a, d
from p5
where ((97 = ((39 - (36 + (49 - b))) * (b - d))) AND ((95 < 95) OR (93 > e)))
) T2(a_r, d_r)
on ((d_r - a_r) > 11)
order by 1, 2, 3, 4
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
Select a_l, b_l, c_r, b_r
from (
Select a, b
from p4
where (c < 16)
) T1(a_l, b_l)
left join (
Select c, b
from p1
where (d = (b + 90))
) T2(c_r, b_r)
on (b_l > c_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, b_r, d_r
from (
Select e, d
from p1
where (d = 88)
) T1(e_l, d_l)
full join (
Select b, d
from p2
where ((e > (b - d)) OR (62 < e))
) T2(b_r, d_r)
on (70 > 67)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l, a_r, b_r
from (
Select c, d
from p2
where (30 = d)
) T1(c_l, d_l)
left join (
Select a, b
from p2
where ((a * c) < 76)
) T2(a_r, b_r)
on ((b_r > 24) AND ((c_l = 97) AND (((18 + 85) < (69 - a_r)) OR (53 = 87))))
order by 1, 2, 3, 4
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
Select c_l, a_l_r_r, b_l_r, d_l_r_r
from (
Select c, a
from p3
where (a < 16)
) T1(c_l, a_l)
left join (
Select b_l, a_l_r, d_l_r
from (
Select b
from p4
where (d > e)
) T1(b_l)
left join (
Select a_l, d_l, c_r_r
from (
Select a, d
from p1
where ((59 > 33) AND (a < 97))
) T1(a_l, d_l)
inner join (
Select e_l, e_r, c_r
from (
Select e
from p1
where (89 < a)
) T1(e_l)
inner join (
Select e, c
from p3
where (72 = (a - 38))
) T2(e_r, c_r)
on ((((e_r - (c_r + e_r)) * (13 + e_r)) = 26) AND (89 = e_r))
) T2(e_l_r, e_r_r, c_r_r)
on (19 < 65)
) T2(a_l_r, d_l_r, c_r_r_r)
on (d_l_r = 55)
) T2(b_l_r, a_l_r_r, d_l_r_r)
on ((27 * 96) > 20)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test39exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, d_r
from (
Select e
from p1
where ((b = 54) OR (c > a))
) T1(e_l)
inner join (
Select e, d
from p3
where (c > 54)
) T2(e_r, d_r)
on (71 = d_r)
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
Select e_l, c_l, e_l_r
from (
Select e, c, d
from p3
where (81 = 85)
) T1(e_l, c_l, d_l)
left join (
Select e_l, b_l, e_l_r
from (
Select e, a, b, d
from p5
where ((e = (9 * 10)) OR ((b > e) OR (((b + 36) - b) > (a - (7 - d)))))
) T1(e_l, a_l, b_l, d_l)
inner join (
select e_l
from (
Select e_l, a_r
from (
Select e
from p3
where (((c - c) > (94 - ((15 * ((63 - 68) * d)) + (e - 68)))) AND ((b = b) OR (75 > b)))
) T1(e_l)
full join (
Select a
from p5
where (67 = c)
) T2(a_r)
on ((24 < a_r) OR (19 = 59))
) T1
union all
select d
from (
Select d
from p5
where (((56 + 1) < e) AND ((57 * 16) = (67 + (51 - e))))
) T2
) T2(e_l_r)
on (e_l_r = b_l)
) T2(e_l_r, b_l_r, e_l_r_r)
on (e_l_r < (e_l_r * e_l_r))
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
Select a_r_l, e_r, a_r, d_r
from (
Select c_l_l, e_l_l, d_l_l, e_r, a_r, b_r
from (
Select e_l, c_l, d_l, a_l_r
from (
Select e, c, b, d
from p1
where (25 < c)
) T1(e_l, c_l, b_l, d_l)
full join (
Select a_l, b_l, b_r
from (
Select a, b
from p3
where (84 = ((a - 86) + 37))
) T1(a_l, b_l)
left join (
Select b
from p2
where ((d + (d * ((27 * (c + 53)) * e))) = 27)
) T2(b_r)
on (b_l = b_l)
) T2(a_l_r, b_l_r, b_r_r)
on ((d_l - ((a_l_r * d_l) + 31)) > 7)
) T1(e_l_l, c_l_l, d_l_l, a_l_r_l)
inner join (
Select e, a, b
from p3
where ((c + d) > (85 * 37))
) T2(e_r, a_r, b_r)
on (e_r < e_r)
) T1(c_l_l_l, e_l_l_l, d_l_l_l, e_r_l, a_r_l, b_r_l)
inner join (
Select e, a, d
from p2
where (76 = 84)
) T2(e_r, a_r, d_r)
on (a_r > 21)
order by 1, 2, 3, 4
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
Select c_r_l_r_l, a_r, d_r
from (
Select e_l, e_r_l_r_r, c_r_l_r
from (
Select e
from p3
where ((d > b) OR (31 = 7))
) T1(e_l)
inner join (
Select e_l_l, c_r_l, e_r_l_r, e_r_r
from (
Select e_l, c_r, d_r
from (
Select e
from p1
where (30 < (0 - a))
) T1(e_l)
inner join (
Select c, d
from p2
where (c = a)
) T2(c_r, d_r)
on (e_l = c_r)
) T1(e_l_l, c_r_l, d_r_l)
left join (
Select c_r_l_l_l, e_r_l, e_r, b_r
from (
Select c_r_l_l, e_r
from (
select c_r_l
from (
Select c_r_l, a_r_l_l, b_r_r, e_l_r
from (
Select a_r_l, c_r
from (
Select c_l, c_r, a_r
from (
Select c, d
from p4
where (53 < (b + b))
) T1(c_l, d_l)
left join (
Select c, a
from p1
where ((80 * 46) = b)
) T2(c_r, a_r)
on (a_r > 75)
) T1(c_l_l, c_r_l, a_r_l)
left join (
Select c, d
from p3
where (74 = 16)
) T2(c_r, d_r)
on ((a_r_l > a_r_l) AND (c_r < c_r))
) T1(a_r_l_l, c_r_l)
inner join (
Select e_l, b_r
from (
Select e
from p4
where ((b + e) = b)
) T1(e_l)
left join (
Select e, b
from p4
where (a < 70)
) T2(e_r, b_r)
on ((e_l = e_l) AND ((64 + e_l) < b_r))
) T2(e_l_r, b_r_r)
on (e_l_r > 30)
) T1
union all
select e_l
from (
select e_l
from (
Select e_l, b_l, a_l_r, d_r_r
from (
Select e, c, b
from p3
where ((d = (75 + e)) AND (62 > c))
) T1(e_l, c_l, b_l)
left join (
Select a_l, c_r, d_r
from (
select a
from (
Select a
from p1
where (((c + ((13 + 33) + c)) + 29) = (54 * c))
) T1
union all
select e
from (
Select e, c, a, d
from p1
where (e > c)
) T2
) T1(a_l)
left join (
Select c, d
from p4
where ((e - 89) > 37)
) T2(c_r, d_r)
on ((70 = ((d_r - 44) * (74 * d_r))) AND (a_l < c_r))
) T2(a_l_r, c_r_r, d_r_r)
on ((b_l < e_l) AND (a_l_r = d_r_r))
) T1
union all
select b_l_r_l
from (
select b_l_r_l
from (
select b_l_r_l
from (
select b_l_r_l
from (
Select b_l_r_l, c_l_l, a_r, d_r
from (
Select c_l, d_l, b_l_r
from (
Select c, b, d
from p5
where (((a * d) > ((d + 22) * 66)) AND (b = a))
) T1(c_l, b_l, d_l)
inner join (
Select a_l, b_l, b_r
from (
Select c, a, b, d
from p3
where (c = 6)
) T1(c_l, a_l, b_l, d_l)
inner join (
select b, d
from (
Select b, d
from p3
where ((c = 45) AND ((71 = b) AND (e > 23)))
) T1
union all
select c, b
from (
Select c, b
from p5
where ((15 < 42) AND (b = (e * (((0 * 37) * a) + 25))))
) T2
) T2(b_r, d_r)
on (b_r > 49)
) T2(a_l_r, b_l_r, b_r_r)
on (c_l < 45)
) T1(c_l_l, d_l_l, b_l_r_l)
left join (
Select e, c, a, d
from p1
where ((55 + e) = (34 + d))
) T2(e_r, c_r, a_r, d_r)
on (94 < a_r)
) T1
union all
select d
from (
Select d
from p1
where ((30 = d) AND ((59 + c) = 31))
) T2
) T1
union all
select a_l
from (
Select a_l, a_r, d_r
from (
Select e, a, b
from p3
where ((b * 82) > 47)
) T1(e_l, a_l, b_l)
full join (
Select c, a, d
from p5
where (a > (((1 + e) - 81) * b))
) T2(c_r, a_r, d_r)
on ((79 = 49) AND (((60 - a_l) = 86) OR ((a_l > (19 - ((86 * d_r) - 4))) AND ((38 < a_l) AND ((d_r - 29) = d_r)))))
) T2
) T1
union all
select e_l
from (
Select e_l, c_l, b_r
from (
Select e, c, a
from p1
where ((c > e) AND ((e = (55 + e)) AND (((26 + 7) - b) > 4)))
) T1(e_l, c_l, a_l)
inner join (
Select b
from p3
where (((89 * 76) = a) OR (d = 21))
) T2(b_r)
on (c_l < b_r)
) T2
) T2
) T2
) T1(c_r_l_l)
left join (
Select e, c, d
from p2
where ((d < 26) AND ((e < 64) OR (((((86 * e) * c) * 88) + 71) < d)))
) T2(e_r, c_r, d_r)
on ((c_r_l_l = e_r) AND ((e_r < c_r_l_l) AND ((43 < ((e_r * 73) - (25 + c_r_l_l))) AND (60 = e_r))))
) T1(c_r_l_l_l, e_r_l)
full join (
Select e, b
from p5
where (((62 * (c * 63)) - 2) > e)
) T2(e_r, b_r)
on (((0 + (c_r_l_l_l * c_r_l_l_l)) > e_r) OR (76 = b_r))
) T2(c_r_l_l_l_r, e_r_l_r, e_r_r, b_r_r)
on ((4 * c_r_l) < e_r_r)
) T2(e_l_l_r, c_r_l_r, e_r_l_r_r, e_r_r_r)
on ((85 > c_r_l_r) AND ((c_r_l_r > 35) OR (63 = 21)))
) T1(e_l_l, e_r_l_r_r_l, c_r_l_r_l)
inner join (
Select a, b, d
from p4
where ((a * d) < e)
) T2(a_r, b_r, d_r)
on (a_r > 29)
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
Select c_l, a_r
from (
Select c
from p2
where ((d * 88) = 84)
) T1(c_l)
left join (
Select a
from p4
where (16 < 19)
) T2(a_r)
on (76 > 19)
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
Select e_l, c_l_r
from (
Select e
from p4
where (b < (c - d))
) T1(e_l)
left join (
Select c_l, d_r
from (
Select c, d
from p3
where (c = a)
) T1(c_l, d_l)
full join (
Select d
from p4
where ((29 > (35 - 60)) OR ((c - e) = 30))
) T2(d_r)
on ((22 < c_l) OR (33 = 15))
) T2(c_l_r, d_r_r)
on (55 = e_l)
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
    #****************
    _testmgr.testcase_end(desc)

