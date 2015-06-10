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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sstream>
#include <string>
#include "sqlcli.h"
#include "sqludr.h"

using namespace tmudr;
#define EXCEPTION_INTERNAL_ERROR 38000
#define EXCEPTION_TEST_ERROR 38001
#define EXCEPTION_NO_ERROR 99999

class QATmudf : public UDR
{
public:
  QATmudf ();

  // compile time interface for TMUDFs
  void describeParamsAndColumns(UDRInvocationInfo &info);
  void describeDataflow(UDRInvocationInfo &info);
  void describeConstraints(UDRInvocationInfo &info);
  void describeStatistics(UDRInvocationInfo &info);
  void describeDesiredDegreeOfParallelism(UDRInvocationInfo &info,
                                          UDRPlanInfo &plan);
  void describePlanProperties(UDRInvocationInfo &info,
                              UDRPlanInfo &plan);
  void completeDescription(UDRInvocationInfo &info,
                           UDRPlanInfo &plan);

  // run time interface for TMUDFs and scalar UDFs (once supported)
  void processData(UDRInvocationInfo &info,
                   UDRPlanInfo &plan);

private:
  std::string testWhat;
  std::string testParm;
  int numKnownTests;
  struct 
  {
    std::string what; 
    std::string parm;
  } knownTests[100];

  int numSqlTypeNames;
  struct
  {
     int value;
     std::string name;
  } sqlTypeNames[100];

  void processTestParameters(UDRInvocationInfo &info);
  void testCmpTimeInterface(UDRInvocationInfo &info,
                            std::string whoAmI);
  // This one is speical, since it can only be called within
  // describeDesiredDegreeOfParallelism()
  void testCmpTimeInterfaceWithPlan(UDRInvocationInfo &info,
                                    UDRPlanInfo &plan,
                                    std::string whoAmI);
  void testCmpTimeInterfaceDescribeParamsAndColumns(UDRInvocationInfo &info);
  void testCmpTimeException(UDRInvocationInfo &info);
  void testCmpTimeInterfaceInvoked(UDRInvocationInfo &info, 
                                   std::string whoAmI);
  void testCmpTimeOutTableDeleteColumns(UDRInvocationInfo &info, 
                                        bool byName);
  // testCmpTimeOutTable() does part I at the compile time.
  // testRunTimeOutTable() does part II at the run time.
  void testCmpTimeOutTable(UDRInvocationInfo &info,
                           bool usePassThru);
  void testCmpTimeDegreeOfParallelism(UDRInvocationInfo &info,
                                      UDRPlanInfo &plan);
  void testCmpTimeInOutTablePartitioning(UDRInvocationInfo &info);
  void testCmpTimeInOutTableOrdering(UDRInvocationInfo &info);

  void testCmpTimeMisc(UDRInvocationInfo &info,
                       std::string what);

  void testRunTimeInterface(UDRInvocationInfo &info,
                            UDRPlanInfo &plan);
  void testRunTimeException(UDRInvocationInfo &info);
  void testRunTimeEmitXRows(UDRInvocationInfo &info);
  void testRunTimeInParmNamesAndIndexes(UDRInvocationInfo &info);
  void testRunTimeInTableNamesAndIndexes(UDRInvocationInfo &info);
  void testRunTimeInParmDataAndTypes(UDRInvocationInfo &info);
  void testRunTimeColDataAndTypes(UDRInvocationInfo &info);
  void testRunTimeInTableDataAndTypes(UDRInvocationInfo &info);
  void testRunTimeInOutTablePartitioning(UDRInvocationInfo &info);
  void testRunTimeInOutTableOrdering(UDRInvocationInfo &info);

  // testCmpTimeOutTable() does part I at the compile time.
  // testRunTimeOutTable() does part II at the run time.
  void testRunTimeOutTable(UDRInvocationInfo &info,
                           bool usePassThru);

  void emitXRows(UDRInvocationInfo &info, 
                 int xRows);
  void verifyElementNameAndIndex(UDRInvocationInfo &info,
                                 int objIdx,
                                 bool isPar);
  void verifyOrCopyElementData(UDRInvocationInfo &info,
                               int inObjIdx,
                               int outObjIdx,
                               bool isPar,
                               bool toVerify,
                               bool toCopy,
                               std::stringstream &errMsg);
#define verifyElementData(info, inObjIdx, outObjIdx, isPar, errMsg) \
  verifyOrCopyElementData(info, inObjIdx, outObjIdx, isPar, \
                          true /* toVerify */, false /* toCopy */, errMsg); 
#define copyElementData(info, inObjIdx, outObjIdx, isPar, errMsg) \
  verifyOrCopyElementData(info, inObjIdx, outObjIdx, isPar, \
                          false /* toVerify */, true /* toCopy */, errMsg);
#define verifyAndCopyElementData(info, inObjIdx, outObjIdx, isPar, errMsg) \
  verifyOrCopyElementData(info, inObjIdx, outObjIdx, isPar, \
                          true /* toVerify */, true /* toCopy */, errMsg);
  bool toTest(std::string what) { return (testWhat == what); }
  bool toTest(std::string what, std::string parm) 
  { 
    return ((testWhat == what) && (testParm == parm));
  }
};

extern "C" UDR * QA_TMUDF(const UDRInvocationInfo *info)
{
  return new QATmudf();
}

