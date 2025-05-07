//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_SETS_H__
#define __BloodSx_SETS_H__

// This is not Python headers before 3.10, but we use it in our assertions.
#if PYTHON_VERSION < 0x3a0
#define PySet_CheckExact(op) (Py_TYPE(op) == &PySet_Type)
#endif

#endif

