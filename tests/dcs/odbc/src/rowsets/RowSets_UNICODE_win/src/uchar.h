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

#ifdef  UNICODE
#define			_T(x)			L ## x
#define			_tmain			wmain
#define			_tcslen		wcslen
#define			_tcsdup		wcsdup
#define			_tcscpy		wcscpy
#define			_tcsncpy		wcsncpy
#define			_tcscmp		wcscmp
#define			_tcsncmp		wcsncmp
#define			_tcsicmp		wcsicmp
#define			_tcsnicmp		wcsnicmp
#define			_tcscat		wcscat
#define			_tcstok		wcstok
#define			_tstoi			watoi
#define			_fgetts		fgetws
#define			_tfopen		wfopen
#define			_tprintf		wprintf
#define			_stprintf		wsprintf
#define			_vftprintf		vfwprintf
#define			_vtprintf		vwprintf
#define			_tcsftime		wcsftime
#else
#define			_T(x)			x
#define			_tmain			main
#define			_tcslen		strlen
#define			_tcsdup		strdup
#define			_tcscpy		strcpy
#define			_tcsncpy		strncpy
#define			_tcscmp		strcmp
#define			_tcsncmp		strncmp
#define			_tcsicmp		strcasecmp
#define			_tcsnicmp		strncasecmp
#define			_tcscat		strcat
#define			_tcstok		strtok
#define			_tstoi			atoi
#define			_fgetts		fgets
#define			_tfopen		fopen
#define			_tprintf		printf
#define			_stprintf		sprintf
#define			_vftprintf		vfprintf
#define			_vtprintf		vprintf
#define			_tcsftime		strftime
#endif

#ifdef UNICODE
#define			TCHAR			wchar_t
#define			SQL_C_TCHAR		SQL_C_WCHAR
#else
#define			TCHAR			char
#define			SQL_C_TCHAR		SQL_C_CHAR
#endif 
