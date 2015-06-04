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

import java.io.PrintStream;
import java.sql.Timestamp;

public class Jdbc_IO_Timestamp
{
  public static void ioTimestamp(Timestamp[] paramArrayOfTimestamp)
    throws Exception
  {
    System.err.println("In the Java Stored Procedure !");

    if (paramArrayOfTimestamp[0].equals(Timestamp.valueOf("1982-03-03 02:02:02")))
      paramArrayOfTimestamp[0] = Timestamp.valueOf("1982-05-05 04:04:04");
    else
      paramArrayOfTimestamp[0] = Timestamp.valueOf("1982-03-03 02:02:02");
  }
}
