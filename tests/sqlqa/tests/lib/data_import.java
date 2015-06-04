/**
 * @@@ START COPYRIGHT @@@
 *
 * (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @@@ END COPYRIGHT @@@
 */

import java.sql.*;
import java.math.*;
import java.util.*;
import java.io.*;

public class data_import
{
    private static PreparedStatement pStmt = null;
    private static String mycat = null;
    private static String mysch = null;

    private static final HashMap<Integer, String> typeMap;
    static
    {
        typeMap = new HashMap<Integer, String>();
        typeMap.put(Types.ARRAY, "Types.ARRAY");
        typeMap.put(Types.BIGINT, "Types.BIGINT");
        typeMap.put(Types.BINARY, "Types.BINARY");
        typeMap.put(Types.BIT, "Types.BIT");
        typeMap.put(Types.BLOB, "Types.BLOB");
        typeMap.put(Types.BOOLEAN, "Types.BOOLEAN");
        typeMap.put(Types.CHAR, "Types.CHAR");
        // typeMap.put(Types.GLOB, "Types.GLOB");
        typeMap.put(Types.DATALINK, "Types.DATALINK");
        typeMap.put(Types.DATE, "Types.DATE");
        typeMap.put(Types.DECIMAL, "Types.DECIMAL");
        typeMap.put(Types.DISTINCT, "Types.DISTINCT");
        typeMap.put(Types.DOUBLE, "Types.DOUBLE");
        typeMap.put(Types.FLOAT, "Types.FLOAT");
        typeMap.put(Types.INTEGER, "Types.INTEGER");
        typeMap.put(Types.JAVA_OBJECT, "Types.JAVA_OBJECT");
        typeMap.put(Types.LONGVARBINARY, "Types.LONGVARBINARY");
        typeMap.put(Types.LONGVARCHAR, "Types.LONGVARCHAR");
        typeMap.put(Types.NULL, "Types.NULL");
        typeMap.put(Types.NUMERIC, "Types.NUMERIC");
        typeMap.put(Types.OTHER, "Types.OTHER");
        typeMap.put(Types.REAL, "Types.REAL");
        typeMap.put(Types.REF, "Types.REF");
        typeMap.put(Types.SMALLINT, "Types.SMALLINT");
        typeMap.put(Types.STRUCT, "Types.STRUCT");
        typeMap.put(Types.TIME, "Types.TIME");
        typeMap.put(Types.TIMESTAMP, "Types.TIMESTAMP");
        typeMap.put(Types.TINYINT, "Types.TINYINT");
        typeMap.put(Types.VARBINARY, "Types.VARBINARY");
        typeMap.put(Types.VARCHAR, "Types.VARCHAR");
    }

    private static void datatypeNotSupported(int t)
    {
        System.out.println("ERROR: datatype " + typeMap.get(t) + " is not supported.");
        System.exit(1);
    }

    public List<Integer> getDDL(Connection conn, String table)
    {
        int i, type;
        String cmd = "select [first 1] * from " + table;
        Statement stmt = null;
        ResultSet rs = null;
        ResultSetMetaData rsMD = null;
        List<Integer> coltypes = new ArrayList<Integer>();

        try
        {
            stmt = conn.createStatement();
            rs = stmt.executeQuery(cmd);
            rsMD = rs.getMetaData();
            for (i = 1; i <= rsMD.getColumnCount(); i++)
                coltypes.add(rsMD.getColumnType(i));
            
            if (stmt != null)
                stmt.close(); 
        }
        catch (SQLException se)
        {
            System.out.println("ERROR: SQLException for: " + cmd);
            se.printStackTrace();
            System.out.println(se.getMessage());
            return null;
        }
        catch (Exception e)
        {
            System.out.println("ERROR: Exception for: " + cmd);
            e.printStackTrace();
            System.out.println(e.getMessage());
            return null;
        }
    
        return coltypes;
    }