QATmudf::QATmudf()
{
  int i = 0;

  knownTests[i].what = "TEST_CMPTIME_EXCEPTION";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "describeParamsAndColumns";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "describeDataflow";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "describeConstraints";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "describeStatistics";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "describeDesiredDegreeOfParallelism";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "describePlanProperties";

  knownTests[i].what = "TEST_CMPTIME_INTERFACE_INVOKED";
  knownTests[i++].parm = "completeDescription";

  knownTests[i].what = "TEST_CMPTIME_DEGREE_OF_PARALLELISM";
  knownTests[i++].parm = "ANY_DEGREE_OF_PARALLELISM";

  knownTests[i].what = "TEST_CMPTIME_DEGREE_OF_PARALLELISM";
  knownTests[i++].parm = "DEFAULT_DEGREE_OF_PARALLELISM";

  knownTests[i].what = "TEST_CMPTIME_DEGREE_OF_PARALLELISM";
  knownTests[i++].parm = "MAX_DEGREE_OF_PARALLELISM";

  knownTests[i].what = "TEST_CMPTIME_DEGREE_OF_PARALLELISM";
  knownTests[i++].parm = "ONE_INSTANCE_PER_NODE";

  knownTests[i].what = "TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_INDEX";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_NAME";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_MISC_GETUDRNAME";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_EXCEPTION";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_IN_TABLE_ROWCOUNT";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_EMIT_X_ROWS";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_IN_PARM_NAMES_AND_INDEXES";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_IN_TABLE_NAMES_AND_INDEXES";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_IN_PARM_DATA_AND_TYPES";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_IN_TABLE_DATA_AND_TYPES";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_RUNTIME_OUT_TABLE_DEFINED_USING_PARMS";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_SET";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_PASSTHRU";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_PARTITIONING";
  knownTests[i++].parm = "<vary>";

  knownTests[i].what = "TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_ORDERING";
  knownTests[i++].parm = "<vary>";

  numKnownTests = i;

   
  /* An array to map to the TypeInfo::SQLTYPE_CODE with its names 
  enum SQLTYPE_CODE // Maps a column to its SQL type.
  {
    UNDEFINED_SQL_TYPE,
    SMALLINT,             // 16 bit integer
    INT,                  // 32 bit integer
    LARGEINT,             // 64 bit integer
    NUMERIC,              // Numeric with decimal precision
    DECIMAL_LSE,          // Decimal, leading sign embedded
    SMALLINT_UNSIGNED,    // unsigned 16 bit integer
    INT_UNSIGNED,         // unsigned 32 bit integer
    NUMERIC_UNSIGNED,     // unsigned numeric
    DECIMAL_UNSIGNED,     // unsigned decimal
    REAL,                 // 4 byte floating point number
    DOUBLE_PRECISION,     // 8 byte floating point number
    CHAR,                 // fixed length character types.
    VARCHAR,              // varying length character types.
    DATE,
    TIME,
    TIMESTAMP,
    INTERVAL
  };
  */
  i = 0;

  sqlTypeNames[i].value = TypeInfo::UNDEFINED_SQL_TYPE;
  sqlTypeNames[i++].name = "UNDEFINED_SQL_TYPE";

  sqlTypeNames[i].value = TypeInfo::SMALLINT;
  sqlTypeNames[i++].name = "SMALLINT";

  sqlTypeNames[i].value = TypeInfo::INT;
  sqlTypeNames[i++].name = "INT";

  sqlTypeNames[i].value = TypeInfo::LARGEINT;
  sqlTypeNames[i++].name = "LARGEINT";

  sqlTypeNames[i].value = TypeInfo::NUMERIC;
  sqlTypeNames[i++].name = "NUMERIC";

  sqlTypeNames[i].value = TypeInfo::DECIMAL_LSE;
  sqlTypeNames[i++].name = "DECIMAL_LSE";

  sqlTypeNames[i].value = TypeInfo::SMALLINT_UNSIGNED;
  sqlTypeNames[i++].name = "SMALLINT_UNSIGNED";

  sqlTypeNames[i].value = TypeInfo::INT_UNSIGNED;
  sqlTypeNames[i++].name = "INT_UNSIGNED";

  sqlTypeNames[i].value = TypeInfo::NUMERIC_UNSIGNED;
  sqlTypeNames[i++].name = "NUMERIC_UNSIGNED";

  sqlTypeNames[i].value = TypeInfo::DECIMAL_UNSIGNED;
  sqlTypeNames[i++].name = "DECIMAL_UNSIGNED";

  sqlTypeNames[i].value = TypeInfo::REAL;
  sqlTypeNames[i++].name = "REAL";

  sqlTypeNames[i].value = TypeInfo::DOUBLE_PRECISION;
  sqlTypeNames[i++].name = "DOUBLE_PRECISION";

  sqlTypeNames[i].value = TypeInfo::CHAR;
  sqlTypeNames[i++].name = "CHAR";

  sqlTypeNames[i].value = TypeInfo::VARCHAR;
  sqlTypeNames[i++].name = "VARCHAR"; 

  sqlTypeNames[i].value = TypeInfo::DATE;
  sqlTypeNames[i++].name = "DATE";

  sqlTypeNames[i].value = TypeInfo::TIME;
  sqlTypeNames[i++].name = "TIME";

  sqlTypeNames[i].value = TypeInfo::TIMESTAMP;
  sqlTypeNames[i++].name = "TIMESTAMP";

  sqlTypeNames[i].value = TypeInfo::INTERVAL;
  sqlTypeNames[i++].name = "INTERVAL";

  numSqlTypeNames = i;
}


void QATmudf::describeParamsAndColumns(UDRInvocationInfo &info)
{
  int t;

  processTestParameters(info);
  testCmpTimeInterface(info, "describeParamsAndColumns");

  // If the output table already has columns defined, we are done. Some of 
  // the tests do this to specifically test the columns at the run time. 
  if (info.out().getNumColumns() > 0)
    return;

  // Otherwise, the default is just to return the same input table back using
  // addPassThruColumns()
  // add all input table columns as output columns (t is the entire table)
  for (t = 0; t < info.getNumTableInputs(); t++)
    info.addPassThruColumns(t);
}

void QATmudf::describeDataflow(UDRInvocationInfo &info)
{
  processTestParameters(info);
  testCmpTimeInterface(info, "describeDataflow");
}

void QATmudf::describeConstraints(UDRInvocationInfo &info)
{
  processTestParameters(info);
  testCmpTimeInterface(info, "describeConstraints");
}
  
void QATmudf::describeStatistics(UDRInvocationInfo &info)
{
  processTestParameters(info);
  testCmpTimeInterface(info, "describeStatistics");
}
  
void QATmudf::describeDesiredDegreeOfParallelism(UDRInvocationInfo &info,
                                                 UDRPlanInfo &plan)
{
  processTestParameters(info);
  testCmpTimeInterface(info, "describeDesiredDegreeOfParallelism");
  testCmpTimeInterfaceWithPlan(info, plan, "describeDesiredDegreeOfParallelism");
}

