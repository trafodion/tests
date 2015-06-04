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
    
def test001(desc="""Joins Set 7"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select e_l, d_r
from (
Select e, c, b
from p4
where ((a - 1) = 89)
) T1(e_l, c_l, b_l)
left join (
Select d
from p1
where (d > 66)
) T2(d_r)
on (59 > d_r)
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
Select b_l, b_l_l_r
from (
Select b, d
from p4
where (6 = a)
) T1(b_l, d_l)
left join (
Select b_l_l, d_l_l, d_r
from (
Select a_l, b_l, d_l, e_r
from (
Select a, b, d
from p1
where (((e * ((89 + 40) + d)) * 24) = a)
) T1(a_l, b_l, d_l)
inner join (
Select e
from p5
where ((5 - 23) = (a * (10 + 67)))
) T2(e_r)
on (e_r = b_l)
) T1(a_l_l, b_l_l, d_l_l, e_r_l)
left join (
Select d
from p5
where ((c = 60) OR ((((c * d) + b) = d) OR (62 = 93)))
) T2(d_r)
on (d_r = 15)
) T2(b_l_l_r, d_l_l_r, d_r_r)
on ((99 = 81) AND (6 = (b_l_l_r * b_l_l_r)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, e_r
from (
Select e, b, d
from p3
where (d = 35)
) T1(e_l, b_l, d_l)
left join (
Select e, d
from p2
where ((3 = (b * 54)) AND (66 > (76 - a)))
) T2(e_r, d_r)
on (b_l < 36)
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
Select a_l, c_l_r
from (
select a
from (
Select a
from p2
where ((12 = (18 + d)) OR (97 < (51 + (b + (a + a)))))
) T1
union all
select e
from (
Select e, b, d
from p4
where (95 = 53)
) T2
) T1(a_l)
left join (
Select c_l, c_r
from (
Select e, c, a
from p1
where ((79 < 68) OR ((63 + a) < b))
) T1(e_l, c_l, a_l)
inner join (
Select c
from p3
where (a > (96 * ((b - (11 + a)) + (73 + (37 + 59)))))
) T2(c_r)
on (29 > 35)
) T2(c_l_r, c_r_r)
on ((a_l = 74) OR (8 = a_l))
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
Select a_l, d_r
from (
Select c, a, b, d
from p1
where (c = 17)
) T1(c_l, a_l, b_l, d_l)
inner join (
Select c, d
from p5
where ((b = 22) AND (99 < c))
) T2(c_r, d_r)
on (d_r = (68 - ((16 - 81) - 65)))
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
Select b_r_l, e_r
from (
Select b_r_l, e_l_l, c_r, a_r, b_r, d_r
from (
Select e_l, b_r
from (
Select e, c, b
from p5
where (96 = (21 - ((95 + a) - (48 * a))))
) T1(e_l, c_l, b_l)
inner join (
Select c, b
from p1
where (97 = 70)
) T2(c_r, b_r)
on ((68 * e_l) < b_r)
) T1(e_l_l, b_r_l)
inner join (
Select c, a, b, d
from p3
where ((70 - 72) = ((92 - 90) * (11 + d)))
) T2(c_r, a_r, b_r, d_r)
on ((a_r = 90) AND (24 > b_r_l))
) T1(b_r_l_l, e_l_l_l, c_r_l, a_r_l, b_r_l, d_r_l)
full join (
Select e
from p5
where ((d = (75 * 46)) OR (b = (31 * 13)))
) T2(e_r)
on (98 = b_r_l)
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
Select a_r_l, a_r
from (
select e_l, a_r
from (
Select e_l, a_r
from (
Select e
from p4
where (a > c)
) T1(e_l)
inner join (
select c, a
from (
Select c, a, b
from p4
where (d < 1)
) T1
union all
select c, d
from (
Select c, d
from p4
where ((74 = 58) OR ((d > 60) AND (b = e)))
) T2
) T2(c_r, a_r)
on ((26 - ((a_r * e_l) + (74 * e_l))) = 51)
) T1
union all
select a_l, e_r
from (
Select a_l, e_r, c_r, a_r
from (
Select a
from p2
where (56 = c)
) T1(a_l)
full join (
Select e, c, a
from p3
where (((a + e) < ((35 + (a * 87)) + 38)) OR ((d = a) AND ((22 < 0) AND (d < (e * 45)))))
) T2(e_r, c_r, a_r)
on (e_r < 1)
) T2
) T1(e_l_l, a_r_l)
left join (
Select a
from p1
where ((71 + b) = 7)
) T2(a_r)
on (a_r_l = a_r_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r, d_r
from (
Select a, d
from p5
where (((31 * 80) = 74) AND ((2 = 2) AND ((e - (89 * a)) < 6)))
) T1(a_l, d_l)
left join (
Select c, d
from p2
where (42 = 83)
) T2(c_r, d_r)
on (d_r < d_r)
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
Select d_l, b_r, d_r
from (
Select d
from p1
where ((a > 1) OR (d > (b * (d * (((e - b) + c) * c)))))
) T1(d_l)
left join (
Select b, d
from p1
where (60 < d)
) T2(b_r, d_r)
on ((((62 * d_l) - (82 - 89)) > 75) OR (64 < (17 - d_l)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r
from (
Select b
from p4
where (((a * 20) < c) OR (58 > d))
) T1(b_l)
full join (
Select a
from p1
where ((a + 67) = b)
) T2(a_r)
on ((74 + ((b_l + a_r) + 56)) = a_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
Select a, d
from p5
where (8 = c)
) T1(a_l, d_l)
inner join (
Select a
from p1
where ((a > (35 * 15)) OR (a = (49 * d)))
) T2(a_r)
on ((17 < 75) AND (a_l > 8))
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
Select a_l, d_r
from (
select e, a, b
from (
Select e, a, b
from p3
where ((39 = 18) AND (e < 45))
) T1
union all
select e, b, d
from (
Select e, b, d
from p5
where (d = 65)
) T2
) T1(e_l, a_l, b_l)
inner join (
Select d
from p5
where ((1 = d) OR ((c = 72) AND ((a < c) OR (c = 24))))
) T2(d_r)
on (d_r = 42)
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
Select e_l, c_r
from (
Select e
from p3
where (((13 + 96) * c) = (b - (66 + d)))
) T1(e_l)
left join (
Select e, c, a
from p4
where (((90 * c) - a) = d)
) T2(e_r, c_r, a_r)
on ((33 < 70) OR (e_l = 24))
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
Select b_l, a_l_r, a_l_r_r
from (
select b, d
from (
select b, d
from (
Select b, d
from p1
where (b > (b + e))
) T1
union all
select e_l, d_l
from (
select e_l, d_l
from (
Select e_l, d_l, e_l_r, a_r_r
from (
Select e, d
from p3
where ((e + 38) = d)
) T1(e_l, d_l)
full join (
Select e_l, a_r
from (
Select e, a
from p3
where (44 < d)
) T1(e_l, a_l)
inner join (
Select a
from p1
where (d > c)
) T2(a_r)
on ((4 = a_r) AND ((10 * (84 - (a_r + a_r))) > (e_l - e_l)))
) T2(e_l_r, a_r_r)
on ((9 = 83) OR ((a_r_r = a_r_r) AND (22 = (a_r_r + 82))))
) T1
union all
select e, b
from (
Select e, b
from p1
where ((44 = d) AND ((a = a) OR (c = d)))
) T2
) T2
) T1
union all
select a_l_l, d_r_l
from (
Select a_l_l, d_r_l, c_r, a_r
from (
Select a_l, d_r
from (
Select e, a
from p1
where ((87 * c) = 10)
) T1(e_l, a_l)
left join (
Select e, c, d
from p5
where (b = a)
) T2(e_r, c_r, d_r)
on (3 > (d_r + d_r))
) T1(a_l_l, d_r_l)
full join (
Select c, a
from p4
where ((a + e) > d)
) T2(c_r, a_r)
on (28 = (a_r + ((94 - 39) * (d_r_l - 35))))
) T2
) T1(b_l, d_l)
left join (
Select a_l, a_l_r, d_r_r
from (
Select e, a, d
from p4
where (b > 58)
) T1(e_l, a_l, d_l)
inner join (
Select a_l, d_r
from (
Select e, a
from p1
where (e > e)
) T1(e_l, a_l)
left join (
Select d
from p4
where (d = b)
) T2(d_r)
on (87 = 28)
) T2(a_l_r, d_r_r)
on ((86 = a_l_r) OR ((d_r_r < (93 + a_l_r)) AND (a_l_r < 59)))
) T2(a_l_r, a_l_r_r, d_r_r_r)
on ((((a_l_r + 95) + 81) < ((68 * 32) - b_l)) AND (a_l_r = 45))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test07exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, e_r
from (
Select e, d
from p5
where ((82 = (e * 0)) AND (64 = 56))
) T1(e_l, d_l)
left join (
select e
from (
Select e
from p2
where (a = 86)
) T1
union all
select b
from (
Select b
from p5
where (d > 59)
) T2
) T2(e_r)
on (56 = ((96 + 88) * e_r))
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
Select b_l, d_l, c_r
from (
Select a, b, d
from p4
where (43 > d)
) T1(a_l, b_l, d_l)
inner join (
Select c, a, b
from p4
where (85 = 44)
) T2(c_r, a_r, b_r)
on (43 < b_l)
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
Select a_r_l, b_r_r, c_r_l_r
from (
Select d_l, e_r, a_r
from (
Select d
from p1
where ((92 = a) AND (a = d))
) T1(d_l)
left join (
Select e, a, b
from p5
where (6 = d)
) T2(e_r, a_r, b_r)
on (95 > 56)
) T1(d_l_l, e_r_l, a_r_l)
left join (
Select c_r_l, d_l_l, b_r, d_r
from (
select d_l, c_r
from (
Select d_l, c_r
from (
Select d
from p4
where (62 < 5)
) T1(d_l)
left join (
Select c
from p3
where (16 = c)
) T2(c_r)
on (78 = c_r)
) T1
union all
select a, b
from (
Select a, b, d
from p4
where ((1 + (77 * (d - d))) = c)
) T2
) T1(d_l_l, c_r_l)
full join (
Select b, d
from p5
where ((80 + 98) = b)
) T2(b_r, d_r)
on (77 > d_r)
) T2(c_r_l_r, d_l_l_r, b_r_r, d_r_r)
on (6 > 43)
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
Select e_l, c_r
from (
Select e
from p5
where (79 = 92)
) T1(e_l)
left join (
Select c
from p2
where (d = 7)
) T2(c_r)
on ((e_l - (e_l + e_l)) < 12)
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
Select a_r_l, a_r_l_l, e_r, c_r
from (
Select a_l_l, a_r_l, a_r, b_r
from (
Select e_l, a_l, a_r
from (
Select e, a
from p4
where (((((d + 86) * c) + 3) = 94) AND (((c - b) < 96) OR ((c < 89) AND ((1 < (a * 73)) AND ((42 * 15) = 51)))))
) T1(e_l, a_l)
inner join (
Select e, c, a, d
from p2
where ((c > a) AND ((15 = (b * d)) AND (4 = 59)))
) T2(e_r, c_r, a_r, d_r)
on ((((a_r - a_r) + e_l) < 90) AND (86 = e_l))
) T1(e_l_l, a_l_l, a_r_l)
full join (
Select a, b, d
from p2
where (((73 - (89 * 66)) - 25) = 51)
) T2(a_r, b_r, d_r)
on ((a_r_l = 55) OR ((71 + 25) = a_r_l))
) T1(a_l_l_l, a_r_l_l, a_r_l, b_r_l)
inner join (
Select e, c
from p1
where ((a * c) = 12)
) T2(e_r, c_r)
on (a_r_l_l = (a_r_l - e_r))
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
Select c_l, b_l, b_r, d_r
from (
Select c, b, d
from p2
where ((b = (46 - d)) AND (59 < c))
) T1(c_l, b_l, d_l)
left join (
Select b, d
from p5
where ((d = d) AND (e = 65))
) T2(b_r, d_r)
on ((c_l * (71 - 14)) < 36)
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

