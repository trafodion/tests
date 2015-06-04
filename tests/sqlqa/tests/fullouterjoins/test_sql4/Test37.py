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
    
def test001(desc="""Joins Set 37"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select b
from (
Select b, d
from t5
where (a = 2)
) T1
union all
select a
from (
select a
from (
Select a
from t3
where ((21 * a) = 84)
) T1
union all
select d_l
from (
Select d_l, e_r
from (
Select d
from t4
where (44 > ((b * b) * 96))
) T1(d_l)
inner join (
Select e, a, b
from t2
where (33 = d)
) T2(e_r, a_r, b_r)
on (e_r < e_r)
) T2
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s1""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, a
from (
Select e, c, a, b
from t2
where (c < 10)
) T1
union all
select c, b, d
from (
Select c, b, d
from t1
where (38 > d)
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d
from (
Select d
from t3
where (78 < b)
) T1
union all
select c
from (
select c, b
from (
Select c, b
from t2
where (a = 54)
) T1
union all
select e, c
from (
Select e, c, b
from t1
where (65 = b)
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
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select d_l
from (
select d_l
from (
Select d_l, b_l_l_r, d_r_r
from (
Select b, d
from t1
where (c = c)
) T1(b_l, d_l)
inner join (
Select b_l_l, d_r
from (
select b_l
from (
select b_l
from (
Select b_l, b_r
from (
Select b, d
from t2
where ((a - 45) > 49)
) T1(b_l, d_l)
full join (
Select b
from t4
where ((13 - (32 + 77)) = 3)
) T2(b_r)
on (24 = b_l)
) T1
union all
select d
from (
Select d
from t2
where (12 = b)
) T2
) T1
union all
select c_l
from (
Select c_l, a_r
from (
Select c, d
from t4
where (47 = ((48 - 23) * (e * (45 + (3 - d)))))
) T1(c_l, d_l)
left join (
Select a
from t5
where (b = d)
) T2(a_r)
on ((c_l - 62) > a_r)
) T2
) T1(b_l_l)
inner join (
Select d
from t1
where ((30 * (b - b)) = d)
) T2(d_r)
on (81 < 94)
) T2(b_l_l_r, d_r_r)
on (b_l_l_r > 93)
) T1
union all
select e
from (
Select e
from t3
where (43 > 41)
) T2
) T1
union all
select a_l_l
from (
Select a_l_l, e_r, c_r
from (
Select a_l, b_r
from (
Select a
from t3
where (e = e)
) T1(a_l)
left join (
Select c, b, d
from t1
where (41 > a)
) T2(c_r, b_r, d_r)
on (b_r > (b_r + ((a_l * a_l) - 13)))
) T1(a_l_l, b_r_l)
inner join (
Select e, c
from t5
where ((e - 75) < ((d - 21) + ((((3 * a) * b) + a) + (1 - 53))))
) T2(e_r, c_r)
on ((c_r * 13) = a_l_l)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s4""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c, b
from (
select e, c, b
from (
Select e, c, b, d
from t2
where (b > c)
) T1
union all
select e, b, d
from (
Select e, b, d
from t5
where (b > b)
) T2
) T1
union all
select a, b, d
from (
Select a, b, d
from t1
where (74 = 7)
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
select b, d
from (
Select b, d
from t5
where (40 = 28)
) T1
union all
select e, a
from (
Select e, a, b
from t5
where (b > b)
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
from t2
where (b > 20)
) T1
union all
select c
from (
Select c
from t3
where (26 < 68)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t2
where (b = c)
) T1
union all
select e, a
from (
Select e, a, d
from t5
where (b = e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t4
where (d = c)
) T1
union all
select e, d
from (
Select e, d
from t1
where ((d + 27) < e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
select c
from (
Select c
from t5
where (62 = (12 * e))
) T1
union all
select c
from (
Select c, b, d
from t1
where (a = (d + 30))
) T2
) T1
union all
select c
from (
Select c
from t1
where (87 < c)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t3
where ((c + 18) < b)
) T1
union all
select a
from (
Select a
from t3
where (86 = (c - c))
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
select c, d
from (
Select c, d
from t1
where (a = a)
) T1
union all
select b_l, c_r
from (
Select b_l, c_r
from (
Select b
from t5
where (e = 49)
) T1(b_l)
inner join (
Select c, b
from t5
where (b = 39)
) T2(c_r, b_r)
on ((c_r - 37) > c_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a
from t2
where ((77 - (25 * d)) < (75 - c))
) T1
union all
select e_l
from (
Select e_l, b_r_r, e_l_r
from (
Select e, c, b
from t5
where (b = b)
) T1(e_l, c_l, b_l)
left join (
Select e_l, b_r
from (
Select e
from t4
where ((82 + 61) > a)
) T1(e_l)
left join (
Select e, b
from t3
where ((c - e) = 52)
) T2(e_r, b_r)
on (e_l < b_r)
) T2(e_l_r, b_r_r)
on (e_l_r < (b_r_r * 12))
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
select e, c
from (
select e, c
from (
Select e, c
from t3
where ((77 * 11) = c)
) T1
union all
select e, c
from (
Select e, c, b
from t3
where (b = a)
) T2
) T1
union all
select d_l, a_r
from (
Select d_l, a_r
from (
Select d
from t4
where (e = e)
) T1(d_l)
left join (
Select a
from t3
where (10 = a)
) T2(a_r)
on (76 = d_l)
) T2
) T1
union all
select e_l, d_l
from (
Select e_l, d_l, c_r
from (
Select e, d
from t4
where (55 < b)
) T1(e_l, d_l)
inner join (
select c
from (
Select c
from t4
where ((b + b) > (b * 25))
) T1
union all
select e
from (
select e, c, b
from (
Select e, c, b
from t2
where (0 = 17)
) T1
union all
select a_l_r_l, c_r, b_r
from (
Select a_l_r_l, c_r, b_r
from (
Select c_l_l, b_r_r_l, a_l_r, e_r_r
from (
Select c_l, d_l, b_r_r
from (
select c, d
from (
Select c, d
from t3
where (47 > b)
) T1
union all
select e, a
from (
Select e, a, d
from t2
where (a = (53 + 22))
) T2
) T1(c_l, d_l)
inner join (
Select d_l, b_r
from (
Select e, d
from t3
where (56 < 89)
) T1(e_l, d_l)
inner join (
Select e, c, a, b
from t2
where (c = e)
) T2(e_r, c_r, a_r, b_r)
on ((b_r * d_l) < (b_r * 54))
) T2(d_l_r, b_r_r)
on (b_r_r = c_l)
) T1(c_l_l, d_l_l, b_r_r_l)
left join (
Select a_l, d_l, e_r
from (
Select a, d
from t4
where (c = 40)
) T1(a_l, d_l)
full join (
Select e
from t5
where (40 < ((20 * d) * a))
) T2(e_r)
on (44 = d_l)
) T2(a_l_r, d_l_r, e_r_r)
on (b_r_r_l = (99 + a_l_r))
) T1(c_l_l_l, b_r_r_l_l, a_l_r_l, e_r_r_l)
left join (
Select c, b
from t3
where (b = 63)
) T2(c_r, b_r)
on (a_l_r_l < c_r)
) T2
) T2
) T2(c_r)
on (d_l < e_l)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b, d
from t2
where (80 = ((23 + a) * 68))
) T1
union all
select e, b
from (
Select e, b
from t2
where (e = e)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e
from t3
where (44 = e)
) T1
union all
select e
from (
Select e, a, d
from t4
where (a < 21)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s16""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, b_r_r
from (
Select e_l, b_r_r
from (
Select e
from t1
where (d > c)
) T1(e_l)
left join (
Select e_l, e_r, b_r
from (
Select e
from t4
where (78 = 6)
) T1(e_l)
left join (
Select e, b
from t2
where (93 > 19)
) T2(e_r, b_r)
on ((76 + e_r) < e_r)
) T2(e_l_r, e_r_r, b_r_r)
on (b_r_r = e_l)
) T1
union all
select d_l, d_r
from (
Select d_l, d_r
from (
Select d
from t4
where ((c + 20) = (c + 82))
) T1(d_l)
left join (
Select b, d
from t4
where (((b + d) + (45 + e)) < (d - (19 + ((b * 29) + a))))
) T2(b_r, d_r)
on (d_r < 66)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a, b
from (
Select e, a, b
from t3
where (84 = 70)
) T1
union all
select a, b, d
from (
Select a, b, d
from t4
where ((36 * d) < ((b * (((d * e) * e) - (d - 98))) * b))
) T2
order by 1, 2, 3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s18""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c
from t4
where (((d - (93 + b)) + b) = ((c - (63 + 85)) + d))
) T1
union all
select d
from (
Select d
from t3
where (d < b)
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
select c, d
from (
Select c, d
from t3
where (45 < (14 + 50))
) T1
union all
select e, c
from (
Select e, c, a
from t3
where (60 > (a * ((25 + ((b * (61 - 56)) - b)) + 44)))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test37exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************************
    _testmgr.testcase_end(desc)

