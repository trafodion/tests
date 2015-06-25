/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

// COAST.cpp : Defines the entry point for the console application.
//
#include <stdlib.h>    
#include <stdio.h> 
#include <string.h>
#include <windows.h>
#include <sqlext.h>
#include <assert.h>
#include <time.h>
#include "common.h"
#include "log.h"
#include "apitests.h"
#include "getopt.h"

#define RUNALL	1
#define RUNFILE	2
#define RUNAPI	3
#define	ARGS	"d:u:p:l:c:f:m:r:"   //Modified for Longvarchar changes - Added 'l' option

TestInfo		*pTestInfo;
char *DSN;//[100];
char *USR;//[100];
char *PWD;//[100];
char *charset;
char *strapi;//[100];
char *strOption;//[100];
char *inputfile;//[100];
char *machine = "local";
FILE *scriptFD = NULL;
time_t start, end;

char *charset_filenames[] = {"charset_ascii.char",
							 "charset_sjis.char",
							 "charset_big5.char",
							 "charset_gb2.char",
							 "charset_gb1.char",
							 "charset_ksc.char",
							 "charset_eucjp.char",
							 "charset_latin1.char"
						 };

bool m_AllApi				= FALSE;

// ODBC 2.x APIs
bool m_AllocEnv				= FALSE;
bool m_AllocConnect			= FALSE;
bool m_BindParameter		= FALSE;
bool m_BrowseConnect		= FALSE;
bool m_Cancel				= FALSE;
bool m_ColAttrib			= FALSE;
bool m_Connect				= FALSE;
bool m_DataSources			= FALSE;
bool m_DesCols 				= FALSE;
bool m_DriverConnect		= FALSE;
bool m_Drivers				= FALSE;
bool m_Error				= FALSE;
bool m_ExecDirect			= FALSE;
bool m_Execute				= FALSE;
bool m_ExtendedFetch		= FALSE;
bool m_Fetch 				= FALSE;
bool m_GetData				= FALSE;
bool m_PutData				= FALSE;
bool m_GetFunctions			= FALSE;
bool m_GetInfo				= FALSE;
bool m_MoreResults			= FALSE;
bool m_AllocStmt			= FALSE;
bool m_BindCol				= FALSE;
bool m_Columns				= FALSE;
bool m_DescribeParam		= FALSE;
bool m_GetTypeInfo			= FALSE;
bool m_PrimaryKeys			= FALSE;
bool m_ResGovern			= FALSE;
bool m_SetConnectOption		= FALSE;
bool m_SetCursorName		= FALSE;
bool m_SetStmtOption		= FALSE;
bool m_SpecialColumns		= FALSE;
bool m_Statistics			= FALSE;
bool m_Tables				= FALSE;
bool m_NativeSql			= FALSE;
bool m_NumParams			= FALSE;
bool m_NumResultCols		= FALSE;
bool m_Prepare				= FALSE;
bool m_RowCount				= FALSE;
bool m_Transact				= FALSE;

//ODBC 3.0 APIs

bool m_AllocHandle30			= FALSE;
bool m_BindCol30				= FALSE;
bool m_BindParameter30			= FALSE;
bool m_CloseCursor30			= FALSE;
bool m_ColAttributes30			= FALSE;
bool m_CopyDesc30				= FALSE;
bool m_DescribeCol30			= FALSE;
bool m_EndTran30				= FALSE;
bool m_GetConnectAttr30			= FALSE;
bool m_GetData30				= FALSE;
bool m_SetGetDescFields30		= FALSE;
bool m_GetDescRec30				= FALSE;
bool m_GetDiagField30			= FALSE;
bool m_GetDiagRec30				= FALSE;
bool m_GetEnvAttr30				= FALSE;
bool m_GetInfo30				= FALSE;
bool m_GetStmtAttr30			= FALSE;
bool m_MoreResults30			= FALSE;
//bool m_PartialDateTimeInput	= FALSE;
//bool m_PartialDateTimeOutput	= FALSE;
bool m_BindParamInterval30		= FALSE;
bool m_GetTypeInfo30R18			= FALSE;
bool m_ProcedureColumns30		= FALSE;
bool m_Procedures30				= FALSE;
bool m_FetchScroll30			= FALSE;
bool m_ForeignKeys30			= FALSE;
bool m_BindColInterval30		= FALSE;
bool m_GetDataInterval30		= FALSE;
bool m_ColumnPrivileges30		= FALSE;
bool m_TablePrivileges30		= FALSE;
bool m_Unicode30				= FALSE;

// TRAF and NDCS Features
bool m_QueryID					= FALSE;
bool m_Hash2					= FALSE;
bool m_LargeBlock				= FALSE;
bool m_InfoStats                = FALSE;

BOOL FlagLongVarchar = FALSE; //Modified for Longvarhcar Changes


int iRunOption = 0;

int Run20Tests ();
int Run21Tests ();
int	Run30Tests ();
void MapApiNameToFlag(char *);
void ReadSelectedTests(char *);

