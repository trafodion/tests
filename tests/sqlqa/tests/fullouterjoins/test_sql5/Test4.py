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
    
def test001(desc="""Joins Set 4"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select d_r_l, e_r
from (
Select a_l, d_r
from (
Select a, b
from p1
where ((d < 38) AND (b = 28))
) T1(a_l, b_l)
left join (
Select a, b, d
from p2
where ((88 - 81) = 48)
) T2(a_r, b_r, d_r)
on (a_l = ((a_l - a_l) - (d_r + 65)))
) T1(a_l_l, d_r_l)
inner join (
Select e, b
from p3
where (c = 23)
) T2(e_r, b_r)
on (e_r < 33)
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
Select c_l, d_l, e_r, b_r, d_r
from (
Select c, d
from p1
where ((((35 - b) - 91) = b) AND (d = d))
) T1(c_l, d_l)
left join (
Select e, b, d
from p5
where ((b - e) = e)
) T2(e_r, b_r, d_r)
on ((82 > 84) AND ((e_r = d_r) AND ((c_l - (50 - d_l)) > 7)))
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
Select e_l, b_l, d_l, c_r
from (
Select e, b, d
from p3
where (6 < (d - d))
) T1(e_l, b_l, d_l)
left join (
Select e, c, b, d
from p5
where (34 = d)
) T2(e_r, c_r, b_r, d_r)
on ((96 = (2 + c_r)) OR (27 = d_l))
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
Select c_l, a_l, a_r, d_r
from (
Select c, a
from p3
where ((e = (87 + 30)) AND (72 < d))
) T1(c_l, a_l)
full join (
Select a, d
from p4
where ((b = 94) AND ((81 > 28) OR (7 > 25)))
) T2(a_r, d_r)
on ((83 > 98) AND ((5 = 18) AND ((c_l < (d_r + 56)) OR ((c_l = 11) OR (a_r < 33)))))
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
Select c_r_l, b_r
from (
Select c_l, c_r
from (
Select c, a, d
from p3
where ((5 + d) > 15)
) T1(c_l, a_l, d_l)
full join (
Select e, c, d
from p1
where ((b = 41) OR (a < 56))
) T2(e_r, c_r, d_r)
on ((27 * 83) = 49)
) T1(c_l_l, c_r_l)
full join (
Select e, b, d
from p1
where (3 > 44)
) T2(e_r, b_r, d_r)
on (18 > 86)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, a_r
from (
Select d
from p3
where (76 > 28)
) T1(d_l)
inner join (
Select e, c, a
from p4
where (41 < (b + 69))
) T2(e_r, c_r, a_r)
on ((11 > 70) AND (58 = 63))
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
Select e_l, d_r
from (
select e
from (
Select e, a
from p5
where (c > c)
) T1
union all
select b
from (
Select b
from p3
where (41 = (52 - 45))
) T2
) T1(e_l)
full join (
Select a, b, d
from p3
where ((c = 43) OR ((d > 57) OR (((71 + 92) = b) OR (a = 61))))
) T2(a_r, b_r, d_r)
on (e_l < d_r)
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
Select e_r_l, d_r_r, d_r_l_r, e_l_l_r
from (
Select a_r_l, e_r
from (
Select d_l, a_r, b_r
from (
Select d
from p4
where (d < 27)
) T1(d_l)
full join (
Select a, b
from p3
where (d = 33)
) T2(a_r, b_r)
on (38 > (((a_r * 93) + a_r) * 64))
) T1(d_l_l, a_r_l, b_r_l)
full join (
select e
from (
Select e, b
from p1
where ((b * a) = 86)
) T1
union all
select b
from (
Select b
from p2
where ((e < e) AND (d > 68))
) T2
) T2(e_r)
on (a_r_l = (33 + ((95 - a_r_l) + (e_r * a_r_l))))
) T1(a_r_l_l, e_r_l)
full join (
Select e_l_l, d_r_l, e_r_l, d_r
from (
Select e_l, e_r, d_r
from (
Select e, d
from p4
where ((46 * 49) < 17)
) T1(e_l, d_l)
inner join (
Select e, c, b, d
from p2
where ((b = 93) OR (37 = 38))
) T2(e_r, c_r, b_r, d_r)
on (1 = (d_r * (((e_l * 22) * e_r) + (24 - 83))))
) T1(e_l_l, e_r_l, d_r_l)
full join (
select e, d
from (
Select e, d
from p2
where (99 = (a * c))
) T1
union all
select e, b
from (
Select e, b
from p3
where (d = b)
) T2
) T2(e_r, d_r)
on (e_l_l = e_l_l)
) T2(e_l_l_r, d_r_l_r, e_r_l_r, d_r_r)
on (94 > d_r_l_r)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l_l, e_r
from (
Select b_l, b_r, d_r
from (
Select b
from p2
where (((90 + b) - 91) = 90)
) T1(b_l)
left join (
Select b, d
from p1
where (a < 31)
) T2(b_r, d_r)
on (40 = 73)
) T1(b_l_l, b_r_l, d_r_l)
inner join (
Select e
from p3
where ((59 = c) AND ((82 = c) OR (85 = 53)))
) T2(e_r)
on ((e_r + b_l_l) = ((63 - e_r) * 34))
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
Select d_l, e_r_r
from (
Select d
from p1
where (87 = a)
) T1(d_l)
inner join (
Select a_l_l, e_r
from (
Select a_l, b_l, a_r
from (
Select a, b
from p4
where ((82 < a) OR (c = c))
) T1(a_l, b_l)
left join (
select e, c, a
from (
Select e, c, a
from p2
where ((e = b) OR ((a = e) AND (((23 - 66) = d) AND (86 > 70))))
) T1
union all
select c, a, b
from (
Select c, a, b
from p2
where (((b * e) = 79) OR (e = 73))
) T2
) T2(e_r, c_r, a_r)
on ((b_l = (a_l * a_r)) AND ((56 > (b_l + (a_r - b_l))) OR (a_l = 44)))
) T1(a_l_l, b_l_l, a_r_l)
full join (
Select e
from p2
where ((e > 39) OR ((35 = 70) OR (10 < a)))
) T2(e_r)
on ((((36 - 98) + 67) > (90 * e_r)) OR ((e_r + 29) = (a_l_l - e_r)))
) T2(a_l_l_r, e_r_r)
on ((55 * 14) = 42)
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
Select d_l_l_l, e_l_l_l, b_r
from (
Select e_l_l, d_l_l, e_r, b_r
from (
Select e_l, d_l, d_r
from (
Select e, d
from p2
where (((59 + (31 - d)) > ((c * (31 - 58)) - (a + (58 - a)))) OR (((77 + 64) + ((13 - 9) - (d - 39))) = 8))
) T1(e_l, d_l)
inner join (
Select e, d
from p3
where (((9 + d) = (b + 88)) AND (((35 + 10) = (d * b)) AND ((68 = (d * 81)) AND ((e = ((b + 51) * (20 + 39))) OR ((d < 79) OR (d < (95 * (30 * (b + (92 + (15 * 70)))))))))))
) T2(e_r, d_r)
on (d_l = 79)
) T1(e_l_l, d_l_l, d_r_l)
left join (
Select e, b
from p4
where (19 > 6)
) T2(e_r, b_r)
on ((43 = e_l_l) OR (e_l_l < (e_l_l + 88)))
) T1(e_l_l_l, d_l_l_l, e_r_l, b_r_l)
left join (
Select b
from p4
where (51 = 37)
) T2(b_r)
on (27 = 46)
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
Select e_l, d_l, e_l_r
from (
Select e, d
from p3
where (a = (((c - d) * b) * b))
) T1(e_l, d_l)
full join (
select e_l
from (
Select e_l, e_r, d_r
from (
Select e, a, b
from p3
where (a = (a + (86 - 75)))
) T1(e_l, a_l, b_l)
full join (
Select e, d
from p5
where ((14 + (c + 69)) = (9 - e))
) T2(e_r, d_r)
on (81 > d_r)
) T1
union all
select b
from (
Select b
from p1
where (81 = 26)
) T2
) T2(e_l_r)
on (e_l > (84 - e_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, c_l_r, a_r_r
from (
Select a_l, b_r
from (
Select c, a, d
from p3
where (c = c)
) T1(c_l, a_l, d_l)
inner join (
Select b
from p3
where (c = (26 - e))
) T2(b_r)
on ((74 * 32) = b_r)
) T1(a_l_l, b_r_l)
inner join (
Select c_l, a_r
from (
Select c
from p4
where (16 = d)
) T1(c_l)
left join (
Select a, b, d
from p1
where ((((56 + 2) * (53 * e)) < b) OR (61 > a))
) T2(a_r, b_r, d_r)
on (60 < c_l)
) T2(c_l_r, a_r_r)
on (c_l_r > a_r_r)
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
Select c_l, c_l_l_r, c_r_l_r
from (
select c
from (
Select c, a
from p4
where (c = (33 + a))
) T1
union all
select a
from (
Select a
from p3
where (64 = 98)
) T2
) T1(c_l)
full join (
Select c_l_l, c_r_l, b_r
from (
Select c_l, c_r
from (
Select c
from p3
where (c < ((a + 38) * 82))
) T1(c_l)
left join (
Select e, c, d
from p3
where (d < d)
) T2(e_r, c_r, d_r)
on (c_r = c_l)
) T1(c_l_l, c_r_l)
inner join (
Select e, b
from p2
where (e = 21)
) T2(e_r, b_r)
on (((c_r_l + 82) < b_r) AND (b_r < 30))
) T2(c_l_l_r, c_r_l_r, b_r_r)
on (((c_l + (c_l_l_r * c_l_l_r)) - c_l) = 52)
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
Select d_l, b_r
from (
Select d
from p1
where (81 = d)
) T1(d_l)
full join (
Select c, b
from p2
where (14 < a)
) T2(c_r, b_r)
on (((87 - d_l) = 69) OR (d_l < 91))
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
Select b_l_l, a_r_r
from (
Select b_l, c_r_r, d_l_r
from (
Select b
from p3
where (4 = 88)
) T1(b_l)
left join (
Select d_l, c_r, b_r
from (
Select d
from p2
where (27 = (b + b))
) T1(d_l)
left join (
Select c, b
from p3
where (45 > (b * ((b + 27) * d)))
) T2(c_r, b_r)
on (b_r = 84)
) T2(d_l_r, c_r_r, b_r_r)
on ((b_l = 95) OR (47 < 16))
) T1(b_l_l, c_r_r_l, d_l_r_l)
full join (
Select a_l, e_r, a_r, d_r
from (
Select a
from p3
where (e < (b + 39))
) T1(a_l)
left join (
Select e, c, a, d
from p1
where (88 > 14)
) T2(e_r, c_r, a_r, d_r)
on (36 = 84)
) T2(a_l_r, e_r_r, a_r_r, d_r_r)
on (30 = b_l_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l, a_r, b_r, d_r
from (
Select b_l_l, e_r
from (
Select c_l, b_l, b_r
from (
select c, b
from (
Select c, b
from p5
where (((31 * (65 - ((d - a) - a))) < 42) OR (((11 * 97) = 78) OR (((0 + ((c * (e + 50)) - 8)) = 65) OR ((a + (d - (c - 10))) < e))))
) T1
union all
select e, c
from (
select e, c
from (
Select e, c
from p2
where (52 > ((64 + (86 * 96)) + 69))
) T1
union all
select a_l, d_l
from (
Select a_l, d_l, e_r
from (
Select c, a, b, d
from p1
where ((0 > 2) OR (39 < 31))
) T1(c_l, a_l, b_l, d_l)
left join (
Select e
from p2
where (20 > (75 + (d * 38)))
) T2(e_r)
on ((d_l * (a_l - 48)) = d_l)
) T2
) T2
) T1(c_l, b_l)
left join (
Select b
from p3
where ((97 = (a * (d - e))) OR (41 = c))
) T2(b_r)
on (20 > b_r)
) T1(c_l_l, b_l_l, b_r_l)
full join (
Select e
from p3
where ((20 = ((38 - ((42 - (83 - e)) + 48)) - c)) AND (68 = e))
) T2(e_r)
on (e_r > e_r)
) T1(b_l_l_l, e_r_l)
left join (
Select c, a, b, d
from p1
where ((e + e) = 23)
) T2(c_r, a_r, b_r, d_r)
on ((e_r_l = 96) OR ((92 = b_r) AND (15 = 50)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_l_r
from (
Select e, a
from p4
where (57 < 8)
) T1(e_l, a_l)
left join (
select e_l
from (
Select e_l, c_l, e_r
from (
select e, c, a
from (
Select e, c, a, b
from p5
where ((a * b) < c)
) T1
union all
select e, a, b
from (
Select e, a, b
from p4
where ((d < 0) OR ((b = (18 + c)) OR (a = (c + 72))))
) T2
) T1(e_l, c_l, a_l)
left join (
select e
from (
Select e, a, d
from p4
where (37 = a)
) T1
union all
select e
from (
Select e
from p5
where ((57 > 93) OR ((44 > (((c + d) * 92) - d)) AND (e = 60)))
) T2
) T2(e_r)
on (34 < e_l)
) T1
union all
select b
from (
Select b
from p3
where (d > 75)
) T2
) T2(e_l_r)
on (e_l_r = e_l_r)
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
Select c_l, c_r
from (
Select c
from p5
where (23 = a)
) T1(c_l)
full join (
select c
from (
Select c
from p4
where (e > (e - c))
) T1
union all
select e
from (
Select e, b
from p2
where (e = c)
) T2
) T2(c_r)
on (c_l < (((77 * 30) - 88) - c_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test04exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, d_r
from (
Select d
from p5
where ((12 - 16) = 48)
) T1(d_l)
left join (
Select d
from p4
where (c = 82)
) T2(d_r)
on ((9 = (d_r * (d_l - 47))) AND (39 = d_r))
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
    #**********************************************
    _testmgr.testcase_end(desc)

