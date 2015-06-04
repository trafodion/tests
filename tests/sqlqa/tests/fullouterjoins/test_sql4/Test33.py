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
    
def test001(desc="""Joins Set 33"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select b, d
from (
select b, d
from (
Select b, d
from t3
where (a > (24 * d))
) T1
union all
select e_l_r_l, b_l_l
from (
Select e_l_r_l, b_l_l, e_r, a_r, d_r
from (
Select b_l, e_l_r
from (
select b
from (
select b
from (
Select b
from t4
where (c < 37)
) T1
union all
select e
from (
Select e, d
from t3
where (b = (56 + a))
) T2
) T1
union all
select b_l
from (
Select b_l, d_r
from (
Select c, b
from t1
where ((a * 14) = d)
) T1(c_l, b_l)
inner join (
select a, d
from (
Select a, d
from t2
where ((88 + 61) = 83)
) T1
union all
select c, a
from (
Select c, a, d
from t2
where (65 = 31)
) T2
) T2(a_r, d_r)
on (13 = 40)
) T2
) T1(b_l)
left join (
Select e_l, b_l, c_r
from (
Select e, b
from t5
where (c < d)
) T1(e_l, b_l)
left join (
Select c, a, b
from t3
where (29 < 36)
) T2(c_r, a_r, b_r)
on (((b_l * (4 * b_l)) * 59) = b_l)
) T2(e_l_r, b_l_r, c_r_r)
on (e_l_r = (b_l + b_l))
) T1(b_l_l, e_l_r_l)
inner join (
Select e, a, d
from t1
where ((a * (e + (86 * 10))) = (22 * c))
) T2(e_r, a_r, d_r)
on (b_l_l = d_r)
) T2
) T1
union all
select e_l, d_r_r
from (
Select e_l, d_r_r, c_r_l_r
from (
select e, a, d
from (
Select e, a, d
from t3
where (d < e)
) T1
union all
select e, c, b
from (
Select e, c, b, d
from t4
where (65 < 20)
) T2
) T1(e_l, a_l, d_l)
inner join (
Select c_r_l, d_r
from (
Select c_l, c_r
from (
Select c
from t3
where (e = a)
) T1(c_l)
full join (
Select c
from t5
where (a > a)
) T2(c_r)
on (c_l < 50)
) T1(c_l_l, c_r_l)
full join (
Select a, d
from t1
where ((16 + 82) = c)
) T2(a_r, d_r)
on (d_r < (95 + c_r_l))
) T2(c_r_l_r, d_r_r)
on (e_l > d_r_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t1
where (b < 94)
) T1
union all
select a_l_l, b_r_l
from (
Select a_l_l, b_r_l, d_r
from (
Select a_l, b_r
from (
Select a, b
from t2
where (e > (b * 73))
) T1(a_l, b_l)
left join (
Select b
from t2
where (3 = ((79 - 63) * (47 + 3)))
) T2(b_r)
on ((b_r + 81) = 36)
) T1(a_l_l, b_r_l)
inner join (
Select e, b, d
from t2
where (a < (98 - 96))
) T2(e_r, b_r, d_r)
on (35 > 1)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, c_r
from (
Select c_l, c_r
from (
Select c
from t4
where ((b - ((71 + (d * 64)) - 46)) = 1)
) T1(c_l)
left join (
Select e, c
from t5
where ((33 + (7 - a)) = d)
) T2(e_r, c_r)
on (40 = 79)
) T1
union all
select e, a
from (
Select e, a
from t4
where (83 = d)
) T2
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
select c, a
from (
Select c, a
from t4
where ((((d - e) + 50) + c) = d)
) T1
union all
select e, b
from (
select e, b
from (
Select e, b
from t5
where (e > 31)
) T1
union all
select a, d
from (
Select a, d
from t3
where (d = (a + b))
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b, d
from (
Select e, b, d
from t4
where (65 > c)
) T1
union all
select c, a, b
from (
Select c, a, b
from t3
where (10 > (a + 3))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
Select e
from t2
where (10 = d)
) T1
union all
select b
from (
Select b
from t5
where (e = 26)
) T2
) T1
union all
select e
from (
Select e, d
from t1
where (91 = 81)
) T2
order by 1
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
select e, c
from (
select e, c
from (
Select e, c, a, d
from t3
where (41 = e)
) T1
union all
select e_l, a_r
from (
Select e_l, a_r
from (
Select e, a
from t1
where (e = (e - d))
) T1(e_l, a_l)
full join (
Select a
from t2
where (b > c)
) T2(a_r)
on (13 = (5 * 25))
) T2
) T1
union all
select a_l, b_r
from (
Select a_l, b_r, d_r
from (
Select c, a, b
from t1
where (((e - ((62 + 18) - 62)) * (88 - 30)) < 94)
) T1(c_l, a_l, b_l)
inner join (
Select e, b, d
from t2
where (42 > (45 - (a - (((a + (61 * e)) * d) * (b + 51)))))
) T2(e_r, b_r, d_r)
on (78 = d_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, a
from t4
where (a = b)
) T1
union all
select b, d
from (
Select b, d
from t3
where (64 = 47)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, d
from t3
where (a < 5)
) T1
union all
select b
from (
Select b
from t2
where (((67 + (91 - 95)) * ((c * (e + a)) - 33)) = 2)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e, a
from (
Select e, a
from t2
where (89 > a)
) T1
union all
select c_r_l_l, a_r_l_l
from (
Select c_r_l_l, a_r_l_l, a_r
from (
Select a_r_l, c_r_l, e_r
from (
Select b_l, c_r, a_r
from (
Select b
from t2
where ((90 * 4) < e)
) T1(b_l)
left join (
Select c, a
from t4
where (((d + ((d + c) * e)) * e) = e)
) T2(c_r, a_r)
on ((47 - 8) > 42)
) T1(b_l_l, c_r_l, a_r_l)
left join (
Select e, c
from t5
where ((c - b) = 4)
) T2(e_r, c_r)
on (5 > e_r)
) T1(a_r_l_l, c_r_l_l, e_r_l)
inner join (
select a
from (
Select a
from t1
where (65 = (95 + 25))
) T1
union all
select e
from (
Select e, c, b
from t4
where (d = (c + (e + a)))
) T2
) T2(a_r)
on (c_r_l_l = c_r_l_l)
) T2
) T1
union all
select c
from (
Select c
from t3
where (b > 0)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a, b
from (
Select c, a, b
from t3
where (56 = d)
) T1
union all
select c_l, a_l, a_r
from (
Select c_l, a_l, a_r, b_r
from (
Select e, c, a
from t3
where (((21 * 78) + (a * (49 - (86 + 79)))) < 75)
) T1(e_l, c_l, a_l)
left join (
Select a, b
from t4
where (10 = c)
) T2(a_r, b_r)
on (b_r = (c_l - a_r))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t5
where (0 = 50)
) T1
union all
select e, c
from (
Select e, c
from t4
where (c > b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b, d
from t3
where (e = 6)
) T1
union all
select e_l, c_l_l_r_r
from (
select e_l, c_l_l_r_r
from (
Select e_l, c_l_l_r_r, d_l_r, b_l_r
from (
Select e, a
from t2
where (d > 53)
) T1(e_l, a_l)
left join (
Select b_l, d_l, c_l_l_r
from (
Select b, d
from t2
where (19 = ((36 + 65) + 27))
) T1(b_l, d_l)
full join (
Select c_l_l, e_l_l, e_r_r_l, e_r
from (
Select e_l, c_l, e_r_r
from (
select e, c
from (
Select e, c
from t3
where (8 > c)
) T1
union all
select c_l, b_l
from (
Select c_l, b_l, e_r
from (
Select c, b
from t5
where (a = b)
) T1(c_l, b_l)
left join (
Select e
from t5
where ((e - 32) < (97 - d))
) T2(e_r)
on (64 > 19)
) T2
) T1(e_l, c_l)
left join (
Select e_l, e_r, b_r
from (
Select e
from t3
where (e = d)
) T1(e_l)
left join (
Select e, a, b
from t3
where ((19 - 19) > ((c * 99) + (d * 73)))
) T2(e_r, a_r, b_r)
on (e_r = e_l)
) T2(e_l_r, e_r_r, b_r_r)
on ((25 * c_l) = 48)
) T1(e_l_l, c_l_l, e_r_r_l)
left join (
Select e, c
from t1
where (c = a)
) T2(e_r, c_r)
on (e_l_l = c_l_l)
) T2(c_l_l_r, e_l_l_r, e_r_r_l_r, e_r_r)
on (c_l_l_r = (b_l - b_l))
) T2(b_l_r, d_l_r, c_l_l_r_r)
on (46 = 76)
) T1
union all
select b_r_l, b_l_l
from (
select b_r_l, b_l_l
from (
Select b_r_l, b_l_l, b_r_r, a_l_l_r
from (
Select b_l, b_r
from (
Select b
from t1
where (c > 93)
) T1(b_l)
left join (
Select a, b, d
from t5
where (48 < c)
) T2(a_r, b_r, d_r)
on (77 = (56 - (46 + (b_r + (b_r + b_r)))))
) T1(b_l_l, b_r_l)
left join (
Select a_l_l, b_r
from (
select a_l
from (
Select a_l, d_l_r
from (
Select a
from t3
where (b = (31 - (((d - b) + 43) + 75)))
) T1(a_l)
left join (
select d_l
from (
select d_l
from (
select d_l
from (
Select d_l, b_r
from (
Select d
from t1
where (88 = 19)
) T1(d_l)
left join (
Select a, b, d
from t1
where (77 = 69)
) T2(a_r, b_r, d_r)
on (((58 * b_r) + 27) < b_r)
) T1
union all
select e
from (
Select e
from t5
where ((((38 * e) + 97) - 86) = c)
) T2
) T1
union all
select c
from (
Select c
from t5
where (85 > 91)
) T2
) T1
union all
select e
from (
Select e, c, b
from t3
where ((34 + d) = d)
) T2
) T2(d_l_r)
on (27 = a_l)
) T1
union all
select e_l
from (
select e_l
from (
Select e_l, c_l, d_l, e_r, d_r
from (
Select e, c, d
from t2
where (e = 86)
) T1(e_l, c_l, d_l)
left join (
Select e, d
from t5
where (e = 69)
) T2(e_r, d_r)
on (e_r = 13)
) T1
union all
select c_l
from (
select c_l
from (
Select c_l, e_l_r, a_r_r
from (
Select e, c, b
from t4
where (3 = c)
) T1(e_l, c_l, b_l)
left join (
Select e_l, b_l, a_r
from (
Select e, b
from t1
where (e = c)
) T1(e_l, b_l)
left join (
Select e, a
from t3
where (d > c)
) T2(e_r, a_r)
on ((25 * e_l) < (13 - (24 + e_l)))
) T2(e_l_r, b_l_r, a_r_r)
on (c_l < a_r_r)
) T1
union all
select c
from (
Select c
from t1
where (21 = a)
) T2
) T2
) T2
) T1(a_l_l)
inner join (
Select b
from t3
where (76 = a)
) T2(b_r)
on (b_r < (59 + 66))
) T2(a_l_l_r, b_r_r)
on (24 < 71)
) T1
union all
select e, c
from (
Select e, c
from t2
where (b = e)
) T2
) T2
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, d_l, e_l_r, b_r_r_r
from (
Select b_l, d_l, e_l_r, b_r_r_r
from (
Select b, d
from t3
where (e = 92)
) T1(b_l, d_l)
full join (
Select e_l, a_l_r, b_r_r
from (
Select e, a
from t1
where (d > c)
) T1(e_l, a_l)
inner join (
Select a_l, b_r
from (
Select c, a
from t4
where (94 = 88)
) T1(c_l, a_l)
inner join (
Select b
from t4
where ((5 * (81 * 80)) = d)
) T2(b_r)
on (8 = b_r)
) T2(a_l_r, b_r_r)
on (14 = e_l)
) T2(e_l_r, a_l_r_r, b_r_r_r)
on ((b_l - e_l_r) = e_l_r)
) T1
union all
select d_l_l_r_l, e_l_l_l_l, c_r_l_l, e_l_r
from (
Select d_l_l_r_l, e_l_l_l_l, c_r_l_l, e_l_r, d_r_r, d_l_r
from (
Select c_r_l, e_l_l_l, d_l_l_r, d_r_r, d_l_r_l_r
from (
Select e_l_l, c_r
from (
Select e_l, d_r
from (
Select e, a
from t5
where (c = c)
) T1(e_l, a_l)
inner join (
Select d
from t2
where (a = 29)
) T2(d_r)
on (d_r < e_l)
) T1(e_l_l, d_r_l)
inner join (
Select e, c
from t3
where (a < 18)
) T2(e_r, c_r)
on (e_l_l < (90 - 76))
) T1(e_l_l_l, c_r_l)
left join (
Select d_l_l, d_l_r_l, d_r
from (
Select d_l, e_l_l_r_r, d_l_r
from (
select c, d
from (
Select c, d
from t5
where ((d - d) > 11)
) T1
union all
select e_l, a_l_r
from (
Select e_l, a_l_r
from (
Select e
from t2
where (65 = e)
) T1(e_l)
left join (
select a_l
from (
select a_l
from (
Select a_l, d_l, e_r, c_r
from (
Select a, b, d
from t5
where (((e * 92) - 99) = e)
) T1(a_l, b_l, d_l)
left join (
select e, c
from (
Select e, c, b
from t1
where (e = d)
) T1
union all
select a, b
from (
Select a, b
from t4
where (87 = 31)
) T2
) T2(e_r, c_r)
on ((d_l + 7) = 33)
) T1
union all
select d
from (
Select d
from t4
where (c = (e - d))
) T2
) T1
union all
select b
from (
Select b
from t4
where (e = (80 * b))
) T2
) T2(a_l_r)
on (e_l < 21)
) T2
) T1(c_l, d_l)
full join (
select d_l, e_l_l_r
from (
Select d_l, e_l_l_r
from (
Select e, c, b, d
from t3
where (72 < 57)
) T1(e_l, c_l, b_l, d_l)
left join (
Select b_r_l, e_l_l, a_r, d_r
from (
Select e_l, b_r
from (
Select e, b
from t1
where (46 > 83)
) T1(e_l, b_l)
full join (
Select b, d
from t3
where (b = a)
) T2(b_r, d_r)
on (47 < (e_l - b_r))
) T1(e_l_l, b_r_l)
inner join (
Select c, a, d
from t3
where (((39 * d) + 6) > e)
) T2(c_r, a_r, d_r)
on (89 < 83)
) T2(b_r_l_r, e_l_l_r, a_r_r, d_r_r)
on (89 > 70)
) T1
union all
select e, d
from (
Select e, d
from t5
where ((a - 52) = 92)
) T2
) T2(d_l_r, e_l_l_r_r)
on (d_l < 0)
) T1(d_l_l, e_l_l_r_r_l, d_l_r_l)
inner join (
Select d
from t3
where (57 = c)
) T2(d_r)
on (d_r > 47)
) T2(d_l_l_r, d_l_r_l_r, d_r_r)
on (e_l_l_l > d_l_l_r)
) T1(c_r_l_l, e_l_l_l_l, d_l_l_r_l, d_r_r_l, d_l_r_l_r_l)
full join (
Select e_l, d_l, d_r
from (
Select e, d
from t2
where (37 > e)
) T1(e_l, d_l)
left join (
Select e, a, b, d
from t4
where (23 < 1)
) T2(e_r, a_r, b_r, d_r)
on (94 = d_l)
) T2(e_l_r, d_l_r, d_r_r)
on ((46 * d_l_r) = e_l_r)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (e > 71)
) T1
union all
select e
from (
select e
from (
Select e, b
from t2
where ((d + a) = b)
) T1
union all
select a
from (
Select a
from t1
where (67 = a)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where (86 < 36)
) T1
union all
select e
from (
Select e
from t5
where (b < a)
) T2
order by 1
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
select c
from (
Select c
from t4
where (d = (76 * ((e - 66) * a)))
) T1
union all
select d_l
from (
select d_l, e_r, b_r
from (
Select d_l, e_r, b_r
from (
Select d
from t4
where (67 < 73)
) T1(d_l)
left join (
Select e, a, b
from t1
where (d < 32)
) T2(e_r, a_r, b_r)
on (44 = b_r)
) T1
union all
select e_l, a_l, b_r
from (
Select e_l, a_l, b_r, d_r
from (
Select e, a, d
from t4
where (b < (12 - 88))
) T1(e_l, a_l, d_l)
left join (
Select e, b, d
from t4
where (d > 5)
) T2(e_r, b_r, d_r)
on (28 = 52)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t1
where (a = c)
) T1
union all
select e_l
from (
select e_l, c_l, b_r_r
from (
Select e_l, c_l, b_r_r
from (
Select e, c
from t3
where (e < (b * c))
) T1(e_l, c_l)
full join (
Select e_l_r_l, b_r
from (
Select c_l_l_l, e_r_l, e_l_r
from (
Select c_l_l, e_r, c_r
from (
Select c_l, a_l, e_r
from (
Select c, a, d
from t4
where (61 < 37)
) T1(c_l, a_l, d_l)
left join (
Select e, c
from t3
where ((38 - b) = (c + c))
) T2(e_r, c_r)
on (1 > e_r)
) T1(c_l_l, a_l_l, e_r_l)
left join (
select e, c
from (
Select e, c, b
from t1
where (57 = a)
) T1
union all
select d_l_l_l, a_r
from (
Select d_l_l_l, a_r
from (
Select e_r_l, d_l_l, c_r, b_r
from (
Select b_l, d_l, e_r
from (
Select e, b, d
from t4
where (a < 81)
) T1(e_l, b_l, d_l)
inner join (
select e
from (
Select e, a, b
from t1
where (c < b)
) T1
union all
select e
from (
select e
from (
Select e, a, d
from t1
where (c = a)
) T1
union all
select a
from (
Select a
from t5
where (85 = ((((50 + a) - e) + 41) + 32))
) T2
) T2
) T2(e_r)
on (97 = d_l)
) T1(b_l_l, d_l_l, e_r_l)
left join (
select c, b
from (
Select c, b
from t2
where (74 > 52)
) T1
union all
select c_l_l, c_r_l
from (
Select c_l_l, c_r_l, d_l_r, e_r_r
from (
select c_l, c_r, b_r, d_r
from (
Select c_l, c_r, b_r, d_r
from (
Select c
from t2
where (e = (c + c))
) T1(c_l)
left join (
Select c, b, d
from t3
where ((20 - 52) = b)
) T2(c_r, b_r, d_r)
on (55 < c_r)
) T1
union all
select e_l, c_l, a_l, c_r
from (
Select e_l, c_l, a_l, c_r, b_r
from (
Select e, c, a
from t3
where (36 = 99)
) T1(e_l, c_l, a_l)
left join (
Select c, a, b, d
from t1
where (82 = (((96 - 51) - (c - 69)) * c))
) T2(c_r, a_r, b_r, d_r)
on (66 > ((72 - 60) - (88 * 66)))
) T2
) T1(c_l_l, c_r_l, b_r_l, d_r_l)
inner join (
Select d_l, e_r
from (
Select d
from t1
where (85 = d)
) T1(d_l)
inner join (
Select e
from t4
where (e > (51 * c))
) T2(e_r)
on (d_l = ((d_l + e_r) + 52))
) T2(d_l_r, e_r_r)
on ((e_r_r * e_r_r) > e_r_r)
) T2
) T2(c_r, b_r)
on (d_l_l > 54)
) T1(e_r_l_l, d_l_l_l, c_r_l, b_r_l)
left join (
Select a, b
from t5
where (7 > b)
) T2(a_r, b_r)
on ((d_l_l_l - 78) < d_l_l_l)
) T2
) T2(e_r, c_r)
on (c_l_l = 60)
) T1(c_l_l_l, e_r_l, c_r_l)
left join (
select e_l
from (
Select e_l, c_l, b_l, c_l_r, a_r_r_r, a_l_l_r_r
from (
Select e, c, b
from t4
where ((98 + d) = 90)
) T1(e_l, c_l, b_l)
left join (
Select c_l, a_r_r, a_l_l_r
from (
Select c
from t1
where (d > a)
) T1(c_l)
left join (
Select a_l_l, e_r, a_r, b_r
from (
Select a_l, d_l, c_r, b_r, d_r
from (
Select a, d
from t4
where (26 > c)
) T1(a_l, d_l)
inner join (
Select c, b, d
from t2
where (a = ((25 + (43 * (26 * e))) - 70))
) T2(c_r, b_r, d_r)
on (92 = 0)
) T1(a_l_l, d_l_l, c_r_l, b_r_l, d_r_l)
left join (
Select e, c, a, b
from t3
where (a < a)
) T2(e_r, c_r, a_r, b_r)
on (69 = 71)
) T2(a_l_l_r, e_r_r, a_r_r, b_r_r)
on (a_r_r = c_l)
) T2(c_l_r, a_r_r_r, a_l_l_r_r)
on (13 = e_l)
) T1
union all
select a
from (
Select a
from t2
where (92 = 61)
) T2
) T2(e_l_r)
on ((77 * (((42 + 45) - 49) * e_r_l)) > (e_l_r - 26))
) T1(c_l_l_l_l, e_r_l_l, e_l_r_l)
full join (
Select a, b
from t1
where ((e - b) > 20)
) T2(a_r, b_r)
on (49 = 90)
) T2(e_l_r_l_r, b_r_r)
on (((37 * c_l) - ((46 * 51) + 76)) = 94)
) T1
union all
select e, c, b
from (
Select e, c, b
from t4
where ((2 + 74) > c)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where (96 < 27)
) T1
union all
select a_r_l_l
from (
Select a_r_l_l, c_r, b_r
from (
select a_r_l
from (
Select a_r_l, d_l_l_r
from (
Select a_l, b_l, a_r
from (
Select c, a, b
from t1
where (38 > (43 - 49))
) T1(c_l, a_l, b_l)
left join (
Select e, a
from t5
where (e = a)
) T2(e_r, a_r)
on ((98 + 43) = a_r)
) T1(a_l_l, b_l_l, a_r_l)
inner join (
select d_l_l, b_r
from (
Select d_l_l, b_r
from (
Select d_l, e_r, b_r
from (
Select a, d
from t2
where (((21 + b) + (51 - (a * (27 * 99)))) = 52)
) T1(a_l, d_l)
full join (
Select e, b
from t3
where (25 > 83)
) T2(e_r, b_r)
on (e_r = b_r)
) T1(d_l_l, e_r_l, b_r_l)
left join (
Select b, d
from t4
where (b = 22)
) T2(b_r, d_r)
on (d_l_l = 83)
) T1
union all
select e, c
from (
Select e, c
from t1
where (28 = 64)
) T2
) T2(d_l_l_r, b_r_r)
on (a_r_l < d_l_l_r)
) T1
union all
select a
from (
Select a
from t2
where ((a - (((56 * c) + ((c * b) * d)) - 16)) > b)
) T2
) T1(a_r_l_l)
inner join (
Select c, b
from t4
where (c > (25 * a))
) T2(c_r, b_r)
on (62 < 70)
) T2
order by 1
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
select a, b
from (
Select a, b
from t5
where (a = 18)
) T1
union all
select c, a
from (
Select c, a, b, d
from t1
where (d = 51)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test33exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************
    _testmgr.testcase_end(desc)

