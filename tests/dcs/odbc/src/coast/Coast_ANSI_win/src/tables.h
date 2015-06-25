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

/* tables.h
   Defininitions and declaration for tables.c, functions for testing
   SQLTables functionality.
*/
#define NUM_CALLS   15
#define RESULT_DIR  "\\results\\SQLTables"

typedef struct TABPARAMSTRUCTtag   {
    char   *szQualifier;
    char   *szOwner;
    char   *szName;
    char   *szType;
}  TABPARAMSTRUCT;


PassFail TestSQLTablesExec( TestInfo *pTestInfo, TABPARAMSTRUCT * );

 /* Parameter Arrays for testing */
 TABPARAMSTRUCT tps[NUM_CALLS] = {
    NULL,       NULL,					NULL,               NULL,
    NULL,       (char*)"%",				NULL,               NULL,
    (char*)"%" ,NULL,					NULL,               NULL,
    NULL,       NULL,					(char*)"%1",		NULL,
    NULL,       (char*)"MOUSE_MINNIE",	NULL,				(char*)"TABLE",
    NULL,       (char*)"MOUSE_%",		(char*)"_tab_",		(char*)"VIEW",
    NULL,       (char*)"%_s%",			(char*)"d%",		NULL,
    NULL,       (char*)"%",				(char*)"_tab%",		(char*)"TABLE",
    NULL,       (char*)"______M%",		(char*)"%b_",		NULL,
    NULL,       (char*)"dbo",			(char*)"_tab",		(char*)"TABLE",
    NULL,       (char*)"dbo",			(char*)"_tab",		(char*)"VIEW",
    NULL,       (char*)"C%",			(char*)"%tab%",		(char*)"VIEW",
    NULL,       (char*)"_at%",			(char*)"%",			(char*)"TABLE",
    NULL,       NULL,					(char*)"A%B",		(char*)"TABLE",
    NULL,       (char*)"MOUSE_%",		(char*)"A%B1",		(char*)"VIEW"
 };
