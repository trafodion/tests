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
select e, c, d
from (
Select e, c, d
from t5
where ((d - ((c + 75) * (31 - 40))) = a)
) T1
union all
select e, a, d
from (
Select e, a, d
from t5
where (65 < 46)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
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
Select e, c
from t3
where ((24 + b) = 84)
) T1
union all
select c_l_l, b_l_l
from (
Select c_l_l, b_l_l, b_r
from (
Select c_l, b_l, e_r, c_r
from (
Select c, b
from t5
where (4 = 6)
) T1(c_l, b_l)
left join (
Select e, c, b
from t3
where (73 < ((b + a) + 63))
) T2(e_r, c_r, b_r)
on (52 = 54)
) T1(c_l_l, b_l_l, e_r_l, c_r_l)
left join (
Select c, b, d
from t5
where (19 = (47 + 0))
) T2(c_r, b_r, d_r)
on (19 = b_l_l)
) T2
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
select a_l_l, d_r_l, d_l_l
from (
Select a_l_l, d_r_l, d_l_l, a_l_r, a_r_r
from (
Select a_l, d_l, c_r, d_r
from (
Select e, a, d
from t3
where (a > 50)
) T1(e_l, a_l, d_l)
left join (
Select c, a, d
from t2
where (c < (0 + d))
) T2(c_r, a_r, d_r)
on (a_l < d_r)
) T1(a_l_l, d_l_l, c_r_l, d_r_l)
left join (
Select a_l, a_r, b_r
from (
Select a, d
from t2
where (a = (65 + c))
) T1(a_l, d_l)
left join (
Select a, b
from t1
where ((68 - ((87 * 38) * (85 + (b + ((d + 48) + 76))))) = 5)
) T2(a_r, b_r)
on (23 = 81)
) T2(a_l_r, a_r_r, b_r_r)
on (91 < 93)
) T1
union all
select c, a, d
from (
Select c, a, d
from t3
where (58 > 6)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t4
where ((d + ((72 + d) - 11)) < 42)
) T1
union all
select b_r_l
from (
select b_r_l, d_l_l
from (
Select b_r_l, d_l_l, d_r
from (
Select d_l, b_r
from (
Select e, d
from t5
where (72 < a)
) T1(e_l, d_l)
left join (
Select a, b
from t3
where (51 > (83 - c))
) T2(a_r, b_r)
on (b_r = b_r)
) T1(d_l_l, b_r_l)
full join (
Select d
from t4
where (c > 1)
) T2(d_r)
on (d_l_l < d_l_l)
) T1
union all
select d_l, c_r
from (
Select d_l, c_r
from (
Select d
from t1
where (c = d)
) T1(d_l)
left join (
Select c
from t4
where ((16 + (d * (d - 68))) > e)
) T2(c_r)
on ((d_l * 10) < d_l)
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
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l, e_r
from (
Select d_l, e_r
from (
select d
from (
Select d
from t3
where (d < (51 * a))
) T1
union all
select d_l
from (
Select d_l, e_l_r, d_r_r
from (
Select d
from t5
where (e = 80)
) T1(d_l)
left join (
Select e_l, c_l, d_r
from (
Select e, c
from t3
where (24 = 75)
) T1(e_l, c_l)
full join (
Select c, a, d
from t3
where (21 < 95)
) T2(c_r, a_r, d_r)
on (49 = 7)
) T2(e_l_r, c_l_r, d_r_r)
on (11 > d_l)
) T2
) T1(d_l)
left join (
select e
from (
Select e
from t3
where (a = b)
) T1
union all
select e
from (
Select e, b
from t3
where (b = 1)
) T2
) T2(e_r)
on (51 = 79)
) T1
union all
select e_l, c_l
from (
Select e_l, c_l, a_l, e_l_r
from (
Select e, c, a
from t4
where (85 > 36)
) T1(e_l, c_l, a_l)
full join (
Select e_l, e_l_l_r
from (
select e
from (
Select e, a, d
from t3
where (a > d)
) T1
union all
select b
from (
Select b
from t5
where (((13 + (49 * 43)) - 93) = b)
) T2
) T1(e_l)
left join (
Select e_l_l, e_r_l, d_r_r, a_r_r, b_l_r
from (
Select e_l, e_r, c_r
from (
Select e
from t2
where (47 > (67 * (87 - c)))
) T1(e_l)
full join (
Select e, c
from t2
where (((e - c) * d) = 33)
) T2(e_r, c_r)
on ((7 + 32) > 46)
) T1(e_l_l, e_r_l, c_r_l)
left join (
Select b_l, d_l, a_r, d_r
from (
Select b, d
from t5
where (40 > c)
) T1(b_l, d_l)
inner join (
Select a, b, d
from t3
where (67 = 0)
) T2(a_r, b_r, d_r)
on (29 > 86)
) T2(b_l_r, d_l_r, a_r_r, d_r_r)
on (a_r_r < d_r_r)
) T2(e_l_l_r, e_r_l_r, d_r_r_r, a_r_r_r, b_l_r_r)
on (38 = e_l)
) T2(e_l_r, e_l_l_r_r)
on (97 < a_l)
) T2
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
select e, b
from (
Select e, b
from t5
where (e = c)
) T1
union all
select b_l, d_l
from (
Select b_l, d_l, e_r, c_r
from (
Select e, b, d
from t2
where ((72 + 94) < 9)
) T1(e_l, b_l, d_l)
full join (
Select e, c
from t3
where (20 < d)
) T2(e_r, c_r)
on ((c_r - (c_r + (b_l - 30))) < (d_l + 79))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_l, c_r
from (
Select e_l, b_l, c_r
from (
Select e, b
from t5
where (82 < a)
) T1(e_l, b_l)
left join (
Select e, c
from t3
where (c = 33)
) T2(e_r, c_r)
on (73 > (e_l - 36))
) T1
union all
select c_l, a_l, c_r
from (
select c_l, a_l, c_r
from (
Select c_l, a_l, c_r
from (
Select c, a
from t1
where (b = 0)
) T1(c_l, a_l)
inner join (
Select c, b
from t3
where ((c * 95) = e)
) T2(c_r, b_r)
on (c_r > c_l)
) T1
union all
select a_l, b_r_r, b_l_r
from (
Select a_l, b_r_r, b_l_r
from (
Select a
from t5
where (((a * (61 - 14)) * c) = 87)
) T1(a_l)
inner join (
Select b_l, b_r
from (
Select b
from t2
where (b = e)
) T1(b_l)
left join (
Select b
from t5
where (b = 95)
) T2(b_r)
on (85 < 72)
) T2(b_l_r, b_r_r)
on (82 > 53)
) T2
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, a_l_l_r_r
from (
Select b_l, a_l_l_r_r
from (
Select c, b
from t3
where (b < 32)
) T1(c_l, b_l)
left join (
Select b_l, a_l_l_r
from (
Select b, d
from t1
where (72 > 89)
) T1(b_l, d_l)
inner join (
Select a_l_l, c_r, d_r
from (
Select a_l, b_l, e_r, b_r
from (
Select a, b
from t5
where (e < 37)
) T1(a_l, b_l)
left join (
Select e, c, a, b
from t1
where (56 = 48)
) T2(e_r, c_r, a_r, b_r)
on (b_l = 74)
) T1(a_l_l, b_l_l, e_r_l, b_r_l)
left join (
Select c, d
from t1
where ((77 + 21) > 66)
) T2(c_r, d_r)
on (c_r = (c_r * (98 * 23)))
) T2(a_l_l_r, c_r_r, d_r_r)
on (21 = 35)
) T2(b_l_r, a_l_l_r_r)
on ((17 - 78) = (41 - a_l_l_r_r))
) T1
union all
select c_l, d_l
from (
Select c_l, d_l, d_r
from (
Select e, c, d
from t1
where ((80 + ((18 * (d - d)) * (e + 82))) = 96)
) T1(e_l, c_l, d_l)
full join (
Select c, b, d
from t3
where ((d * d) > b)
) T2(c_r, b_r, d_r)
on (d_l = d_l)
) T2
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
select a, d
from (
Select a, d
from t4
where (c > 22)
) T1
union all
select e, b
from (
Select e, b
from t4
where (e = a)
) T2
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
select e, c, b
from (
Select e, c, b
from t3
where (84 > 68)
) T1
union all
select b_l, e_r, c_r
from (
Select b_l, e_r, c_r
from (
Select b
from t5
where (d < b)
) T1(b_l)
left join (
Select e, c
from t4
where (b > 42)
) T2(e_r, c_r)
on (44 = (59 * (8 - b_l)))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a, b
from (
Select a, b, d
from t3
where (84 = ((c + 95) * 16))
) T1
union all
select e, a
from (
Select e, a
from t2
where (17 < d)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t1
where (b = (e + 39))
) T1
union all
select b_l
from (
select b_l, d_r
from (
Select b_l, d_r
from (
Select b
from t4
where (d = d)
) T1(b_l)
inner join (
Select a, d
from t1
where (b > b)
) T2(a_r, d_r)
on (90 < 67)
) T1
union all
select b_l, b_l_l_r
from (
Select b_l, b_l_l_r, b_r_l_r, c_r_r, d_r_l_r
from (
Select b
from t4
where (14 = c)
) T1(b_l)
inner join (
Select b_r_l, d_r_l, b_l_l, c_r
from (
Select b_l, d_l, c_r, b_r, d_r
from (
Select b, d
from t2
where (e < e)
) T1(b_l, d_l)
full join (
Select c, b, d
from t3
where ((1 + 55) < 38)
) T2(c_r, b_r, d_r)
on (b_l = 47)
) T1(b_l_l, d_l_l, c_r_l, b_r_l, d_r_l)
left join (
Select c
from t1
where (11 < (e - 20))
) T2(c_r)
on (79 = (1 - 87))
) T2(b_r_l_r, d_r_l_r, b_l_l_r, c_r_r)
on ((b_r_l_r + (b_l_l_r - 8)) = (89 + d_r_l_r))
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
    _dci.expect_selected_msg(output, 0)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t5
where (c = b)
) T1
union all
select a
from (
Select a, d
from t2
where (c = (a * 26))
) T2
order by 1
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
select e, b
from (
Select e, b
from t1
where (35 = b)
) T1
union all
select e, b
from (
Select e, b, d
from t2
where (51 < 14)
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
select b
from (
Select b
from t5
where (46 > e)
) T1
union all
select c
from (
Select c, a
from t4
where (((b - 90) * b) > (((53 - (c - (98 * c))) - 42) - e))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a_l
from (
Select a_l, d_l, b_r
from (
Select c, a, d
from t3
where (76 < e)
) T1(c_l, a_l, d_l)
left join (
select b
from (
Select b
from t2
where (90 < 63)
) T1
union all
select a
from (
Select a
from t2
where (d = 25)
) T2
) T2(b_r)
on (b_r = 27)
) T1
union all
select d
from (
Select d
from t3
where ((c - (13 - c)) = 13)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, d_l, d_r_l_r
from (
Select b_l, d_l, d_r_l_r
from (
Select a, b, d
from t3
where (b < 99)
) T1(a_l, b_l, d_l)
left join (
Select d_r_l, d_l_l, a_r
from (
Select d_l, d_r
from (
Select d
from t4
where (c < (53 - (32 + 58)))
) T1(d_l)
inner join (
Select a, d
from t2
where (41 = e)
) T2(a_r, d_r)
on (71 > (62 * d_r))
) T1(d_l_l, d_r_l)
full join (
Select a
from t2
where (c < 27)
) T2(a_r)
on (31 = d_l_l)
) T2(d_r_l_r, d_l_l_r, a_r_r)
on ((d_l - 26) = d_r_l_r)
) T1
union all
select e, a, b
from (
Select e, a, b
from t2
where ((80 - 9) = d)
) T2
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
select c, d
from (
Select c, d
from t1
where (b = c)
) T1
union all
select b_l, a_r
from (
Select b_l, a_r
from (
Select e, b
from t4
where ((69 * d) = (d + 29))
) T1(e_l, b_l)
full join (
Select a, b
from t2
where (68 < 23)
) T2(a_r, b_r)
on (b_l > ((a_r * 58) + (a_r - 20)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test23exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c, d
from t4
where (91 < c)
) T1
union all
select a, d
from (
Select a, d
from t1
where (b = 58)
) T2
order by 1, 2
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
select c, d
from (
Select c, d
from t4
where (e < 98)
) T1
union all
select a_l, d_r
from (
Select a_l, d_r
from (
Select a
from t2
where (46 = 8)
) T1(a_l)
left join (
Select e, a, d
from t5
where (d = b)
) T2(e_r, a_r, d_r)
on ((42 + d_r) = 0)
) T2
order by 1, 2
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
    _testmgr.testcase_end(desc)