void QATmudf::describePlanProperties(UDRInvocationInfo &info,
                                     UDRPlanInfo &plan)
{
  processTestParameters(info);
  testCmpTimeInterface(info, "describePlanProperties");
  testCmpTimeInterfaceWithPlan(info, plan, "describePlanProperties");
}

void QATmudf::completeDescription(UDRInvocationInfo &info,
                                  UDRPlanInfo &plan)
{
  processTestParameters(info);
  testCmpTimeInterface(info, "completeDescription");
  testCmpTimeInterfaceWithPlan(info, plan, "completeDescription");
}


void QATmudf::processData(UDRInvocationInfo &info, UDRPlanInfo &plan)
{
  processTestParameters(info);
  testRunTimeInterface(info, plan);
}


// private helper
void QATmudf::processTestParameters(UDRInvocationInfo &info)
{
  int i; 
  bool found = false;
  std::string colName;

  testWhat = "UNKNOWN";
  testParm = "UNKNOWN";

  // validate the input parameters
  if (info.getNumTableInputs() != 1)
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Invalid number of input table: expect 1, got %d",
      info.getNumTableInputs());

  if (info.par().getNumColumns() < 2)
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Invalid number of input parameters: expect at least 2: testWhat, testParm");

  if (info.par().getColumn(0).getType().getSQLType() == TypeInfo::CHAR)
  {
    colName = info.par().getColumn(0).getColName();
    testWhat = info.par().getString(0);
  }
  else
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Invalid input parameter testWhat: type(%d) usaege(%d)",
      info.par().getColumn(0).getType().getSQLType(),
      info.par().getColumn(0).getUsage());

  if (info.par().getColumn(1).getType().getSQLType() == TypeInfo::CHAR)
  {
    colName = info.par().getColumn(1).getColName();
    testParm = info.par().getString(1);
  }
  else
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Invalid input parameter testParm: type(%d) usaege(%d)",
      info.par().getColumn(1).getType().getSQLType(),
      info.par().getColumn(1).getUsage());

  // Make sure testWhat and testParm provided by the user is supported.
  for (i = 0; i < numKnownTests; i++)
  {
    if (knownTests[i].what == testWhat)
      {
         if ((knownTests[i].parm == "<vary>") ||
             (knownTests[i].parm == testParm))
         {
           found = true;
           break;
         }
      }
  } 

  if (not found)
   throw UDRException(
     EXCEPTION_INTERNAL_ERROR,
     "Unsupported (testWhat, testParm): (%s, %s)",
     testWhat.c_str(), testParm.c_str());
}


// a helper function to handle test cases for the compile time interface
void QATmudf::testCmpTimeInterface(UDRInvocationInfo &info, 
                                   std::string whoAmI)
{
  if (toTest("TEST_CMPTIME_EXCEPTION"))
    testCmpTimeException(info);
  else if (toTest("TEST_CMPTIME_INTERFACE_INVOKED", whoAmI))
    testCmpTimeInterfaceInvoked(info, whoAmI);
  else if (toTest("TEST_CMPTIME_MISC_GETUDRNAME"))
    testCmpTimeMisc(info, "GETUDRNAME");

  // The following ones are only to be callsed from a certain compiler 
  // interface.  whoAmI tells which function that is.
  if (whoAmI == "describeParamsAndColumns")
  {
    if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_INDEX"))
      testCmpTimeOutTableDeleteColumns(info, false);
    else if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_NAME"))
      testCmpTimeOutTableDeleteColumns(info, true);
    else if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_SET"))
      testCmpTimeOutTable(info, false);
    else if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_PASSTHRU"))
      testCmpTimeOutTable(info, true);
    else if (toTest("TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_PARTITIONING"))
      testCmpTimeInOutTablePartitioning(info);
    else if (toTest("TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_ORDERING"))
      testCmpTimeInOutTableOrdering(info);
  }
}

// a helper function to handle test cases for the compile time interface
void QATmudf::testCmpTimeInterfaceWithPlan(UDRInvocationInfo &info,
                                           UDRPlanInfo &plan,
                                           std::string whoAmI)
{
  // The following ones are only to be callsed from a certain compiler
  // interface.  whoAmI tells which one that is.
  if (whoAmI == "describeDesiredDegreeOfParallelism")
  {
    if (toTest("TEST_CMPTIME_DEGREE_OF_PARALLELISM"))
      testCmpTimeDegreeOfParallelism(info, plan);
  }
}

// Individual cmp time test case: exception
void QATmudf::testCmpTimeException(UDRInvocationInfo &info)
{
  throw UDRException(atoi(testParm.c_str()), "Test Compile Time Exception");
}


// Individual cmp time test case: interface invocation
void QATmudf::testCmpTimeInterfaceInvoked(UDRInvocationInfo &info, 
                                          std::string whoAmI)
{
  // Throw a EXCEPTION_NO_ERROR to let the user know that this interface
  // has been invoked
  throw UDRException(
    EXCEPTION_NO_ERROR,
    "Compiler time interface %s() is invoked",
    whoAmI.c_str());
}


void QATmudf::testCmpTimeOutTableDeleteColumns(UDRInvocationInfo &info,
                                               bool byName)
{
  int idx, numDelCols;
  std::string colName;

  // This is the number of columns to be deleted.  They will show up 
  // as the first <numDelCols>
  numDelCols = atoi(testParm.c_str());

  if (numDelCols > info.out().getNumColumns())
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Invalid number of deleting columns: %d > %d total input parameters\n",
      numDelCols, info.in().getNumColumns());

  if (byName)
  {
    // deleteColumn() by name
    for(idx = 0; idx < numDelCols; idx++)
    {
      colName = info.out().getColumn(0).getColName(); // always delete the new '1st column
      info.out().deleteColumn(colName);
    }
  }
  else
  {
    // deleteColumn by index
    for(idx = 0; idx < numDelCols; idx++)
      info.out().deleteColumn(0); // always delete the new '1st' column
  }
}

