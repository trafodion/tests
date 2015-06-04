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
    
def test001(desc="""Joins Set 13"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r_r, e_l_r
from (
Select d
from p5
where ((42 < (e - b)) OR ((67 = 89) OR (c > e)))
) T1(d_l)
left join (
Select e_l, b_r
from (
Select e
from p5
where (((b - e) = a) OR ((e > 31) OR (2 < 87)))
) T1(e_l)
inner join (
Select c, b
from p2
where ((e < (75 * 58)) OR ((e = (89 - e)) OR ((c = ((80 + ((a - 19) + 10)) - 85)) OR (e < d))))
) T2(c_r, b_r)
on (e_l = e_l)
) T2(e_l_r, b_r_r)
on (b_r_r < (62 * 57))
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
Select b_l, a_r_r
from (
Select b
from p4
where ((e + 64) = 77)
) T1(b_l)
full join (
Select d_l, a_r
from (
Select d
from p4
where ((17 = 12) OR (d = a))
) T1(d_l)
inner join (
Select a
from p3
where (c = 48)
) T2(a_r)
on (46 = (85 + d_l))
) T2(d_l_r, a_r_r)
on (72 = 18)
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
Select c_l_l, e_r_l, b_l_l, e_l_l_r
from (
Select c_l, b_l, e_r
from (
Select c, b
from p2
where (43 = c)
) T1(c_l, b_l)
left join (
Select e, d
from p2
where ((35 * c) = (b * d))
) T2(e_r, d_r)
on ((30 - 78) = ((62 * 70) + 66))
) T1(c_l_l, b_l_l, e_r_l)
full join (
Select e_l_l, e_r
from (
select e_l
from (
Select e_l, d_l, d_r
from (
Select e, d
from p5
where ((52 = (71 + b)) AND (e = ((48 + a) * c)))
) T1(e_l, d_l)
full join (
Select b, d
from p2
where ((13 > d) OR (63 = e))
) T2(b_r, d_r)
on (41 > 76)
) T1
union all
select a
from (
Select a
from p2
where ((b * (c * 56)) > c)
) T2
) T1(e_l_l)
left join (
Select e
from p3
where (d < d)
) T2(e_r)
on (e_l_l = e_r)
) T2(e_l_l_r, e_r_r)
on (((20 + (99 - b_l_l)) = 30) OR (e_r_l < c_l_l))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_r
from (
Select b
from p3
where (c < 57)
) T1(b_l)
left join (
Select d
from p4
where (e > ((c + 14) - c))
) T2(d_r)
on (b_l > (92 * (69 * 92)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_r
from (
Select c, a
from p2
where (((56 * b) = d) OR (35 > e))
) T1(c_l, a_l)
left join (
Select c
from p2
where (d < 17)
) T2(c_r)
on ((0 > (c_l + c_r)) AND ((c_l < c_r) OR (c_l = c_l)))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, a_r
from (
Select c, b
from p5
where ((d * 46) > b)
) T1(c_l, b_l)
left join (
Select a
from p2
where (((d - 32) > (b * 54)) OR ((85 = 72) AND (b < b)))
) T2(a_r)
on (1 < 36)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_r
from (
Select a, d
from p2
where (81 = (c + (c - 70)))
) T1(a_l, d_l)
inner join (
Select b
from p1
where (63 < 66)
) T2(b_r)
on ((d_l > b_r) AND (d_l < (26 * b_r)))
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
Select e_l, a_l, b_r, d_r
from (
Select e, a
from p2
where ((34 > ((12 + (a - c)) - e)) OR (27 > 87))
) T1(e_l, a_l)
left join (
Select b, d
from p3
where (c < 39)
) T2(b_r, d_r)
on ((68 = (d_r - 76)) AND (d_r < b_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l, c_r
from (
select d_l
from (
select d_l
from (
select d_l, e_r, c_r
from (
Select d_l, e_r, c_r
from (
Select d
from p3
where ((13 + 62) < (c + a))
) T1(d_l)
left join (
Select e, c
from p2
where (b = (37 + 80))
) T2(e_r, c_r)
on (45 < 88)
) T1
union all
select e_l, b_l_r_r, c_r_l_r
from (
Select e_l, b_l_r_r, c_r_l_r
from (
Select e
from p3
where ((3 * 73) = d)
) T1(e_l)
full join (
Select a_l_l, c_r_l, b_l_r
from (
select a_l, c_r, b_r
from (
Select a_l, c_r, b_r
from (
Select a
from p1
where ((a > d) AND (e > (c * 9)))
) T1(a_l)
full join (
Select c, b
from p2
where (88 > 92)
) T2(c_r, b_r)
on (a_l > c_r)
) T1
union all
select e, c, a
from (
Select e, c, a, b
from p4
where ((e = 14) AND ((96 = (a + 54)) OR ((74 + c) = 66)))
) T2
) T1(a_l_l, c_r_l, b_r_l)
full join (
Select e_l, b_l, c_l_r, d_r_r
from (
select e, b
from (
Select e, b
from p5
where (8 = 16)
) T1
union all
select e, c
from (
Select e, c, a
from p4
where (68 > d)
) T2
) T1(e_l, b_l)
full join (
Select c_l, d_r
from (
Select e, c
from p2
where (50 > 68)
) T1(e_l, c_l)
inner join (
Select b, d
from p5
where (((a + c) > (e * 32)) AND (95 < (c * b)))
) T2(b_r, d_r)
on (39 = d_r)
) T2(c_l_r, d_r_r)
on ((38 = 79) OR (e_l = ((48 * e_l) * d_r_r)))
) T2(e_l_r, b_l_r, c_l_r_r, d_r_r_r)
on (64 = c_r_l)
) T2(a_l_l_r, c_r_l_r, b_l_r_r)
on (64 > c_r_l_r)
) T2
) T1
union all
select a
from (
select a
from (
Select a
from p3
where (a < 84)
) T1
union all
select d
from (
Select d
from p2
where ((c - b) > a)
) T2
) T2
) T1
union all
select e
from (
Select e
from p4
where (a < a)
) T2
) T1(d_l_l)
inner join (
select c
from (
select c, a
from (
Select c, a, d
from p1
where ((3 < b) OR (c = b))
) T1
union all
select c, d
from (
Select c, d
from p4
where (22 < d)
) T2
) T1
union all
select d
from (
Select d
from p4
where (22 = e)
) T2
) T2(c_r)
on (d_l_l > 41)
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
Select c_l, d_l, a_r, b_r
from (
Select c, d
from p4
where (b = (38 - e))
) T1(c_l, d_l)
inner join (
Select a, b
from p3
where ((e < b) AND (34 = b))
) T2(a_r, b_r)
on (c_l = d_l)
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
select e, a, d
from (
Select e, a, d
from p5
where (e > e)
) T1
union all
select e, c, a
from (
Select e, c, a
from p3
where (41 = 63)
) T2
) T1(e_l, a_l, d_l)
left join (
Select c
from p4
where ((((35 + 51) - d) > (d + ((b + (((a - a) * 80) - c)) * 28))) OR (70 = e))
) T2(c_r)
on (c_r > e_l)
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
Select d_l, e_r, b_r
from (
Select d
from p4
where ((d < c) AND (a > ((a + 9) - a)))
) T1(d_l)
left join (
Select e, b, d
from p1
where (34 > e)
) T2(e_r, b_r, d_r)
on ((27 = e_r) OR (72 = 25))
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
Select e_l, b_l, a_r_r
from (
Select e, b, d
from p2
where (85 = a)
) T1(e_l, b_l, d_l)
inner join (
Select a_l_l, c_r_l, a_r
from (
Select a_l, c_r
from (
Select a
from p2
where ((56 = 13) AND ((e = d) OR ((a - d) = (c - c))))
) T1(a_l)
full join (
select c
from (
Select c
from p1
where (1 = (b + 34))
) T1
union all
select d
from (
Select d
from p5
where (87 < d)
) T2
) T2(c_r)
on ((25 < 81) OR ((c_r = 89) OR (7 > c_r)))
) T1(a_l_l, c_r_l)
full join (
Select a
from p2
where (b = 82)
) T2(a_r)
on (60 < 48)
) T2(a_l_l_r, c_r_l_r, a_r_r)
on ((70 > b_l) AND ((79 * (b_l - b_l)) < 10))
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
Select a_l, a_r
from (
Select a
from p5
where ((a < 43) OR ((15 < 61) AND (a = ((55 * c) + (a * 92)))))
) T1(a_l)
left join (
Select a
from p1
where (a > 72)
) T2(a_r)
on (19 < a_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_r_r, b_l_r
from (
Select c, b
from p3
where ((2 > 76) OR ((c = d) OR (((d - (66 - a)) - (c * a)) > 65)))
) T1(c_l, b_l)
left join (
Select b_l, d_r
from (
Select c, b
from p2
where ((9 < c) AND ((75 = b) OR (((68 - 46) < c) OR (93 = 66))))
) T1(c_l, b_l)
inner join (
Select d
from p5
where ((a > 40) AND (2 > (44 * a)))
) T2(d_r)
on (((d_r * 79) = b_l) OR (((b_l - ((((94 - 0) + (58 - b_l)) - d_r) + 16)) = b_l) OR (13 = (b_l - 61))))
) T2(b_l_r, d_r_r)
on (b_l = b_l_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, a_r, b_r
from (
Select e
from p1
where ((18 < a) OR (41 = e))
) T1(e_l)
left join (
Select e, c, a, b
from p4
where (60 = 10)
) T2(e_r, c_r, a_r, b_r)
on (52 > 73)
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
Select b_r_l, d_l_l, e_r
from (
select d_l, b_r
from (
Select d_l, b_r
from (
Select e, a, d
from p3
where ((64 = 76) AND (8 = a))
) T1(e_l, a_l, d_l)
full join (
select e, a, b
from (
Select e, a, b
from p3
where ((66 = d) AND (71 < (c * 37)))
) T1
union all
select b_l, c_r_r, e_r_r
from (
Select b_l, c_r_r, e_r_r
from (
Select e, c, b
from p4
where ((31 > b) OR (35 < c))
) T1(e_l, c_l, b_l)
inner join (
Select d_l_l_l, e_r, c_r
from (
Select c_l_l, c_r_l, d_l_l, d_r_r
from (
Select c_l, d_l, c_r
from (
Select c, d
from p1
where (74 = (e - 73))
) T1(c_l, d_l)
left join (
select c, d
from (
Select c, d
from p2
where ((e > (b + 65)) AND (((((75 * b) * d) + 3) = 41) OR ((4 = 69) AND (((d - 18) < b) AND (b = d)))))
) T1
union all
select c, a
from (
Select c, a, b
from p5
where ((e - 62) = b)
) T2
) T2(c_r, d_r)
on (80 = 93)
) T1(c_l_l, d_l_l, c_r_l)
full join (
Select e_l, c_l, d_r
from (
Select e, c
from p2
where (18 = b)
) T1(e_l, c_l)
left join (
Select c, d
from p4
where (2 < 16)
) T2(c_r, d_r)
on (d_r < 99)
) T2(e_l_r, c_l_r, d_r_r)
on (d_r_r = 4)
) T1(c_l_l_l, c_r_l_l, d_l_l_l, d_r_r_l)
inner join (
Select e, c
from p5
where ((74 * d) > b)
) T2(e_r, c_r)
on (d_l_l_l > (99 - e_r))
) T2(d_l_l_l_r, e_r_r, c_r_r)
on (5 > 29)
) T2
) T2(e_r, a_r, b_r)
on ((d_l > (42 * 68)) OR (d_l > 81))
) T1
union all
select a, d
from (
Select a, d
from p4
where (40 < a)
) T2
) T1(d_l_l, b_r_l)
left join (
select e
from (
Select e, a, d
from p3
where (30 = 18)
) T1
union all
select b
from (
Select b
from p1
where ((e + 8) < 87)
) T2
) T2(e_r)
on ((9 * 2) > 63)
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
Select d_l, e_r, d_r
from (
Select d
from p4
where ((e < 38) OR (24 = d))
) T1(d_l)
left join (
Select e, d
from p1
where ((90 > a) AND (54 < 12))
) T2(e_r, d_r)
on ((e_r * d_l) > e_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test13exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, e_r, a_r, b_r
from (
Select c
from p5
where (b = 19)
) T1(c_l)
left join (
Select e, a, b
from p5
where (c = (11 * b))
) T2(e_r, a_r, b_r)
on (58 > 27)
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
Select a_l_l, b_r_l, e_l_l, b_r
from (
Select e_l, c_l, a_l, b_r
from (
select e, c, a
from (
Select e, c, a, d
from p2
where ((27 = (31 * 22)) AND (66 = 47))
) T1
union all
select c_l, e_r, c_r
from (
Select c_l, e_r, c_r
from (
select c
from (
Select c
from p5
where ((87 - a) = 34)
) T1
union all
select e
from (
Select e
from p1
where (a > c)
) T2
) T1(c_l)
full join (
Select e, c
from p1
where (42 = 91)
) T2(e_r, c_r)
on ((c_r < (((37 * 39) - 21) * (e_r * (c_l + e_r)))) AND (c_r < c_l))
) T2
) T1(e_l, c_l, a_l)
inner join (
Select c, b
from p1
where (c < (65 * d))
) T2(c_r, b_r)
on ((93 > c_l) AND ((((c_l + b_r) + e_l) - 98) < 1))
) T1(e_l_l, c_l_l, a_l_l, b_r_l)
inner join (
Select b
from p1
where (77 > 91)
) T2(b_r)
on (94 > 48)
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
    #********************************************
    _testmgr.testcase_end(desc)

