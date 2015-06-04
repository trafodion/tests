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
    
def test001(desc="""Joins Set 29"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l_r
from (
Select c
from p1
where (b = (d - 72))
) T1(c_l)
full join (
Select a_l, a_r, b_r
from (
Select a
from p1
where (27 = 68)
) T1(a_l)
full join (
Select e, a, b
from p4
where ((28 = 77) OR (45 > c))
) T2(e_r, a_r, b_r)
on (b_r < 69)
) T2(a_l_r, a_r_r, b_r_r)
on ((c_l + a_l_r) = a_l_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, a_r
from (
Select d
from p2
where ((c = 87) AND ((b * b) = (a - 41)))
) T1(d_l)
full join (
Select a
from p3
where (d = 32)
) T2(a_r)
on (5 > 29)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r
from (
Select e, d
from p5
where ((98 > 76) AND (c = 73))
) T1(e_l, d_l)
full join (
Select e, c, b
from p1
where (((59 - (c + 99)) > d) OR (1 < 96))
) T2(e_r, c_r, b_r)
on ((60 < c_r) AND (52 > 43))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r
from (
Select d
from p4
where (14 > b)
) T1(d_l)
inner join (
select e, c, b
from (
Select e, c, b
from p2
where ((a < a) OR (e < (a - a)))
) T1
union all
select e_l_l, a_r_l, a_l_r_r
from (
Select e_l_l, a_r_l, a_l_r_r, e_l_r
from (
Select e_l, a_r
from (
Select e
from p3
where (b = d)
) T1(e_l)
full join (
Select a
from p1
where ((a > 49) AND (d < b))
) T2(a_r)
on ((a_r + (47 + 32)) = (38 - e_l))
) T1(e_l_l, a_r_l)
left join (
select e_l, c_l, a_l_r
from (
Select e_l, c_l, a_l_r, b_r_r
from (
Select e, c
from p3
where (b > 33)
) T1(e_l, c_l)
inner join (
Select a_l, b_r
from (
Select a
from p5
where (78 > a)
) T1(a_l)
full join (
select b
from (
Select b
from p4
where (36 > 94)
) T1
union all
select e
from (
select e, c
from (
Select e, c
from p3
where ((63 - d) > e)
) T1
union all
select e, c
from (
select e, c
from (
Select e, c
from p5
where (d = b)
) T1
union all
select b, d
from (
Select b, d
from p5
where ((b = 51) OR (55 = b))
) T2
) T2
) T2
) T2(b_r)
on (b_r = (66 * a_l))
) T2(a_l_r, b_r_r)
on (31 = 32)
) T1
union all
select e_l, e_r, a_r
from (
Select e_l, e_r, a_r
from (
select e
from (
Select e, a, d
from p1
where ((d = c) AND (c = a))
) T1
union all
select c
from (
Select c
from p3
where (0 = 84)
) T2
) T1(e_l)
inner join (
Select e, a
from p1
where (72 = (38 + 97))
) T2(e_r, a_r)
on (((30 * (26 * 44)) > ((e_l * 86) - 45)) OR ((a_r = e_l) AND ((a_r - 85) < a_r)))
) T2
) T2(e_l_r, c_l_r, a_l_r_r)
on (e_l_r > a_r_l)
) T2
) T2(e_r, c_r, b_r)
on ((89 = 80) OR ((39 = b_r) OR ((b_r + 38) = 89)))
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
Select a_l_l, e_l_l, c_r, d_r
from (
Select e_l, a_l, d_l, a_l_r_r, c_l_l_l_r
from (
Select e, a, d
from p4
where ((2 < d) AND ((b = (8 * ((14 + c) + ((9 + d) * ((91 + a) + 28))))) AND (c = 43)))
) T1(e_l, a_l, d_l)
left join (
Select c_l_l_l, a_r_l, a_l_r
from (
Select c_l_l, c_r_l, a_r
from (
Select c_l, a_l, e_r, c_r
from (
Select c, a, d
from p3
where ((c = 74) AND (((a + 89) - a) = c))
) T1(c_l, a_l, d_l)
left join (
Select e, c, a, d
from p4
where (12 < 15)
) T2(e_r, c_r, a_r, d_r)
on ((c_r = a_l) AND (e_r = c_r))
) T1(c_l_l, a_l_l, e_r_l, c_r_l)
left join (
Select a
from p5
where (45 < 57)
) T2(a_r)
on ((77 - a_r) = 97)
) T1(c_l_l_l, c_r_l_l, a_r_l)
left join (
Select e_l, a_l, e_r
from (
Select e, a
from p1
where (e < 93)
) T1(e_l, a_l)
inner join (
select e, c, a
from (
Select e, c, a, b
from p2
where (((94 * 50) < 92) AND (a = b))
) T1
union all
select c, a, b
from (
Select c, a, b
from p1
where (15 < 55)
) T2
) T2(e_r, c_r, a_r)
on (e_l = 8)
) T2(e_l_r, a_l_r, e_r_r)
on (61 > (12 * (23 + (12 - a_l_r))))
) T2(c_l_l_l_r, a_r_l_r, a_l_r_r)
on (a_l = a_l_r_r)
) T1(e_l_l, a_l_l, d_l_l, a_l_r_r_l, c_l_l_l_r_l)
left join (
Select c, d
from p5
where (91 = 8)
) T2(c_r, d_r)
on ((85 > c_r) AND (17 > 58))
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
Select d_l, a_r
from (
Select c, a, d
from p5
where (78 < 5)
) T1(c_l, a_l, d_l)
left join (
Select e, a, b
from p3
where ((59 + b) = 5)
) T2(e_r, a_r, b_r)
on (a_r = a_r)
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
Select c_l_l, a_r_l, a_l_r, e_r_r
from (
Select c_l, a_r, d_r
from (
select e, c
from (
Select e, c, a, b
from p4
where ((98 < 2) OR (((d * 34) - 64) > c))
) T1
union all
select b, d
from (
Select b, d
from p5
where ((a = 97) OR ((4 = b) OR (((b * a) = 73) OR (36 = 31))))
) T2
) T1(e_l, c_l)
inner join (
Select a, d
from p5
where ((d * (c * (57 + e))) = 98)
) T2(a_r, d_r)
on (a_r = c_l)
) T1(c_l_l, a_r_l, d_r_l)
left join (
Select a_l, e_r
from (
select a
from (
Select a, d
from p5
where (26 > b)
) T1
union all
select b
from (
Select b
from p5
where (44 = (12 - 15))
) T2
) T1(a_l)
inner join (
Select e, c
from p3
where ((42 + 70) = d)
) T2(e_r, c_r)
on (0 < e_r)
) T2(a_l_r, e_r_r)
on (38 = e_r_r)
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
Select a_r_l, e_l_r, c_r_r
from (
select c_l, a_r, d_r
from (
Select c_l, a_r, d_r
from (
Select c
from p5
where (44 > c)
) T1(c_l)
left join (
Select a, d
from p2
where (((40 * 95) = b) AND (((39 - b) = (a + 44)) OR ((43 - (d * 96)) < 4)))
) T2(a_r, d_r)
on (c_l = 39)
) T1
union all
select e, a, b
from (
Select e, a, b
from p4
where ((52 < d) AND ((a = (e - (c - b))) AND (26 = c)))
) T2
) T1(c_l_l, a_r_l, d_r_l)
full join (
Select e_l, c_r
from (
Select e
from p2
where (3 > c)
) T1(e_l)
left join (
Select c, b
from p5
where ((67 = (90 + 14)) AND (97 < 83))
) T2(c_r, b_r)
on ((77 > (77 + 85)) OR (77 = c_r))
) T2(e_l_r, c_r_r)
on (c_r_r < (a_r_l + c_r_r))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_l_r_r_r, e_l_r_r, b_l_r
from (
Select d
from p5
where (a = b)
) T1(d_l)
full join (
Select b_l, e_l_r, e_l_r_r
from (
Select a, b
from p2
where (b = (d + e))
) T1(a_l, b_l)
full join (
Select e_l, c_l, d_l, e_l_r
from (
Select e, c, d
from p1
where (c < (e - 52))
) T1(e_l, c_l, d_l)
inner join (
Select e_l, d_l, d_l_l_l_r, a_r_l_r
from (
Select e, d
from p1
where (a < c)
) T1(e_l, d_l)
left join (
Select d_l_l_l, a_r_l, d_r
from (
Select c_l_l, d_l_l, a_r
from (
Select c_l, d_l, b_r
from (
Select c, b, d
from p1
where ((((7 + 46) * c) = e) OR (e < c))
) T1(c_l, b_l, d_l)
full join (
Select b, d
from p5
where (10 = 22)
) T2(b_r, d_r)
on ((b_r > 14) AND ((15 - 34) > 89))
) T1(c_l_l, d_l_l, b_r_l)
full join (
Select a
from p2
where ((14 = (11 - b)) AND (e > 35))
) T2(a_r)
on (56 = a_r)
) T1(c_l_l_l, d_l_l_l, a_r_l)
left join (
select d
from (
Select d
from p2
where ((82 * 64) < a)
) T1
union all
select e_l
from (
select e_l
from (
select e_l
from (
Select e_l, a_l, a_r, b_r
from (
select e, a
from (
Select e, a
from p3
where ((c + d) = c)
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, e_r, a_r
from (
Select c, b, d
from p3
where (((12 * 9) * (14 + (e * (d - (27 + (b * e)))))) > c)
) T1(c_l, b_l, d_l)
left join (
Select e, c, a
from p5
where (71 = 13)
) T2(e_r, c_r, a_r)
on (74 > (e_r * a_r))
) T2
) T1(e_l, a_l)
inner join (
Select c, a, b
from p4
where ((49 < ((83 - 15) - e)) AND ((51 > 90) AND ((d = a) AND (b = ((d - ((e * d) * d)) - 34)))))
) T2(c_r, a_r, b_r)
on ((77 > b_r) OR (16 = 68))
) T1
union all
select e
from (
Select e
from p1
where (26 = 11)
) T2
) T1
union all
select e
from (
Select e, c, a
from p5
where ((b < e) OR ((41 > d) OR (17 < (40 + a))))
) T2
) T2
) T2(d_r)
on ((44 < 56) AND ((83 = a_r_l) AND (37 > d_r)))
) T2(d_l_l_l_r, a_r_l_r, d_r_r)
on (d_l = ((48 + (e_l * 22)) + 61))
) T2(e_l_r, d_l_r, d_l_l_l_r_r, a_r_l_r_r)
on ((91 = 30) AND ((68 + 20) = e_l))
) T2(e_l_r, c_l_r, d_l_r, e_l_r_r)
on (62 = e_l_r)
) T2(b_l_r, e_l_r_r, e_l_r_r_r)
on (e_l_r_r > d_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r
from (
Select a
from p2
where (47 = d)
) T1(a_l)
full join (
select d
from (
Select d
from p4
where (75 > d)
) T1
union all
select e
from (
Select e, a, b
from p1
where ((49 < 4) OR (b < e))
) T2
) T2(d_r)
on ((d_r = 55) OR ((9 = 25) AND (a_l = 18)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_r_r, b_l_r
from (
Select c
from p5
where (57 < c)
) T1(c_l)
left join (
Select a_l, b_l, a_r
from (
Select a, b, d
from p5
where (a > d)
) T1(a_l, b_l, d_l)
inner join (
Select a
from p4
where ((((98 - (35 + (d + 90))) * a) - c) > a)
) T2(a_r)
on (a_r = a_l)
) T2(a_l_r, b_l_r, a_r_r)
on ((a_r_r > a_r_r) OR (b_l_r > c_l))
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
Select b_l, b_r
from (
select b
from (
Select b
from p5
where ((c = d) OR (53 < e))
) T1
union all
select c_l
from (
Select c_l, a_l, b_r, d_r
from (
select c, a
from (
Select c, a
from p2
where (a < c)
) T1
union all
select e, c
from (
Select e, c, d
from p5
where ((17 < 10) AND (d = (((87 + (17 * b)) * 91) + d)))
) T2
) T1(c_l, a_l)
left join (
Select b, d
from p1
where (c = b)
) T2(b_r, d_r)
on (((89 + 94) = b_r) AND (c_l < d_r))
) T2
) T1(b_l)
left join (
Select c, b
from p3
where ((69 * (73 * b)) = c)
) T2(c_r, b_r)
on (2 < b_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_r_l, e_r, c_r, d_r
from (
Select e_l, e_r_r
from (
Select e
from p4
where (4 = 81)
) T1(e_l)
left join (
Select e_l_l, a_r_l, e_r_l, e_r
from (
select e_l, e_r, a_r
from (
Select e_l, e_r, a_r
from (
select e
from (
Select e
from p4
where (((c + (a + (e * a))) * c) = 79)
) T1
union all
select e_l
from (
select e_l, b_l, d_r
from (
Select e_l, b_l, d_r
from (
Select e, c, b
from p5
where (95 = 69)
) T1(e_l, c_l, b_l)
left join (
Select d
from p3
where (76 > 7)
) T2(d_r)
on ((35 > e_l) OR (81 = (e_l - 27)))
) T1
union all
select e, c, a
from (
Select e, c, a, d
from p1
where ((84 * ((61 - c) - a)) < 72)
) T2
) T2
) T1(e_l)
full join (
Select e, a
from p4
where (((e * d) = a) AND (27 = (c + 52)))
) T2(e_r, a_r)
on (((46 * 28) = 66) OR (77 = (e_l + 34)))
) T1
union all
select e, c, a
from (
Select e, c, a, d
from p2
where ((10 < 38) OR (a = 85))
) T2
) T1(e_l_l, e_r_l, a_r_l)
inner join (
Select e, c, b, d
from p2
where (90 = 4)
) T2(e_r, c_r, b_r, d_r)
on ((89 - e_l_l) < 28)
) T2(e_l_l_r, a_r_l_r, e_r_l_r, e_r_r)
on (67 = 95)
) T1(e_l_l, e_r_r_l)
left join (
Select e, c, d
from p5
where ((24 - a) = e)
) T2(e_r, c_r, d_r)
on ((e_r > d_r) OR (e_r < 98))
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
Select d_l, c_r
from (
Select d
from p2
where (47 = d)
) T1(d_l)
left join (
Select c, b
from p2
where (((96 - d) > (b + e)) OR (c > c))
) T2(c_r, b_r)
on ((c_r = 85) OR (95 = c_r))
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
Select a_l, c_r_r_r_r_r
from (
Select a
from p4
where (a = a)
) T1(a_l)
full join (
Select d_l, e_l_r_r_r, c_r_r_r_r, e_l_l_r
from (
Select a, b, d
from p3
where ((c * e) < ((e * a) * 28))
) T1(a_l, b_l, d_l)
inner join (
Select e_l_l, c_l_r, c_r_r_r, e_l_r_r
from (
select e_l
from (
Select e_l, b_r
from (
Select e
from p3
where (61 < a)
) T1(e_l)
left join (
Select e, a, b
from p4
where (68 = 38)
) T2(e_r, a_r, b_r)
on (b_r < b_r)
) T1
union all
select e
from (
Select e
from p3
where ((73 - (95 * (54 - 53))) = d)
) T2
) T1(e_l_l)
inner join (
Select c_l, b_l, e_l_r, c_r_r, d_l_r
from (
Select c, b
from p2
where ((e = (a - e)) AND (a = 14))
) T1(c_l, b_l)
inner join (
Select e_l, c_l, b_l, d_l, c_r
from (
Select e, c, b, d
from p3
where ((54 + 76) = 53)
) T1(e_l, c_l, b_l, d_l)
inner join (
select c
from (
select c
from (
Select c
from p1
where ((13 > d) OR ((33 = e) AND (20 > a)))
) T1
union all
select e
from (
Select e, c
from p4
where ((e < 18) OR (e > c))
) T2
) T1
union all
select e
from (
Select e, d
from p4
where (d = a)
) T2
) T2(c_r)
on ((d_l > 34) AND (d_l > c_r))
) T2(e_l_r, c_l_r, b_l_r, d_l_r, c_r_r)
on (b_l > 96)
) T2(c_l_r, b_l_r, e_l_r_r, c_r_r_r, d_l_r_r)
on ((7 = c_l_r) OR (c_r_r_r = c_l_r))
) T2(e_l_l_r, c_l_r_r, c_r_r_r_r, e_l_r_r_r)
on (d_l = (d_l + e_l_r_r_r))
) T2(d_l_r, e_l_r_r_r_r, c_r_r_r_r_r, e_l_l_r_r)
on (a_l > (c_r_r_r_r_r * 26))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, e_r
from (
select c_l
from (
Select c_l, e_r, b_r
from (
Select c, a
from p4
where (((9 * b) > 46) OR ((e = 27) AND ((20 + 74) < 38)))
) T1(c_l, a_l)
inner join (
Select e, b
from p1
where ((((52 - c) + (74 + 5)) - a) = a)
) T2(e_r, b_r)
on (b_r = c_l)
) T1
union all
select d
from (
Select d
from p1
where ((b = 53) AND (97 = d))
) T2
) T1(c_l_l)
left join (
Select e, b
from p4
where (0 = ((a * 80) - 4))
) T2(e_r, b_r)
on (7 = c_l_l)
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
Select d_l, e_r
from (
Select b, d
from p5
where (c < ((92 * 6) * 7))
) T1(b_l, d_l)
inner join (
Select e, b, d
from p5
where (33 = 1)
) T2(e_r, b_r, d_r)
on ((96 < 25) AND (((d_l * d_l) = d_l) AND ((77 = ((e_r + e_r) * 82)) OR (e_r < e_r))))
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
Select a_l, c_r, d_r
from (
Select a
from p3
where (34 > 82)
) T1(a_l)
left join (
Select c, d
from p4
where ((c = (b + c)) OR (((88 + 76) < (28 + b)) AND (a < e)))
) T2(c_r, d_r)
on (27 = a_l)
) T1(a_l_l, c_r_l, d_r_l)
left join (
select c
from (
Select c, a, b, d
from p4
where (b < e)
) T1
union all
select d
from (
Select d
from p2
where (23 < 53)
) T2
) T2(c_r)
on ((a_l_l * a_l_l) = a_l_l)
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
Select a_l, e_r_r_l_r, c_r_r
from (
Select a, d
from p2
where (d > 47)
) T1(a_l, d_l)
left join (
Select e_r_r_l, c_r, a_r
from (
Select d_l, e_l_r, e_r_r
from (
Select d
from p3
where ((7 = 37) AND (36 = (87 - d)))
) T1(d_l)
full join (
Select e_l, c_l, e_r
from (
select e, c
from (
Select e, c, a
from p5
where (3 = a)
) T1
union all
select a, b
from (
Select a, b
from p3
where (2 > 76)
) T2
) T1(e_l, c_l)
left join (
Select e, d
from p2
where (23 < (13 * d))
) T2(e_r, d_r)
on (c_l < 71)
) T2(e_l_r, c_l_r, e_r_r)
on ((d_l = 54) OR ((16 + 81) = 88))
) T1(d_l_l, e_l_r_l, e_r_r_l)
full join (
Select e, c, a
from p2
where (e < c)
) T2(e_r, c_r, a_r)
on (64 < 42)
) T2(e_r_r_l_r, c_r_r, a_r_r)
on (c_r_r = 10)
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
Select c_l_r_l, e_r_r_r_l, a_r_r, e_r_r
from (
Select a_r_r_l, c_l_r, e_r_r_r
from (
Select c_l, a_l, a_r_r, d_l_r
from (
Select c, a, d
from p5
where ((70 = 57) OR ((78 = e) OR (79 = 23)))
) T1(c_l, a_l, d_l)
full join (
Select d_l, a_r
from (
Select b, d
from p1
where ((e * d) > (d - (58 - ((b - 90) + (d * (d - c))))))
) T1(b_l, d_l)
left join (
select a
from (
Select a
from p2
where ((79 = (95 * 92)) OR (a = c))
) T1
union all
select c
from (
Select c, d
from p5
where ((64 < c) AND (b < e))
) T2
) T2(a_r)
on (10 = (d_l - 77))
) T2(d_l_r, a_r_r)
on ((((57 - 85) + 5) = d_l_r) AND ((15 > d_l_r) AND (a_r_r < 28)))
) T1(c_l_l, a_l_l, a_r_r_l, d_l_r_l)
full join (
Select c_l, d_l, e_l_r, e_r_r
from (
Select c, d
from p2
where (d = 80)
) T1(c_l, d_l)
left join (
Select e_l, e_r
from (
Select e
from p3
where ((((69 + c) - 16) < 98) OR ((76 - (76 + (d * 81))) = 40))
) T1(e_l)
full join (
Select e
from p4
where (76 > 68)
) T2(e_r)
on (((23 - e_l) = 94) OR ((91 > e_r) AND ((((11 - e_l) * (80 - e_l)) = ((e_l * e_l) - 21)) OR (94 < e_l))))
) T2(e_l_r, e_r_r)
on (e_l_r > e_l_r)
) T2(c_l_r, d_l_r, e_l_r_r, e_r_r_r)
on ((11 < a_r_r_l) AND (c_l_r = (65 * (32 * c_l_r))))
) T1(a_r_r_l_l, c_l_r_l, e_r_r_r_l)
left join (
Select c_l_l, e_r_l, e_r, a_r
from (
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r, a_r
from (
Select e, c, a, d
from p2
where (45 = 64)
) T1(e_l, c_l, a_l, d_l)
left join (
Select e, a
from p2
where (a > (43 + 9))
) T2(e_r, a_r)
on ((14 - c_l) > (89 + a_r))
) T1
union all
select e, c, d
from (
Select e, c, d
from p2
where (87 > e)
) T2
) T1(c_l_l, a_l_l, e_r_l)
inner join (
Select e, a, d
from p2
where ((b > (80 + d)) OR ((((b * 10) + (a * ((78 * 99) - c))) * 78) = a))
) T2(e_r, a_r, d_r)
on ((c_l_l = 39) OR (14 = 29))
) T2(c_l_l_r, e_r_l_r, e_r_r, a_r_r)
on ((e_r_r > c_l_r_l) AND ((((61 * 71) - a_r_r) = (63 * e_r_r_r_l)) AND (73 = e_r_r)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #******************************************
    _testmgr.testcase_end(desc)

