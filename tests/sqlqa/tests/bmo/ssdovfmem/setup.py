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
    _dci.setup_schema(defs.my_schema)

    stmt = """prepare explainIt from                                                      
    	select substring(cast(SEQ_NUM+100 as char(3)),2,2) s,                               
    	cast(LEFT_CHILD_SEQ_NUM as char(2)) lc,                                             
    	cast(RIGHT_CHILD_SEQ_NUM as char(2)) rc,                                            
    	substring(operator,1,16) operator,                                                  
    	substring                                                                           
    	(substring(tname from (1+locate('.',tname))),                                       
    	(1+locate('.',substring(tname from (1+locate('.',tname))))),                        
    	10) tab_name,                                                                       
    	cast(cardinality as numeric(11)) cardinal,                                          
    	cast(operator_cost as char(11)) op_cost,                                            
    	cast(total_cost as char(11)) tot_cost                                               
    	from table (explain(NULL,'XX'))                                                     
    	order by 1 desc;"""                                                                 
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D01                                                            
    	(                                                                                   
    	pk int not null not droppable primary key                                           
    	, val01 int                                                                         
    	, val02 int                                                                         
    	) number of partitions 1;"""                                                        
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D02                                                            
    	(                                                                                   
    	pk int not null not droppable primary key                                           
    	, val01 int                                                                         
    	, val02 int                                                                         
    	) number of partitions 1;"""                                                        
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D03                                                            
    	(                                                                                   
    	pk int not null not droppable primary key                                           
    	, val01 int                                                                         
    	, val02 int                                                                         
    	);"""                                                                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D04 like D01 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D05 like D02 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D06 like D03 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D07 like D01 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D08 like D02 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D09 like D03 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table D10 like D01 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table F01                                                            
    	(                                                                                   
    	pk int not null not droppable primary key                                           
    	, fk_d01 int not null -- foreign key references D01(pk)                             
    	, fk_d02 int not null -- foreign key references D02(pk)                             
    	, fk_d03 int not null -- foreign key references D03(pk)                             
    	, fk_d04 int not null -- foreign key references D04(pk)                             
    	, fk_d05 int not null -- foreign key references D05(pk)                             
    	, fk_d06 int not null -- foreign key references D06(pk)                             
    	, fk_d07 int not null -- foreign key references D07(pk)                             
    	, fk_d08 int not null -- foreign key references D08(pk)                             
    	, fk_d09 int not null -- foreign key references D09(pk)                             
    	, fk_d10 int not null -- foreign key references D10(pk)                             
    	, val01 int                                                                         
    	, val02 int                                                                         
    	, val01_d01 int                                                                     
    	, val02_d01 int                                                                     
    	, val01_d02 int                                                                     
    	, val02_d02 int                                                                     
    	, val01_d03 int                                                                     
    	, val02_d03 int                                                                     
    	);"""                                                                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """Create table F02 like F01 with partitions;"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D01                                                             
    	select c1, mod(c1,3), mod(c1,6)                                                     
    	from (values(1)) T                                                                  
    	transpose 0,1,2,3,4,5,6,7,8,9 as c1                                                 
    	;"""                                                                                
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D02                                                             
    	select c1+c2*10, mod(c1+c2*10,5), c1                                                
    	from (values(1)) T                                                                  
    	transpose 0,1,2,3,4,5,6,7,8,9 as c1                                                 
    	transpose 0,1,2,3,4,5,6,7,8,9 as c2                                                 
    	;"""                                                                                
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D03                                                             
    	select c1+c2*10+c3*100, c1, c1+c2*10                                                
    	from (values(1)) T                                                                  
    	transpose 0,1,2,3,4,5,6,7,8,9 as c1                                                 
    	transpose 0,1,2,3,4,5,6,7,8,9 as c2                                                 
    	transpose 0,1,2,3,4,5,6,7,8,9 as c3                                                 
    	;"""                                                                                
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert with no rollback into F01                                            
    	select c1+c2*10+c3*100+c4*1000+c5*10000+c6*100000                                   
    	,c1                       -- fk_d01(10)                                             
    	,c1+c2*10                 -- fk_d02(100)                                            
    	,c1+c2*10+c3*100          -- fk_d03(1,000)                                          
    	,c1                       -- fk_d04(10)                                             
    	,c1+c2*10                 -- fk_d05(100)                                            
    	,c1+c2*10+c3*100          -- fk_d06(1,000)                                          
    	,c1                       -- fk_d07(10)                                             
    	,c1+c2*10                 -- fk_d08(100)                                            
    	,c1+c2*10+c3*100          -- fk_d09(1,000)                                          
    	,c1                       -- fk_d10(10)                                             
    	,c1+c2*10                 -- val01 (100)                                            
    	,mod(c1+c2*100+c3*100,200)-- val02 (200)                                            
    	,mod(c1,3)                -- val01_d01(3)                                           
    	,mod(c1,6)                -- val02_d01(6)                                           
    	,mod(c1+c2*10,5)          -- val01_d02(5)                                           
    	,c1                       -- val02_d02(10)                                          
    	,c1                       -- val01_d03(10)                                          
    	,c1+c2*10                 -- val02_d03(100)                                         
    	from (values(1)) T                                                                  
    	transpose 0,1,2,3,4,5,6,7,8,9 as c1                                                 
    	transpose 0,1,2,3,4,5,6,7,8,9 as c2                                                 
    	transpose 0,1,2,3,4,5,6,7,8,9 as c3                                                 
    	transpose 0,1,2,3,4,5,6,7,8,9 as c4                                                 
    	transpose 0 as c5                                                                   
    	transpose 0 as c6                                                                   
    	-- transpose 0,1,2,3,4,5,6,7,8,9 as c5                                              
    	-- transpose 0,1,2,3,4,5,6,7,8,9 as c6                                              
    	;"""                                                                                
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D04 select * from D01;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D05 select * from D02;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D06 select * from D03;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D07 select * from D01;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D08 select * from D02;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D09 select * from D03;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into D10 select * from D01;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into F02 select * from F01;"""                                       
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """set schema """ + defs.w_schema + """;"""                                    
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D01 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D02 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D03 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D04 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D05 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D06 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D07 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D08 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D09 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table D10 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table F01 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """update statistics for table F02 on every column;"""                         
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """create table Customers (Cust_Id int, Cust_Name varchar(10)) no partition;"""
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into Customers values (1, 'Craig');"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into Customers values (2, 'John Doe');"""                            
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into Customers values (3, 'Jane Doe');"""                            
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """create table Sales (Cust_Id int, Item varchar(10)) no partition ;"""        
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into Sales values (2, 'Camera');"""                                  
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into  Sales values (3, 'Computer');"""                               
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into Sales values (3, 'Monitor');"""                                 
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """insert into Sales values (4, 'Printer');"""                                 
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """cqd EXE_DIAGNOSTIC_EVENTS 'ON';"""                                          
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """cqd EXE_BMO_DISABLE_CMP_HINTS_OVERFLOW_SORT 'OFF';"""     
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """cqd EXE_BMO_DISABLE_CMP_HINTS_OVERFLOW_HASH 'OFF';"""     
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """cqd PHY_MEM_CONTINGENCY_MB '$PHY_MEM_PRESSURE';"""                          
    output = _dci.cmdexec(stmt)                                                           
                                                                                           
    stmt = """cqd query_cache '0';"""                                                     
    output = _dci.cmdexec(stmt)
