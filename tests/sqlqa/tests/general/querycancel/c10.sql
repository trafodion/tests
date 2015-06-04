-- @@@ START COPYRIGHT @@@
--
-- (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
--
--  Licensed under the Apache License, Version 2.0 (the "License");
--  you may not use this file except in compliance with the License.
--  You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
--  Unless required by applicable law or agreed to in writing, software
--  distributed under the License is distributed on an "AS IS" BASIS,
--  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--  See the License for the specific language governing permissions and
--  limitations under the License.
--
-- @@@ END COPYRIGHT @@@
control query default CANCEL_MINIMUM_BLOCKING_INTERVAL '1';

set schema TEST_SCHEMA_1;

create table t1 (a int, b int, c int, d int, e int) no partitions attribute extent (128);
create table t2 (a int, b int, c int, d int, e int) no partitions attribute extent (128);
create table t3 (a int, b int, c int, d int, e int) no partitions attribute extent (128);
create table t4 (a int, b int, c int, d int, e int) no partitions attribute extent (128);
create table t5 (a int, b int, c int, d int, e int) no partitions attribute extent (128);

upsert using load into t1
select x1 + 10*x2 + 100*x3 + 1000*x4 + 10000*x5,
       2*(x1 + 10*x2 + 100*x3 + 1000*x4 + 10000*x5),
       3*(x1 + 10*x2 + 100*x3 + 1000*x4 + 10000*x5),
       4*(x1 + 10*x2 + 100*x3 + 1000*x4 + 10000*x5),
       5*(x1 + 10*x2 + 100*x3 + 1000*x4 + 10000*x5)
from (values(0)) T
transpose 0,1,2,3,4,5,6,7,8,9 as x1
transpose 0,1,2,3,4,5,6,7,8,9 as x2
transpose 0,1,2,3,4,5,6,7,8,9 as x3
transpose 0,1,2,3,4,5,6,7,8,9 as x4
transpose 0,1,2,3,4,5,6,7,8,9 as x5;

upsert using load into t2 select * from t1;
upsert using load into t3 select * from t1;
upsert using load into t4 select * from t1;
upsert using load into t5 select * from t1;

prepare xx from
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
;

infostats xx;

execute xx;

get statistics for qid current;

drop table t1 cascade;
drop table t2 cascade;
drop table t3 cascade;
drop table t4 cascade;
drop table t5 cascade;

exit