int main(int argc, char* argv[])
{
	//process command line params
	int c, errflag = 0;
//	char temp[256];

	optarg = NULL;
	if (argc < 3 || argc > 16) //Modified for Longvarhcar Changes //if (argc < 2 || argc > 14)
		errflag++;

	while (!errflag && (c = getopt_c(argc, argv, ARGS)) != -1)
		switch (c) {
			case 'd':
				DSN = optarg;	
				break;
			case 'u':
				USR = optarg;
				break;
			case 'p':
				PWD = optarg;
				break;
			case 'l':  //Case Added for Longvarchar Changes
				strOption = optarg;
				if(!stricmp(strOption,"ON"))
					FlagLongVarchar = TRUE;
				else 
					FlagLongVarchar = FALSE;
				break;
			case 'f':
				strOption = optarg;
				if (!stricmp(strOption,"FILE"))
				{
					iRunOption = RUNFILE;
					inputfile = secondarg;
                    strapi = (char*)"FILE";
				}
				else if (!stricmp(strOption,"API"))
				{
					iRunOption = RUNAPI;
					strapi = secondarg;
				}
				else if (!stricmp(strOption,"ALL"))
				{
					strapi = strOption;
					iRunOption = RUNALL;
				}
				break;
			case 'c':
				charset = optarg;
				if (!stricmp(charset,"ASCII")) {
					strcpy(charset_file,charset_filenames[0]);
				} else {
					isCharSet = TRUE;
					if (!stricmp(charset,"SJIS"))
						strcpy(charset_file,charset_filenames[1]);
					else if (!stricmp(charset,"BIG5")) {
						strcpy(charset_file,charset_filenames[2]);
					}
					else if (!stricmp(charset,"GB2")) {
						strcpy(charset_file,charset_filenames[3]);
					}
					else if (!stricmp(charset,"GB1")) {
						strcpy(charset_file,charset_filenames[4]);
					}
					else if (!stricmp(charset,"KSC")) {
						strcpy(charset_file,charset_filenames[5]);
					}
					else if (!stricmp(charset,"EUCJP")) {
						strcpy(charset_file,charset_filenames[6]);
					}
					else if (!stricmp(charset,"LATIN1")) {
						strcpy(charset_file,charset_filenames[7]);
					}
					else {
						errflag++;
					}
				}
				break;
			case 'm':
				machine = optarg;
				break;
			case 'r':
				secondaryRole = optarg;
				break;
			default :
				errflag++;
				break;
		}
	if (errflag) {
		printf("Usage: %s [-d <datasource>] [-u <userid>] [-p <password>] [-c <ASCII|SJIS|BIG5|GB1|GB2|KSC|EJCJP|LATIN1>] [-f <ALL|API api_name|FILE file_name>] [-m <machine_name>\n"
				"Or:   %s [-d <datasource>]\n"
				"   where default userID is 'odbcqa' and default password is 'odbcqa' with default character set is 'ASCII'\n", argv[0], argv[0] );
		return FALSE;
	}

	if(!USR)
		USR = (char*)"odbcqa";
	if(!PWD)
		PWD = (char*)"odbcqa";
	if(!charset) {
		charset = (char*)"ASCII";
		strcpy(charset_file,charset_filenames[0]);
	}
	if(!strOption) {
		iRunOption = RUNALL;
		strapi = (char*)"ALL";
	}

//#ifndef unixcli
//	if ((scriptFD = fopen(charset_file, "r")) == NULL) {
//		//strcpy(temp, "..\\..\\..\\src\\");
//		sprintf(temp, ".\\%s", charset_file);
//		strcpy(charset_file, temp);
//
//		if ((scriptFD = fopen(charset_file, "r")) == NULL) {
//			printf("Error open textfile %s\n", charset_file);
//			return FALSE;
//		}
//	}
//	fclose(scriptFD);
//	printf("Loaded textfile from: %s\n", charset_file);
//#endif

    pTestInfo	= new TestInfo;

	strcpy (pTestInfo->DataSource,(const char *)DSN);
	strcpy (pTestInfo->UserID,(const char *)USR);
	strcpy (pTestInfo->Password,(const char *)PWD);
	pTestInfo->bLongOn = FlagLongVarchar; // Modified for Longvarchar changes

	switch (iRunOption)
	{
		case RUNALL:
			m_AllApi = true;
			break;
		case RUNAPI:
			MapApiNameToFlag((char *)strapi);
			break;
		case RUNFILE:
			ReadSelectedTests((char *)inputfile);
			break;
	}

	// initialization added (RS) to prevent some runtime errors with the debug version
	pTestInfo->henv = (SQLHANDLE) NULL;
	pTestInfo->hstmt =(SQLHANDLE) NULL;
	pTestInfo->hdbc = (SQLHANDLE) NULL;
	
     
	// Initialize the log file
	char buff[1024];
	char timebuf[256];

	time_t my_clock = time( NULL);
    strftime( timebuf, 256, "%Y-%m-%d_%H.%M.%S", localtime( &my_clock ) );
	while (true) {
		#ifdef unixcli
			sprintf(buff, "%s/coast_%s.%s.%s.%s.%s.log", (char*)".", timebuf, charset, strapi, machine, DSN);
		#else
			sprintf(buff, "%s\\coast.%s.%s.%s.%s.%s.log", (char*)".", timebuf, charset, strapi, machine, DSN);
		#endif /* WIN32 */

		FILE *myFile;
		myFile = fopen (buff,"r");
		if (myFile == NULL)
			break;
		fclose (myFile);
	}

	LogInit(buff,3,"***ERROR: ");

	// need to get initial values for DSN, UID, and Password and set
	// the values in the Testinfo structure so all tests can use these
	if(!DriverConnectNoPrompt(pTestInfo)){
		LogMsg(ERRMSG+LINEBEFORE+LINEAFTER,
			"Unable to establish an initial connection.  No tests can be executed.\n");
		delete pTestInfo;
		return 0;
	}

	LogInfo (pTestInfo);
       
	FullDisconnect(pTestInfo);

	g_Trace=TRUE;
	pTestInfo->Trace=TRUE;

	Run20Tests();
	Run21Tests();
	Run30Tests();

	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Total Tests=%d  Failed=%d\n",_gTestCount,_gTestFailedCount);
	printf ("Total Tests=%d  Failed=%d\r\n",_gTestCount,_gTestFailedCount);
	//puts ("Results logged in file: ");
	//puts (buff);
	puts ("\r\nHave a good day! \r\n");

	delete pTestInfo;

	return 0;
}

