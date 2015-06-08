#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"
#include "apitests.h"

/*
---------------------------------------------------------
TestQueryID() and TestJobID()
---------------------------------------------------------
*/

PassFail TestQueryID (TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR			Heading[MAX_STRING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv, henv2;
 	SQLHANDLE 		hdbc, hdbc2 = (SQLHANDLE)NULL;
 	SQLHANDLE		hstmt, hstmt2;

	int				loop = 0;
	//TCHAR			preparedStmt[1024];
	TCHAR			infoStatsStmt[ 1024 ];
	SQLTCHAR		cursorName[ 1024 ];
	TCHAR			jobid[256];
	TCHAR			queryID[256];
	SQLINTEGER		jobidlen;
	SQLLEN			queryIDPtr;
	TCHAR			tempStr[256];
                              
	TCHAR *droptab   =  _T("DROP TABLE JOBID cascade");
  	TCHAR *createtab =  _T("CREATE TABLE JOBID (C int) NO PARTITION");
  	TCHAR *inserttab =  _T("INSERT INTO JOBID VALUES (10)");
  	TCHAR *selecttab =  _T("SELECT * FROM JOBID");

	struct
	{
		RETCODE		returncode;
		TCHAR		*jobID;
		TCHAR		*jobIDExpected;
	} jobIDMatrix[] = {
		{ SQL_SUCCESS, _T("")                                                   , _T("") },
		{ SQL_SUCCESS, _T("H")                                                  , _T("H") },
		{ SQL_SUCCESS, _T("h")                                                  , _T("h") },
		{ SQL_SUCCESS, _T("0")                                                  , _T("0") },
		{ SQL_SUCCESS, _T("_")                                                  , _T("_") },
		{ SQL_SUCCESS, _T("________________________")                           , _T("________________________") },
		{ SQL_SUCCESS, _T("odbcqa")                                             , _T("odbcqa") },
		{ SQL_SUCCESS, _T("odbcqa00")                                           , _T("odbcqa00") },
		{ SQL_SUCCESS, _T("00odbcqa")                                           , _T("00odbcqa") },
		{ SQL_SUCCESS, _T("0123_HELLOKITTY")                                    , _T("0123_HELLOKITTY") },
		{ SQL_SUCCESS, _T("_Hello_Kitty_123")                                   , _T("_Hello_Kitty_123") },
		{ SQL_SUCCESS, _T("Hello_Kitty_Went_To_The_")							, _T("Hello_Kitty_Went_To_The_") },
		{ SQL_SUCCESS, _T("Hello_Kitty_Went_To_The_")							, _T("Hello_Kitty_Went_To_The_") },
		{ SQL_SUCCESS, _T("1234567890_1234567890")								, _T("1234567890_1234567890") },
		{ SQL_SUCCESS, _T("123456789012345678901234")                           , _T("123456789012345678901234") },
		{ SQL_SUCCESS, _T("123456789012345678901234")                           , _T("123456789012345678901234") },
		{ SQL_SUCCESS, _T("1234567890123456789012345")                          , _T("123456789012345678901234") },
		{ SQL_SUCCESS, _T("Hello_Kitty_Went_To_The_Store_To_Buy")				, _T("Hello_Kitty_Went_To_The_") },
		{ SQL_SUCCESS_WITH_INFO, _T(" ")										, _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T(" HelloKitty")                              , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("Hello Kitty")                              , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("HelloKitty ")                              , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("1 2")						                , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("12345.67890.123456789012")                 , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("Hello$Kitty")                              , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("\"HelloKitty\"")							, _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("'HelloKitty'")								, _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("\" \"")                                    , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("\"\"")                                     , _T("") },
		{ SQL_SUCCESS_WITH_INFO, _T("\"#@*()-_=+[]{}|:;'<>,.?\"")               , _T("") },
		{ -101				   , _T("")                                         , _T("") }
	};

	//struct
	//{
	//	RETCODE		rtc;
	//	TCHAR		*queryID;
	//	TCHAR		*queryIDExpected;
	//} queryIDMatrix[] = {
	//	{ SQL_SUCCESS, "HELLOKITTY"	                                        , "HELLOKITTY" },
	//	{ SQL_SUCCESS, "H"                                                  , "H" },
	//	{ SQL_SUCCESS, "HELLOKITTYWENTTOTHESTORETOBUYDRI"                   , "HELLOKITTYWENTTOTHESTORETOBUYDRI" },
	//	{ SQL_SUCCESS, "HELLOKITTYWENTTOTHESTORETOBUYDRINKSFORTHEPARTY"     , "HELLOKITTYWENTTOTHESTORETOBUYDRI" },
	//	{ SQL_SUCCESS, "HelloKitty"                                         , "HELLOKITTY" },
	//	{ SQL_SUCCESS, "h"                                                  , "H" },
	//	{ SQL_SUCCESS, "HelloKittyWentToTheStoreToBuyDri"                   , "HELLOKITTYWENTTOTHESTORETOBUYDRI" },
	//	{ SQL_SUCCESS, "HelloKittyWentToTheStoreToBuyDrinksForTheParty"     , "HELLOKITTYWENTTOTHESTORETOBUYDRI" },
	//	{ SQL_SUCCESS, "H_1"                                                , "H_1" },
	//	{ SQL_SUCCESS, "HELLO_KITTY_1234"                                   , "HELLO_KITTY_1234" },
	//	{ SQL_SUCCESS, "HELLO_KITTY_1234_ABCDEFGHIJKLMNO"                   , "HELLO_KITTY_1234_ABCDEFGHIJKLMNO" },
	//	{ SQL_SUCCESS, "HELLO_KITTY_1234_ABCDEFGHIJKLMNOPQRSTUVWXYZ"        , "HELLO_KITTY_1234_ABCDEFGHIJKLMNO" },
	//	{ SQL_SUCCESS, "Hello_Kitty_1234"                                   , "HELLO_KITTY_1234" },
	//	{ SQL_SUCCESS, "Hello_Kitty_1234_abcdefghijklmno"                   , "HELLO_KITTY_1234_ABCDEFGHIJKLMNO" },
	//	{ SQL_SUCCESS, "Hello_Kitty_1234_abcdefghijklmnopqrstuvwxyz"        , "HELLO_KITTY_1234_ABCDEFGHIJKLMNO" },
	//	{ SQL_SUCCESS, "\"HELLOKITTY\""                                     , "HELLOKITTY" },
	//	{ SQL_SUCCESS, "\"H\""                                              , "H" },
	//	{ SQL_SUCCESS, "\"HELLOKITTYWENTTOTHESTORETOBUYDRI\""               , "HELLOKITTYWENTTOTHESTORETOBUYDRI" },
	//	{ SQL_SUCCESS, "\"HELLOKITTYWENTTOTHESTORETOBUYDRINKSFORTHEPARTY\"" , "HELLOKITTYWENTTOTHESTORETOBUYDRI" },
	//	{ SQL_SUCCESS, "\"HelloKitty\""                                     , "HelloKitty" },
	//	{ SQL_SUCCESS, "\"h\""                                              , "h" },
	//	{ SQL_SUCCESS, "\"HelloKittyWentToTheStoreToBuyDri\""               , "HelloKittyWentToTheStoreToBuyDri" },
	//	{ SQL_SUCCESS, "\"HelloKittyWentToTheStoreToBuyDrinksForTheParty\"" , "HelloKittyWentToTheStoreToBuyDri" },
	//	{ SQL_SUCCESS, "\"H_1\""                                            , "H_1" },
	//	{ SQL_SUCCESS, "\"HELLO_KITTY_1234\""                               , "HELLO_KITTY_1234" },
	//	{ SQL_SUCCESS, "\"HELLO_KITTY_1234_ABCDEFGHIJKLMNO\""               , "HELLO_KITTY_1234_ABCDEFGHIJKLMNO" },
	//	{ SQL_SUCCESS, "\"HELLO_KITTY_1234_ABCDEFGHIJKLMNOPQRSTUVWXYZ\""    , "HELLO_KITTY_1234_ABCDEFGHIJKLMNO" },
	//	{ SQL_SUCCESS, "\"Hello_Kitty_1234\""                               , "Hello_Kitty_1234" },
	//	{ SQL_SUCCESS, "\"Hello_Kitty_1234_abcdefghijklmno\""               , "Hello_Kitty_1234_abcdefghijklmno" },
	//	{ SQL_SUCCESS, "\"Hello_Kitty_1234_abcdefghijklmnopqrstuvwxyz\""    , "Hello_Kitty_1234_abcdefghijklmno" },
	//	{ SQL_SUCCESS, "\"Hello Kitty\""                                    , "Hello Kitty" },
	//	{ SQL_SUCCESS, "\"Hello Kitty says \"\"MEOW!\"\"\""                 , "Hello Kitty says \"MEOW\"" },
	//	{ SQL_SUCCESS, "\"Hello Kitty's Pruse\""                            , "Hello Kitty's Purse" },
	//	{ SQL_SUCCESS, "\"CREATE\""                                         , "CREATE" },
	//	{ SQL_SUCCESS, "\"SELECT * FROM T1\""								, "SELECT * FROM T1" },
	//	{ SQL_ERROR  , ""                                                   , "" },
	//	{ SQL_ERROR  , "	"                                               , "" },
	//	{ SQL_ERROR  , "1HelloKitty"                                        , "" },
	//	{ SQL_ERROR  , "_A"                                                 , "" },
	//	{ SQL_ERROR  , "Hello Kitty"                                        , "" },
	//	{ SQL_ERROR  , "Hello$Kitty"                                        , "" },
	//	{ SQL_ERROR  , "\"\\HelloKitty\""                                   , "" },
	//	{ SQL_ERROR  , "\"$HelloKitty\""                                    , "" },
	//	{ SQL_ERROR  , "\" \""                                              , "" },
	//	{ SQL_ERROR  , "\"\""                                               , "" },
	//	{ SQL_ERROR  , "\"@*()-_=+[]{}|:;'<>,.?\""                          , "" },
	//	{ SQL_ERROR  , "CREATE"												, "" },
	//	{ -101       , ""                                                   , "" }
	//};

	//struct
	//{
	//	TCHAR*	sqlStmt;
	//} sqlPrepareMatrix[] = {
	//	{ "CREATE CATALOG STMNT" },
	//	{ "CREATE SCHEMA STMNT.TEST" },
	//	{ "CREATE TABLE T2 ( C1 INTEGER NOT NULL NOT DROPPABLE, C2 INTEGER, PRIMARY KEY( C1 ) )" },
	//	{ "CREATE INDEX T2_INDEX ON T2 ( C1 ) NO POPULATE" },
	//	{ "CREATE PROCEDURE T2_PROC (IN IN1 TIME) EXTERNAL NAME 'Procs.N4210' EXTERNAL PATH '/usr/spjqa/Testware/Class' LANGUAGE JAVA PARAMETER STYLE JAVA NO SQL NO ISOLATE" },
	//	{ "CREATE VIEW T2_VIEW AS SELECT C1 FROM T2" },
	//	{ "INSERT INTO T2 VALUES ( 1 , 1) " },
	//	{ "SELECT C1 FROM T2" },
	//	{ "UPDATE T2 SET C2 = 2 WHERE C1 = 1" },
	//	{ "DELETE FROM T2" },
	//	{ "ALTER INDEX T2_INDEX ON T2 ( C2 ) NO POPULATE" },
	//	{ "ALTER TABLE T2 ( C1 INTEGER NOT NULL NOT DROPPABLE, C2 INTEGER NOT NULL, PRIMARY KEY( C1 ) )" },
	//	{ "ALTER TRIGGER" },
	//	{ "DROP SCHEMA STMT.TEST" },
	//	{ "DROP CATALOG STMT" },
	//	{ "DROP INDEX T2_INDEX" },
	//	{ "DROP VIEW T2_VIEW" },
	//	{ "DROP PROCEDURE T2_PROC" },
	//	{ "DROP TABLE T2" },
	//	{ "STOP" }
	//};

//======================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => JobID.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for JobID tests\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect as ODBC3.0 application.\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt, (SQLTCHAR*)droptab,SQL_NTS);

	returncode = SQLExecDirect(hstmt, (SQLTCHAR*)createtab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt, (SQLTCHAR*)inserttab,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	FullDisconnect(pTestInfo);
	TESTCASE_END;

//======================================================================================================
	_stprintf(Heading,_T("Test positive functionality of SessionName, single connection\n"));
	TESTCASE_BEGINW( Heading);

	// Allocate Environment Handle
	returncode = SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")) {
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLFreeEnv(henv);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Allocate Connection handle
	returncode = SQLAllocConnect(henv,&hdbc);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")) {
		LogAllErrors(henv,hdbc,hstmt);
		SQLFreeEnv(henv);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;
	
	loop = 0;
	while( jobIDMatrix[ loop ].returncode != -101 )
	{
		_stprintf(Heading,_T("Test #%d: Testing for jobID: \"%s\" \n"), loop, jobIDMatrix[ loop ].jobID);
		TESTCASE_BEGINW( Heading);

		returncode = SQLSetConnectAttr(hdbc, (SQLINTEGER)SQL_ATTR_SESSIONNAME,(SQLTCHAR*) jobIDMatrix[ loop ].jobID, SQL_NTS);
		if (jobIDMatrix[ loop ].returncode == SQL_SUCCESS) {
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr")) {
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				loop++;
				continue;
			}

		}
		else {
#ifdef unixcli
			if(returncode != SQL_ERROR) {
#else
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr")) {
#endif
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				loop++;
				continue;
			}
		}
		returncode = SQLGetConnectAttr(hdbc, (SQLINTEGER)SQL_ATTR_SESSIONNAME, jobid, 300, &jobidlen);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetConnectAttr")) {
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			loop++;
			continue;
		}
		if (jobIDMatrix[ loop ].returncode == SQL_SUCCESS) {
			//if (_tcscmp(jobIDMatrix[ loop ].jobID, jobid) == 0) {
			if (_tcscmp(jobIDMatrix[ loop ].jobIDExpected, jobid) == 0) {
				LogMsg(NONE, _T("JobIDs are matched. Expected: \"%s\", Actual: \"%s\"\n"), jobIDMatrix[ loop ].jobID, jobid);
				TESTCASE_END;
			}
			else {
				LogMsg(ERRMSG, _T("JobIDs are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), jobIDMatrix[ loop ].jobID, jobid, __LINE__);
				TEST_FAILED;
			}
		}
		else {
#ifdef unixcli
			if (_tcscmp(jobIDMatrix[ loop ].jobIDExpected, jobid) == 0) {
				LogMsg(NONE, _T("JobIDs are matched. Expected: \"%s\", Actual: \"%s\"\n"), jobIDMatrix[ loop ].jobIDExpected, jobid);
				TESTCASE_END;
			}
			else {
				LogMsg(ERRMSG, _T("JobIDs are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), jobIDMatrix[ loop ].jobIDExpected, jobid, __LINE__);
				TEST_FAILED;
			}
#else
			if (_tcscmp(jobIDMatrix[ loop ].jobID, jobid) == 0) {
				LogMsg(NONE, _T("JobIDs are matched. Expected: \"%s\", Actual: \"%s\"\n"), jobIDMatrix[ loop ].jobID, jobid);
				TESTCASE_END;
			}
			else {
				LogMsg(ERRMSG, _T("JobIDs are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), jobIDMatrix[ loop ].jobID, jobid, __LINE__);
				TEST_FAILED;
			}
#endif
		}

		returncode = SQLConnect(hdbc,
							   (SQLTCHAR*)pTestInfo->DataSource,(SWORD)_tcslen(pTestInfo->DataSource),
							   (SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),
							   (SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password)
							   );	
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

#ifndef unixcli
		if (jobIDMatrix[ loop ].returncode ==  SQL_SUCCESS_WITH_INFO) {
			if (returncode != jobIDMatrix[ loop ].returncode) {
				LogMsg(ERRMSG, _T("The retcode has to be SQL_SUCCESS_WITH_INFO, with the error message \"Driver's SQLSetConnectAttr failed.\" in it, at line=%d\n"), __LINE__);
				SQLFreeConnect(hdbc);
				SQLFreeEnv(henv);
				TEST_FAILED;
				TEST_RETURN;
			}
//			LogAllErrors(henv,hdbc,NULL);
			if (!FindError(_T("IM006"),henv,hdbc,NULL)) {
				LogMsg(ERRMSG, _T("Couldn't find state error IM006, with the error message \"Driver's SQLSetConnectAttr failed.\", at line=%d\n"), __LINE__);
				SQLFreeConnect(hdbc);
				SQLFreeEnv(henv);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
#endif

		returncode = SQLAllocStmt(hdbc,&hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLAllocStmt(hdbc,&hstmt2);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLPrepare( hstmt, (SQLTCHAR *)selecttab, SQL_NTS );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLGetCursorName(hstmt, cursorName, sizeof(cursorName), NULL );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}
		LogMsg(NONE,_T("The Cursor for the STMT is \"%s\" \n"),cursorName);
		
		//Get queryID
		_stprintf( infoStatsStmt, _T("INFOSTATS %s"), (TCHAR*)cursorName );
		LogMsg(NONE,_T("The Execute STMT is \"%s\" \n"),infoStatsStmt);

		returncode = SQLBindCol( hstmt2, 1, SQL_C_TCHAR, &queryID, 256, &queryIDPtr );
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLExecDirect( hstmt2, (SQLTCHAR *)infoStatsStmt, SQL_NTS );
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLFetch( hstmt2 );
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		LogMsg(NONE, _T("QueryID: \"%s\"\n"), queryID);
		SQLFreeStmt(hstmt2,SQL_CLOSE);
		SQLFreeStmt(hstmt2,SQL_UNBIND);

		//Get Jobid
		if(isCharSet || isUCS2)
			_stprintf( infoStatsStmt, _T("SELECT queryid_extract( _ISO88591'%s', _ISO88591'SESSIONNAME') FROM JOBID"), (TCHAR*)queryID );
		else
			_stprintf( infoStatsStmt, _T("SELECT queryid_extract('%s','SESSIONNAME') FROM JOBID"), (TCHAR*)queryID );

//		returncode = SQLBindCol( hstmt2, 1, SQL_C_TCHAR, &queryID, 256, &queryIDPtr );
		returncode = SQLBindCol( hstmt2, 1, SQL_C_TCHAR, &jobid, 256, &queryIDPtr );
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLExecDirect( hstmt2, (SQLTCHAR *)infoStatsStmt, SQL_NTS );
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLFetch( hstmt2 );
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

/*		LogMsg(NONE, _T("JobID: \"%s\"\n"), queryID);
		if (_tcscmp(jobIDMatrix[ loop ].jobIDExpected, queryID) == 0) {
			LogMsg(NONE, _T("JobIDs are matched. Expected: \"%s\", Actual: \"%s\"\n"), jobIDMatrix[ loop ].jobIDExpected, queryID);
			TESTCASE_END;
		}
		else {
			LogMsg(ERRMSG, _T("JobIDs are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), jobIDMatrix[ loop ].jobIDExpected, queryID, __LINE__);
			TEST_FAILED;
		}
*/

		LogMsg(NONE, _T("JobID: \"%s\"\n"),jobid );
		if (_tcscmp(jobIDMatrix[ loop ].jobIDExpected, jobid) == 0) {
			LogMsg(NONE, _T("JobIDs are matched. Expected: \"%s\", Actual: \"%s\"\n"), jobIDMatrix[ loop ].jobIDExpected,jobid);
			TESTCASE_END;
		}
		else {
			LogMsg(ERRMSG, _T("JobIDs are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), jobIDMatrix[ loop ].jobIDExpected,jobid , __LINE__);
			TEST_FAILED;
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLFreeStmt(hstmt2,SQL_CLOSE);
		SQLFreeStmt(hstmt2,SQL_UNBIND);

		returncode = SQLDisconnect(hdbc);
		if (returncode != SQL_SUCCESS)
		{
			LogAllErrors(henv,hdbc,hstmt);
			SQLDisconnect(hdbc);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
		}
   		loop++;
	}

	returncode = SQLFreeConnect(hdbc);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}

	returncode = SQLFreeEnv(henv);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}

//======================================================================================================
	_stprintf(Heading,_T("Test positive functionality of SessionName, mutiple connection using the same session name\n"));
	TESTCASE_BEGINW(Heading);

	// Allocate Environment Handle
	returncode = SQLAllocEnv(&henv);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")) {
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLAllocEnv(&henv2);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv2")) {
		LogAllErrors(henv2,hdbc2,hstmt2);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLFreeEnv(henv);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLSetEnvAttr(henv2, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr2"))
	{
		LogAllErrors(henv2,hdbc2,hstmt2);
		SQLFreeEnv(henv2);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Allocate Connection handle
	returncode = SQLAllocConnect(henv,&hdbc);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")) {
		LogAllErrors(henv,hdbc,hstmt);
		SQLFreeEnv(henv);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLAllocConnect(henv2,&hdbc2);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect2")) {
		LogAllErrors(henv2,hdbc2,hstmt2);
		SQLFreeEnv(henv2);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;
	

	_tcscpy(tempStr,_T("123456789012345678901234"));
	_stprintf(Heading,_T("Testing for jobID: %s\n"), tempStr);
	TESTCASE_BEGINW(Heading);

	returncode = SQLSetConnectAttr(hdbc, (SQLINTEGER)SQL_ATTR_SESSIONNAME,(SQLTCHAR*) tempStr, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr")) {
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLSetConnectAttr(hdbc2, (SQLINTEGER)SQL_ATTR_SESSIONNAME,(SQLTCHAR*) tempStr, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetConnectAttr2")) {
		LogAllErrors(henv2,hdbc2,hstmt2);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLGetConnectAttr(hdbc, (SQLINTEGER)SQL_ATTR_SESSIONNAME, jobid, SQL_MAX_SESSIONNAME_LEN*2, &jobidlen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetConnectAttr")) {
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
	}
	if (_tcscmp(tempStr, jobid) == 0) {
		LogMsg(NONE, _T("JobID1 are matched. Expected: \"%s\", Actual: \"%s\"\n"), tempStr, jobid);
	}
	else {
		LogMsg(ERRMSG, _T("JobID1 are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), tempStr, jobid, __LINE__);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLGetConnectAttr(hdbc2, (SQLINTEGER)SQL_ATTR_SESSIONNAME, jobid, SQL_MAX_SESSIONNAME_LEN*2, &jobidlen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetConnectAttr2")) {
		LogAllErrors(henv2,hdbc2,hstmt2);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (_tcscmp(tempStr, jobid) == 0) {
		LogMsg(NONE, _T("JobID2 are matched. Expected: \"%s\", Actual: \"%s\"\n"), tempStr, jobid);
	}
	else {
		LogMsg(ERRMSG, _T("JobID2 are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), tempStr, jobid, __LINE__);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLConnect(hdbc,
						   (SQLTCHAR*)pTestInfo->DataSource,(SWORD)_tcslen(pTestInfo->DataSource),
						   (SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),
						   (SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password)
						   );	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect")) {
		LogAllErrors(henv,hdbc,hstmt);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
		TEST_FAILED;
		TEST_RETURN;
	}
	returncode = SQLConnect(hdbc2,
						   (SQLTCHAR*)pTestInfo->DataSource,(SWORD)_tcslen(pTestInfo->DataSource),
						   (SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),
						   (SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password)
						   );	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect2")) {
		LogAllErrors(henv2,hdbc2,hstmt2);
		SQLFreeConnect(hdbc2);
		SQLFreeEnv(henv2);
		TEST_FAILED;
		TEST_RETURN;
	}

	for (loop=0; loop<2; loop++) {
		if (loop == 0) {
			returncode = SQLAllocStmt(hdbc,&hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")) {
				LogAllErrors(henv,hdbc,hstmt);
				SQLFreeConnect(hdbc);
				SQLFreeEnv(henv);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLAllocStmt(hdbc,&hstmt2);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt3")) {
				LogAllErrors(henv,hdbc,hstmt2);
				SQLFreeConnect(hdbc);
				SQLFreeEnv(henv);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
		else {
			returncode = SQLAllocStmt(hdbc2,&hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")) {
				LogAllErrors(henv2,hdbc2,hstmt);
				SQLFreeConnect(hdbc2);
				SQLFreeEnv(henv2);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLAllocStmt(hdbc2,&hstmt2);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt3")) {
				LogAllErrors(henv2,hdbc2,hstmt2);
				SQLFreeConnect(hdbc2);
				SQLFreeEnv(henv2);
				TEST_FAILED;
				TEST_RETURN;
			}
		}

		returncode = SQLPrepare( hstmt, (SQLTCHAR *)selecttab, SQL_NTS );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLGetCursorName(hstmt, cursorName, sizeof(cursorName), NULL );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")) {
			LogAllErrors(henv,hdbc,hstmt);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		//Get queryID
		_stprintf( infoStatsStmt, _T("INFOSTATS %s"), (TCHAR*)cursorName );
		returncode = SQLBindCol( hstmt2, 1, SQL_C_TCHAR, &queryID, 256, &queryIDPtr );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLExecDirect( hstmt2, (SQLTCHAR *)infoStatsStmt, SQL_NTS );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLFetch( hstmt2 );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		LogMsg(NONE, _T("queryID%d: \"%s\"\n"), loop, queryID);
		SQLFreeStmt(hstmt2,SQL_CLOSE);
		SQLFreeStmt(hstmt2,SQL_UNBIND);

		//Get Jobid
		if(isCharSet || isUCS2)
			_stprintf( infoStatsStmt, _T("SELECT queryid_extract( _ISO88591'%s', _ISO88591'SESSIONNAME') FROM JOBID"), (TCHAR*)queryID );
		else
			_stprintf( infoStatsStmt, _T("SELECT queryid_extract('%s','SESSIONNAME') FROM JOBID"), (TCHAR*)queryID );

		returncode = SQLBindCol( hstmt2, 1, SQL_C_TCHAR, &queryID, 256, &queryIDPtr );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLExecDirect( hstmt2, (SQLTCHAR *)infoStatsStmt, SQL_NTS );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLFetch( hstmt2 );
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol")) {
			LogAllErrors(henv,hdbc,hstmt2);
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			TEST_FAILED;
			TEST_RETURN;
		}

		LogMsg(NONE, _T("JobID%d: \"%s\"\n"), loop, queryID);
		if (_tcscmp(tempStr, queryID) == 0) {
			LogMsg(NONE, _T("JobID%d are matched. Expected: \"%s\", Actual: \"%s\"\n"), loop, tempStr, queryID);
			TESTCASE_END;
		}
		else {
			LogMsg(ERRMSG, _T("JobID%d are not matched. Expected: \"%s\", Actual: \"%s\", at line=%d\n"), loop, tempStr, queryID, __LINE__);
			TEST_FAILED;
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLFreeStmt(hstmt2,SQL_CLOSE);
		SQLFreeStmt(hstmt2,SQL_UNBIND);
	}

	returncode = SQLDisconnect(hdbc);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}
	returncode = SQLDisconnect(hdbc2);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv2,hdbc2,hstmt2);
		SQLDisconnect(hdbc2);
		SQLFreeConnect(hdbc2);
		SQLFreeEnv(henv2);
	}

	returncode = SQLFreeConnect(hdbc);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}
	returncode = SQLFreeConnect(hdbc2);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv2,hdbc2,hstmt2);
		SQLDisconnect(hdbc2);
		SQLFreeConnect(hdbc2);
		SQLFreeEnv(henv2);
	}

	returncode = SQLFreeEnv(henv);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv,hdbc,hstmt);
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}
	returncode = SQLFreeEnv(henv2);
	if (returncode != SQL_SUCCESS)
	{
		LogAllErrors(henv2,hdbc2,hstmt2);
		SQLDisconnect(hdbc2);
		SQLFreeConnect(hdbc2);
		SQLFreeEnv(henv2);
	}

	//=========================================================================================

	//FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => JobID.\n"));
	TEST_RETURN;
}



////======================================================================================================
//
//	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => QueryID.\n");
//
//	TEST_INIT;
//
//	TESTCASE_BEGIN("Setup for QueryID tests\n");
//	// for ODBC 3.0
//	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
//	{
//		LogMsg(NONE,_T("Unable to connect as ODBC3.0 application.\n"));
//		TEST_FAILED;
//		TEST_RETURN;
//	}
//
//	henv = pTestInfo->henv;
// 	hdbc = pTestInfo->hdbc;
// 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
//
//	// This statement handle is for PREPARE commands.
//	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
//	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
//	{
//		TEST_FAILED;
//		LogAllErrors(henv,hdbc,hstmt);
//	}
//	else
//	{
//		LogMsg(NONE,_T("Allocate a stmt handle successfully.\n"));
//	}
//
//	// This statement handle is for INFOSTATS.
//	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt2);	
//	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
//	{
//		TEST_FAILED;
//		LogAllErrors(henv,hdbc,hstmt2);
//	}
//	else
//	{
//		LogMsg(NONE,_T("Allocate a stmt2 handle successfully.\n"));
//	}
//
//	SQLExecDirect(hstmt,(SQLTCHAR *)_T("CREATE TABLE T1( C1 INT NOT NULL NOT DROPPABLE, C2 INT, C3 INT, C4 INT, PRIMARY KEY( C1 ) )"),SQL_NTS);
//
//	TESTCASE_END;
//
////=========================================================================================
//	// Test PREPARE syntax for the QueryID name.
//	while( queryIDMatrix[ loop ].rtc != -101 )
//	{
//		_stprintf( preparedStmt, "PREPARE %s FROM SELECT C1 FROM T1 WHERE C2 > C3 AND C3 > 100", queryIDMatrix[ loop ].queryID );
//		TESTCASE_BEGIN( preparedStmt );
//		LogMsg(NONE,_T("\n"));
//		returncode = SQLPrepare( hstmt, (SQLTCHAR *)preparedStmt, SQL_NTS );
//		if( returncode != queryIDMatrix[ loop ].rtc )
//		{
//			if( queryIDMatrix[ loop ].rtc == SQL_SUCCESS )
//				LogAllErrors( henv, hdbc, hstmt );
//			TEST_FAILED;
//		}
//		else if( returncode == SQL_SUCCESS )
//		{
//			returncode = SQLExecute( hstmt );
//			if( returncode != queryIDMatrix[ loop ].rtc )
//			{
//				if( queryIDMatrix[ loop ].rtc == SQL_SUCCESS )
//					LogAllErrors( henv, hdbc, hstmt );
//				TEST_FAILED;
//			} 
//			else
//			{
//				TESTCASE_END;
//			}
//		}
//		SQLFreeStmt( hstmt, SQL_CLOSE );
//		loop++;
//	}
////=========================================================================================
//	// Test the following scenarios regarding statement id being passed in.
//	// As an extra bonus we make sure all scenarios are run for all the positive
//	// tests tested earlier.
//	TCHAR queryID[33];
//	SQLLEN queryIDPtr;
//
//	loop = 0;
//	while( queryIDMatrix[ loop ].rtc != -101 && queryIDMatrix[ loop ].rtc == SQL_SUCCESS )
//	{
//		LogMsg( NONE, "Scenario 1.%d:\n", loop );
//		_stprintf( preparedStmt, "PREPARE %s FROM SELECT C1 FROM T1 WHERE C2 > C3 AND C3 > 100", queryIDMatrix[ loop ].queryID );
//		TESTCASE_BEGIN( preparedStmt );
//		LogMsg(NONE,_T("\n"));
//		returncode = SQLPrepare( hstmt, (SQLTCHAR *)preparedStmt, SQL_NTS );
//		if( returncode != SQL_SUCCESS )
//		{
//			LogAllErrors( henv, hdbc, hstmt );
//			TEST_FAILED;
//			goto NEXTTEST;
//		}
//		// Then get the cursor name.
//		returncode = SQLGetCursorName( hstmt, cursorName, sizeof(cursorName), NULL );
//		if( returncode != SQL_SUCCESS )	
//		{
//			LogAllErrors( henv, hdbc, hstmt );
//			TEST_FAILED;
//			goto NEXTTEST;
//		}
//		// Gather the INFOSTATS for the command.
//		_stprintf( infoStatsStmt, "INFOSTATS %s", (TCHAR*)cursorName );
//		returncode = SQLBindCol( hstmt2, 1, SQL_C_TCHAR, 
//                                 &queryID, 33, // 32 characters for the query ID and 1 character for NULL terminator.
//                                 &queryIDPtr );
//        returncode = SQLExecDirect( hstmt2, (SQLTCHAR *)infoStatsStmt, SQL_NTS );
//        if( returncode != SQL_SUCCESS )	
//        {
//            LogAllErrors( henv, hdbc, hstmt2 );
//			TEST_FAILED;
//			goto NEXTTEST;
//        }
//		returncode = SQLFetch( hstmt2 );
//		if( returncode != SQL_SUCCESS )	
//        {
//            LogAllErrors( henv, hdbc, hstmt2 );
//			TEST_FAILED;
//			goto NEXTTEST;
//        }
//		// Execute the command.
//		returncode = SQLExecute( hstmt );
//		if( returncode != SQL_SUCCESS )	
//        {
//            LogAllErrors( henv, hdbc, hstmt );
//			TEST_FAILED;
//			goto NEXTTEST;
//        }
//		// Query the repsoitory for results
//
//		// Compare the repository results and INFOSTATS.
//		if( _tcscmp( queryID, queryIDMatrix[ loop ].queryID ) != 0 )
//		{
//			LogMsg(ERRMSG+SHORTTIMESTAMP,"Statement ID mismatch. Expected: %s Actual: %s\n", queryIDMatrix[ loop ].queryID, queryID );
//			TEST_FAILED;
//			goto NEXTTEST;
//		}
//		TESTCASE_END;
//
//NEXTTEST:
//		loop++;
//		LogMsg(NONE,_T("\n"));
//	}
//
//	// Clean up
//	SQLExecDirect(hstmt,(SQLTCHAR*)_T("DROP TABLE T1"),SQL_NTS);
//
////=========================================================================================
//	// Test to make sure we can prepare different kinds of SQL statements.
//	loop = 0;
//	while( _tcscmp( sqlPrepareMatrix[ loop ].sqlStmt, "STOP" ) != 0 )
//	{
//		_stprintf( preparedStmt, "PREPARE STMTID%d FROM %s", loop, sqlPrepareMatrix[ loop ].sqlStmt );
//		TESTCASE_BEGIN( preparedStmt );
//		LogMsg(NONE,_T("\n"));
//		returncode = SQLPrepare( hstmt, (SQLTCHAR *)preparedStmt, SQL_NTS );
//		if( returncode != SQL_SUCCESS )
//		{
//			LogAllErrors( henv, hdbc, hstmt );
//			TEST_FAILED;
//		}
//		else
//		{
//			returncode = SQLExecute( hstmt );
//			if( returncode != SQL_SUCCESS )
//			{
//				LogAllErrors( henv, hdbc, hstmt );
//				TEST_FAILED;
//			} 
//			else
//			{
//				TESTCASE_END;
//			}
//		}
//		SQLFreeStmt( hstmt, SQL_CLOSE );
//		loop++;
//		LogMsg(NONE,_T("\n"));
//	}
//
////=========================================================================================
//
//	FullDisconnect(pTestInfo);
//	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => QueryID.\n"));
//	TEST_RETURN;
//}
