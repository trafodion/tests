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
   CREATE UNIQUE INDEX LORDERLINEX_q2p ON f32_lineitem
       (
         L_ORDERKEY ASC,
          L_PARTKEY ASC,  L_SUPPKEY ASC , L_LINENUMBER ASC, L_QUANTITY ASC
       )
       populate
       ATTRIBUTES EXTENT (10000, 10000), MAXEXTENTS 500
       HASH2 PARTITION BY (L_ORDERKEY);

infostats xx;

execute xx;

get statistics for qid current;

exit