int Run20Tests()
{
	// Execute the selected tests
	// (as you add 'if' statements for each procedure to be tested
	//  try and keep them in alphabetical order so it is a bit 
	//  easier to find things)
	pTestInfo->Trace=FALSE;

	if (m_AllApi)
	{
		m_AllocEnv		= TRUE;
		m_AllocConnect	= TRUE;
		m_BrowseConnect = TRUE;
		m_Connect		= TRUE;
		m_DataSources	= TRUE;
		m_DriverConnect	= TRUE;
		m_Drivers		= TRUE;
		m_Error			= TRUE;
		m_ExecDirect	= TRUE;
		m_ExtendedFetch	= TRUE;
		m_Fetch			= TRUE;
		m_GetFunctions	= TRUE;
		m_MoreResults	= TRUE;
		m_NativeSql		= TRUE;
		m_NumParams		= TRUE;
		m_NumResultCols	= TRUE;
		m_Prepare		= TRUE;
		m_RowCount		= TRUE;
		m_Transact		= TRUE;
	}
	
	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Starting ODBC 2.0 tests...\n");
	puts ("Starting ODBC 2.0 tests...");
	if (m_AllocEnv)
	{
		puts ("Running AllocEnv API.\r\n");
		start = time( NULL);
		TestSQLAllocEnv(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLAllocEnv (2.0)");
	}
	if (m_AllocConnect)
	{
		puts("Running AllocConnect API.\r\n");
		start = time( NULL);
		TestSQLAllocConnect(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLAllocConnect (2.0)");
	}
	if (m_BrowseConnect)
	{
		puts("Running BrowseConnect API.\r\n");
		start = time( NULL);
		TestSQLBrowseConnect(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBrowseConnect (2.0)");
	}
	if (m_Connect)				
	{
		puts("Running Connect API.\r\n");
		start = time( NULL);
		TestSQLConnect(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLConnect (2.0)");
	}
	if (m_DataSources)
	{
		puts("Running DataSources API.\r\n");
		start = time( NULL);
		TestSQLDataSources(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLDataSources (2.0)");
	}
	if (m_DriverConnect)
	{
		puts("Running DriveConnect API.\r\n");
		start = time( NULL);
		TestSQLDriverConnect(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLDriverConnect (2.0)");
	}
	if (m_Drivers)
	{
		puts("Running Drivers API.\r\n");
		start = time( NULL);
		TestSQLDrivers(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLDrivers (2.0)");
	}
	if (m_Error)
	{
		puts("Running Error API.\r\n");
		start = time( NULL);
		TestSQLError(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLError (2.0)");
	}
	if (m_ExecDirect)			
	{
		puts("Running ExecDirect API.\r\n");
		start = time( NULL);
		TestSQLExecDirect(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLExecDirect (2.0)");
	}
	if (m_ExtendedFetch)				
	{
		puts("Running ExtendedFetch API.\r\n");
		start = time( NULL);
		TestSQLExtendedFetch(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLExtendedFetch (2.0)");
	}
	if (m_Fetch)				
	{
		puts("Running Fetch API.\r\n");
		start = time( NULL);
		TestSQLFetch(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLFetch (2.0)");
	}
	if (m_GetFunctions)		
	{
		puts("Running GetFunctions API.\r\n");
		start = time( NULL);
		TestSQLGetFunctions(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetFunctions (2.0)");
	}
	if (m_MoreResults)		
	{
		puts("Running MoreResults API.\r\n");
		start = time( NULL);
		TestSQLMoreResults(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLMoreResults (2.0)");
	}
	if (m_NativeSql)			
	{
		puts("Running NativeSql API.\r\n");
		start = time( NULL);
		TestSQLNativeSql(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLNativeSql (2.0)");
	}
	if (m_NumParams)			
	{
		puts("Running NumParams API.\r\n");
		start = time( NULL);
		TestSQLNumParams(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLNumParams (2.0)");
	}
	if (m_NumResultCols)		
	{
		puts("Running NumResultCols API.\r\n");
		start = time( NULL);
		TestSQLNumResultCols(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLNumResultCols (2.0)");
	}
	if (m_Prepare)				
	{
		puts("Running Prepare API.\r\n");
		start = time( NULL);
		TestSQLPrepare(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLPrepare (2.0)");
	}
	if (m_RowCount)			
	{
		puts("Running RowCount API.\r\n");
		start = time( NULL);
		TestSQLRowCount(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLRowCount (2.0)");
	}
	if (m_Transact)			
	{
		puts("Running Transact API.\r\n");
		start = time( NULL);
		TestSQLTransact(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLTransact (2.0)");
	}

	// Display statistics for tests ran
	//LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Total Tests=%d  Failed=%d\n",_gTestCount,_gTestFailedCount);

	return 0;
}

int Run21Tests ()
{
	pTestInfo->Trace = FALSE;
	g_Trace=FALSE;

	if (m_AllApi)
	{
		m_AllocStmt			= TRUE;
		m_BindCol			= TRUE;
		m_BindParameter		= TRUE;
		m_Cancel			= TRUE;
		m_ColAttrib			= TRUE;
		m_Columns			= TRUE;
		m_DesCols			= TRUE;
		m_DescribeParam		= TRUE;
		m_Execute			= TRUE;
		m_GetData			= TRUE;
		m_PutData			= TRUE;
		m_GetInfo			= TRUE;
		m_GetTypeInfo		= TRUE;
		m_PrimaryKeys		= TRUE;
		m_SetConnectOption	= TRUE;
		m_SetCursorName		= TRUE;
		m_SetStmtOption		= TRUE;
		m_SpecialColumns	= TRUE;
		m_Statistics		= TRUE;
		m_Tables			= TRUE;
		m_ResGovern			= TRUE;
	}

	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Starting ODBC 2.1 tests...\n");
	puts("Starting ODBC 2.1 tests...");
	if (m_AllocStmt)
	{
		puts("Running MX 2.10 AllocStmt API.\r\n");
		start = time( NULL);
		TestSQLAllocStmt(pTestInfo, MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLAllocStmt (2.1)");
	}

	if (m_BindCol)			
	{
		puts("Running MX 2.10 SQLBindCol API.\r\n");
		start = time( NULL);
		TestMXSQLBindCol(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBindCol (2.1)");
	}
	if (m_BindParameter)			
	{
		puts("Running MX 2.10 SQLBindParameter API.\r\n");
		start = time( NULL);
		TestMXSQLBindParameter(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBindParameter (2.1)");
	}
	
	if (m_Cancel)			
	{
		puts("Running MX 2.10 SQLCancel API.\r\n");
		start = time( NULL);
		TestMXSQLCancel(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLCancel (2.1)");
	}
	
	if (m_ColAttrib)			
	{
		puts("Running MX 2.10 SQLColumnAttributes API.\r\n");
		start = time( NULL);
		TestMXSQLColAttributes(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLColumnAttributes (2.1)");
	}
	if (m_Columns)			
	{
		puts("Running MX 2.10 SQLColumns API.\r\n");
		start = time( NULL);
		TestMXSQLColumns(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLColumns (2.1)");
	}
	if (m_DesCols)			
	{
		puts("Running MX 2.10 SQLDescribeColumns API.\r\n");
		start = time( NULL);
		TestMXSQLDescribeCol(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLDescribeColumns (2.1)");
	}
	if (m_DescribeParam)			
	{
		puts("Running MX 2.10 SQLDescribeParam API.\r\n");
		start = time( NULL);
		TestSQLDescribeParam(pTestInfo,MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLDescribeParam (2.1)");
	}
	if (m_Execute)			
	{
		puts("Running MX 2.10 SQLExecute API.\r\n");
		start = time( NULL);
		TestSQLExecute(pTestInfo,MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLExecute (2.1)");
	}
	if (m_GetData)			
	{
		puts("Running MX 2.10 SQLGetData API.\r\n");
		start = time( NULL);
		TestMXSQLGetData(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetData (2.1)");
	}
	if (m_PutData)			
	{
		puts("Running MX 2.10 SQLPutData API.\r\n");
		start = time( NULL);
		TestMXSQLPutData(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLPutData (2.1)");
	}
	if (m_GetInfo)			
	{
		puts("Running MX 2.10 SQLGetInfo API.\r\n");
		start = time( NULL);
		TestMXSQLGetInfo(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetInfo (2.1)");
	}
	if (m_GetTypeInfo)			
	{
		puts("Running MX 2.10 SQLGetTypeInfo API.\r\n");
		start = time( NULL);
		TestSQLGetTypeInfo(pTestInfo,MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetTypeInfo (2.1)");
	}
	if (m_PrimaryKeys)
	{
		puts("Running MX 2.10 SQLPrimaryKeys API.\r\n");
		start = time( NULL);
		TestSQLPrimaryKeys(pTestInfo,MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLPrimaryKeys (2.1)");
	}
	if (m_SetConnectOption)
	{
		puts("Running MX 2.10 SQLSet/GetConnectOption API.\r\n");
		start = time( NULL);
		TestSQLSetConnectOption(pTestInfo, MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetConnectOption (2.1)");
	}
	if (m_SetCursorName)
	{
		puts("Running MX 2.10 SQLSet/GetCursorName API.\r\n");
		start = time( NULL);
		TestSQLSetCursorName(pTestInfo, MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetCursorName (2.1)");
	}
	if (m_SetStmtOption)
	{
		puts("Running MX 2.10 SQLSet/GetStmtOption API.\r\n");
		start = time( NULL);
		TestSQLSetStmtOption(pTestInfo, MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetStmtOption (2.1)");
	}
	if (m_SpecialColumns)	
	{
		puts("Running MX 2.10 SQLSpecialColumns API.\r\n");
		start = time( NULL);
		TestSQLSpecialColumns(pTestInfo, MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSpecialColumns (2.1)");
	}
	if (m_Statistics)			
	{
		puts("Running MX 2.10 SQLStatistics API.\r\n");
		start = time( NULL);
		TestSQLStatistics(pTestInfo, MX_SPECIFIC);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLStatistics (2.1)");
	}
	if (m_Tables)			
	{
		puts("Running MX 2.10 SQLTables API.\r\n");
		start = time( NULL);
		TestMXSQLTables(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLTables (2.1)");
	}
	if (m_ResGovern)			
	{
		puts("Running MX 2.10 Resource Governing.\r\n");
		start = time( NULL);
		TestMXResourceGovern(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("Resource Governing (2.1)");
	}
	
	// Display statistics for tests ran
	//LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Total Tests=%d  Failed=%d\n",_gTestCount,_gTestFailedCount);
	return 0;
}

int	Run30Tests ()
{
	g_Trace=FALSE;
	pTestInfo->Trace=FALSE;

	if (m_AllApi)
	{
		m_AllocHandle30 = TRUE;
		m_BindCol30 = TRUE;
		m_GetConnectAttr30 = TRUE;
		m_EndTran30 = TRUE;
		m_CloseCursor30 = TRUE;
		m_CopyDesc30 = TRUE;
		m_GetDescRec30 = TRUE;	//also tests SQLSetDescRec
		m_GetEnvAttr30 = TRUE;
		m_GetData30 = TRUE;
		m_GetDiagRec30 = TRUE;
		m_GetDiagField30 = TRUE;
		m_BindParameter30 = TRUE;
		m_DescribeCol30 = TRUE;
		m_GetInfo30 = TRUE;
		m_MoreResults30 = TRUE;
		m_SetGetDescFields30 = TRUE;
		m_GetStmtAttr30 = TRUE;
		m_ColAttributes30 = TRUE;
		m_GetTypeInfo30R18 = TRUE;
		m_FetchScroll30 = TRUE;
		m_ForeignKeys30 = TRUE;
		m_ColumnPrivileges30 = TRUE;
		m_TablePrivileges30 = TRUE;

		// Interval Data Type Tests
		m_BindColInterval30 = TRUE;
		m_GetDataInterval30 = TRUE;
		m_BindParamInterval30 = TRUE;
		m_Unicode30 = TRUE;

		// Stored Procedures
		m_ProcedureColumns30 = TRUE;
		m_Procedures30 = TRUE;

		// Partial Date Time Conversions
		//m_PartialDateTimeInput30 = TRUE;
		//m_PartialDateTimeOutput30 = TRUE;

		// TRAF and NDCS Features
		m_QueryID = TRUE;
		m_Hash2 = TRUE;
		m_LargeBlock = TRUE;
        m_InfoStats = TRUE;
	}

	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Starting ODBC 3.0 tests...\n");
	puts("Starting ODBC 3.0 tests...");

	if (m_AllocHandle30)
	{
		puts("Running MX 3.0 AllocHandle API.\r\n");
		start = time( NULL);
		TestMXSQLAllocHandle(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLAllocHandle (3.0)");
	}
	if (m_BindCol30)			
	{
		puts("Running MX 3.0 SQLBindCol API.\r\n");
		start = time( NULL);
		TestMXSQLBindColVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBindCol (3.0)");
	}
	if (m_GetConnectAttr30)
	{
		puts("Running MX 3.0 SetConnectAttr/GetConnectAttr API.\r\n");
		start = time( NULL);
		TestMXSQLSetConnectAttr(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetConnectAttr (3.0)");
	}
	if (m_EndTran30)
	{
		puts("Running MX 3.0 EndTran API.\r\n");
		start = time( NULL);
		TestMXSQLEndTran(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLEndTran (3.0)");
	}
	if (m_CloseCursor30)
	{
		puts("Running MX 3.0 CloseCursor API.\r\n");
		start = time( NULL);
		TestMXSQLCloseCursor(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLCloseCursor (3.0)");
	}
	if (m_CopyDesc30)
	{
		puts("Running MX 3.0 CopyDesc API.\r\n");
		start = time( NULL);
		TestMXSQLCopyDesc(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLCopyDesc (3.0)");
	}
	if (m_GetData30)			
	{
		puts("Running MX 3.0 SQLGetData API.\r\n");
		start = time( NULL);
		TestMXSQLGetDataVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetData (3.0)");
	}
	if (m_GetDescRec30)
	{
		puts("Running MX 3.0 GetDescRec API.\r\n");
		start = time( NULL);
		TestMXSQLGetDescRec(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetDescRec (3.0)");
	}
	if (m_GetEnvAttr30)
	{
		puts("Running MX 3.0 Set/GetEnvAttr API.\r\n");
		start = time( NULL);
		TestMXSQLSetEnvAttr(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetEnvAttr (3.0)");
	}
	if (m_GetDiagRec30)
	{
		puts("Running MX 3.0 GetDiagRec API.\r\n");
		start = time( NULL);
		TestMXSQLGetDiagRec(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetDiagRec (3.0)");
	}
	if (m_GetDiagField30)
	{
		puts("Running MX 3.0 GetDiagField API.\r\n");
		start = time( NULL);
		TestMXSQLGetDiagField(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetDiagField (3.0)");
	}
	if (m_GetStmtAttr30)
	{
		puts("Running MX 3.0 Set/GetStmtAttr API.\r\n");
		start = time( NULL);
		TestMXSQLSetStmtAttr(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetStmtAttr (3.0)");
	}
	if (m_ColAttributes30)
	{
		puts("Running MX 3.0 ColAttribute API.\r\n");
		start = time( NULL);
		TestMXSQLColAttributeVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLColAttribute (3.0)");
	}
	if (m_BindParameter30)
	{
		puts("Running MX 3.0 BindParameter API.\r\n");
		start = time( NULL);
		TestMXSQLBindParameterVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBindParameter (3.0)");
	}
	if (m_DescribeCol30)
	{
		puts("Running MX 3.0 DescribeCol API.\r\n");
		start = time( NULL);
		TestMXSQLDescribeColVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLDescribeCol (3.0)");
	}
	if (m_FetchScroll30)			
	{
		puts("Running MX 3.0 SQLFetchScroll API.\r\n");
		start = time( NULL);
		TestMXSQLFetchScroll(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLFetchScroll (3.0)");
	}
	if (m_GetInfo30)
	{
		puts("Running MX 3.0 GetInfo API.\r\n");
		start = time( NULL);
		TestMXSQLGetInfoVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetInfo (3.0)");
	}
	if (m_MoreResults30)
	{
		puts("Running MX 3.0 MoreResults API.\r\n");
		start = time( NULL);
		TestSQLMoreResultsVer3(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLMoreResults (3.0)");
	}
	if (m_SetGetDescFields30)
	{
		puts("Running MX 3.0 Set and Get DescFields APIs.\r\n");
		start = time( NULL);
		TestMXSQLSetGetDescFields(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLSet/GetDescFields (3.0)");
	}
	if (m_GetTypeInfo30R18)			
	{
		puts("Running MX 3.0 SQLGetTypeInfo API for R1.8.\r\n");
		start = time( NULL);
		TestSQLGetTypeInfoR18(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetTypeInfo (3.0)");
	}
	if (m_ColumnPrivileges30)			
	{
		puts("Running MX 3.0 SQLColumnPrivileges API.\r\n");
		start = time( NULL);
		TestMXSQLColumnPrivileges(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLColumnPrivileges (3.0)");
    }
	
	// Interval Data Type Tests
	if (m_BindParamInterval30)
	{
		puts("Running MX 3.0 Interval BindParam API.\r\n");
		start = time( NULL);
		TestMXSQLBindParameterInterval(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBindParameter - Interval (3.0)");
	}
	if (m_BindColInterval30)
	{
		puts("Running MX 3.0 Interval BindCol API.\r\n");
		start = time( NULL);
		TestMXSQLBindColInterval(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLBindCol - Interval (3.0)");
	}
	if (m_GetDataInterval30)
	{
		puts("Running MX 3.0 Interval GetData API.\r\n");
		start = time( NULL);
		TestMXSQLGetDataInterval(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLGetData - interval (3.0)");
	}
	if (m_ProcedureColumns30)	
	{
		puts("Running MX 3.0 ProcedureColumns API.\r\n");
		start = time( NULL);
		TestMXSQLProcedureColumns(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLProcedureColumns (3.0)");
	}
	if (m_Procedures30)			
	{
		puts("Running MX 3.0 Procedures API.\r\n");
		start = time( NULL);
		TestMXSQLProcedures(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLProcedures (3.0)");
	}
	if (m_Unicode30)
	{
		#ifdef unixcli
			puts("Running MX 3.0 Unicode tests.\r\n");
			puts("Driver doesn't support Unicode yet!\r\n");
		#else
			puts("Running MX 3.0 Unicode tests.\r\n");
			start = time( NULL);
			TestMXSQLUnicode(pTestInfo);
			end = time( NULL);
			LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
			LogResultsTest("Unicode (3.0)");
		#endif
	}
	if (m_LargeBlock)
	{
		puts("Running TRAF LargeBlock feature tests.\r\n");
		start = time( NULL);
		TestLargeBlock(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("LargeBlock");
	}
	if (m_ForeignKeys30)			
	{
		puts("Running MX 3.0 SQLForeignKeys API.\r\n");
		start = time( NULL);
		TestMXSQLForeignKeys(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLForeignKeys (3.0)");
	}
	if (m_QueryID)
	{
		puts("Running TRAF QueryID feature tests.\r\n");
		start = time( NULL);
		TestQueryID(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("Query ID");
	}
	if (m_Hash2)
	{
		#ifdef _HASH2
			puts("Running Hash2 feature tests.\r\n");
			start = time( NULL);
			TestHash2(pTestInfo);
			end = time( NULL);
			LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
			LogResultsTest("Hash2");
		#else
			puts("Running Hash2 feature tests.\r\n");
			puts("Hash2 feature is only supported by Linux and Solaris drivers\r\n");
		#endif
	}
	if (m_InfoStats)
    {
        puts("Running InfoStats tests\r\n");
		
		start = time( NULL);
		TestInfoStats(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("InfoStats");
    }
    if (m_TablePrivileges30)			
	{
		puts("Running MX 3.0 SQLTablePrivileges API.\r\n");
		start = time( NULL);
		TestMXSQLTablePrivileges(pTestInfo);
		end = time( NULL);
		LogMsg(NONE,"Time elapsed: %f\n", difftime(end, start));
		LogResultsTest("SQLTablePrivileges (3.0)");
	}
/*
	// Partial DateTime Conversions
	if (m_PartialDateTimeInput30)	
	{
		puts("Running MX 3.0 Partial DateTime Input Conversion tests\r\n");
		TestMXPartialDateTimeInputConversions(pTestInfo);
		LogResultsTest("Partial Date/time - input conversion (3.0)");
	}

	if (m_PartialDateTimeOutput30)	
	{
		puts("Running MX 3.0 Partial DateTime Output Conversion tests\r\n");
		TestMXPartialDateTimeOutputConversions(pTestInfo);
		LogResultsTest("Partial Date/time - output conversion (3.0)");
	}
*/
	return 0;
}

void ReadSelectedTests(char* filename) 
{
	char line[100];
    char *ret;
	char seps[]   = " \t";
	char *token;
	FILE *input_file;
	
	input_file = fopen(filename, "r");
	printf("%s\n", filename);
	if (input_file == NULL)
	{
		printf("Error opening file %s\n", filename);
		perror("Unable to open file");
		exit(-1);
	}

	ret = fgets(line, 80, input_file);

	while (ret != NULL)
	{
		line[strlen(line)-1] = '\0';
		token = strtok(line, seps);

		if (_stricmp(token,"SQLAllocEnv") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_AllocEnv = TRUE;
			else
				m_AllocEnv = FALSE;
			}
		else if (_stricmp(token,"SQLAllocConnect") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_AllocConnect = TRUE;
			else
				m_AllocConnect = FALSE;
			}
		else if (_stricmp(token,"SQLBindParameter") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BindParameter = TRUE;
			else
				m_BindParameter = FALSE;
			}
		else if (_stricmp(token,"SQLBrowseConnect") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BrowseConnect = TRUE;
			else
				m_BrowseConnect = FALSE;
			}
		else if (_stricmp(token,"SQLColumnAttribute") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ColAttrib = TRUE;
			else
				m_ColAttrib = FALSE;
			}
		else if (_stricmp(token,"SQLConnectDisconnect") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Connect = TRUE;
			else
				m_Connect = FALSE;
			}
		else if (_stricmp(token,"SQLDataSources") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_DataSources = TRUE;
			else
				m_DataSources = FALSE;
			}
		else if (_stricmp(token,"SQLDescribeColumns") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_DesCols = TRUE;
			else
				m_DesCols = FALSE;
			}
		else if (_stricmp(token,"SQLDriverConnect") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_DriverConnect = TRUE;
			else
				m_DriverConnect = FALSE;
			}
		else if (_stricmp(token,"SQLDrivers") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Drivers = TRUE;
			else
				m_Drivers = FALSE;
			}
		else if (_stricmp(token,"SQLError") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Error = TRUE;
			else
				m_Error = FALSE;
			}
		else if (_stricmp(token,"SQLExecuteDirect") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ExecDirect = TRUE;
			else
				m_ExecDirect = FALSE;
			}
		else if (_stricmp(token,"SQLExecute") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Execute = TRUE;
			else
				m_Execute = FALSE;
			}
		else if (_stricmp(token,"SQLExtendedFetch") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ExtendedFetch = TRUE;
			else
				m_ExtendedFetch = FALSE;
			}
		else if (_stricmp(token,"SQLFetch") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Fetch = TRUE;
			else
				m_Fetch = FALSE;
			}
		else if (_stricmp(token,"SQLGetData") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetData = TRUE;
			else
				m_GetData = FALSE;
			}
		else if (_stricmp(token,"SQLPutData") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_PutData = TRUE;
			else
				m_PutData = FALSE;
			}
		else if (_stricmp(token,"SQLGetFunctions") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetFunctions = TRUE;
			else
				m_GetFunctions = FALSE;
			}
		else if (_stricmp(token,"SQLGetInfo") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetInfo = TRUE;
			else
				m_GetInfo = FALSE;
			}
		else if (_stricmp(token,"SQLMoreResults") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_MoreResults = TRUE;
			else
				m_MoreResults = FALSE;
			}
		else if (_stricmp(token,"SQLAllocStmt") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_AllocStmt = TRUE;
			else
				m_AllocStmt = FALSE;
			}
		else if (_stricmp(token,"SQLBindColumn") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BindCol = TRUE;
			else
				m_BindCol = FALSE;
			}
		else if (_stricmp(token,"SQLColumns") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Columns = TRUE;
			else
				m_Columns = FALSE;
			}
		else if (_stricmp(token,"SQLDescribeParam") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_DescribeParam = TRUE;
			else
				m_DescribeParam = FALSE;
			}
		else if (_stricmp(token,"SQLGetTypeInfo") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetTypeInfo = TRUE;
			else
				m_GetTypeInfo = FALSE;
			}
		else if (_stricmp(token,"SQLPrimaryKeys") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_PrimaryKeys = TRUE;
			else
				m_PrimaryKeys = FALSE;
			}
		else if (_stricmp(token,"ResourceGoverning") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ResGovern = TRUE;
			else
				m_ResGovern = FALSE;
			}
		else if (_stricmp(token,"SQLSetConnectOption") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_SetConnectOption = TRUE;
			else
				m_SetConnectOption = FALSE;
			}
		else if (_stricmp(token,"SQLSetCursorName") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_SetCursorName = TRUE;
			else
				m_SetCursorName = FALSE;
			}
		else if (_stricmp(token,"SQLSetStatementOption") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_SetStmtOption = TRUE;
			else
				m_SetStmtOption = FALSE;
			}
		else if (_stricmp(token,"SQLSpecialColumns") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_SpecialColumns = TRUE;
			else
				m_SpecialColumns = FALSE;
			}
		else if (_stricmp(token,"SQLStatistics") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Statistics = TRUE;
			else
				m_Statistics = FALSE;
			}
		else if (_stricmp(token,"SQLTables") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Tables = TRUE;
			else
				m_Tables = FALSE;
			}
		else if (_stricmp(token,"SQLNativeSql") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_NativeSql = TRUE;
			else
				m_NativeSql = FALSE;
			}
		else if (_stricmp(token,"SQLNumParams") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_NumParams = TRUE;
			else
				m_NumParams = FALSE;
			}
		else if (_stricmp(token,"SQLNumResultCols") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_NumResultCols = TRUE;
			else
				m_NumResultCols = FALSE;
			}
		else if (_stricmp(token,"SQLPrepare") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Prepare = TRUE;
			else
				m_Prepare = FALSE;
			}
		else if (_stricmp(token,"SQLRowCount") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_RowCount = TRUE;
			else
				m_RowCount = FALSE;
			}
		else if (_stricmp(token,"SQLTransact") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Transact = TRUE;
			else
				m_Transact = FALSE;
			}
		else if (_stricmp(token,"SQLAllocHandle") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_AllocHandle30= TRUE;
			else
				m_AllocHandle30 = FALSE;
			}
		else if (_stricmp(token,"SQLBindParameter30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BindParameter30 = TRUE;
			else
				m_BindParameter30 = FALSE;
			}
		else if (_stricmp(token,"SQLCloseCursor") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_CloseCursor30 = TRUE;
			else
				m_CloseCursor30 = FALSE;
			}
		else if (_stricmp(token,"SQLColumnAttributes30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ColAttributes30 = TRUE;
			else
				m_ColAttributes30 = FALSE;
			}
		else if (_stricmp(token,"SQLCopyDescriptor") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_CopyDesc30 = TRUE;
			else
				m_CopyDesc30 = FALSE;
			}
		else if (_stricmp(token,"SQLDescribeColumns30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_DescribeCol30 = TRUE;
			else
				m_DescribeCol30 = FALSE;
			}
		else if (_stricmp(token,"SQLEndTran") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_EndTran30 = TRUE;
			else
				m_EndTran30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetConnectAttr") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetConnectAttr30 = TRUE;
			else
				m_GetConnectAttr30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetDescField") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_SetGetDescFields30 = TRUE;
			else
				m_SetGetDescFields30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetDescRec") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetDescRec30 = TRUE;
			else
				m_GetDescRec30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetDiagField") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetDiagField30 = TRUE;
			else
				m_GetDiagField30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetDiagRec") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetDiagRec30 = TRUE;
			else
				m_GetDiagRec30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetEnvAttr") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetEnvAttr30 = TRUE;
			else
				m_GetEnvAttr30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetInfo30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetInfo30 = TRUE;
			else
				m_GetInfo30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetStmtAttr") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetStmtAttr30 = TRUE;
			else
				m_GetStmtAttr30 = FALSE;
			}
		else if (_stricmp(token,"SQLMoreResults30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_MoreResults30 = TRUE;
			else
				m_MoreResults30 = FALSE;
			}
		else if (_stricmp(token,"SQLBindCol30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BindCol30 = TRUE;
			else
				m_BindCol30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetData30") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetData30 = TRUE;
			else
				m_GetData30 = FALSE;
			}
/*		else if (_stricmp(token,"SQLPartialDateTimeInput") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_PartialDateTimeInput = TRUE;
			else
				m_PartialDateTimeInput = FALSE;
			}
		else if (_stricmp(token,"SQLPartialDateTimeOutput") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_PartialDateTimeOutput = TRUE;
			else
				m_PartialDateTimeOutput = FALSE;
			}
*/		else if (_stricmp(token,"SQLBindColInterval") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BindColInterval30 = TRUE;
			else
				m_BindColInterval30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetDataInterval") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetDataInterval30 = TRUE;
			else
				m_GetDataInterval30 = FALSE;
			}
		else if (_stricmp(token,"SQLBindParamInterval") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_BindParamInterval30 = TRUE;
			else
				m_BindParamInterval30 = FALSE;
			}
		else if (_stricmp(token,"SQLForeignKeys") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ForeignKeys30 = TRUE;
			else
				m_ForeignKeys30 = FALSE;
			}
		else if (_stricmp(token,"SQLColumnPriv") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ColumnPrivileges30 = TRUE;
			else
				m_ColumnPrivileges30 = FALSE;
			}
		else if (_stricmp(token,"SQLTablePriv") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_TablePrivileges30 = TRUE;
			else
				m_TablePrivileges30 = FALSE;
			}
		else if (_stricmp(token,"SQLGetTypeInfo3") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_GetTypeInfo30R18 = TRUE;
			else
				m_GetTypeInfo30R18 = FALSE;
			}
		else if (_stricmp(token,"SQLProcedures") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Procedures30 = TRUE;
			else
				m_Procedures30 = FALSE;
			}
		else if (_stricmp(token,"SQLProcedureColumns") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_ProcedureColumns30 = TRUE;
			else
				m_ProcedureColumns30 = FALSE;
			}
		else if (_stricmp(token,"SQLFetchScroll") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_FetchScroll30 = TRUE;
			else
				m_FetchScroll30 = FALSE;
			}
		else if (_stricmp(token,"Unicode") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Unicode30 = TRUE;
			else
				m_Unicode30 = FALSE;
			}
		else if (_stricmp(token,"QueryID") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_QueryID = TRUE;
			else
				m_QueryID = FALSE;
			}
		else if (_stricmp(token,"Hash2") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Hash2 = TRUE;
			else
				m_Hash2 = FALSE;
			}
		else if (_stricmp(token,"LargeBlock") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_LargeBlock = TRUE;
			else
				m_LargeBlock = FALSE;
			}
        else if (_stricmp(token,"InfoStats") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_InfoStats = TRUE;
			else
				m_InfoStats = FALSE;
			}
		else if (_stricmp(token,"SQLCancel") == 0)
			{
			token = strtok(NULL, seps);
			if (_stricmp(token,"YES") == 0)
				m_Cancel = TRUE;
			else
				m_Cancel = FALSE;
			}
		else printf("***ERROR: %s does not match any of the expected API names or known tokens.\n",token);

		ret = fgets(line, 80, input_file);
	}
}

void MapApiNameToFlag(char *token)
{
	if (_stricmp(token,"SQLAllocEnv") == 0)
		m_AllocEnv = TRUE;
	else if (_stricmp(token,"SQLAllocConnect") == 0)
		m_AllocConnect = TRUE;
	else if (_stricmp(token,"SQLBindParameter") == 0)
		m_BindParameter = TRUE;
	else if (_stricmp(token,"SQLBrowseConnect") == 0)
		m_BrowseConnect = TRUE;
	else if (_stricmp(token,"SQLColumnAttribute") == 0)
		m_ColAttrib = TRUE;
	else if (_stricmp(token,"SQLConnectDisconnect") == 0)
		m_Connect = TRUE;
	else if (_stricmp(token,"SQLDataSources") == 0)
		m_DataSources = TRUE;
	else if (_stricmp(token,"SQLDescribeColumns") == 0)
		m_DesCols = TRUE;
	else if (_stricmp(token,"SQLDriverConnect") == 0)
		m_DriverConnect = TRUE;
	else if (_stricmp(token,"SQLDrivers") == 0)
		m_Drivers = TRUE;
	else if (_stricmp(token,"SQLError") == 0)
		m_Error = TRUE;
	else if (_stricmp(token,"SQLExecuteDirect") == 0)
		m_ExecDirect = TRUE;
	else if (_stricmp(token,"SQLExecute") == 0)
		m_Execute = TRUE;
	else if (_stricmp(token,"SQLExtendedFetch") == 0)
		m_ExtendedFetch = TRUE;
	else if (_stricmp(token,"SQLFetch") == 0)
		m_Fetch = TRUE;
	else if (_stricmp(token,"SQLGetData") == 0)
		m_GetData = TRUE;
	else if (_stricmp(token,"SQLPutData") == 0)
		m_PutData = TRUE;
	else if (_stricmp(token,"SQLGetFunctions") == 0)
		m_GetFunctions = TRUE;
	else if (_stricmp(token,"SQLGetInfo") == 0)
		m_GetInfo = TRUE;
	else if (_stricmp(token,"SQLMoreResults") == 0)
		m_MoreResults = TRUE;
	else if (_stricmp(token,"SQLAllocStmt") == 0)
		m_AllocStmt = TRUE;
	else if (_stricmp(token,"SQLBindColumn") == 0)
		m_BindCol = TRUE;
	else if (_stricmp(token,"SQLColumns") == 0)
		m_Columns = TRUE;
	else if (_stricmp(token,"SQLDescribeParam") == 0)
		m_DescribeParam = TRUE;
	else if (_stricmp(token,"SQLGetTypeInfo") == 0)
		m_GetTypeInfo = TRUE;
	else if (_stricmp(token,"SQLPrimaryKeys") == 0)
		m_PrimaryKeys = TRUE;
	else if (_stricmp(token,"ResourceGoverning") == 0)
		m_ResGovern = TRUE;
	else if (_stricmp(token,"SQLSetConnectOption") == 0)
		m_SetConnectOption = TRUE;
	else if (_stricmp(token,"SQLSetCursorName") == 0)
		m_SetCursorName = TRUE;
	else if (_stricmp(token,"SQLSetStatementOption") == 0)
		m_SetStmtOption = TRUE;
	else if (_stricmp(token,"SQLSpecialColumns") == 0)
		m_SpecialColumns = TRUE;
	else if (_stricmp(token,"SQLStatistics") == 0)
		m_Statistics = TRUE;
	else if (_stricmp(token,"SQLTables") == 0)
		m_Tables = TRUE;
	else if (_stricmp(token,"SQLNativeSql") == 0)
		m_NativeSql = TRUE;
	else if (_stricmp(token,"SQLNumParams") == 0)
		m_NumParams = TRUE;
	else if (_stricmp(token,"SQLNumResultCols") == 0)
		m_NumResultCols = TRUE;
	else if (_stricmp(token,"SQLPrepare") == 0)
		m_Prepare = TRUE;
	else if (_stricmp(token,"SQLRowCount") == 0)
		m_RowCount = TRUE;
	else if (_stricmp(token,"SQLTransact") == 0)
		m_Transact = TRUE;
	else if (_stricmp(token,"SQLAllocHandle") == 0)
		m_AllocHandle30 = TRUE;
	else if (_stricmp(token,"SQLBindParameter30") == 0)
		m_BindParameter30 = TRUE;
	else if (_stricmp(token,"SQLCloseCursor") == 0)
		m_CloseCursor30 = TRUE;
	else if (_stricmp(token,"SQLColumnAttributes30") == 0)
		m_ColAttributes30 = TRUE;
	else if (_stricmp(token,"SQLCopyDescriptor") == 0)
		m_CopyDesc30 = TRUE;
	else if (_stricmp(token,"SQLDescribeColumns30") == 0)
		m_DescribeCol30 = TRUE;
	else if (_stricmp(token,"SQLEndTran") == 0)
		m_EndTran30 = TRUE;
	else if (_stricmp(token,"SQLGetConnectAttr") == 0)
		m_GetConnectAttr30 = TRUE;
	else if (_stricmp(token,"SQLGetDescField") == 0)
		m_SetGetDescFields30 = TRUE;
	else if (_stricmp(token,"SQLGetDescRec") == 0)
		m_GetDescRec30 = TRUE;
	else if (_stricmp(token,"SQLGetDiagField") == 0)
		m_GetDiagField30 = TRUE;
	else if (_stricmp(token,"SQLGetDiagRec") == 0)
		m_GetDiagRec30 = TRUE;
	else if (_stricmp(token,"SQLGetEnvAttr") == 0)
		m_GetEnvAttr30 = TRUE;
	else if (_stricmp(token,"SQLGetInfo30") == 0)
		m_GetInfo30 = TRUE;
	else if (_stricmp(token,"SQLGetStmtAttr") == 0)
		m_GetStmtAttr30 = TRUE;
	else if (_stricmp(token,"SQLMoreResults30") == 0)
		m_MoreResults30 = TRUE;
	else if (_stricmp(token,"SQLBindCol30") == 0)
		m_BindCol30 = TRUE;
	else if (_stricmp(token,"SQLGetData30") == 0)
		m_GetData30 = TRUE;
/*	else if (_stricmp(token,"SQLPartialDateTimeInput") == 0)
		m_PartialDateTimeInput = TRUE;
	else if (_stricmp(token,"SQLPartialDateTimeOutput") == 0)
		m_PartialDateTimeOutput = TRUE;
*/
	else if (_stricmp(token,"SQLBindColInterval") == 0)
		m_BindColInterval30 = TRUE;
	else if (_stricmp(token,"SQLGetDataInterval") == 0)
		m_GetDataInterval30 = TRUE;
	else if (_stricmp(token,"SQLBindParamInterval") == 0)
		m_BindParamInterval30 = TRUE;
	else if (_stricmp(token,"SQLForeignKeys") == 0)
		m_ForeignKeys30 = TRUE;
	else if (_stricmp(token,"SQLColumnPriv") == 0)
		m_ColumnPrivileges30 = TRUE;
	else if (_stricmp(token,"SQLTablePriv") == 0)
		m_TablePrivileges30 = TRUE;
	else if (_stricmp(token,"SQLGetTypeInfo3") == 0)
		m_GetTypeInfo30R18 = TRUE;
	else if (_stricmp(token,"SQLProcedures") == 0)
		m_Procedures30 = TRUE;
	else if (_stricmp(token,"SQLProcedureColumns") == 0)
		m_ProcedureColumns30 = TRUE;
	else if (_stricmp(token,"SQLFetchScroll") == 0)
		m_FetchScroll30 = TRUE;
	else if (_stricmp(token,"Unicode") == 0)
		m_Unicode30 = TRUE;
	else if (_stricmp(token,"QueryID") == 0)
		m_QueryID = TRUE;
	else if (_stricmp(token,"Hash2") == 0)
		m_Hash2 = TRUE;
	else if (_stricmp(token,"SQLCancel") == 0)
		m_Cancel = TRUE;
	else if (_stricmp(token,"LargeBlock") == 0)
		m_LargeBlock = TRUE;
    else if (_stricmp(token,"InfoStats") == 0)
		m_InfoStats = TRUE;
	else printf("***ERROR: %s does not match any of the expected API names or known tokens.\n",token);
}
