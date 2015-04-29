#ifndef _TEST_TYPEDEF_H_
#define _TEST_TYPEDEF_H_
#include <stddef.h>

#include "test_typedef_external.h"


/* Test standard typedefs in the same file. */

typedef int newtype1_t;

typedef newtype1_t newtype2_t;

typedef newtype2_t newtype3_t;

typedef newtype3_t newtype4_t;

typedef newtype4_t newtype5_t;

/* Test external typedefs. These will also be added to the Stitched class */

typedef externtype1_t localtype1_t;

typedef externtype2_t localtype2_t;

typedef externtype3_t localtype3_t;

typedef localtype1_t newlocaltype_t;

/* Test typedefs from stdlib */

typedef size_t stdtype;

#endif