// Individual cmp time test case: table columns.  
// testCmpTimeOutTable() does part I at the compile time.
// testRunTimeOutTable() does part II at the run time.
void QATmudf::testCmpTimeOutTable(UDRInvocationInfo &info, bool usePassThru)
{
  int idx, numCols, t;

  numCols = atoi(testParm.c_str());

  if (numCols != info.in().getNumColumns())
    throw UDRException(
      EXCEPTION_TEST_ERROR,
      "Invalid number of table columns: expecting %d got %d",
      numCols, info.in().getNumColumns());

  /* delete all columns in the output table first */
  while (info.out().getNumColumns() > 0)
    info.out().deleteColumn(0);

  if (usePassThru)
  {
    // Use Pass thru method
    // we only support at most one table now, so t should be 0
    for (t = 0; t < info.getNumTableInputs(); t++)
      info.addPassThruColumns(t);
  }
  else
  {
    // Fetch the column definition one by one from the input table and
    // add them to the output table.
    for (idx = 0; idx < info.in().getNumColumns(); idx++)
      info.out().addColumn(info.in().getColumn(idx));
  }
}

void QATmudf::testCmpTimeDegreeOfParallelism(UDRInvocationInfo &info, 
                                             UDRPlanInfo &plan)
{
  if (toTest("TEST_CMPTIME_DEGREE_OF_PARALLELISM", "ANY_DEGREE_OF_PARALLELISM"))
    plan.setDesiredDegreeOfParallelism(UDRPlanInfo::ANY_DEGREE_OF_PARALLELISM);
  else if (toTest("TEST_CMPTIME_DEGREE_OF_PARALLELISM", "DEFAULT_DEGREE_OF_PARALLELISM"))
    plan.setDesiredDegreeOfParallelism(UDRPlanInfo::DEFAULT_DEGREE_OF_PARALLELISM);
  else if (toTest("TEST_CMPTIME_DEGREE_OF_PARALLELISM", "MAX_DEGREE_OF_PARALLELISM"))
    plan.setDesiredDegreeOfParallelism(UDRPlanInfo::MAX_DEGREE_OF_PARALLELISM);
  else if (toTest("TEST_CMPTIME_DEGREE_OF_PARALLELISM", "ONE_INSTANCE_PER_NODE"))
    plan.setDesiredDegreeOfParallelism(UDRPlanInfo::ONE_INSTANCE_PER_NODE);
}


void QATmudf::testCmpTimeInOutTablePartitioning(UDRInvocationInfo &info)
{
  int i, t, objIdx, numPartKeys;

  // addPassThruColumns() is generally called in describeParamsAndColumns().
  // But this fucntion gets called at the very beginining of 
  // describeParamsAndColumns() and we need the output columns defined before
  // specifying partitioning keys, so we have to call it here.  
  // describeParamsAndColumns() has a mechanism to skip calling 
  // addPassThruColumns() if the output columns already exist, so it's fine
  // to call it a bit earlier here.

  // Return the same input table back using addPassThruColumns()
  // add all input table columns as output columns (t is the entire table)
  for(t = 0; t < info.getNumTableInputs(); t++)
    info.addPassThruColumns(t);

  numPartKeys = atoi(testParm.c_str());
  if(numPartKeys != info.in().getQueryPartitioning().getNumEntries())
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of partitioning keys: expect %d, got %d",
       numPartKeys, info.in().getQueryPartitioning().getNumEntries());

  // Add all input table partitioning keys as the output table partitioning 
  // keys.  This is only to make sure that specifying output table
  // partitioning keys does not screw up anything.  We really have no way
  // of verifying that the rows with the same partitioning keys all went
  // to the same parallel instance.
  for(i = 0; i < numPartKeys; i++)
  {
    objIdx = info.in().getQueryPartitioning().getColumnNum(i);
    info.out().getQueryPartitioning().addEntry(objIdx);
  }
}


void QATmudf::testCmpTimeInOutTableOrdering(UDRInvocationInfo &info)
{
  int i, t, objIdx, numOrderKeys;

  // addPassThruColumns() is generally called in describeParamsAndColumns().
  // But this fucntion gets called at the very beginining of
  // describeParamsAndColumns() and we need the output columns defined before
  // specifying ordering keys, so we have to call it here.
  // describeParamsAndColumns() has a mechanism to skip calling
  // addPassThruColumns() if the output columns already exist, so it's fine
  // to call it a bit earlier here.

  // Return the same input table back using addPassThruColumns()
  // add all input table columns as output columns (t is the entire table)
  for(t = 0; t < info.getNumTableInputs(); t++)
    info.addPassThruColumns(t);

  numOrderKeys = atoi(testParm.c_str());
  if(numOrderKeys != info.in().getQueryOrdering().getNumEntries())
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of ordering keys: expect %d, got %d",
       numOrderKeys, info.in().getQueryOrdering().getNumEntries());

  // Add all input table ordering keys as the output table ordering keys.
  // This is to make sure that specifying output table ordering keys does 
  // not screw up anything.
  for(i = 0; i < numOrderKeys; i++)
  {
    objIdx = info.in().getQueryOrdering().getColumnNum(i);
    info.out().getQueryOrdering().addEntry(objIdx);
  }
}


void QATmudf::testCmpTimeMisc(UDRInvocationInfo &info,
                              std::string what)
{ 
  if (what == "GETUDRNAME") 
  {
    if (info.getUDRName() != testParm)
//.find(".QaTmUdf"))
    {
      throw UDRException(
        EXCEPTION_INTERNAL_ERROR,
        "Invalid UDR name: expecting %s got %s",
        testParm.c_str(), info.getUDRName().c_str());
    } 
  }
}


