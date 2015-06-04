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
    
def test001(desc="""Joins Set 15"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, a_r, b_r
from (
Select d
from p2
where (40 = (((31 - 42) + 18) * (62 * a)))
) T1(d_l)
left join (
Select a, b
from p4
where (48 = b)
) T2(a_r, b_r)
on ((23 + a_r) < b_r)
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
Select e_l, a_l, d_r
from (
Select e, a
from p4
where ((d = (a - (a + b))) OR (c < d))
) T1(e_l, a_l)
left join (
Select d
from p3
where (88 < (e + c))
) T2(d_r)
on (84 = 99)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, d_r_r, c_l_l_l_r
from (
Select e, c, a
from p1
where (79 = a)
) T1(e_l, c_l, a_l)
left join (
Select c_l_l_l, d_r
from (
Select a_l_l, c_l_l, b_r
from (
Select c_l, a_l, e_r_r, d_l_r
from (
Select c, a
from p2
where ((((68 + e) - 5) > ((b * (68 * 55)) + (54 + c))) OR ((49 = ((11 + 95) * 87)) AND ((72 > 71) AND ((20 = e) AND ((e > (99 - b)) OR (45 = 52))))))
) T1(c_l, a_l)
inner join (
Select d_l, e_r, a_r
from (
select d
from (
Select d
from p2
where ((a = 21) OR ((36 + 34) < 77))
) T1
union all
select e
from (
Select e, b
from p4
where ((e > b) AND (35 = 12))
) T2
) T1(d_l)
inner join (
Select e, a
from p1
where (((e - ((27 + 34) - 62)) > d) AND (b > a))
) T2(e_r, a_r)
on (63 > 66)
) T2(d_l_r, e_r_r, a_r_r)
on (e_r_r = 44)
) T1(c_l_l, a_l_l, e_r_r_l, d_l_r_l)
inner join (
Select a, b
from p5
where (b = 49)
) T2(a_r, b_r)
on ((36 - (c_l_l * a_l_l)) = 60)
) T1(a_l_l_l, c_l_l_l, b_r_l)
left join (
Select d
from p1
where (46 < 71)
) T2(d_r)
on ((c_l_l_l = c_l_l_l) AND (d_r < c_l_l_l))
) T2(c_l_l_l_r, d_r_r)
on (c_l_l_l_r < (67 * 14))
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
Select e_r_l_l, c_r
from (
Select e_l_l, e_r_l, b_l_l, c_r
from (
Select e_l, b_l, e_r
from (
Select e, b, d
from p3
where (d = 4)
) T1(e_l, b_l, d_l)
left join (
Select e, c, d
from p5
where (c = ((66 + (b + e)) - d))
) T2(e_r, c_r, d_r)
on (69 > (e_r - (b_l - 53)))
) T1(e_l_l, b_l_l, e_r_l)
full join (
Select c
from p1
where (d = 72)
) T2(c_r)
on (23 = e_l_l)
) T1(e_l_l_l, e_r_l_l, b_l_l_l, c_r_l)
left join (
select c, b
from (
Select c, b
from p1
where ((21 = 57) AND ((c > b) AND (c = (c - 61))))
) T1
union all
select d_l, d_r
from (
Select d_l, d_r
from (
Select e, d
from p2
where (61 > 32)
) T1(e_l, d_l)
inner join (
Select c, d
from p4
where (89 < c)
) T2(c_r, d_r)
on (d_l < (62 * ((d_r + d_r) + 47)))
) T2
) T2(c_r, b_r)
on (c_r < (c_r * 42))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l_l, c_r_l, d_r_r
from (
Select c_r_l, c_r
from (
Select a_l_l_r_l, c_r
from (
Select c_l, b_l, a_l_l_r
from (
Select c, b
from p4
where ((a = e) AND (((25 - e) > (6 * c)) OR (99 > ((a * b) + (40 * (93 + (((68 + e) * 3) * (e * 97))))))))
) T1(c_l, b_l)
left join (
Select a_l_l, b_r_r_l, e_r, c_r
from (
Select c_l, a_l, b_r_r, e_r_l_r, c_r_r
from (
Select e, c, a
from p3
where (((a - 92) < b) OR ((54 < c) OR ((e < 58) OR (((d * 10) < a) AND (77 = 10)))))
) T1(e_l, c_l, a_l)
full join (
Select c_r_l, a_r_l_l, e_r_l, e_l_l_l, e_r, c_r, b_r
from (
Select d_r_l, e_l_l, a_r_l, e_r, c_r
from (
Select e_l, a_r, d_r
from (
Select e, c, a
from p3
where (b < 82)
) T1(e_l, c_l, a_l)
left join (
Select c, a, d
from p2
where ((e > 75) OR (b = 87))
) T2(c_r, a_r, d_r)
on (d_r = ((91 * e_l) * d_r))
) T1(e_l_l, a_r_l, d_r_l)
left join (
select e, c
from (
Select e, c, a, b
from p4
where (((34 + b) * 87) = (a - 80))
) T1
union all
select c_l, b_l_l_r
from (
Select c_l, b_l_l_r
from (
Select c
from p1
where ((e < 58) OR (a = 78))
) T1(c_l)
inner join (
Select b_r_l, b_l_l, e_r, c_r, d_r
from (
Select b_l, b_r
from (
Select b, d
from p2
where (d > 4)
) T1(b_l, d_l)
left join (
Select c, b
from p4
where (e = ((c - 36) * e))
) T2(c_r, b_r)
on (((67 * (b_r - 87)) < b_r) AND (b_r = (62 - b_r)))
) T1(b_l_l, b_r_l)
left join (
Select e, c, b, d
from p4
where (91 < 73)
) T2(e_r, c_r, b_r, d_r)
on ((b_r_l = d_r) AND ((92 < b_r_l) AND (((e_r + d_r) = 98) OR ((0 + 32) = 64))))
) T2(b_r_l_r, b_l_l_r, e_r_r, c_r_r, d_r_r)
on (((c_l * c_l) < 22) AND ((b_l_l_r = 13) AND (b_l_l_r < 80)))
) T2
) T2(e_r, c_r)
on (54 > (d_r_l - e_l_l))
) T1(d_r_l_l, e_l_l_l, a_r_l_l, e_r_l, c_r_l)
inner join (
Select e, c, b
from p3
where ((b < d) OR (e = 25))
) T2(e_r, c_r, b_r)
on ((37 = (44 + 45)) AND ((c_r = (5 + 46)) AND ((a_r_l_l > ((57 - 23) + (b_r + b_r))) AND ((e_r_l = c_r_l) AND ((0 > (17 + e_r)) OR ((89 * a_r_l_l) > 95))))))
) T2(c_r_l_r, a_r_l_l_r, e_r_l_r, e_l_l_l_r, e_r_r, c_r_r, b_r_r)
on ((15 = a_l) OR (71 < b_r_r))
) T1(c_l_l, a_l_l, b_r_r_l, e_r_l_r_l, c_r_r_l)
left join (
select e, c
from (
Select e, c, a, d
from p3
where ((a = (b * 72)) AND (c < (a - d)))
) T1
union all
select c, a
from (
Select c, a
from p5
where (11 = 40)
) T2
) T2(e_r, c_r)
on ((((24 - (c_r + a_l_l)) + (a_l_l * e_r)) < a_l_l) OR (b_r_r_l > 85))
) T2(a_l_l_r, b_r_r_l_r, e_r_r, c_r_r)
on (((51 - (24 * 98)) < 5) AND (a_l_l_r > 9))
) T1(c_l_l, b_l_l, a_l_l_r_l)
inner join (
Select e, c, d
from p2
where (d = 66)
) T2(e_r, c_r, d_r)
on (a_l_l_r_l = 82)
) T1(a_l_l_r_l_l, c_r_l)
left join (
Select c
from p1
where (64 = (d - (b - 82)))
) T2(c_r)
on (c_r = c_r_l)
) T1(c_r_l_l, c_r_l)
left join (
Select e_l, c_l, d_r
from (
Select e, c
from p3
where ((d + e) > 31)
) T1(e_l, c_l)
left join (
Select d
from p3
where ((e = 78) AND (62 = 51))
) T2(d_r)
on ((c_l + (c_l - 96)) = 74)
) T2(e_l_r, c_l_r, d_r_r)
on ((d_r_r < 40) OR (((5 - d_r_r) > 44) AND (d_r_r < c_r_l_l)))
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
Select d_l, e_r, d_r
from (
Select d
from p5
where (d = e)
) T1(d_l)
left join (
Select e, b, d
from p5
where ((d = a) OR ((e = 83) AND ((a < e) AND (c = (49 - 36)))))
) T2(e_r, b_r, d_r)
on (((98 + 12) = (e_r - d_l)) AND (((14 + 73) * e_r) > e_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, a_r
from (
Select c, a, b
from p5
where (87 > 48)
) T1(c_l, a_l, b_l)
full join (
Select a
from p1
where ((31 - d) < 24)
) T2(a_r)
on ((a_r = (30 + 3)) OR (b_l > c_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r
from (
Select d
from p4
where (83 = b)
) T1(d_l)
full join (
Select c
from p3
where (((d - 95) = b) OR (40 > b))
) T2(c_r)
on (c_r = 68)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, d_r
from (
Select e, a, d
from p5
where (((a - (17 * c)) - d) < 57)
) T1(e_l, a_l, d_l)
inner join (
Select e, c, b, d
from p3
where (82 = b)
) T2(e_r, c_r, b_r, d_r)
on (((0 * (34 - 14)) < (d_l * 51)) OR (3 > 62))
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
Select e_l, d_l, e_r, b_r
from (
Select e, d
from p3
where ((d < e) AND ((c * (e * c)) > c))
) T1(e_l, d_l)
inner join (
Select e, b, d
from p3
where (49 < c)
) T2(e_r, b_r, d_r)
on (b_r = (1 + ((d_l - 73) * 49)))
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
Select a_l, e_r
from (
Select e, a, d
from p1
where ((72 = a) AND ((28 = (((d + a) + e) + 47)) OR ((b + 57) > 76)))
) T1(e_l, a_l, d_l)
full join (
Select e, c, b
from p2
where ((d = a) AND (c > 73))
) T2(e_r, c_r, b_r)
on (30 = 51)
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
Select c_l, b_l, d_l, a_r
from (
Select c, b, d
from p4
where (89 > b)
) T1(c_l, b_l, d_l)
left join (
Select a
from p5
where ((d - b) < b)
) T2(a_r)
on ((b_l = d_l) OR (d_l = c_l))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l, b_l_l, a_r_r
from (
select b_l, c_r
from (
Select b_l, c_r
from (
Select b
from p3
where (d > 88)
) T1(b_l)
left join (
Select c, a, b
from p5
where (a = c)
) T2(c_r, a_r, b_r)
on (c_r = c_r)
) T1
union all
select c_r_l, d_l_l
from (
Select c_r_l, d_l_l, e_r_r
from (
Select d_l, c_r
from (
Select d
from p4
where (((b + 15) = 49) AND ((b = d) AND (26 = 11)))
) T1(d_l)
full join (
Select c, a, b, d
from p4
where ((d < d) AND (((c - (e + (b + 98))) = a) AND (a = 0)))
) T2(c_r, a_r, b_r, d_r)
on (89 = ((c_r - 74) * 59))
) T1(d_l_l, c_r_l)
left join (
Select d_l, e_r, a_r, b_r
from (
Select a, d
from p2
where (74 = 24)
) T1(a_l, d_l)
left join (
Select e, a, b
from p1
where ((a - e) < a)
) T2(e_r, a_r, b_r)
on (e_r < e_r)
) T2(d_l_r, e_r_r, a_r_r, b_r_r)
on (8 > 18)
) T2
) T1(b_l_l, c_r_l)
left join (
Select a_l, a_r
from (
Select c, a, b
from p4
where ((4 = 66) AND ((48 - 56) = c))
) T1(c_l, a_l, b_l)
full join (
Select a
from p3
where (78 > 62)
) T2(a_r)
on (10 = 2)
) T2(a_l_r, a_r_r)
on (15 < 32)
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
Select e_l, d_l, c_r, a_r
from (
Select e, d
from p2
where ((e = 45) AND (68 = d))
) T1(e_l, d_l)
full join (
select c, a
from (
Select c, a, d
from p2
where (c = b)
) T1
union all
select e_r_l_l, a_r
from (
Select e_r_l_l, a_r
from (
Select c_l_l, e_l_l, e_r_l, e_r, c_r
from (
Select e_l, c_l, d_l, e_r
from (
Select e, c, d
from p1
where (e < a)
) T1(e_l, c_l, d_l)
left join (
Select e, d
from p4
where (84 = 2)
) T2(e_r, d_r)
on ((88 * 82) > e_r)
) T1(e_l_l, c_l_l, d_l_l, e_r_l)
left join (
Select e, c
from p2
where (((a * 22) < b) AND (d < (e - b)))
) T2(e_r, c_r)
on (c_l_l > 96)
) T1(c_l_l_l, e_l_l_l, e_r_l_l, e_r_l, c_r_l)
left join (
Select a, b
from p1
where (((d + 71) = d) AND ((d < b) OR (a = 53)))
) T2(a_r, b_r)
on (e_r_l_l < (e_r_l_l - a_r))
) T2
) T2(c_r, a_r)
on ((a_r > 48) AND ((a_r = a_r) OR (57 > c_r)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_r_l, b_r
from (
Select d_r_l, b_l_l, d_r_r, e_r_r_r_r_l_r
from (
Select b_l, d_r
from (
Select b
from p1
where ((b = a) OR (90 > c))
) T1(b_l)
full join (
Select d
from p2
where ((18 < c) OR (((b + 73) + 72) > 21))
) T2(d_r)
on (d_r > d_r)
) T1(b_l_l, d_r_l)
inner join (
Select e_r_r_r_r_l, d_r
from (
Select b_l_l_l_l_l, c_r_l, d_r_l_l, e_r_r_r_r, d_l_r
from (
Select d_r_l, b_l_l_l_l, d_r_l_l, c_r
from (
Select b_r_l, b_l_l_l, d_r_l, d_r
from (
Select a_l_l, b_l_l, b_r, d_r
from (
Select a_l, b_l, d_r
from (
Select e, a, b
from p2
where (70 < c)
) T1(e_l, a_l, b_l)
left join (
Select e, d
from p3
where (((((2 + 99) + c) * c) < 62) OR ((d > (c * a)) AND (56 = 50)))
) T2(e_r, d_r)
on (b_l = 72)
) T1(a_l_l, b_l_l, d_r_l)
left join (
Select e, a, b, d
from p2
where (91 < ((57 + ((27 * a) * (e * 6))) + d))
) T2(e_r, a_r, b_r, d_r)
on ((53 = d_r) OR ((59 = 2) AND (52 > 9)))
) T1(a_l_l_l, b_l_l_l, b_r_l, d_r_l)
left join (
Select e, d
from p5
where (10 > 34)
) T2(e_r, d_r)
on (d_r < b_l_l_l)
) T1(b_r_l_l, b_l_l_l_l, d_r_l_l, d_r_l)
full join (
select c
from (
Select c
from p1
where (d > a)
) T1
union all
select c
from (
select c
from (
Select c, b
from p3
where ((a - 79) > 96)
) T1
union all
select c
from (
Select c
from p4
where (70 = c)
) T2
) T2
) T2(c_r)
on (b_l_l_l_l > d_r_l_l)
) T1(d_r_l_l, b_l_l_l_l_l, d_r_l_l_l, c_r_l)
left join (
Select d_l, e_r_r_r
from (
Select e, a, d
from p1
where (9 < 89)
) T1(e_l, a_l, d_l)
inner join (
Select d_l, e_r_r
from (
Select d
from p5
where ((c = b) AND ((32 < 33) OR (a > a)))
) T1(d_l)
left join (
select d_l, e_r
from (
Select d_l, e_r, a_r, b_r
from (
Select e, d
from p1
where (d = e)
) T1(e_l, d_l)
left join (
Select e, a, b
from p3
where (8 > 27)
) T2(e_r, a_r, b_r)
on (e_r = 13)
) T1
union all
select b, d
from (
Select b, d
from p1
where ((90 * 51) = 99)
) T2
) T2(d_l_r, e_r_r)
on ((e_r_r * e_r_r) = e_r_r)
) T2(d_l_r, e_r_r_r)
on ((23 > d_l) OR (68 = (69 * d_l)))
) T2(d_l_r, e_r_r_r_r)
on ((16 < d_l_r) OR ((((((((((e_r_r_r_r - c_r_l) * d_l_r) - ((25 + 36) * d_r_l_l)) * d_l_r) + 43) - c_r_l) * (97 * c_r_l)) + ((31 + 97) * 55)) * (e_r_r_r_r + 15)) = b_l_l_l_l_l))
) T1(b_l_l_l_l_l_l, c_r_l_l, d_r_l_l_l, e_r_r_r_r_l, d_l_r_l)
inner join (
Select d
from p5
where (24 = 58)
) T2(d_r)
on (e_r_r_r_r_l = d_r)
) T2(e_r_r_r_r_l_r, d_r_r)
on (65 > 12)
) T1(d_r_l_l, b_l_l_l, d_r_r_l, e_r_r_r_r_l_r_l)
inner join (
Select c, b
from p3
where (c > d)
) T2(c_r, b_r)
on (b_r = 63)
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
Select e_r_l, a_r
from (
Select c_l, a_l, e_r
from (
Select c, a
from p3
where ((e * d) = e)
) T1(c_l, a_l)
full join (
Select e
from p1
where (47 = ((d - c) * c))
) T2(e_r)
on (c_l > 95)
) T1(c_l_l, a_l_l, e_r_l)
left join (
select a
from (
Select a
from p1
where (4 = (d - (e * (91 - ((77 - a) + 90)))))
) T1
union all
select e
from (
Select e
from p3
where (42 > b)
) T2
) T2(a_r)
on (e_r_l = a_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, a_r_l, a_r
from (
Select c_l, a_r
from (
Select c
from p2
where (b > a)
) T1(c_l)
left join (
Select e, c, a, b
from p2
where ((65 = a) AND (e = 33))
) T2(e_r, c_r, a_r, b_r)
on (22 = 26)
) T1(c_l_l, a_r_l)
left join (
Select a, b, d
from p3
where (34 = 47)
) T2(a_r, b_r, d_r)
on (96 < 48)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_r_l, b_r_l_l, e_r
from (
Select b_r_l, c_l_r
from (
Select c_l, b_r
from (
Select c, a, d
from p3
where ((b = 1) OR (10 > (49 * d)))
) T1(c_l, a_l, d_l)
inner join (
Select c, b
from p3
where ((e = 27) AND (29 = c))
) T2(c_r, b_r)
on (71 > (c_l - b_r))
) T1(c_l_l, b_r_l)
left join (
Select c_l, b_l, e_r
from (
Select c, b
from p1
where (e = 25)
) T1(c_l, b_l)
inner join (
Select e, a
from p2
where (12 < 20)
) T2(e_r, a_r)
on (4 > (30 - c_l))
) T2(c_l_r, b_l_r, e_r_r)
on ((c_l_r > 2) OR (b_r_l > (b_r_l * 85)))
) T1(b_r_l_l, c_l_r_l)
full join (
select e
from (
Select e
from p5
where (4 = b)
) T1
union all
select c_l
from (
Select c_l, e_r, d_r
from (
Select c
from p3
where (e < a)
) T1(c_l)
inner join (
Select e, c, a, d
from p2
where (29 = a)
) T2(e_r, c_r, a_r, d_r)
on ((e_r = e_r) AND ((c_l + 5) = 36))
) T2
) T2(e_r)
on (c_l_r_l < 6)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test15exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, e_l_l, a_r
from (
Select e_l, b_l, b_r
from (
Select e, c, b
from p3
where (c < d)
) T1(e_l, c_l, b_l)
left join (
Select b
from p4
where (1 = d)
) T2(b_r)
on (12 = (e_l + (b_r * e_l)))
) T1(e_l_l, b_l_l, b_r_l)
inner join (
Select a
from p1
where (96 < c)
) T2(a_r)
on (34 < b_r_l)
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
Select a_l, b_l, c_r, b_r
from (
Select e, c, a, b
from p5
where (c > c)
) T1(e_l, c_l, a_l, b_l)
left join (
Select c, b
from p1
where ((60 > c) AND ((30 + ((89 * (77 - d)) + b)) = c))
) T2(c_r, b_r)
on (c_r < b_l)
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
    _testmgr.testcase_end(desc)

