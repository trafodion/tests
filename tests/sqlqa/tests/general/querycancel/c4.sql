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
drop volatile table vf00 cascade;

create volatile table vf00(
        colkey int not null,
        colint int not null,
        --   coldate date,
        colnum numeric(11,3),
        colchariso char(11) character set iso88591 not null,
        colcharucs2 char(11) character set ucs2 not null,
        colintn int,
        --   colts timestamp,
        colcharison char(13) character set iso88591,
        colcharucs2n char(13) character set ucs2,
        primary key(colint, colchariso, colcharucs2, colkey)
        );
upsert using load into vf00 select
        c1+c2*10+c3*100+c4*1000+c5*10000, --colkey
        c1+c2*10+c3*100+c4*1000+c5*10000, --colint
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as numeric(11,3)), --colnum
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(11) character set iso88591), --colchariso
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(11) character set ucs2), --colcharucs2
        c1+c2*10+c3*100+c4*1000+c5*10000, --colintn
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(13) character set iso88591), --colvchriso
        cast(c1+c2*10+c3*100+c4*1000+c5*10000 as char(13) character set ucs2) --colvchrucs2
        from (values(1)) t
        transpose 0,1,2,3,4,5,6,7,8,9 as c1
        transpose 0,1,2,3,4,5,6,7,8,9 as c2
        transpose 0,1,2,3,4,5,6,7,8,9 as c3
        transpose 0,1,2,3,4,5,6,7,8,9 as c4
        transpose 0,1,2,3,4,5,6,7,8,9 as c5
        ;

prepare xx from select [first 10] * from vf00 order by colchariso desc;

infostats xx;

execute xx;

get statistics for qid current;

exit