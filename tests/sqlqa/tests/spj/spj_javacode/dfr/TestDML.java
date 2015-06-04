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

public class TestDML  {

	public static void main (String[] args) { }
   
	public static void testInsert() throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter insert ...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("insert into t1 values (1, 'aaa', 101)");
		stmt.executeUpdate("insert into t1 values (2, 'aaa', 102)");
	}

	public static void testSelect(java.sql.ResultSet[] rs) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter select ...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		rs[0] = stmt.executeQuery("select * from t1");
	}

	public static void testUserFunction(java.sql.ResultSet[] rs) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		//System.out.println("Enter testUserFunction...");
		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		rs[0] = stmt.executeQuery("select current_user as current_user_c, user as user_c, session_user as session_user_c " +
                            " from (values(1)) t");
	}

	public static void testCallSPJ(java.sql.ResultSet[] rs) throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";
	       CallableStatement cs = null;

		conn = DriverManager.getConnection(url) ;
		cs = conn.prepareCall("{call testUserFunction()}");
		boolean hasResults = cs.execute();
		if (hasResults == true) {
			rs[0] = cs.getResultSet();
		}
	}

	public static void testDelete() throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("delete from t1");
	}

	public static void testUpdate() throws Exception
	{
		Connection conn = null;
		String url = "jdbc:default:connection";

		conn = DriverManager.getConnection(url) ;
		Statement stmt = conn.createStatement();
		stmt.executeUpdate("update t1 set c3 = 111 where c1 = 1");
	}
}


