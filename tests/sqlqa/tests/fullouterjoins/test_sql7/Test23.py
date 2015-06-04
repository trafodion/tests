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
    
def test001(desc="""Joins Set 23"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, e_r
from (
Select c, a
from p5
where (b > ((c + 75) * (31 - 40)))
) T1(c_l, a_l)
inner join (
Select e
from p5
where ((a > 65) OR ((d < (c * (24 + b))) AND ((78 > e) OR (33 > 4))))
) T2(e_r)
on (a_l = a_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l, d_r
from (
select b_l, e_r, c_r
from (
Select b_l, e_r, c_r
from (
Select c, a, b, d
from p5
where (e = a)
) T1(c_l, a_l, b_l, d_l)
inner join (
Select e, c
from p1
where (e = 43)
) T2(e_r, c_r)
on (b_l = e_r)
) T1
union all
select a, b, d
from (
Select a, b, d
from p2
where ((e * ((99 * (e + 28)) * 13)) = (e * c))
) T2
) T1(b_l_l, e_r_l, c_r_l)
left join (
Select d
from p4
where ((56 = a) OR ((e > 17) AND (b < a)))
) T2(d_r)
on (e_r_l < 38)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, a_l_l_r
from (
Select b
from p1
where ((d > (a + a)) AND ((38 = d) AND ((e + 15) > (87 * 38))))
) T1(b_l)
left join (
Select a_l_l, c_l_l, e_r_l, a_r
from (
Select c_l, a_l, e_r, a_r
from (
Select c, a, d
from p2
where (a = (d + 48))
) T1(c_l, a_l, d_l)
left join (
Select e, a
from p1
where (34 = d)
) T2(e_r, a_r)
on ((49 = 58) OR (((c_l * 3) - c_l) < ((72 + e_r) - 11)))
) T1(c_l_l, a_l_l, e_r_l, a_r_l)
left join (
Select e, a
from p5
where (d < 77)
) T2(e_r, a_r)
on ((25 = a_l_l) AND (98 < 65))
) T2(a_l_l_r, c_l_l_r, e_r_l_r, a_r_r)
on ((a_l_l_r = a_l_l_r) OR (a_l_l_r < 56))
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
Select c_l, b_l, a_l_r, c_r_r
from (
Select c, b
from p5
where ((c + d) > 30)
) T1(c_l, b_l)
inner join (
Select a_l, d_l, c_r
from (
Select a, d
from p1
where (a = 13)
) T1(a_l, d_l)
full join (
Select c
from p5
where ((d * (d - 68)) > e)
) T2(c_r)
on ((d_l = 25) AND (((d_l - 92) < d_l) OR ((51 * a_l) = 75)))
) T2(a_l_r, d_l_r, c_r_r)
on ((82 = 97) AND (c_r_r = a_l_r))
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
select d
from (
Select d
from p3
where ((a - e) < 20)
) T1
union all
select c_l_r_l
from (
select c_l_r_l, b_r_r_l, e_r, c_r
from (
Select c_l_r_l, b_r_r_l, e_r, c_r
from (
Select d_l, c_l_r, b_r_r
from (
Select d
from p1
where (((50 - d) < a) OR ((c = 89) AND ((a > c) AND (c = ((b - ((e - 12) * (94 - d))) * (33 + 51))))))
) T1(d_l)
inner join (
Select c_l, a_r, b_r
from (
Select c, a
from p4
where ((92 > e) OR (52 > 18))
) T1(c_l, a_l)
left join (
select a, b
from (
Select a, b
from p4
where (79 = (((13 + (49 * 43)) - 93) * b))
) T1
union all
select e_l_l, c_r_l
from (
Select e_l_l, c_r_l, a_r, d_r
from (
Select e_l, c_r
from (
Select e
from p2
where ((e = 82) OR (d > c))
) T1(e_l)
left join (
Select c
from p2
where (11 = e)
) T2(c_r)
on (((c_r * 46) > c_r) OR (44 < c_r))
) T1(e_l_l, c_r_l)
left join (
Select a, b, d
from p1
where (67 = 0)
) T2(a_r, b_r, d_r)
on (a_r < 68)
) T2
) T2(a_r, b_r)
on (67 = c_l)
) T2(c_l_r, a_r_r, b_r_r)
on ((72 + 94) < 9)
) T1(d_l_l, c_l_r_l, b_r_r_l)
left join (
Select e, c
from p5
where ((c < 20) OR (26 < 51))
) T2(e_r, c_r)
on (b_r_r_l = 79)
) T1
union all
select b_l, d_l, e_r, d_r
from (
Select b_l, d_l, e_r, d_r
from (
Select b, d
from p5
where ((60 = (e - c)) OR (d = e))
) T1(b_l, d_l)
full join (
Select e, c, d
from p4
where (88 < (b - a))
) T2(e_r, c_r, d_r)
on (b_l < d_l)
) T2
) T2
) T1(d_l)
full join (
Select c, b
from p4
where (e > c)
) T2(c_r, b_r)
on ((c_r + 92) = d_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, e_r, b_r
from (
Select e, d
from p4
where (((12 + b) = c) OR (a > b))
) T1(e_l, d_l)
inner join (
Select e, b
from p2
where (86 = 88)
) T2(e_r, b_r)
on (38 = 72)
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
Select b_r_l, d_r_l, c_r_l_l, c_r_r
from (
Select b_r_l, c_r_l, b_r, d_r
from (
Select c_l, c_r, b_r
from (
select c
from (
Select c, b, d
from p2
where ((70 = 21) OR ((37 = (a - 56)) AND ((e > a) OR ((3 * 14) > e))))
) T1
union all
select e
from (
Select e
from p1
where ((7 = (77 + 21)) OR (25 < 6))
) T2
) T1(c_l)
left join (
Select c, b
from p4
where (c = 60)
) T2(c_r, b_r)
on (19 > 85)
) T1(c_l_l, c_r_l, b_r_l)
inner join (
Select a, b, d
from p5
where (a = 17)
) T2(a_r, b_r, d_r)
on (d_r > 28)
) T1(b_r_l_l, c_r_l_l, b_r_l, d_r_l)
inner join (
Select b_l, c_r
from (
select c, b
from (
Select c, b, d
from p3
where (50 < (d * d))
) T1
union all
select a, b
from (
Select a, b
from p4
where (c > a)
) T2
) T1(c_l, b_l)
full join (
Select c
from p4
where ((85 - (b * 53)) > c)
) T2(c_r)
on ((68 < 53) AND ((c_r = 29) OR (b_l = c_r)))
) T2(b_l_r, c_r_r)
on ((d_r_l = c_r_l_l) OR ((94 + b_r_l) < 8))
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
Select a_l, a_r
from (
Select a, b
from p2
where (d > a)
) T1(a_l, b_l)
left join (
Select a
from p5
where ((16 > 1) AND (b > (d - 92)))
) T2(a_r)
on ((26 < a_r) AND (13 = a_l))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, a_l_r_r
from (
Select e
from p2
where ((b < (29 + c)) AND (49 < (61 - (91 + 92))))
) T1(e_l)
full join (
select b_r_l_l_l, a_l_r, d_r_r
from (
Select b_r_l_l_l, a_l_r, d_r_r
from (
Select b_r_l_l, c_r_l, d_l_r
from (
Select b_r_l, c_r
from (
Select d_l, b_r, d_r
from (
Select d
from p4
where (((c + b) > 11) AND (59 < 88))
) T1(d_l)
left join (
Select c, b, d
from p2
where (a = 1)
) T2(c_r, b_r, d_r)
on ((88 - 16) = 91)
) T1(d_l_l, b_r_l, d_r_l)
left join (
select c
from (
Select c
from p5
where ((63 < b) OR (((83 + (91 * d)) = 82) AND ((14 = e) OR (a = c))))
) T1
union all
select a
from (
Select a, b
from p2
where (((89 + e) + e) = c)
) T2
) T2(c_r)
on ((b_r_l = c_r) OR (14 > c_r))
) T1(b_r_l_l, c_r_l)
left join (
Select d_l, b_r
from (
Select b, d
from p2
where ((46 > e) AND (d = 13))
) T1(b_l, d_l)
left join (
select b
from (
Select b
from p2
where (((((53 - (c - (98 * c))) - 42) - e) > ((33 - e) - 73)) AND ((67 = e) OR (90 < 63)))
) T1
union all
select e
from (
Select e
from p2
where (18 > a)
) T2
) T2(b_r)
on (d_l = 26)
) T2(d_l_r, b_r_r)
on (((72 + c_r_l) * b_r_l_l) < 99)
) T1(b_r_l_l_l, c_r_l_l, d_l_r_l)
full join (
Select a_l, c_r, d_r
from (
Select c, a
from p2
where (65 = 39)
) T1(c_l, a_l)
left join (
Select c, d
from p4
where ((32 + 58) = 49)
) T2(c_r, d_r)
on ((90 = 71) OR (84 < d_r))
) T2(a_l_r, c_r_r, d_r_r)
on (78 = a_l_r)
) T1
union all
select b_r_l, e_r, a_r
from (
Select b_r_l, e_r, a_r
from (
Select a_l, b_l, b_r
from (
Select a, b
from p2
where (d > c)
) T1(a_l, b_l)
left join (
Select b, d
from p3
where ((b < (d - 26)) AND (15 = (80 - 9)))
) T2(b_r, d_r)
on ((69 * b_r) = (b_l + 29))
) T1(a_l_l, b_l_l, b_r_l)
full join (
Select e, a
from p2
where ((b < 57) OR (6 = (c + (30 + (83 - b)))))
) T2(e_r, a_r)
on ((54 < a_r) AND ((b_r_l + (e_r - 18)) < 45))
) T2
) T2(b_r_l_l_l_r, a_l_r_r, d_r_r_r)
on ((a_l_r_r + a_l_r_r) = e_l)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, a_l, e_r, a_r
from (
select c, a
from (
Select c, a
from p1
where ((95 = d) OR (6 > 25))
) T1
union all
select e, a
from (
select e, a
from (
Select e, a
from p2
where (e = e)
) T1
union all
select a, b
from (
Select a, b
from p4
where (b > c)
) T2
) T2
) T1(c_l, a_l)
inner join (
Select e, a, d
from p3
where (d > e)
) T2(e_r, a_r, d_r)
on ((a_l > c_l) AND ((((8 - 49) - a_r) > (99 * 58)) AND (53 = (e_r * 7))))
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
Select b_l_l, e_r, c_r
from (
Select b_l, d_r_r, a_l_r_l_r
from (
Select b
from p5
where ((12 = 88) OR (b > 61))
) T1(b_l)
left join (
Select a_l_r_l, e_l_l, d_r
from (
Select e_l, a_l_r, c_l_r
from (
Select e
from p3
where (e = 88)
) T1(e_l)
inner join (
Select c_l, a_l, d_r
from (
Select c, a
from p1
where ((b < 24) OR (c > b))
) T1(c_l, a_l)
full join (
Select a, b, d
from p5
where ((e = a) AND (e = (56 + 13)))
) T2(a_r, b_r, d_r)
on ((a_l = d_r) OR (c_l > (a_l * 70)))
) T2(c_l_r, a_l_r, d_r_r)
on (((e_l * 58) * (c_l_r - 54)) < 34)
) T1(e_l_l, a_l_r_l, c_l_r_l)
full join (
Select e, d
from p4
where (c = d)
) T2(e_r, d_r)
on ((1 < 78) OR ((62 + (21 * 44)) = a_l_r_l))
) T2(a_l_r_l_r, e_l_l_r, d_r_r)
on (d_r_r = ((((8 - (d_r_r - 44)) + b_l) - a_l_r_l_r) + a_l_r_l_r))
) T1(b_l_l, d_r_r_l, a_l_r_l_r_l)
inner join (
Select e, c, a
from p4
where (((a + (8 - c)) = 18) OR ((e = 89) AND ((b = 72) OR ((b > (a - d)) AND (b > 49)))))
) T2(e_r, c_r, a_r)
on (b_l_l < 1)
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
Select e_l, c_l_r, e_r_r
from (
Select e, b
from p4
where (c > 7)
) T1(e_l, b_l)
left join (
Select c_l, e_r, c_r
from (
Select c, b
from p3
where ((e = (c * (e - ((43 - c) - (d * (d - (b + ((b * (c - 21)) + c)))))))) AND (51 > a))
) T1(c_l, b_l)
inner join (
Select e, c
from p3
where ((50 < 10) AND (a < 50))
) T2(e_r, c_r)
on ((35 = 35) OR ((24 * c_r) = (c_l + 70)))
) T2(c_l_r, e_r_r, c_r_r)
on (((68 + (5 * e_l)) = c_l_r) AND (39 = 97))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, c_r, b_r, d_r
from (
Select e, d
from p3
where (a < e)
) T1(e_l, d_l)
left join (
Select c, b, d
from p3
where ((b = 46) AND ((74 = 85) OR (25 > (94 * 37))))
) T2(c_r, b_r, d_r)
on (5 = 47)
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, d_r
from (
Select b
from p5
where (26 = 44)
) T1(b_l)
inner join (
Select d
from p2
where (a > d)
) T2(d_r)
on ((b_l + 25) = b_l)
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
Select e_l, a_l_r, b_r_r
from (
Select e, b
from p3
where ((c > (c - 13)) AND (84 = 67))
) T1(e_l, b_l)
left join (
Select a_l, b_r
from (
Select e, a
from p2
where (((c - (b + a)) = c) OR (91 > a))
) T1(e_l, a_l)
left join (
Select c, a, b
from p2
where ((c - 59) = c)
) T2(c_r, a_r, b_r)
on (76 < a_l)
) T2(a_l_r, b_r_r)
on (a_l_r < ((e_l * (e_l * 33)) - 80))
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
Select c_r_l, c_r_r_l_l, d_r
from (
Select a_l_l, c_r_r_l, c_r, d_r
from (
Select a_l, a_r_r, c_r_r
from (
Select a
from p3
where (43 = 41)
) T1(a_l)
left join (
select c_l, b_l, c_r, a_r
from (
Select c_l, b_l, c_r, a_r
from (
Select e, c, b
from p5
where (((9 * b) = (e * b)) OR (73 > 24))
) T1(e_l, c_l, b_l)
full join (
Select c, a
from p1
where ((c < d) OR (53 > (53 * 53)))
) T2(c_r, a_r)
on (((24 - a_r) = 63) OR (c_r = 38))
) T1
union all
select c_l_l, d_r_l, e_l_l, e_r
from (
Select c_l_l, d_r_l, e_l_l, e_r
from (
Select e_l, c_l, e_r, d_r
from (
Select e, c
from p4
where ((9 + 49) = 6)
) T1(e_l, c_l)
left join (
Select e, d
from p5
where ((9 < a) OR (5 < 25))
) T2(e_r, d_r)
on ((23 - d_r) = e_l)
) T1(e_l_l, c_l_l, e_r_l, d_r_l)
inner join (
Select e, d
from p5
where (44 = 3)
) T2(e_r, d_r)
on (e_l_l = ((c_l_l + 22) - 89))
) T2
) T2(c_l_r, b_l_r, c_r_r, a_r_r)
on ((a_r_r = a_r_r) OR (35 = a_l))
) T1(a_l_l, a_r_r_l, c_r_r_l)
inner join (
Select c, d
from p2
where (c = a)
) T2(c_r, d_r)
on (c_r_r_l < a_l_l)
) T1(a_l_l_l, c_r_r_l_l, c_r_l, d_r_l)
left join (
Select c, b, d
from p5
where (b > 48)
) T2(c_r, b_r, d_r)
on (c_r_l = 61)
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
Select e_l, c_r, d_r
from (
Select e
from p3
where (41 > (b - (87 - d)))
) T1(e_l)
left join (
Select c, d
from p3
where (1 < 80)
) T2(c_r, d_r)
on (d_r = c_r)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_l, c_r
from (
Select b
from p5
where (78 = c)
) T1(b_l)
left join (
Select c
from p3
where ((c > d) OR (d = c))
) T2(c_r)
on ((94 - c_r) < c_r)
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
Select d_l_l, e_r_l, e_r
from (
Select d_l, e_r
from (
Select a, d
from p2
where (((c * (b - c)) < b) AND (d < e))
) T1(a_l, d_l)
full join (
Select e
from p1
where (((83 - 58) < (49 + d)) AND (c > 39))
) T2(e_r)
on ((31 = 11) AND ((e_r * d_l) = 99))
) T1(d_l_l, e_r_l)
left join (
Select e, c
from p1
where (21 < b)
) T2(e_r, c_r)
on (e_r_l > 85)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, c_r, b_r
from (
select e
from (
Select e
from p3
where ((d = (b + c)) AND ((e - 1) = 64))
) T1
union all
select a_l_l
from (
Select a_l_l, b_r_r_l, d_l_l, b_r
from (
Select a_l, b_l, d_l, b_r_r
from (
Select a, b, d
from p5
where ((65 = (36 - 41)) OR (12 < d))
) T1(a_l, b_l, d_l)
inner join (
Select b_r_l, c_l_l_r_l_l, c_r, b_r
from (
Select c_l_l_r_l, b_r
from (
Select e_l, c_l_l_r, e_l_r_r
from (
Select e, c, d
from p1
where (2 < 56)
) T1(e_l, c_l, d_l)
full join (
Select c_l_l, e_l_r, d_l_r
from (
Select c_l, c_r
from (
Select c
from p3
where ((((5 * 15) * c) + 90) = d)
) T1(c_l)
full join (
Select e, c, a, d
from p4
where (76 = 94)
) T2(e_r, c_r, a_r, d_r)
on (54 = ((c_r * c_r) + c_l))
) T1(c_l_l, c_r_l)
inner join (
Select e_l, d_l, a_r
from (
Select e, d
from p4
where (e = ((b * 79) * e))
) T1(e_l, d_l)
left join (
Select a, b
from p5
where (c > 90)
) T2(a_r, b_r)
on (64 = 14)
) T2(e_l_r, d_l_r, a_r_r)
on (52 = e_l_r)
) T2(c_l_l_r, e_l_r_r, d_l_r_r)
on (47 = (c_l_l_r + e_l_r_r))
) T1(e_l_l, c_l_l_r_l, e_l_r_r_l)
left join (
Select b
from p3
where ((a > (27 + (b - 23))) OR (84 < e))
) T2(b_r)
on (c_l_l_r_l > c_l_l_r_l)
) T1(c_l_l_r_l_l, b_r_l)
left join (
Select c, b
from p4
where (e > 45)
) T2(c_r, b_r)
on (84 = c_r)
) T2(b_r_l_r, c_l_l_r_l_l_r, c_r_r, b_r_r)
on ((d_l = 52) AND (91 > d_l))
) T1(a_l_l, b_l_l, d_l_l, b_r_r_l)
full join (
Select b
from p1
where (e = (d * e))
) T2(b_r)
on (96 = b_r_r_l)
) T2
) T1(e_l)
left join (
select c, b
from (
Select c, b
from p5
where ((e > 49) AND (d = c))
) T1
union all
select e, b
from (
select e, b
from (
select e, b
from (
Select e, b
from p5
where ((6 * b) > 26)
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, e_r, c_r
from (
Select e, c, d
from p2
where ((37 < 48) AND ((28 = a) AND ((20 > 90) OR (e = (26 * (54 * 69))))))
) T1(e_l, c_l, d_l)
left join (
Select e, c
from p4
where (27 < d)
) T2(e_r, c_r)
on (13 < c_r)
) T2
) T1
union all
select c_l, a_r
from (
Select c_l, a_r, d_r
from (
Select e, c
from p1
where (b > 30)
) T1(e_l, c_l)
inner join (
select e, a, d
from (
Select e, a, d
from p5
where (a = b)
) T1
union all
select d_r_l, b_r_r, d_l_r
from (
Select d_r_l, b_r_r, d_l_r, e_r_r
from (
Select a_l, d_r
from (
Select a
from p3
where ((d > 13) AND ((b = (4 - b)) OR (b > 54)))
) T1(a_l)
left join (
Select d
from p5
where (a = e)
) T2(d_r)
on ((d_r * d_r) < d_r)
) T1(a_l_l, d_r_l)
full join (
Select d_l, e_r, b_r
from (
Select c, a, b, d
from p3
where ((e < 57) OR (e = 84))
) T1(c_l, a_l, b_l, d_l)
left join (
select e, b
from (
Select e, b
from p1
where ((c > 79) OR (d > e))
) T1
union all
select e, c
from (
Select e, c
from p2
where (((87 - 66) > c) OR (d = b))
) T2
) T2(e_r, b_r)
on (4 = e_r)
) T2(d_l_r, e_r_r, b_r_r)
on ((3 = 96) AND ((b_r_r = (d_r_l + 56)) OR ((b_r_r < (b_r_r + 26)) AND (27 < 87))))
) T2
) T2(e_r, a_r, d_r)
on ((c_l = a_r) OR (((9 * 13) + c_l) = ((d_r + (c_l + 3)) - d_r)))
) T2
) T2
) T2(c_r, b_r)
on (((60 * 75) = ((e_l + c_r) * 51)) OR ((36 < 42) AND (62 < 69)))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************************
    _testmgr.testcase_end(desc)

