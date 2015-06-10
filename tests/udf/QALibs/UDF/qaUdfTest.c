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

#include "sqludr.h"
#include <time.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include "sqlcli.h"

const char ERROR_STATE[] = "38001";
const char ERROR_STATE_STR[] = "ERROR:";

#define OUT_EQUAL_IN_SVF \
  if (calltype == SQLUDR_CALLTYPE_FINAL) \
    return SQLUDR_SUCCESS; \
  if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL) \
    SQLUDR_SETNULLIND(outInd); \
  else \
    *out = *in; \
  return SQLUDR_SUCCESS;

#define OUT_EQUAL_IN_MVF \
  if (calltype == SQLUDR_CALLTYPE_FINAL) \
    return SQLUDR_SUCCESS; \
  if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL) \
  { \
    SQLUDR_SETNULLIND(outInd1); \
    SQLUDR_SETNULLIND(outInd2); \
  } \
  else \
  { \
    *out1 = *in; \
    *out2 = *in; \
  } \
  return SQLUDR_SUCCESS;

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_int16 (
  SQLUDR_INT16 *in,
  SQLUDR_INT16 *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_uint16 (
  SQLUDR_UINT16 *in,
  SQLUDR_UINT16 *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_int32 (
  SQLUDR_INT32 *in,
  SQLUDR_INT32 *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_uint32 (
  SQLUDR_UINT32 *in,
  SQLUDR_UINT32 *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_int64 (
  SQLUDR_INT64 *in,
  SQLUDR_INT64 *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_char (
  SQLUDR_CHAR *in,
  SQLUDR_CHAR *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;

  if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL)
    SQLUDR_SETNULLIND(outInd);
  else
    memcpy (out, in, udrinfo->inputs->data_len);

  return SQLUDR_SUCCESS;
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_vcstruct (
  SQLUDR_VC_STRUCT *in,
  SQLUDR_VC_STRUCT *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;

  if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL)
    SQLUDR_SETNULLIND(outInd);
  else
  {
    memcpy (out->data, in->data, in->length);
    out->length = in->length;
  }

  return SQLUDR_SUCCESS;
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_real (
  SQLUDR_REAL *in,
  SQLUDR_REAL *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}


SQLUDR_LIBFUNC SQLUDR_DOUBLE qa_func_double (
  SQLUDR_DOUBLE *in,
  SQLUDR_DOUBLE *out,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_SVF
}

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_int16_mvf (
  SQLUDR_INT16 *in,
  SQLUDR_INT16 *out1,
  SQLUDR_INT16 *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_uint16_mvf (
  SQLUDR_UINT16 *in,
  SQLUDR_UINT16 *out1,
  SQLUDR_UINT16 *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_int32_mvf (
  SQLUDR_INT32 *in,
  SQLUDR_INT32 *out1,
  SQLUDR_INT32 *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_uint32_mvf (
  SQLUDR_UINT32 *in,
  SQLUDR_UINT32 *out1,
  SQLUDR_UINT32 *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_int64_mvf (
  SQLUDR_INT64 *in,
  SQLUDR_INT64 *out1,
  SQLUDR_INT64 *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_char_mvf (
  SQLUDR_CHAR *in,
  SQLUDR_CHAR *out1,
  SQLUDR_CHAR *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;

  if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL)
  {
    SQLUDR_SETNULLIND(outInd1);
    SQLUDR_SETNULLIND(outInd2);
  }
  else
  {
    memcpy (out1, in, udrinfo->inputs->data_len);
    memcpy (out2, in, udrinfo->inputs->data_len);
  }
  return SQLUDR_SUCCESS;
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_vcstruct_mvf (
  SQLUDR_VC_STRUCT *in,
  SQLUDR_VC_STRUCT *out1,
  SQLUDR_VC_STRUCT *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;

  if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL)
  {
    SQLUDR_SETNULLIND(outInd1);
    SQLUDR_SETNULLIND(outInd2);
  }
  else
  {
    memcpy(out1->data, in->data, in->length);
    out1->length = in->length;
    memcpy(out2->data, in->data, in->length);
    out2->length = in->length;
  }

  return SQLUDR_SUCCESS;
}


SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_real_mvf (
  SQLUDR_REAL *in,
  SQLUDR_REAL *out1,
  SQLUDR_REAL *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}


SQLUDR_LIBFUNC SQLUDR_DOUBLE qa_func_double_mvf (
  SQLUDR_DOUBLE *in,
  SQLUDR_DOUBLE *out1,
  SQLUDR_DOUBLE *out2,
  SQLUDR_INT16 *inInd,
  SQLUDR_INT16 *outInd1,
  SQLUDR_INT16 *outInd2,
  SQLUDR_TRAIL_ARGS)
{
  OUT_EQUAL_IN_MVF
}


#define ADD_VAL(count,val,inInd) \
if (SQLUDR_GETNULLIND(inInd) == SQLUDR_NULL) \
  count += 0; \
else \
  count += *val;

/*
 * 32 parameters (31 input + 1 output).  A UDF is allowed to have up to 32
 * 32 parameters, so this should work.
 */
SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_32_parameters (
  SQLUDR_INT32 *i1, SQLUDR_INT32 *i2, SQLUDR_INT32 *i3, SQLUDR_INT32 *i4,
  SQLUDR_INT32 *i5, SQLUDR_INT32 *i6, SQLUDR_INT32 *i7, SQLUDR_INT32 *i8,
  SQLUDR_INT32 *i9, SQLUDR_INT32 *i10, SQLUDR_INT32 *i11, SQLUDR_INT32 *i12,
  SQLUDR_INT32 *i13, SQLUDR_INT32 *i14, SQLUDR_INT32 *i15, SQLUDR_INT32 *i16,
  SQLUDR_INT32 *i17, SQLUDR_INT32 *i18, SQLUDR_INT32 *i19, SQLUDR_INT32 *i20,
  SQLUDR_INT32 *i21, SQLUDR_INT32 *i22, SQLUDR_INT32 *i23, SQLUDR_INT32 *i24,
  SQLUDR_INT32 *i25, SQLUDR_INT32 *i26, SQLUDR_INT32 *i27, SQLUDR_INT32 *i28,
  SQLUDR_INT32 *i29, SQLUDR_INT32 *i30, SQLUDR_INT32 *i31, 
  SQLUDR_INT32 *o,
  SQLUDR_INT16 *d1, SQLUDR_INT16 *d2, SQLUDR_INT16 *d3, SQLUDR_INT16 *d4,
  SQLUDR_INT16 *d5, SQLUDR_INT16 *d6, SQLUDR_INT16 *d7, SQLUDR_INT16 *d8,
  SQLUDR_INT16 *d9, SQLUDR_INT16 *d10, SQLUDR_INT16 *d11, SQLUDR_INT16 *d12,
  SQLUDR_INT16 *d13, SQLUDR_INT16 *d14, SQLUDR_INT16 *d15, SQLUDR_INT16 *d16,
  SQLUDR_INT16 *d17, SQLUDR_INT16 *d18, SQLUDR_INT16 *d19, SQLUDR_INT16 *d20,
  SQLUDR_INT16 *d21, SQLUDR_INT16 *d22, SQLUDR_INT16 *d23, SQLUDR_INT16 *d24,
  SQLUDR_INT16 *d25, SQLUDR_INT16 *d26, SQLUDR_INT16 *d27, SQLUDR_INT16 *d28,
  SQLUDR_INT16 *d29, SQLUDR_INT16 *d30, SQLUDR_INT16 *d31, 
  SQLUDR_INT16 *od,
  SQLUDR_TRAIL_ARGS)
{
  int count = 0;

  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;

  ADD_VAL(count,i1,d1) ADD_VAL(count,i2,d2) ADD_VAL(count,i3,d3)
  ADD_VAL(count,i4,d4) ADD_VAL(count,i5,d5) ADD_VAL(count,i6,d6)
  ADD_VAL(count,i7,d7) ADD_VAL(count,i8,d8) ADD_VAL(count,i9,d9)
  ADD_VAL(count,i10,d10) ADD_VAL(count,i11,d11) ADD_VAL(count,i12,d12)
  ADD_VAL(count,i13,d13) ADD_VAL(count,i14,d14) ADD_VAL(count,i15,d15)
  ADD_VAL(count,i16,d16) ADD_VAL(count,i17,d17) ADD_VAL(count,i18,d18)
  ADD_VAL(count,i19,d19) ADD_VAL(count,i20,d20) ADD_VAL(count,i21,d21)
  ADD_VAL(count,i22,d22) ADD_VAL(count,i23,d23) ADD_VAL(count,i24,d24)
  ADD_VAL(count,i25,d25) ADD_VAL(count,i26,d26) ADD_VAL(count,i27,d27)
  ADD_VAL(count,i28,d28) ADD_VAL(count,i29,d29) ADD_VAL(count,i30,d30)
  ADD_VAL(count,i31,d31) 

  *o = count;

  return SQLUDR_SUCCESS;
}

/*
 * 33 parameters (32 input + 1 output).  A UDF is only allowed to have up
 * to 32 parameters, so this is going to fail.
 */
SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_33_parameters (
  SQLUDR_INT32 *i1, SQLUDR_INT32 *i2, SQLUDR_INT32 *i3, SQLUDR_INT32 *i4,
  SQLUDR_INT32 *i5, SQLUDR_INT32 *i6, SQLUDR_INT32 *i7, SQLUDR_INT32 *i8,
  SQLUDR_INT32 *i9, SQLUDR_INT32 *i10, SQLUDR_INT32 *i11, SQLUDR_INT32 *i12,
  SQLUDR_INT32 *i13, SQLUDR_INT32 *i14, SQLUDR_INT32 *i15, SQLUDR_INT32 *i16,
  SQLUDR_INT32 *i17, SQLUDR_INT32 *i18, SQLUDR_INT32 *i19, SQLUDR_INT32 *i20,
  SQLUDR_INT32 *i21, SQLUDR_INT32 *i22, SQLUDR_INT32 *i23, SQLUDR_INT32 *i24,
  SQLUDR_INT32 *i25, SQLUDR_INT32 *i26, SQLUDR_INT32 *i27, SQLUDR_INT32 *i28,
  SQLUDR_INT32 *i29, SQLUDR_INT32 *i30, SQLUDR_INT32 *i31, SQLUDR_INT32 *i32,
  SQLUDR_INT32 *o,
  SQLUDR_INT16 *d1, SQLUDR_INT16 *d2, SQLUDR_INT16 *d3, SQLUDR_INT16 *d4,
  SQLUDR_INT16 *d5, SQLUDR_INT16 *d6, SQLUDR_INT16 *d7, SQLUDR_INT16 *d8,
  SQLUDR_INT16 *d9, SQLUDR_INT16 *d10, SQLUDR_INT16 *d11, SQLUDR_INT16 *d12,
  SQLUDR_INT16 *d13, SQLUDR_INT16 *d14, SQLUDR_INT16 *d15, SQLUDR_INT16 *d16,
  SQLUDR_INT16 *d17, SQLUDR_INT16 *d18, SQLUDR_INT16 *d19, SQLUDR_INT16 *d20,
  SQLUDR_INT16 *d21, SQLUDR_INT16 *d22, SQLUDR_INT16 *d23, SQLUDR_INT16 *d24,
  SQLUDR_INT16 *d25, SQLUDR_INT16 *d26, SQLUDR_INT16 *d27, SQLUDR_INT16 *d28,
  SQLUDR_INT16 *d29, SQLUDR_INT16 *d30, SQLUDR_INT16 *d31, SQLUDR_INT16 *d32,
  SQLUDR_INT16 *od,
  SQLUDR_TRAIL_ARGS)
{
  int count = 0;

  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;

  ADD_VAL(count,i1,d1) ADD_VAL(count,i2,d2) ADD_VAL(count,i3,d3)
  ADD_VAL(count,i4,d4) ADD_VAL(count,i5,d5) ADD_VAL(count,i6,d6)
  ADD_VAL(count,i7,d7) ADD_VAL(count,i8,d8) ADD_VAL(count,i9,d9)
  ADD_VAL(count,i10,d10) ADD_VAL(count,i11,d11) ADD_VAL(count,i12,d12)
  ADD_VAL(count,i13,d13) ADD_VAL(count,i14,d14) ADD_VAL(count,i15,d15)
  ADD_VAL(count,i16,d16) ADD_VAL(count,i17,d17) ADD_VAL(count,i18,d18)
  ADD_VAL(count,i19,d19) ADD_VAL(count,i20,d20) ADD_VAL(count,i21,d21)
  ADD_VAL(count,i22,d22) ADD_VAL(count,i23,d23) ADD_VAL(count,i24,d24)
  ADD_VAL(count,i25,d25) ADD_VAL(count,i26,d26) ADD_VAL(count,i27,d27)
  ADD_VAL(count,i28,d28) ADD_VAL(count,i29,d29) ADD_VAL(count,i30,d30)
  ADD_VAL(count,i31,d31) ADD_VAL(count,i32,d32)

  *o = count;

  return SQLUDR_SUCCESS;
}


// internal helper
static SQLUDR_INT32 test_udf_schema (
  SQLUDR_CHAR *out,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS,
  const char *ret)
{
  char errmsg[1024];

  /* Make sure the paramater stype is for UDF. */
  if (udrinfo->param_style != SQLUDR_PARAMSTYLE_SQL)
    {
      sprintf (errmsg, "Invalid parameter style %d\n", udrinfo->param_style);
      goto err;
    }

  if (calltype == SQLUDR_CALLTYPE_FINAL)
    return SQLUDR_SUCCESS;
  memset(out, ' ', sizeof(out));
  memcpy(out, ret, strlen(ret));

  return SQLUDR_SUCCESS;

err:
  strcpy (sqlstate, ERROR_STATE);
  sprintf (msgtext, "%s (UDF: %s) %s",
           ERROR_STATE_STR, udrinfo->routine_name, errmsg);
  return SQLUDR_ERROR;
}

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_schema_0 (
  SQLUDR_CHAR *out,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  return test_udf_schema (out,
                          outInd,
                          sqlstate,
                          msgtext,
                          calltype,
                          statearea,
                          udrinfo,
                          "SCHEMA 0" );
}

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_schema_1 (
  SQLUDR_CHAR *out,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  return test_udf_schema (out,
                          outInd,
                          sqlstate,
                          msgtext,
                          calltype,
                          statearea,
                          udrinfo,
                          "SCHEMA 1" );
}

SQLUDR_LIBFUNC SQLUDR_INT32 qa_func_schema_2 (
  SQLUDR_CHAR *out,
  SQLUDR_INT16 *outInd,
  SQLUDR_TRAIL_ARGS)
{
  return test_udf_schema (out,
                          outInd,
                          sqlstate,
                          msgtext,
                          calltype,
                          statearea,
                          udrinfo,
                          "SCHEMA 2" );
}

