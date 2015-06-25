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


/* ***
 * wcharsplmt.h - declarations of functions supplement for wchar.h
 *
 * Date: Dec 20, 2011
 *
 * Purpose: provide supplement functions for wchar.h, 
 *		   which are provided in MS Windows systems.
 *		   Defining these functions makes tchar.h unifies
 *		   the codes between Windows and Linux.
 *
 * ***/


#ifndef _WCHAR_SUPLMT_H
#define _WCHAR_SUPLMT_H

#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <locale.h>
#include <ctype.h>
#include <wctype.h>
#include <inttypes.h>
#include <time.h>
#include "unicode/utypes.h"
#include "unicode/ustdio.h"
#include "unicode/uchar.h"
#include "unicode/ustring.h"
#include "unicode/ucnv.h"
#include "unicode/uvernum.h"

#define MAX_STRING_LEN	500
#define PERCENT_SIGN	37

#ifdef __cplusplus
extern "C" {
#endif

// open a file with returning UFILE pointer
// Data will be read or written to with specified locale and code page.
extern UFILE* u_fopen_u (
		const UChar *fname,	// file path/name in wide characters
		const UChar *mode // open mode (r, w, r+, w+...)
		);

// print system error, unicode string, supplement for icu.
extern void u_perror (
		const UChar *uerr		// error message wide characters
		);

// printf() with UChar args, if the icu version 4.4 is used.
// This is not neccessary for icu 4.9, u_printf and u_printf_u is introduced in 4.9
extern int32_t u_printf_u (
		const UChar *format,
		...
		);

// strtok wrapper for unicode character string, compliance with Windows version
extern UChar* u_strtok (
		UChar *wcs,
		const UChar *delim
		);

/** Convert date and time to unicode string
 * This is for icu usage to comply with all _T()
 * for UChar* in this COAST unicode test
 * */
extern size_t u_strftime (
		UChar* ucs,
		size_t maxsize,
		const UChar* format,
		const struct tm* timeptr
		);

/* Convert a time_t to a unicode string 
 * A unicode version for icu UChar type
 * */
extern UChar* u_ctime(const time_t *timep);

/* *Returns a pointer to a new string which is a duplicate 
 * of the string ucs. Memory for the new string is obtained
 * with malloc(), and can be freeed with free();
 * */
extern UChar* u_strdup(const UChar* ucs);

/* * Convert a UChar string to upper case
 * Returns the pointer of the new string
 * */
extern UChar* u_strupr(UChar* ucs);

/* * Compare two strings (ucs1, ucs2) ignoring case of the characters
 * Returns an negative, zero, or positive integer, respectively,
 * representing ucs1 is less than, match, or greater than ucs2.
 * */
extern int32_t u_stricmp(const UChar* ucs1,const UChar* ucs2);

/* * Compare two strings (ucs1, ucs2) withing the specified first n
 * characters of ucs1ignoring case of the characters.
 * Returns an negative, zero, or positive integer, respectively,
 * representing ucs1 is less than, match, or greater than ucs2.
 * */
extern int32_t u_strnicmp(const UChar* ucs1,const UChar* ucs2, int32_t n);

//
extern double ucnv_tof (
		const UChar *nptr
		);

//
extern UChar* ucnv_fromi (
		int value,
		UChar *ucs,
		int radix
		);

//
extern UChar* ucnv_froml (
		long value,
		UChar *ucs,
		int radix
		);

//
extern int ucnv_toi (
		const UChar *nptr
		);

extern size_t u_mbstoucs(UChar* dest, const char* src, size_t n);
extern size_t u_ucstombs(char* dest, const UChar* uSrc, size_t n);

#if defined(unixcli)&&defined(UNICODE)
extern int32_t u_sprintf_conv(UChar* ucs, const UChar* format, ...);
extern int32_t u_vfprintf_conv(UFILE* ufile, const UChar* format, va_list ap);
extern int32_t u_fprintf_conv(UFILE* ufile, const UChar* format, ...);
extern int32_t u_printf_conv(const UChar* format, ...);
extern UChar* replace_sToS(const UChar* format);
#endif

#ifdef __cplusplus
}
#endif

#endif
