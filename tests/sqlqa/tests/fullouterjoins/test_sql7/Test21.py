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
    
def test001(desc="""Joins Set 21"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_r
from (
Select a
from p3
where (32 = (d - e))
) T1(a_l)
inner join (
Select b, d
from p4
where ((e - b) = e)
) T2(b_r, d_r)
on ((a_l > (a_l + 7)) OR (a_l > d_r))
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
Select c_r_l, d_l_l, e_r
from (
Select d_l, c_r
from (
Select c, b, d
from p4
where (((d + 43) = 29) AND ((c = d) AND (e < (67 * (4 - ((d + (16 - 46)) + 68))))))
) T1(c_l, b_l, d_l)
full join (
Select c
from p2
where (66 > e)
) T2(c_r)
on ((c_r - c_r) = 32)
) T1(d_l_l, c_r_l)
full join (
Select e, a, b
from p2
where (20 = d)
) T2(e_r, a_r, b_r)
on (c_r_l = (41 + 18))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select a_l, d_l, a_r
from (
Select a, d
from p1
where (32 = (11 + 14))
) T1(a_l, d_l)
left join (
Select a
from p3
where ((b * (57 - (29 * 69))) = (d + 71))
) T2(a_r)
on (d_l < a_l)
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
Select c_l_l, b_r_l, b_r
from (
select c_l, b_r
from (
Select c_l, b_r, d_r
from (
Select c, d
from p1
where (a > 74)
) T1(c_l, d_l)
left join (
Select c, b, d
from p1
where (b > e)
) T2(c_r, b_r, d_r)
on (d_r = (b_r * (c_l - (((89 - (39 + (72 + 30))) - c_l) * (c_l * b_r)))))
) T1
union all
select c_l, e_r
from (
Select c_l, e_r
from (
Select c, a, d
from p3
where ((c = 73) AND (85 < (53 + d)))
) T1(c_l, a_l, d_l)
left join (
select e, c
from (
select e, c
from (
Select e, c, a
from p2
where ((50 < 29) AND (35 < c))
) T1
union all
select b, d
from (
Select b, d
from p5
where ((d = 59) AND ((82 > 4) AND ((c * (a + (61 * c))) > 57)))
) T2
) T1
union all
select b_l, e_l_r
from (
Select b_l, e_l_r
from (
Select e, a, b
from p2
where ((((((d + 20) + b) - e) - ((82 + d) - a)) < c) OR (28 < 66))
) T1(e_l, a_l, b_l)
left join (
Select e_l, c_l_r_r
from (
Select e
from p1
where ((a = 35) AND (e = 17))
) T1(e_l)
left join (
Select a_l, c_l_r
from (
select a
from (
Select a
from p4
where (b = (d * b))
) T1
union all
select c_r_r_r_l
from (
Select c_r_r_r_l, c_r, b_r
from (
Select e_l, a_l, c_l_r, c_r_r_r
from (
select e, a
from (
Select e, a, b
from p3
where (b = 8)
) T1
union all
select c, d
from (
Select c, d
from p1
where ((44 = 39) OR (e = c))
) T2
) T1(e_l, a_l)
full join (
Select c_l, c_r_r, a_r_l_r
from (
Select e, c, d
from p2
where (8 > b)
) T1(e_l, c_l, d_l)
left join (
Select a_r_l, c_r
from (
Select d_l, a_r
from (
Select c, a, d
from p5
where (e > e)
) T1(c_l, a_l, d_l)
full join (
Select a, b
from p2
where (a = 46)
) T2(a_r, b_r)
on ((80 = a_r) OR (71 > 63))
) T1(d_l_l, a_r_l)
left join (
Select c, a
from p1
where (a < b)
) T2(c_r, a_r)
on ((c_r + 50) < c_r)
) T2(a_r_l_r, c_r_r)
on ((8 * 27) > (a_r_l_r - ((49 + (c_r_r * a_r_l_r)) - 78)))
) T2(c_l_r, c_r_r_r, a_r_l_r_r)
on (7 < 20)
) T1(e_l_l, a_l_l, c_l_r_l, c_r_r_r_l)
left join (
Select c, b
from p5
where ((52 < 4) OR ((70 = e) OR ((57 > 18) OR (((b * 32) > (((36 + d) * d) - b)) AND (a = (((40 * a) + a) * (b * 53)))))))
) T2(c_r, b_r)
on ((c_r < 75) OR (2 = (51 - c_r)))
) T2
) T1(a_l)
inner join (
select c_l, d_r
from (
Select c_l, d_r
from (
Select c
from p5
where ((16 = 26) AND (60 = 63))
) T1(c_l)
full join (
Select a, d
from p1
where (a = 95)
) T2(a_r, d_r)
on ((40 * c_l) = (c_l - c_l))
) T1
union all
select c, a
from (
Select c, a
from p5
where ((30 = (57 - 45)) AND (b = 94))
) T2
) T2(c_l_r, d_r_r)
on (69 = 18)
) T2(a_l_r, c_l_r_r)
on (e_l = c_l_r_r)
) T2(e_l_r, c_l_r_r_r)
on ((31 - e_l_r) < (74 * e_l_r))
) T2
) T2(e_r, c_r)
on ((c_l * c_l) > c_l)
) T2
) T1(c_l_l, b_r_l)
left join (
Select b
from p1
where ((65 = c) AND (c < a))
) T2(b_r)
on ((b_r > b_r_l) AND (((34 - b_r_l) - (84 + 51)) < 83))
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
Select e_l, b_l, b_r_r
from (
Select e, b
from p5
where (b < 0)
) T1(e_l, b_l)
inner join (
Select c_l, a_l, e_r, b_r
from (
Select e, c, a
from p5
where (35 > (d + (57 * (31 - (61 + a)))))
) T1(e_l, c_l, a_l)
left join (
select e, a, b
from (
Select e, a, b
from p5
where ((62 = 67) OR (71 = 27))
) T1
union all
select e_r_r_r_l, b_r_l_l_l_l, e_r
from (
Select e_r_r_r_l, b_r_l_l_l_l, e_r
from (
Select b_r_l_l_l, a_l_r_r_l, b_l_r_r, e_r_r_r
from (
select b_r_l_l, a_l_r_r
from (
Select b_r_l_l, a_l_r_r
from (
select b_r_l, b_l_l_l
from (
Select b_r_l, b_l_l_l, b_r
from (
Select b_l_l, b_r
from (
Select b_l, a_l_l_l_r_r, d_l_r
from (
Select b
from p3
where (63 < 95)
) T1(b_l)
full join (
select d_l, a_l_l_l_r
from (
Select d_l, a_l_l_l_r, a_r_r
from (
Select a, d
from p1
where (a = 71)
) T1(a_l, d_l)
inner join (
Select e_r_l_l, a_l_l_l, a_r
from (
Select a_l_l, e_r_l, b_r_r
from (
Select a_l, b_l, e_r
from (
select a, b
from (
Select a, b
from p5
where (b = 51)
) T1
union all
select c_l, b_l
from (
select c_l, b_l
from (
Select c_l, b_l, d_l, a_r
from (
Select e, c, b, d
from p5
where ((a < 6) OR (c < 47))
) T1(e_l, c_l, b_l, d_l)
full join (
Select a
from p3
where ((73 - (70 - 98)) > 94)
) T2(a_r)
on ((4 = a_r) OR ((c_l < c_l) AND (a_r > 10)))
) T1
union all
select c, d
from (
Select c, d
from p2
where ((b > 58) AND (b < (45 * 66)))
) T2
) T2
) T1(a_l, b_l)
left join (
Select e
from p4
where (d > (b - ((b - 50) * 23)))
) T2(e_r)
on (e_r = ((67 + b_l) + b_l))
) T1(a_l_l, b_l_l, e_r_l)
left join (
select b_l_l_l, e_r, b_r
from (
Select b_l_l_l, e_r, b_r
from (
select b_l_l, c_r
from (
Select b_l_l, c_r
from (
Select c_l, b_l, d_l, d_r_r, b_l_r
from (
Select c, a, b, d
from p2
where (((96 * (a * e)) = 36) AND (e = a))
) T1(c_l, a_l, b_l, d_l)
inner join (
Select b_l, d_r
from (
Select c, b, d
from p2
where (((21 - d) * (6 - 71)) > 4)
) T1(c_l, b_l, d_l)
left join (
Select d
from p5
where (58 = e)
) T2(d_r)
on (b_l = 71)
) T2(b_l_r, d_r_r)
on (d_l = 72)
) T1(c_l_l, b_l_l, d_l_l, d_r_r_l, b_l_r_l)
inner join (
Select e, c
from p1
where ((a > c) OR (69 > a))
) T2(e_r, c_r)
on ((97 = 92) OR (c_r < c_r))
) T1
union all
select e, c
from (
Select e, c
from p3
where ((63 - (e - 9)) < (((97 * d) + 75) + (e * 48)))
) T2
) T1(b_l_l_l, c_r_l)
left join (
Select e, b
from p3
where (55 > e)
) T2(e_r, b_r)
on ((30 - b_r) > (b_l_l_l * 31))
) T1
union all
select c_l, b_l, d_l
from (
Select c_l, b_l, d_l, e_r, d_r
from (
Select c, b, d
from p4
where (e = a)
) T1(c_l, b_l, d_l)
inner join (
Select e, d
from p5
where (d = 17)
) T2(e_r, d_r)
on ((d_l - d_l) = d_r)
) T2
) T2(b_l_l_l_r, e_r_r, b_r_r)
on (b_r_r = 38)
) T1(a_l_l_l, e_r_l_l, b_r_r_l)
left join (
Select a, b
from p5
where ((31 * 57) = c)
) T2(a_r, b_r)
on (a_l_l_l = 40)
) T2(e_r_l_l_r, a_l_l_l_r, a_r_r)
on (65 < ((d_l + 20) + a_r_r))
) T1
union all
select e, a
from (
Select e, a
from p1
where (d = (98 * (b - (13 * c))))
) T2
) T2(d_l_r, a_l_l_l_r_r)
on ((61 > d_l_r) OR ((78 = 86) AND ((((95 + (24 - 23)) * ((99 - 93) + b_l)) + 81) > d_l_r)))
) T1(b_l_l, a_l_l_l_r_r_l, d_l_r_l)
left join (
Select a, b, d
from p3
where (a < 99)
) T2(a_r, b_r, d_r)
on ((86 = b_r) OR ((b_r = (14 - b_r)) AND ((38 = b_l_l) OR ((b_r * b_l_l) = (83 * 14)))))
) T1(b_l_l_l, b_r_l)
full join (
Select e, b
from p1
where ((40 = 26) AND ((e * d) < 61))
) T2(e_r, b_r)
on ((b_l_l_l < ((b_l_l_l - b_r_l) * b_r)) AND (b_l_l_l = 87))
) T1
union all
select e, d
from (
Select e, d
from p3
where (19 = d)
) T2
) T1(b_r_l_l, b_l_l_l_l)
full join (
Select a_l_l, a_l_r, e_r_r
from (
Select a_l, d_r
from (
Select a
from p5
where ((20 = 83) AND ((21 < 0) AND ((c < 98) AND ((38 * 4) > ((80 + 36) + b)))))
) T1(a_l)
left join (
Select d
from p4
where ((90 = 70) OR ((6 > 78) OR ((b = e) OR ((d = a) OR ((a > 31) AND (((d * 49) * a) = (16 - 45)))))))
) T2(d_r)
on (a_l = a_l)
) T1(a_l_l, d_r_l)
full join (
Select c_l, a_l, e_r
from (
Select c, a, d
from p2
where ((b < (a + c)) AND ((e * c) = 63))
) T1(c_l, a_l, d_l)
inner join (
Select e
from p4
where ((33 * e) = (e * 49))
) T2(e_r)
on ((e_r = ((45 - 41) * (c_l - e_r))) OR ((30 < 25) AND ((57 < 30) OR ((7 > (((31 + 55) + c_l) - (69 * a_l))) OR (a_l < a_l)))))
) T2(c_l_r, a_l_r, e_r_r)
on ((62 + 88) = 3)
) T2(a_l_l_r, a_l_r_r, e_r_r_r)
on (a_l_r_r < a_l_r_r)
) T1
union all
select e, a
from (
Select e, a, b, d
from p3
where ((((e * 56) - c) = 86) AND (b = 84))
) T2
) T1(b_r_l_l_l, a_l_r_r_l)
full join (
Select d_l_l, e_r_r, b_l_r
from (
Select a_l, d_l, d_r
from (
Select c, a, d
from p1
where (c = 18)
) T1(c_l, a_l, d_l)
full join (
select d
from (
Select d
from p1
where (d = a)
) T1
union all
select c_l
from (
Select c_l, c_r, d_r
from (
Select c
from p3
where ((11 < a) AND (36 > b))
) T1(c_l)
full join (
Select c, a, d
from p1
where (d < 18)
) T2(c_r, a_r, d_r)
on (c_r > ((c_l * 6) - d_r))
) T2
) T2(d_r)
on (((a_l + d_r) = 7) OR ((37 - (69 + 13)) > d_r))
) T1(a_l_l, d_l_l, d_r_l)
left join (
Select b_l, e_r
from (
Select b
from p4
where (d > b)
) T1(b_l)
inner join (
Select e
from p2
where ((d = (33 - (29 * (77 - a)))) AND (((e + d) + 58) = b))
) T2(e_r)
on (18 < e_r)
) T2(b_l_r, e_r_r)
on ((d_l_l = (b_l_r * (b_l_r * d_l_l))) AND (e_r_r = b_l_r))
) T2(d_l_l_r, e_r_r_r, b_l_r_r)
on (b_r_l_l_l < 99)
) T1(b_r_l_l_l_l, a_l_r_r_l_l, b_l_r_r_l, e_r_r_r_l)
left join (
Select e, d
from p5
where ((c = 12) OR (60 = (90 - 55)))
) T2(e_r, d_r)
on ((e_r = 67) OR (99 = (b_r_l_l_l_l - 21)))
) T2
) T2(e_r, a_r, b_r)
on (56 = (41 + (a_l + 1)))
) T2(c_l_r, a_l_r, e_r_r, b_r_r)
on (b_r_r = 20)
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
Select a_r_l, e_r, d_r
from (
Select c_l, a_r
from (
Select c
from p5
where (44 < b)
) T1(c_l)
left join (
select e, a
from (
Select e, a, d
from p3
where (d = (92 + 55))
) T1
union all
select a, b
from (
Select a, b
from p3
where ((b = c) OR (((b + c) = 22) AND (e > e)))
) T2
) T2(e_r, a_r)
on (a_r = a_r)
) T1(c_l_l, a_r_l)
left join (
Select e, d
from p1
where ((b = e) OR (((78 * d) < (54 * e)) OR ((d = a) AND ((60 = (91 - c)) AND (87 < 18)))))
) T2(e_r, d_r)
on (a_r_l > e_r)
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
Select c_l_l, a_r_l, e_r_l, a_r
from (
Select e_l, c_l, e_r, a_r
from (
Select e, c, a
from p1
where (25 = c)
) T1(e_l, c_l, a_l)
full join (
Select e, a
from p1
where ((53 < 72) AND (70 < b))
) T2(e_r, a_r)
on (71 < 49)
) T1(e_l_l, c_l_l, e_r_l, a_r_l)
full join (
Select e, a, b
from p4
where ((66 > 95) OR (22 > e))
) T2(e_r, a_r, b_r)
on (62 = ((82 - (((c_l_l * a_r) * a_r_l) * 19)) * (a_r - 35)))
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_r, d_r
from (
Select e, c
from p4
where ((88 = (47 * d)) OR (57 = c))
) T1(e_l, c_l)
full join (
Select c, d
from p5
where ((a = 29) AND (7 < 27))
) T2(c_r, d_r)
on (87 = (c_r + 76))
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
Select b_l, e_r
from (
Select b, d
from p3
where (36 < (22 + d))
) T1(b_l, d_l)
full join (
Select e
from p4
where (a > 81)
) T2(e_r)
on (21 < 39)
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_l, d_l, d_r
from (
Select e, a, d
from p3
where ((c = 37) OR (((d - ((21 * a) - c)) * d) < 18))
) T1(e_l, a_l, d_l)
full join (
Select c, a, d
from p1
where (79 > (d * b))
) T2(c_r, a_r, d_r)
on (65 > d_l)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select d_l, b_l_r_r, b_l_r
from (
Select e, b, d
from p2
where (d = e)
) T1(e_l, b_l, d_l)
inner join (
Select b_l, b_l_r
from (
Select b
from p2
where ((a < 60) AND ((2 + d) = e))
) T1(b_l)
left join (
select b_l, e_r
from (
Select b_l, e_r, a_r
from (
Select c, b
from p2
where (58 = e)
) T1(c_l, b_l)
inner join (
Select e, a
from p2
where (0 > (35 * (b * 59)))
) T2(e_r, a_r)
on (66 = e_r)
) T1
union all
select d_l, a_r
from (
Select d_l, a_r
from (
Select d
from p3
where (71 > 43)
) T1(d_l)
full join (
Select a
from p2
where (94 > (42 + 14))
) T2(a_r)
on ((32 = 26) OR (a_r < 93))
) T2
) T2(b_l_r, e_r_r)
on ((6 = 91) AND ((((b_l * (b_l + b_l_r)) + 74) + b_l_r) = 32))
) T2(b_l_r, b_l_r_r)
on (14 = d_l)
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
Select b_l, d_r_r, d_l_l_r, a_r_r, e_l_l_r
from (
Select c, a, b
from p5
where (96 = 3)
) T1(c_l, a_l, b_l)
full join (
Select e_l_l, d_l_l, a_r, d_r
from (
Select e_l, d_l, e_r
from (
select e, d
from (
Select e, d
from p5
where ((62 = 0) OR ((95 = (5 - b)) AND (79 < (d - 30))))
) T1
union all
select e, c
from (
Select e, c
from p3
where ((c = 4) AND (d > 88))
) T2
) T1(e_l, d_l)
left join (
Select e
from p2
where (((38 * (66 - (82 - d))) > 45) OR (46 = (e * 30)))
) T2(e_r)
on (e_l > e_l)
) T1(e_l_l, d_l_l, e_r_l)
left join (
Select e, a, d
from p3
where ((c < e) OR (84 < a))
) T2(e_r, a_r, d_r)
on (d_r = d_r)
) T2(e_l_l_r, d_l_l_r, a_r_r, d_r_r)
on (e_l_l_r = 51)
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
Select a_r_l, d_r
from (
Select a_l, b_l, a_r
from (
Select a, b
from p5
where ((b = a) OR (c = d))
) T1(a_l, b_l)
inner join (
select a
from (
select a
from (
Select a
from p1
where (a = 43)
) T1
union all
select c
from (
Select c, b
from p3
where ((a * (7 - b)) = ((b + c) + d))
) T2
) T1
union all
select e
from (
Select e, c, a
from p2
where (c < a)
) T2
) T2(a_r)
on ((24 - 21) > (1 + a_l))
) T1(a_l_l, b_l_l, a_r_l)
full join (
select b, d
from (
Select b, d
from p1
where ((((39 * ((6 + 25) - b)) - (0 - b)) > d) AND (42 = 88))
) T1
union all
select e, c
from (
Select e, c, b
from p2
where (d = e)
) T2
) T2(b_r, d_r)
on (d_r = (a_r_l * 98))
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select c_l, c_l_r, a_r_r_r
from (
select c
from (
Select c
from p1
where (e < (97 - 60))
) T1
union all
select a_l
from (
select a_l, b_l, d_r
from (
Select a_l, b_l, d_r
from (
Select a, b
from p5
where (36 < a)
) T1(a_l, b_l)
left join (
Select a, b, d
from p3
where (32 = 37)
) T2(a_r, b_r, d_r)
on ((b_l < 80) AND (20 < 86))
) T1
union all
select e, c, a
from (
Select e, c, a
from p4
where ((b = a) AND ((20 + c) = c))
) T2
) T2
) T1(c_l)
inner join (
Select c_l, b_r_r, a_r_r
from (
Select c, d
from p5
where ((51 > b) AND (d > 55))
) T1(c_l, d_l)
inner join (
Select a_l, a_r, b_r
from (
Select a
from p2
where ((b = b) AND (e = e))
) T1(a_l)
left join (
Select c, a, b
from p2
where ((a - c) > 31)
) T2(c_r, a_r, b_r)
on ((87 + (93 * 38)) > 41)
) T2(a_l_r, a_r_r, b_r_r)
on (14 < 59)
) T2(c_l_r, b_r_r_r, a_r_r_r)
on (78 > 41)
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
Select a_r_l, a_l_r, c_l_r, e_r_r
from (
Select e_l, c_l, a_r
from (
Select e, c, a, d
from p4
where (e < b)
) T1(e_l, c_l, a_l, d_l)
inner join (
Select a
from p1
where (a < 66)
) T2(a_r)
on (e_l = e_l)
) T1(e_l_l, c_l_l, a_r_l)
full join (
select c_l, a_l, e_r
from (
Select c_l, a_l, e_r, b_r
from (
Select c, a
from p1
where (d = b)
) T1(c_l, a_l)
inner join (
Select e, b, d
from p3
where ((b + a) = 2)
) T2(e_r, b_r, d_r)
on (((71 * c_l) < 35) OR ((72 < (a_l - 84)) OR (e_r < e_r)))
) T1
union all
select e, c, b
from (
Select e, c, b
from p3
where (49 = d)
) T2
) T2(c_l_r, a_l_r, e_r_r)
on ((c_l_r = c_l_r) AND (38 = 11))
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
Select a_l_l, e_r, c_r
from (
Select a_l, b_l, d_r
from (
Select c, a, b
from p2
where (38 = 79)
) T1(c_l, a_l, b_l)
left join (
Select d
from p5
where (1 < (20 - a))
) T2(d_r)
on ((a_l < (a_l * b_l)) AND (18 = 33))
) T1(a_l_l, b_l_l, d_r_l)
left join (
Select e, c
from p5
where ((34 * 82) < 46)
) T2(e_r, c_r)
on ((76 = a_l_l) OR (87 > ((e_r * a_l_l) - 80)))
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
Select d_r_l_r_l, a_l_r_r_l, e_r
from (
Select e_l, a_l_r_r, d_r_l_r
from (
Select e
from p4
where (a = 5)
) T1(e_l)
full join (
Select d_r_l, e_l_l, a_l_r
from (
Select e_l, d_r
from (
select e, d
from (
Select e, d
from p4
where ((a > (a - 1)) AND (6 > 68))
) T1
union all
select b_l, e_r
from (
Select b_l, e_r, b_r
from (
Select b
from p2
where (46 < (b * c))
) T1(b_l)
full join (
Select e, b, d
from p3
where ((45 < b) AND ((12 < a) OR ((e < d) OR (20 > b))))
) T2(e_r, b_r, d_r)
on ((b_l < 42) OR (40 = 24))
) T2
) T1(e_l, d_l)
inner join (
Select d
from p5
where (96 = b)
) T2(d_r)
on (74 < 78)
) T1(e_l_l, d_r_l)
left join (
Select a_l, d_r_r_r
from (
Select a
from p2
where ((b > (e + e)) AND (69 = d))
) T1(a_l)
left join (
Select d_l, c_l_r, d_r_r
from (
Select d
from p5
where (d = 19)
) T1(d_l)
left join (
Select c_l, d_r
from (
Select e, c, a, d
from p2
where (c < a)
) T1(e_l, c_l, a_l, d_l)
inner join (
Select e, d
from p3
where ((11 + a) > 97)
) T2(e_r, d_r)
on (71 > ((d_r + (((41 + ((d_r + d_r) * 30)) * c_l) + c_l)) - d_r))
) T2(c_l_r, d_r_r)
on ((57 = (d_l - 83)) OR ((d_r_r = d_l) AND (2 < (7 * d_r_r))))
) T2(d_l_r, c_l_r_r, d_r_r_r)
on (82 = (d_r_r_r - (a_l * (d_r_r_r + (a_l + a_l)))))
) T2(a_l_r, d_r_r_r_r)
on (40 < 81)
) T2(d_r_l_r, e_l_l_r, a_l_r_r)
on (35 = (((d_r_l_r - 84) + d_r_l_r) + 20))
) T1(e_l_l, a_l_r_r_l, d_r_l_r_l)
left join (
select e
from (
Select e
from p3
where (49 < (e - b))
) T1
union all
select c_l
from (
Select c_l, a_l, d_l, d_r
from (
Select c, a, d
from p3
where ((c = 77) AND (50 < a))
) T1(c_l, a_l, d_l)
left join (
Select c, d
from p3
where (((d + 74) = d) AND ((c > e) OR ((30 > b) AND (86 = (c - c)))))
) T2(c_r, d_r)
on (c_l < 39)
) T2
) T2(e_r)
on (23 < 83)
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select b_r_l, e_r_l, d_r
from (
Select c_r_l, e_r, b_r
from (
Select b_l, c_r, a_r
from (
Select b
from p5
where (90 > 13)
) T1(b_l)
inner join (
Select c, a
from p4
where (0 > 61)
) T2(c_r, a_r)
on (b_l > (c_r * 90))
) T1(b_l_l, c_r_l, a_r_l)
full join (
Select e, b, d
from p3
where (((32 - (c - ((a + 30) * a))) - d) = d)
) T2(e_r, b_r, d_r)
on (c_r_l = b_r)
) T1(c_r_l_l, e_r_l, b_r_l)
full join (
Select d
from p2
where ((c - e) = b)
) T2(d_r)
on (69 = (e_r_l * 58))
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test21exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
Select e_r_l, d_l_l, e_r
from (
Select c_l, d_l, e_r, d_r
from (
Select e, c, d
from p1
where (a = 89)
) T1(e_l, c_l, d_l)
inner join (
Select e, c, d
from p4
where ((((75 * ((b * 81) + a)) - (88 + 51)) > c) OR (28 = 33))
) T2(e_r, c_r, d_r)
on (e_r = e_r)
) T1(c_l_l, d_l_l, e_r_l, d_r_l)
full join (
Select e
from p2
where ((59 * 57) = a)
) T2(e_r)
on (54 > e_r)
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
Select e_l, b_l, e_r_l_r, e_r_r
from (
Select e, b
from p3
where ((c - (c + d)) > d)
) T1(e_l, b_l)
inner join (
Select e_r_l, e_r
from (
Select a_l_l, d_l_l, e_r
from (
select a_l, d_l
from (
Select a_l, d_l, c_r
from (
Select a, b, d
from p1
where (((69 - d) = e) OR (b = 21))
) T1(a_l, b_l, d_l)
left join (
select c
from (
Select c, a
from p2
where ((43 < c) OR ((c * 96) = 54))
) T1
union all
select b
from (
Select b
from p3
where (e = 70)
) T2
) T2(c_r)
on ((a_l < 45) OR (54 = 87))
) T1
union all
select e, b
from (
Select e, b
from p5
where (26 > 22)
) T2
) T1(a_l_l, d_l_l)
inner join (
Select e, b
from p2
where ((d = 42) OR (e = b))
) T2(e_r, b_r)
on (e_r > e_r)
) T1(a_l_l_l, d_l_l_l, e_r_l)
left join (
Select e
from p4
where ((b = (e + (16 + (d + d)))) AND ((97 = a) AND (d > b)))
) T2(e_r)
on ((5 * e_r_l) = e_r_l)
) T2(e_r_l_r, e_r_r)
on (97 < e_r_r)
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
    #**********************************************
    _testmgr.testcase_end(desc)

