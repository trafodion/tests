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
    
def test001(desc="""Joins Set 41"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l_l_l, c_r_l, e_r_l, e_r, c_r
from (
Select a_l_l, c_r_l, e_r, c_r
from (
Select a_l, b_l, c_r
from (
Select a, b
from p5
where (0 > 21)
) T1(a_l, b_l)
inner join (
Select e, c
from p2
where (44 = b)
) T2(e_r, c_r)
on (c_r < c_r)
) T1(a_l_l, b_l_l, c_r_l)
inner join (
select e, c
from (
Select e, c, d
from p2
where ((b * 26) > c)
) T1
union all
select b_l, c_r_r
from (
Select b_l, c_r_r
from (
Select b
from p4
where (c < e)
) T1(b_l)
left join (
Select c_l, b_l, c_r
from (
Select c, a, b
from p1
where (c > (31 + e))
) T1(c_l, a_l, b_l)
inner join (
select c
from (
select c
from (
Select c
from p2
where ((60 = (67 - d)) AND (a > d))
) T1
union all
select b
from (
Select b
from p2
where ((6 < (7 + b)) OR (70 = e))
) T2
) T1
union all
select e
from (
Select e, b
from p4
where (27 = 65)
) T2
) T2(c_r)
on ((76 + (c_r * c_l)) < 69)
) T2(c_l_r, b_l_r, c_r_r)
on (c_r_r < b_l)
) T2
) T2(e_r, c_r)
on (a_l_l < 69)
) T1(a_l_l_l, c_r_l_l, e_r_l, c_r_l)
inner join (
Select e, c, b
from p4
where (87 < (a * b))
) T2(e_r, c_r, b_r)
on (c_r_l < 60)
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
Select c_l_r_l, d_l_l, e_r
from (
Select d_l, c_l_r
from (
Select c, b, d
from p1
where (23 > d)
) T1(c_l, b_l, d_l)
inner join (
Select c_l, d_l_r
from (
Select c, d
from p2
where (31 = b)
) T1(c_l, d_l)
left join (
Select d_l, d_r_l_r, a_r_l_r
from (
Select c, a, d
from p4
where ((b < a) AND (66 < 19))
) T1(c_l, a_l, d_l)
left join (
Select d_r_l, a_r_l, d_r
from (
Select c_l, c_r, a_r, d_r
from (
Select c
from p5
where (57 = 66)
) T1(c_l)
left join (
Select c, a, d
from p2
where (e > 17)
) T2(c_r, a_r, d_r)
on ((24 > a_r) AND ((65 + 19) = c_l))
) T1(c_l_l, c_r_l, a_r_l, d_r_l)
left join (
Select c, d
from p1
where (d = 26)
) T2(c_r, d_r)
on (d_r < 9)
) T2(d_r_l_r, a_r_l_r, d_r_r)
on (66 < d_r_l_r)
) T2(d_l_r, d_r_l_r_r, a_r_l_r_r)
on (d_l_r = d_l_r)
) T2(c_l_r, d_l_r_r)
on ((43 = c_l_r) OR (88 = d_l))
) T1(d_l_l, c_l_r_l)
left join (
Select e
from p2
where (21 = 69)
) T2(e_r)
on ((e_r = d_l_l) OR (30 < 96))
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
Select c_r_l_l, e_r_l, b_r
from (
Select c_r_l, e_r
from (
Select a_l_l, d_r_l, e_r, c_r
from (
Select a_l, c_r, d_r
from (
Select c, a
from p1
where (((28 - b) = (c * 31)) OR ((23 = 32) OR (((79 + 63) = 91) AND ((a < 11) OR ((d + a) = d)))))
) T1(c_l, a_l)
inner join (
Select c, d
from p2
where ((c < d) AND ((d > 20) OR ((e = d) AND (41 = ((b - 48) * 52)))))
) T2(c_r, d_r)
on (a_l = 53)
) T1(a_l_l, c_r_l, d_r_l)
left join (
Select e, c, d
from p3
where (21 = 33)
) T2(e_r, c_r, d_r)
on ((d_r_l > d_r_l) AND ((84 = 0) OR ((e_r - e_r) = 82)))
) T1(a_l_l_l, d_r_l_l, e_r_l, c_r_l)
full join (
Select e
from p4
where ((67 * 69) = (95 + e))
) T2(e_r)
on ((c_r_l = e_r) AND ((e_r - (37 + e_r)) = 4))
) T1(c_r_l_l, e_r_l)
left join (
select e, b
from (
Select e, b, d
from p1
where ((a - e) > 26)
) T1
union all
select c_l, b_r
from (
Select c_l, b_r
from (
Select c, a, d
from p4
where ((a = a) OR (c < 64))
) T1(c_l, a_l, d_l)
left join (
Select b
from p1
where ((39 < c) AND ((e = e) OR (d = d)))
) T2(b_r)
on ((((b_r - (39 * 27)) - 10) > 28) AND ((6 > c_l) OR ((((c_l * (b_r + 15)) * c_l) > (66 - b_r)) OR (b_r < b_r))))
) T2
) T2(e_r, b_r)
on ((c_r_l_l < e_r_l) AND (59 = (98 * e_r_l)))
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
Select a_l, b_l, b_r_l_l_r, c_r_r
from (
Select a, b
from p2
where (4 < 45)
) T1(a_l, b_l)
inner join (
Select b_r_l_l, c_r
from (
Select b_r_l, b_r
from (
Select e_l, b_r
from (
Select e, d
from p5
where (81 > 65)
) T1(e_l, d_l)
inner join (
Select b
from p3
where (c = 65)
) T2(b_r)
on (b_r = e_l)
) T1(e_l_l, b_r_l)
left join (
Select c, b, d
from p5
where ((e = c) AND ((c < ((88 * 26) * d)) AND (7 = e)))
) T2(c_r, b_r, d_r)
on (b_r < 18)
) T1(b_r_l_l, b_r_l)
inner join (
Select c, d
from p3
where ((66 + d) = 59)
) T2(c_r, d_r)
on (((b_r_l_l + 46) = b_r_l_l) AND ((b_r_l_l = (c_r * (95 * 3))) AND ((74 * 71) = (c_r * ((24 * 64) + ((b_r_l_l - c_r) * c_r))))))
) T2(b_r_l_l_r, c_r_r)
on (((20 * (a_l * b_r_l_l_r)) > a_l) OR (((c_r_r * b_r_l_l_r) * 6) = 37))
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
Select a_r_l, a_r
from (
Select b_l, c_r, a_r
from (
Select c, b, d
from p3
where (e > 76)
) T1(c_l, b_l, d_l)
inner join (
Select c, a
from p5
where (70 > e)
) T2(c_r, a_r)
on ((52 = c_r) OR (a_r = (60 - a_r)))
) T1(b_l_l, c_r_l, a_r_l)
full join (
Select a
from p5
where ((31 > ((87 * c) - c)) AND ((e = b) OR (59 < 20)))
) T2(a_r)
on ((40 < a_r) OR (a_r_l = 7))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_r_l, b_r_l_l, c_r_l, a_l_r_r, d_r_r_r, d_l_r
from (
Select b_r_l, e_r_l_l, c_r, a_r
from (
Select e_r_l, b_r
from (
Select d_l, e_r
from (
Select e, d
from p4
where (((b + d) + 74) < (c + a))
) T1(e_l, d_l)
left join (
Select e, c, b
from p2
where (58 = 55)
) T2(e_r, c_r, b_r)
on ((40 + 49) = 32)
) T1(d_l_l, e_r_l)
inner join (
Select e, b
from p1
where ((8 + e) < 65)
) T2(e_r, b_r)
on ((e_r_l = (b_r - (b_r + (b_r * 33)))) AND ((70 = b_r) OR (61 > e_r_l)))
) T1(e_r_l_l, b_r_l)
left join (
Select c, a, b
from p3
where (b = 7)
) T2(c_r, a_r, b_r)
on (((c_r - 92) = a_r) AND ((98 = c_r) AND (99 = (b_r_l + c_r))))
) T1(b_r_l_l, e_r_l_l_l, c_r_l, a_r_l)
left join (
Select e_l, c_l, d_l, a_l_r, d_r_r
from (
Select e, c, a, d
from p3
where (c = 79)
) T1(e_l, c_l, a_l, d_l)
left join (
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from p4
where (((d - a) * e) = b)
) T1(a_l)
full join (
Select c, a, d
from p5
where (c = 96)
) T2(c_r, a_r, d_r)
on (44 = (11 - 56))
) T1
union all
select e, d
from (
select e, d
from (
Select e, d
from p4
where ((16 * d) > 64)
) T1
union all
select e, a
from (
Select e, a, b, d
from p2
where ((b = b) AND (a = (b - 28)))
) T2
) T2
) T2(a_l_r, d_r_r)
on ((e_l - 63) = d_r_r)
) T2(e_l_r, c_l_r, d_l_r, a_l_r_r, d_r_r_r)
on ((56 < 68) OR ((d_l_r = c_r_l) OR ((b_r_l_l + ((a_l_r_r + (a_r_l + (5 - (a_l_r_r - 22)))) + 46)) = a_l_r_r)))
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
    
    stmt = """prepare s1 from
Select b_l, c_r_r_r_r
from (
Select e, b, d
from p3
where ((19 - b) = 13)
) T1(e_l, b_l, d_l)
inner join (
Select a_l_l, d_l_r_l, e_l_r, c_r_r_r
from (
Select a_l, d_l, d_l_r
from (
Select a, d
from p4
where (d = (e * (e - e)))
) T1(a_l, d_l)
inner join (
select a_l, d_l
from (
Select a_l, d_l, e_r
from (
Select a, d
from p5
where ((40 + d) > 23)
) T1(a_l, d_l)
full join (
Select e
from p1
where (((c - 22) > 0) OR ((14 - (42 + ((e - 27) - a))) > e))
) T2(e_r)
on (73 = 99)
) T1
union all
select e, d
from (
Select e, d
from p5
where ((37 * d) > ((97 + a) + c))
) T2
) T2(a_l_r, d_l_r)
on ((95 = d_l_r) AND ((d_l_r - 69) = d_l_r))
) T1(a_l_l, d_l_l, d_l_r_l)
full join (
Select e_l, b_l, c_l_r, c_r_r
from (
Select e, b
from p5
where ((b < (d + d)) AND (48 = c))
) T1(e_l, b_l)
left join (
select c_l, e_r, c_r
from (
Select c_l, e_r, c_r
from (
select c
from (
Select c
from p1
where ((83 - d) = c)
) T1
union all
select c
from (
Select c, d
from p3
where ((e * e) < 73)
) T2
) T1(c_l)
left join (
Select e, c
from p5
where (32 = e)
) T2(e_r, c_r)
on (e_r = e_r)
) T1
union all
select e, c, b
from (
Select e, c, b, d
from p2
where ((c = (b + b)) OR ((32 < (b - c)) AND (c = d)))
) T2
) T2(c_l_r, e_r_r, c_r_r)
on ((66 = 45) AND (85 > 39))
) T2(e_l_r, b_l_r, c_l_r_r, c_r_r_r)
on ((46 = ((c_r_r_r + 98) - (33 * 48))) AND (c_r_r_r = a_l_l))
) T2(a_l_l_r, d_l_r_l_r, e_l_r_r, c_r_r_r_r)
on (b_l > (c_r_r_r_r * (64 + b_l)))
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
Select c_l, e_r, b_r
from (
Select c
from p4
where (42 = 3)
) T1(c_l)
inner join (
Select e, b
from p4
where (33 = 62)
) T2(e_r, b_r)
on (b_r < 43)
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
Select c_l, b_r
from (
Select c, d
from p1
where ((c > (a * b)) AND (31 > 87))
) T1(c_l, d_l)
left join (
select b
from (
Select b
from p5
where (11 < 39)
) T1
union all
select e
from (
Select e
from p2
where (b = (c + e))
) T2
) T2(b_r)
on ((78 = (c_l + 92)) AND ((c_l = (4 + b_r)) OR ((b_r < c_l) OR (b_r = b_r))))
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
Select c_l, a_l, d_r
from (
Select e, c, a
from p5
where (b = 48)
) T1(e_l, c_l, a_l)
left join (
Select d
from p5
where (d = b)
) T2(d_r)
on ((79 - c_l) < c_l)
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
Select e_l_l, d_r
from (
select e_l
from (
Select e_l, b_l, e_r
from (
Select e, b
from p2
where ((87 = 63) AND (a = e))
) T1(e_l, b_l)
inner join (
select e, c
from (
Select e, c, a, d
from p2
where (a = a)
) T1
union all
select a_l, b_r
from (
Select a_l, b_r
from (
Select a
from p3
where ((a - (e + a)) > b)
) T1(a_l)
left join (
Select b
from p5
where (73 > c)
) T2(b_r)
on (a_l < ((82 + ((b_r + a_l) * b_r)) - a_l))
) T2
) T2(e_r, c_r)
on (e_r = 72)
) T1
union all
select d
from (
Select d
from p5
where ((((75 - 73) * b) * (61 - ((d - 84) * e))) = a)
) T2
) T1(e_l_l)
left join (
Select d
from p5
where ((41 < 47) OR ((((b + c) - a) + 13) = (b - 41)))
) T2(d_r)
on (5 = d_r)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r
from (
Select d
from p4
where ((a = (b - d)) AND (25 > (94 * e)))
) T1(d_l)
full join (
Select e, d
from p3
where ((d < 13) OR ((((51 * a) - (96 - (c * (49 + c)))) > a) OR ((41 < e) OR ((13 = (c - 81)) OR (60 = e)))))
) T2(e_r, d_r)
on ((d_l < ((52 + d_l) * (d_l - e_r))) OR (e_r > d_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r, b_r
from (
select d
from (
Select d
from p5
where ((d = e) OR (d = e))
) T1
union all
select e_l
from (
Select e_l, a_l, c_r, b_r
from (
Select e, a
from p3
where ((47 < 24) AND ((77 = 99) AND (e < c)))
) T1(e_l, a_l)
left join (
Select c, b
from p5
where (69 = e)
) T2(c_r, b_r)
on (((e_l - 44) = (a_l * c_r)) AND (17 > 36))
) T2
) T1(d_l)
full join (
Select e, c, b
from p5
where (66 = a)
) T2(e_r, c_r, b_r)
on ((42 = (((22 * e_r) * b_r) - (((d_l * d_l) * d_l) + b_r))) OR ((e_r = b_r) AND ((65 > ((d_l - d_l) - 41)) AND (65 < ((d_l + d_l) - d_l)))))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, a_r, b_r
from (
select e, c, b
from (
Select e, c, b
from p1
where (b = b)
) T1
union all
select e_l, b_l, c_r
from (
Select e_l, b_l, c_r
from (
Select e, a, b
from p3
where (64 > a)
) T1(e_l, a_l, b_l)
full join (
Select c
from p1
where (87 = a)
) T2(c_r)
on (c_r = 35)
) T2
) T1(e_l, c_l, b_l)
full join (
Select a, b
from p4
where (9 = (23 + 44))
) T2(a_r, b_r)
on (((60 * 52) > (91 + 59)) OR ((75 = (70 + 18)) OR (b_l < (c_l - b_r))))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, c_l_r
from (
Select c, b
from p4
where ((98 > e) OR (b = 18))
) T1(c_l, b_l)
left join (
Select c_l, d_l, a_l_r, d_l_r_r
from (
Select c, b, d
from p5
where (d > d)
) T1(c_l, b_l, d_l)
left join (
select c_l, a_l, e_r_r, d_l_r
from (
Select c_l, a_l, e_r_r, d_l_r
from (
Select c, a, b
from p5
where (b < d)
) T1(c_l, a_l, b_l)
full join (
Select d_l, e_r, b_r
from (
Select d
from p4
where ((33 = d) OR (a > 89))
) T1(d_l)
full join (
Select e, b
from p2
where ((74 - 59) < 40)
) T2(e_r, b_r)
on ((e_r * 98) = d_l)
) T2(d_l_r, e_r_r, b_r_r)
on (90 > ((28 - (92 * 48)) + (((c_l * c_l) * d_l_r) * (((d_l_r + a_l) + 78) + a_l))))
) T1
union all
select e, a, b, d
from (
Select e, a, b, d
from p4
where ((b > a) OR (d = 72))
) T2
) T2(c_l_r, a_l_r, e_r_r_r, d_l_r_r)
on ((a_l_r + a_l_r) < 28)
) T2(c_l_r, d_l_r, a_l_r_r, d_l_r_r_r)
on ((60 * 11) < (c_l * 46))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, e_r, c_r
from (
select d
from (
Select d
from p1
where (72 < d)
) T1
union all
select e
from (
Select e, c
from p5
where (c = d)
) T2
) T1(d_l)
inner join (
Select e, c
from p5
where (33 = e)
) T2(e_r, c_r)
on (65 < d_l)
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
Select e_l, a_l, d_l, b_r
from (
Select e, a, d
from p5
where ((c = (96 - c)) OR ((e = c) AND (66 > (12 + 26))))
) T1(e_l, a_l, d_l)
full join (
Select b
from p4
where (14 < c)
) T2(b_r)
on (35 = (e_l - 44))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_l_r
from (
select c
from (
Select c, b
from p3
where (93 > d)
) T1
union all
select b
from (
Select b
from p4
where (c < c)
) T2
) T1(c_l)
left join (
select c_l
from (
Select c_l, e_r_r
from (
Select c
from p2
where (7 < 29)
) T1(c_l)
inner join (
select b_l_r_l_l_l_l, e_r, b_r
from (
Select b_l_r_l_l_l_l, e_r, b_r
from (
Select b_l_r_l_l_l, c_r_l, a_r, d_r
from (
Select b_r_l, b_l_r_l_l, c_r, b_r
from (
Select b_l_r_l, c_r, a_r, b_r
from (
Select b_l, e_l_r, b_l_r
from (
Select b
from p1
where ((d < 4) AND (c < a))
) T1(b_l)
full join (
Select e_l, b_l, d_l_r_r_r, a_l_l_r, b_l_l_r_r
from (
Select e, b
from p1
where ((b = d) AND (b = a))
) T1(e_l, b_l)
full join (
Select a_l_l, e_r_l, c_l_l_r, b_l_l_r, d_l_r_r
from (
Select c_l, a_l, e_r
from (
Select c, a
from p4
where (94 < b)
) T1(c_l, a_l)
left join (
Select e
from p1
where ((22 < d) AND ((d > 56) AND (45 = e)))
) T2(e_r)
on (a_l > c_l)
) T1(c_l_l, a_l_l, e_r_l)
left join (
Select b_r_l, c_l_l, b_l_l, d_l_r
from (
Select c_l, b_l, b_r
from (
Select c, b
from p1
where (e > (d + (49 - b)))
) T1(c_l, b_l)
full join (
Select e, b
from p1
where (77 = 48)
) T2(e_r, b_r)
on (b_l = 36)
) T1(c_l_l, b_l_l, b_r_l)
full join (
Select d_l, e_r
from (
Select d
from p5
where (b = 20)
) T1(d_l)
inner join (
Select e, a
from p4
where ((b > 6) AND (c < b))
) T2(e_r, a_r)
on (69 > e_r)
) T2(d_l_r, e_r_r)
on (d_l_r = 37)
) T2(b_r_l_r, c_l_l_r, b_l_l_r, d_l_r_r)
on ((63 + (c_l_l_r * 66)) > (d_l_r_r - 33))
) T2(a_l_l_r, e_r_l_r, c_l_l_r_r, b_l_l_r_r, d_l_r_r_r)
on (e_l < b_l)
) T2(e_l_r, b_l_r, d_l_r_r_r_r, a_l_l_r_r, b_l_l_r_r_r)
on ((b_l_r + (b_l_r - 65)) > b_l)
) T1(b_l_l, e_l_r_l, b_l_r_l)
left join (
Select c, a, b, d
from p1
where ((c > 75) AND (39 > (a - 58)))
) T2(c_r, a_r, b_r, d_r)
on (8 = 5)
) T1(b_l_r_l_l, c_r_l, a_r_l, b_r_l)
left join (
Select c, b
from p3
where (66 = 95)
) T2(c_r, b_r)
on (93 = 6)
) T1(b_r_l_l, b_l_r_l_l_l, c_r_l, b_r_l)
left join (
Select a, d
from p5
where ((d - 26) = 51)
) T2(a_r, d_r)
on (25 = a_r)
) T1(b_l_r_l_l_l_l, c_r_l_l, a_r_l, d_r_l)
left join (
Select e, c, b
from p4
where (35 > 28)
) T2(e_r, c_r, b_r)
on (34 < b_l_r_l_l_l_l)
) T1
union all
select c, b, d
from (
Select c, b, d
from p5
where (b = 52)
) T2
) T2(b_l_r_l_l_l_l_r, e_r_r, b_r_r)
on ((5 < e_r_r) AND ((18 + c_l) > 28))
) T1
union all
select a
from (
select a
from (
Select a, b
from p2
where (73 = 58)
) T1
union all
select a
from (
Select a
from p1
where ((24 = (c * 75)) OR (12 > d))
) T2
) T2
) T2(c_l_r)
on ((c_l = (69 + c_l)) OR (c_l = c_l_r))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, b_l, d_l, b_r_r_r
from (
Select c, b, d
from p5
where (((d * e) * 64) > d)
) T1(c_l, b_l, d_l)
left join (
Select b_l, b_r_r
from (
Select b, d
from p2
where (((a - 88) > 22) OR (a > a))
) T1(b_l, d_l)
inner join (
select c_l, e_r, b_r
from (
Select c_l, e_r, b_r
from (
Select c
from p2
where ((e - (e * c)) = 97)
) T1(c_l)
inner join (
Select e, b, d
from p5
where (31 = b)
) T2(e_r, b_r, d_r)
on (((47 + 36) = (b_r * ((c_l + 82) - 74))) OR ((43 = 14) AND (e_r = 20)))
) T1
union all
select e, b, d
from (
Select e, b, d
from p1
where (57 < (e - (16 - 61)))
) T2
) T2(c_l_r, e_r_r, b_r_r)
on (((b_l + 13) = 65) AND (32 = (62 * b_l)))
) T2(b_l_r, b_r_r_r)
on ((39 > b_r_r_r) OR (b_l = 29))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test41exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_l_r, e_r_r
from (
Select e, d
from p5
where ((c < (b + 46)) AND ((b + (54 * 67)) = e))
) T1(e_l, d_l)
left join (
Select e_l, c_l, e_r, b_r
from (
Select e, c
from p4
where ((a = 19) OR ((55 * c) = 90))
) T1(e_l, c_l)
full join (
Select e, b
from p5
where ((e = c) OR ((((a * b) + c) < 38) OR ((d < 97) AND (10 = 32))))
) T2(e_r, b_r)
on (51 = (35 - 30))
) T2(e_l_r, c_l_r, e_r_r, b_r_r)
on (e_r_r = (56 + c_l_r))
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
    #*****************
    _testmgr.testcase_end(desc)

