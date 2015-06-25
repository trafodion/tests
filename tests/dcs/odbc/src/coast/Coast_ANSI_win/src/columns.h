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

extern PassFail CreateMouseDB( TestInfo *);

/*
---------------------------------------------------------
TestSQLColumns()                      
Tests the SQLColumns function in ODBC, also tests wildcard 
syntax of parser.

TestSQLColumns loops through the test cases and generates the
calls to 'TestSQLColumnsExec' which actually does the work and
analyzes the return values
*/

#define NUM_CALLS	16
#define RESULT_DIR	"\\results\\SQLColumns"

typedef struct COLPARAMSTRUCTtag	{
	char	*szQualifier;
	char	*szOwner;
	char	*szName;
	char	*szCol;	
}  COLPARAMSTRUCT;

 /* Parameter Arrays for testing */
 COLPARAMSTRUCT cps[NUM_CALLS] = {
	NULL,		NULL,				(char*)"mice",		NULL,
	NULL,		(char*)"%",		NULL,				(char*)"%e",			
	NULL,       "CAT_SYLVESTR",		NULL,				NULL,
	NULL,		NULL,				(char*)"%1",		NULL,
	NULL,		(char*)"MOUSE_MINNIE",	NULL,			(char*)"H%",
	NULL,		(char*)"MOUSE_%",	(char*)"_tab_",	NULL,
	NULL,		(char*)"%.s%",		(char*)"d%",		(char*)"%",
	NULL,		(char*)"%",		(char*)"_tab%",	(char*)NULL,
	NULL,		(char*)"______M%", (char*)"%b_",		NULL,
	NULL,		(char*)"dbo",		(char*)"_tab",		(char*)"%t%",
	NULL,		(char*)"dbo",		(char*)"_tab",		(char*)"s%",
	NULL,		(char*)"C%",		(char*)"%tab%",	(char*)"%",
	NULL,		(char*)"_at_%",	(char*)"%",		NULL,
	NULL,		NULL,				(char*)"ATAB",		(char*)NULL,
	NULL,		(char*)"MOUSE_%",  (char*)"A%B1",		(char*)"%FLD_",
	NULL,		NULL,				NULL,				(char*)"NAMEFLD_",
 };
