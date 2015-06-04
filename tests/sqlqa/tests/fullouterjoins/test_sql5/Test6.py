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
    
def test001(desc="""Joins Set 6"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
Select c_l, e_l_r
from (
Select c
from p5
where (50 = 9)
) T1(c_l)
full join (
select e_l
from (
Select e_l, c_l, d_l, b_r
from (
Select e, c, d
from p1
where (((b + c) < c) OR ((9 * a) > b))
) T1(e_l, c_l, d_l)
left join (
Select b
from p5
where (30 = a)
) T2(b_r)
on (b_r = ((87 - 30) - (79 - b_r)))
) T1
union all
select d
from (
Select d
from p4
where ((54 < a) OR (66 > d))
) T2
) T2(e_l_r)
on (46 < (e_l_r - c_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_r
from (
Select a, d
from p5
where (69 > c)
) T1(a_l, d_l)
left join (
Select c
from p4
where (34 < b)
) T2(c_r)
on ((c_r = 42) AND ((a_l = 10) AND (((17 - c_r) < 59) OR ((7 < 23) OR (71 < (c_r - (56 * 28)))))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l, c_r_l_r
from (
Select e, b
from p2
where ((a > b) OR (20 > 20))
) T1(e_l, b_l)
left join (
Select b_r_l, c_r_l, c_r
from (
Select b_r_l, c_r_l, e_r_l, c_r, b_r
from (
Select d_l, e_r, c_r, b_r
from (
select d
from (
Select d
from p5
where ((e < a) AND ((e > 36) AND ((58 = 91) OR ((63 - 63) < 51))))
) T1
union all
select d_l
from (
Select d_l, a_r, b_r, d_r
from (
Select e, d
from p2
where ((c - a) > c)
) T1(e_l, d_l)
inner join (
select a, b, d
from (
Select a, b, d
from p2
where (70 > b)
) T1
union all
select a_l, d_l, e_r
from (
Select a_l, d_l, e_r, b_r
from (
Select e, a, d
from p2
where (51 = 53)
) T1(e_l, a_l, d_l)
left join (
Select e, b
from p5
where (7 = 6)
) T2(e_r, b_r)
on ((a_l = 43) AND (((((95 * a_l) - 26) * b_r) = 3) AND (39 = 53)))
) T2
) T2(a_r, b_r, d_r)
on (48 = 48)
) T2
) T1(d_l)
left join (
Select e, c, b
from p3
where (d > (10 * 50))
) T2(e_r, c_r, b_r)
on ((46 + 13) > (5 * 75))
) T1(d_l_l, e_r_l, c_r_l, b_r_l)
left join (
Select c, b
from p3
where (43 = (46 * d))
) T2(c_r, b_r)
on (c_r > 21)
) T1(b_r_l_l, c_r_l_l, e_r_l_l, c_r_l, b_r_l)
inner join (
Select c
from p1
where (((e * 93) < b) OR (90 < b))
) T2(c_r)
on (((13 - c_r) < b_r_l) AND ((b_r_l = 11) OR (b_r_l = c_r_l)))
) T2(b_r_l_r, c_r_l_r, c_r_r)
on ((79 = 61) OR (c_r_l_r < 86))
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
Select b_l, e_r, c_r
from (
Select b
from p1
where (((b + (96 + 95)) = 2) AND ((23 > 31) AND (e > 36)))
) T1(b_l)
inner join (
select e, c
from (
select e, c
from (
select e, c
from (
select e, c
from (
Select e, c
from p4
where ((((a * e) - 54) = 48) AND (((e * c) - b) > (c - a)))
) T1
union all
select c, b
from (
Select c, b
from p2
where (75 = (c - c))
) T2
) T1
union all
select e, a
from (
Select e, a, d
from p4
where ((92 = c) OR (22 > (((e - 12) * 78) + b)))
) T2
) T1
union all
select e, c
from (
Select e, c, d
from p4
where (e > c)
) T2
) T1
union all
select e, b
from (
Select e, b
from p5
where ((86 < ((a * d) - 96)) OR ((b < b) OR ((3 = 59) OR (75 = d))))
) T2
) T2(e_r, c_r)
on (27 = c_r)
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
where (87 = 14)
) T1(e_l)
left join (
Select e, d
from p5
where (57 = (e * d))
) T2(e_r, d_r)
on ((e_l > 58) OR (e_l = 43))
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
Select e_l, a_r_r, c_r_r, b_l_r
from (
Select e, d
from p2
where (12 = (35 - 2))
) T1(e_l, d_l)
full join (
Select b_l, c_r, a_r
from (
Select c, b
from p2
where (((33 * 74) + 46) = b)
) T1(c_l, b_l)
full join (
Select c, a
from p1
where ((43 = 13) OR (a > 99))
) T2(c_r, a_r)
on ((87 = 76) OR ((a_r * c_r) < (26 - 57)))
) T2(b_l_r, c_r_r, a_r_r)
on (73 < 0)
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
Select a_l, b_l, e_r
from (
Select a, b, d
from p2
where (12 > c)
) T1(a_l, b_l, d_l)
inner join (
Select e, b, d
from p5
where ((a = b) OR (b > a))
) T2(e_r, b_r, d_r)
on ((b_l + 2) < 69)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_r_l_l, c_r
from (
select d_r_l
from (
Select d_r_l, e_r
from (
Select c_l, d_l, d_r
from (
select c, d
from (
Select c, d
from p2
where (((10 * e) = d) OR (9 < 66))
) T1
union all
select c, b
from (
Select c, b
from p3
where (68 = 18)
) T2
) T1(c_l, d_l)
full join (
Select c, d
from p1
where ((d < 60) OR ((35 = e) OR ((a = 59) OR (83 = d))))
) T2(c_r, d_r)
on (d_r = d_r)
) T1(c_l_l, d_l_l, d_r_l)
inner join (
Select e, a
from p2
where (b = (a * 68))
) T2(e_r, a_r)
on (17 > (45 + 98))
) T1
union all
select c
from (
Select c
from p4
where ((c = (a - b)) OR (76 = e))
) T2
) T1(d_r_l_l)
left join (
Select e, c, a, d
from p2
where (32 < d)
) T2(e_r, c_r, a_r, d_r)
on ((d_r_l_l = (93 + c_r)) OR (59 = 69))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_r_r, d_r_r, b_l_r
from (
Select c, d
from p4
where (b = 1)
) T1(c_l, d_l)
left join (
Select a_l, b_l, b_r, d_r
from (
Select a, b
from p4
where (c < (a - 57))
) T1(a_l, b_l)
inner join (
Select b, d
from p1
where (40 > 1)
) T2(b_r, d_r)
on ((38 - 65) < 43)
) T2(a_l_r, b_l_r, b_r_r, d_r_r)
on (88 > b_l_r)
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
Select b_r_l, e_r
from (
Select a_l_r_l, b_l_l, c_r, a_r, b_r
from (
Select b_l, a_l_r
from (
Select b, d
from p4
where (d = e)
) T1(b_l, d_l)
left join (
Select a_l, d_l, c_r
from (
Select a, d
from p4
where (64 < (c + 91))
) T1(a_l, d_l)
left join (
Select e, c, d
from p5
where ((36 < (c * 81)) AND (59 = 88))
) T2(e_r, c_r, d_r)
on (23 > 65)
) T2(a_l_r, d_l_r, c_r_r)
on (63 = 60)
) T1(b_l_l, a_l_r_l)
left join (
Select e, c, a, b
from p3
where (69 < 35)
) T2(e_r, c_r, a_r, b_r)
on (76 = 84)
) T1(a_l_r_l_l, b_l_l_l, c_r_l, a_r_l, b_r_l)
full join (
Select e, b, d
from p3
where (a < 84)
) T2(e_r, b_r, d_r)
on (((e_r * 5) > 87) AND (99 = e_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, b_l_r
from (
select e
from (
Select e
from p3
where (b = 27)
) T1
union all
select d
from (
Select d
from p1
where (26 = e)
) T2
) T1(e_l)
inner join (
Select e_l, a_l, b_l, a_r, d_r
from (
Select e, a, b
from p3
where (a > 24)
) T1(e_l, a_l, b_l)
left join (
Select a, d
from p5
where (67 < 75)
) T2(a_r, d_r)
on ((d_r < 26) OR (95 = 51))
) T2(e_l_r, a_l_r, b_l_r, a_r_r, d_r_r)
on (b_l_r < (89 * e_l))
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
Select a_l, b_l_r_l_r
from (
select a, b, d
from (
select a, b, d
from (
Select a, b, d
from p3
where (44 < 27)
) T1
union all
select c, a, b
from (
Select c, a, b, d
from p4
where (82 > (e - 32))
) T2
) T1
union all
select d_l_l, e_r_l, c_r
from (
Select d_l_l, e_r_l, c_r
from (
Select d_l, e_r
from (
Select a, d
from p4
where (e < e)
) T1(a_l, d_l)
full join (
select e
from (
Select e, c
from p4
where (((c + 15) - c) > (b + c))
) T1
union all
select a
from (
select a
from (
Select a
from p2
where ((e - c) = e)
) T1
union all
select e
from (
Select e, c, a
from p2
where (c = (c - b))
) T2
) T2
) T2(e_r)
on (d_l > ((e_r * 45) + 68))
) T1(d_l_l, e_r_l)
inner join (
select c, a
from (
Select c, a, d
from p5
where ((c + (c + ((3 * 85) * e))) = b)
) T1
union all
select e_l, d_r
from (
Select e_l, d_r
from (
Select e
from p4
where (42 = 42)
) T1(e_l)
left join (
Select b, d
from p5
where (((d * 70) < (b + 79)) OR (15 < b))
) T2(b_r, d_r)
on (66 < e_l)
) T2
) T2(c_r, a_r)
on ((d_l_l = ((d_l_l - 95) * 59)) OR (((c_r + (e_r_l + 65)) = 68) OR ((49 = 34) OR (((55 - c_r) > d_l_l) OR ((42 = (3 - d_l_l)) AND (95 = 8))))))
) T2
) T1(a_l, b_l, d_l)
left join (
Select b_l_r_l, a_l_l, c_r
from (
Select a_l, b_l_r
from (
Select a, b, d
from p5
where (e < 14)
) T1(a_l, b_l, d_l)
inner join (
Select b_l, e_l_r, b_l_r
from (
Select b
from p3
where (e > 80)
) T1(b_l)
inner join (
Select e_l, b_l, c_r
from (
Select e, b
from p1
where (9 = 80)
) T1(e_l, b_l)
full join (
Select c, a, b, d
from p4
where ((c < c) OR (9 = 28))
) T2(c_r, a_r, b_r, d_r)
on (93 = (b_l + ((c_r - (c_r - 14)) - b_l)))
) T2(e_l_r, b_l_r, c_r_r)
on ((b_l_r - b_l) = 19)
) T2(b_l_r, e_l_r_r, b_l_r_r)
on ((a_l = b_l_r) AND ((a_l = 21) AND ((54 > 50) AND (68 = 82))))
) T1(a_l_l, b_l_r_l)
full join (
Select c, a, d
from p3
where (90 > b)
) T2(c_r, a_r, d_r)
on (a_l_l > 64)
) T2(b_l_r_l_r, a_l_l_r, c_r_r)
on ((85 = 25) OR (b_l_r_l_r = 97))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, a_r, d_r
from (
Select e, c, d
from p3
where (81 = e)
) T1(e_l, c_l, d_l)
left join (
Select a, b, d
from p3
where (53 = 54)
) T2(a_r, b_r, d_r)
on (84 = 90)
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
Select d_l, b_l_l_r, b_r_l_r
from (
Select a, d
from p3
where ((86 = 71) OR (d = a))
) T1(a_l, d_l)
full join (
Select b_r_l, b_l_l, d_r
from (
Select b_l, b_r
from (
Select e, c, b
from p2
where (10 < 31)
) T1(e_l, c_l, b_l)
full join (
Select b
from p5
where ((b * c) > e)
) T2(b_r)
on (b_l < 86)
) T1(b_l_l, b_r_l)
inner join (
Select a, d
from p1
where ((61 = a) OR ((e - b) < ((29 - (62 * a)) - 75)))
) T2(a_r, d_r)
on (47 > (51 * b_l_l))
) T2(b_r_l_r, b_l_l_r, d_r_r)
on (b_l_l_r > 76)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r_r
from (
Select a, b, d
from p1
where (48 = c)
) T1(a_l, b_l, d_l)
full join (
Select a_l_l, e_l_l, e_r, b_r
from (
Select e_l, a_l, b_r
from (
Select e, c, a
from p3
where ((d < c) AND (c = ((b - b) * 65)))
) T1(e_l, c_l, a_l)
inner join (
Select b
from p1
where ((a * 16) > 76)
) T2(b_r)
on (e_l < 18)
) T1(e_l_l, a_l_l, b_r_l)
inner join (
Select e, b
from p5
where (33 = e)
) T2(e_r, b_r)
on ((22 > 47) OR (e_l_l = 2))
) T2(a_l_l_r, e_l_l_r, e_r_r, b_r_r)
on ((d_l - e_r_r) < 19)
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
Select a_l, b_r, d_r
from (
Select a
from p5
where ((d = 36) AND (85 = a))
) T1(a_l)
full join (
Select b, d
from p4
where (46 = a)
) T2(b_r, d_r)
on ((b_r + 69) = b_r)
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
Select e_l, b_l, d_r_l_r, c_l_l_l_r
from (
select e, b
from (
select e, b
from (
select e, b
from (
Select e, b, d
from p2
where (d > 40)
) T1
union all
select b, d
from (
Select b, d
from p3
where ((c < ((11 * 21) * 83)) AND ((35 + 86) > 47))
) T2
) T1
union all
select e, a
from (
Select e, a, d
from p5
where ((98 > 50) AND (d > b))
) T2
) T1
union all
select c, b
from (
Select c, b
from p2
where ((60 = b) OR ((1 + (b * 17)) > e))
) T2
) T1(e_l, b_l)
full join (
select b_r_l, c_l_l_l, d_r_l, b_r_l_l
from (
Select b_r_l, c_l_l_l, d_r_l, b_r_l_l, c_r, b_r
from (
Select b_r_l, c_l_l, b_r, d_r
from (
Select c_l, e_r, b_r
from (
Select e, c
from p3
where (d = 58)
) T1(e_l, c_l)
full join (
Select e, b
from p3
where (a = (14 * c))
) T2(e_r, b_r)
on (99 > c_l)
) T1(c_l_l, e_r_l, b_r_l)
inner join (
select b, d
from (
Select b, d
from p1
where (d > b)
) T1
union all
select e, c
from (
Select e, c
from p1
where (19 < (b + (66 - c)))
) T2
) T2(b_r, d_r)
on (c_l_l > 18)
) T1(b_r_l_l, c_l_l_l, b_r_l, d_r_l)
left join (
Select e, c, b, d
from p4
where ((19 > 98) AND ((54 * 87) > c))
) T2(e_r, c_r, b_r, d_r)
on (63 = (((b_r - 89) - 89) - 80))
) T1
union all
select c, a, b, d
from (
select c, a, b, d
from (
Select c, a, b, d
from p5
where ((b = e) OR (c < 62))
) T1
union all
select e, c, a, b
from (
Select e, c, a, b
from p2
where ((b = (c + (50 * 89))) AND (c < 65))
) T2
) T2
) T2(b_r_l_r, c_l_l_l_r, d_r_l_r, b_r_l_l_r)
on (c_l_l_l_r < (b_l + 2))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_l_r
from (
Select c
from p5
where (d = a)
) T1(c_l)
left join (
select e_l
from (
Select e_l, a_r
from (
Select e
from p3
where ((6 < 78) OR (((a + (53 - 95)) - e) = 96))
) T1(e_l)
left join (
Select a
from p2
where ((92 = 27) AND (88 = (e - 16)))
) T2(a_r)
on (a_r < 16)
) T1
union all
select d
from (
Select d
from p1
where (d < ((a * ((70 * a) + d)) + e))
) T2
) T2(e_l_r)
on ((28 = 83) OR ((75 > e_l_r) OR ((c_l = 80) AND ((e_l_r < 59) OR (5 = 31)))))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, b_r
from (
Select e
from p5
where ((d = 12) OR ((e > (59 + 53)) AND (40 > (d * e))))
) T1(e_l)
left join (
Select e, b
from p5
where ((72 - c) = (b - c))
) T2(e_r, b_r)
on (57 > b_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test06exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, c_l_r_l_r
from (
Select c, a, b
from p5
where (e > 52)
) T1(c_l, a_l, b_l)
left join (
select c_l_r_l, a_r_r_l
from (
select c_l_r_l, a_r_r_l
from (
Select c_l_r_l, a_r_r_l, e_r, a_r, d_r
from (
Select c_l, c_l_r, a_r_r
from (
Select c
from p2
where (((d - d) < 95) OR (e = 52))
) T1(c_l)
left join (
Select c_l, b_l, a_r
from (
Select e, c, b
from p3
where (44 = 70)
) T1(e_l, c_l, b_l)
inner join (
Select a
from p1
where (a > 55)
) T2(a_r)
on ((c_l < (a_r - 32)) AND ((93 = c_l) OR (((((b_l * 26) * 95) * (17 - b_l)) < (77 * b_l)) OR (51 = c_l))))
) T2(c_l_r, b_l_r, a_r_r)
on (((16 - 9) < 5) AND ((78 < (c_l_r + c_l)) OR (c_l_r = 83)))
) T1(c_l_l, c_l_r_l, a_r_r_l)
full join (
Select e, a, d
from p3
where (48 = b)
) T2(e_r, a_r, d_r)
on ((e_r < e_r) OR (70 = a_r))
) T1
union all
select c, d
from (
Select c, d
from p1
where (45 = (46 + 43))
) T2
) T1
union all
select e, c
from (
select e, c, a
from (
Select e, c, a, b
from p3
where (37 = d)
) T1
union all
select c, a, b
from (
Select c, a, b
from p1
where (a > c)
) T2
) T2
) T2(c_l_r_l_r, a_r_r_l_r)
on ((a_l > 69) AND ((c_l_r_l_r = 81) OR (23 > 4)))
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
    #*********************************************
    _testmgr.testcase_end(desc)

