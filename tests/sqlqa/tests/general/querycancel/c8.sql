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

set schema TEST_SCHEMA_2;


Prepare xx  from
select  l_returnflag,
    l_linestatus,
      cast(sum(l_quantity)                                   as numeric(18,2)) as sum_qty,
      cast(sum(l_extendedprice)                              as numeric(18,2)) as sum_base_price,
      cast(sum(l_extendedprice * (1 - l_discount))           as numeric(18,2)) as sum_disc_price,
      cast(sum(l_extendedprice * (1 - l_discount)*(1+l_tax)) as numeric(18,2)) as sum_charge,
      cast(avg(l_quantity)                                   as numeric(18,3)) as avg_qty,
      cast(avg(l_extendedprice)                              as numeric(18,3)) as avg_price,
      cast(avg(l_discount)                                   as numeric(18,3)) as avg_disc,
        count(*) as count_order
from
    lineitem
where
    l_shipdate <= date '1998-12-01' - interval '69' day (3)
group by
    l_returnflag,
    l_linestatus;

infostats xx;

execute xx;

get statistics for qid current;

exit