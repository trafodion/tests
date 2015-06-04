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
    
    stmt = """create table web_page
(
wp_web_page_sk            integer               not null,
wp_web_page_id            char(16)              not null,
wp_rec_start_date         date                          ,
wp_rec_end_date           date                          ,
wp_creation_date_sk       integer                       ,
wp_access_date_sk         integer                       ,
wp_autogen_flag           char(1)                       ,
wp_customer_sk            integer                       ,
wp_url                    varchar(100)                  ,
wp_type                   char(50)                      ,
wp_char_count             integer                       ,
wp_link_count             integer                       ,
wp_image_count            integer                       ,
wp_max_ad_count           integer                       ,
primary key (wp_web_page_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ no partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    
