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
    
def test001(desc="""Joins Set 36"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t1
where (62 = c)
) T1
union all
select c, a
from (
Select c, a, d
from t1
where (c = d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l_l_l_l
from (
select b_l_l_l_l, c_r_l, d_r_l_l
from (
Select b_l_l_l_l, c_r_l, d_r_l_l, d_l_l_r, c_r_r
from (
Select d_r_l, b_l_l_l, e_r, c_r
from (
Select b_l_l, b_r, d_r
from (
Select e_l, b_l, d_l, b_r_r
from (
Select e, b, d
from t2
where (97 = 11)
) T1(e_l, b_l, d_l)
full join (
Select a_l, b_l, b_r
from (
Select e, c, a, b
from t2
where (d = (71 + 2))
) T1(e_l, c_l, a_l, b_l)
left join (
Select e, a, b
from t4
where (((26 * d) + (b * (39 * b))) < 8)
) T2(e_r, a_r, b_r)
on (66 > b_l)
) T2(a_l_r, b_l_r, b_r_r)
on (b_l < 82)
) T1(e_l_l, b_l_l, d_l_l, b_r_r_l)
left join (
Select b, d
from t4
where ((57 - 59) > 27)
) T2(b_r, d_r)
on ((d_r + b_r) = (b_r + 95))
) T1(b_l_l_l, b_r_l, d_r_l)
inner join (
select e, c
from (
select e, c, b
from (
Select e, c, b
from t3
where (d = (c + d))
) T1
union all
select e_l, d_l, e_r
from (
Select e_l, d_l, e_r, b_r, d_r
from (
Select e, d
from t2
where (b = (((d * 14) - c) - ((c * (80 + (74 * b))) + 19)))
) T1(e_l, d_l)
left join (
Select e, a, b, d
from t3
where (c = (b - e))
) T2(e_r, a_r, b_r, d_r)
on (e_l < (77 + 27))
) T2
) T1
union all
select e, c
from (
Select e, c
from t5
where (b > c)
) T2
) T2(e_r, c_r)
on (81 = 95)
) T1(d_r_l_l, b_l_l_l_l, e_r_l, c_r_l)
left join (
Select d_l_l, c_r
from (
Select e_l, d_l, c_r
from (
Select e, c, d
from t3
where (83 = (79 * b))
) T1(e_l, c_l, d_l)
inner join (
Select c
from t4
where (e < 75)
) T2(c_r)
on (46 = d_l)
) T1(e_l_l, d_l_l, c_r_l)
inner join (
Select c
from t3
where ((b - ((86 + (21 - 89)) + 5)) = 18)
) T2(c_r)
on (21 = c_r)
) T2(d_l_l_r, c_r_r)
on (d_r_l_l > c_r_l)
) T1
union all
select e, b, d
from (
Select e, b, d
from t1
where (97 < c)
) T2
) T1
union all
select e
from (
Select e
from t3
where ((99 + a) > 12)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_r_r_l, a_r_l_l_r
from (
Select c_r_r_l, a_r_l_l_r
from (
Select b_r_l_l, b_r_r, d_l_l_r, c_r_r
from (
select b_r_l
from (
select b_r_l
from (
select b_r_l
from (
Select b_r_l, e_r_r_l_l, e_r, a_r
from (
Select a_l_l, e_r_r_l, b_r
from (
Select a_l, c_r_r, e_r_r
from (
Select a, b
from t2
where (d = b)
) T1(a_l, b_l)
inner join (
Select e_l, e_r, c_r
from (
Select e
from t2
where (84 = ((((3 - e) - 84) * 8) - d))
) T1(e_l)
left join (
Select e, c
from t2
where (c = d)
) T2(e_r, c_r)
on (e_l = c_r)
) T2(e_l_r, e_r_r, c_r_r)
on (2 > 5)
) T1(a_l_l, c_r_r_l, e_r_r_l)
left join (
Select a, b
from t1
where (73 < 15)
) T2(a_r, b_r)
on (a_l_l = (42 - (a_l_l + 5)))
) T1(a_l_l_l, e_r_r_l_l, b_r_l)
inner join (
Select e, a
from t2
where (29 < 5)
) T2(e_r, a_r)
on (65 = (e_r * a_r))
) T1
union all
select c
from (
Select c
from t5
where (36 = a)
) T2
) T1
union all
select b_r_r_l
from (
Select b_r_r_l, e_r, b_r
from (
Select e_r_l_l_l, b_r_r
from (
select e_r_l_l
from (
Select e_r_l_l, e_l_l_l, a_l_r, c_l_r, e_r_r_r
from (
Select e_l_l, e_r_l, d_r
from (
Select e_l, c_l, e_r
from (
Select e, c
from t4
where (56 = a)
) T1(e_l, c_l)
left join (
Select e, b
from t5
where (87 = 67)
) T2(e_r, b_r)
on ((c_l * 32) = 90)
) T1(e_l_l, c_l_l, e_r_l)
left join (
Select a, d
from t5
where (29 < ((86 * d) * a))
) T2(a_r, d_r)
on (e_l_l < 90)
) T1(e_l_l_l, e_r_l_l, d_r_l)
left join (
Select e_l, c_l, a_l, c_l_l_r_l_r, e_r_r
from (
Select e, c, a
from t4
where ((d - 97) = (85 - 5))
) T1(e_l, c_l, a_l)
full join (
Select c_l_l_r_l, e_r
from (
Select a_l, b_l, c_l_l_r
from (
Select a, b
from t5
where (a = d)
) T1(a_l, b_l)
inner join (
Select c_l_l, c_r, a_r
from (
Select c_l, b_l, b_r
from (
Select c, b
from t4
where (38 = c)
) T1(c_l, b_l)
left join (
Select b
from t4
where ((a * b) < e)
) T2(b_r)
on (b_r = 68)
) T1(c_l_l, b_l_l, b_r_l)
left join (
Select c, a
from t5
where (17 = d)
) T2(c_r, a_r)
on (63 = (c_l_l * c_r))
) T2(c_l_l_r, c_r_r, a_r_r)
on (68 > a_l)
) T1(a_l_l, b_l_l, c_l_l_r_l)
left join (
Select e, b
from t3
where (33 = c)
) T2(e_r, b_r)
on (c_l_l_r_l = c_l_l_r_l)
) T2(c_l_l_r_l_r, e_r_r)
on (28 > c_l)
) T2(e_l_r, c_l_r, a_l_r, c_l_l_r_l_r_r, e_r_r_r)
on (68 < 9)
) T1
union all
select e
from (
Select e
from t5
where ((c - (43 + (4 * e))) = ((b * b) + 8))
) T2
) T1(e_r_l_l_l)
full join (
Select d_l, b_r, d_r
from (
Select e, d
from t2
where (d > 54)
) T1(e_l, d_l)
left join (
Select b, d
from t4
where (86 > 98)
) T2(b_r, d_r)
on ((d_l * 36) = 39)
) T2(d_l_r, b_r_r, d_r_r)
on (b_r_r = 54)
) T1(e_r_l_l_l_l, b_r_r_l)
full join (
Select e, b
from t3
where (e < 40)
) T2(e_r, b_r)
on (b_r_r_l > (b_r + 1))
) T2
) T1
union all
select a
from (
Select a
from t2
where (a > d)
) T2
) T1(b_r_l_l)
inner join (
Select d_l_l, c_r, b_r, d_r
from (
Select a_l, d_l, c_r
from (
Select a, d
from t5
where (b > d)
) T1(a_l, d_l)
full join (
Select c, b
from t3
where (43 < (e - 47))
) T2(c_r, b_r)
on (d_l > d_l)
) T1(a_l_l, d_l_l, c_r_l)
left join (
Select c, b, d
from t5
where (30 = 76)
) T2(c_r, b_r, d_r)
on (((b_r * d_r) - 93) = 60)
) T2(d_l_l_r, c_r_r, b_r_r, d_r_r)
on (49 > d_l_l_r)
) T1(b_r_l_l_l, b_r_r_l, d_l_l_r_l, c_r_r_l)
left join (
Select a_r_l_l, b_r, d_r
from (
Select a_r_l, a_l_l_l, a_r, d_r
from (
Select a_l_l, a_r
from (
Select c_l, a_l, b_r_r, c_l_r
from (
Select c, a
from t3
where (32 > 59)
) T1(c_l, a_l)
left join (
Select c_l, b_r
from (
Select c, d
from t4
where (a = 81)
) T1(c_l, d_l)
full join (
Select c, b
from t1
where (((e + (e * c)) + ((53 + 24) - b)) < d)
) T2(c_r, b_r)
on (61 < c_l)
) T2(c_l_r, b_r_r)
on ((15 * b_r_r) = (24 + (b_r_r + b_r_r)))
) T1(c_l_l, a_l_l, b_r_r_l, c_l_r_l)
full join (
Select a
from t2
where (91 = (c + c))
) T2(a_r)
on (24 = (a_l_l * 77))
) T1(a_l_l_l, a_r_l)
inner join (
Select a, d
from t4
where (13 = d)
) T2(a_r, d_r)
on (a_r > 28)
) T1(a_r_l_l, a_l_l_l_l, a_r_l, d_r_l)
full join (
Select b, d
from t4
where (b = c)
) T2(b_r, d_r)
on (b_r > 5)
) T2(a_r_l_l_r, b_r_r, d_r_r)
on (((91 + (c_r_r_l * a_r_l_l_r)) - (21 - (a_r_l_l_r * 37))) = a_r_l_l_r)
) T1
union all
select d_l_l_l, e_r_l
from (
Select d_l_l_l, e_r_l, e_r, c_r
from (
Select d_l_l, e_r
from (
select d_l, e_l_r
from (
Select d_l, e_l_r
from (
Select e, b, d
from t3
where ((b - (c + b)) < (b - 31))
) T1(e_l, b_l, d_l)
left join (
Select e_l, b_l, b_r
from (
Select e, b
from t1
where (a = (a * 93))
) T1(e_l, b_l)
left join (
Select b
from t5
where (c = 88)
) T2(b_r)
on (b_r = e_l)
) T2(e_l_r, b_l_r, b_r_r)
on (d_l = 89)
) T1
union all
select a, b
from (
Select a, b
from t2
where (a = (0 - c))
) T2
) T1(d_l_l, e_l_r_l)
left join (
Select e, a, b
from t3
where ((c + 44) < (38 + (42 * 96)))
) T2(e_r, a_r, b_r)
on (90 = d_l_l)
) T1(d_l_l_l, e_r_l)
left join (
Select e, c, d
from t2
where (46 > (50 + c))
) T2(e_r, c_r, d_r)
on (d_l_l_l > 5)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
Select e, c, b, d
from t2
where (a = 30)
) T1
union all
select c_l_l, e_r_l, c_l_r
from (
Select c_l_l, e_r_l, c_l_r
from (
Select e_l, c_l, e_r, a_r
from (
Select e, c, a, b
from t4
where (74 > 62)
) T1(e_l, c_l, a_l, b_l)
left join (
select e, a
from (
Select e, a
from t2
where ((60 * 73) > e)
) T1
union all
select c, a
from (
Select c, a
from t2
where (66 = c)
) T2
) T2(e_r, a_r)
on (c_l > (c_l - 58))
) T1(e_l_l, c_l_l, e_r_l, a_r_l)
inner join (
select c_l, a_l
from (
Select c_l, a_l, e_l_r, e_r_r
from (
Select c, a
from t1
where (e = c)
) T1(c_l, a_l)
inner join (
Select e_l, e_r
from (
select e
from (
Select e, c, d
from t1
where (83 = 73)
) T1
union all
select e
from (
Select e
from t5
where (24 = 99)
) T2
) T1(e_l)
full join (
Select e, b
from t5
where ((d - 67) = 26)
) T2(e_r, b_r)
on (e_r = e_r)
) T2(e_l_r, e_r_r)
on (((c_l * 29) * 43) > e_r_r)
) T1
union all
select a, b
from (
Select a, b
from t5
where (81 = (38 - c))
) T2
) T2(c_l_r, a_l_r)
on (20 < e_r_l)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e, b, d
from (
Select e, b, d
from t4
where (14 = 7)
) T1
union all
select e_l_l_l, a_l_r, c_r_r
from (
Select e_l_l_l, a_l_r, c_r_r
from (
Select e_l_l, d_r
from (
Select e_l, b_r
from (
Select e, a
from t5
where (e = 53)
) T1(e_l, a_l)
left join (
Select e, a, b
from t3
where (72 > 67)
) T2(e_r, a_r, b_r)
on (e_l < b_r)
) T1(e_l_l, b_r_l)
left join (
Select c, d
from t3
where (b = d)
) T2(c_r, d_r)
on (e_l_l = (31 + 74))
) T1(e_l_l_l, d_r_l)
inner join (
Select a_l, c_r
from (
select a
from (
Select a
from t2
where (e < (c - 65))
) T1
union all
select d
from (
Select d
from t1
where (82 < a)
) T2
) T1(a_l)
left join (
Select c, a, b
from t3
where (0 = (((a + a) * 39) + b))
) T2(c_r, a_r, b_r)
on (42 > c_r)
) T2(a_l_r, c_r_r)
on (a_l_r = c_r_r)
) T2
) T1
union all
select a
from (
Select a
from t2
where ((a * e) > b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l
from (
select d_l, e_r, c_r
from (
Select d_l, e_r, c_r
from (
Select e, d
from t2
where ((84 * 52) > ((a * e) - a))
) T1(e_l, d_l)
inner join (
Select e, c
from t5
where (42 = e)
) T2(e_r, c_r)
on (38 = d_l)
) T1
union all
select c, a, d
from (
Select c, a, d
from t4
where (21 = c)
) T2
) T1
union all
select a
from (
Select a
from t4
where ((a * 90) = (b + 56))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a
from t1
where (88 > 71)
) T1
union all
select b_r_l, e_l_l
from (
Select b_r_l, e_l_l, e_r, c_r
from (
Select e_l, c_l, b_r
from (
Select e, c
from t2
where (a > a)
) T1(e_l, c_l)
left join (
Select b, d
from t4
where (c = (d + e))
) T2(b_r, d_r)
on (c_l > 51)
) T1(e_l_l, c_l_l, b_r_l)
full join (
Select e, c
from t1
where (79 = d)
) T2(e_r, c_r)
on ((59 + c_r) < 17)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t2
where (e < b)
) T1
union all
select a, d
from (
Select a, d
from t4
where (d = 49)
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
select e, d
from (
select e, d
from (
Select e, d
from t3
where (c = c)
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, b_l, e_r
from (
Select e, c, b, d
from t1
where (26 = 61)
) T1(e_l, c_l, b_l, d_l)
left join (
Select e
from t5
where (b = 44)
) T2(e_r)
on (91 > e_r)
) T2
) T1
union all
select c_l, b_r
from (
Select c_l, b_r
from (
select c
from (
Select c, d
from t4
where (b = e)
) T1
union all
select e
from (
Select e
from t3
where (e < 49)
) T2
) T1(c_l)
inner join (
Select b
from t3
where (a < b)
) T2(b_r)
on (b_r = ((c_l - c_l) * c_l))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
select a
from (
Select a
from t5
where (97 = e)
) T1
union all
select e
from (
Select e, b
from t1
where ((29 * e) = 36)
) T2
) T1
union all
select d
from (
Select d
from t2
where (16 < d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t2
where (((36 * (41 - d)) + (((42 * 52) - 77) - 84)) < b)
) T1
union all
select e, c
from (
Select e, c, b
from t5
where (34 = 68)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a
from t5
where (d = c)
) T1
union all
select e
from (
select e
from (
Select e, c
from t1
where (8 = 89)
) T1
union all
select e
from (
Select e
from t5
where (81 = 51)
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
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
select a_l
from (
Select a_l, b_l, a_r
from (
Select c, a, b, d
from t2
where (51 = (b - ((7 - b) - a)))
) T1(c_l, a_l, b_l, d_l)
full join (
Select a, d
from t4
where (e > c)
) T2(a_r, d_r)
on (25 = 31)
) T1
union all
select c_r_l
from (
select c_r_l
from (
Select c_r_l, d_r_l_l, c_r_r
from (
Select d_r_l, a_r_r_l_l_l, c_r, a_r
from (
Select a_r_r_l_l, e_r_l_r_l_l, d_r
from (
Select a_l_l, e_r_l_r_l, a_r_r_l, b_r
from (
Select a_l, e_r_l_r, a_r_r
from (
Select c, a, b, d
from t1
where (c = 71)
) T1(c_l, a_l, b_l, d_l)
full join (
Select e_r_l, b_r_r_r_l_l, a_r
from (
Select c_l_l, b_r_r_r_l, e_r, c_r, b_r
from (
Select c_l, e_l_r, b_r_r_r
from (
Select c
from t5
where (24 < 3)
) T1(c_l)
full join (
Select e_l, b_r_r, b_l_r
from (
select e
from (
Select e, b
from t4
where (d > (22 * 30))
) T1
union all
select d
from (
Select d
from t1
where ((27 * 3) = 16)
) T2
) T1(e_l)
left join (
Select b_l, e_r, b_r
from (
select b
from (
Select b
from t3
where ((14 * (a - c)) > e)
) T1
union all
select b_l_r_l
from (
select b_l_r_l
from (
Select b_l_r_l, e_r
from (
Select e_l, b_l, b_l_r
from (
Select e, c, b
from t4
where (d = (79 - e))
) T1(e_l, c_l, b_l)
full join (
Select b_l, b_l_r
from (
Select e, b
from t1
where (19 > e)
) T1(e_l, b_l)
full join (
Select e_l, b_l, c_r
from (
Select e, b
from t1
where (e > 37)
) T1(e_l, b_l)
full join (
Select c, d
from t3
where (((d - e) * c) = 33)
) T2(c_r, d_r)
on (e_l = c_r)
) T2(e_l_r, b_l_r, c_r_r)
on (30 = ((b_l_r + b_l) + 73))
) T2(b_l_r, b_l_r_r)
on (35 < b_l)
) T1(e_l_l, b_l_l, b_l_r_l)
inner join (
Select e, a
from t3
where (25 = (31 * b))
) T2(e_r, a_r)
on (b_l_r_l = b_l_r_l)
) T1
union all
select d
from (
Select d
from t5
where (28 > a)
) T2
) T2
) T1(b_l)
inner join (
Select e, b, d
from t1
where (b > c)
) T2(e_r, b_r, d_r)
on (0 < 86)
) T2(b_l_r, e_r_r, b_r_r)
on (b_r_r = 84)
) T2(e_l_r, b_r_r_r, b_l_r_r)
on ((95 * e_l_r) > c_l)
) T1(c_l_l, e_l_r_l, b_r_r_r_l)
full join (
Select e, c, b
from t4
where (94 = 3)
) T2(e_r, c_r, b_r)
on ((23 + (b_r_r_r_l + 11)) = c_r)
) T1(c_l_l_l, b_r_r_r_l_l, e_r_l, c_r_l, b_r_l)
full join (
Select a
from t1
where (d < (e * 85))
) T2(a_r)
on (6 = e_r_l)
) T2(e_r_l_r, b_r_r_r_l_l_r, a_r_r)
on (9 = (a_r_r + a_r_r))
) T1(a_l_l, e_r_l_r_l, a_r_r_l)
left join (
Select a, b, d
from t3
where (14 < a)
) T2(a_r, b_r, d_r)
on (a_r_r_l = 56)
) T1(a_l_l_l, e_r_l_r_l_l, a_r_r_l_l, b_r_l)
full join (
Select e, c, d
from t3
where (20 > d)
) T2(e_r, c_r, d_r)
on (57 < 66)
) T1(a_r_r_l_l_l, e_r_l_r_l_l_l, d_r_l)
left join (
Select c, a
from t1
where (d = 28)
) T2(c_r, a_r)
on (((d_r_l - 56) * a_r_r_l_l_l) > 90)
) T1(d_r_l_l, a_r_r_l_l_l_l, c_r_l, a_r_l)
full join (
Select e_r_l, b_l_l, c_r
from (
Select a_l, b_l, e_r
from (
Select a, b
from t3
where (((60 - d) + 43) < e)
) T1(a_l, b_l)
inner join (
Select e
from t2
where (c = e)
) T2(e_r)
on (b_l < a_l)
) T1(a_l_l, b_l_l, e_r_l)
full join (
Select c
from t4
where ((93 + d) = 13)
) T2(c_r)
on (c_r = (b_l_l - 17))
) T2(e_r_l_r, b_l_l_r, c_r_r)
on (11 < c_r_r)
) T1
union all
select e
from (
select e
from (
Select e
from t2
where (((72 - d) + a) = a)
) T1
union all
select a
from (
Select a, d
from t5
where (88 > 40)
) T2
) T2
) T2
) T1
union all
select a
from (
Select a, b
from t1
where ((97 * 53) = a)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, b, d
from t4
where (25 < 43)
) T1
union all
select c_r_r_l, a_r
from (
Select c_r_r_l, a_r
from (
Select b_l_l, c_l_r, c_r_r
from (
Select b_l, a_r
from (
Select b, d
from t3
where (24 < 48)
) T1(b_l, d_l)
full join (
Select a
from t2
where (a < (((a * b) - c) - 23))
) T2(a_r)
on (32 < 70)
) T1(b_l_l, a_r_l)
left join (
select c_l, c_r
from (
Select c_l, c_r
from (
Select c
from t5
where (d = (c + (c + (b * b))))
) T1(c_l)
left join (
Select c, d
from t1
where (c < d)
) T2(c_r, d_r)
on (c_l < c_l)
) T1
union all
select e, b
from (
Select e, b
from t3
where (79 = b)
) T2
) T2(c_l_r, c_r_r)
on (b_l_l = c_l_r)
) T1(b_l_l_l, c_l_r_l, c_r_r_l)
left join (
Select a
from t5
where (23 > 23)
) T2(a_r)
on ((22 - c_r_r_l) > (0 + a_r))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
Select a_l, d_l, a_r_r, e_r_r
from (
Select a, b, d
from t3
where (((b - e) + 96) = d)
) T1(a_l, b_l, d_l)
inner join (
Select d_l, e_r, a_r, b_r
from (
select d
from (
Select d
from t5
where (d = 4)
) T1
union all
select e
from (
Select e
from t2
where (((b - 67) * ((b * (a - (e * 13))) - e)) = e)
) T2
) T1(d_l)
inner join (
Select e, a, b
from t1
where (66 > b)
) T2(e_r, a_r, b_r)
on (a_r = (6 + (51 + d_l)))
) T2(d_l_r, e_r_r, a_r_r, b_r_r)
on (97 = 40)
) T1
union all
select d
from (
Select d
from t5
where ((a * e) = (79 + c))
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
select b_l, d_l, a_r_r_r
from (
Select b_l, d_l, a_r_r_r, c_r_l_r, d_r_l_r
from (
Select b, d
from t5
where (a = (83 + (38 * (72 - d))))
) T1(b_l, d_l)
inner join (
Select d_r_l, c_r_l, b_r_r, a_r_r
from (
Select a_l_l, c_r, d_r
from (
Select a_l, c_r_r
from (
Select e, a, b
from t3
where (99 > a)
) T1(e_l, a_l, b_l)
left join (
Select c_l, c_r
from (
select c, b
from (
select c, b
from (
Select c, b
from t1
where (d = e)
) T1
union all
select c_l, a_r_r_l_r_r
from (
Select c_l, a_r_r_l_r_r, d_l_r
from (
Select c
from t5
where (d < 6)
) T1(c_l)
left join (
Select d_l, a_r_r, a_r_r_l_r
from (
Select d
from t1
where (62 = d)
) T1(d_l)
left join (
Select b_l_r_l, a_r_r_l, d_l_l, a_r
from (
Select e_l, d_l, a_r_r, b_l_r
from (
Select e, d
from t3
where (8 < (b * 9))
) T1(e_l, d_l)
left join (
Select b_l, d_l, c_r, a_r
from (
Select b, d
from t3
where ((97 + 36) = 94)
) T1(b_l, d_l)
inner join (
Select c, a
from t4
where ((c * ((14 + 66) - c)) > (77 * a))
) T2(c_r, a_r)
on ((c_r - 37) > (b_l - d_l))
) T2(b_l_r, d_l_r, c_r_r, a_r_r)
on (98 = a_r_r)
) T1(e_l_l, d_l_l, a_r_r_l, b_l_r_l)
full join (
select a
from (
Select a
from t5
where (31 > d)
) T1
union all
select a_l_r_l
from (
Select a_l_r_l, b_l_l_l, e_r_l_l, e_r, b_r
from (
Select e_r_l, b_l_l, a_l_r
from (
Select b_l, e_r
from (
Select b
from t1
where (d = e)
) T1(b_l)
full join (
Select e, c, a
from t4
where (98 < 92)
) T2(e_r, c_r, a_r)
on (21 = (e_r - 54))
) T1(b_l_l, e_r_l)
inner join (
Select c_l, a_l, b_r, d_r
from (
Select c, a, d
from t1
where (e = 91)
) T1(c_l, a_l, d_l)
left join (
Select b, d
from t5
where (4 > 56)
) T2(b_r, d_r)
on (b_r < a_l)
) T2(c_l_r, a_l_r, b_r_r, d_r_r)
on (b_l_l = 99)
) T1(e_r_l_l, b_l_l_l, a_l_r_l)
left join (
select e, c, b
from (
Select e, c, b
from t4
where (b = ((46 * e) - a))
) T1
union all
select a_l, b_r, d_r
from (
Select a_l, b_r, d_r
from (
Select a
from t1
where (80 = 47)
) T1(a_l)
inner join (
Select a, b, d
from t4
where (44 = 43)
) T2(a_r, b_r, d_r)
on ((18 + 82) > 23)
) T2
) T2(e_r, c_r, b_r)
on (e_r_l_l > 50)
) T2
) T2(a_r)
on (d_l_l = ((a_r_r_l - 15) * a_r))
) T2(b_l_r_l_r, a_r_r_l_r, d_l_l_r, a_r_r)
on (44 = d_l)
) T2(d_l_r, a_r_r_r, a_r_r_l_r_r)
on ((c_l - c_l) > 71)
) T2
) T1
union all
select a, b
from (
Select a, b, d
from t2
where ((22 * 94) < c)
) T2
) T1(c_l, b_l)
left join (
select c
from (
Select c
from t5
where (e = 40)
) T1
union all
select b
from (
select b
from (
Select b
from t1
where (e = 67)
) T1
union all
select e
from (
Select e, d
from t3
where (e < b)
) T2
) T2
) T2(c_r)
on (((c_l - 22) * (4 + (29 * c_r))) = c_l)
) T2(c_l_r, c_r_r)
on (c_r_r = 40)
) T1(a_l_l, c_r_r_l)
left join (
Select c, d
from t1
where (d < (28 - 81))
) T2(c_r, d_r)
on (30 = d_r)
) T1(a_l_l_l, c_r_l, d_r_l)
inner join (
Select a_l, b_l, a_r, b_r
from (
select a, b
from (
Select a, b
from t3
where (72 > b)
) T1
union all
select b_r_l, b_r
from (
select b_r_l, b_r, d_r
from (
Select b_r_l, b_r, d_r
from (
Select d_l, c_r, b_r
from (
Select e, d
from t1
where ((c - c) < (b * 9))
) T1(e_l, d_l)
inner join (
Select c, a, b
from t4
where (a = 85)
) T2(c_r, a_r, b_r)
on ((d_l - c_r) < d_l)
) T1(d_l_l, c_r_l, b_r_l)
full join (
Select b, d
from t5
where (c > 12)
) T2(b_r, d_r)
on (20 > b_r)
) T1
union all
select d_l, a_l_r, e_l_r
from (
Select d_l, a_l_r, e_l_r
from (
Select d
from t3
where (b = 10)
) T1(d_l)
left join (
Select e_l, a_l, a_r, d_r
from (
Select e, a, b
from t2
where ((c - 60) = 25)
) T1(e_l, a_l, b_l)
left join (
select a, d
from (
Select a, d
from t4
where (e = c)
) T1
union all
select d_r_l_l, e_r
from (
select d_r_l_l, e_r, a_r
from (
Select d_r_l_l, e_r, a_r, b_r
from (
Select d_r_l, d_r
from (
Select e_l, b_l, e_r, d_r
from (
Select e, b
from t1
where (82 = b)
) T1(e_l, b_l)
full join (
Select e, d
from t3
where (66 = ((3 + 24) - b))
) T2(e_r, d_r)
on ((e_r * 78) < (31 + (b_l - d_r)))
) T1(e_l_l, b_l_l, e_r_l, d_r_l)
left join (
Select d
from t1
where (c > 80)
) T2(d_r)
on ((d_r - d_r_l) < d_r_l)
) T1(d_r_l_l, d_r_l)
inner join (
Select e, a, b
from t4
where (b < 84)
) T2(e_r, a_r, b_r)
on (d_r_l_l < (6 - d_r_l_l))
) T1
union all
select c, a, b
from (
Select c, a, b
from t1
where (c = 13)
) T2
) T2
) T2(a_r, d_r)
on (34 < d_r)
) T2(e_l_r, a_l_r, a_r_r, d_r_r)
on ((64 + (e_l_r - (68 - a_l_r))) < e_l_r)
) T2
) T2
) T1(a_l, b_l)
full join (
select a, b
from (
Select a, b, d
from t3
where (e < a)
) T1
union all
select e, a
from (
Select e, a
from t1
where (c > a)
) T2
) T2(a_r, b_r)
on (a_r = b_r)
) T2(a_l_r, b_l_r, a_r_r, b_r_r)
on (59 < b_r_r)
) T2(d_r_l_r, c_r_l_r, b_r_r_r, a_r_r_r)
on (c_r_l_r = b_l)
) T1
union all
select e, c, a
from (
Select e, c, a
from t2
where (d < (d - e))
) T2
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
select d_l, c_r, a_r
from (
Select d_l, c_r, a_r
from (
Select c, a, b, d
from t4
where (99 = (c - 10))
) T1(c_l, a_l, b_l, d_l)
left join (
Select c, a
from t5
where (1 < 82)
) T2(c_r, a_r)
on (49 = d_l)
) T1
union all
select e, c, d
from (
Select e, c, d
from t1
where (49 = c)
) T2
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
select c
from (
Select c
from t3
where (46 > d)
) T1
union all
select c
from (
Select c
from t1
where (52 = c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, a, d
from t3
where (a < a)
) T1
union all
select b
from (
Select b
from t4
where (62 > 91)
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
select b, d
from (
Select b, d
from t5
where (((c * 77) + (35 - ((d * b) + c))) < a)
) T1
union all
select e, a
from (
Select e, a
from t2
where (c > e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test36exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #************************************************
    _testmgr.testcase_end(desc)

