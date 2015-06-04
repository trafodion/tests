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
    
def test001(desc="""Joins Set 28"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_r, b_r
from (
Select c
from p3
where ((24 > d) AND (50 > 97))
) T1(c_l)
left join (
Select c, a, b
from p4
where (46 < 63)
) T2(c_r, a_r, b_r)
on (c_l > c_l)
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
Select e_l, e_r, a_r
from (
Select e
from p4
where (d > 5)
) T1(e_l)
left join (
Select e, a
from p3
where (c < (e * a))
) T2(e_r, a_r)
on (((34 - e_r) * e_l) = 0)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l, d_l_r_l_l, e_l_l_l, a_r
from (
Select e_l_l, b_r_r_l, d_l_r_l, d_r
from (
Select e_l, d_l, b_r_r, b_l_r, d_l_r
from (
Select e, d
from p2
where (b = d)
) T1(e_l, d_l)
left join (
select b_l, d_l, b_r
from (
Select b_l, d_l, b_r
from (
Select b, d
from p1
where ((b + b) = 89)
) T1(b_l, d_l)
left join (
Select b
from p5
where ((d < 88) OR (23 < 21))
) T2(b_r)
on (28 > 76)
) T1
union all
select e_l, b_l, a_r
from (
Select e_l, b_l, a_r
from (
Select e, b
from p1
where (((e * c) > 17) OR ((d > 35) OR (a > 62)))
) T1(e_l, b_l)
left join (
select c, a, d
from (
Select c, a, d
from p2
where ((d = (e - a)) AND ((((15 * (64 + 39)) - a) = (65 + d)) OR ((20 = 28) OR ((b > e) OR (57 > b)))))
) T1
union all
select e, b, d
from (
Select e, b, d
from p4
where (62 > e)
) T2
) T2(c_r, a_r, d_r)
on ((((a_r - 55) + b_l) - ((97 - 8) + a_r)) > 4)
) T2
) T2(b_l_r, d_l_r, b_r_r)
on (48 = d_l_r)
) T1(e_l_l, d_l_l, b_r_r_l, b_l_r_l, d_l_r_l)
left join (
select d
from (
Select d
from p4
where ((69 = b) AND (36 < c))
) T1
union all
select c
from (
select c, a
from (
Select c, a
from p5
where (((14 - (51 * 55)) = c) AND (b < e))
) T1
union all
select a, d
from (
select a, d
from (
Select a, d
from p5
where ((78 + (76 - 85)) > 0)
) T1
union all
select e, b
from (
select e, b, d
from (
Select e, b, d
from p1
where ((55 > 65) OR ((d = (56 - 84)) AND ((d > 62) AND (c < b))))
) T1
union all
select b_l, b_r, d_r
from (
Select b_l, b_r, d_r
from (
Select b
from p5
where (b < 8)
) T1(b_l)
inner join (
select e, b, d
from (
Select e, b, d
from p4
where ((d = b) AND (47 < e))
) T1
union all
select e, b, d
from (
select e, b, d
from (
Select e, b, d
from p4
where ((d * ((25 - 80) - b)) > a)
) T1
union all
select e, b, d
from (
Select e, b, d
from p5
where ((25 + (16 * 16)) = 75)
) T2
) T2
) T2(e_r, b_r, d_r)
on (((49 + b_r) < d_r) OR (48 > 60))
) T2
) T2
) T2
) T2
) T2(d_r)
on ((72 < b_r_r_l) AND ((26 < ((72 + 51) + (79 + 25))) OR (e_l_l < (38 * d_r))))
) T1(e_l_l_l, b_r_r_l_l, d_l_r_l_l, d_r_l)
left join (
Select a
from p4
where (6 = (e * e))
) T2(a_r)
on ((d_l_r_l_l * 19) > 68)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, c_r, a_r
from (
Select c, a
from p2
where (12 > (b - (a - 2)))
) T1(c_l, a_l)
left join (
Select c, a, b
from p1
where ((b > d) AND (87 = (44 * e)))
) T2(c_r, a_r, b_r)
on ((14 * 98) = 88)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l_r
from (
Select c
from p2
where ((5 + e) < 92)
) T1(c_l)
inner join (
Select d_l, c_l_r_r
from (
Select b, d
from p3
where ((((b - (b - a)) * 78) < 86) AND (61 > (93 + e)))
) T1(b_l, d_l)
inner join (
Select c_l, b_l, c_l_r, e_l_r
from (
Select c, b
from p2
where (16 = 74)
) T1(c_l, b_l)
left join (
Select e_l, c_l, b_r
from (
Select e, c, b
from p3
where ((13 * (68 + ((63 - c) - (60 - 44)))) < 23)
) T1(e_l, c_l, b_l)
inner join (
Select b
from p3
where ((e = 58) OR (d > c))
) T2(b_r)
on ((b_r = b_r) AND (c_l > 58))
) T2(e_l_r, c_l_r, b_r_r)
on (((c_l - (34 + b_l)) + ((32 - 34) - b_l)) > 56)
) T2(c_l_r, b_l_r, c_l_r_r, e_l_r_r)
on (40 = c_l_r_r)
) T2(d_l_r, c_l_r_r_r)
on ((c_l - ((d_l_r - c_l) * (38 * 55))) = c_l)
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
Select e_l, b_r
from (
Select e, c, d
from p3
where ((c = b) AND (74 > e))
) T1(e_l, c_l, d_l)
inner join (
Select b
from p5
where (a > 47)
) T2(b_r)
on (26 = (b_r - 52))
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
Select e_l, d_l_r_r, b_l_r
from (
Select e, c
from p3
where (((82 - 89) - 57) < e)
) T1(e_l, c_l)
left join (
Select b_l, d_l_r
from (
Select b
from p1
where (e > 24)
) T1(b_l)
left join (
Select d_l, d_l_r
from (
Select a, d
from p4
where ((d < c) AND (a = 24))
) T1(a_l, d_l)
left join (
Select d_l, e_r, b_r
from (
Select c, d
from p3
where ((1 < 79) OR (34 = d))
) T1(c_l, d_l)
full join (
Select e, b
from p3
where ((89 = 83) OR (b > 95))
) T2(e_r, b_r)
on ((b_r - b_r) < (49 + (14 - 62)))
) T2(d_l_r, e_r_r, b_r_r)
on ((d_l = 82) AND (13 > d_l_r))
) T2(d_l_r, d_l_r_r)
on (((60 * d_l_r) > (((d_l_r * 89) - 1) * b_l)) OR (b_l = d_l_r))
) T2(b_l_r, d_l_r_r)
on ((65 + 23) < e_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l_r, a_r_r, e_r_r
from (
select e
from (
Select e, d
from p2
where (((e - b) > a) OR (70 < 28))
) T1
union all
select a
from (
Select a
from p5
where ((26 > 62) OR ((43 - e) > 78))
) T2
) T1(e_l)
full join (
Select a_l, e_r, a_r
from (
select a
from (
Select a, b
from p2
where (d > 56)
) T1
union all
select a
from (
Select a
from p2
where ((84 * a) < (68 - ((98 * d) + c)))
) T2
) T1(a_l)
left join (
Select e, a
from p5
where ((d > 50) OR ((c < b) AND ((d = a) AND (e = c))))
) T2(e_r, a_r)
on ((0 = ((a_l * a_r) - a_r)) OR (93 < (31 - a_l)))
) T2(a_l_r, e_r_r, a_r_r)
on (e_r_r = 9)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, c_r_r
from (
Select c, a, b, d
from p1
where (2 = ((84 - 83) - d))
) T1(c_l, a_l, b_l, d_l)
inner join (
Select d_l, c_r, b_r
from (
Select a, d
from p1
where (28 = 65)
) T1(a_l, d_l)
full join (
Select c, b
from p2
where (47 < 26)
) T2(c_r, b_r)
on ((b_r > b_r) OR ((d_l = d_l) OR ((99 = c_r) AND (61 = d_l))))
) T2(d_l_r, c_r_r, b_r_r)
on ((c_r_r - 42) = 88)
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
Select a_l, d_l, a_r
from (
Select a, b, d
from p5
where (79 < 27)
) T1(a_l, b_l, d_l)
full join (
Select a
from p4
where (((9 + e) < 91) OR (c = ((a + 84) * a)))
) T2(a_r)
on ((42 = a_r) OR (47 > a_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test28exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l, b_r_l_r_l_l_l_r
from (
Select a_l, b_l, d_l_r
from (
Select a, b
from p3
where (90 = 93)
) T1(a_l, b_l)
left join (
Select d_l, c_r
from (
Select e, a, d
from p2
where (13 < b)
) T1(e_l, a_l, d_l)
inner join (
Select c
from p1
where (62 < c)
) T2(c_r)
on ((30 = 11) OR ((13 = 51) OR (69 > 21)))
) T2(d_l_r, c_r_r)
on (((b_l * d_l_r) + b_l) = 29)
) T1(a_l_l, b_l_l, d_l_r_l)
left join (
Select b_r_l_r_l_l_l, d_r_r_r_r_r, b_l_r
from (
select a_r_l, b_r_l_r_l_l, e_l_r
from (
Select a_r_l, b_r_l_r_l_l, e_l_r, c_l_l_r_r
from (
Select b_r_l_r_l, a_r
from (
Select d_l, a_l_l_r, b_r_l_r
from (
Select e, a, d
from p4
where ((b * 80) < d)
) T1(e_l, a_l, d_l)
full join (
Select a_l_l, b_r_l, c_r
from (
Select a_l, b_r, d_r
from (
Select c, a, b, d
from p5
where ((b = 45) AND ((33 > 73) OR (e = 84)))
) T1(c_l, a_l, b_l, d_l)
left join (
Select a, b, d
from p4
where (d = 71)
) T2(a_r, b_r, d_r)
on ((18 = a_l) OR ((44 = d_r) OR ((60 = 58) AND (b_r > b_r))))
) T1(a_l_l, b_r_l, d_r_l)
left join (
select e, c, a
from (
Select e, c, a
from p3
where (c < (e - 48))
) T1
union all
select d_l, e_r, c_r
from (
Select d_l, e_r, c_r
from (
select d
from (
Select d
from p4
where ((d - a) = 70)
) T1
union all
select a
from (
Select a
from p2
where ((59 + d) < d)
) T2
) T1(d_l)
left join (
Select e, c
from p3
where (23 = (a - (85 * c)))
) T2(e_r, c_r)
on (c_r = e_r)
) T2
) T2(e_r, c_r, a_r)
on (c_r > 59)
) T2(a_l_l_r, b_r_l_r, c_r_r)
on (b_r_l_r < 20)
) T1(d_l_l, a_l_l_r_l, b_r_l_r_l)
left join (
Select a
from p3
where ((d = d) AND (a = c))
) T2(a_r)
on (a_r < 18)
) T1(b_r_l_r_l_l, a_r_l)
left join (
Select e_l, c_l_l_r
from (
Select e, c
from p4
where (((d + (c * (75 - 41))) * a) = e)
) T1(e_l, c_l)
left join (
Select c_l_l, c_r_r_l, e_r_r_l, e_r_l_l_r_l, c_r
from (
Select e_l, c_l, c_r_r, e_r_l_l_r, e_r_r
from (
Select e, c
from p5
where (37 > 98)
) T1(e_l, c_l)
left join (
Select b_r_l, e_r_l_l, e_r, c_r, d_r
from (
Select d_r_l, e_r_l, b_r
from (
Select d_l, e_r, d_r
from (
Select c, d
from p1
where ((19 + (86 - 3)) < 93)
) T1(c_l, d_l)
full join (
Select e, d
from p3
where ((31 < 54) OR (c = 55))
) T2(e_r, d_r)
on ((83 = d_r) OR ((86 * 0) = d_l))
) T1(d_l_l, e_r_l, d_r_l)
full join (
Select b
from p3
where ((c < b) OR (63 < e))
) T2(b_r)
on (29 > b_r)
) T1(d_r_l_l, e_r_l_l, b_r_l)
left join (
Select e, c, d
from p3
where (((77 - 74) < 65) AND ((b - a) = 44))
) T2(e_r, c_r, d_r)
on (e_r > 67)
) T2(b_r_l_r, e_r_l_l_r, e_r_r, c_r_r, d_r_r)
on ((e_l < 8) AND (93 = ((e_r_r + e_r_r) - 69)))
) T1(e_l_l, c_l_l, c_r_r_l, e_r_l_l_r_l, e_r_r_l)
inner join (
Select e, c, d
from p4
where (((47 - 30) = a) OR (69 > d))
) T2(e_r, c_r, d_r)
on ((c_r > e_r_r_l) OR ((e_r_r_l < 34) AND ((e_r_r_l > c_r) AND ((e_r_l_l_r_l = c_r) AND (c_r = c_l_l)))))
) T2(c_l_l_r, c_r_r_l_r, e_r_r_l_r, e_r_l_l_r_l_r, c_r_r)
on ((c_l_l_r = e_l) OR (e_l = 95))
) T2(e_l_r, c_l_l_r_r)
on (a_r_l > b_r_l_r_l_l)
) T1
union all
select e, c, d
from (
Select e, c, d
from p3
where ((89 + 17) = d)
) T2
) T1(a_r_l_l, b_r_l_r_l_l_l, e_l_r_l)
inner join (
Select a_l, b_l, d_r_r_r_r
from (
Select a, b
from p4
where (((d - 29) = b) OR (c > 84))
) T1(a_l, b_l)
left join (
Select d_l, d_r_r_r
from (
Select d
from p2
where (a = d)
) T1(d_l)
inner join (
Select b_r_r_l, d_r_r, a_r_l_r
from (
Select b_l, b_r_r
from (
Select c, b, d
from p2
where ((37 * 81) < ((7 - (1 + 98)) - d))
) T1(c_l, b_l, d_l)
left join (
Select d_l, c_r, b_r
from (
select d
from (
Select d
from p3
where (71 < c)
) T1
union all
select b
from (
Select b
from p3
where (e = c)
) T2
) T1(d_l)
inner join (
Select c, b
from p5
where (d > 3)
) T2(c_r, b_r)
on ((29 + 47) > (d_l - c_r))
) T2(d_l_r, c_r_r, b_r_r)
on (b_l = (50 - b_l))
) T1(b_l_l, b_r_r_l)
full join (
Select e_l_l, a_r_l, d_r
from (
Select e_l, a_r
from (
Select e
from p3
where ((e > 5) OR ((16 = a) AND (e = (30 * b))))
) T1(e_l)
inner join (
select a
from (
Select a
from p4
where (((b + a) > e) AND ((72 * 19) > 29))
) T1
union all
select e
from (
Select e, c, a, d
from p3
where ((b < e) OR ((c + d) = (b + (c + 2))))
) T2
) T2(a_r)
on ((31 < a_r) OR (((a_r - a_r) > (e_l - a_r)) OR ((65 < 44) OR (53 = 17))))
) T1(e_l_l, a_r_l)
inner join (
select d
from (
select d
from (
Select d
from p3
where (((e * b) = a) OR (50 = 13))
) T1
union all
select c
from (
Select c, a, b, d
from p5
where (d = b)
) T2
) T1
union all
select e_l
from (
Select e_l, c_l, c_r_r, b_l_r
from (
Select e, c
from p3
where (73 < (60 * 71))
) T1(e_l, c_l)
full join (
Select c_l, b_l, c_r, a_r
from (
Select c, a, b
from p1
where (((e * b) < d) OR ((a > e) OR ((87 = e) OR (b > (c + c)))))
) T1(c_l, a_l, b_l)
left join (
Select e, c, a
from p3
where ((c > a) AND ((59 - ((27 + (e + 64)) - b)) < 34))
) T2(e_r, c_r, a_r)
on (a_r > c_l)
) T2(c_l_r, b_l_r, c_r_r, a_r_r)
on ((b_l_r = 64) OR ((93 = 64) OR ((14 * 58) < 56)))
) T2
) T2(d_r)
on ((((d_r + ((17 - ((56 + 32) * (54 - 62))) * 98)) + d_r) = 23) OR (46 = e_l_l))
) T2(e_l_l_r, a_r_l_r, d_r_r)
on ((d_r_r = 68) OR ((58 - d_r_r) > a_r_l_r))
) T2(b_r_r_l_r, d_r_r_r, a_r_l_r_r)
on (((d_l - 33) = (44 * 1)) AND (37 < d_r_r_r))
) T2(d_l_r, d_r_r_r_r)
on (((10 - 80) < 12) AND (29 > d_r_r_r_r))
) T2(a_l_r, b_l_r, d_r_r_r_r_r)
on ((21 > 48) OR ((b_l_r = d_r_r_r_r_r) AND (b_l_r > b_r_l_r_l_l_l)))
) T2(b_r_l_r_l_l_l_r, d_r_r_r_r_r_r, b_l_r_r)
on (((a_l_l + 55) + 91) > b_r_l_r_l_l_l_r)
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
Select e_l, c_l, c_r, b_r, d_r
from (
Select e, c, a
from p2
where (e = b)
) T1(e_l, c_l, a_l)
inner join (
Select c, b, d
from p5
where (6 = 1)
) T2(c_r, b_r, d_r)
on ((d_r = ((15 + ((83 * 86) + 44)) - 33)) OR ((e_l * 46) = 35))
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
Select b_l, e_r
from (
select a, b, d
from (
Select a, b, d
from p1
where (50 = c)
) T1
union all
select e, a, d
from (
Select e, a, d
from p4
where ((10 = 83) OR (a > d))
) T2
) T1(a_l, b_l, d_l)
full join (
Select e, d
from p2
where ((c = 70) AND (((a - 83) > e) AND (d = c)))
) T2(e_r, d_r)
on (30 < (81 + e_r))
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
Select d_l_l, a_l_r, c_r_r
from (
select d_l
from (
Select d_l, b_r
from (
Select d
from p1
where ((45 = d) AND (85 > e))
) T1(d_l)
inner join (
select b
from (
select b
from (
Select b
from p5
where (d > d)
) T1
union all
select c
from (
Select c, a, b
from p4
where ((44 - 28) = a)
) T2
) T1
union all
select e
from (
Select e, c
from p3
where ((89 = 0) OR (((36 - 82) + a) = a))
) T2
) T2(b_r)
on ((b_r = 24) AND ((62 = d_l) OR ((33 = 78) OR ((76 + d_l) = b_r))))
) T1
union all
select a
from (
Select a
from p4
where ((c > a) OR ((56 = 72) OR ((29 + 72) < c)))
) T2
) T1(d_l_l)
inner join (
Select a_l, c_r
from (
Select a
from p3
where ((64 = (2 * 8)) OR (40 = a))
) T1(a_l)
left join (
Select c, b
from p5
where ((44 - b) < e)
) T2(c_r, b_r)
on ((a_l < 65) OR (36 = c_r))
) T2(a_l_r, c_r_r)
on ((6 + a_l_r) < (8 + 51))
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
Select a_l_r_l, e_r, d_r
from (
Select d_l, a_l_r
from (
Select b, d
from p4
where (37 > (73 + 81))
) T1(b_l, d_l)
inner join (
Select a_l, a_r, b_r
from (
Select c, a, d
from p3
where (d > e)
) T1(c_l, a_l, d_l)
left join (
select a, b
from (
Select a, b
from p3
where ((60 + d) = c)
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, a_r
from (
select c, b
from (
Select c, b
from p4
where (1 > (a * 23))
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, a_r, d_r
from (
select e, c
from (
Select e, c, d
from p2
where (5 > 13)
) T1
union all
select e, b
from (
Select e, b
from p4
where ((e = 32) AND (((b * 23) = (17 * 83)) AND ((d = 66) OR (46 > a))))
) T2
) T1(e_l, c_l)
left join (
Select a, d
from p4
where (c = 35)
) T2(a_r, d_r)
on (e_l < d_r)
) T2
) T1(c_l, b_l)
full join (
Select e, a, d
from p2
where ((e = 58) OR (e > (44 * a)))
) T2(e_r, a_r, d_r)
on (77 > 0)
) T2
) T2(a_r, b_r)
on ((11 < a_r) AND ((37 = b_r) OR (48 < b_r)))
) T2(a_l_r, a_r_r, b_r_r)
on ((a_l_r = 4) AND (47 = 36))
) T1(d_l_l, a_l_r_l)
left join (
Select e, d
from p3
where (81 = 19)
) T2(e_r, d_r)
on (31 = d_r)
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
Select b_l, c_l_l_r, a_r_r
from (
Select b
from p2
where (a = (36 - (41 - ((65 + 42) * b))))
) T1(b_l)
full join (
Select b_r_l, c_l_l, a_r
from (
Select e_l, c_l, c_r, b_r
from (
Select e, c, d
from p3
where (((e * (d + c)) * b) = c)
) T1(e_l, c_l, d_l)
inner join (
Select c, b, d
from p3
where ((b = 36) AND ((b * 71) > 76))
) T2(c_r, b_r, d_r)
on (((85 + e_l) > 50) AND (44 > 58))
) T1(e_l_l, c_l_l, c_r_l, b_r_l)
inner join (
Select a
from p5
where ((66 * ((b * 3) - (d + a))) > c)
) T2(a_r)
on ((c_l_l * c_l_l) < a_r)
) T2(b_r_l_r, c_l_l_r, a_r_r)
on ((b_l > (59 * b_l)) OR ((b_l - c_l_l_r) > 55))
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
Select b_l, c_r_r, d_r_l_r
from (
select b
from (
Select b
from p3
where (30 = ((96 * b) - 19))
) T1
union all
select e
from (
Select e, c, b
from p2
where ((26 - b) < 62)
) T2
) T1(b_l)
inner join (
Select d_r_l, b_l_l, c_r
from (
select b_l, d_r
from (
select b_l, d_r
from (
Select b_l, d_r
from (
select a, b
from (
Select a, b, d
from p3
where (66 = e)
) T1
union all
select b_r_l, e_l_l
from (
select b_r_l, e_l_l
from (
select b_r_l, e_l_l
from (
Select b_r_l, e_l_l, d_l_l, a_r
from (
Select e_l, d_l, b_r
from (
Select e, b, d
from p4
where ((98 = 81) OR ((d + b) = 37))
) T1(e_l, b_l, d_l)
full join (
Select a, b, d
from p1
where ((42 < a) AND (54 = 80))
) T2(a_r, b_r, d_r)
on (1 < ((18 * (d_l * d_l)) - 88))
) T1(e_l_l, d_l_l, b_r_l)
left join (
select e, a
from (
Select e, a
from p5
where (b = a)
) T1
union all
select e, b
from (
Select e, b, d
from p1
where (79 = d)
) T2
) T2(e_r, a_r)
on (89 > 99)
) T1
union all
select e, c
from (
Select e, c
from p3
where ((e - c) = d)
) T2
) T1
union all
select c, d
from (
select c, d
from (
Select c, d
from p2
where ((19 < (16 * 27)) AND ((c - e) < 89))
) T1
union all
select e_l_l, e_r
from (
Select e_l_l, e_r
from (
select e_l, a_r
from (
Select e_l, a_r
from (
Select e
from p4
where ((e + e) = 3)
) T1(e_l)
left join (
Select a, b
from p4
where (d > b)
) T2(a_r, b_r)
on ((a_r > 81) AND ((e_l - (a_r - 33)) = 21))
) T1
union all
select e, c
from (
Select e, c
from p3
where (e < e)
) T2
) T1(e_l_l, a_r_l)
full join (
Select e
from p3
where (d = (d + (c * a)))
) T2(e_r)
on ((25 > e_r) OR ((0 > e_l_l) AND (60 > 26)))
) T2
) T2
) T2
) T1(a_l, b_l)
full join (
Select b, d
from p1
where (16 > b)
) T2(b_r, d_r)
on (((d_r + d_r) = b_l) OR (35 < 83))
) T1
union all
select e, b
from (
Select e, b, d
from p5
where (55 = d)
) T2
) T1
union all
select b_l, e_r
from (
Select b_l, e_r
from (
Select b
from p5
where (d = 82)
) T1(b_l)
full join (
Select e, c, b, d
from p1
where (79 > 80)
) T2(e_r, c_r, b_r, d_r)
on (38 > 8)
) T2
) T1(b_l_l, d_r_l)
inner join (
Select c, d
from p3
where (61 = c)
) T2(c_r, d_r)
on (6 < b_l_l)
) T2(d_r_l_r, b_l_l_r, c_r_r)
on (50 = b_l)
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
Select a_l, d_l, c_r, b_r
from (
Select a, d
from p1
where (95 = (70 - 97))
) T1(a_l, d_l)
left join (
Select c, b
from p3
where ((a < d) AND (70 = d))
) T2(c_r, b_r)
on (b_r > c_r)
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
Select d_r_l, a_r, d_r
from (
Select b_l, d_r
from (
select e, b
from (
Select e, b
from p1
where ((c = c) AND (91 < c))
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, a_r
from (
select c, a
from (
Select c, a
from p2
where (((58 + c) = d) AND (41 = 35))
) T1
union all
select b, d
from (
Select b, d
from p3
where (91 = (44 - b))
) T2
) T1(c_l, a_l)
full join (
Select a
from p5
where (60 < ((22 * e) - 94))
) T2(a_r)
on (1 > 63)
) T2
) T1(e_l, b_l)
left join (
Select d
from p5
where ((c = a) OR ((10 > e) OR (((d - 8) = 13) AND ((51 - (e + c)) > c))))
) T2(d_r)
on (d_r = d_r)
) T1(b_l_l, d_r_l)
inner join (
Select a, d
from p4
where ((((61 + 72) * (11 - a)) = 65) OR (72 = c))
) T2(a_r, d_r)
on (((d_r + 8) = 91) OR (30 = 88))
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
Select d_r_l, a_r
from (
Select a_r_l, d_l_l_l_l, e_r_l, d_r
from (
Select d_l_l_l, a_r_l_l, e_r, a_r
from (
Select a_r_l, d_l_l, c_r
from (
Select d_l, a_r
from (
Select a, d
from p2
where (a = d)
) T1(a_l, d_l)
left join (
select e, a
from (
Select e, a, d
from p1
where (((d - ((40 + e) + 39)) = e) AND (b > d))
) T1
union all
select e, a
from (
Select e, a
from p1
where (e = (d - 15))
) T2
) T2(e_r, a_r)
on (37 = (45 + d_l))
) T1(d_l_l, a_r_l)
full join (
select c
from (
Select c
from p5
where ((64 = d) AND (b = c))
) T1
union all
select a_r_l_l
from (
Select a_r_l_l, e_l_l_l, b_l_r
from (
Select e_l_l, a_r_l, c_r_l, e_r, d_r
from (
Select e_l, a_l, b_l, c_r, a_r
from (
Select e, a, b, d
from p5
where (95 > (31 * e))
) T1(e_l, a_l, b_l, d_l)
left join (
Select c, a
from p3
where ((97 < 77) AND (a = d))
) T2(c_r, a_r)
on ((3 = 41) OR (37 > c_r))
) T1(e_l_l, a_l_l, b_l_l, c_r_l, a_r_l)
inner join (
Select e, d
from p4
where (32 < (38 - 66))
) T2(e_r, d_r)
on ((37 = e_l_l) AND ((39 < (a_r_l - 99)) OR (62 < c_r_l)))
) T1(e_l_l_l, a_r_l_l, c_r_l_l, e_r_l, d_r_l)
inner join (
Select b_l, b_r
from (
Select b
from p1
where (47 = 96)
) T1(b_l)
full join (
Select a, b, d
from p4
where ((44 = 6) AND (92 < d))
) T2(a_r, b_r, d_r)
on (35 = b_r)
) T2(b_l_r, b_r_r)
on (b_l_r = a_r_l_l)
) T2
) T2(c_r)
on (93 = d_l_l)
) T1(a_r_l_l, d_l_l_l, c_r_l)
inner join (
Select e, a
from p4
where (a < 34)
) T2(e_r, a_r)
on ((7 * d_l_l_l) < (a_r - 78))
) T1(d_l_l_l_l, a_r_l_l_l, e_r_l, a_r_l)
left join (
Select c, d
from p2
where (31 > 36)
) T2(c_r, d_r)
on ((d_l_l_l_l < 44) AND (92 = (d_r - d_l_l_l_l)))
) T1(a_r_l_l, d_l_l_l_l_l, e_r_l_l, d_r_l)
left join (
Select a, b
from p3
where (32 > 69)
) T2(a_r, b_r)
on (35 < d_r_l)
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
    #***********************************************
    _testmgr.testcase_end(desc)

