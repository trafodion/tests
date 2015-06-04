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
    
def test001(desc="""Joins Set 45"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, e_r, b_r
from (
Select a, d
from p3
where (4 < 34)
) T1(a_l, d_l)
inner join (
Select e, b, d
from p4
where (d = e)
) T2(e_r, b_r, d_r)
on (b_r > a_l)
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
Select a_l_l, e_l_r_r_l, e_r
from (
select e_l, a_l, e_l_r_r
from (
Select e_l, a_l, e_l_r_r
from (
Select e, c, a
from p4
where (a < 43)
) T1(e_l, c_l, a_l)
left join (
Select e_l, e_l_r
from (
select e
from (
Select e, d
from p3
where (33 = 43)
) T1
union all
select e
from (
Select e
from p3
where (4 > 51)
) T2
) T1(e_l)
full join (
Select e_l, d_r
from (
select e, a
from (
Select e, a
from p4
where (62 = e)
) T1
union all
select c_l, d_r
from (
Select c_l, d_r
from (
Select c, b
from p3
where (((26 * (c * e)) = a) OR (b = ((b + b) - a)))
) T1(c_l, b_l)
left join (
Select a, b, d
from p1
where (e > a)
) T2(a_r, b_r, d_r)
on ((((71 * 80) * d_r) > 26) AND ((c_l < d_r) AND (c_l > (26 + 37))))
) T2
) T1(e_l, a_l)
left join (
Select e, a, d
from p5
where ((37 < c) AND ((51 > d) AND ((a - e) < c)))
) T2(e_r, a_r, d_r)
on (d_r = 41)
) T2(e_l_r, d_r_r)
on ((76 > e_l) OR ((e_l * (e_l_r - e_l)) > 45))
) T2(e_l_r, e_l_r_r)
on ((42 = 43) OR ((72 - e_l) > (32 * (e_l + (1 + ((95 * 69) + a_l))))))
) T1
union all
select e, c, a
from (
Select e, c, a
from p3
where (59 > (33 - c))
) T2
) T1(e_l_l, a_l_l, e_l_r_r_l)
inner join (
Select e
from p2
where (d < b)
) T2(e_r)
on (a_l_l = (87 + (31 + (27 * 41))))
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
Select b_r_l, d_l_l, a_r
from (
Select d_l, e_r, b_r
from (
Select d
from p1
where (c = 30)
) T1(d_l)
inner join (
select e, b
from (
Select e, b
from p5
where (26 = 60)
) T1
union all
select c, b
from (
Select c, b
from p4
where (e = b)
) T2
) T2(e_r, b_r)
on ((79 - e_r) < b_r)
) T1(d_l_l, e_r_l, b_r_l)
full join (
Select a
from p2
where (78 = 20)
) T2(a_r)
on (80 < 65)
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
Select e_l, c_r, a_r
from (
select e
from (
Select e, a, b
from p3
where ((94 = b) AND (((e * (85 + 46)) < 2) OR ((a < e) OR (37 = 76))))
) T1
union all
select a
from (
Select a
from p2
where (88 < (92 * 24))
) T2
) T1(e_l)
left join (
Select c, a
from p4
where ((68 > d) OR (((70 * 69) - 18) = 5))
) T2(c_r, a_r)
on (63 = 57)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_r, a_r
from (
Select e, c, a, d
from p4
where (97 = 21)
) T1(e_l, c_l, a_l, d_l)
full join (
Select c, a, b
from p5
where ((24 * c) = e)
) T2(c_r, a_r, b_r)
on ((a_r + (32 - (49 + 47))) > (91 - 82))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, e_r, a_r
from (
Select e, d
from p4
where (c = c)
) T1(e_l, d_l)
left join (
Select e, a
from p1
where (a = d)
) T2(e_r, a_r)
on (a_r > e_l)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l_l, e_l_l, e_r_l, d_r
from (
Select e_l, c_l, e_r, b_r
from (
Select e, c
from p5
where ((((e - 74) + (a - (b * 21))) > a) AND ((e = b) AND ((15 * c) < d)))
) T1(e_l, c_l)
left join (
Select e, b
from p1
where (e > (64 * 13))
) T2(e_r, b_r)
on (95 < b_r)
) T1(e_l_l, c_l_l, e_r_l, b_r_l)
left join (
Select d
from p5
where ((11 + d) < 50)
) T2(d_r)
on (d_r = 78)
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
Select c_l, b_l, b_l_r_r, b_l_r
from (
Select c, b
from p2
where (e < e)
) T1(c_l, b_l)
full join (
Select b_l, d_r_r, b_l_r
from (
select b
from (
Select b
from p2
where ((e = e) OR (d = c))
) T1
union all
select c
from (
Select c
from p4
where (97 > d)
) T2
) T1(b_l)
left join (
Select b_l, d_r
from (
Select e, c, b, d
from p2
where ((c = 38) AND ((e * (79 * 90)) = (72 * d)))
) T1(e_l, c_l, b_l, d_l)
left join (
Select d
from p5
where (89 = 26)
) T2(d_r)
on ((d_r = d_r) OR ((7 < 52) OR ((41 < d_r) AND (b_l > d_r))))
) T2(b_l_r, d_r_r)
on ((d_r_r = 63) AND (87 = b_l))
) T2(b_l_r, d_r_r_r, b_l_r_r)
on ((92 = (b_l_r_r - 77)) AND (b_l > b_l_r_r))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, c_r_l, b_r
from (
Select e_l, c_l, c_r, a_r
from (
Select e, c
from p5
where (15 < (93 + 86))
) T1(e_l, c_l)
full join (
Select c, a
from p3
where (a = 27)
) T2(c_r, a_r)
on ((e_l - (e_l - (58 + ((61 + c_r) - 50)))) < a_r)
) T1(e_l_l, c_l_l, c_r_l, a_r_l)
full join (
Select b
from p5
where (b < 0)
) T2(b_r)
on (((((76 - 71) - b_r) * b_r) > 8) AND (55 < 59))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, d_l, b_r_r, d_l_r
from (
Select e, c, d
from p1
where ((5 < 71) AND (c = (((c - 0) * 22) + a)))
) T1(e_l, c_l, d_l)
left join (
Select d_l, b_r
from (
Select a, b, d
from p5
where (e = 51)
) T1(a_l, b_l, d_l)
inner join (
Select e, b
from p1
where (c = 38)
) T2(e_r, b_r)
on (b_r = d_l)
) T2(d_l_r, b_r_r)
on (((d_l - 42) = c_l) OR (((1 + d_l_r) = 54) OR (d_l = 18)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l_l_r_l, c_r_r_l, b_l_r_r_r_r
from (
Select d_l, b_r_l_l_r, c_r_l_r, c_r_r
from (
Select e, d
from p3
where ((d * a) = b)
) T1(e_l, d_l)
left join (
Select b_r_l_l, c_r_l_l, c_r_l, c_r
from (
Select b_r_l, c_r_l, c_r
from (
Select e_l, c_r, b_r
from (
Select e
from p5
where (d < 89)
) T1(e_l)
inner join (
select c, b
from (
Select c, b
from p3
where ((c * e) = (47 - d))
) T1
union all
select c, b
from (
Select c, b
from p2
where ((1 + 95) = (e - 50))
) T2
) T2(c_r, b_r)
on ((e_l > 93) OR (e_l = 28))
) T1(e_l_l, c_r_l, b_r_l)
full join (
Select c, d
from p1
where (b > 15)
) T2(c_r, d_r)
on ((56 + 12) = 70)
) T1(b_r_l_l, c_r_l_l, c_r_l)
left join (
Select c, a, b, d
from p5
where (((47 - b) = 32) OR (98 = (21 * 56)))
) T2(c_r, a_r, b_r, d_r)
on ((18 = (c_r_l_l * (c_r * 58))) AND (94 = c_r_l_l))
) T2(b_r_l_l_r, c_r_l_l_r, c_r_l_r, c_r_r)
on (((56 + 20) = (b_r_l_l_r * b_r_l_l_r)) AND (((34 + b_r_l_l_r) * (c_r_l_r - (26 * (60 - d_l)))) = b_r_l_l_r))
) T1(d_l_l, b_r_l_l_r_l, c_r_l_r_l, c_r_r_l)
left join (
Select b_l, b_l_r_r_r
from (
Select c, b, d
from p4
where (53 = e)
) T1(c_l, b_l, d_l)
full join (
Select c_l, b_l, b_l_r_r, b_l_r
from (
Select c, b
from p2
where (74 > 84)
) T1(c_l, b_l)
left join (
Select a_l, b_l, b_l_r
from (
Select a, b
from p1
where (c = 2)
) T1(a_l, b_l)
inner join (
Select b_l, a_r
from (
Select e, c, b
from p3
where (a > 80)
) T1(e_l, c_l, b_l)
full join (
Select a
from p1
where (((c + e) < (c + a)) OR (e = (e - 32)))
) T2(a_r)
on (41 > 8)
) T2(b_l_r, a_r_r)
on (99 < (a_l + 7))
) T2(a_l_r, b_l_r, b_l_r_r)
on (b_l > b_l_r)
) T2(c_l_r, b_l_r, b_l_r_r_r, b_l_r_r)
on (45 > 78)
) T2(b_l_r, b_l_r_r_r_r)
on ((b_l_r_r_r_r * (24 - b_l_r_r_r_r)) > 51)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l_l, e_r_l, a_r_r_r
from (
Select b_r_l, d_l_l, e_r, b_r
from (
Select d_l, b_r
from (
Select d
from p2
where (((b * (b + 49)) = 30) AND (((3 * d) > 64) OR (c < d)))
) T1(d_l)
left join (
Select b
from p2
where ((15 = 61) OR ((b > 61) AND (e > 10)))
) T2(b_r)
on (41 > 3)
) T1(d_l_l, b_r_l)
full join (
Select e, b
from p2
where ((c < (d - d)) AND ((9 > 47) AND (a < 43)))
) T2(e_r, b_r)
on (64 < 58)
) T1(b_r_l_l, d_l_l_l, e_r_l, b_r_l)
left join (
Select b_l, d_l, a_r_r
from (
Select b, d
from p4
where ((e = d) AND ((a > 11) AND ((0 - b) = 43)))
) T1(b_l, d_l)
left join (
Select e_l, c_r, a_r
from (
Select e, d
from p5
where ((c * e) = ((41 + 22) * d))
) T1(e_l, d_l)
inner join (
Select c, a
from p5
where (a = a)
) T2(c_r, a_r)
on ((a_r * 3) < 87)
) T2(e_l_r, c_r_r, a_r_r)
on ((b_l > 96) AND (d_l < d_l))
) T2(b_l_r, d_l_r, a_r_r_r)
on ((18 = (a_r_r_r * 80)) AND ((((a_r_r_r + 68) - (a_r_r_r * e_r_l)) = 91) AND (80 > 41)))
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
from p3
where (67 = b)
) T1(a_l)
left join (
select a
from (
Select a, b
from p2
where ((24 = 93) AND (40 = b))
) T1
union all
select b
from (
Select b
from p1
where (e = 96)
) T2
) T2(a_r)
on ((3 = a_r) OR ((21 = a_r) AND ((a_r < a_l) OR (((95 * 15) > a_r) AND ((10 - a_r) = 62)))))
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
Select e_l, c_l, a_r
from (
Select e, c, b
from p4
where ((e < e) OR ((e * 48) < (d * 36)))
) T1(e_l, c_l, b_l)
inner join (
Select a
from p3
where (82 > b)
) T2(a_r)
on (c_l = c_l)
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
Select e_l, c_l, c_r, a_r
from (
Select e, c, d
from p2
where ((e < 59) OR (d > a))
) T1(e_l, c_l, d_l)
left join (
select c, a, b
from (
Select c, a, b
from p1
where (9 < (23 * d))
) T1
union all
select c_l_l, b_r_l, d_l_l
from (
Select c_l_l, b_r_l, d_l_l, c_l_r, a_r_r, e_r_r
from (
Select c_l, a_l, d_l, b_r
from (
Select c, a, d
from p4
where ((b = (a + 74)) OR (((a + a) > 94) AND ((b * e) = 95)))
) T1(c_l, a_l, d_l)
left join (
Select a, b
from p3
where (a = a)
) T2(a_r, b_r)
on (b_r = 80)
) T1(c_l_l, a_l_l, d_l_l, b_r_l)
inner join (
Select c_l, e_r, a_r
from (
Select c
from p2
where (b = e)
) T1(c_l)
inner join (
Select e, a, d
from p5
where (((18 - 81) + 2) > b)
) T2(e_r, a_r, d_r)
on (19 > (c_l * (64 + c_l)))
) T2(c_l_r, e_r_r, a_r_r)
on (c_l_r < a_r_r)
) T2
) T2(c_r, a_r, b_r)
on (c_l = 93)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, c_r
from (
Select e, d
from p4
where (((1 * d) - a) > 52)
) T1(e_l, d_l)
left join (
Select c
from p4
where (87 < b)
) T2(c_r)
on ((d_l > 20) AND (d_l < 14))
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
Select a_r_l, c_l_r, d_r_r
from (
Select b_l, a_r, b_r
from (
Select a, b, d
from p3
where (c > (16 + 48))
) T1(a_l, b_l, d_l)
inner join (
Select a, b, d
from p3
where ((b - (85 * 19)) = a)
) T2(a_r, b_r, d_r)
on ((b_l = 0) AND (6 = b_l))
) T1(b_l_l, a_r_l, b_r_l)
left join (
Select c_l, a_l, c_r, d_r
from (
Select c, a, b
from p2
where ((b > 82) AND (24 = c))
) T1(c_l, a_l, b_l)
inner join (
Select c, d
from p5
where ((d + 93) = (7 - a))
) T2(c_r, d_r)
on (57 > 22)
) T2(c_l_r, a_l_r, c_r_r, d_r_r)
on (72 = 23)
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
Select a_r_l, d_r_l_l, e_r
from (
Select d_r_l, a_r
from (
Select d_l, b_r, d_r
from (
Select a, d
from p4
where ((e < b) AND ((10 + c) = c))
) T1(a_l, d_l)
full join (
Select b, d
from p3
where (13 = (76 + a))
) T2(b_r, d_r)
on (18 = 16)
) T1(d_l_l, b_r_l, d_r_l)
left join (
Select a
from p2
where ((e = c) AND (((c + ((a - c) - 30)) = e) OR (c < (d - (29 - e)))))
) T2(a_r)
on ((a_r * d_r_l) = d_r_l)
) T1(d_r_l_l, a_r_l)
full join (
Select e
from p1
where ((b = (0 - b)) OR (57 = b))
) T2(e_r)
on (8 > a_r_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test45exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_l_l, d_l_r_l_l, e_r, d_r
from (
Select c_l_r_l, d_l_r_l, d_l_l, e_r_r
from (
Select d_l, b_r_r, c_l_r, d_l_r
from (
Select c, d
from p5
where (74 = d)
) T1(c_l, d_l)
full join (
Select c_l, d_l, e_r, b_r
from (
Select e, c, d
from p4
where (e = 73)
) T1(e_l, c_l, d_l)
left join (
Select e, b
from p2
where (d = 22)
) T2(e_r, b_r)
on ((((e_r + 98) + b_r) > c_l) AND (e_r = d_l))
) T2(c_l_r, d_l_r, e_r_r, b_r_r)
on (c_l_r > (26 + 28))
) T1(d_l_l, b_r_r_l, c_l_r_l, d_l_r_l)
full join (
select a_l, e_r
from (
Select a_l, e_r, a_r
from (
Select a
from p1
where (10 > 13)
) T1(a_l)
left join (
Select e, a
from p2
where (c = 7)
) T2(e_r, a_r)
on ((a_r < 63) AND (a_l > a_l))
) T1
union all
select e, b
from (
Select e, b
from p1
where ((e < b) AND (12 = (((64 + 82) * 80) - 4)))
) T2
) T2(a_l_r, e_r_r)
on (c_l_r_l > d_l_l)
) T1(c_l_r_l_l, d_l_r_l_l, d_l_l_l, e_r_r_l)
full join (
Select e, d
from p1
where (36 = c)
) T2(e_r, d_r)
on (7 = 93)
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
Select b_l, e_r
from (
Select b
from p3
where (b > (a + ((37 + (27 * (d + (36 * (b * e))))) + 26)))
) T1(b_l)
left join (
Select e, b
from p1
where (2 = 30)
) T2(e_r, b_r)
on (b_l = 5)
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
    #*******************
    _testmgr.testcase_end(desc)

