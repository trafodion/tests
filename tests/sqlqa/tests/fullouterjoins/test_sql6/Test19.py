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
    
def test001(desc="""Joins Set 19"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, c_l_l, c_r_l, a_r
from (
Select c_l, c_r, b_r, d_r
from (
Select c
from p1
where ((e = (d - b)) OR ((89 > a) OR (e = b)))
) T1(c_l)
inner join (
Select c, b, d
from p3
where (62 > 49)
) T2(c_r, b_r, d_r)
on (d_r > c_r)
) T1(c_l_l, c_r_l, b_r_l, d_r_l)
inner join (
Select a
from p4
where (e < 94)
) T2(a_r)
on (1 = (c_r_l - c_r_l))
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
Select c_l, b_l, b_r_r, b_r_l_r
from (
Select c, b, d
from p4
where (a = 69)
) T1(c_l, b_l, d_l)
inner join (
Select b_r_l, e_l_l, b_r
from (
Select e_l, a_l, e_r, b_r, d_r
from (
Select e, a, d
from p5
where ((e < (28 + (38 - 58))) AND (66 = c))
) T1(e_l, a_l, d_l)
left join (
Select e, b, d
from p3
where (81 = e)
) T2(e_r, b_r, d_r)
on (90 = 95)
) T1(e_l_l, a_l_l, e_r_l, b_r_l, d_r_l)
left join (
Select b, d
from p3
where (85 > c)
) T2(b_r, d_r)
on ((b_r * b_r_l) < b_r_l)
) T2(b_r_l_r, e_l_l_r, b_r_r)
on ((b_r_l_r < 6) AND ((75 + c_l) > b_r_l_r))
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
Select b_l_r_l, d_l_l, b_l_r_r, d_r_r_r_r
from (
Select d_l, b_l_r
from (
Select e, c, b, d
from p5
where ((((61 * 1) - d) * (e - e)) > 97)
) T1(e_l, c_l, b_l, d_l)
left join (
select b_l
from (
Select b_l, a_r
from (
select b
from (
Select b
from p1
where (b = 68)
) T1
union all
select e_l
from (
Select e_l, c_l, a_l, a_r
from (
Select e, c, a
from p1
where (a = (e + a))
) T1(e_l, c_l, a_l)
left join (
Select a
from p3
where (c < b)
) T2(a_r)
on ((75 * 48) = e_l)
) T2
) T1(b_l)
inner join (
Select e, a
from p5
where (86 < (d - a))
) T2(e_r, a_r)
on ((95 = 51) OR ((b_l > a_r) OR ((b_l > b_l) AND (((88 - a_r) = a_r) OR (((25 * a_r) = b_l) OR ((a_r = b_l) OR ((b_l < b_l) OR ((b_l * 27) = 20))))))))
) T1
union all
select c
from (
Select c
from p2
where ((e = 37) OR (b = 21))
) T2
) T2(b_l_r)
on (d_l > 88)
) T1(d_l_l, b_l_r_l)
inner join (
Select a_l, b_l, d_r_r_r, b_l_r
from (
Select a, b
from p2
where ((95 > (90 - (c + c))) OR (69 < (e + 0)))
) T1(a_l, b_l)
left join (
Select b_l, d_l, d_r_r
from (
Select b, d
from p2
where (20 < (47 * (e - (89 + 34))))
) T1(b_l, d_l)
left join (
Select a_l, b_r, d_r
from (
Select e, a, b
from p5
where ((c = 53) OR (a > 74))
) T1(e_l, a_l, b_l)
left join (
Select b, d
from p3
where (a < (59 + a))
) T2(b_r, d_r)
on ((d_r = (a_l + a_l)) AND ((d_r > a_l) AND ((71 < 88) OR (d_r > 17))))
) T2(a_l_r, b_r_r, d_r_r)
on ((74 < d_r_r) AND ((42 = 12) OR (d_r_r > d_l)))
) T2(b_l_r, d_l_r, d_r_r_r)
on ((38 > (24 * 37)) OR (b_l < d_r_r_r))
) T2(a_l_r, b_l_r, d_r_r_r_r, b_l_r_r)
on ((((b_l_r_l * (66 - b_l_r_l)) * b_l_r_r) * b_l_r_r) < (b_l_r_r - 66))
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
Select b_l, a_r
from (
select a, b
from (
Select a, b
from p2
where (b = 82)
) T1
union all
select c, b
from (
Select c, b, d
from p5
where ((92 * 99) = 78)
) T2
) T1(a_l, b_l)
left join (
Select e, a
from p4
where (90 < 0)
) T2(e_r, a_r)
on (63 < (b_l * 26))
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
Select a_l_l, e_r_r_l, d_r_r, a_r_r
from (
Select e_l, c_l, a_l, e_r_r
from (
Select e, c, a, d
from p1
where (18 < 24)
) T1(e_l, c_l, a_l, d_l)
left join (
Select e_l, e_r
from (
Select e, a
from p3
where (31 < 94)
) T1(e_l, a_l)
left join (
Select e, c
from p5
where ((b < a) OR ((e - 94) = 18))
) T2(e_r, c_r)
on ((83 < e_l) AND ((55 > e_r) AND (e_l = e_l)))
) T2(e_l_r, e_r_r)
on (a_l < 7)
) T1(e_l_l, c_l_l, a_l_l, e_r_r_l)
left join (
Select a_l, b_l, a_r, d_r
from (
select a, b
from (
Select a, b
from p4
where ((e < 43) AND (58 < 55))
) T1
union all
select c, a
from (
Select c, a
from p1
where ((61 * 88) = ((e + (b + (c * 72))) + 0))
) T2
) T1(a_l, b_l)
left join (
select a, d
from (
Select a, d
from p5
where ((b * 96) > 55)
) T1
union all
select e, b
from (
Select e, b
from p3
where (18 = c)
) T2
) T2(a_r, d_r)
on (b_l = 83)
) T2(a_l_r, b_l_r, a_r_r, d_r_r)
on ((95 > a_l_l) AND (82 > (15 + d_r_r)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, b_r
from (
Select e, d
from p4
where ((e = a) OR ((50 + c) = (c * 76)))
) T1(e_l, d_l)
full join (
Select b
from p2
where (a = 13)
) T2(b_r)
on (e_l = ((94 - 71) * d_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, e_r, a_r
from (
Select a, b
from p5
where (e = d)
) T1(a_l, b_l)
inner join (
Select e, a
from p4
where (((a - e) < c) AND ((d - ((3 * d) + a)) < d))
) T2(e_r, a_r)
on (((e_r * 91) < e_r) AND (62 < 41))
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
Select b_l, d_r
from (
Select e, b
from p1
where ((54 = 86) AND ((91 > (d + a)) OR (a < ((d - e) - d))))
) T1(e_l, b_l)
left join (
Select c, d
from p2
where (c < 51)
) T2(c_r, d_r)
on (d_r = d_r)
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
Select c_l, a_r_r_r, d_l_l_l_r
from (
select c
from (
Select c
from p1
where (e = c)
) T1
union all
select a_r_l
from (
Select a_r_l, b_r_l_l, b_r
from (
Select b_r_l, a_r
from (
Select d_l, b_r
from (
Select e, b, d
from p5
where (59 > e)
) T1(e_l, b_l, d_l)
left join (
Select b
from p1
where ((53 < c) OR ((b = c) AND (73 = ((c - e) + 81))))
) T2(b_r)
on ((d_l + 28) = b_r)
) T1(d_l_l, b_r_l)
full join (
Select a, b
from p2
where (((c * 78) - 91) = c)
) T2(a_r, b_r)
on ((((71 - (65 * (a_r * b_r_l))) - (31 - (17 - b_r_l))) * a_r) < b_r_l)
) T1(b_r_l_l, a_r_l)
left join (
select b
from (
Select b
from p5
where (87 > a)
) T1
union all
select a
from (
Select a
from p1
where (d = (d * e))
) T2
) T2(b_r)
on (b_r_l_l < a_r_l)
) T2
) T1(c_l)
left join (
Select d_l_l_l, a_r_r
from (
Select e_l_l, d_l_l, e_r_l, d_r
from (
Select e_l, d_l, e_r
from (
Select e, d
from p1
where ((83 = (((11 - 96) - 7) * e)) AND ((57 > e) OR ((c = (28 - (b + b))) OR (d < a))))
) T1(e_l, d_l)
left join (
Select e, a
from p3
where (((d + a) = (22 - ((92 - a) - (((b + c) + c) - 65)))) AND ((67 = c) OR (d > e)))
) T2(e_r, a_r)
on ((e_l < (27 + 76)) OR ((e_l > (3 * e_l)) OR (e_r > e_l)))
) T1(e_l_l, d_l_l, e_r_l)
inner join (
Select d
from p1
where (((d * d) = d) OR ((a - (31 - 34)) = 84))
) T2(d_r)
on ((14 = (23 - 31)) OR ((7 = d_l_l) OR (97 < e_r_l)))
) T1(e_l_l_l, d_l_l_l, e_r_l_l, d_r_l)
inner join (
Select c_l, d_l, a_r
from (
Select c, d
from p2
where ((d + 66) > e)
) T1(c_l, d_l)
left join (
Select a
from p3
where ((a * (0 - d)) > 25)
) T2(a_r)
on (42 > d_l)
) T2(c_l_r, d_l_r, a_r_r)
on ((d_l_l_l < 28) AND (90 = ((a_r_r + 32) - ((58 - d_l_l_l) - a_r_r))))
) T2(d_l_l_l_r, a_r_r_r)
on (80 = d_l_l_l_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_r_r_l, c_r
from (
Select c_l, b_r_r, c_r_r
from (
Select c
from p1
where (((e * 8) > 10) AND (51 = (d + 78)))
) T1(c_l)
inner join (
Select b_l_r_l, a_l_l, c_r, b_r
from (
Select a_l, b_l_r
from (
Select e, a, d
from p4
where (((94 * 27) < b) OR ((c < 84) OR (e = 42)))
) T1(e_l, a_l, d_l)
left join (
Select b_l, e_r, a_r, b_r
from (
select b
from (
Select b
from p1
where (8 > c)
) T1
union all
select c
from (
Select c
from p3
where (b = (7 - 16))
) T2
) T1(b_l)
inner join (
Select e, a, b
from p3
where (79 < 12)
) T2(e_r, a_r, b_r)
on ((a_r + 2) = 70)
) T2(b_l_r, e_r_r, a_r_r, b_r_r)
on ((72 = (85 * b_l_r)) AND ((b_l_r = (a_l + a_l)) AND (((54 - a_l) = 27) OR (a_l = 95))))
) T1(a_l_l, b_l_r_l)
left join (
Select c, a, b
from p3
where ((28 = 47) AND ((39 = c) AND (c < 46)))
) T2(c_r, a_r, b_r)
on (47 = b_r)
) T2(b_l_r_l_r, a_l_l_r, c_r_r, b_r_r)
on (43 < c_r_r)
) T1(c_l_l, b_r_r_l, c_r_r_l)
inner join (
Select c
from p3
where (63 < d)
) T2(c_r)
on ((c_r_r_l * 41) = c_r)
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
Select a_l_r_l, a_r_r, e_r_r, b_l_r
from (
Select a_l, a_l_r
from (
Select a
from p5
where ((d = b) OR (b = 78))
) T1(a_l)
full join (
Select c_l, a_l, b_l_r_r, c_l_r_r, b_l_r
from (
Select c, a
from p1
where (d = 3)
) T1(c_l, a_l)
full join (
Select b_l, c_l_r, b_l_r
from (
Select b
from p4
where (23 = d)
) T1(b_l)
left join (
Select c_l, b_l, a_r
from (
Select e, c, b, d
from p2
where (69 > 29)
) T1(e_l, c_l, b_l, d_l)
full join (
select a
from (
Select a
from p4
where (((4 * 32) = e) OR (b < (30 + 73)))
) T1
union all
select a_l_l_l
from (
Select a_l_l_l, b_r
from (
Select a_l_l, b_r
from (
Select c_l, a_l, b_l_r_r, c_r_l_r, e_l_l_r
from (
Select c, a
from p2
where ((67 = d) OR ((d > (a - c)) OR (68 > e)))
) T1(c_l, a_l)
inner join (
Select e_l_l, c_r_l, b_l_r
from (
Select e_l, c_r
from (
Select e
from p4
where (a = b)
) T1(e_l)
left join (
Select e, c
from p4
where ((37 = 34) AND (65 = (e * c)))
) T2(e_r, c_r)
on (79 = 77)
) T1(e_l_l, c_r_l)
full join (
select b_l, e_r, b_r
from (
Select b_l, e_r, b_r
from (
Select b
from p5
where ((76 > 57) AND (1 = e))
) T1(b_l)
left join (
Select e, c, b
from p4
where (e < 91)
) T2(e_r, c_r, b_r)
on ((22 < e_r) AND (e_r > b_l))
) T1
union all
select e, a, b
from (
Select e, a, b
from p3
where (a = d)
) T2
) T2(b_l_r, e_r_r, b_r_r)
on ((7 * 70) = (e_l_l * 4))
) T2(e_l_l_r, c_r_l_r, b_l_r_r)
on (c_l > b_l_r_r)
) T1(c_l_l, a_l_l, b_l_r_r_l, c_r_l_r_l, e_l_l_r_l)
full join (
Select e, a, b
from p5
where (((e * ((a * 19) + d)) + 43) = (e * (62 - 52)))
) T2(e_r, a_r, b_r)
on ((b_r * b_r) < 57)
) T1(a_l_l_l, b_r_l)
left join (
select c, b, d
from (
Select c, b, d
from p3
where (51 = 47)
) T1
union all
select a_l, a_r, d_r
from (
Select a_l, a_r, d_r
from (
select a
from (
select a
from (
Select a, b
from p2
where ((d + 26) = 72)
) T1
union all
select a
from (
Select a
from p5
where ((c - 26) = 58)
) T2
) T1
union all
select c
from (
Select c, a
from p2
where (a = (84 * (30 - (b + (((((c * c) - b) * a) + a) + 3)))))
) T2
) T1(a_l)
inner join (
Select c, a, d
from p3
where (37 = (69 + 87))
) T2(c_r, a_r, d_r)
on ((97 + a_r) = a_r)
) T2
) T2(c_r, b_r, d_r)
on (((77 + b_r) = b_r) AND (a_l_l_l = (45 + a_l_l_l)))
) T2
) T2(a_r)
on ((c_l < a_r) OR ((b_l = c_l) OR (((c_l + 62) < 2) OR ((c_l = (36 - b_l)) OR (a_r = (2 - 23))))))
) T2(c_l_r, b_l_r, a_r_r)
on (88 > c_l_r)
) T2(b_l_r, c_l_r_r, b_l_r_r)
on (b_l_r < c_l)
) T2(c_l_r, a_l_r, b_l_r_r_r, c_l_r_r_r, b_l_r_r)
on (((a_l - a_l_r) = a_l_r) OR ((a_l * (16 * a_l)) = (98 + a_l)))
) T1(a_l_l, a_l_r_l)
inner join (
select b_l, e_r, a_r
from (
Select b_l, e_r, a_r
from (
Select e, a, b
from p4
where (((d + 47) = 23) OR (66 < 88))
) T1(e_l, a_l, b_l)
left join (
Select e, a, d
from p1
where ((a + a) > 18)
) T2(e_r, a_r, d_r)
on (88 > 90)
) T1
union all
select e_l, c_r_r, d_l_r
from (
Select e_l, c_r_r, d_l_r
from (
Select e
from p2
where (b > e)
) T1(e_l)
full join (
Select e_l, d_l, c_r
from (
Select e, d
from p2
where (d = 38)
) T1(e_l, d_l)
full join (
Select c, b
from p5
where (60 < 73)
) T2(c_r, b_r)
on (e_l < ((61 - 18) * e_l))
) T2(e_l_r, d_l_r, c_r_r)
on (5 < e_l)
) T2
) T2(b_l_r, e_r_r, a_r_r)
on (e_r_r > 38)
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
Select c_l_l, d_r_l, c_l_r
from (
Select c_l, d_r
from (
Select c
from p5
where ((24 = d) AND (d = 83))
) T1(c_l)
left join (
Select e, c, d
from p2
where (95 > 18)
) T2(e_r, c_r, d_r)
on (d_r = 75)
) T1(c_l_l, d_r_l)
left join (
select c_l
from (
Select c_l, a_l_r_r_r
from (
Select c
from p2
where (32 > (28 + e))
) T1(c_l)
left join (
Select e_l, c_l, a_l_r_r, d_r_r_r
from (
Select e, c
from p4
where (((82 - b) = d) AND (((52 * e) < b) AND ((50 > 15) AND ((a < e) OR ((c < d) OR ((a = b) AND (47 = d)))))))
) T1(e_l, c_l)
left join (
Select c_l, a_l_r, d_r_r
from (
Select c
from p5
where (22 > d)
) T1(c_l)
full join (
Select a_l, e_r, d_r
from (
Select a
from p2
where (d = 96)
) T1(a_l)
left join (
Select e, b, d
from p1
where ((89 * (0 + 62)) < e)
) T2(e_r, b_r, d_r)
on ((96 = 21) OR ((((d_r - e_r) + a_l) < 42) AND ((20 = 87) OR (((d_r * d_r) < 79) AND (a_l > (d_r - 51))))))
) T2(a_l_r, e_r_r, d_r_r)
on (25 < 75)
) T2(c_l_r, a_l_r_r, d_r_r_r)
on (20 < 50)
) T2(e_l_r, c_l_r, a_l_r_r_r, d_r_r_r_r)
on (a_l_r_r_r < c_l)
) T1
union all
select b
from (
Select b
from p1
where ((13 > b) OR ((d > ((d * 1) - 78)) AND ((33 - (a - a)) = 30)))
) T2
) T2(c_l_r)
on (19 = (c_l_l + (99 - (45 * 68))))
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
Select e_l, a_l, b_l, c_r
from (
Select e, a, b
from p2
where (((a * 67) > (11 - 75)) OR (73 = a))
) T1(e_l, a_l, b_l)
inner join (
Select c
from p1
where ((e < b) AND (e = 30))
) T2(c_r)
on ((e_l = 5) OR (a_l < 32))
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
Select e_l, a_l, d_r
from (
Select e, a
from p1
where (((60 - 60) = 52) OR (b = d))
) T1(e_l, a_l)
left join (
Select d
from p3
where ((((56 + 64) * 80) = 49) AND ((50 = (a * d)) AND (72 > 75)))
) T2(d_r)
on ((22 < a_l) OR (32 > e_l))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_l_r, c_l_r_r
from (
Select b
from p3
where (38 > (86 - b))
) T1(b_l)
left join (
Select e_l, a_l, c_l_r, b_r_r_r
from (
select e, a
from (
Select e, a, d
from p1
where ((((67 - b) + 90) < 51) OR (c < 23))
) T1
union all
select a, d
from (
Select a, d
from p4
where (a = e)
) T2
) T1(e_l, a_l)
full join (
Select c_l, d_l, b_r_l_l_r, b_r_r, c_r_l_r
from (
select c, d
from (
Select c, d
from p4
where (b < d)
) T1
union all
select e, d
from (
Select e, d
from p1
where ((48 = 63) AND (67 < (d * a)))
) T2
) T1(c_l, d_l)
left join (
Select b_r_l_l, c_r_l, b_r
from (
Select b_r_l, c_r
from (
Select e_l, b_r
from (
select e
from (
Select e
from p3
where (d = 68)
) T1
union all
select b
from (
Select b
from p1
where ((c + (d - (b - 39))) > 26)
) T2
) T1(e_l)
full join (
Select b
from p1
where ((e = 17) OR (c < c))
) T2(b_r)
on (e_l = 20)
) T1(e_l_l, b_r_l)
inner join (
Select c, d
from p4
where ((37 < e) OR (45 = 33))
) T2(c_r, d_r)
on (22 = (89 + c_r))
) T1(b_r_l_l, c_r_l)
inner join (
Select b, d
from p2
where (70 > 73)
) T2(b_r, d_r)
on ((((c_r_l + 8) - b_r) - b_r) = (b_r * 35))
) T2(b_r_l_l_r, c_r_l_r, b_r_r)
on ((((c_r_l_r - c_l) + 0) = 7) OR ((((86 * c_l) * 1) = 49) OR (35 > 39)))
) T2(c_l_r, d_l_r, b_r_l_l_r_r, b_r_r_r, c_r_l_r_r)
on (a_l < 16)
) T2(e_l_r, a_l_r, c_l_r_r, b_r_r_r_r)
on (c_l_r_r = (27 + a_l_r))
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
Select d_l, d_r
from (
Select e, a, d
from p1
where ((c + 9) < 20)
) T1(e_l, a_l, d_l)
inner join (
Select c, d
from p2
where (a = c)
) T2(c_r, d_r)
on (13 = d_l)
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
Select c_l, d_l, e_r
from (
Select c, d
from p1
where (a < e)
) T1(c_l, d_l)
left join (
Select e, b, d
from p1
where (d > d)
) T2(e_r, b_r, d_r)
on (84 < 45)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test19exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l_r_l_l, a_r
from (
Select a_l_l, d_l_r_l, b_r
from (
Select a_l, c_r_r, d_l_r
from (
Select c, a
from p2
where ((92 = e) AND (11 > d))
) T1(c_l, a_l)
left join (
Select d_l, c_r
from (
Select b, d
from p1
where (28 < c)
) T1(b_l, d_l)
left join (
Select c
from p3
where (a > (5 * c))
) T2(c_r)
on (17 < c_r)
) T2(d_l_r, c_r_r)
on (a_l > a_l)
) T1(a_l_l, c_r_r_l, d_l_r_l)
inner join (
Select b
from p3
where ((3 = d) AND ((95 + 6) = a))
) T2(b_r)
on (35 = ((33 - 35) - (a_l_l - (b_r + (17 * d_l_r_l)))))
) T1(a_l_l_l, d_l_r_l_l, b_r_l)
left join (
select a
from (
Select a
from p3
where (e < 8)
) T1
union all
select e
from (
select e
from (
Select e, c, a
from p5
where ((c - d) > 29)
) T1
union all
select b
from (
select b
from (
Select b
from p1
where (60 = e)
) T1
union all
select c
from (
Select c, d
from p5
where ((((24 * e) - 61) = 74) OR ((b = 47) AND ((30 * 48) < (83 * 53))))
) T2
) T2
) T2
) T2(a_r)
on (46 = d_l_r_l_l)
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
Select a_l, a_r, b_r
from (
Select c, a
from p5
where (((29 - e) = 78) OR ((21 > d) AND (c < (c - 42))))
) T1(c_l, a_l)
left join (
Select c, a, b, d
from p1
where (68 < a)
) T2(c_r, a_r, b_r, d_r)
on ((a_r < a_r) OR ((a_l = b_r) OR (b_r = (a_r * a_l))))
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
Select c_l, d_l, e_l_r, b_l_r
from (
Select c, d
from p3
where (44 = (55 - d))
) T1(c_l, d_l)
left join (
Select e_l, c_l, b_l, c_r, b_r
from (
Select e, c, b
from p5
where ((e > a) OR ((40 * (((b * e) * c) - (e - c))) = 3))
) T1(e_l, c_l, b_l)
left join (
Select c, b
from p3
where (49 < 48)
) T2(c_r, b_r)
on ((b_l > 61) AND (e_l > b_r))
) T2(e_l_r, c_l_r, b_l_r, c_r_r, b_r_r)
on (10 = c_l)
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

