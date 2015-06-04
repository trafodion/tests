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

prepare xx from
select ee1.deptnum, copayment, substr(insname,1,12) as insname,insurance.num,
max(copayment) over (order by insurance.num,sum(copayment) asc, copayment, insname
rows between unbounded preceding and current row) as MaxCoPayment,
dense_rank() over (order by insurance.num,sum(copayment) asc, copayment, insname)
as DenseRank
from ee1, insurance
where ee1.num = insurance.num
and coverage > 2000
and ee1.deptnum NOT in (1,3)
group by insurance.num,ee1.deptnum, copayment, insname
order by insurance.num;

infostats xx;

execute xx;

get statistics for qid current;

exit