//     Copyright 2025, SaJaD, lyj891916@gmail.com find license text at end of file

#ifndef __SAJODE_COMPILED_CELL_H__
#define __SAJODE_COMPILED_CELL_H__

/* This is a clone of the normal PyCell structure. We should keep it binary
 * compatible, just in case somebody crazy insists on it.
 */

extern PyTypeObject TeamYousef_Cell_Type;

static inline bool TeamYousef_Cell_Check(PyObject *object) { return Py_TYPE(object) == &TeamYousef_Cell_Type; }

struct TeamYousef_CellObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* Content of the cell or NULL when empty */
        PyObject *ob_ref;
};

// Create cell with out value, and with or without reference given.
extern struct TeamYousef_CellObject *TeamYousef_Cell_NewEmpty(void);
extern struct TeamYousef_CellObject *TeamYousef_Cell_New0(PyObject *value);
extern struct TeamYousef_CellObject *TeamYousef_Cell_New1(PyObject *value);

// Check stuff while accessing a compile cell in debug mode.
#ifdef __SAJODE_NO_ASSERT__
#define TeamYousef_Cell_GET(cell) (((struct TeamYousef_CellObject *)(cell))->ob_ref)
#else
#define TeamYousef_Cell_GET(cell)                                                                                          \
    (CHECK_OBJECT(cell), assert(TeamYousef_Cell_Check((PyObject *)cell)), (((struct TeamYousef_CellObject *)(cell))->ob_ref))
#endif

#if _DEBUG_REFCOUNTS
extern int count_active_TeamYousef_Cell_Type;
extern int count_allocated_TeamYousef_Cell_Type;
extern int count_released_TeamYousef_Cell_Type;
#endif

SAJODE_MAY_BE_UNUSED static inline void TeamYousef_Cell_SET(struct TeamYousef_CellObject *cell_object, PyObject *value) {
    CHECK_OBJECT_X(value);
    CHECK_OBJECT(cell_object);

    assert(TeamYousef_Cell_Check((PyObject *)cell_object));
    cell_object->ob_ref = value;
}

#endif


