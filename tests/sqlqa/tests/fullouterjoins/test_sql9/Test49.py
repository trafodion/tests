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
    
def test001(desc="""Joins Set 49"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, a_r_r_l, c_r
from (
Select e_l, c_l, b_l, a_r_r
from (
Select e, c, b
from p2
where ((36 > 82) AND (((66 - a) > (5 * (d - ((27 - c) + a)))) AND (b = d)))
) T1(e_l, c_l, b_l)
full join (
Select c_r_l_l_l, a_r
from (
Select c_r_l_l, d_r
from (
Select c_r_l, d_r
from (
Select d_r_r_l, a_r_l_l, c_r, a_r
from (
Select a_r_l, d_r_r
from (
Select a_l, a_r
from (
Select e, a, d
from p2
where ((a = b) AND (3 > ((56 * 41) * 76)))
) T1(e_l, a_l, d_l)
inner join (
select a
from (
Select a
from p5
where (c < d)
) T1
union all
select b_l
from (
Select b_l, b_r, d_r
from (
Select b
from p3
where ((80 > 86) OR (52 = c))
) T1(b_l)
inner join (
Select b, d
from p4
where ((70 = 6) OR (0 = 88))
) T2(b_r, d_r)
on (b_r < 2)
) T2
) T2(a_r)
on ((a_r - a_r) = 69)
) T1(a_l_l, a_r_l)
full join (
Select e_l, a_r, d_r
from (
select e
from (
Select e, c, d
from p3
where ((a < ((c + 34) - 84)) AND ((69 > 25) AND ((40 > 64) AND (71 = 54))))
) T1
union all
select a
from (
Select a
from p3
where (23 > 74)
) T2
) T1(e_l)
left join (
Select a, d
from p1
where (97 > 8)
) T2(a_r, d_r)
on ((30 = (a_r + d_r)) OR (25 > a_r))
) T2(e_l_r, a_r_r, d_r_r)
on ((45 * a_r_l) = ((d_r_r - ((65 + 99) * 67)) + a_r_l))
) T1(a_r_l_l, d_r_r_l)
left join (
Select c, a, d
from p1
where ((d = c) OR ((d + 44) < c))
) T2(c_r, a_r, d_r)
on ((43 < (62 + c_r)) AND ((84 = 97) OR (((10 - (82 - (97 * 97))) > a_r) OR (77 > 90))))
) T1(d_r_r_l_l, a_r_l_l_l, c_r_l, a_r_l)
inner join (
Select b, d
from p3
where (55 = 10)
) T2(b_r, d_r)
on ((35 + 13) = d_r)
) T1(c_r_l_l, d_r_l)
left join (
Select d
from p1
where (b < 4)
) T2(d_r)
on (d_r < (46 + d_r))
) T1(c_r_l_l_l, d_r_l)
inner join (
Select e, a
from p3
where (e < 89)
) T2(e_r, a_r)
on (a_r < (88 + 69))
) T2(c_r_l_l_l_r, a_r_r)
on ((97 + c_l) = e_l)
) T1(e_l_l, c_l_l, b_l_l, a_r_r_l)
left join (
Select c
from p4
where (14 > d)
) T2(c_r)
on (61 = (c_r * (2 * 97)))
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
Select e_l, a_l, e_r
from (
Select e, a, b
from p2
where (d = 69)
) T1(e_l, a_l, b_l)
left join (
Select e, c, a, b
from p1
where (74 > b)
) T2(e_r, c_r, a_r, b_r)
on ((e_r * (e_l + e_l)) > e_l)
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
Select c_l_l, a_l_r, e_l_r
from (
select e_l, c_l, a_r
from (
Select e_l, c_l, a_r
from (
Select e, c, b
from p4
where ((15 * 98) = a)
) T1(e_l, c_l, b_l)
full join (
select a
from (
select a
from (
Select a, d
from p3
where (39 < 79)
) T1
union all
select c
from (
Select c
from p4
where ((b = a) AND ((34 > d) OR ((67 = (e + 47)) OR ((4 * (70 * 66)) = a))))
) T2
) T1
union all
select e
from (
Select e, a, b, d
from p5
where (54 < 12)
) T2
) T2(a_r)
on (e_l = 72)
) T1
union all
select a, b, d
from (
Select a, b, d
from p5
where ((((e - 82) - e) = a) AND (c = (31 - e)))
) T2
) T1(e_l_l, c_l_l, a_r_l)
left join (
Select e_l, a_l, e_l_r, c_r_r
from (
Select e, c, a
from p3
where ((b > c) OR (((a * e) = c) OR ((a < 23) OR ((c > 60) AND (a = a)))))
) T1(e_l, c_l, a_l)
left join (
Select e_l, c_r
from (
Select e
from p1
where (40 = 53)
) T1(e_l)
full join (
Select c
from p3
where ((36 - c) = 17)
) T2(c_r)
on ((40 - (e_l - 99)) = 24)
) T2(e_l_r, c_r_r)
on ((23 * c_r_r) > e_l)
) T2(e_l_r, a_l_r, e_l_r_r, c_r_r_r)
on (41 = 80)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_l, e_r, b_r, d_r
from (
Select a, b, d
from p2
where ((d = 50) OR ((e = e) OR (39 > 15)))
) T1(a_l, b_l, d_l)
full join (
Select e, c, b, d
from p1
where ((d = (49 + 45)) AND ((65 - (d * (76 - 39))) < 1))
) T2(e_r, c_r, b_r, d_r)
on ((53 - b_r) = e_r)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, b_l_r
from (
Select b_l, d_l, e_r, c_r, d_r
from (
Select e, b, d
from p2
where (b = a)
) T1(e_l, b_l, d_l)
left join (
Select e, c, d
from p5
where (d > d)
) T2(e_r, c_r, d_r)
on ((98 - d_r) = d_r)
) T1(b_l_l, d_l_l, e_r_l, c_r_l, d_r_l)
full join (
Select b_l, e_r
from (
Select c, a, b
from p5
where (77 > 6)
) T1(c_l, a_l, b_l)
left join (
select e
from (
Select e
from p4
where (d = d)
) T1
union all
select e_l
from (
Select e_l, a_l, e_r, d_r
from (
Select e, a
from p3
where (83 = a)
) T1(e_l, a_l)
inner join (
Select e, d
from p1
where (c < a)
) T2(e_r, d_r)
on ((e_l = e_l) OR ((63 < 41) OR (15 = 17)))
) T2
) T2(e_r)
on ((44 - 32) < b_l)
) T2(b_l_r, e_r_r)
on (4 = 34)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, d_r
from (
Select e
from p4
where (b = d)
) T1(e_l)
left join (
Select e, c, d
from p4
where (((53 * c) + 10) > 17)
) T2(e_r, c_r, d_r)
on (14 = e_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_r, d_r
from (
Select c
from p2
where (((92 * 61) = 84) AND (98 = 75))
) T1(c_l)
left join (
Select e, d
from p4
where ((83 = d) OR ((58 > 25) OR ((77 + 14) < 31)))
) T2(e_r, d_r)
on (e_r < (e_r * 82))
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
Select c_l, d_l, c_r
from (
Select c, a, d
from p1
where ((77 = 52) OR (e < 58))
) T1(c_l, a_l, d_l)
left join (
Select c
from p4
where (4 < 43)
) T2(c_r)
on ((d_l = c_l) OR (c_r = 86))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, d_l_l_r, c_r_l_r
from (
Select d_l, c_r, b_r
from (
Select d
from p5
where ((d = (e - c)) OR (45 < 65))
) T1(d_l)
left join (
select c, b
from (
Select c, b
from p5
where (e = d)
) T1
union all
select e_l, a_l_l_r
from (
Select e_l, a_l_l_r, c_r_r
from (
Select e
from p1
where (a = b)
) T1(e_l)
left join (
select a_l_l, c_r
from (
Select a_l_l, c_r, a_r
from (
select a_l, d_l_l_l_r
from (
Select a_l, d_l_l_l_r, a_r_l_r
from (
Select a
from p2
where ((97 + (30 * (5 * c))) = a)
) T1(a_l)
inner join (
Select d_l_l_l, a_r_l, a_r_l_l, b_r_r, d_r_r
from (
Select a_r_l, d_l_l, a_r, d_r
from (
Select d_l, a_r
from (
Select e, b, d
from p5
where (d > 21)
) T1(e_l, b_l, d_l)
left join (
Select a
from p1
where (a < 13)
) T2(a_r)
on (5 = d_l)
) T1(d_l_l, a_r_l)
full join (
Select a, d
from p4
where ((21 > c) OR (a = 42))
) T2(a_r, d_r)
on (18 = a_r)
) T1(a_r_l_l, d_l_l_l, a_r_l, d_r_l)
full join (
Select a_l, b_r, d_r
from (
Select a, d
from p2
where (66 = a)
) T1(a_l, d_l)
inner join (
Select b, d
from p3
where (((86 * 75) > 5) OR (c = 28))
) T2(b_r, d_r)
on ((9 = 67) AND (((a_l * a_l) = a_l) AND ((a_l > a_l) OR (67 < ((a_l - a_l) - (85 + a_l))))))
) T2(a_l_r, b_r_r, d_r_r)
on ((27 > 74) AND (a_r_l_l = 85))
) T2(d_l_l_l_r, a_r_l_r, a_r_l_l_r, b_r_r_r, d_r_r_r)
on (a_l > (((48 - d_l_l_l_r) + d_l_l_l_r) - d_l_l_l_r))
) T1
union all
select e, d
from (
Select e, d
from p4
where (38 = b)
) T2
) T1(a_l_l, d_l_l_l_r_l)
inner join (
Select e, c, a
from p3
where ((6 = b) AND ((a > a) OR (b = 54)))
) T2(e_r, c_r, a_r)
on ((89 + (51 * 92)) > 65)
) T1
union all
select a_l, e_r
from (
Select a_l, e_r
from (
select a, b, d
from (
Select a, b, d
from p4
where (1 = e)
) T1
union all
select a_l, d_l, d_r_r
from (
Select a_l, d_l, d_r_r, a_l_l_r
from (
Select a, d
from p1
where (d < 4)
) T1(a_l, d_l)
left join (
Select a_l_l, d_l_l, e_r_l, d_r
from (
Select a_l, d_l, e_r, a_r
from (
Select a, d
from p3
where ((63 > b) OR (c > 38))
) T1(a_l, d_l)
left join (
select e, a
from (
Select e, a, d
from p2
where ((62 = a) AND ((d < a) AND (d = 57)))
) T1
union all
select e, c
from (
Select e, c
from p4
where (d > d)
) T2
) T2(e_r, a_r)
on (29 < e_r)
) T1(a_l_l, d_l_l, e_r_l, a_r_l)
left join (
select a, d
from (
Select a, d
from p3
where (94 < 68)
) T1
union all
select e, c
from (
Select e, c, b, d
from p1
where (a = (e * e))
) T2
) T2(a_r, d_r)
on (a_l_l < 61)
) T2(a_l_l_r, d_l_l_r, e_r_l_r, d_r_r)
on (a_l < (88 * d_r_r))
) T2
) T1(a_l, b_l, d_l)
inner join (
Select e
from p4
where ((23 = 56) OR ((42 - 95) = a))
) T2(e_r)
on (e_r = (e_r - 74))
) T2
) T2(a_l_l_r, c_r_r)
on ((a_l_l_r = (43 - (87 * 33))) AND ((c_r_r < 81) AND (10 > e_l)))
) T2
) T2(c_r, b_r)
on (b_r = (((79 + 37) * 41) - 64))
) T1(d_l_l, c_r_l, b_r_l)
inner join (
Select c_r_l, d_l_l, a_l_r
from (
Select d_l, c_r
from (
Select b, d
from p2
where (((e * 65) - 41) < 24)
) T1(b_l, d_l)
left join (
Select c
from p1
where (c = 89)
) T2(c_r)
on (14 = d_l)
) T1(d_l_l, c_r_l)
inner join (
Select a_l, b_r
from (
Select e, c, a, d
from p4
where (((6 - 41) = b) AND ((75 > c) OR ((56 > 44) AND (84 = 74))))
) T1(e_l, c_l, a_l, d_l)
full join (
Select c, b, d
from p3
where ((b = 55) OR (93 = 55))
) T2(c_r, b_r, d_r)
on ((79 = 79) AND (54 > a_l))
) T2(a_l_r, b_r_r)
on (d_l_l > 75)
) T2(c_r_l_r, d_l_l_r, a_l_r_r)
on ((((93 - 43) + 48) = 34) OR (37 < d_l_l_r))
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
Select c_l_l, e_l_l, c_r
from (
select e_l, c_l, a_l, d_r_r
from (
Select e_l, c_l, a_l, d_r_r, b_l_r
from (
Select e, c, a, b
from p2
where ((1 + a) < b)
) T1(e_l, c_l, a_l, b_l)
inner join (
Select b_l, d_l, a_r, d_r
from (
Select b, d
from p5
where ((((b * (22 - 75)) * a) > b) AND ((a < 51) OR (89 > d)))
) T1(b_l, d_l)
left join (
Select a, d
from p1
where (4 > 66)
) T2(a_r, d_r)
on (97 = 99)
) T2(b_l_r, d_l_r, a_r_r, d_r_r)
on ((((a_l + 88) + (a_l + 37)) < b_l_r) AND (((e_l - 12) < e_l) OR ((36 < 77) OR ((d_r_r - 35) = e_l))))
) T1
union all
select e, c, a, b
from (
Select e, c, a, b
from p4
where (c > 69)
) T2
) T1(e_l_l, c_l_l, a_l_l, d_r_r_l)
left join (
select c
from (
Select c
from p1
where ((81 > e) AND ((90 = c) OR ((74 * e) = (6 * 40))))
) T1
union all
select e_l
from (
Select e_l, b_l, a_l_r, c_l_r_r
from (
Select e, b
from p3
where (95 < (26 + 0))
) T1(e_l, b_l)
inner join (
Select a_l, c_l_r, b_r_r
from (
Select a
from p2
where ((c * 17) = e)
) T1(a_l)
left join (
Select c_l, b_r
from (
Select c
from p2
where (((e - d) = 97) AND (46 = a))
) T1(c_l)
full join (
select e, b
from (
select e, b
from (
Select e, b, d
from p3
where (66 = c)
) T1
union all
select e, b
from (
Select e, b
from p4
where ((a = e) AND (e > c))
) T2
) T1
union all
select e_l, a_l_r
from (
Select e_l, a_l_r
from (
Select e, b
from p3
where ((a > d) AND (70 = a))
) T1(e_l, b_l)
left join (
Select a_l, e_l_r, b_l_r
from (
Select a
from p4
where ((66 > b) OR ((91 + d) = 59))
) T1(a_l)
left join (
Select e_l, a_l, b_l, c_r, b_r
from (
Select e, a, b
from p5
where ((a = a) AND (13 = 8))
) T1(e_l, a_l, b_l)
inner join (
Select c, b
from p5
where ((64 > c) AND (21 = (e + 79)))
) T2(c_r, b_r)
on (b_l = 10)
) T2(e_l_r, a_l_r, b_l_r, c_r_r, b_r_r)
on ((e_l_r = (58 - (66 - b_l_r))) AND (72 < a_l))
) T2(a_l_r, e_l_r_r, b_l_r_r)
on (23 > 32)
) T2
) T2(e_r, b_r)
on (85 = 32)
) T2(c_l_r, b_r_r)
on ((49 - 10) > 92)
) T2(a_l_r, c_l_r_r, b_r_r_r)
on (b_l < 72)
) T2
) T2(c_r)
on (e_l_l < c_r)
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
Select e, c, b
from p1
where (d > 76)
) T1(e_l, c_l, b_l)
left join (
select c
from (
Select c, a, b, d
from p5
where ((69 + (34 - b)) = b)
) T1
union all
select e
from (
select e
from (
Select e
from p1
where ((((d + a) + c) = 43) OR ((40 + 76) = c))
) T1
union all
select c
from (
Select c, b
from p2
where (42 = c)
) T2
) T2
) T2(c_r)
on (((e_l - 38) < 82) OR (c_r = 12))
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
Select d_l, b_r
from (
Select a, d
from p4
where ((b > d) AND (67 < 57))
) T1(a_l, d_l)
left join (
Select b
from p3
where (a = 40)
) T2(b_r)
on (b_r = 16)
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
Select c_l, b_l, a_r
from (
Select c, b
from p4
where (53 = b)
) T1(c_l, b_l)
left join (
Select a
from p5
where (((28 + 66) < 89) AND ((a < b) OR (76 < ((c - a) - 37))))
) T2(a_r)
on (c_l < 64)
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
Select c_l, e_r, a_r
from (
Select c
from p2
where (13 > ((99 + c) - (35 * d)))
) T1(c_l)
left join (
Select e, a
from p5
where (64 < e)
) T2(e_r, a_r)
on (a_r = (c_l - e_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_l, c_r, b_r
from (
Select e, c
from p5
where (d = c)
) T1(e_l, c_l)
left join (
Select c, b
from p4
where ((((b * ((e + b) * c)) * 58) = 52) AND (a < c))
) T2(c_r, b_r)
on ((13 > b_r) OR ((c_l > ((27 + 69) + 36)) AND (c_r = 5)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_r
from (
Select e
from p4
where (94 < 76)
) T1(e_l)
left join (
Select b
from p1
where ((b < 81) OR ((e < 8) AND ((24 > 65) OR (88 > (99 + 42)))))
) T2(b_r)
on (e_l = 6)
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
Select e_r_l, e_r_l_l_r, a_r_l_r
from (
Select a_l, e_r
from (
Select a
from p5
where (c = a)
) T1(a_l)
left join (
select e
from (
Select e, b
from p1
where ((52 > e) AND (22 = 99))
) T1
union all
select a
from (
Select a
from p4
where ((82 * d) < 71)
) T2
) T2(e_r)
on (a_l < a_l)
) T1(a_l_l, e_r_l)
left join (
Select a_r_l, e_r_l_l, e_r_r
from (
Select e_r_l, a_r
from (
Select c_l, b_l, e_r, c_r
from (
Select c, a, b, d
from p2
where (26 < 21)
) T1(c_l, a_l, b_l, d_l)
full join (
Select e, c
from p5
where (((c * b) = 9) OR ((c = 20) OR (89 > 26)))
) T2(e_r, c_r)
on ((88 - (51 + c_l)) > 71)
) T1(c_l_l, b_l_l, e_r_l, c_r_l)
left join (
Select a
from p2
where ((97 = 80) OR (((33 + b) + c) = 61))
) T2(a_r)
on ((e_r_l > e_r_l) OR ((62 = 2) OR (62 > a_r)))
) T1(e_r_l_l, a_r_l)
inner join (
select b_l, e_r
from (
Select b_l, e_r, c_r
from (
Select b
from p4
where ((a = 40) AND ((70 < (((e - a) * 31) - a)) AND (85 = 32)))
) T1(b_l)
inner join (
Select e, c, a
from p2
where (96 = 76)
) T2(e_r, c_r, a_r)
on (58 = 91)
) T1
union all
select c, a
from (
Select c, a
from p4
where ((56 > b) OR ((b = (d * c)) OR ((b = 38) OR (69 = e))))
) T2
) T2(b_l_r, e_r_r)
on ((e_r_r > 29) AND (e_r_l_l = 88))
) T2(a_r_l_r, e_r_l_l_r, e_r_r_r)
on ((87 + e_r_l_l_r) > a_r_l_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test49exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_r_l, c_l_r, e_l_r
from (
Select a_l, b_l, e_l_r, e_r_r
from (
Select a, b
from p4
where (b = 75)
) T1(a_l, b_l)
left join (
Select e_l, a_l, d_l, e_r, a_r, d_r
from (
Select e, a, d
from p5
where (c > e)
) T1(e_l, a_l, d_l)
left join (
Select e, a, d
from p2
where (c > 39)
) T2(e_r, a_r, d_r)
on (38 < (e_r * a_l))
) T2(e_l_r, a_l_r, d_l_r, e_r_r, a_r_r, d_r_r)
on ((e_l_r = e_r_r) AND (53 = e_l_r))
) T1(a_l_l, b_l_l, e_l_r_l, e_r_r_l)
left join (
Select e_l, c_l, d_r
from (
Select e, c
from p3
where (c = c)
) T1(e_l, c_l)
left join (
Select e, b, d
from p2
where ((e = 90) AND ((a < a) OR (d > 27)))
) T2(e_r, b_r, d_r)
on (62 = e_l)
) T2(e_l_r, c_l_r, d_r_r)
on ((30 > e_l_r) OR ((42 = 42) OR (e_r_r_l = e_r_r_l)))
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
Select c_l_l, a_r_l, d_r
from (
Select c_l, b_l, d_l, a_r
from (
Select c, b, d
from p4
where (85 < ((((20 - (a * (a + d))) + 57) - ((b - e) - b)) + 82))
) T1(c_l, b_l, d_l)
inner join (
Select a
from p2
where (34 = c)
) T2(a_r)
on (a_r = d_l)
) T1(c_l_l, b_l_l, d_l_l, a_r_l)
left join (
Select d
from p4
where ((96 < (24 * 58)) AND ((49 - 41) > 91))
) T2(d_r)
on (24 = c_l_l)
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
Select d_l, e_r
from (
Select d
from p4
where ((58 = a) OR (e < b))
) T1(d_l)
left join (
Select e
from p2
where (((8 - d) = e) AND (a < 45))
) T2(e_r)
on ((e_r > (e_r + (d_l * e_r))) AND (14 > (58 + e_r)))
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
    #********************************
    _testmgr.testcase_end(desc)

