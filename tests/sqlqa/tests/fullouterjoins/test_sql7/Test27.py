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
Select e_r_l_r_l, c_r, b_r
from (
Select c_l_r_r_l, b_l_l, e_r_l_r
from (
Select e_l, b_l, c_l_r_r
from (
Select e, c, b
from p3
where (6 = c)
) T1(e_l, c_l, b_l)
full join (
select a_l, d_l, c_l_r
from (
Select a_l, d_l, c_l_r
from (
select a, d
from (
Select a, d
from p4
where ((0 = b) AND ((c < 46) AND ((c = (72 - e)) OR (((e * b) > 12) AND (b < a)))))
) T1
union all
select a, d
from (
Select a, d
from p2
where ((30 = 26) AND ((a - b) > 76))
) T2
) T1(a_l, d_l)
inner join (
select c_l, a_l
from (
Select c_l, a_l, e_r
from (
Select c, a
from p5
where (d > b)
) T1(c_l, a_l)
left join (
Select e
from p4
where (51 > e)
) T2(e_r)
on (((61 + c_l) - 5) = 61)
) T1
union all
select c, b
from (
Select c, b
from p1
where ((17 > d) OR ((b - e) > 96))
) T2
) T2(c_l_r, a_l_r)
on (36 = 59)
) T1
union all
select e, c, d
from (
Select e, c, d
from p2
where (b = d)
) T2
) T2(a_l_r, d_l_r, c_l_r_r)
on (e_l > (b_l - c_l_r_r))
) T1(e_l_l, b_l_l, c_l_r_r_l)
left join (
Select e_r_l, c_r
from (
Select c_l, a_l, e_r
from (
Select c, a
from p1
where (d = 15)
) T1(c_l, a_l)
left join (
Select e, a, d
from p5
where ((d = 72) AND ((c < 36) OR (b > e)))
) T2(e_r, a_r, d_r)
on (83 = e_r)
) T1(c_l_l, a_l_l, e_r_l)
left join (
Select c, b
from p3
where (a = b)
) T2(c_r, b_r)
on ((e_r_l - 91) > 37)
) T2(e_r_l_r, c_r_r)
on ((((b_l_l + ((40 + b_l_l) - 40)) * b_l_l) = e_r_l_r) OR (c_l_r_r_l < c_l_r_r_l))
) T1(c_l_r_r_l_l, b_l_l_l, e_r_l_r_l)
left join (
Select c, b
from p4
where (d = ((c * a) + (b * (c * 12))))
) T2(c_r, b_r)
on ((c_r = 97) OR (8 > 16))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_r, b_r
from (
Select e
from p1
where (d = a)
) T1(e_l)
full join (
Select a, b, d
from p1
where (44 > c)
) T2(a_r, b_r, d_r)
on (47 > 71)
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
Select e_l_l, c_r_r
from (
Select e_l, c_l, d_r_l_r
from (
Select e, c, a
from p5
where (66 < 97)
) T1(e_l, c_l, a_l)
left join (
select a_l_l, d_r_l
from (
Select a_l_l, d_r_l, e_r, a_r
from (
Select a_l, d_r
from (
Select a
from p4
where (a < b)
) T1(a_l)
full join (
Select e, d
from p1
where (60 < 75)
) T2(e_r, d_r)
on ((((17 + 33) - 45) * a_l) = a_l)
) T1(a_l_l, d_r_l)
left join (
Select e, a
from p2
where (81 = (b + 33))
) T2(e_r, a_r)
on (e_r = (e_r + a_r))
) T1
union all
select a_l, b_r
from (
select a_l, b_r
from (
Select a_l, b_r
from (
select a
from (
Select a
from p1
where ((10 < (52 * c)) AND ((c = 91) AND (b = e)))
) T1
union all
select b_l_l
from (
Select b_l_l, b_l_r
from (
Select b_l, d_r
from (
Select b, d
from p2
where (28 > (e + b))
) T1(b_l, d_l)
left join (
Select a, b, d
from p4
where (((a - a) = d) AND (98 > c))
) T2(a_r, b_r, d_r)
on (d_r = 60)
) T1(b_l_l, d_r_l)
full join (
Select b_l, d_l_l_r, a_r_r
from (
Select b
from p2
where ((a = d) OR ((45 < 26) AND ((b < d) OR (((30 - 28) = a) OR (93 < 4)))))
) T1(b_l)
left join (
Select d_l_l, a_r
from (
Select d_l, b_r
from (
Select a, d
from p2
where ((67 = a) OR (((41 + c) * 30) = (b * (b * b))))
) T1(a_l, d_l)
full join (
Select b
from p2
where (22 > b)
) T2(b_r)
on (47 = b_r)
) T1(d_l_l, b_r_l)
left join (
Select a
from p4
where ((69 < 47) OR ((b > e) AND (44 = c)))
) T2(a_r)
on (a_r = 88)
) T2(d_l_l_r, a_r_r)
on (d_l_l_r = a_r_r)
) T2(b_l_r, d_l_l_r_r, a_r_r_r)
on (b_l_l = 41)
) T2
) T1(a_l)
inner join (
Select a, b
from p1
where ((b = e) AND ((16 + 30) > 23))
) T2(a_r, b_r)
on ((((b_r + (b_r + (a_l * 40))) - a_l) < 22) AND (b_r > 9))
) T1
union all
select e_l_l, e_r_l
from (
Select e_l_l, e_r_l, e_l_r, c_r_r, d_l_r
from (
Select e_l, e_r, a_r, b_r
from (
Select e, d
from p2
where (c = e)
) T1(e_l, d_l)
inner join (
Select e, a, b
from p5
where (86 < e)
) T2(e_r, a_r, b_r)
on (b_r > 84)
) T1(e_l_l, e_r_l, a_r_l, b_r_l)
left join (
Select e_l, b_l, d_l, c_r
from (
Select e, a, b, d
from p4
where (((c * ((76 - 96) + e)) > 73) OR ((74 < 68) AND ((b * b) = c)))
) T1(e_l, a_l, b_l, d_l)
left join (
Select c
from p2
where ((b > (c + 3)) OR (94 = c))
) T2(c_r)
on (4 = b_l)
) T2(e_l_r, b_l_r, d_l_r, c_r_r)
on ((e_l_r = (21 - d_l_r)) OR ((((c_r_r - 87) + 12) < 16) OR (41 = (e_l_r * (e_l_l + e_l_l)))))
) T2
) T2
) T2(a_l_l_r, d_r_l_r)
on (((e_l * e_l) = c_l) OR (c_l > 53))
) T1(e_l_l, c_l_l, d_r_l_r_l)
inner join (
Select a_l_l, b_r_l, b_l_l, c_r
from (
Select a_l, b_l, b_r
from (
Select a, b
from p5
where (((71 - 21) < (a + 65)) OR (e > (d * 19)))
) T1(a_l, b_l)
left join (
Select b
from p2
where ((88 < c) AND ((e = (a - (e + e))) AND (69 = 7)))
) T2(b_r)
on ((a_l = (((a_l * b_l) + (52 - (((20 + 72) + b_l) * 40))) - b_r)) OR (64 < b_r))
) T1(a_l_l, b_l_l, b_r_l)
left join (
Select e, c
from p5
where ((a < e) OR (48 > 97))
) T2(e_r, c_r)
on (79 < c_r)
) T2(a_l_l_r, b_r_l_r, b_l_l_r, c_r_r)
on ((c_r_r = 98) AND (c_r_r = 4))
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
Select c_l, b_l_r
from (
Select c
from p5
where (((e - d) = 72) OR (((5 - (a * 66)) * 6) > 11))
) T1(c_l)
full join (
Select b_l, b_l_r
from (
Select c, b
from p1
where ((a < ((16 - a) + c)) AND (d > 14))
) T1(c_l, b_l)
left join (
Select b_l, d_l, e_l_r, c_r_r
from (
Select e, b, d
from p4
where (((a * 3) > (c + b)) AND ((67 = 17) AND ((88 < 56) OR ((c > a) AND (((((e * a) + (28 - 31)) + 93) < 20) AND (b = a))))))
) T1(e_l, b_l, d_l)
left join (
Select e_l, a_l, c_r
from (
Select e, a
from p4
where (96 = d)
) T1(e_l, a_l)
full join (
Select c, d
from p5
where ((84 = 56) AND (d > b))
) T2(c_r, d_r)
on (((81 + c_r) > ((5 - 24) * 63)) OR ((48 > 26) OR ((e_l - e_l) > e_l)))
) T2(e_l_r, a_l_r, c_r_r)
on (45 < 95)
) T2(b_l_r, d_l_r, e_l_r_r, c_r_r_r)
on ((b_l_r = 93) AND (b_l = (b_l_r * b_l_r)))
) T2(b_l_r, b_l_r_r)
on (16 < (2 + b_l_r))
order by 1, 2
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
Select e_l, d_l, a_r
from (
Select e, d
from p1
where (e < 62)
) T1(e_l, d_l)
inner join (
Select a
from p3
where (68 < 68)
) T2(a_r)
on (7 > 0)
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
Select b_l, c_r, a_r
from (
Select b
from p3
where ((56 = b) OR (c = d))
) T1(b_l)
left join (
Select c, a
from p5
where (87 > 45)
) T2(c_r, a_r)
on ((90 + (91 + 87)) > a_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, a_r
from (
Select a, b
from p1
where (52 = b)
) T1(a_l, b_l)
left join (
Select e, a
from p5
where (e = b)
) T2(e_r, a_r)
on ((38 < a_l) OR ((27 + 60) < a_r))
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
Select e_l, c_l, c_r
from (
Select e, c
from p1
where (a = 46)
) T1(e_l, c_l)
inner join (
Select c
from p1
where (a < (b + 92))
) T2(c_r)
on (c_r = c_r)
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
Select d_l_l, b_l_l, c_l_l_r
from (
Select e_l, b_l, d_l, a_r
from (
Select e, a, b, d
from p2
where ((c > a) OR (e = b))
) T1(e_l, a_l, b_l, d_l)
left join (
Select a
from p5
where (((e * 27) = 37) OR (87 > b))
) T2(a_r)
on ((89 = d_l) OR (((90 * a_r) < 33) AND ((28 = 79) OR (92 > ((25 * d_l) - e_l)))))
) T1(e_l_l, b_l_l, d_l_l, a_r_l)
full join (
Select c_l_l, c_r_l, e_r_l, b_r, d_r
from (
Select e_l, c_l, e_r, c_r
from (
Select e, c
from p3
where (a < 63)
) T1(e_l, c_l)
left join (
Select e, c, d
from p5
where (66 = a)
) T2(e_r, c_r, d_r)
on (75 = (c_r + 54))
) T1(e_l_l, c_l_l, e_r_l, c_r_l)
inner join (
Select e, a, b, d
from p3
where (e = e)
) T2(e_r, a_r, b_r, d_r)
on ((63 = (c_r_l * d_r)) AND (d_r = 34))
) T2(c_l_l_r, c_r_l_r, e_r_l_r, b_r_r, d_r_r)
on (6 = b_l_l)
order by 1, 2, 3
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
Select e_l, c_l, d_l, c_r, b_r
from (
Select e, c, b, d
from p1
where ((4 < 6) AND ((c > 37) OR ((d = 9) OR ((0 - c) < 95))))
) T1(e_l, c_l, b_l, d_l)
left join (
Select c, b
from p1
where (b = 74)
) T2(c_r, b_r)
on (67 = 84)
order by 1, 2, 3, 4, 5
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
Select a_l, b_r_r, e_r_r
from (
select a
from (
Select a
from p2
where (8 = a)
) T1
union all
select e
from (
Select e, a
from p3
where ((32 * 90) = 10)
) T2
) T1(a_l)
inner join (
Select e_l, a_l, e_r, b_r
from (
Select e, a, b
from p4
where (1 < c)
) T1(e_l, a_l, b_l)
inner join (
Select e, b, d
from p5
where (1 = e)
) T2(e_r, b_r, d_r)
on (e_l > e_l)
) T2(e_l_r, a_l_r, e_r_r, b_r_r)
on (b_r_r = b_r_r)
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
Select e_l, c_l, a_r, d_r
from (
Select e, c, b
from p1
where ((a - d) < 36)
) T1(e_l, c_l, b_l)
left join (
Select a, b, d
from p2
where ((d - c) = a)
) T2(a_r, b_r, d_r)
on (66 > c_l)
order by 1, 2, 3, 4
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
Select a_r_l, d_r
from (
Select b_l, a_r
from (
select b
from (
Select b
from p4
where ((d > c) AND ((26 < 30) OR ((70 = 71) OR ((((13 + ((a * 5) - (a + 54))) + (46 * 50)) > d) OR (40 > (a - 30))))))
) T1
union all
select d
from (
Select d
from p5
where ((78 = b) AND (c < 23))
) T2
) T1(b_l)
left join (
Select c, a
from p1
where (2 = 69)
) T2(c_r, a_r)
on (((b_l * a_r) > 17) AND (63 = b_l))
) T1(b_l_l, a_r_l)
left join (
Select e, b, d
from p2
where ((80 = c) OR ((b = e) OR ((((e * 84) * a) * ((b + b) + 23)) > (e * b))))
) T2(e_r, b_r, d_r)
on ((60 < (88 - a_r_l)) OR ((31 = 45) AND (a_r_l = d_r)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test27exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l_l, d_l_r_l, b_r_r
from (
select c_l_l, d_l_r
from (
Select c_l_l, d_l_r
from (
Select c_l, b_l, c_l_r, e_r_r
from (
Select c, b, d
from p4
where (d < 69)
) T1(c_l, b_l, d_l)
inner join (
Select c_l, e_r
from (
Select e, c
from p4
where (b < 57)
) T1(e_l, c_l)
left join (
Select e
from p5
where (3 > 64)
) T2(e_r)
on ((13 = e_r) AND (c_l < 57))
) T2(c_l_r, e_r_r)
on (79 > 46)
) T1(c_l_l, b_l_l, c_l_r_l, e_r_r_l)
left join (
Select e_l, d_l, c_r, a_r
from (
Select e, d
from p2
where (67 = a)
) T1(e_l, d_l)
left join (
Select c, a
from p2
where (c > ((2 + (44 + c)) - e))
) T2(c_r, a_r)
on (39 > 9)
) T2(e_l_r, d_l_r, c_r_r, a_r_r)
on (d_l_r = c_l_l)
) T1
union all
select e, a
from (
Select e, a, b
from p1
where (68 = e)
) T2
) T1(c_l_l_l, d_l_r_l)
full join (
Select e_r_r_l, e_r, b_r
from (
Select e_l, e_r_r
from (
Select e
from p1
where ((a * c) = b)
) T1(e_l)
left join (
Select a_l, b_l, d_l, e_r
from (
Select a, b, d
from p1
where ((b > a) OR ((32 = (d * c)) OR ((70 * d) < d)))
) T1(a_l, b_l, d_l)
left join (
Select e, c, d
from p4
where ((46 > b) AND (71 = 20))
) T2(e_r, c_r, d_r)
on (a_l = a_l)
) T2(a_l_r, b_l_r, d_l_r, e_r_r)
on ((e_r_r > 45) OR (e_r_r = e_r_r))
) T1(e_l_l, e_r_r_l)
left join (
Select e, b
from p5
where (a = a)
) T2(e_r, b_r)
on (((e_r_r_l + b_r) = ((77 - (18 + 74)) - e_r_r_l)) OR (b_r < (18 * b_r)))
) T2(e_r_r_l_r, e_r_r, b_r_r)
on (83 > 5)
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
Select e_l, a_r
from (
Select e
from p1
where (0 = a)
) T1(e_l)
inner join (
Select a, b, d
from p3
where ((d = 7) AND ((81 + 48) = 78))
) T2(a_r, b_r, d_r)
on (86 > 54)
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
Select c_l, d_l, c_r
from (
Select c, b, d
from p4
where ((33 + b) = d)
) T1(c_l, b_l, d_l)
full join (
Select e, c
from p2
where ((86 = 64) AND (58 = 24))
) T2(e_r, c_r)
on (((d_l * 59) > c_r) AND ((63 = 84) OR (97 < (18 + d_l))))
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
Select d_l_r_l, c_r
from (
Select e_l, a_l, e_r_r, d_l_r
from (
select e, a
from (
Select e, a, d
from p5
where (47 > (c - 41))
) T1
union all
select c_l, a_l_r
from (
Select c_l, a_l_r
from (
select e, c
from (
Select e, c, b
from p1
where (e < (41 - 49))
) T1
union all
select e, a
from (
Select e, a
from p5
where ((2 < 54) OR (a < (c * e)))
) T2
) T1(e_l, c_l)
left join (
Select a_l, e_r, c_r, d_r
from (
Select e, a
from p1
where ((b = 89) OR ((86 = (45 - e)) OR (88 = d)))
) T1(e_l, a_l)
left join (
Select e, c, a, d
from p1
where ((b + 44) = b)
) T2(e_r, c_r, a_r, d_r)
on ((49 = d_r) AND ((13 + d_r) < d_r))
) T2(a_l_r, e_r_r, c_r_r, d_r_r)
on (c_l > 20)
) T2
) T1(e_l, a_l)
left join (
Select d_l, e_r
from (
Select d
from p5
where ((41 = a) AND ((79 + a) = 65))
) T1(d_l)
inner join (
select e
from (
select e
from (
Select e, c, a
from p2
where (32 < 89)
) T1
union all
select b
from (
Select b
from p4
where ((11 > 82) AND ((99 < e) AND ((94 - (75 + 51)) = 35)))
) T2
) T1
union all
select d_l
from (
Select d_l, a_r, b_r
from (
Select d
from p4
where ((e = d) OR ((e < (17 + b)) AND (a = d)))
) T1(d_l)
left join (
Select a, b
from p5
where ((20 = 6) OR ((51 * 22) = 99))
) T2(a_r, b_r)
on (5 = 78)
) T2
) T2(e_r)
on (97 < (42 + 99))
) T2(d_l_r, e_r_r)
on (((((31 - 67) - 26) - d_l_r) = (d_l_r + e_r_r)) AND ((26 = a_l) AND (((33 + 6) < 7) AND ((85 = 62) AND ((76 < 63) OR ((d_l_r + 33) = a_l))))))
) T1(e_l_l, a_l_l, e_r_r_l, d_l_r_l)
inner join (
Select c, a, d
from p4
where (((d * 96) = b) OR (72 = a))
) T2(c_r, a_r, d_r)
on (37 = 31)
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
Select e_l, e_l_r, e_l_r_r
from (
Select e
from p1
where (63 > 77)
) T1(e_l)
left join (
select e_l, e_l_r
from (
Select e_l, e_l_r, d_l_r
from (
Select e
from p4
where (c < (55 - e))
) T1(e_l)
left join (
Select e_l, d_l, a_l_r_l_r
from (
Select e, d
from p2
where (e = ((b - (a - 90)) * 4))
) T1(e_l, d_l)
left join (
Select a_l_r_l, d_l_l_l, c_r_l_l, c_r, b_r
from (
Select c_r_l, d_l_l, a_l_r, b_r_r
from (
Select d_l, c_r
from (
select d
from (
Select d
from p5
where (a > 97)
) T1
union all
select c_r_l
from (
select c_r_l
from (
select c_r_l
from (
Select c_r_l, c_r, b_r, d_r
from (
select e_r_l, c_r
from (
Select e_r_l, c_r
from (
Select b_l, e_r
from (
Select b
from p1
where ((58 > (29 - 38)) OR (e < d))
) T1(b_l)
left join (
Select e, a
from p4
where (((c * a) > b) OR (51 > a))
) T2(e_r, a_r)
on ((49 + 88) = 60)
) T1(b_l_l, e_r_l)
left join (
Select c, a
from p2
where (c = 22)
) T2(c_r, a_r)
on (c_r = c_r)
) T1
union all
select e, b
from (
Select e, b, d
from p1
where ((c > b) AND ((a < 68) OR (18 < a)))
) T2
) T1(e_r_l_l, c_r_l)
inner join (
Select e, c, b, d
from p1
where (e > e)
) T2(e_r, c_r, b_r, d_r)
on ((78 - 60) = 72)
) T1
union all
select e
from (
Select e
from p1
where (c = c)
) T2
) T1
union all
select c_l
from (
select c_l
from (
Select c_l, b_l, d_r
from (
Select c, b, d
from p5
where (((59 * 15) < a) AND (9 = 26))
) T1(c_l, b_l, d_l)
left join (
Select c, d
from p1
where ((2 > ((37 * 40) + a)) OR ((d = b) AND (a < 55)))
) T2(c_r, d_r)
on (c_l = (c_l - c_l))
) T1
union all
select d
from (
Select d
from p2
where (b = b)
) T2
) T2
) T2
) T1(d_l)
left join (
Select c, b, d
from p3
where ((c + 28) < c)
) T2(c_r, b_r, d_r)
on (36 < 62)
) T1(d_l_l, c_r_l)
full join (
Select a_l, e_r, b_r
from (
Select a
from p3
where (82 < 95)
) T1(a_l)
left join (
Select e, b
from p2
where ((46 - 55) = (97 + (90 * 70)))
) T2(e_r, b_r)
on (((a_l - a_l) + e_r) > e_r)
) T2(a_l_r, e_r_r, b_r_r)
on (((d_l_l - 68) = (a_l_r + 53)) OR (c_r_l < a_l_r))
) T1(c_r_l_l, d_l_l_l, a_l_r_l, b_r_r_l)
full join (
Select e, c, b
from p3
where (a = 38)
) T2(e_r, c_r, b_r)
on (((d_l_l_l - 33) = 60) OR (44 = c_r_l_l))
) T2(a_l_r_l_r, d_l_l_l_r, c_r_l_l_r, c_r_r, b_r_r)
on (a_l_r_l_r = 3)
) T2(e_l_r, d_l_r, a_l_r_l_r_r)
on (97 = 72)
) T1
union all
select c, d
from (
Select c, d
from p5
where ((90 = c) AND (42 > d))
) T2
) T2(e_l_r, e_l_r_r)
on ((e_l - e_l_r) < e_l_r_r)
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
Select c_l, a_r, d_r
from (
Select c
from p2
where (b = 76)
) T1(c_l)
left join (
select a, d
from (
Select a, d
from p4
where ((((77 + 69) * (d + 52)) + 82) = (75 - a))
) T1
union all
select a_l, c_r_l_r
from (
Select a_l, c_r_l_r
from (
Select c, a, b
from p2
where ((91 = 13) AND (((49 * 41) > c) AND (43 = ((57 * b) + e))))
) T1(c_l, a_l, b_l)
full join (
Select c_r_l, d_l_l, e_r_l_l_r
from (
Select d_l, c_r
from (
Select b, d
from p4
where ((80 > ((b + e) + (63 * b))) OR (c = 81))
) T1(b_l, d_l)
left join (
Select c, a
from p1
where (46 = (90 + (e - 91)))
) T2(c_r, a_r)
on (25 < 28)
) T1(d_l_l, c_r_l)
left join (
select e_r_l_l
from (
Select e_r_l_l, b_r
from (
Select e_r_l, b_l_l, d_r
from (
Select b_l, e_r
from (
Select e, c, b
from p2
where (69 = 79)
) T1(e_l, c_l, b_l)
left join (
Select e
from p4
where ((c > 71) AND ((34 < e) AND ((d = 1) OR (c = (c + a)))))
) T2(e_r)
on (68 = b_l)
) T1(b_l_l, e_r_l)
left join (
Select d
from p4
where (d = 98)
) T2(d_r)
on (17 < 39)
) T1(e_r_l_l, b_l_l_l, d_r_l)
left join (
Select c, b
from p1
where (b > (c - (87 * (30 - 91))))
) T2(c_r, b_r)
on ((b_r - 81) < e_r_l_l)
) T1
union all
select c
from (
select c
from (
select c
from (
Select c
from p5
where ((e + 88) < c)
) T1
union all
select a
from (
Select a, b, d
from p2
where ((89 = 10) OR ((77 = 7) OR (d = 27)))
) T2
) T1
union all
select e
from (
Select e, a
from p1
where (c = 61)
) T2
) T2
) T2(e_r_l_l_r)
on ((78 - 64) = e_r_l_l_r)
) T2(c_r_l_r, d_l_l_r, e_r_l_l_r_r)
on (c_r_l_r < (c_r_l_r - 80))
) T2
) T2(a_r, d_r)
on (d_r < 11)
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
Select a_l, b_r_r_r, b_l_r
from (
Select e, a, b
from p4
where ((87 > 48) OR ((0 = 90) AND (a = (28 * c))))
) T1(e_l, a_l, b_l)
left join (
select b_l, b_r_r
from (
Select b_l, b_r_r
from (
Select e, b, d
from p5
where (a = (((95 - 97) + b) * (14 + 44)))
) T1(e_l, b_l, d_l)
left join (
Select a_l, b_r
from (
Select a
from p1
where ((a < 52) OR ((18 < a) AND (c = 98)))
) T1(a_l)
left join (
Select a, b
from p1
where (c < 82)
) T2(a_r, b_r)
on (5 = a_l)
) T2(a_l_r, b_r_r)
on ((b_l + 41) < 66)
) T1
union all
select e, c
from (
Select e, c, d
from p1
where ((83 = (b * (a * 40))) AND (d = 35))
) T2
) T2(b_l_r, b_r_r_r)
on (44 < 52)
order by 1, 2, 3
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
    #****************************************
    _testmgr.testcase_end(desc)