    public static boolean handleBatchUpdateException(BatchUpdateException e, PrintWriter writer) 
    {
        boolean needRetry = false;
        String output = "";
        int count = 0;

        output = "---BatchUpdateException----\n";
        e.printStackTrace();
        output = output + e.getMessage() + "\n";
        // System.out.println("  e.getUpdateCounts().length = "
        //                  + e.getUpdateCounts().length);
        // int[] bueUpdateCount = e.getUpdateCounts();
        // for (int i = 0; i < e.getUpdateCounts().length; i++)
        //   System.out.println("ERROR: update count for " + i + "th command: "
        //                                + bueUpdateCount[i]);
        output = output + "  SQLState   " + e.getSQLState() + "\n";
        output = output + "  Error Code " + e.getErrorCode() + "\n";

        Throwable cause = e.getCause();
        while (cause != null) 
        {
            output = output + "  Cause = " + cause.getMessage() + "\n";
            cause = cause.getCause();
        }

        SQLException nextException = e.getNextException();

        while (nextException != null) 
        {
            count++;
            if (count >= 5)
            {
                output = output + "<more exceptions are not printed>\n";
                break;
            }

            output = output + "---SQLException----\n";
            // nextException.printStackTrace();
            output = output + nextException.getMessage() + "\n";
            // System.out.println("  e.getUpdateCounts().length = "
            //                   + e.getUpdateCounts().length);
            output = output + "  SQLState   " + nextException.getSQLState() + "\n";
            output = output + "  Error Code " + nextException.getErrorCode() + "\n"; 

            if (/* nextException.getErrorCode() == -8606 && */ nextException.getMessage().contains("TMF") && nextException.getMessage().contains("error 97"))
                needRetry = true;

            cause = nextException.getCause();

            while (cause != null) 
            {
                output = output + "  Cause = " + cause.getMessage() + "\n";
                cause = cause.getCause();
            }
            nextException = nextException.getNextException();
        }

        if (! needRetry)
        {
            System.out.println(output);
            writer.println(output);
            writer.flush();
        }
        else
        {
            System.out.println ("-> Sees TMF error 97");
            writer.println("-> Sees TMF error 97");
            writer.flush();
        }

        return needRetry;
    }

    private static Connection getMyConnection(String targettype)
    {
        Properties props = null;
        String url = null;
        Connection conn = null;
        final int max_conn_retry = 10;

        for (int retry = 1; retry <= max_conn_retry; retry++)
        {
            try
            {
                String propFile = System.getProperty("hpt4jdbc.properties");
                if (propFile != null)
                {
                    FileInputStream fs = new FileInputStream(new File(propFile));
                    props = new Properties();
                    props.load(fs);

                    url = props.getProperty("url");
                    mycat = props.getProperty("catalog");
                    mysch = props.getProperty("schema");
                }
                else
                {
                    System.out.println("ERROR: hpt4jdbc.properties is not set. Exiting.");
                    System.exit(0);
                }

                if (targettype.equals("TR"))
                    Class.forName("org.trafodion.jdbc.t4.T4Driver");

                conn = DriverManager.getConnection(url, props);
 
                // no exception, no need to retry, we are done
                break;
            }
            catch (SQLException se)
            {
                System.out.println("ERROR: SQLException");
                se.printStackTrace();
                System.out.println(se.getMessage());
                // retry this particular error to workaruond BUG#1252790.  The
                // rest are fatal, exit right now
                if (! se.getMessage().contains("Zookeeper entry not in connecting state"))
                    System.exit(1);
            }
            catch (Exception e)
            {
                System.out.println("ERROR: Exception");
                e.printStackTrace();
                System.out.println(e.getMessage());
                System.exit(1);
            }
        } // retry loop

        return conn;
    }

    private static void setColType(int num, String col, int type)
    {
       int idx;
       String s = null;

       /* SQ SQL types
          fixed length character
            CHAR[ACTER]
            NCHAR
            NATIONAL CHAR[ACTER]
          variable length character
            VARCHAR
            CHAR[ACTER] VARYING
            NCHAR VARYING
            NATIONAL CHAR[ACTER] VARYING
          numeric
            NUMERIC
            SMALLINT
            INTEGER
            LARGEINT
          floating point
            FLOAT
            REAL
            DOUBLE PRECISION
            Decimal
            DECIMAL
            Date Time
            DATE      (example: DATE '2007 10 02')
            TIME      (example: TIME '21:08:15:00.00')
            TIMESTAMP (example: TIMESTAMP '2007 12 21:08:15:00.00')
            interval
            INTERVAL  (example: INTERVAL '30' DAY)
        */
        try 
        {
            if ("".equals(col))
            {
                pStmt.setNull(num, type);
                return;
            }

            switch (type)
            {
            case Types.BIGINT:
                pStmt.setLong(num, Long.parseLong(col.trim()));
                break;
            case Types.BINARY:
            case Types.LONGVARBINARY:
            case Types.TINYINT:
            case Types.VARBINARY:
                pStmt.setByte(num, Byte.parseByte(col.trim()));
                break;
            case Types.BIT:
            case Types.BOOLEAN:
                pStmt.setBoolean(num, Boolean.parseBoolean(col.trim()));
                break;
            case Types.CHAR:
            case Types.LONGVARCHAR:
            case Types.VARCHAR:
                pStmt.setString(num, col);
                break;
            case Types.DATE:
                pStmt.setDate(num, java.sql.Date.valueOf(col.trim()));
                break;
            case Types.DECIMAL:
            case Types.NUMERIC:
                pStmt.setBigDecimal(num, new BigDecimal(col.trim()));
                break;
            case Types.DOUBLE:
                pStmt.setDouble(num, Double.parseDouble(col.trim()));
                break;
            case Types.FLOAT:
            case Types.REAL:
                pStmt.setFloat(num, Float.parseFloat(col.trim()));
                break;
            case Types.INTEGER:
                pStmt.setInt(num, Integer.parseInt(col.trim()));
                break;
            case Types.SMALLINT:
                pStmt.setShort(num, Short.parseShort(col.trim()));
                break;
            case Types.TIME:
                pStmt.setTime(num, java.sql.Time.valueOf(col.trim()));
                break;
            case Types.TIMESTAMP:
                // java Timestamp needs to be in the format of
                // yyyy-mm-dd hh:mm:ss[.fffffffff]
                // some of our data file has it as:
                // yyyy-mm-dd:hh:mm:ss[.fffffffff]
                s = col.trim();
                idx = "yyyy-mm-dd".length();
                if (s.substring(idx, idx+1).equals(":"))
                    s = s.substring(0, idx) + ' ' + s.substring(idx+1);
                pStmt.setTimestamp(num, java.sql.Timestamp.valueOf(s));
                break;
            case Types.OTHER:
                // INTERVAL uses Types.OTHER
                pStmt.setObject(num, col.trim());
                break;
            case Types.ARRAY:
            case Types.BLOB:
                // case Types.GLOB:
            case Types.DATALINK:
            case Types.DISTINCT:
            case Types.JAVA_OBJECT:
            case Types.NULL:
            case Types.REF:
            case Types.STRUCT:
                datatypeNotSupported(type);
                break;
            default:
                System.out.println("ERROR: Unrecognized type code: " + type);
                System.exit(1);
            }
        }
        catch (SQLException se)
        {
            System.out.println("ERROR: SQLException");
            se.printStackTrace();
            System.out.println(se.getMessage());
            System.exit(1);
        }
        catch (Exception e)
        {
            System.out.println("ERROR: Exception");
            e.printStackTrace();
            System.out.println(e.getMessage());
            System.exit(1);
        }
    }

