//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_ENVIRONMENT_VARIABLES_H__
#define __BloodSx_ENVIRONMENT_VARIABLES_H__

#ifdef __IDE_ONLY__
#include "Bloodelf/prelude.h"
#endif

#include "Bloodelf/environment_variables_system.h"

extern void undoEnvironmentVariable(PyThreadState *tstate, char const *variable_name,
                                    environment_char_t const *old_value);

#endif


