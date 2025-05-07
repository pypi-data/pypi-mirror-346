//     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file

#ifndef __BloodSx_COMPILED_CELL_H__
#define __BloodSx_COMPILED_CELL_H__

/* This is a clone of the normal PyCell structure. We should keep it binary
 * compatible, just in case somebody crazy insists on it.
 */

extern PyTypeObject BloodQ_Cell_Type;

static inline bool BloodQ_Cell_Check(PyObject *object) { return Py_TYPE(object) == &BloodQ_Cell_Type; }

struct BloodQ_CellObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* Content of the cell or NULL when empty */
        PyObject *ob_ref;
};

// Create cell with out value, and with or without reference given.
extern struct BloodQ_CellObject *BloodQ_Cell_NewEmpty(void);
extern struct BloodQ_CellObject *BloodQ_Cell_New0(PyObject *value);
extern struct BloodQ_CellObject *BloodQ_Cell_New1(PyObject *value);

// Check stuff while accessing a compile cell in debug mode.
#ifdef __BloodSx_NO_ASSERT__
#define BloodQ_Cell_GET(cell) (((struct BloodQ_CellObject *)(cell))->ob_ref)
#else
#define BloodQ_Cell_GET(cell)                                                                                          \
    (CHECK_OBJECT(cell), assert(BloodQ_Cell_Check((PyObject *)cell)), (((struct BloodQ_CellObject *)(cell))->ob_ref))
#endif

#if _DEBUG_REFCOUNTS
extern int count_active_BloodQ_Cell_Type;
extern int count_allocated_BloodQ_Cell_Type;
extern int count_released_BloodQ_Cell_Type;
#endif

BloodSx_MAY_BE_UNUSED static inline void BloodQ_Cell_SET(struct BloodQ_CellObject *cell_object, PyObject *value) {
    CHECK_OBJECT_X(value);
    CHECK_OBJECT(cell_object);

    assert(BloodQ_Cell_Check((PyObject *)cell_object));
    cell_object->ob_ref = value;
}

#endif