    // Returns actual row count loaded, 0 if we are done.
    private static int loadOneBatch(Connection conn, String tablename, 
        List<Integer> coltypes, String datafile, int batch_startrow, 
        int batch_rowcount, String delim, String targettype
        ) throws SQLException, IOException
    {
        FileReader fr = null; //new FileReader("nation_data");
        BufferedReader br = null; //new BufferedReader(fr);
        String line = null;
        String col = null;
        String insert = null;
        int lineno, type, myrowcount = 0;
        int[] rescnt = null;

        try {
            if (targettype.equals("TR"))
                insert = "upsert using load into ";
            else
                insert = "insert into ";
            insert += (tablename + " values (?"); 
            for (int i = 1; i < coltypes.size(); i++)
                insert += ",?";
            insert += ")";
            pStmt = conn.prepareStatement(insert);

            fr = new FileReader(datafile);
            br = new BufferedReader(fr);

            lineno = -1;

            while((line = br.readLine()) != null)
            {
                lineno++;
               
                // we are not in the assigned range yet.
                if (lineno < batch_startrow)
                    continue;

                // we are done
                if (batch_rowcount != -1 && // read until the end of file
                   (lineno >= batch_startrow + batch_rowcount))
                    break;

                // The second parameter -1 means: "If n is non-positive
                // then the pattern will be applied as many times as
                // possible and the array can have any length."  This
                // is important, because we do want a string like
                // "<token>,,<token2>' to be parsed as
                // <token1> <empty string> <token2>.  That "any
                // length" is what we need here.
                String splitarray[] = line.split("[" + delim + "]", -1);
                if (splitarray.length != coltypes.size())
                {
                    System.out.println("ERROR: Mismatched column numbers. Columns in table: " + coltypes.size() + " columns in file: " + splitarray.length);
                    System.exit(1);
                }

                for (int i = 0; i < splitarray.length; i++)
                {
                    col = splitarray[i];
                    // col = col.trim();
                    type = coltypes.get(i);
                    setColType(i+1, col, type);
                }

                pStmt.addBatch();
                myrowcount++;
            }

            /* run the batch now. */
            rescnt = pStmt.executeBatch();
            fr.close();
            pStmt.close();

            return myrowcount;
        }
        catch (Exception e)
        {
            throw e;
        }
    }

