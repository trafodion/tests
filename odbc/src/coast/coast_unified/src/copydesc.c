#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
//#include <winbase.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	NAME_LEN		300
#define ROWS 100
#define DESC_LEN        100
#define SQL_API_SUCCEEDED(returncode) (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)


/*
---------------------------------------------------------
   TestSQLCopyDesc
---------------------------------------------------------
*/
PassFail TestMXSQLCopyDesc(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
//  TCHAR			Heading[MAX_STRING_SIZE];
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;

// Template for a row
typedef struct {
	SQLINTEGER    sPartID;
	SQLLEN        cbPartID; // sushil
	SQLTCHAR		  szDescription[DESC_LEN];
	SQLLEN        cbDescription; // sushil
	SQLREAL       sPrice;
	SQLLEN        cbPrice; // sushil
}	PartsSource;

	PartsSource	  rget[ROWS];	// rowset buffer
	SQLUSMALLINT  sts_ptr[ROWS]; 	//status pointer
	SQLHANDLE     hstmt0, hstmt1;

	SQLHDESC       hArd0, hIrd0, hApd1, hIpd1;

	int i = 0, j = 0;

	struct{
		TCHAR	*DrpTab;
		TCHAR	*CrtTab;
		TCHAR	*InsTab[3];
		TCHAR	*SelTab;
	} Data[] = {  {_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")},
				{_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")}  };

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLCopyDescriptor"), charset_file);
	if (var_list == NULL) return FAILED;

	Data[0].DrpTab		= var_mapping(_T("SQLCopyDescriptor_Data_DrpTab_0"), var_list);
	Data[0].CrtTab		= var_mapping(_T("SQLCopyDescriptor_Data_CrtTab_0"), var_list);
	Data[0].InsTab[0]	= var_mapping(_T("SQLCopyDescriptor_Data_InsTab0_0"), var_list);
	Data[0].InsTab[1]	= var_mapping(_T("SQLCopyDescriptor_Data_InsTab1_0"), var_list);
	Data[0].InsTab[2]	= var_mapping(_T("SQLCopyDescriptor_Data_InsTab2_0"), var_list);
	Data[0].SelTab		= var_mapping(_T("SQLCopyDescriptor_Data_SelTab_0"), var_list);

	Data[1].DrpTab		= var_mapping(_T("SQLCopyDescriptor_Data_DrpTab_1"), var_list);
	Data[1].CrtTab		= var_mapping(_T("SQLCopyDescriptor_Data_CrtTab_1"), var_list);
	Data[1].InsTab[0]	= var_mapping(_T("SQLCopyDescriptor_Data_InsTab0_1"), var_list);
//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLCopyDesc.\n"));
	TEST_INIT;

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

   TESTCASE_BEGIN("Initializing SQLCopyDesc test environment\n");

   if (returncode != SQL_SUCCESS)
   {
	  TEST_FAILED;
	  TEST_RETURN;
   }

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt0);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt1);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLExecDirect(hstmt0,(SQLTCHAR *)Data[0].DrpTab, SQL_NTS);

	SQLExecDirect(hstmt1,(SQLTCHAR *)Data[1].DrpTab, SQL_NTS);

	i = sizeof(rget)/sizeof(rget[0]);
	for(j=0; j<i; j++) {
		rget[j].sPartID = i;
		_tcscpy((TCHAR*)(rget[j].szDescription),_T("abc123"));
		rget[j].sPrice = 0.0;
	}

	TESTCASE_END;

    TESTCASE_BEGIN("Getting Descriptor Handles \n");

	// ARD and IRD of hstmt0
	returncode = SQLGetStmtAttr(hstmt0, SQL_ATTR_APP_ROW_DESC, &hArd0, 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	returncode = SQLGetStmtAttr(hstmt0, SQL_ATTR_IMP_ROW_DESC, &hIrd0, 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
// APD and IPD of hstmt1
	returncode = SQLGetStmtAttr(hstmt1, SQL_ATTR_APP_PARAM_DESC, &hApd1, 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLGetStmtAttr(hstmt1, SQL_ATTR_IMP_PARAM_DESC, &hIpd1, 0, NULL);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;

    TESTCASE_BEGIN("Setting Descriptor Attribs \n");

    // Use row-wise binding on hstmt0 to fetch rows
	returncode = SQLSetStmtAttr(hstmt0, SQL_ATTR_ROW_BIND_TYPE, (SQLPOINTER) sizeof(PartsSource), 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

    // Set rowset size for hstmt0
	returncode = SQLSetStmtAttr(hstmt0, SQL_ATTR_ROW_ARRAY_SIZE, (SQLPOINTER) ROWS, 0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;

    TESTCASE_BEGIN("Creating and setting source and destionation tables \n");

	returncode = SQLExecDirect(hstmt0,(SQLTCHAR *)Data[0].CrtTab, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"Create table"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	//MAY 9, 2014 - MOVING THIS TO AFTER DDLs FOR TRAF
	returncode = SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_OFF, 0);
	returncode = SQLExecDirect(hstmt0, (SQLTCHAR *)Data[0].InsTab[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"insert 1"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt0,(SQLTCHAR *)Data[0].InsTab[1], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"insert 2"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLExecDirect(hstmt0,(SQLTCHAR *)Data[0].InsTab[2], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"insert 3"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	// Execute a select statement
	returncode = SQLExecDirect(hstmt0, (SQLTCHAR *)Data[0].SelTab, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"select statement hstmt0"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	//i = sizeof(rget)/sizeof(rget[0]);
	//for(j=0; j<i; j++) {
	//	LogMsg(NONE,_T("___%d___%s___%d___\n"),rget[j].sPartID,rget[j].szDescription,rget[j].sPrice);
	//}

    // Bind
	returncode = SQLBindCol(hstmt0, 1, SQL_C_SLONG, &rget[0].sPartID, 0, &rget[0].cbPartID);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	returncode = SQLBindCol(hstmt0, 2, SQL_C_TCHAR, &rget[0].szDescription, DESC_LEN, &rget[0].cbDescription);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	returncode = SQLBindCol(hstmt0, 3, SQL_C_FLOAT, &rget[0].sPrice, 0, &rget[0].cbPrice);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	TESTCASE_END;

    TESTCASE_BEGIN("Testing SQLCopyDesc API \n");

    // Perform parameter bindings on hstmt1. 
	returncode = SQLCopyDesc(hArd0, hApd1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLCopyDesc"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLCopyDesc(hIrd0, hIpd1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLCopyDesc"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	TESTCASE_END;

	// Set the array status pointer of IRD
	returncode = SQLSetStmtAttr(hstmt0, SQL_ATTR_ROW_STATUS_PTR, sts_ptr, SQL_IS_POINTER);
    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
    // Set the ARRAY_STATUS_PTR field of APD to be the same
    // as that in IRD.
	returncode = SQLSetStmtAttr(hstmt1, SQL_ATTR_PARAM_OPERATION_PTR, sts_ptr, SQL_IS_POINTER);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetStmtAttr"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

    TESTCASE_BEGIN("Testing SQLCopyDesc results by fetching destination table \n");

	// Prepare an insert statement on hstmt1. Partsb is a copy of
	// PartsSource

	LogMsg(NONE,_T("%s\n"),Data[1].CrtTab);
	
	//MAY 9, 2014 - FOR TRAF DDLs
	SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, 0);
	
	returncode = SQLExecDirect(hstmt1, (SQLTCHAR *)Data[1].CrtTab, SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"Create table 2"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	//MAY 9, 2014 - FOR TRAF DDLs
	returncode = SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_OFF, 0);

	LogMsg(NONE,_T("%s\n"),Data[1].InsTab[0]);
	returncode = SQLPrepare(hstmt1, (SQLTCHAR *)Data[1].InsTab[0], SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,returncode,"Insert table 2"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}

	returncode = SQLFetch(hstmt0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQL Fetch"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		FullDisconnect(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	while (SQL_API_SUCCEEDED(returncode)) 
	{
        //LogMsg(NONE,_T("\nData to be insert into:\n"));
        //for(k = 0; k < ROWS; k++) {
        //    LogMsg(NONE,_T("==> %d\t%s\t%f\n"), rget[k].sPartID, rget[k].szDescription, rget[k].sPrice);
        //}

		// After the call to SQLFetchScroll, the status array has row 
		// statuses. This array is used as input status in the APD
		// and hence determines which elements of the rowset buffer
		// are inserted.
		returncode = SQLExecute(hstmt1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute(hstmt1)"))
		{
			LogAllErrorsVer3(henv,hdbc,hstmt1);
			FullDisconnect(pTestInfo);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLFetch(hstmt0);
	    /*if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch(hstmt0)"))
		{
		   LogAllErrorsVer3(henv,hdbc,hstmt0);
		   FullDisconnect(pTestInfo);
		   TEST_FAILED;
		   TEST_RETURN;
		} */
	} // while     
	
	TESTCASE_END;

//========================================================================================================
	//MAY 9, 2014 - TRAF - MOVING ENDTRAN ABOVE DROP TABLES
	returncode = SQLEndTran(SQL_HANDLE_DBC, (SQLHANDLE)hdbc, SQL_COMMIT);

	//MAY 9, 2014 - SETTING AUTOCOMMIT ON FOR DROP TABLES ON TRAF
	SQLSetConnectAttr((SQLHANDLE)hdbc, SQL_AUTOCOMMIT, (void *)SQL_AUTOCOMMIT_ON, 0);

	SQLExecDirect(hstmt0,(SQLTCHAR *)Data[0].DrpTab, SQL_NTS);

	SQLExecDirect(hstmt1,(SQLTCHAR *)Data[1].DrpTab, SQL_NTS);

	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt0);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt0);
		TEST_FAILED;
	}

	returncode = SQLFreeHandle(SQL_HANDLE_STMT,hstmt1);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt1);
		TEST_FAILED;
	}

	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLCopyDesc.\n"));
	FullDisconnect3(pTestInfo);
	TEST_RETURN;

}
