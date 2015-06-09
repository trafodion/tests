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

?section drop_table
----------------------------------------------------------------------------------
set schema a28schema1;
drop table a28tab_up cascade;
drop table a28tab_me cascade;
drop table a28tab_cas cascade;
drop table a28tab_load1 cascade;
drop table a28tab_load2 cascade;
drop table a28tab_index cascade;
drop schema a28schema1 cascade;
