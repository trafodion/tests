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
    
def test001(desc="""Joins Set 22"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r_r, b_l_r
from (
Select b, d
from p2
where ((c + (b + (63 - (71 + a)))) = 40)
) T1(b_l, d_l)
inner join (
Select b_l, c_r
from (
Select b, d
from p5
where ((c < 3) AND (26 < 6))
) T1(b_l, d_l)
inner join (
Select c, b
from p5
where ((79 > 29) AND (a > 3))
) T2(c_r, b_r)
on (c_r < 98)
) T2(b_l_r, c_r_r)
on ((b_l_r = b_l_r) AND (c_r_r = b_l_r))
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
Select e_l, b_r, d_r
from (
Select e
from p4
where (a < 84)
) T1(e_l)
left join (
Select a, b, d
from p5
where ((((18 - 41) + 77) < d) AND (c = 26))
) T2(a_r, b_r, d_r)
on ((d_r - ((d_r * 84) + e_l)) < b_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l, b_r_r, e_r_l_r
from (
Select e_l, b_r
from (
Select e, d
from p3
where (44 > d)
) T1(e_l, d_l)
inner join (
Select b
from p2
where ((e > 74) AND ((c * a) < 61))
) T2(b_r)
on ((3 = 22) OR (e_l = 34))
) T1(e_l_l, b_r_l)
left join (
Select d_r_r_l_l, e_r_l, e_r, a_r, b_r
from (
Select d_r_r_l, d_l_l, e_r
from (
Select d_l, d_r_r
from (
Select e, d
from p5
where ((b > c) OR (58 > 70))
) T1(e_l, d_l)
inner join (
Select d_l, d_r
from (
Select d
from p5
where ((c > 80) OR (61 > b))
) T1(d_l)
left join (
Select c, b, d
from p4
where (c = e)
) T2(c_r, b_r, d_r)
on ((63 - 22) = d_r)
) T2(d_l_r, d_r_r)
on (d_l < 36)
) T1(d_l_l, d_r_r_l)
left join (
Select e, d
from p3
where (b < a)
) T2(e_r, d_r)
on (d_r_r_l = d_r_r_l)
) T1(d_r_r_l_l, d_l_l_l, e_r_l)
left join (
Select e, a, b
from p1
where (90 < ((47 - d) + e))
) T2(e_r, a_r, b_r)
on (65 = 0)
) T2(d_r_r_l_l_r, e_r_l_r, e_r_r, a_r_r, b_r_r)
on ((e_r_l_r > 63) OR (35 = 2))
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
Select a_l, d_l, a_r, d_r
from (
Select a, d
from p3
where (43 < 38)
) T1(a_l, d_l)
inner join (
select e, a, d
from (
select e, a, d
from (
Select e, a, d
from p4
where (28 = 14)
) T1
union all
select a_l, b_l, e_r
from (
Select a_l, b_l, e_r
from (
Select c, a, b
from p1
where (a > 48)
) T1(c_l, a_l, b_l)
left join (
Select e
from p4
where (29 < (c + 23))
) T2(e_r)
on (b_l = 69)
) T2
) T1
union all
select e, a, d
from (
Select e, a, d
from p1
where ((d < (45 - 6)) OR (97 < a))
) T2
) T2(e_r, a_r, d_r)
on ((61 = 12) OR (35 > a_r))
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
Select c_l_l_l, a_l_r_l, c_r, b_r
from (
Select c_l_l, a_l_r
from (
Select c_l, c_r_r, d_l_r
from (
Select c
from p1
where (d = (21 + 18))
) T1(c_l)
left join (
select d_l, c_r
from (
Select d_l, c_r
from (
Select c, d
from p2
where (d > e)
) T1(c_l, d_l)
inner join (
Select c
from p3
where ((a > b) AND (82 = a))
) T2(c_r)
on ((46 > 20) OR ((5 = c_r) OR (d_l < (15 * c_r))))
) T1
union all
select e_l, d_l_l_r
from (
Select e_l, d_l_l_r, d_r_r_r_r
from (
select e
from (
Select e, c, d
from p4
where (((31 - 60) = e) OR ((67 - 74) < 24))
) T1
union all
select e
from (
Select e
from p1
where ((98 > d) OR ((27 = 89) AND (6 = 83)))
) T2
) T1(e_l)
inner join (
Select d_r_l, d_l_l, d_r_r_r, b_l_r
from (
Select d_l, a_r, d_r
from (
Select d
from p4
where ((13 * c) < 97)
) T1(d_l)
left join (
Select a, d
from p1
where (((e * 84) * 52) < b)
) T2(a_r, d_r)
on ((d_r = (d_r - 8)) OR (41 = a_r))
) T1(d_l_l, a_r_l, d_r_l)
inner join (
Select b_l, d_r_r
from (
Select e, b
from p1
where (89 = 34)
) T1(e_l, b_l)
left join (
Select e_l, d_r
from (
Select e, a, b
from p1
where (c = (d * (0 * 76)))
) T1(e_l, a_l, b_l)
inner join (
Select d
from p4
where (65 = 33)
) T2(d_r)
on ((30 = (((86 - 63) * 77) * e_l)) AND (e_l < (d_r + 62)))
) T2(e_l_r, d_r_r)
on ((13 * 79) < 97)
) T2(b_l_r, d_r_r_r)
on ((b_l_r < b_l_r) AND (d_l_l > 56))
) T2(d_r_l_r, d_l_l_r, d_r_r_r_r, b_l_r_r)
on ((41 > 11) OR (d_l_l_r < d_r_r_r_r))
) T2
) T2(d_l_r, c_r_r)
on (77 = 74)
) T1(c_l_l, c_r_r_l, d_l_r_l)
full join (
select a_l
from (
Select a_l, d_l, c_r, b_r
from (
Select a, d
from p3
where ((a < e) OR (e < 33))
) T1(a_l, d_l)
full join (
Select c, b
from p1
where ((45 * (c - 97)) = 6)
) T2(c_r, b_r)
on (a_l > d_l)
) T1
union all
select a
from (
Select a
from p4
where (e = (96 * c))
) T2
) T2(a_l_r)
on (c_l_l = 43)
) T1(c_l_l_l, a_l_r_l)
full join (
Select c, b
from p2
where (66 > (30 + c))
) T2(c_r, b_r)
on ((b_r + (67 - (35 + (b_r + (a_l_r_l - ((b_r - 9) * (a_l_r_l - c_r))))))) > 27)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, e_r_l, a_l_r_r, d_l_r, b_l_r
from (
Select c_l, e_r
from (
Select c, a, b, d
from p2
where ((70 = (67 - 48)) AND ((82 = 65) OR ((59 = c) AND (35 > a))))
) T1(c_l, a_l, b_l, d_l)
full join (
Select e, a
from p3
where ((13 > 7) AND (a = 33))
) T2(e_r, a_r)
on ((e_r = e_r) AND ((c_l = c_l) OR (e_r = e_r)))
) T1(c_l_l, e_r_l)
left join (
Select b_l, d_l, a_l_r
from (
Select b, d
from p3
where (4 < 55)
) T1(b_l, d_l)
left join (
select a_l
from (
Select a_l, b_l, d_l, d_r
from (
Select a, b, d
from p1
where ((76 = d) AND (0 = 94))
) T1(a_l, b_l, d_l)
left join (
Select d
from p3
where (((50 + b) < 5) OR (a > d))
) T2(d_r)
on (42 < 2)
) T1
union all
select a_l
from (
select a_l
from (
Select a_l, b_l, e_r
from (
Select a, b
from p5
where ((a = (e - a)) OR ((b = 37) OR (9 = (e - 12))))
) T1(a_l, b_l)
inner join (
Select e, a, b
from p5
where ((91 > a) OR ((51 - b) = a))
) T2(e_r, a_r, b_r)
on ((e_r < e_r) AND ((12 > e_r) OR (27 < a_l)))
) T1
union all
select e
from (
Select e
from p1
where (((c * a) = a) AND ((43 < 53) OR (13 < d)))
) T2
) T2
) T2(a_l_r)
on ((b_l > d_l) OR (33 = 73))
) T2(b_l_r, d_l_r, a_l_r_r)
on (17 > c_l_l)
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
Select c_l_r_l, c_r
from (
Select e_l_l, c_l_r
from (
Select e_l, b_l, d_r
from (
select e, b
from (
Select e, b, d
from p5
where (b < (a - 17))
) T1
union all
select c_r_l, d_r_r_r
from (
Select c_r_l, d_r_r_r
from (
Select c_l, c_r, a_r
from (
Select c
from p3
where (c = (b - d))
) T1(c_l)
inner join (
Select c, a
from p2
where ((9 - a) < c)
) T2(c_r, a_r)
on (((36 * a_r) < a_r) OR (15 < a_r))
) T1(c_l_l, c_r_l, a_r_l)
inner join (
Select b_l, d_r_r, e_r_r
from (
select b
from (
Select b
from p1
where (6 < ((e * 19) - 56))
) T1
union all
select d_l
from (
Select d_l, b_r_r_l_l_r
from (
Select d
from p1
where ((61 = 76) OR (23 = (78 + e)))
) T1(d_l)
left join (
Select b_r_r_l_l, c_r
from (
Select b_r_r_l, a_l_r_l_r, e_r_r
from (
Select e_r_l_l, b_r_r, d_r_r
from (
Select d_l_l, e_r_l, b_r_r, d_l_l_l_r
from (
Select d_l, e_r
from (
Select c, d
from p2
where ((30 = 29) OR ((((30 - a) * (a * c)) * 70) > 45))
) T1(c_l, d_l)
left join (
Select e, c, b
from p4
where (((33 - ((c * (b - 0)) * (c * b))) < b) AND ((d = d) OR (25 = c)))
) T2(e_r, c_r, b_r)
on (79 > 28)
) T1(d_l_l, e_r_l)
left join (
Select d_l_l_l, e_r, b_r
from (
Select d_l_l, d_r
from (
Select d_l, d_r
from (
Select c, d
from p5
where (46 = d)
) T1(c_l, d_l)
full join (
Select d
from p1
where ((b = 80) AND (e > 45))
) T2(d_r)
on (d_r = d_l)
) T1(d_l_l, d_r_l)
left join (
Select d
from p5
where (a > 30)
) T2(d_r)
on (42 > 50)
) T1(d_l_l_l, d_r_l)
left join (
Select e, b
from p1
where ((a < e) OR (23 = (89 + (c * e))))
) T2(e_r, b_r)
on ((((33 - b_r) * 23) = (b_r - (d_l_l_l + 30))) AND (e_r = (73 * 64)))
) T2(d_l_l_l_r, e_r_r, b_r_r)
on ((48 - (b_r_r + b_r_r)) = (5 + ((((d_l_l + b_r_r) * b_r_r) - ((86 * 22) + b_r_r)) - 62)))
) T1(d_l_l_l, e_r_l_l, b_r_r_l, d_l_l_l_r_l)
left join (
Select a_r_l_l_l, e_r_l, b_r, d_r
from (
Select a_r_l_l, e_r
from (
Select a_r_l, c_r_l, a_l_r, c_r_r
from (
Select e_l, c_r, a_r
from (
Select e, a
from p2
where ((a = a) OR (94 = 49))
) T1(e_l, a_l)
left join (
Select e, c, a, d
from p3
where (((49 + 99) > 60) OR (53 = 99))
) T2(e_r, c_r, a_r, d_r)
on (45 > e_l)
) T1(e_l_l, c_r_l, a_r_l)
left join (
Select a_l, d_l, c_r, d_r
from (
Select a, d
from p1
where ((((d + 59) - 40) = 8) AND (21 = 15))
) T1(a_l, d_l)
left join (
Select c, d
from p5
where (b < 8)
) T2(c_r, d_r)
on (67 > 97)
) T2(a_l_r, d_l_r, c_r_r, d_r_r)
on ((a_l_r > (83 + a_l_r)) OR ((63 < 25) OR ((c_r_l = c_r_r) AND (19 = 27))))
) T1(a_r_l_l, c_r_l_l, a_l_r_l, c_r_r_l)
inner join (
select e
from (
Select e
from p4
where ((e = e) AND ((b = 72) OR (c < 79)))
) T1
union all
select a
from (
Select a, b
from p4
where (((7 - a) = d) AND ((a + (83 + a)) < (e + d)))
) T2
) T2(e_r)
on (a_r_l_l < 86)
) T1(a_r_l_l_l, e_r_l)
left join (
Select e, b, d
from p2
where (e < ((82 * 24) * a))
) T2(e_r, b_r, d_r)
on ((d_r - 29) < 52)
) T2(a_r_l_l_l_r, e_r_l_r, b_r_r, d_r_r)
on (d_r_r = d_r_r)
) T1(e_r_l_l_l, b_r_r_l, d_r_r_l)
inner join (
Select a_l_l, a_l_r_l, e_r
from (
Select a_l, a_l_r, e_r_r
from (
select a
from (
Select a
from p3
where (e = 71)
) T1
union all
select e
from (
Select e, a
from p2
where ((c = e) AND (c = 61))
) T2
) T1(a_l)
left join (
Select a_l, e_r
from (
Select a
from p4
where (3 > 63)
) T1(a_l)
full join (
Select e, c
from p3
where (72 > c)
) T2(e_r, c_r)
on (((49 * 13) < e_r) OR (a_l > a_l))
) T2(a_l_r, e_r_r)
on ((a_l_r = a_l_r) OR (a_l = 12))
) T1(a_l_l, a_l_r_l, e_r_r_l)
left join (
Select e, b
from p2
where (88 = b)
) T2(e_r, b_r)
on (78 > 86)
) T2(a_l_l_r, a_l_r_l_r, e_r_r)
on ((78 * a_l_r_l_r) = 10)
) T1(b_r_r_l_l, a_l_r_l_r_l, e_r_r_l)
left join (
select c
from (
Select c
from p2
where ((e = (((34 * c) * (46 - 10)) * b)) OR (56 = 60))
) T1
union all
select e
from (
Select e, c, d
from p1
where (a = b)
) T2
) T2(c_r)
on (c_r = c_r)
) T2(b_r_r_l_l_r, c_r_r)
on (96 = 4)
) T2
) T1(b_l)
full join (
Select d_l, e_r, d_r
from (
Select d
from p3
where ((e < (5 - 0)) OR (c = a))
) T1(d_l)
left join (
Select e, d
from p4
where (a < c)
) T2(e_r, d_r)
on ((20 - (d_l + ((e_r + d_r) * d_r))) > e_r)
) T2(d_l_r, e_r_r, d_r_r)
on ((75 = 11) AND (d_r_r = 76))
) T2(b_l_r, d_r_r_r, e_r_r_r)
on (5 < 87)
) T2
) T1(e_l, b_l)
full join (
Select c, d
from p3
where (43 < 85)
) T2(c_r, d_r)
on (31 = (((d_r * 29) + 34) + 0))
) T1(e_l_l, b_l_l, d_r_l)
left join (
Select c_l, a_r
from (
Select c, a
from p1
where (14 = (18 * b))
) T1(c_l, a_l)
inner join (
Select a
from p2
where (26 < (c * a))
) T2(a_r)
on (((a_r - a_r) > 28) OR (62 < (92 * a_r)))
) T2(c_l_r, a_r_r)
on (51 > 53)
) T1(e_l_l_l, c_l_r_l)
left join (
Select c
from p5
where (95 > (98 - e))
) T2(c_r)
on (c_r < 56)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_r_r, c_r_r, d_l_r, b_l_r
from (
Select b
from p1
where ((65 < a) AND (1 > (39 - 56)))
) T1(b_l)
full join (
Select b_l, d_l, e_r, c_r, d_r
from (
Select b, d
from p3
where (d = (a + e))
) T1(b_l, d_l)
left join (
Select e, c, d
from p2
where (d = c)
) T2(e_r, c_r, d_r)
on ((3 = d_r) OR (7 > (((e_r - (e_r - 38)) + 91) - 83)))
) T2(b_l_r, d_l_r, e_r_r, c_r_r, d_r_r)
on (b_l_r = b_l_r)
order by 1, 2, 3, 4, 5
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_r, b_r
from (
Select c
from p5
where ((e < 37) AND (b = 3))
) T1(c_l)
full join (
Select e, b
from p4
where ((62 < 36) AND ((32 < 0) AND (d > b)))
) T2(e_r, b_r)
on (e_r = c_l)
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
Select e_l, c_l, b_r
from (
select e, c, b
from (
Select e, c, b
from p3
where ((e + d) > (91 - 0))
) T1
union all
select a, b, d
from (
Select a, b, d
from p1
where (b = e)
) T2
) T1(e_l, c_l, b_l)
inner join (
Select b
from p2
where (c > (30 + 11))
) T2(b_r)
on (b_r > e_l)
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
Select a_l_l, e_l_l, e_r
from (
select e_l, a_l
from (
Select e_l, a_l, e_r, d_r
from (
Select e, a, d
from p2
where (a = c)
) T1(e_l, a_l, d_l)
inner join (
Select e, c, b, d
from p2
where (e > 77)
) T2(e_r, c_r, b_r, d_r)
on ((e_l - 6) = e_r)
) T1
union all
select e, c
from (
Select e, c
from p3
where ((73 < 27) AND (a = (e - a)))
) T2
) T1(e_l_l, a_l_l)
left join (
Select e
from p4
where (b < b)
) T2(e_r)
on (72 > e_r)
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
Select d_l, c_r, b_r
from (
Select d
from p4
where (51 = d)
) T1(d_l)
full join (
Select c, b
from p2
where ((e * (b - d)) < 81)
) T2(c_r, b_r)
on (93 = d_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, c_r, d_r
from (
Select e_l, a_r
from (
Select e
from p5
where (e < 16)
) T1(e_l)
left join (
select a
from (
Select a, d
from p4
where (49 < (80 - 94))
) T1
union all
select a
from (
Select a
from p5
where ((52 = 43) AND (71 < d))
) T2
) T2(a_r)
on (e_l = 83)
) T1(e_l_l, a_r_l)
inner join (
Select c, a, d
from p4
where ((42 > d) AND ((b = 28) AND (((((b * (d + 12)) + d) * 39) < 4) AND ((d = 56) AND (44 > e)))))
) T2(c_r, a_r, d_r)
on (c_r < 60)
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
Select a_l, a_l_r, e_l_r, e_l_r_r_r
from (
Select a
from p3
where ((b > e) OR ((e - 66) = 0))
) T1(a_l)
left join (
Select e_l, a_l, e_l_r_r, b_l_r
from (
Select e, a
from p1
where (35 = 34)
) T1(e_l, a_l)
left join (
Select b_l, e_l_r
from (
Select b
from p1
where ((34 < 29) OR ((25 = b) OR (34 < e)))
) T1(b_l)
full join (
Select e_l, d_l, d_r_r, e_l_r, a_r_r
from (
Select e, c, d
from p1
where ((c = 62) AND ((d > 96) OR (((e - (69 * c)) = d) OR (b = 8))))
) T1(e_l, c_l, d_l)
full join (
Select e_l, c_r, a_r, d_r
from (
Select e
from p2
where ((e * 84) = (16 + c))
) T1(e_l)
inner join (
Select c, a, b, d
from p1
where ((95 - 17) = b)
) T2(c_r, a_r, b_r, d_r)
on ((14 < 34) AND (34 < c_r))
) T2(e_l_r, c_r_r, a_r_r, d_r_r)
on (a_r_r < e_l_r)
) T2(e_l_r, d_l_r, d_r_r_r, e_l_r_r, a_r_r_r)
on (((e_l_r - b_l) = ((30 + e_l_r) + e_l_r)) OR (e_l_r = e_l_r))
) T2(b_l_r, e_l_r_r)
on (80 > 70)
) T2(e_l_r, a_l_r, e_l_r_r_r, b_l_r_r)
on (((e_l_r_r_r * a_l) = 13) AND ((88 > (e_l_r * 56)) OR (72 = 53)))
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
Select a_l, b_l, e_l_l_l_r, a_r_l_r, e_r_r
from (
Select a, b
from p5
where (68 < c)
) T1(a_l, b_l)
full join (
Select a_r_l, e_l_l_l, e_r
from (
Select e_l_l, a_r_l, a_r
from (
select e_l, a_r
from (
Select e_l, a_r
from (
select e
from (
Select e
from p3
where (a < b)
) T1
union all
select e
from (
select e, a
from (
Select e, a, b
from p5
where (((((((d + c) - (52 - (3 - 34))) * c) - b) + 24) > 96) AND ((3 - 49) < b))
) T1
union all
select c_l, e_r
from (
select c_l, e_r
from (
Select c_l, e_r
from (
select c
from (
Select c
from p3
where ((b - 85) < a)
) T1
union all
select a_r_l
from (
select a_r_l, d_r
from (
Select a_r_l, d_r
from (
Select d_l_l_l, d_r_l_r_l, d_r_l_l, a_r
from (
Select d_r_l, d_l_l, d_r_l_r
from (
Select d_l, d_r
from (
Select d
from p2
where (56 = a)
) T1(d_l)
left join (
Select d
from p5
where ((97 = 43) AND (82 = 19))
) T2(d_r)
on (78 = d_l)
) T1(d_l_l, d_r_l)
left join (
Select d_r_l, d_l_r_l_l, a_r
from (
Select a_l_l, d_l_r_l, d_r
from (
Select a_l, d_l_r
from (
Select a
from p2
where ((92 = 34) OR (((94 * 62) > e) OR ((((75 + d) - (a * 9)) > 69) AND (d = ((8 * c) - 17)))))
) T1(a_l)
left join (
Select d_l, c_l_r, c_r_r
from (
Select a, d
from p3
where ((95 < 52) AND ((d < a) AND (56 = e)))
) T1(a_l, d_l)
left join (
Select c_l, c_r
from (
select c, d
from (
Select c, d
from p3
where ((d = 47) OR (a < 5))
) T1
union all
select c, a
from (
Select c, a
from p3
where ((24 > a) AND (a < b))
) T2
) T1(c_l, d_l)
full join (
select c
from (
Select c
from p2
where (e < 55)
) T1
union all
select c
from (
Select c
from p2
where (b > b)
) T2
) T2(c_r)
on (c_l = c_r)
) T2(c_l_r, c_r_r)
on ((c_l_r > 23) OR (c_l_r > (c_l_r + (d_l + (c_l_r * c_l_r)))))
) T2(d_l_r, c_l_r_r, c_r_r_r)
on ((a_l > d_l_r) AND ((d_l_r * a_l) = d_l_r))
) T1(a_l_l, d_l_r_l)
inner join (
Select a, d
from p5
where ((84 > a) OR (0 < d))
) T2(a_r, d_r)
on (d_l_r_l < (74 - 33))
) T1(a_l_l_l, d_l_r_l_l, d_r_l)
left join (
Select e, a
from p1
where ((94 * (42 + 98)) = ((c - c) + (c + 38)))
) T2(e_r, a_r)
on ((90 = d_l_r_l_l) OR (((11 * (a_r - 88)) > 64) OR (11 = 43)))
) T2(d_r_l_r, d_l_r_l_l_r, a_r_r)
on ((74 < d_r_l_r) AND (d_r_l < 52))
) T1(d_r_l_l, d_l_l_l, d_r_l_r_l)
left join (
Select a
from p4
where (e = d)
) T2(a_r)
on ((76 + 82) < 18)
) T1(d_l_l_l_l, d_r_l_r_l_l, d_r_l_l_l, a_r_l)
left join (
Select e, a, b, d
from p3
where ((76 + (e + (e * (95 + d)))) = e)
) T2(e_r, a_r, b_r, d_r)
on ((a_r_l * d_r) = (d_r + 77))
) T1
union all
select b_l, d_l
from (
Select b_l, d_l, e_r, b_r
from (
select b, d
from (
Select b, d
from p4
where (45 = (73 - b))
) T1
union all
select e, a
from (
Select e, a, b
from p5
where (77 > 36)
) T2
) T1(b_l, d_l)
full join (
Select e, b, d
from p4
where ((b + 48) = a)
) T2(e_r, b_r, d_r)
on (16 = b_l)
) T2
) T2
) T1(c_l)
left join (
Select e, a, b, d
from p5
where (85 < (69 + b))
) T2(e_r, a_r, b_r, d_r)
on (c_l = e_r)
) T1
union all
select c, b
from (
Select c, b
from p1
where ((d = a) AND (50 = 16))
) T2
) T2
) T2
) T1(e_l)
left join (
Select a
from p1
where (a = (b - (61 * (95 - 41))))
) T2(a_r)
on ((a_r > a_r) OR (((a_r + (65 * (a_r * a_r))) = a_r) AND ((90 < 62) OR ((42 = a_r) OR (e_l > (43 + (a_r - (23 * a_r))))))))
) T1
union all
select b_r_l, a_r
from (
Select b_r_l, a_r
from (
Select c_l, b_r
from (
Select c
from p4
where ((b < 60) OR (56 > e))
) T1(c_l)
full join (
Select b
from p5
where (b = e)
) T2(b_r)
on (c_l > 55)
) T1(c_l_l, b_r_l)
inner join (
Select a
from p5
where (71 = 65)
) T2(a_r)
on (a_r > 46)
) T2
) T1(e_l_l, a_r_l)
inner join (
Select e, c, a
from p3
where ((d - 57) < a)
) T2(e_r, c_r, a_r)
on ((a_r = 48) AND (a_r > 26))
) T1(e_l_l_l, a_r_l_l, a_r_l)
left join (
Select e, a
from p3
where ((e < c) AND ((74 < b) AND (3 = 36)))
) T2(e_r, a_r)
on (91 > a_r_l)
) T2(a_r_l_r, e_l_l_l_r, e_r_r)
on (e_l_l_l_r < (19 + 41))
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
Select e_l, a_l, b_l, a_r, b_r
from (
Select e, a, b
from p4
where (d > d)
) T1(e_l, a_l, b_l)
left join (
Select a, b, d
from p2
where ((13 < a) AND ((16 > c) OR ((30 + 7) > a)))
) T2(a_r, b_r, d_r)
on ((3 < e_l) OR ((55 < e_l) AND ((79 = 27) OR (51 > ((2 + ((78 - 41) + e_l)) - e_l)))))
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
Select a_l, b_r_r, e_l_r, a_r_r
from (
Select e, a
from p5
where (47 = 12)
) T1(e_l, a_l)
inner join (
Select e_l, a_r, b_r
from (
Select e
from p1
where (8 > e)
) T1(e_l)
left join (
Select a, b, d
from p5
where (e > e)
) T2(a_r, b_r, d_r)
on ((b_r < b_r) AND ((87 = b_r) OR ((e_l + ((a_r * 34) - 43)) = b_r)))
) T2(e_l_r, a_r_r, b_r_r)
on (27 > e_l_r)
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
Select b_l, c_r, b_r
from (
Select b, d
from p1
where ((a = 69) AND ((e = e) OR ((a * 0) = a)))
) T1(b_l, d_l)
left join (
Select c, b
from p4
where (a = b)
) T2(c_r, b_r)
on (b_r < 25)
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
from p3
where ((d + a) = d)
) T1(c_l)
full join (
Select e, a
from p2
where ((63 = 17) OR (47 = b))
) T2(e_r, a_r)
on (c_l = e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test22exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, d_l, e_r, b_r, d_r
from (
Select c, b, d
from p4
where ((49 * (e + 17)) = c)
) T1(c_l, b_l, d_l)
left join (
Select e, b, d
from p4
where ((30 < 19) OR (d < 63))
) T2(e_r, b_r, d_r)
on ((22 = b_l) AND (d_l = b_l))
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
    #************************************************
    _testmgr.testcase_end(desc)