// a helper function to handle test cases for the run time interface
void QATmudf::testRunTimeInterface(UDRInvocationInfo &info,
                                   UDRPlanInfo &plan)
{
  // By default, we will return the same input table back.
  bool toEmitRows = true;

  if (toTest("TEST_RUNTIME_EXCEPTION"))
    testRunTimeException(info);
  else if (toTest("TEST_RUNTIME_EMIT_X_ROWS"))
  {
    testRunTimeEmitXRows(info);
    // This test already returns tables, no need to return another one.
    toEmitRows = false; 
  }
  else if (toTest("TEST_RUNTIME_IN_PARM_NAMES_AND_INDEXES"))
    testRunTimeInParmNamesAndIndexes(info);
  else if (toTest("TEST_RUNTIME_IN_TABLE_NAMES_AND_INDEXES"))
    testRunTimeInTableNamesAndIndexes(info);
  else if (toTest("TEST_RUNTIME_IN_PARM_DATA_AND_TYPES"))
    testRunTimeInParmDataAndTypes(info);
  else if (toTest("TEST_RUNTIME_IN_TABLE_DATA_AND_TYPES"))
  {
    testRunTimeInTableDataAndTypes(info);
    toEmitRows = false;
  }
  else if (toTest("TEST_RUNTIME_OUT_TABLE_DEFINED_USING_PARMS"))
  {
    // This test already returns tables, no need to return another one.
    testRunTimeOutTable(info, false);
    toEmitRows = false;
  }
  else if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_SET"))
  {
    // This test already returns tables, no need to return another one.
    testRunTimeOutTable(info, false);
    toEmitRows = false;
  }
  else if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DEFINED_USING_PASSTHRU"))
  {
    // This test already returns tables, no need to return another one.
    testRunTimeOutTable(info, true);
    toEmitRows = false;
  }
  else if (toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_INDEX") ||
           toTest("TEST_CMPTIME_RUNTIME_OUT_TABLE_DELETE_COLUMNS_BY_NAME"))
  {
    // This test already returns tables, no need to return another one.
    testRunTimeOutTable(info, false); // false -> don't use passthrough
    toEmitRows = false;
  }
  else if (toTest("TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_PARTITIONING"))
  {
    testRunTimeInOutTablePartitioning(info);
    toEmitRows = false;
  }
  else if (toTest("TEST_CMPTIME_RUNTIME_IN_OUT_TABLE_ORDERING"))
  {
    testRunTimeInOutTableOrdering(info);
    toEmitRows = false;
  }

  if (toEmitRows)
    emitXRows(info, 1);
}


// Individual run time test case: exception
void QATmudf::testRunTimeException(UDRInvocationInfo &info)
{
  throw UDRException(atoi(testParm.c_str()), "Test Run Time Exception");
}

// helper routine to return x times of the table rows
void QATmudf::emitXRows(UDRInvocationInfo &info, int xRows)
{
  int i;

  // loop over input rows
  while (getNextRow(info))
  {
    // produce the remaining columns and emit the row
    info.copyPassThruData();

    for (i = 0; i < xRows; i++)
      emitRow(info);
  }
}


// Individual run time test case: return x times of the table rows
void QATmudf::testRunTimeEmitXRows(UDRInvocationInfo &info)
{
  int xRows = 0;

  xRows = atoi(testParm.c_str());
  emitXRows(info, xRows);
}

