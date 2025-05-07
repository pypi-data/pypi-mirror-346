//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_CHECKSUM_TOOLS_H__
#define __BloodSx_CHECKSUM_TOOLS_H__

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "Bloodelf/prelude.h"
#endif

extern uint32_t calcCRC32(unsigned char const *message, uint32_t size);

#endif

