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
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table store
(
s_store_sk                integer               not null,
s_store_id                char(16)              not null,
s_rec_start_date          date                          ,
s_rec_end_date            date                          ,
s_closed_date_sk          integer                       ,
s_store_name              varchar(50)                   ,
s_number_employees        integer                       ,
s_floor_space             integer                       ,
s_hours                   char(20)                      ,
s_manager                 varchar(40)                   ,
s_market_id               integer                       ,
s_geography_class         varchar(100)                  ,
s_market_desc             varchar(100)                  ,
s_market_manager          varchar(40)                   ,
s_division_id             integer                       ,
s_division_name           varchar(50)                   ,
s_company_id              integer                       ,
s_company_name            varchar(50)                   ,
s_street_number           varchar(10)                   ,
s_street_name             varchar(60)                   ,
s_street_type             char(15)                      ,
s_suite_number            char(10)                      ,
s_city                    varchar(60)                   ,
s_county                  varchar(30)                   ,
s_state                   char(2)                       ,
s_zip                     char(10)                      ,
s_country                 varchar(20)                   ,
s_gmt_offset              decimal(5,2)                  ,
s_tax_precentage          decimal(5,2)                  ,
primary key (s_store_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ no partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    
