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
    
def test001(desc="""Joins Set 2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select e_l, e_r
from (
select e
from (
Select e
from p3
where ((b < 62) OR (53 > c))
) T1
union all
select c
from (
Select c
from p4
where (d = 91)
) T2
) T1(e_l)
inner join (
Select e, c
from p3
where (((b * a) * a) = 0)
) T2(e_r, c_r)
on (e_r = e_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_r, d_r
from (
select a
from (
Select a
from p4
where (c < c)
) T1
union all
select a
from (
Select a
from p1
where ((b - 43) > b)
) T2
) T1(a_l)
full join (
Select b, d
from p5
where (((61 * c) * e) > (d - (78 * 25)))
) T2(b_r, d_r)
on (a_l = (d_r + 21))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, b_l, e_r
from (
Select e, c, b
from p5
where (((52 - (62 + c)) * 38) < (a - 34))
) T1(e_l, c_l, b_l)
left join (
select e
from (
Select e, a, d
from p2
where (b > 32)
) T1
union all
select b
from (
Select b
from p2
where ((8 = d) AND ((d > e) AND (d < 68)))
) T2
) T2(e_r)
on (41 = c_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r_r
from (
Select d
from p5
where (20 > 37)
) T1(d_l)
left join (
Select a_l_l, b_r_r_l, c_r, a_r, b_r
from (
Select e_l, a_l, b_r_r
from (
Select e, c, a
from p2
where (b > 59)
) T1(e_l, c_l, a_l)
left join (
Select b_r_l, b_r, d_r
from (
Select c_l, e_r, b_r
from (
Select c
from p4
where ((b = 12) AND ((57 + a) > c))
) T1(c_l)
full join (
Select e, a, b, d
from p4
where (67 > d)
) T2(e_r, a_r, b_r, d_r)
on (8 > e_r)
) T1(c_l_l, e_r_l, b_r_l)
left join (
Select b, d
from p1
where (a > 49)
) T2(b_r, d_r)
on (((((b_r * b_r) - b_r_l) + d_r) = 10) AND (((38 * 51) = 45) OR (97 < (b_r_l - 18))))
) T2(b_r_l_r, b_r_r, d_r_r)
on (55 = 79)
) T1(e_l_l, a_l_l, b_r_r_l)
left join (
Select e, c, a, b
from p1
where (d = a)
) T2(e_r, c_r, a_r, b_r)
on ((a_r = 42) OR (a_l_l > (75 * (((c_r * 85) + b_r_r_l) - a_l_l))))
) T2(a_l_l_r, b_r_r_l_r, c_r_r, a_r_r, b_r_r)
on (d_l = b_r_r)
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
Select e_l, e_r
from (
Select e
from p5
where (b < 84)
) T1(e_l)
inner join (
select e
from (
Select e, a
from p5
where (42 = (d * d))
) T1
union all
select e
from (
select e
from (
Select e, c, b, d
from p4
where ((84 = 44) OR (c = 60))
) T1
union all
select a
from (
Select a
from p1
where ((a = 3) AND (9 < 12))
) T2
) T2
) T2(e_r)
on (e_l = e_r)
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
Select e_l, a_l, e_r, d_r
from (
Select e, a, d
from p3
where (b < 11)
) T1(e_l, a_l, d_l)
left join (
Select e, d
from p4
where ((1 < b) AND (15 = b))
) T2(e_r, d_r)
on ((a_l < (e_l * 98)) AND (((a_l + 33) = a_l) OR ((e_r = e_r) OR (((17 + 22) + (e_r - d_r)) > ((55 * 39) * e_l)))))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, e_r_r
from (
Select c, a, b
from p1
where ((39 > 15) AND (37 > 19))
) T1(c_l, a_l, b_l)
inner join (
Select e_l, b_l, e_r, a_r
from (
Select e, b
from p4
where (((73 * b) + 82) = 73)
) T1(e_l, b_l)
left join (
Select e, a
from p2
where ((b - d) > 52)
) T2(e_r, a_r)
on (((5 * (80 - e_r)) < e_r) OR ((60 = (93 * ((b_l - 49) - 47))) AND ((e_l = 4) OR (96 < 52))))
) T2(e_l_r, b_l_r, e_r_r, a_r_r)
on (33 > e_r_r)
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
Select c_l_r_l, b_l_l, c_r
from (
Select b_l, c_l_r
from (
Select b
from p4
where (a > ((a + 18) - 13))
) T1(b_l)
full join (
select c_l, d_l, b_r
from (
Select c_l, d_l, b_r
from (
Select c, d
from p5
where (89 = 86)
) T1(c_l, d_l)
full join (
Select b
from p3
where (3 = a)
) T2(b_r)
on (((b_r + 26) = 69) AND (c_l = 33))
) T1
union all
select a_l_l, c_r, b_r
from (
Select a_l_l, c_r, b_r
from (
Select c_l, a_l, b_l, c_r
from (
Select c, a, b
from p3
where (47 < 78)
) T1(c_l, a_l, b_l)
full join (
Select c
from p2
where ((((((14 * (29 * a)) * 26) * e) * c) = 77) OR ((e = e) AND ((b < b) AND ((25 > (d + 35)) OR (a < 8)))))
) T2(c_r)
on (b_l < c_l)
) T1(c_l_l, a_l_l, b_l_l, c_r_l)
left join (
Select c, b
from p2
where (a < 2)
) T2(c_r, b_r)
on (c_r = 56)
) T2
) T2(c_l_r, d_l_r, b_r_r)
on (74 < (54 - c_l_r))
) T1(b_l_l, c_l_r_l)
left join (
Select c
from p3
where ((78 = ((b + b) * b)) OR (c > a))
) T2(c_r)
on (72 = c_l_r_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_l_r, c_r_r
from (
Select c
from p2
where ((a = e) AND (c < ((43 - 90) + d)))
) T1(c_l)
full join (
Select e_l, c_l, a_l, c_r
from (
Select e, c, a
from p3
where (d > c)
) T1(e_l, c_l, a_l)
full join (
Select c
from p1
where (47 = e)
) T2(c_r)
on (((22 + c_l) < 10) OR ((77 > 42) AND (a_l < c_l)))
) T2(e_l_r, c_l_r, a_l_r, c_r_r)
on (97 = (26 * c_l_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r
from (
Select b
from p1
where ((e < (((60 - (c + 56)) + b) - a)) OR ((e < 81) OR ((56 = b) OR (94 > e))))
) T1(b_l)
inner join (
Select c, b
from p3
where ((d = 99) OR ((((78 - 1) + 79) = (42 * 83)) AND (35 = 20)))
) T2(c_r, b_r)
on (b_l < 44)
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
Select a_l_l, c_r
from (
Select a_l, c_r
from (
Select a, b
from p1
where (60 = 75)
) T1(a_l, b_l)
inner join (
Select c
from p2
where ((d > 87) OR (b > 60))
) T2(c_r)
on (((a_l - 80) > (c_r * a_l)) OR (((12 - 83) + 67) < 61))
) T1(a_l_l, c_r_l)
left join (
Select c
from p1
where (a < 60)
) T2(c_r)
on (((59 - c_r) = ((35 * 85) * (85 + 37))) OR (a_l_l < 47))
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
Select b_r_l, b_l_r
from (
select e_l_l, e_r, b_r
from (
Select e_l_l, e_r, b_r
from (
Select e_l, d_r
from (
Select e, c, b
from p1
where ((c = c) AND (c > 17))
) T1(e_l, c_l, b_l)
left join (
Select c, b, d
from p3
where (a > 84)
) T2(c_r, b_r, d_r)
on (71 = e_l)
) T1(e_l_l, d_r_l)
full join (
Select e, b, d
from p3
where (a = 6)
) T2(e_r, b_r, d_r)
on (e_l_l < 80)
) T1
union all
select e, c, a
from (
select e, c, a
from (
Select e, c, a
from p4
where (b > d)
) T1
union all
select e, c, d
from (
Select e, c, d
from p5
where (e = (4 - e))
) T2
) T2
) T1(e_l_l_l, e_r_l, b_r_l)
inner join (
select a_l, b_l
from (
Select a_l, b_l, d_r
from (
Select a, b
from p2
where ((e = 77) OR (c = d))
) T1(a_l, b_l)
left join (
Select a, d
from p4
where ((34 = b) OR (67 > e))
) T2(a_r, d_r)
on (b_l > b_l)
) T1
union all
select a, d
from (
Select a, d
from p3
where ((97 < 27) OR (34 = 19))
) T2
) T2(a_l_r, b_l_r)
on (98 > b_l_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l_l_r
from (
Select e
from p5
where ((d > 65) AND (((34 + b) = b) OR (41 = a)))
) T1(e_l)
inner join (
select c_l_r_l_l_r_l, d_l_l
from (
select c_l_r_l_l_r_l, d_l_l
from (
Select c_l_r_l_l_r_l, d_l_l, a_r
from (
Select d_l, b_r_r, b_r_r_l_l_r, c_l_r_l_l_r
from (
Select d
from p5
where (58 < 68)
) T1(d_l)
inner join (
Select b_r_r_l_l, c_l_r_l_l, e_r, b_r
from (
Select c_l_r_l, b_r_r_l, e_r
from (
Select a_l, c_l_r, b_r_r
from (
Select a
from p1
where (c = 96)
) T1(a_l)
left join (
Select c_l, b_r
from (
Select c
from p1
where (((98 - d) - ((((89 * 35) - c) + (b + b)) - e)) = 67)
) T1(c_l)
full join (
select b
from (
Select b
from p5
where ((d + (91 * 22)) = a)
) T1
union all
select b
from (
Select b
from p2
where ((73 + 31) > 47)
) T2
) T2(b_r)
on (80 > b_r)
) T2(c_l_r, b_r_r)
on (34 > c_l_r)
) T1(a_l_l, c_l_r_l, b_r_r_l)
inner join (
Select e
from p3
where (b < 77)
) T2(e_r)
on (((((c_l_r_l - 86) - e_r) * 7) - 66) < b_r_r_l)
) T1(c_l_r_l_l, b_r_r_l_l, e_r_l)
inner join (
Select e, b
from p4
where (e = (13 + 32))
) T2(e_r, b_r)
on (11 = b_r_r_l_l)
) T2(b_r_r_l_l_r, c_l_r_l_l_r, e_r_r, b_r_r)
on (b_r_r_l_l_r = (c_l_r_l_l_r * 26))
) T1(d_l_l, b_r_r_l, b_r_r_l_l_r_l, c_l_r_l_l_r_l)
left join (
Select a, b
from p3
where ((23 < a) OR (24 = (e + 58)))
) T2(a_r, b_r)
on (d_l_l = ((41 + 49) - c_l_r_l_l_r_l))
) T1
union all
select b, d
from (
Select b, d
from p4
where (e = (84 * 64))
) T2
) T1
union all
select c, b
from (
select c, b
from (
Select c, b, d
from p5
where (c > 49)
) T1
union all
select e, d
from (
Select e, d
from p5
where ((b = e) OR ((35 * a) < 45))
) T2
) T2
) T2(c_l_r_l_l_r_l_r, d_l_l_r)
on ((d_l_l_r = 86) OR (64 = 33))
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
Select e_l, c_l_r, c_r_r, d_l_r
from (
Select e
from p4
where (((73 * 17) - 59) = (c + (90 * b)))
) T1(e_l)
left join (
Select c_l, b_l, d_l, c_r
from (
Select c, b, d
from p3
where ((b * e) = d)
) T1(c_l, b_l, d_l)
left join (
select c
from (
Select c
from p2
where ((62 < c) OR (d > (d + 24)))
) T1
union all
select e
from (
Select e, c
from p5
where ((c = b) AND (90 = e))
) T2
) T2(c_r)
on (d_l > 54)
) T2(c_l_r, b_l_r, d_l_r, c_r_r)
on (80 > c_r_r)
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
Select e_l, c_r
from (
select e, c
from (
Select e, c
from p3
where ((94 * 54) < 63)
) T1
union all
select e_r_l, a_r
from (
Select e_r_l, a_r, d_r
from (
Select b_l, e_r
from (
Select b
from p2
where (a = 53)
) T1(b_l)
full join (
Select e, a, d
from p1
where ((24 * c) > c)
) T2(e_r, a_r, d_r)
on (((b_l * e_r) = e_r) AND ((e_r > e_r) OR (30 < (22 + b_l))))
) T1(b_l_l, e_r_l)
full join (
Select a, d
from p2
where (a < 57)
) T2(a_r, d_r)
on (a_r = a_r)
) T2
) T1(e_l, c_l)
full join (
Select c
from p2
where (b < a)
) T2(c_r)
on (14 > 58)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, a_r
from (
Select a
from p5
where (47 > (a - (65 - e)))
) T1(a_l)
full join (
Select a, b
from p5
where (51 = c)
) T2(a_r, b_r)
on ((((a_l * a_l) + a_l) = a_l) OR (1 = a_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, a_l_l_l_l, a_r, d_r
from (
Select a_l_l_l, e_r, b_r
from (
Select a_l_l, c_l_r_l, a_r_r_l, b_r
from (
Select a_l, c_l_r, a_r_r, c_r_r
from (
Select c, a
from p3
where ((d > a) OR (e < b))
) T1(c_l, a_l)
inner join (
Select c_l, c_r, a_r, d_r
from (
Select e, c
from p2
where (76 > (25 + (b - e)))
) T1(e_l, c_l)
inner join (
Select c, a, b, d
from p3
where ((a > d) AND (33 < 43))
) T2(c_r, a_r, b_r, d_r)
on ((12 = 28) AND (c_r = 25))
) T2(c_l_r, c_r_r, a_r_r, d_r_r)
on (c_l_r = c_l_r)
) T1(a_l_l, c_l_r_l, a_r_r_l, c_r_r_l)
left join (
Select a, b, d
from p2
where (96 < c)
) T2(a_r, b_r, d_r)
on (a_r_r_l = a_l_l)
) T1(a_l_l_l, c_l_r_l_l, a_r_r_l_l, b_r_l)
full join (
Select e, c, b, d
from p5
where ((b < ((95 - 22) + b)) AND (a = b))
) T2(e_r, c_r, b_r, d_r)
on ((a_l_l_l = 64) AND (27 > (b_r * 94)))
) T1(a_l_l_l_l, e_r_l, b_r_l)
full join (
Select e, a, d
from p1
where (96 > 21)
) T2(e_r, a_r, d_r)
on (d_r < 32)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, e_r_l, b_r_r, a_r_r, d_l_r
from (
select a_l, e_r
from (
Select a_l, e_r
from (
Select c, a, b
from p2
where ((c = d) AND (58 = 24))
) T1(c_l, a_l, b_l)
left join (
Select e
from p5
where (91 < 54)
) T2(e_r)
on (e_r = e_r)
) T1
union all
select e, c
from (
select e, c
from (
Select e, c, b, d
from p4
where (d = d)
) T1
union all
select c, b
from (
Select c, b
from p3
where (d = 53)
) T2
) T2
) T1(a_l_l, e_r_l)
left join (
Select c_l, d_l, a_r, b_r
from (
Select c, a, d
from p1
where ((c + 53) = b)
) T1(c_l, a_l, d_l)
inner join (
Select a, b
from p4
where (25 = ((93 * a) + d))
) T2(a_r, b_r)
on (b_r = d_l)
) T2(c_l_r, d_l_r, a_r_r, b_r_r)
on ((((42 - 50) + ((29 + (37 + ((b_r_r + ((59 * e_r_l) - 31)) - 88))) * b_r_r)) > 32) OR (44 < b_r_r))
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test02exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r, d_r
from (
Select a, d
from p3
where ((51 > 65) AND ((c = (18 - e)) AND (80 < d)))
) T1(a_l, d_l)
full join (
Select e, d
from p3
where (a = 82)
) T2(e_r, d_r)
on ((10 < 55) OR (((57 - (e_r - d_r)) < d_r) AND (1 > e_r)))
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
Select d_r_l, b_l_l, e_r, c_r
from (
Select b_l, d_r
from (
Select b, d
from p4
where (c = ((e + a) * a))
) T1(b_l, d_l)
left join (
Select a, d
from p2
where ((e = b) OR (18 = 26))
) T2(a_r, d_r)
on ((d_r = 92) AND ((48 < d_r) OR (b_l < 5)))
) T1(b_l_l, d_r_l)
inner join (
Select e, c, a
from p5
where ((c > 75) OR (27 = (e + (((((4 - 10) * 66) - a) - d) + 26))))
) T2(e_r, c_r, a_r)
on (58 = 29)
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
    #*********************************************
    _testmgr.testcase_end(desc)

