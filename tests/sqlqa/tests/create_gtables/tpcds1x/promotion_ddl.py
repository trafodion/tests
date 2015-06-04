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
    
    stmt = """create table promotion
(
p_promo_sk                integer               not null,
p_promo_id                char(16)              not null,
p_start_date_sk           integer                       ,
p_end_date_sk             integer                       ,
p_item_sk                 integer                       ,
p_cost                    decimal(15,2)                 ,
p_response_target         integer                       ,
p_promo_name              char(50)                      ,
p_channel_dmail           char(1)                       ,
p_channel_email           char(1)                       ,
p_channel_catalog         char(1)                       ,
p_channel_tv              char(1)                       ,
p_channel_radio           char(1)                       ,
p_channel_press           char(1)                       ,
p_channel_event           char(1)                       ,
p_channel_demo            char(1)                       ,
p_channel_details         varchar(100)                  ,
p_purpose                 char(15)                      ,
p_discount_active         char(1)                       ,
primary key (p_promo_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ no partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    
