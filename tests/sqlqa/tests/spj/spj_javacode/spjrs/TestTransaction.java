// @@@ START COPYRIGHT @@@
//
// (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

//
//	Test SQL transaction in SPJ
//
public class TestTransaction  {

	public static void main (String[] args) { }
   
       // 
	//   Auto Commit 
	//
	public static void InsertAutoCommit (String in) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";
		String name = in.trim();

		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("insert into " + name + " values (1, 'aaa', 101)");
		stmt.executeUpdate("insert into " + name + " values (2, 'aaa', 102)");
	}

       // 
	//    Commit transaction, disable auto commit 
	//
	public static void InsertCommit (String in) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";
		String name = in.trim();

		conn = DriverManager.getConnection(url) ;
		conn.setAutoCommit(false);
		Statement stmt = conn.createStatement();
		stmt.execute("Begin Work;");
		stmt.executeUpdate("insert into " + name + " values (1, 'aaa', 101)");
		stmt.executeUpdate("insert into " + name + " values (2, 'aaa', 102)");
		conn.commit();
		conn.setAutoCommit(true);
	}

       // 
	//    Rollback transaction, disable auto commit 
	//
	public static void InsertRollback (String in) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";
		String name = in.trim();

		conn = DriverManager.getConnection(url) ;
		conn.setAutoCommit(false);
		Statement stmt = conn.createStatement();
		stmt.execute("Begin Work;");
		stmt.executeUpdate("insert into " + name + " values (1, 'aaa', 101)");
		stmt.executeUpdate("insert into " + name + " values (2, 'aaa', 102)");
		conn.rollback();
		conn.setAutoCommit(true);
	}

	public static void testSelect (String in, java.sql.ResultSet[] rs) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";
		String name = in.trim();

		try {
			System.out.println("Enter select ...");
			conn = DriverManager.getConnection(url) ;
			Statement stmt = conn.createStatement();
			rs[0] = stmt.executeQuery("select * from " + name);
		}
		catch (Exception ex) {
			//rs[0] = ex.getMessage();
			throw ex;
		}
	}

}