// internal helper routine to verify (or copy) a column (or a parameter)
// This routine only throw an exception if it's an fatal error.  Otherwise, it 
// just keeps appending the error message to errMsg for the caller to handle
// the exception eventually.
void QATmudf::verifyOrCopyElementData(UDRInvocationInfo &info,
                                      int inObjIdx,
                                      int outObjIdx,
                                      bool isPar,
                                      bool toVerify,
                                      bool toCopy,
                                      std::stringstream &errMsg)
{
  #define MAX_CHAR_LEN 500
  int j, k, precision, scale, sqlType, usage, typeIdx, 
      length, maxCharLength, myLen;
  bool wasNull;
  std::string objName;
  std::string objValueStr;
  int objValueInt;
  long objValueLong;
  double objValueDouble;
  float myFloat, expFloat;
  const char *objValueChar;
  char origBuf[MAX_CHAR_LEN], expBuf[MAX_CHAR_LEN], 
       tmpBuf1[MAX_CHAR_LEN], tmpBuf2[MAX_CHAR_LEN];
  TypeInfo::SQLCharsetCode charsetCode;
  TypeInfo::SQLIntervalCode intervalCode;

  /* The list of SQL Type Code to be tested
     enum SQLTYPE_CODE // Maps a column to its SQL type.
     {
       UNDEFINED_SQL_TYPE,
       SMALLINT,             // 16 bit integer
       INT,                  // 32 bit integer
       LARGEINT,             // 64 bit integer
       NUMERIC,              // Numeric with decimal precision
       DECIMAL_LSE,          // Decimal, leading sign embedded
       SMALLINT_UNSIGNED,    // unsigned 16 bit integer
       INT_UNSIGNED,         // unsigned 32 bit integer
       NUMERIC_UNSIGNED,     // unsigned numeric
       DECIMAL_UNSIGNED,     // unsigned decimal
       REAL,                 // 4 byte floating point number
       DOUBLE_PRECISION,     // 8 byte floating point number
       CHAR,                 // fixed length character types.
       VARCHAR,              // varying length character types.
       DATE,
       TIME,
       TIMESTAMP,
       INTERVAL
     };
  */
  if (isPar)
  {
    sqlType = info.par().getColumn(inObjIdx).getType().getSQLType();
    usage = info.par().getColumn(inObjIdx).getUsage();
    objName = info.par().getColumn(inObjIdx).getColName();
  }
  else
  {
    sqlType = info.in().getColumn(inObjIdx).getType().getSQLType();
    usage = info.in().getColumn(inObjIdx).getUsage();
    objName = info.in().getColumn(inObjIdx).getColName();
  }

  if (toVerify)
  {
    typeIdx = -1;
    for (j = 0; j < numSqlTypeNames; j++)
    {
      // objName is in the format of Pxx_<type> or Cxx_<type>, only get the
      // <type> part.
      if (objName.length() < 4)
        throw UDRException(
          EXCEPTION_INTERNAL_ERROR,
          "Invalid parameter|column name: expect Pxx_<type>|Cxx_<type>, got %s",
          objName.c_str());

      if (objName.substr(4) == sqlTypeNames[j].name)
      {
        typeIdx = j;
        break;
      } 
    }

    if (typeIdx == -1)
      throw UDRException(
        EXCEPTION_INTERNAL_ERROR,
        "Failed to find a matching SQL type for the name %s",
        objName.c_str());

    if (sqlType != sqlTypeNames[typeIdx].value)
        errMsg << objName << " type(" << sqlTypeNames[typeIdx].value << "->" << sqlType << ")" << std::endl;
  }

  // Now verify or copy.
  // The value of each element should contain the index that element.
  // This design helps verifying the content of parameters being passed in
  // properly.
  switch (sqlType) 
  {
  // The value of each parameter should contain the index that parameter.
  // This is to help verifying the content of parameters being passed in
  // properly.

  // 16 bit integer (smallint)
  case TypeInfo::SMALLINT: 
  // 32 bit integer (int)
  case TypeInfo::INT: 
  // unsigned 16 bit integer (smallint unsigned)
  case TypeInfo::SMALLINT_UNSIGNED:
  // unsigned 32 bit integer (int unsigned)
  case TypeInfo::INT_UNSIGNED: 
    // 32 bit C++ int
    if (isPar)
    {
      objValueInt = info.par().getInt(inObjIdx);
      wasNull = info.par().wasNull();
    }
    else
    {
      objValueInt = info.in().getInt(inObjIdx);
      wasNull = info.in().wasNull();
    }
  
    if (toVerify)
    {
      if (objValueInt != inObjIdx)
        errMsg << objName << " val(" << inObjIdx << "->" << objValueInt << ")" << std::endl;
    }   
    if (toCopy)
    {
      if (wasNull)
        info.out().setNull(outObjIdx);
      else 
        info.out().setInt(outObjIdx, objValueInt);
    }
    break;

  // 64 bit integer (largeint)
  case TypeInfo::LARGEINT:
    // 64 bit C++ long
    if (isPar)
    {
      objValueLong = info.par().getLong(inObjIdx);
      wasNull = info.par().wasNull();
    }
    else
    {
      objValueLong = info.in().getLong(inObjIdx); 
      wasNull = info.in().wasNull();
    }

    if (toVerify)
    {
      if (objValueLong != inObjIdx)
        errMsg << objName << " val(" << inObjIdx << "->" << objValueLong << ")" << std::endl;
    }
    if (toCopy)
    {
      if (wasNull)
        info.out().setNull(outObjIdx);
      else
        info.out().setLong(outObjIdx, objValueLong);
    }
    break;

  // Numeric with decimal precision (numeric)
  case TypeInfo::NUMERIC: 
  // unsigned numeric (numeric unsigned)
  case TypeInfo::NUMERIC_UNSIGNED:
  // Decimal, leading sign embedded (decimal)
  case TypeInfo::DECIMAL_LSE: 
  // unsigned decimal (decimal unsigned)
  case TypeInfo::DECIMAL_UNSIGNED: 
    // 64 bit C++ long
    if (isPar)
    {
      objValueLong = info.par().getLong(inObjIdx);
      wasNull = info.par().wasNull();
      precision = info.par().getColumn(inObjIdx).getType().getPrecision();
      scale = info.par().getColumn(inObjIdx).getType().getScale();
    }
    else
    {
      objValueLong = info.in().getLong(inObjIdx);
      wasNull = info.in().wasNull();
      precision = info.in().getColumn(inObjIdx).getType().getPrecision();
      scale = info.in().getColumn(inObjIdx).getType().getScale();
    }

    if (toVerify)
    {
      if (precision != 9)
        errMsg << objName << " precision(" << 9 << "->" << precision << ")" << std::endl;

      myFloat = (float) objValueLong;
      if (scale > 0)
      {
        for (k = 0; k < scale; k++)
          myFloat /= 10.0;
      }
  
      expFloat = (float) inObjIdx + (float) inObjIdx / 100.0;
      // Compare the original long value, to avoid inprecise float values.
      if (objValueLong != inObjIdx * 100 + inObjIdx)
        errMsg << objName << " val(" << expFloat << "->" << myFloat << ")" << std::endl;
    }
    if (toCopy)
    {
      if (wasNull)
        info.out().setNull(outObjIdx);
      else
        info.out().setLong(outObjIdx, objValueLong);
    }
    break;
    
  // 8 byte floating point number (float, double precision)
  case TypeInfo::DOUBLE_PRECISION:
  // 4 byte floating point number (real)
  case TypeInfo::REAL:
    // 64 bit C++ double
    if (isPar)
    {
      objValueDouble = info.par().getDouble(inObjIdx);
      wasNull = info.par().wasNull();
    }
    else
    {
      objValueDouble = info.in().getDouble(inObjIdx);
      wasNull = info.in().wasNull();
    }
    if (toVerify)
    {
      if (objValueDouble != inObjIdx)
        errMsg << objName << " val(" << inObjIdx << "->" << objValueDouble << ")" << std::endl;
    }
    if (toCopy)
    {
      if (wasNull)
        info.out().setNull(outObjIdx);
      else
        info.out().setDouble(outObjIdx, objValueDouble);
    }
    break;

  // fixed length character types (char)     
  case TypeInfo::CHAR: 
  // varying length character types (char varing, varchar)
  case TypeInfo::VARCHAR: 
    // C++ std::string, char *
    if (isPar)
    {
      charsetCode = info.par().getType(inObjIdx).getCharset();
      length = info.par().getType(inObjIdx).getByteLength();
      maxCharLength = info.par().getType(inObjIdx).getMaxCharLength();
    }
    else
    {
      charsetCode = info.in().getType(inObjIdx).getCharset();
      length = info.in().getType(inObjIdx).getByteLength();
      maxCharLength = info.in().getType(inObjIdx).getMaxCharLength();
    }

    if (charsetCode == TypeInfo::CHARSET_ISO88591)
    { 
      if (isPar)
      {
        objValueStr = info.par().getString(inObjIdx);
        wasNull = info.par().wasNull();
      }
      else
      {
        objValueStr = info.in().getString(inObjIdx);
        wasNull = info.in().wasNull();
      }
      if (toVerify)
      {
        if (atoi(objValueStr.c_str()) != inObjIdx)
          errMsg << objName << " val(" << inObjIdx << "->" << objValueStr << ")" << std::endl;
      }
      if (toCopy)
      {
        if (wasNull)
          info.out().setNull(outObjIdx);
        else
          info.out().setString(outObjIdx, objValueStr);
      }
    } 
    else // CHARSET_UTF8, CHARSET_UCS2
    {
      if (toVerify)
      {
        if (length > MAX_CHAR_LEN)
          throw UDRException(
            EXCEPTION_INTERNAL_ERROR,
            "Invalid charset length: %d longer than supported value %d",
            length, MAX_CHAR_LEN);

        sprintf(origBuf, "%d", inObjIdx);

        // Fill the entire buffer with 4-byte 'white space': 0x3200
        memset(expBuf, 0, MAX_CHAR_LEN);
        for (j=0; j<MAX_CHAR_LEN/2; j++)
          expBuf[j*2] = 0x32;

        // Now fill in the expected string (padded with 00 in the secnd byte
        // for ASCII bytes)
        for (j=0; j<strlen(origBuf); j++)
          expBuf[j*2] = origBuf[j];  
      
        if (isPar)
          objValueChar = info.par().getRaw(inObjIdx, myLen);
        else
          objValueChar = info.in().getRaw(inObjIdx, myLen);

        if (memcmp(expBuf, objValueChar, strlen(origBuf)*2) != 0)
        {
          tmpBuf2[0] = 0;
          for (j=0; j<strlen(origBuf)*2; j++)
          {
            sprintf (tmpBuf1, "0x%02x ", expBuf[j]);
            strcat (tmpBuf2, tmpBuf1);
          }
          errMsg << objName << " val(" << tmpBuf2 << "->";
          tmpBuf2[0] = 0;
          for (j=0; j<strlen(origBuf)*2; j++)
          {
            sprintf (tmpBuf1, "0x%02x ", objValueChar[j]);
            strcat (tmpBuf2, tmpBuf1);
          }
          errMsg << tmpBuf2 << ")" << std::endl;
        }
      }
      if (toCopy)
      {
        if (isPar)
        {
          objValueChar = info.par().getRaw(inObjIdx, myLen);
          wasNull = info.par().wasNull();
        }
        else
        {
          objValueChar = info.in().getRaw(inObjIdx, myLen);
          wasNull = info.in().wasNull();
        }

        if (wasNull)
          info.out().setNull(outObjIdx);
        else
          info.out().setString(outObjIdx, objValueChar, myLen);
      }
    }
    break;

  case TypeInfo::DATE:
  case TypeInfo::TIME:
  case TypeInfo::TIMESTAMP:
    // C++ std::string
    if (isPar)
    {
      objValueStr = info.par().getString(inObjIdx);
      wasNull = info.par().wasNull();
      scale = info.par().getColumn(inObjIdx).getType().getScale();
    }
    else
    {
      objValueStr = info.in().getString(inObjIdx);
      wasNull = info.in().wasNull();
      scale = info.in().getColumn(inObjIdx).getType().getScale();
    }

    if (toVerify)
    {
      if (sqlTypeNames[typeIdx].value == TypeInfo::DATE)
        sprintf(expBuf, "20%02d-01-01", inObjIdx);
      else if (sqlTypeNames[typeIdx].value == TypeInfo::TIME)
        sprintf(expBuf, "01:01:%02d", inObjIdx);
      else if (sqlTypeNames[typeIdx].value == TypeInfo::TIMESTAMP)
        sprintf(expBuf, "20%02d-01-01 01:01:%02d", inObjIdx, inObjIdx);

      if (scale > 0)
      {
        strcat (expBuf, ".");
        for (k = 0; k < scale; k++)
        {
          sprintf (tmpBuf1, "%d", k+1);
          strcat(expBuf, tmpBuf1);
        }
      }

      if (objValueStr != expBuf)
        errMsg << objName << " val(" << expBuf << "->" << objValueStr << ")" << std::endl;
    }
    if (toCopy)
    {
      if (wasNull)
        info.out().setNull(outObjIdx);
      else
        info.out().setString(outObjIdx, objValueStr);
    }
    break;
 
  case TypeInfo::INTERVAL:
    // C++ std::string
    if (isPar)
    {
      objValueLong = info.par().getLong(inObjIdx);
      wasNull = info.par().wasNull();
      intervalCode = info.par().getColumn(inObjIdx).getType().getIntervalCode();
    }
    else
    {
      objValueLong = info.in().getLong(inObjIdx);
      wasNull = info.in().wasNull();
      intervalCode = info.in().getColumn(inObjIdx).getType().getIntervalCode();
    }

    // This is the only interval type that the testts use.
    if (intervalCode != TypeInfo::INTERVAL_YEAR_MONTH)
      throw UDRException(
        EXCEPTION_INTERNAL_ERROR,
        "Invalid interval type: expect only TypeInfo::INTERVAL_YEAR_MONTH, got %d", intervalCode);

    if (toVerify)
    {
      // the test always uses year-01 for the year-month interval
      if (objValueLong != inObjIdx * 12 + 1)
        errMsg << objName << " val(" << inObjIdx * 12 + 1 << "->" << objValueLong << ")" << std::endl;
    }
    if (toCopy)
    {
      if (wasNull)
        info.out().setNull(outObjIdx);
      else
        info.out().setLong(outObjIdx, objValueLong);
    }
    break;
 
  default:
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Unhandled type value %d",
      sqlTypeNames[typeIdx].value);
  }
}

