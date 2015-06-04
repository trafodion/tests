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
    
def test001(desc="""Joins Set 29"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #****************************************
    stmt = """cqd attempt_esp_parallelism 'off';"""
    output = _dci.cmdexec(stmt)
    stmt = """prepare s1 from
select c, b
from (
Select c, b
from t1
where (b = (b + 69))
) T1
union all
select e_l, d_l
from (
Select e_l, d_l, b_r
from (
Select e, d
from t1
where (d = (12 * (67 - 28)))
) T1(e_l, d_l)
left join (
select b
from (
Select b
from t4
where (e = e)
) T1
union all
select e
from (
Select e, a, b
from t5
where (e < b)
) T2
) T2(b_r)
on (15 = 85)
) T2
order by 1, 2
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
select b
from (
Select b
from t2
where (58 > 64)
) T1
union all
select e
from (
select e, a
from (
Select e, a
from t1
where (d > d)
) T1
union all
select a, d
from (
Select a, d
from t1
where (a < 39)
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
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s2""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select a
from (
Select a, b
from t4
where (c = 87)
) T1
union all
select d
from (
select d
from (
Select d
from t2
where (b = (a - 41))
) T1
union all
select e
from (
Select e, a
from t3
where (c < (a * (d + 69)))
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
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s3""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select b
from (
Select b
from t2
where ((98 * 6) > ((29 * (66 * 77)) * 76))
) T1
union all
select e
from (
Select e, c
from t3
where ((32 * 77) < ((59 - (c + 99)) * 29))
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
Select e, c, b, d
from t4
where (96 > c)
) T1
union all
select c, b
from (
Select c, b
from t4
where (b = b)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s5""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t5
where (90 > 60)
) T1
union all
select e, a
from (
Select e, a, d
from t4
where (e > a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s6""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l
from (
Select e_l, c_r
from (
Select e, c
from t2
where ((28 - e) = (a * a))
) T1(e_l, c_l)
inner join (
Select e, c, b
from t3
where (a = (e * e))
) T2(e_r, c_r, b_r)
on (57 = 71)
) T1
union all
select b
from (
Select b
from t3
where (28 < 35)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s7""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, c, b, d
from t1
where (77 < b)
) T1
union all
select a
from (
Select a
from t2
where (((86 - 39) - 25) > 52)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s8""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c, d
from (
Select c, d
from t3
where ((47 + 32) = (38 - a))
) T1
union all
select e, a
from (
Select e, a, b, d
from t2
where (90 = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s9""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b, d
from t4
where (20 = (4 + 44))
) T1
union all
select b, d
from (
Select b, d
from t2
where (22 < a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s10""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e_l, c_l
from (
Select e_l, c_l, b_r
from (
select e, c
from (
Select e, c, a, b
from t5
where (86 = 87)
) T1
union all
select b_l, d_l_r
from (
Select b_l, d_l_r
from (
Select e, c, b
from t3
where (c < 40)
) T1(e_l, c_l, b_l)
left join (
Select c_l, d_l, a_r, b_r
from (
Select e, c, d
from t5
where ((b * b) = d)
) T1(e_l, c_l, d_l)
left join (
Select a, b, d
from t2
where ((d - (d - b)) < a)
) T2(a_r, b_r, d_r)
on (c_l = 51)
) T2(c_l_r, d_l_r, a_r_r, b_r_r)
on (32 < 33)
) T2
) T1(e_l, c_l)
left join (
Select b
from t5
where (d = c)
) T2(b_r)
on (((b_r * 47) + (80 * e_l)) = c_l)
) T1
union all
select b, d
from (
Select b, d
from t4
where (3 > (79 * 24))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s11""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t5
where (b = 38)
) T1
union all
select c, a
from (
Select c, a, b
from t4
where (44 = c)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s12""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, b
from (
Select e, b, d
from t3
where (d = b)
) T1
union all
select e, c
from (
Select e, c
from t5
where ((30 * (26 * 44)) > ((a * 86) - 45))
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s13""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, a
from (
Select e, a
from t1
where (((e - 85) - b) > b)
) T1
union all
select b_l, e_r
from (
Select b_l, e_r, c_r
from (
Select b
from t5
where (e = e)
) T1(b_l)
left join (
select e, c
from (
select e, c, a
from (
Select e, c, a
from t1
where (e > 0)
) T1
union all
select c_l, c_r, b_r
from (
Select c_l, c_r, b_r
from (
Select e, c, a
from t2
where (c = d)
) T1(e_l, c_l, a_l)
full join (
Select c, b
from t1
where ((c * 15) = 4)
) T2(c_r, b_r)
on (74 > c_r)
) T2
) T1
union all
select b, d
from (
Select b, d
from t5
where (20 = b)
) T2
) T2(e_r, c_r)
on ((8 * ((14 + e_r) + ((9 + e_r) * ((91 + b_l) + 28)))) = e_r)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s14""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e, c
from (
Select e, c
from t2
where (43 < (66 - 70))
) T1
union all
select a, b
from (
Select a, b
from t3
where (74 = a)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s15""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c, d
from t5
where (55 = c)
) T1
union all
select e
from (
Select e
from t2
where (43 > (15 * 44))
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
select a_l_l, a_r
from (
Select a_l_l, a_r
from (
Select a_l, d_r_l_r
from (
Select a
from t3
where (a = b)
) T1(a_l)
full join (
Select d_r_l, a_r, b_r
from (
Select c_l, b_l, c_r, d_r
from (
Select c, b
from t3
where ((55 + 78) < 1)
) T1(c_l, b_l)
left join (
Select c, b, d
from t2
where (5 = 16)
) T2(c_r, b_r, d_r)
on (c_r = 48)
) T1(c_l_l, b_l_l, c_r_l, d_r_l)
left join (
Select c, a, b
from t2
where ((77 - e) = 97)
) T2(c_r, a_r, b_r)
on (92 = ((d_r_l - 87) - a_r))
) T2(d_r_l_r, a_r_r, b_r_r)
on ((a_l + d_r_l_r) = 12)
) T1(a_l_l, d_r_l_r_l)
left join (
Select a
from t4
where (d = d)
) T2(a_r)
on (26 = (a_l_l * 61))
) T1
union all
select c, b
from (
Select c, b
from t1
where (51 = 9)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s17""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select c
from (
Select c
from t1
where (73 = b)
) T1
union all
select d
from (
Select d
from t5
where (c < c)
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
Select a, b, d
from t4
where ((12 * (23 + (12 - e))) > (e + a))
) T1
union all
select d_l, a_r
from (
Select d_l, a_r
from (
Select d
from t2
where (a > (b + c))
) T1(d_l)
inner join (
Select a, b
from t5
where ((20 * 8) = d)
) T2(a_r, b_r)
on ((72 - 90) < 12)
) T2
order by 1, 2
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s19""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare s1 from
select e
from (
Select e, a, d
from t5
where ((58 * e) < 78)
) T1
union all
select a
from (
Select a
from t1
where (77 = d)
) T2
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """explain options 'f' s1;"""
    output = _dci.cmdexec(stmt)
    stmt = """execute s1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/Test29exp""", """a1s20""")
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    #**********************************************
    _testmgr.testcase_end(desc)

