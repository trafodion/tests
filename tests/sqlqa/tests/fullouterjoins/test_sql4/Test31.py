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
    
def test001(desc="""Joins Set 31"""):
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
from t3
where (30 = a)
) T1
union all
select e, c
from (
Select e, c, a, d
from t1
where ((d - c) > 23)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t5
where (((e + (73 * b)) * e) < (7 * 89))
) T1
union all
select e_r_l_l
from (
Select e_r_l_l, e_r
from (
Select e_r_l, c_r
from (
Select c_l_l, e_r
from (
select e_l, c_l
from (
Select e_l, c_l, a_r, d_r
from (
Select e, c
from t5
where (((97 - e) * e) > 99)
) T1(e_l, c_l)
inner join (
Select e, a, b, d
from t4
where (62 = e)
) T2(e_r, a_r, b_r, d_r)
on (92 > e_l)
) T1
union all
select e, d
from (
Select e, d
from t3
where (c > (c - 50))
) T2
) T1(e_l_l, c_l_l)
full join (
select e, a
from (
Select e, a
from t3
where (c < d)
) T1
union all
select c, a
from (
Select c, a
from t1
where (a = a)
) T2
) T2(e_r, a_r)
on (48 > (34 + 64))
) T1(c_l_l_l, e_r_l)
left join (
Select c, d
from t4
where ((12 - b) > (c + 65))
) T2(c_r, d_r)
on (e_r_l = 33)
) T1(e_r_l_l, c_r_l)
full join (
select e
from (
Select e, c, a
from t5
where (42 = 75)
) T1
union all
select a
from (
Select a
from t1
where (d < 74)
) T2
) T2(e_r)
on (88 < 11)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t4
where (((d * 57) - d) < 80)
) T1
union all
select e
from (
Select e, d
from t1
where (d < (33 * 16))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t4
where (21 = (87 - (d - b)))
) T1
union all
select e, c
from (
Select e, c, a
from t3
where ((84 - b) = 24)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b
from t1
where (12 = 79)
) T1
union all
select c
from (
Select c
from t1
where (c > b)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b_l, e_r
from (
Select b_l, e_r
from (
Select b
from t1
where ((31 + (96 + e)) = 95)
) T1(b_l)
full join (
Select e
from t5
where (((27 - (d * d)) + e) > 32)
) T2(e_r)
on (86 > (94 * (82 - b_l)))
) T1
union all
select c_l_l, e_r_l
from (
Select c_l_l, e_r_l, d_r
from (
Select c_l, e_r, d_r
from (
Select c
from t4
where (58 > 18)
) T1(c_l)
left join (
Select e, d
from t1
where (33 = 43)
) T2(e_r, d_r)
on (82 > 58)
) T1(c_l_l, e_r_l, d_r_l)
full join (
Select a, b, d
from t5
where (89 = (8 + d))
) T2(a_r, b_r, d_r)
on (78 = 58)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_r_l, c_r, b_r
from (
Select d_r_l, c_r, b_r
from (
Select c_r_l, d_l_l, b_r, d_r
from (
Select d_l, c_r
from (
Select d
from t3
where (d > ((81 + 92) + 45))
) T1(d_l)
left join (
Select c, d
from t2
where (((((d + c) * b) - 82) - c) = d)
) T2(c_r, d_r)
on (d_l = d_l)
) T1(d_l_l, c_r_l)
inner join (
Select b, d
from t2
where (39 < (26 * 76))
) T2(b_r, d_r)
on (b_r = 92)
) T1(c_r_l_l, d_l_l_l, b_r_l, d_r_l)
left join (
Select c, b, d
from t5
where ((c * 79) = e)
) T2(c_r, b_r, d_r)
on (c_r = (d_r_l * 98))
) T1
union all
select e, a, d
from (
Select e, a, d
from t5
where (19 < (79 + d))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a
from t4
where (b = 93)
) T1
union all
select d
from (
Select d
from t1
where (a = e)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b, d
from (
Select b, d
from t1
where (a < 14)
) T1
union all
select b, d
from (
Select b, d
from t5
where ((c + 9) < 15)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, a
from (
Select c, a, d
from t5
where (e < (93 * e))
) T1
union all
select c, a
from (
Select c, a
from t4
where (d = b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e
from (
select e
from (
Select e, c, a
from t2
where (73 = (25 - (c + d)))
) T1
union all
select c
from (
Select c
from t3
where (d < (73 - 14))
) T2
) T1
union all
select e
from (
Select e, b, d
from t1
where (e < (c - b))
) T2
) T1
union all
select a_l
from (
Select a_l, a_r
from (
Select e, a, d
from t5
where (62 = e)
) T1(e_l, a_l, d_l)
left join (
Select a
from t2
where ((44 + 66) < 55)
) T2(a_r)
on (a_r = ((8 - a_r) - (a_l - a_l)))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
select e, a
from (
Select e, a
from t1
where (9 = a)
) T1
union all
select c, b
from (
Select c, b
from t3
where (a = 25)
) T2
) T1
union all
select c
from (
Select c
from t4
where (84 = 25)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
select e, a
from (
select e, a
from (
Select e, a
from t4
where (40 = a)
) T1
union all
select b, d
from (
Select b, d
from t1
where (2 = c)
) T2
) T1
union all
select c, b
from (
Select c, b
from t3
where (25 = 48)
) T2
) T1
union all
select b, d
from (
Select b, d
from t3
where (57 = (c - 68))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, e_r, c_r
from (
Select e_l, e_r, c_r
from (
select e
from (
Select e, a, b
from t2
where (c < 39)
) T1
union all
select a
from (
Select a
from t2
where ((c + b) > (30 * 63))
) T2
) T1(e_l)
full join (
Select e, c
from t5
where (70 > 9)
) T2(e_r, c_r)
on (89 < ((((94 * 6) - 9) + c_r) * (e_r + c_r)))
) T1
union all
select e, b, d
from (
Select e, b, d
from t1
where (88 = (d + 63))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t5
where (e > 71)
) T1
union all
select b_l, c_r
from (
Select b_l, c_r, a_r
from (
Select a, b
from t4
where (d = ((c * a) * 50))
) T1(a_l, b_l)
left join (
Select c, a, b
from t2
where (b = 53)
) T2(c_r, a_r, b_r)
on (33 = 54)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, a_l, c_r
from (
Select e, a, b
from t1
where (52 < 4)
) T1(e_l, a_l, b_l)
left join (
select c
from (
Select c, d
from t4
where (15 = ((34 * 7) - e))
) T1
union all
select e
from (
select e
from (
Select e
from t3
where (e > e)
) T1
union all
select c_l_l
from (
Select c_l_l, e_r_l, a_r, b_r
from (
Select c_l, e_r
from (
Select c
from t1
where (d < 99)
) T1(c_l)
full join (
Select e
from t2
where (b < b)
) T2(e_r)
on (80 = e_r)
) T1(c_l_l, e_r_l)
left join (
Select a, b
from t4
where (e = c)
) T2(a_r, b_r)
on (b_r < 40)
) T2
) T2
) T2(c_r)
on (38 > (((e_l + e_l) + c_r) - 12))
) T1
union all
select d
from (
select d
from (
Select d
from t5
where (33 = 35)
) T1
union all
select b
from (
select b
from (
Select b
from t3
where (c > e)
) T1
union all
select e
from (
select e, a, b
from (
Select e, a, b
from t4
where (79 < (c - ((c + a) * (77 + 56))))
) T1
union all
select e, c, a
from (
Select e, c, a, d
from t2
where (e > 68)
) T2
) T2
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
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t2
where (c = d)
) T1
union all
select e
from (
Select e, a
from t1
where (e < (32 * b))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, d
from t5
where (b = 11)
) T1
union all
select c
from (
Select c
from t2
where (((d - (e - c)) * (76 + a)) < b)
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
select e_l_l, a_r_l
from (
Select e_l_l, a_r_l, e_r, b_r
from (
Select e_l, a_l, a_r
from (
Select e, a
from t3
where (e = a)
) T1(e_l, a_l)
full join (
Select a
from t2
where (a = 63)
) T2(a_r)
on (a_l = 68)
) T1(e_l_l, a_l_l, a_r_l)
full join (
Select e, b
from t4
where (e < 23)
) T2(e_r, b_r)
on (e_r > 69)
) T1
union all
select e, a
from (
Select e, a
from t5
where (d = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t3
where (d < 62)
) T1
union all
select b_l
from (
select b_l
from (
Select b_l, c_l_r, c_r_r
from (
Select e, b
from t4
where (60 < d)
) T1(e_l, b_l)
full join (
Select c_l, c_r, b_r
from (
Select c
from t1
where (40 > 70)
) T1(c_l)
inner join (
Select c, b
from t2
where (a = 12)
) T2(c_r, b_r)
on (b_r > 74)
) T2(c_l_r, c_r_r, b_r_r)
on (89 < 76)
) T1
union all
select e
from (
select e
from (
Select e, c, d
from t2
where (e < 39)
) T1
union all
select c
from (
Select c
from t4
where (65 = a)
) T2
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
    _dci.expect_file(output, defs.test_dir + """/Test31exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    _testmgr.testcase_end(desc)

