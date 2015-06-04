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
    
def test001(desc="""Joins Set 47"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, c_r_r
from (
Select c, a, b, d
from p5
where ((2 > 58) AND ((67 < (d - 99)) OR (22 > 87)))
) T1(c_l, a_l, b_l, d_l)
left join (
Select a_r_l, e_r, c_r
from (
select d_l, a_r
from (
Select d_l, a_r
from (
Select c, d
from p2
where ((d - e) = c)
) T1(c_l, d_l)
inner join (
Select a, b, d
from p5
where (e < 26)
) T2(a_r, b_r, d_r)
on (90 > (40 - 21))
) T1
union all
select c_l, e_r
from (
Select c_l, e_r, a_r
from (
Select c
from p1
where (((28 - a) < 93) OR ((((e + 42) + 63) = 53) AND (57 = 33)))
) T1(c_l)
left join (
Select e, a, b
from p4
where (c = 81)
) T2(e_r, a_r, b_r)
on ((e_r = 24) AND (a_r = 29))
) T2
) T1(d_l_l, a_r_l)
left join (
Select e, c, d
from p4
where ((60 < (a - 50)) AND ((16 = 91) AND ((c + (96 + a)) = c)))
) T2(e_r, c_r, d_r)
on ((56 = c_r) OR (e_r < e_r))
) T2(a_r_l_r, e_r_r, c_r_r)
on (a_l < 57)
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
Select e_l_l, d_r_l, c_r, d_r
from (
Select e_l, b_l, d_r
from (
Select e, b
from p1
where ((e < 54) OR (((d - (e + b)) + d) < 90))
) T1(e_l, b_l)
left join (
select a, d
from (
Select a, d
from p1
where ((6 * (61 * a)) > 2)
) T1
union all
select a_l, d_r
from (
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from p5
where (4 = (c + 29))
) T1(a_l)
left join (
Select d
from p1
where (3 > a)
) T2(d_r)
on (96 > 34)
) T1
union all
select e, a
from (
Select e, a
from p4
where (45 = (74 * (a - 77)))
) T2
) T2
) T2(a_r, d_r)
on ((63 = 33) OR ((95 < b_l) AND ((60 + d_r) > b_l)))
) T1(e_l_l, b_l_l, d_r_l)
left join (
Select c, a, d
from p3
where (d = e)
) T2(c_r, a_r, d_r)
on (2 = ((c_r + (e_l_l + (e_l_l - (32 - (94 * c_r))))) - c_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, e_r
from (
Select b
from p3
where (59 = c)
) T1(b_l)
left join (
Select e, a
from p1
where (b > 60)
) T2(e_r, a_r)
on (((45 + 38) = e_r) AND ((b_l = 77) OR ((11 + 74) = 98)))
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
Select a_l, b_l, e_r
from (
Select a, b
from p5
where (((53 + a) > (d + 10)) OR ((((d + 93) + 79) = 76) OR (91 = e)))
) T1(a_l, b_l)
left join (
Select e, c
from p1
where ((71 = 22) OR ((15 = a) OR ((22 > 27) OR (((80 + a) * (b * 2)) = (66 + 16)))))
) T2(e_r, c_r)
on ((e_r = b_l) OR (41 = 4))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, a_l, b_r_r, d_r_r, e_r_r
from (
Select e, c, a
from p1
where (c = 64)
) T1(e_l, c_l, a_l)
full join (
Select e_l, e_r, b_r, d_r
from (
Select e
from p4
where ((d < 96) AND ((c > 87) AND (b = 95)))
) T1(e_l)
left join (
Select e, b, d
from p2
where (e > c)
) T2(e_r, b_r, d_r)
on (15 > 3)
) T2(e_l_r, e_r_r, b_r_r, d_r_r)
on ((a_l = 28) OR ((e_r_r < (62 - (60 * b_r_r))) AND (a_l = 38)))
order by 1, 2, 3, 4, 5, 6
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
Select e_l, c_l, b_l, e_r, c_r, b_r
from (
Select e, c, b
from p3
where (21 > (b + (b + 65)))
) T1(e_l, c_l, b_l)
left join (
Select e, c, b
from p3
where (e = 15)
) T2(e_r, c_r, b_r)
on (4 = 28)
order by 1, 2, 3, 4, 5, 6
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
Select c_l, e_l_r
from (
Select c, d
from p2
where (58 = a)
) T1(c_l, d_l)
inner join (
Select e_l, d_l_r
from (
Select e
from p1
where ((e = (e + 61)) OR (((b + c) < d) OR ((27 < a) AND (c = d))))
) T1(e_l)
left join (
Select d_l, c_r
from (
Select e, c, d
from p4
where ((72 = 18) OR ((71 - 84) = (((e - (70 * c)) * (b - 2)) - b)))
) T1(e_l, c_l, d_l)
full join (
Select c, b
from p4
where (a < a)
) T2(c_r, b_r)
on (c_r < d_l)
) T2(d_l_r, c_r_r)
on (((e_l + 69) > (49 + 69)) AND ((53 > 73) AND (e_l = d_l_r)))
) T2(e_l_r, d_l_r_r)
on ((c_l * 68) < 54)
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
Select b_l, d_l, a_r
from (
Select b, d
from p2
where (d = 63)
) T1(b_l, d_l)
left join (
Select a, b
from p4
where (c = b)
) T2(a_r, b_r)
on (16 < (60 + d_l))
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
from p3
where ((e * e) > a)
) T1(c_l)
left join (
Select a, d
from p4
where (55 = a)
) T2(a_r, d_r)
on (40 < c_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_r
from (
Select c
from p4
where (((93 + 92) = c) AND (e < 3))
) T1(c_l)
left join (
Select a, d
from p4
where ((c = (d - 83)) AND ((b = b) AND (97 > e)))
) T2(a_r, d_r)
on (((9 - 89) = 57) AND (a_r > 13))
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
Select c_l, b_l, c_r
from (
Select c, b
from p4
where (15 < 59)
) T1(c_l, b_l)
full join (
Select e, c, b, d
from p4
where ((c = 41) OR ((25 > 2) OR (a > 35)))
) T2(e_r, c_r, b_r, d_r)
on (c_l = ((3 * 66) + b_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_r
from (
select e
from (
Select e
from p2
where (82 = 75)
) T1
union all
select d
from (
Select d
from p5
where (((20 * d) - 93) < 85)
) T2
) T1(e_l)
left join (
Select c, a, d
from p4
where ((d < (82 + (c + 54))) OR (79 = 21))
) T2(c_r, a_r, d_r)
on (62 > d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_r, d_r
from (
Select b, d
from p3
where (19 < ((((97 - e) - (d + 59)) + 84) * b))
) T1(b_l, d_l)
full join (
Select c, a, b, d
from p3
where (35 < a)
) T2(c_r, a_r, b_r, d_r)
on (b_l > d_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, a_l_r
from (
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r
from (
select c, a
from (
Select c, a
from p2
where (93 > d)
) T1
union all
select e_l, d_r
from (
Select e_l, d_r
from (
Select e
from p1
where ((18 - (65 + (a * 14))) = e)
) T1(e_l)
left join (
Select d
from p2
where (b = a)
) T2(d_r)
on ((e_l + e_l) = d_r)
) T2
) T1(c_l, a_l)
full join (
Select e, c
from p1
where ((c = d) OR (b > 32))
) T2(e_r, c_r)
on ((2 + 53) = 11)
) T1
union all
select c, b, d
from (
Select c, b, d
from p5
where ((a + 72) = 56)
) T2
) T1(c_l_l, a_l_l, e_r_l)
left join (
Select a_l, e_l_r, a_r_r
from (
Select a
from p4
where ((e > c) OR (c = c))
) T1(a_l)
full join (
select e_l, a_r
from (
Select e_l, a_r
from (
Select e, a, d
from p3
where ((e > c) AND (77 > 68))
) T1(e_l, a_l, d_l)
left join (
select a, b
from (
Select a, b, d
from p1
where ((79 > c) OR ((c < 85) OR (29 = 11)))
) T1
union all
select e, b
from (
Select e, b
from p2
where ((36 - 66) = 42)
) T2
) T2(a_r, b_r)
on ((3 > (e_l - 18)) AND (a_r < 55))
) T1
union all
select e, c
from (
Select e, c
from p5
where (a = a)
) T2
) T2(e_l_r, a_r_r)
on ((a_r_r - a_l) = a_r_r)
) T2(a_l_r, e_l_r_r, a_r_r_r)
on ((39 + a_l_r) = a_l_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l, b_r
from (
Select c, b, d
from p3
where (63 = d)
) T1(c_l, b_l, d_l)
full join (
Select e, b, d
from p3
where (1 = 90)
) T2(e_r, b_r, d_r)
on (d_l > d_l)
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
Select c_l, a_l, e_r
from (
Select c, a
from p4
where (79 < 44)
) T1(c_l, a_l)
left join (
Select e
from p3
where ((33 = (26 - (79 * 97))) OR (0 < 20))
) T2(e_r)
on ((e_r - a_l) = e_r)
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
Select e_l, c_l, d_l, b_r
from (
Select e, c, d
from p3
where ((10 < e) OR (((c - 2) > 6) OR (57 < (12 * ((45 + (21 * (b + d))) * 82)))))
) T1(e_l, c_l, d_l)
full join (
Select c, b, d
from p2
where (((c * 94) = d) AND ((e + (50 * (51 * (85 * (18 * (d + 41)))))) < c))
) T2(c_r, b_r, d_r)
on ((97 - d_l) > c_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r
from (
Select a, d
from p4
where (((c * ((80 + 60) + 47)) = c) OR (31 < e))
) T1(a_l, d_l)
left join (
Select c
from p4
where (7 = d)
) T2(c_r)
on (a_l < c_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_l_l, e_r_l, e_r
from (
Select c_r_l, d_l_l, e_r_l, e_r, b_r
from (
Select d_l, e_r, c_r
from (
select e, a, d
from (
Select e, a, d
from p5
where ((1 < 11) AND ((32 = (e + ((44 * 43) - 84))) AND ((28 * 13) > 76)))
) T1
union all
select e, c, a
from (
Select e, c, a, b
from p5
where ((52 - 33) = 84)
) T2
) T1(e_l, a_l, d_l)
inner join (
Select e, c
from p5
where (c < a)
) T2(e_r, c_r)
on (22 = c_r)
) T1(d_l_l, e_r_l, c_r_l)
full join (
Select e, b
from p5
where (17 < e)
) T2(e_r, b_r)
on (((b_r * 60) > 60) AND (e_r = 96))
) T1(c_r_l_l, d_l_l_l, e_r_l_l, e_r_l, b_r_l)
full join (
Select e, c, b
from p5
where ((65 = d) AND (12 > 11))
) T2(e_r, c_r, b_r)
on ((c_r_l_l > 36) OR ((e_r_l = 63) AND ((46 < e_r) OR ((e_r > (e_r_l - 33)) OR (((95 + (c_r_l_l - e_r_l)) + c_r_l_l) = e_r_l)))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test47exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, c_r, a_r
from (
Select e, d
from p4
where ((4 - b) > (16 + a))
) T1(e_l, d_l)
left join (
Select c, a
from p3
where ((73 < b) AND (97 < d))
) T2(c_r, a_r)
on (e_l < 27)
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
    #**********
    _testmgr.testcase_end(desc)