// Individual run time test case: parameter values and types
void QATmudf::testRunTimeInParmDataAndTypes(UDRInvocationInfo &info)
{
  int objIdx, numParms;
  std::stringstream errMsg;
  errMsg.str("");
  errMsg.clear();

  // info.par().getNumColumns() include test_what and tset_parm
  numParms = atoi(testParm.c_str());
  if (info.par().getNumColumns() != numParms)
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of input parameters: expecting %d, got %d",
       numParms, info.par().getNumColumns()-2);

  // The first 2 params are test_what and test_parm, hence starting from 2
  for (objIdx = 2; objIdx < numParms; objIdx++)
    verifyElementData(info, objIdx, objIdx-2, true /* isPar */, errMsg);

  if (errMsg.str() != "")
    throw UDRException(
      EXCEPTION_TEST_ERROR,
      "Wrong types or values:\n%s",
      errMsg.str().c_str());

  // This test will let the default implementation returns the same input
  // table as the output table, nothing to be done here. 
}


// internal helper routine
void QATmudf::verifyElementNameAndIndex(UDRInvocationInfo &info, 
                                        int objIdx,
                                        bool isPar)
{
  int myIdx;
  std::string myName, objName; 

  if (isPar)
  {
    myName = info.par().getColumn(objIdx).getColName();
    myIdx = info.par().getColNum(myName);
  }
  else
  {
    myName = info.in().getColumn(objIdx).getColName();
    myIdx = info.in().getColNum(myName);
  }

  if (myIdx != objIdx)
    throw UDRException(
      EXCEPTION_TEST_ERROR,
      "Invalid (idx, name): expect (%d %s), got (%d %s)",
      objIdx, myName.c_str(), myIdx, myName.c_str());
}

