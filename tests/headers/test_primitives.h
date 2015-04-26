#ifndef _TEST_PRIMITIVES_H_
#define _TEST_PRIMITIVES_H_
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/* Basic primitive types */
_Bool bool_val;

char char_val;
signed char schar_val;
unsigned char uchar_val;

short short_val;
unsigned short ushort_val;

int int_val;
unsigned int uint_val;

long long_val;
unsigned long ulong_val;

long long longlong_val;
unsigned long long ulonglong_val;

float float_val;
double double_val;
long double ldouble_val;

intmax_t intmax_t_val;
size_t size_t_val;


/* Typedef'd types */
typedef int INT;
typedef float FLOAT32;

INT tdint;
FLOAT32 tdfloat;


/* Const modifiers */
const _Bool const_bool_val;

const char const_char_val;
const signed char const_schar_val;
const unsigned char const_uchar_val;

const short const_short_val;
const unsigned short const_ushort_val;

const int const_int_val;
const unsigned int const_uint_val;

const long const_long_val;
const unsigned long const_ulong_val;

const long long const_longlong_val;
unsigned long long const_ulonglong_val;

const float const_float_val;
const double const_double_val;
const long double const_ldouble_val;

const intmax_t const_intmax_t_val;
const size_t const_size_t_val;

const INT const_tdint;
const FLOAT32 const_tdfloat;


/* Pointers */


/* Const pointers */


/* Pointers to pointers */


/* Externs */


#endif
