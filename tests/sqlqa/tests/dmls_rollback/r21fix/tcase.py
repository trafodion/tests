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
from ...lib import gvars
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
    
def test001(desc="""t02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Now that row counts in operators partition_access and tuple_flow
    #   in ESP are propagated properly.
    
    stmt = """control query default * reset;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default ATTEMPT_ESP_PARALLELISM 'ON';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Contracts (
Player_Id int not null,  -- 217
Update_Date date,  -- date
Joined_Club date,  -- date '2001-01-01'
Club_Id int,       -- 1500000040
Left_Club int,     -- NULL
Squad_Id int,
Squad_Stat_Id int,
Wage int,          -- 75
Contract_Type char(1),   -- 'P'
On_Loan char(1),   -- 'N'
Contract_End    date,    -- date '2006-06-30'
Minimum_Fee     int,     -- 0
Relegation_Fee  int,     -- 0
Non_Promo_Fee   int,     -- 0
Trans_Stat_Id   int,
Sale_Value      int,     -- 6
Per_Squad_Stat  int,
Happiness       int,     -- 45
Squad_Rep       int      -- 491
) store by (Player_Id);"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl contracts;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Application_Control (
Application_Id char(10) not null,
Last_Update date) store by (Application_Id);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Squad  (
Squad_Id int not null,
Squad_Name char(15)) store by (Squad_Id);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Squad_Status   (
Status_Id int not null,
Status_Name char(15)) store by (Status_Id);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Transfer_Status   (
Trans_Stat_Id int not null,
Status_Name char(20)) store by (Trans_Stat_Id);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from Application_Control;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from Contracts;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from Squad;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from Squad_Status;"""
    output = _dci.cmdexec(stmt)
    stmt = """delete from Transfer_Status;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Application_Control values ('SoccerV10',date '2004-11-01');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into Application_Control values ('SoccerV11',date '2004-11-01');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Application_Control values ('SoccerV12',date '2004-11-01');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Application_Control values ('SoccerV13',date '2004-11-01');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Application_Control values ('SoccerV14',date '2004-11-01');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Squad values (1, 'First Team');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad values (2, 'second Team');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad values (3, 'third Team');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad values (4, 'fourth Team');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad values (5, 'fifth Team');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad values (6, 'sixth Team');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad values (7, 'seventh Team');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Squad_Status  values (3, 'Hot Prospect');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad_Status  values (2, 'mid Prospect');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Squad_Status  values (1, 'Low Prospect');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Transfer_Status  values (1, 'Listed For Loan');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Transfer_Status  values (2, 'Listed For Life');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Transfer_Status  values (3, 'Listed For Save');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Transfer_Status  values (4, 'Listed For Keep');"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into Transfer_Status  values (5, 'Listed For Sell');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """prepare ins1 from
INSERT INTO Contracts (Player_Id, Update_Date,
Joined_Club, Club_Id, Left_Club, Squad_Id,
Squad_Stat_Id, Wage, Contract_Type, On_Loan,
Contract_End, Minimum_Fee,Relegation_Fee,
Non_Promo_Fee, Trans_Stat_Id, Sale_Value,
Per_Squad_Stat, Happiness, Squad_Rep)
VALUES
(215, (SELECT Last_Update FROM Application_Control
WHERE Application_Id = 'SoccerV10'), DATE '2000-01-01',
1500000015, NULL,
(SELECT Squad_Id FROM Squad
WHERE Squad_Name = 'First Team'),
(SELECT Status_Id FROM Squad_Status
WHERE Status_Name = 'Hot Prospect'),
25, 'P', 'N', DATE '2006-06-30', 0, 0, 0,
(SELECT Trans_Stat_Id FROM Transfer_Status
WHERE Status_Name = 'Listed For Loan'), 5,
(SELECT Status_Id FROM Squad_Status
WHERE Status_Name = 'First Team'),
25, 291);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """prepare ins2 from
INSERT INTO Contracts (Player_Id, Update_Date,
Joined_Club, Club_Id, Left_Club, Squad_Id,
Squad_Stat_Id, Wage, Contract_Type, On_Loan,
Contract_End, Minimum_Fee,Relegation_Fee,
Non_Promo_Fee, Trans_Stat_Id, Sale_Value,
Per_Squad_Stat, Happiness, Squad_Rep)
VALUES
(217, DATE '2004-11-01', DATE '2001-01-01',
1500000040, NULL, 0, 5, 75, 'P', 'N', DATE '2006-06-30', 0,
0, 0, 4, 6, 2, 45, 491);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """explain options 'f' ins1;"""
    output = _dci.cmdexec(stmt)
    stmt = """explain options 'f' ins2;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute ins1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """execute ins2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """explain options 'f'
DELETE FROM
CONTRACTS WHERE PLAYER_ID = 215 AND UPDATE_DATE =
(SELECT Last_Update FROM Application_Control
WHERE Application_Id = 'SoccerV10');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """DELETE FROM
CONTRACTS WHERE PLAYER_ID = 215 AND UPDATE_DATE =
(SELECT Last_Update FROM Application_Control
WHERE Application_Id = 'SoccerV10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """select * from Contracts;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)