// Individual run time test case: parameter names and indexes
void QATmudf::testRunTimeInParmNamesAndIndexes(UDRInvocationInfo &info)
{
  int objIdx, numParms;

  numParms = atoi(testParm.c_str());
  if (info.par().getNumColumns() != numParms)
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of input parameters: expecting testWhat, testParm, %d <user specified parameters>, got %d",
       numParms-2, info.par().getNumColumns());

  for (objIdx = 0; objIdx < numParms; objIdx++)
    verifyElementNameAndIndex(info, objIdx, true);
}


// Individual run time test case: table column names and indexes
void QATmudf::testRunTimeInTableNamesAndIndexes(UDRInvocationInfo &info)
{
  int objIdx, numTableCols;

  numTableCols = atoi(testParm.c_str());
  if (info.in().getNumColumns() != numTableCols)
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of input table columns: expect %d, got %d",
       numTableCols, info.in().getNumColumns());

  for (objIdx = 0; objIdx < numTableCols; objIdx++)
    verifyElementNameAndIndex(info, objIdx, false);
}


// Individual run time test case: table column values and types
void QATmudf::testRunTimeInTableDataAndTypes(UDRInvocationInfo &info)
{
  int objIdx, numTableCols;
  std::stringstream errMsg;
  errMsg.str("");
  errMsg.clear();

  // The input table should ohave only one row.  Go get that row
  if (! getNextRow(info))
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Fail to fetch the row from the table");

  numTableCols = atoi(testParm.c_str());
  if (info.in().getNumColumns() != numTableCols)
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of input table columns: expect %d, got %d",
       numTableCols, info.in().getNumColumns());

  for (objIdx = 0; objIdx < numTableCols; objIdx++)
    verifyAndCopyElementData(info, objIdx, objIdx, false /* isPar */, errMsg);

  if (errMsg.str() != "")
    throw UDRException(
      EXCEPTION_TEST_ERROR,
      "Wrong types or values:\n%s",
      errMsg.str().c_str());
  
  // emit that row back
  emitRow(info);

  // This test only expect a one-row table.
  if (getNextRow(info))
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Input table has more than one row; test expects a one-row table");
}


// Individual run time test case: table partitioning
void QATmudf::testRunTimeInOutTablePartitioning(UDRInvocationInfo &info)
{
  int i, objIdx, numPartKeys;
  std::stringstream errMsg;
  errMsg.str("");
  errMsg.clear();

  // The input table should have only one row.  Go get that row.
  if (! getNextRow(info))
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Fail to fetch the row from the table");

  numPartKeys = atoi(testParm.c_str());
  if (numPartKeys != info.in().getQueryPartitioning().getNumEntries())
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of partitioning keys: expect %d, got %d",
       numPartKeys, info.in().getQueryPartitioning().getNumEntries());

  // The list of partitioning keys used by the test would match exactly the
  // column list of the input table.  Therefore, by copying the entire
  // partitioning keys to the output table, we are expecting to see the 
  // output table to be the same as the input table for the verification
  // purpose.
  for (i = 0; i < numPartKeys; i++)
  {
    objIdx = info.in().getQueryPartitioning().getColumnNum(i);
    verifyAndCopyElementData(info, objIdx, objIdx, false /* isPar */, errMsg);
  }

  if (errMsg.str() != "")
    throw UDRException(
      EXCEPTION_TEST_ERROR,
      "Wrong types or values:\n%s",
      errMsg.str().c_str());

  // emit that row back
  emitRow(info);

  // This test only expect a one-row table.
  if (getNextRow(info))
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Input table has more than one row; test expects a one-row table");
}


// Individual run time test case: table partitioning
void QATmudf::testRunTimeInOutTableOrdering(UDRInvocationInfo &info)
{
  int i, objIdx, numOrderKeys;
  std::stringstream errMsg;
  errMsg.str("");
  errMsg.clear();

  // The input table should ohave only one row.  Go get that row
  if (! getNextRow(info))
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Fail to fetch the row from the table");

  numOrderKeys = atoi(testParm.c_str());
  if (numOrderKeys != info.in().getQueryOrdering().getNumEntries())
    throw UDRException(
       EXCEPTION_INTERNAL_ERROR,
       "Invalid number of ordering keys: expect %d, got %d",
       numOrderKeys, info.in().getQueryOrdering().getNumEntries());

  // The list of ordering keys used by the test would match exactly the
  // column list of the input table.  Therefore, by copying the entire
  // ordering keys to the output table, we are expecting to see the
  // output table to be the same as the input table for the verification
  // purpose.
  for (i = 0; i < numOrderKeys; i++)
  {
    objIdx = info.in().getQueryOrdering().getColumnNum(i);
    verifyAndCopyElementData(info, objIdx, objIdx, false /* isPar */, errMsg);
  }

  if (errMsg.str() != "")
    throw UDRException(
      EXCEPTION_TEST_ERROR,
      "Wrong types or values:\n%s",
      errMsg.str().c_str());

  // emit that row back
  emitRow(info);

  // This test only expect a one-row table.
  if (getNextRow(info))
    throw UDRException(
      EXCEPTION_INTERNAL_ERROR,
      "Input table has more than one row; test expects a one-row table");
}


// Individual run time test case: table columns.
// testCmpTimeOutTable() does part I at the compile time.
// testRunTimeOutTable() does part II at the run time.
void QATmudf::testRunTimeOutTable(UDRInvocationInfo &info, bool usePassThru)
{
  int objIdx;
  std::stringstream errMsg;
  errMsg.str("");
  errMsg.clear();

  // loop over input rows
  while (getNextRow(info))
  {
    if (usePassThru)
    {
      info.copyPassThruData();
    }
    else
    {
      for (objIdx = 0; objIdx < info.in().getNumColumns(); objIdx++)
        copyElementData(info, objIdx, objIdx, false /* isPar */, errMsg);

      if (errMsg.str() != "")
        throw UDRException(
          EXCEPTION_TEST_ERROR,
          "Wrong types or values:\n%s",
          errMsg.str().c_str());
    }

    emitRow(info);
  }
}


