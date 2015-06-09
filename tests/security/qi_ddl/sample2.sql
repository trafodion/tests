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

?section table_operation1
----------------------------------------------------------------------------------
set schema a28schema1;
upsert into a28tab_up values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);
merge into a28tab_me on c1= 0 when not matched then insert values(10,20),(11,21),(12,22);
create table a28tab_cas2 as select * from a28tab_cas;
load into a28tab_load2 select * a28tab_load1;
populate index a28index;
