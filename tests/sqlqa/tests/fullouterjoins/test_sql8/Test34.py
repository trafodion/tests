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
    
def test001(desc="""Joins Set 34"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l_l_l, e_r_l, e_r, a_r
from (
Select e_l_l, e_r
from (
Select e_l, b_r
from (
Select e, c
from p4
where ((d - 22) > c)
) T1(e_l, c_l)
inner join (
Select a, b, d
from p5
where ((c - 92) < 26)
) T2(a_r, b_r, d_r)
on (20 < (e_l * (b_r + (7 * (14 * b_r)))))
) T1(e_l_l, b_r_l)
left join (
Select e, d
from p1
where (b > 81)
) T2(e_r, d_r)
on (e_l_l > e_r)
) T1(e_l_l_l, e_r_l)
inner join (
Select e, a
from p5
where (68 < 15)
) T2(e_r, a_r)
on (30 = 55)
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
Select e_l, c_l, c_l_r
from (
Select e, c
from p1
where (80 < d)
) T1(e_l, c_l)
full join (
Select e_l, c_l, a_r
from (
Select e, c
from p3
where (((e * a) > 86) AND ((a = 50) OR (1 < 20)))
) T1(e_l, c_l)
left join (
Select a
from p5
where ((a * ((70 + 9) - 53)) < (54 * 7))
) T2(a_r)
on ((((c_l * 73) + c_l) = 77) AND (18 > a_r))
) T2(e_l_r, c_l_r, a_r_r)
on ((80 = c_l_r) AND (6 < (14 + c_l_r)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, b_r
from (
Select e, b
from p5
where (b = 62)
) T1(e_l, b_l)
left join (
Select b
from p4
where ((e + b) < c)
) T2(b_r)
on (b_l < b_l)
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
Select e_l, a_l, e_r
from (
Select e, a, b
from p3
where ((82 < c) AND ((a = 23) OR ((b = (4 - 91)) OR (97 = 25))))
) T1(e_l, a_l, b_l)
left join (
Select e, c
from p5
where (a = (b * 23))
) T2(e_r, c_r)
on (((7 - e_r) < a_l) AND (e_r > 73))
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
Select c_l, c_r, a_r
from (
Select c
from p5
where (d > 33)
) T1(c_l)
left join (
Select c, a, b
from p3
where ((27 = d) AND (b < c))
) T2(c_r, a_r, b_r)
on (5 > 72)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_r_l, e_l_r_l, c_r
from (
Select a_l_l, a_l_r, e_l_r, b_l_r
from (
select a_l, e_r_r_r
from (
select a_l, e_r_r_r
from (
Select a_l, e_r_r_r
from (
Select a
from p2
where (38 < 42)
) T1(a_l)
full join (
Select b_l, e_l_r, e_r_r
from (
select b
from (
Select b
from p4
where ((6 - 48) < d)
) T1
union all
select b
from (
Select b
from p4
where ((b * c) < 30)
) T2
) T1(b_l)
left join (
Select e_l, a_l, e_r
from (
Select e, a, b
from p3
where (10 > 57)
) T1(e_l, a_l, b_l)
inner join (
Select e, d
from p3
where (a < c)
) T2(e_r, d_r)
on (a_l = (e_r + 25))
) T2(e_l_r, a_l_r, e_r_r)
on (((e_l_r + 61) > 19) OR (34 > (39 * (b_l + 6))))
) T2(b_l_r, e_l_r_r, e_r_r_r)
on ((a_l > 82) OR (a_l = 15))
) T1
union all
select c_l, a_l
from (
Select c_l, a_l, b_l_l_l_l_r_r
from (
Select c, a
from p2
where (19 < 13)
) T1(c_l, a_l)
full join (
Select c_r_l, b_l_l_l_l_r, b_l_r_r
from (
Select c_r_r_l, c_r
from (
Select b_l, c_r_r
from (
Select b
from p4
where ((20 > 36) AND (88 = c))
) T1(b_l)
left join (
Select e_r_l, c_r
from (
Select b_l, e_r
from (
Select b
from p1
where (64 = a)
) T1(b_l)
full join (
Select e
from p5
where (a = a)
) T2(e_r)
on ((31 > b_l) OR (b_l > b_l))
) T1(b_l_l, e_r_l)
full join (
Select c, b
from p4
where (27 > 83)
) T2(c_r, b_r)
on (e_r_l = (e_r_l * 5))
) T2(e_r_l_r, c_r_r)
on ((92 * c_r_r) > c_r_r)
) T1(b_l_l, c_r_r_l)
left join (
Select c
from p4
where ((d < a) OR (c > e))
) T2(c_r)
on ((c_r_r_l > 89) OR (c_r_r_l > 91))
) T1(c_r_r_l_l, c_r_l)
inner join (
Select b_l_l_l_l, c_r_l_l, b_l_r
from (
Select b_l_l_l, a_r_l, c_r_l, b_r
from (
Select e_l_l_r_l, b_l_l, c_r, a_r
from (
select b_l, c_r_r, e_l_l_r
from (
Select b_l, c_r_r, e_l_l_r
from (
Select e, a, b
from p1
where ((67 * e) = (73 + 25))
) T1(e_l, a_l, b_l)
left join (
Select e_l_l, c_r
from (
select e_l
from (
Select e_l, e_r, a_r, b_r
from (
Select e, c
from p4
where ((75 = e) AND ((d > 42) AND (a < 47)))
) T1(e_l, c_l)
left join (
Select e, a, b
from p1
where (((e * (20 + 46)) = 8) OR (((d - 55) = d) OR ((96 = e) AND ((a = 76) AND ((e * 30) > 70)))))
) T2(e_r, a_r, b_r)
on (b_r < 24)
) T1
union all
select a
from (
Select a
from p2
where (a = (78 - 89))
) T2
) T1(e_l_l)
full join (
Select e, c
from p5
where ((12 = e) AND ((e * d) > 82))
) T2(e_r, c_r)
on ((e_l_l * (e_l_l * 89)) < e_l_l)
) T2(e_l_l_r, c_r_r)
on (18 = 8)
) T1
union all
select a_l, b_l, a_r
from (
Select a_l, b_l, a_r
from (
select a, b
from (
select a, b
from (
Select a, b
from p4
where ((d > (d - (b + (33 + a)))) OR (54 = 37))
) T1
union all
select c_l_l, a_r_r_r_l
from (
Select c_l_l, a_r_r_r_l, c_r
from (
Select c_l, e_l_r, a_r_r_r
from (
Select c, b
from p4
where (((82 + 87) = d) AND (83 = (a * 2)))
) T1(c_l, b_l)
left join (
Select e_l, a_r_r
from (
select e, c
from (
Select e, c, d
from p3
where (73 = b)
) T1
union all
select e, d
from (
Select e, d
from p1
where ((c > 89) OR (((c + (e + e)) = 16) AND ((95 < (92 - 22)) AND (((d * 90) > d) AND ((c = a) OR (((b + 64) + c) < 41))))))
) T2
) T1(e_l, c_l)
left join (
Select c_l, a_r
from (
Select c
from p5
where (e > 9)
) T1(c_l)
full join (
Select a
from p1
where ((79 > 80) AND (d = 39))
) T2(a_r)
on (((72 + (32 + 3)) > 77) OR ((69 - 7) > 28))
) T2(c_l_r, a_r_r)
on (e_l < 3)
) T2(e_l_r, a_r_r_r)
on (e_l_r = 8)
) T1(c_l_l, e_l_r_l, a_r_r_r_l)
left join (
Select c
from p1
where ((5 = c) OR ((84 = a) AND ((d * 31) > 50)))
) T2(c_r)
on ((c_r = (72 + 71)) AND (a_r_r_r_l = c_l_l))
) T2
) T1
union all
select a_l, c_r
from (
Select a_l, c_r
from (
Select a
from p3
where (36 < 99)
) T1(a_l)
inner join (
Select c
from p2
where (93 = e)
) T2(c_r)
on (a_l < c_r)
) T2
) T1(a_l, b_l)
left join (
select a
from (
Select a
from p3
where (54 < e)
) T1
union all
select a_l
from (
Select a_l, d_l, a_r, d_r
from (
Select e, a, d
from p5
where ((b * c) > (98 + 81))
) T1(e_l, a_l, d_l)
left join (
Select a, d
from p3
where (5 < 43)
) T2(a_r, d_r)
on ((a_r > 70) OR (a_r < d_r))
) T2
) T2(a_r)
on (91 = ((48 + (95 - a_l)) * (b_l - 56)))
) T2
) T1(b_l_l, c_r_r_l, e_l_l_r_l)
left join (
Select c, a
from p5
where ((a > (1 * 13)) OR ((36 > 55) AND ((d > b) OR ((94 * 76) < a))))
) T2(c_r, a_r)
on ((0 > 81) OR (c_r = c_r))
) T1(e_l_l_r_l_l, b_l_l_l, c_r_l, a_r_l)
left join (
Select b
from p1
where (d = 32)
) T2(b_r)
on (71 < 58)
) T1(b_l_l_l_l, a_r_l_l, c_r_l_l, b_r_l)
full join (
Select c_l, b_l, e_r
from (
select c, b
from (
Select c, b
from p1
where (20 = a)
) T1
union all
select a, d
from (
Select a, d
from p3
where ((97 = a) AND (((66 * c) = a) AND (b < b)))
) T2
) T1(c_l, b_l)
full join (
Select e
from p5
where (((82 + e) = a) OR (63 > c))
) T2(e_r)
on (b_l < 77)
) T2(c_l_r, b_l_r, e_r_r)
on ((74 < b_l_r) AND (((b_l_r * ((51 - b_l_r) + 16)) - 82) = c_r_l_l))
) T2(b_l_l_l_l_r, c_r_l_l_r, b_l_r_r)
on (c_r_l = (1 + b_l_r_r))
) T2(c_r_l_r, b_l_l_l_l_r_r, b_l_r_r_r)
on (((((c_l + (a_l + 24)) - 41) + b_l_l_l_l_r_r) * (a_l + a_l)) = b_l_l_l_l_r_r)
) T2
) T1
union all
select c, b
from (
Select c, b
from p5
where (a = (a + (((48 - b) - d) + e)))
) T2
) T1(a_l_l, e_r_r_r_l)
inner join (
Select e_l, a_l, b_l, c_r
from (
Select e, a, b
from p3
where (((0 * 95) < 26) OR ((d = (b + 18)) OR ((68 < b) AND (76 > 38))))
) T1(e_l, a_l, b_l)
inner join (
Select c, a
from p1
where (21 < (0 - ((58 + d) + (94 - d))))
) T2(c_r, a_r)
on (75 = 3)
) T2(e_l_r, a_l_r, b_l_r, c_r_r)
on (b_l_r = (29 * 5))
) T1(a_l_l_l, a_l_r_l, e_l_r_l, b_l_r_l)
left join (
Select c, a
from p1
where (e = b)
) T2(c_r, a_r)
on (((40 * (c_r + 87)) = 8) AND ((e_l_r_l = 33) AND (a_l_r_l > a_l_r_l)))
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
Select e_l, e_r
from (
Select e, b
from p5
where (13 = 69)
) T1(e_l, b_l)
left join (
select e, c
from (
Select e, c
from p1
where (69 > (e + (e * 80)))
) T1
union all
select d_l, b_r
from (
Select d_l, b_r
from (
Select d
from p2
where (((36 - a) = 25) AND (28 < d))
) T1(d_l)
left join (
select b
from (
select b
from (
Select b
from p1
where ((b < (45 - 92)) AND (c > d))
) T1
union all
select e
from (
select e
from (
Select e, c, a, b
from p4
where (((b + d) > (((a + 66) * 62) - c)) OR ((((d + d) * d) = 0) OR ((14 * 54) < 8)))
) T1
union all
select b
from (
Select b
from p1
where (76 = b)
) T2
) T2
) T1
union all
select e_l
from (
Select e_l, b_r, d_r
from (
Select e
from p1
where (b > b)
) T1(e_l)
left join (
Select a, b, d
from p5
where (e < (c - (b - 72)))
) T2(a_r, b_r, d_r)
on (14 > 23)
) T2
) T2(b_r)
on ((b_r < (d_l * 22)) OR ((b_r = 61) AND ((69 * 18) = ((b_r * 2) * (39 + (63 + 49))))))
) T2
) T2(e_r, c_r)
on ((59 < 68) OR (38 < ((56 * 84) * 22)))
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
Select c_l, c_r_r, e_r_l_l_r, e_r_r
from (
Select c
from p1
where ((c = (d - c)) OR ((56 = 20) AND (d < e)))
) T1(c_l)
left join (
Select e_r_l_l, c_r_r_l, e_r, c_r
from (
Select b_r_l, e_r_l, c_l_l_r, c_r_r, e_r_r
from (
Select c_l, e_r, b_r
from (
Select e, c, a, d
from p4
where ((b > e) OR (b = 55))
) T1(e_l, c_l, a_l, d_l)
inner join (
Select e, c, b, d
from p3
where ((d + e) = 82)
) T2(e_r, c_r, b_r, d_r)
on (51 = (b_r + b_r))
) T1(c_l_l, e_r_l, b_r_l)
left join (
Select c_l_l, e_r, c_r
from (
Select c_l, b_r
from (
Select e, c, a, d
from p2
where ((89 = 2) AND (86 > 2))
) T1(e_l, c_l, a_l, d_l)
left join (
Select e, b, d
from p5
where ((((82 * b) + (b + d)) < 33) OR (((e - d) > 1) AND ((((d - 90) + 52) = e) AND ((b > ((e - 45) + (54 + d))) AND (a = (d * 89))))))
) T2(e_r, b_r, d_r)
on (b_r = 14)
) T1(c_l_l, b_r_l)
inner join (
Select e, c, d
from p2
where ((38 < a) AND (a < e))
) T2(e_r, c_r, d_r)
on ((65 = 26) AND (c_r = (c_l_l * 64)))
) T2(c_l_l_r, e_r_r, c_r_r)
on (73 > e_r_l)
) T1(b_r_l_l, e_r_l_l, c_l_l_r_l, c_r_r_l, e_r_r_l)
left join (
Select e, c
from p2
where (77 < 21)
) T2(e_r, c_r)
on (98 = 73)
) T2(e_r_l_l_r, c_r_r_l_r, e_r_r, c_r_r)
on (91 > (e_r_r + e_r_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_r, b_r
from (
Select c
from p4
where ((37 = c) OR ((84 - (d * 62)) > 95))
) T1(c_l)
full join (
Select a, b
from p1
where (((77 * (b + 95)) * b) > b)
) T2(a_r, b_r)
on ((54 - 73) > a_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_r
from (
Select c, a
from p3
where (e = 69)
) T1(c_l, a_l)
inner join (
Select e
from p1
where (1 = 17)
) T2(e_r)
on (30 > e_r)
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
Select d_l_l, a_r
from (
select d_l
from (
Select d_l, c_l_r
from (
Select b, d
from p2
where ((8 = e) OR (e < a))
) T1(b_l, d_l)
inner join (
Select c_l, c_r
from (
Select c, a
from p2
where ((43 - b) < c)
) T1(c_l, a_l)
full join (
Select e, c, a
from p1
where (a > e)
) T2(e_r, c_r, a_r)
on ((c_r = (10 + 1)) OR (6 = 93))
) T2(c_l_r, c_r_r)
on ((78 = 43) AND (d_l = d_l))
) T1
union all
select e
from (
Select e
from p4
where ((c = 21) OR (c = 13))
) T2
) T1(d_l_l)
full join (
select a, d
from (
Select a, d
from p1
where ((23 < 5) OR (((((66 * b) - d) - (9 + (3 * b))) = 88) OR (44 > (54 + 83))))
) T1
union all
select a, d
from (
Select a, d
from p5
where (68 = e)
) T2
) T2(a_r, d_r)
on ((((27 + d_l_l) * a_r) > a_r) OR ((80 - a_r) = (d_l_l - 26)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_l_r_r, e_r_r_r_r
from (
Select c
from p2
where (c < a)
) T1(c_l)
full join (
Select c_l, c_l_r, e_r_r_r
from (
Select c, b, d
from p2
where (((c - 34) * 46) > (e - 3))
) T1(c_l, b_l, d_l)
inner join (
Select c_l, e_r_r
from (
Select e, c
from p1
where (22 = b)
) T1(e_l, c_l)
full join (
select d_r_l, e_r
from (
Select d_r_l, e_r, c_r, a_r
from (
Select e_l, d_r
from (
Select e
from p3
where ((d > c) OR (((47 + d) - 88) < (8 * a)))
) T1(e_l)
left join (
Select e, c, b, d
from p5
where ((b < ((c + c) - (13 - e))) AND ((48 - (a - (a + b))) = 30))
) T2(e_r, c_r, b_r, d_r)
on (e_l < 38)
) T1(e_l_l, d_r_l)
left join (
Select e, c, a, b
from p5
where (e = e)
) T2(e_r, c_r, a_r, b_r)
on (((77 * d_r_l) = 71) AND ((a_r < 90) OR (99 = 62)))
) T1
union all
select a, d
from (
Select a, d
from p1
where (98 = 39)
) T2
) T2(d_r_l_r, e_r_r)
on (70 = (e_r_r + e_r_r))
) T2(c_l_r, e_r_r_r)
on (c_l_r > 25)
) T2(c_l_r, c_l_r_r, e_r_r_r_r)
on (c_l_r_r = c_l)
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
Select c_l, e_r, a_r, d_r
from (
select c
from (
Select c, d
from p4
where ((90 = d) OR ((c = e) OR ((36 > (20 - a)) OR (d = (a * 61)))))
) T1
union all
select a
from (
Select a
from p2
where ((92 * 55) = (b + (28 + 88)))
) T2
) T1(c_l)
left join (
Select e, a, d
from p5
where (d < 96)
) T2(e_r, a_r, d_r)
on ((13 = (c_l + e_r)) OR (c_l > ((3 - c_l) * e_r)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l, a_r_l, a_r
from (
Select d_l, a_r, d_r
from (
select d
from (
Select d
from p5
where ((24 > 29) OR ((c < a) OR (c = a)))
) T1
union all
select e
from (
Select e
from p5
where (((75 * b) > a) OR ((67 * 38) = (c * a)))
) T2
) T1(d_l)
inner join (
Select a, b, d
from p4
where ((e - 61) = a)
) T2(a_r, b_r, d_r)
on (40 > d_r)
) T1(d_l_l, a_r_l, d_r_l)
inner join (
Select a
from p1
where (a = (e + (c + d)))
) T2(a_r)
on ((24 = 41) AND ((a_r_l = 71) AND (a_r = (81 + a_r_l))))
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
Select c_l, d_r_l_r, c_r_r
from (
Select c
from p3
where (83 = d)
) T1(c_l)
full join (
Select d_r_l, e_r, c_r
from (
Select d_l_l, d_r
from (
Select d_l, a_r
from (
Select c, d
from p5
where ((e = 24) OR (26 > e))
) T1(c_l, d_l)
left join (
select a
from (
Select a
from p4
where ((9 > 87) AND ((b = 49) OR (29 = 46)))
) T1
union all
select e
from (
Select e, d
from p1
where (79 > 41)
) T2
) T2(a_r)
on ((d_l < (a_r - d_l)) AND (16 = 64))
) T1(d_l_l, a_r_l)
inner join (
Select d
from p2
where ((a < 33) AND ((c = e) OR (a = e)))
) T2(d_r)
on ((40 = d_r) OR ((d_r < d_r) OR ((((23 - (17 - d_r)) + (d_l_l - (d_r * d_r))) - 82) < (d_r + d_l_l))))
) T1(d_l_l_l, d_r_l)
inner join (
Select e, c
from p2
where ((80 = d) AND (68 > e))
) T2(e_r, c_r)
on (e_r = e_r)
) T2(d_r_l_r, e_r_r, c_r_r)
on (((d_r_l_r * c_l) > c_l) OR ((c_r_r + c_l) > c_r_r))
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
Select e_l, d_r
from (
Select e
from p1
where (71 = a)
) T1(e_l)
left join (
Select d
from p5
where ((19 = (d + (((a - e) * c) * 41))) AND (44 < 7))
) T2(d_r)
on (((48 - d_r) < e_l) OR (1 < 97))
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
Select a_l, c_r, b_r
from (
Select a, b
from p3
where ((62 > 54) OR ((11 = a) AND ((56 = a) AND ((41 = c) AND ((a = (b * d)) OR (a = e))))))
) T1(a_l, b_l)
inner join (
Select e, c, a, b
from p4
where ((88 - c) < (e * 72))
) T2(e_r, c_r, a_r, b_r)
on ((5 < b_r) AND (61 = a_l))
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
Select b_l_r_l, e_l_l, a_l_r, c_l_r_r, d_r_r_r
from (
Select e_l, c_l_r, d_r_r, b_l_r
from (
select e, b
from (
Select e, b
from p5
where ((32 = 2) AND ((b + ((c + c) * ((1 * e) + d))) < c))
) T1
union all
select a, b
from (
Select a, b
from p1
where (35 < 27)
) T2
) T1(e_l, b_l)
left join (
Select c_l, b_l, d_r
from (
Select e, c, b, d
from p4
where ((4 > c) OR ((70 - d) = (2 - 79)))
) T1(e_l, c_l, b_l, d_l)
full join (
Select e, c, d
from p2
where (((94 + b) = ((e * 31) + 45)) OR ((67 - 25) < 32))
) T2(e_r, c_r, d_r)
on (9 = (c_l * ((65 + (94 - (b_l + (73 * 71)))) * 88)))
) T2(c_l_r, b_l_r, d_r_r)
on (80 = d_r_r)
) T1(e_l_l, c_l_r_l, d_r_r_l, b_l_r_l)
left join (
Select a_l, c_l_r, d_r_r
from (
Select e, a
from p5
where (71 < 26)
) T1(e_l, a_l)
left join (
Select e_l, c_l, b_r, d_r
from (
Select e, c
from p4
where (c < 1)
) T1(e_l, c_l)
inner join (
Select e, b, d
from p5
where (c > ((86 - c) - (b - 39)))
) T2(e_r, b_r, d_r)
on (c_l < d_r)
) T2(e_l_r, c_l_r, b_r_r, d_r_r)
on ((a_l = d_r_r) OR (a_l = a_l))
) T2(a_l_r, c_l_r_r, d_r_r_r)
on (48 > 37)
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
Select a_l, e_r, a_r
from (
Select e, c, a
from p3
where (((a + a) < c) AND ((e - 28) > a))
) T1(e_l, c_l, a_l)
full join (
Select e, a
from p5
where (b = (77 * 4))
) T2(e_r, a_r)
on (39 < e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test34exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, b_l, d_l, b_r, d_r
from (
Select a, b, d
from p5
where ((a + 21) = 81)
) T1(a_l, b_l, d_l)
inner join (
Select c, a, b, d
from p5
where ((b < e) AND ((93 + d) = b))
) T2(c_r, a_r, b_r, d_r)
on (b_l > (58 * 91))
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
    #*********************************
    _testmgr.testcase_end(desc)

