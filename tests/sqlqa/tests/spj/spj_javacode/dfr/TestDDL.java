// @@@ START COPYRIGHT @@@
//
// (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
// @@@ END COPYRIGHT @@@

import java.sql.*;

public class TestDDL  {

	public static void main (String[] args) { }
   
	public static void createTable() throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter createTable...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int)");
		stmt.executeUpdate("alter table t1 rename to t1_tmp");
		stmt.executeUpdate("drop table t1_tmp");
		stmt.executeUpdate("create table t1 (c1 int not null primary key, c2 varchar(20) not null, c3 int)");
	}

	public static void createIndex () throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter createIndex...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create index idx1 on t1(c2)");
		stmt.executeUpdate("drop index idx1");
		stmt.executeUpdate("create index idx1 on t1(c2)");
	}

	public static void createView () throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter createView...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create view v1(a, b) as select c1, c3 from t1");
		stmt.executeUpdate("drop view v1");
		stmt.executeUpdate("create view v1(a, b) as select c1, c3 from t1");
	}
 
	public static void createTrigger () throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter createTrigger...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create trigger trg1 before insert on t1" +
                                 " REFERENCING NEW AS newR " +
                                 "FOR EACH ROW SET newR.c3 = newR.c3 + 100");
		stmt.executeUpdate("alter trigger disable trg1");
		stmt.executeUpdate("drop trigger trg1");
		stmt.executeUpdate("create trigger trg1 before insert on t1" +
                                 " REFERENCING NEW AS newR " +
                                 "FOR EACH ROW SET newR.c3 = newR.c3 + 100");
	}

	public static void createMV () throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter createMV...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create mv mv1 refresh on request initialize on refresh " +
                                        "hash partition by (c1) " +
                                        "as select c1, c2 from t1");
		stmt.executeUpdate("alter mv mv1 rename to mv1_tmp");
		stmt.executeUpdate("drop mv mv1_tmp" );
		stmt.executeUpdate("create mv mv1 refresh on request initialize on refresh " +
                                        "hash partition by (c1) " +
                                        "as select c1, c2 from t1");
	}

	public static void createSynonym () throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter createSynonym ...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create synonym st1 for t1"); 
		stmt.executeUpdate("drop synonym st1");
		stmt.executeUpdate("create synonym st1 for t1"); 
	}

	public static void createProcedure() throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		System.out.println("Enter createProcedure...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("create procedure proc1() " +
					     "external name 'TestDDL.createTable' " +
					     "library qa_spjlib.qa_dfr " + 
					     "language java " +
					     "parameter style java"); 
		stmt.executeUpdate("drop procedure proc1");
		stmt.executeUpdate("create procedure proc1() " +
					     "external name 'TestDDL.createTable' " +
					     "library qa_spjlib.qa_dfr " + 
					     "language java " +
					     "parameter style java"); 
	}
}