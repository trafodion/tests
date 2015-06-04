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
drop view v2_sqlc cascade;

create view 
           v2_sqlc 
           as 
           select
        lineitem.L_ORDERKEY,                     
        lineitem.L_PARTKEY,                        
        lineitem.L_SUPPKEY,                        
        lineitem.L_LINENUMBER,                  
        orders.O_ORDERKEY,                       
        orders.O_CUSTKEY,                        
        orders.O_ORDERSTATUS,
        orders.O_TOTALPRICE,                     
        customer.C_CUSTKEY,                        
        customer.C_NAME,   
    customer. C_ADDRESS
    from
    lineitem,
    orders,
    customer
    where 
    l_orderkey = o_orderkey
    and
    o_custkey = c_custkey
    and
    o_orderdate BETWEEN  DATE '1995-01-01' AND  DATE '2010-12-31'
    ;

prepare xx from select [first 1] * from v2_sqlc order by L_ORDERKEY desc;

infostats xx;

execute xx;

get statistics for qid current;

drop view v2_sqlc cascade;
exit
