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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""full join"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l
from (
select b_l, d_l
from (
Select b_l, d_l, e_r
from (
Select c, b, d
from t3
where (e < d)
) T1(c_l, b_l, d_l)
full join (
select e
from (
Select e, b
from t2
where (62 < ((d + (d - 36)) + e))
) T1
union all
select d
from (
Select d
from t3
where (((77 + ((94 * 92) * b)) - e) = e)
) T2
) T2(e_r)
on (97 = d_l)
) T1
union all
select e, c
from (
Select e, c
from t2
where (62 = 83)
) T2
) T1
union all
select a
from (
Select a
from t1
where (8 > 33)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b
from t2
where (a = (91 - 39))
) T1
union all
select b, d
from (
Select b, d
from t2
where (d < d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t1
where (((90 * (e + (e + (98 + (c - 67))))) - b) < 45)
) T1
union all
select e, a
from (
Select e, a
from t5
where (d > d)
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
from t3
where (69 = 95)
) T1
union all
select a_l, c_l_r
from (
Select a_l, c_l_r
from (
Select e, a, d
from t5
where (d > b)
) T1(e_l, a_l, d_l)
left join (
Select c_l, b_r_r, b_l_l_r, e_l_l_r
from (
Select e, c, a
from t2
where (7 > (57 + 47))
) T1(e_l, c_l, a_l)
full join (
Select e_l_l, b_l_l, b_r, d_r
from (
Select e_l, b_l, b_r
from (
Select e, b, d
from t1
where (a < c)
) T1(e_l, b_l, d_l)
inner join (
select b
from (
Select b, d
from t4
where (a > (e + 13))
) T1
union all
select d
from (
Select d
from t3
where ((e + 81) = 97)
) T2
) T2(b_r)
on (73 = 13)
) T1(e_l_l, b_l_l, b_r_l)
full join (
Select b, d
from t2
where ((68 - d) > 90)
) T2(b_r, d_r)
on ((32 - d_r) = 9)
) T2(e_l_l_r, b_l_l_r, b_r_r, d_r_r)
on (c_l = (78 + c_l))
) T2(c_l_r, b_r_r_r, b_l_l_r_r, e_l_l_r_r)
on (9 > a_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, a
from t5
where ((14 + 45) < 80)
) T1
union all
select c, d
from (
Select c, d
from t5
where (48 < e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t3
where (18 = a)
) T1
union all
select a
from (
Select a
from t4
where (85 > 68)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l_l, e_l_l_r_r_l, a_r
from (
Select e_l_l, e_l_l_r_r_l, a_r
from (
Select e_l, e_l_l_r_r, e_l_r, d_l_r
from (
Select e
from t1
where ((((c * b) * c) - e) = 13)
) T1(e_l)
left join (
Select e_l, d_l, e_l_l_r
from (
Select e, c, d
from t4
where (42 < ((d - 19) + a))
) T1(e_l, c_l, d_l)
inner join (
Select e_l_l, e_l_r_l, c_r
from (
Select e_l, e_l_r
from (
select e
from (
Select e, c, a
from t2
where (89 = 89)
) T1
union all
select c
from (
Select c
from t3
where (c = (99 + c))
) T2
) T1(e_l)
inner join (
select e_l
from (
Select e_l, b_l, a_r_r
from (
Select e, c, b, d
from t4
where (d < (e - e))
) T1(e_l, c_l, b_l, d_l)
inner join (
Select a_l, b_l, d_l, e_r, c_r, a_r
from (
Select a, b, d
from t1
where (11 < d)
) T1(a_l, b_l, d_l)
inner join (
Select e, c, a
from t2
where (31 = 32)
) T2(e_r, c_r, a_r)
on (a_r > b_l)
) T2(a_l_r, b_l_r, d_l_r, e_r_r, c_r_r, a_r_r)
on (5 < a_r_r)
) T1
union all
select d
from (
Select d
from t2
where (d = d)
) T2
) T2(e_l_r)
on (e_l_r > e_l)
) T1(e_l_l, e_l_r_l)
inner join (
Select c, b
from t2
where ((18 - d) > b)
) T2(c_r, b_r)
on (e_l_r_l > c_r)
) T2(e_l_l_r, e_l_r_l_r, c_r_r)
on (e_l_l_r = (96 - (d_l - (27 + 57))))
) T2(e_l_r, d_l_r, e_l_l_r_r)
on (((55 * e_l_l_r_r) - e_l_l_r_r) > (e_l_l_r_r + e_l_l_r_r))
) T1(e_l_l, e_l_l_r_r_l, e_l_r_l, d_l_r_l)
left join (
Select c, a, d
from t2
where (d = b)
) T2(c_r, a_r, d_r)
on (53 > (12 + 84))
) T1
union all
select d_l, a_r, d_r
from (
Select d_l, a_r, d_r
from (
Select c, b, d
from t1
where (d = 52)
) T1(c_l, b_l, d_l)
left join (
Select a, b, d
from t1
where (e = 38)
) T2(a_r, b_r, d_r)
on (a_r = 44)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c_l, e_r, c_r, d_r
from (
Select c_l, e_r, c_r, d_r
from (
Select e, c, b
from t3
where (a = (53 - a))
) T1(e_l, c_l, b_l)
left join (
select e, c, d
from (
Select e, c, d
from t2
where (d < 63)
) T1
union all
select c, a, d
from (
Select c, a, d
from t1
where (b = 64)
) T2
) T2(e_r, c_r, d_r)
on ((c_l * 46) = (78 + 86))
) T1
union all
select e_l_l_r_l, a_r_r_l, b_l_r, e_r_r
from (
Select e_l_l_r_l, a_r_r_l, b_l_r, e_r_r
from (
Select b_r_l, b_l_l_r, a_r_r, e_l_l_r
from (
select e_l_l, b_r
from (
Select e_l_l, b_r
from (
Select e_l, b_r, d_r
from (
Select e, c, a
from t3
where ((b + 38) < (c - 31))
) T1(e_l, c_l, a_l)
left join (
Select b, d
from t2
where (88 = b)
) T2(b_r, d_r)
on (b_r = d_r)
) T1(e_l_l, b_r_l, d_r_l)
left join (
Select e, a, b
from t4
where (c = (70 * 35))
) T2(e_r, a_r, b_r)
on (95 = e_l_l)
) T1
union all
select a_l, b_l
from (
Select a_l, b_l, e_r
from (
Select a, b
from t3
where (81 < 3)
) T1(a_l, b_l)
left join (
select e
from (
Select e, b, d
from t2
where (29 < e)
) T1
union all
select e
from (
Select e
from t5
where ((85 + (34 - c)) < (2 - 21))
) T2
) T2(e_r)
on (97 = 4)
) T2
) T1(e_l_l_l, b_r_l)
left join (
Select e_l_l, b_l_l, a_r
from (
Select e_l, b_l, d_r
from (
Select e, c, b
from t2
where (47 = c)
) T1(e_l, c_l, b_l)
left join (
Select a, b, d
from t3
where ((e + b) < ((b * 94) * d))
) T2(a_r, b_r, d_r)
on (83 < d_r)
) T1(e_l_l, b_l_l, d_r_l)
full join (
Select a
from t2
where (16 < (44 - b))
) T2(a_r)
on ((5 - a_r) > (a_r + a_r))
) T2(e_l_l_r, b_l_l_r, a_r_r)
on (59 > 54)
) T1(b_r_l_l, b_l_l_r_l, a_r_r_l, e_l_l_r_l)
full join (
Select b_l, e_r
from (
Select e, a, b
from t3
where (30 > e)
) T1(e_l, a_l, b_l)
left join (
Select e
from t2
where ((c + (d - 50)) = e)
) T2(e_r)
on (e_r = 73)
) T2(b_l_r, e_r_r)
on (a_r_r_l > 1)
) T2
order by 1, 2, 3, 4
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b
from t5
where (b = (a - (78 * 41)))
) T1
union all
select d_l_l, e_r_l
from (
Select d_l_l, e_r_l, c_l_r, a_r_r, d_l_r
from (
Select e_l, d_l, e_r
from (
Select e, a, d
from t2
where (c = 37)
) T1(e_l, a_l, d_l)
full join (
Select e
from t4
where (31 > 12)
) T2(e_r)
on (36 = 95)
) T1(e_l_l, d_l_l, e_r_l)
left join (
Select c_l, a_l, d_l, e_r, a_r
from (
Select c, a, b, d
from t1
where (b < e)
) T1(c_l, a_l, b_l, d_l)
inner join (
select e, a
from (
Select e, a
from t1
where (((a - e) + ((65 * 7) - b)) < 17)
) T1
union all
select e_l, a_r
from (
Select e_l, a_r
from (
Select e, a, d
from t2
where (b > 45)
) T1(e_l, a_l, d_l)
left join (
Select a
from t5
where ((c * 15) = 53)
) T2(a_r)
on (a_r > (87 + 12))
) T2
) T2(e_r, a_r)
on (32 < 76)
) T2(c_l_r, a_l_r, d_l_r, e_r_r, a_r_r)
on (e_r_l = 1)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (a > (c * 90))
) T1
union all
select e_l_l
from (
Select e_l_l, c_r_l, c_r, a_r
from (
Select e_l, c_r
from (
Select e, a, b, d
from t1
where (a < (c + 78))
) T1(e_l, a_l, b_l, d_l)
inner join (
Select c
from t1
where (c > 23)
) T2(c_r)
on (0 < c_r)
) T1(e_l_l, c_r_l)
left join (
Select c, a, b
from t4
where (b = 80)
) T2(c_r, a_r, b_r)
on (41 > 58)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t1
where (e > 83)
) T1
union all
select e_l
from (
Select e_l, b_r
from (
Select e, b
from t1
where (10 = a)
) T1(e_l, b_l)
inner join (
Select c, b
from t3
where (a = 17)
) T2(c_r, b_r)
on (e_l = 63)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b, d
from t5
where (75 > a)
) T1
union all
select a, d
from (
Select a, d
from t1
where (e = (9 - d))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t4
where (a = d)
) T1
union all
select d_l, e_l_r
from (
Select d_l, e_l_r
from (
Select d
from t5
where (c > 20)
) T1(d_l)
inner join (
select e_l
from (
Select e_l, d_r
from (
Select e, a
from t2
where (e = 41)
) T1(e_l, a_l)
full join (
Select c, d
from t2
where (80 = a)
) T2(c_r, d_r)
on (e_l > e_l)
) T1
union all
select c
from (
Select c
from t3
where (5 > (a * 15))
) T2
) T2(e_l_r)
on ((83 - 8) = d_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, d
from t3
where (69 < c)
) T1
union all
select c, a
from (
select c, a
from (
Select c, a, b
from t1
where ((e + d) = a)
) T1
union all
select c, d
from (
Select c, d
from t2
where (c < c)
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
    _dci.expect_file(output, defs.test_dir + """/Test10exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