    public static void main(String[] args) //throws java.io.IOException
    {
        final int max_retry = 10, max_batch_rowcount = /* 200000 */ /* 100000 */ 50000 /* 30000 */;
        int pos, startrow = -1, rowcount = 0, batch_rowcount, 
            total_rowcount = 0, num_dots, batchnum = 0, rc = -1;
        String tablename = null;
        String datafile = null;
        String delim = null;
        String ln = null;
        List<Integer> coltypes = null;
        data_import di = new data_import();
        Connection conn = null;
        String col = null;
        String workdir = null;
        String logfile = null;
        String targettype = null;

        try
	{
            if (args.length < 5)
	    {
		System.out.println("USAGE: " + data_import.class.getName() + " <table> <data file> <start line> <count> <delimiter> <work dir>");
		System.exit(0);
	    }

            tablename = args[0]; 
            datafile = args[1];
            // -1 means starting from 0
            startrow = Integer.parseInt(args[2]);
            // -1 means all rows
            rowcount = Integer.parseInt(args[3]);
            delim = args[4];
            workdir = args[5];
            targettype = args[6];

            // mycat and mysch is set in getMyConnection().  This need to 
            // be called before they are used.
            conn = getMyConnection(targettype);

            // sanity checks and parameter adjustment.
            pos = -1;
            num_dots = 0;
            while ((pos = tablename.indexOf('.', pos+1)) != -1)
               num_dots ++;
            if (num_dots >= 3 || tablename.trim().startsWith(".") ||
                tablename.trim().endsWith("."))
            {
                System.out.println("ERROR: Invalid <table> :" + tablename);
                System.exit(1);
            }
         
            if (num_dots == 0)
                tablename = mycat + "." + mysch + "." + tablename;
            else if (num_dots == 1)
                tablename = mycat + "." + tablename;
        
            if (startrow < -1)
            {
                System.out.println("ERROR: Invalid <start row>: " + startrow);
                System.exit(1);
            }
            else if (startrow == -1)
                startrow = 0;

            if (rowcount < -1)
            {
                System.out.println("ERROR: Invalid <row count>: " + rowcount);
                System.exit(1);
            } 

            if (delim.length() != 1)
            {
               System.out.println("ERROR: need one and only one delimitor: " + delim);
               System.exit(1);
            }

            if (! targettype.equals("SQ") && ! targettype.equals("TR"))
            {
               System.out.println("ERROR: Only supported TR or SQ target type. Unsupported target type " + targettype);
               System.exit(1);
            }

            coltypes = di.getDDL(conn, tablename);
            if (coltypes == null)
            {
                System.out.println("ERROR: null column type list.");
                conn.close();
                System.exit(1);
            }

            File f = new File(datafile);
            logfile = workdir + "/" + "import_" + tablename + "_" + f.getName() + "_" + String.valueOf(startrow) + "_" + String.valueOf(rowcount) + ".out";
            PrintWriter writer = new PrintWriter(logfile, "UTF-8");

            while (true) {
                if (rowcount == -1)
                    batch_rowcount = max_batch_rowcount;
                else if (max_batch_rowcount * batchnum > rowcount)
                    batch_rowcount = rowcount % max_batch_rowcount;
                else
                    batch_rowcount = max_batch_rowcount;

                for (int retry = 1; retry <= max_retry; retry++)
                {
                    try {
                        rc = loadOneBatch(conn, tablename, coltypes,
                            datafile, 
                            startrow + max_batch_rowcount * batchnum, 
                            batch_rowcount, delim, targettype);

                        if (rc > 0)
                        {
                            System.out.println("loaded (startrow: " + startrow + " batchnum: " + batchnum + ") try: " + retry);
                            writer.println("loaded (startrow: " + startrow + " batchnum: " + batchnum + ") try: " + retry);
                            writer.flush();
                        }

                        break; // no exception, no need to retry.
                    }
                    catch (BatchUpdateException bue)
                    {
                        if (handleBatchUpdateException(bue, writer))
                        {
                            // an exception that should be retried.
                            if (retry == max_retry)
                            {
                                System.out.println("ERROR: BatchUpdateException retried " + max_retry + " times and gave up.");
                                writer.println("ERROR: BatchUpdateException retried " + max_retry + " times and gave up.");
                                writer.flush();

                                System.exit(1);
                            }
 
                            Thread.sleep(5000); // sleep for 5 secs

                            System.out.println("executeBatch() retry " + retry + " TMF error 97: start: " + startrow + " batchnum: " + batchnum);
                            writer.println("executeBatch() retry " + retry + " TMF error 97: start: " + startrow + " batchnum: " + batchnum);
                            writer.flush();

                        }
                        else
                            // an exception that can't be retried, exit now.
                            System.exit(1);
                    }
                } // end of retry loop

                // no more.              
                if (rc <= 0)
                    break;

                total_rowcount += rc; 
                batchnum++;
            } // end of whle (True)

            writer.close();
        } // end of try
        catch (SQLException se)
        {
            System.out.println("ERROR: SQLException");
            se.printStackTrace();
            System.out.println(se.getMessage());
            System.exit(1);
        }
        catch (Exception e)
	{
            System.out.println("ERROR: Exception");
	    e.printStackTrace();
	    System.out.println(e.getMessage());
            System.exit(1);
        }

        System.out.println("start: " + startrow + " count: " + total_rowcount + " row(s) imported.");
    }
}
