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
    
    stmt = """create table call_center
(
cc_call_center_sk         integer               not null,
cc_call_center_id         char(16)              not null,
cc_rec_start_date         date                          ,
cc_rec_end_date           date                          ,
cc_closed_date_sk         integer                       ,
cc_open_date_sk           integer                       ,
cc_name                   varchar(50)                   ,
cc_class                  varchar(50)                   ,
cc_employees              integer                       ,
cc_sq_ft                  integer                       ,
cc_hours                  char(20)                      ,
cc_manager                varchar(40)                   ,
cc_mkt_id                 integer                       ,
cc_mkt_class              char(50)                      ,
cc_mkt_desc               varchar(100)                  ,
cc_market_manager         varchar(40)                   ,
cc_division               integer                       ,
cc_division_name          varchar(50)                   ,
cc_company                integer                       ,
cc_company_name           char(50)                      ,
cc_street_number          char(10)                      ,
cc_street_name            varchar(60)                   ,
cc_street_type            char(15)                      ,
cc_suite_number           char(10)                      ,
cc_city                   varchar(60)                   ,
cc_county                 varchar(30)                   ,
cc_state                  char(2)                       ,
cc_zip                    char(10)                      ,
cc_country                varchar(20)                   ,
cc_gmt_offset             decimal(5,2)                  ,
cc_tax_percentage         decimal(5,2)                  ,
primary key (cc_call_center_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += ("""no partition attributes extent (256) maxextents 700;""")
    output = _dci.cmdexec(stmt)
