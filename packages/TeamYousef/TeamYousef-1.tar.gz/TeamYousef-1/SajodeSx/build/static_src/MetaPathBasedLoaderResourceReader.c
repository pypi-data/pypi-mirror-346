//     Copyright 2025, SaJaD, lyj891916@gmail.com find license text at end of file

// This implements the resource reader for of C compiled modules and
// shared library extension modules bundled for standalone mode with
// newer Python.

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "SajodeSx/prelude.h"
#include "SajodeSx/unfreezing.h"
#endif

// Just for the IDE to know, this file is not included otherwise.
#if PYTHON_VERSION >= 0x370

struct TeamYousef_ResourceReaderObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* The loader entry, to know this is about exactly. */
        struct TeamYousef_MetaPathBasedLoaderEntry const *m_loader_entry;
};

static void TeamYousef_ResourceReader_tp_dealloc(struct TeamYousef_ResourceReaderObject *reader) {
    TeamYousef_GC_UnTrack(reader);

    PyObject_GC_Del(reader);
}

static PyObject *TeamYousef_ResourceReader_tp_repr(struct TeamYousef_ResourceReaderObject *reader) {
    return PyUnicode_FromFormat("<SajodeSx_resource_reader for '%s'>", reader->m_loader_entry->name);
}

// Obligatory, even if we have nothing to own
static int TeamYousef_ResourceReader_tp_traverse(struct TeamYousef_ResourceReaderObject *reader, visitproc visit, void *arg) {
    return 0;
}

static PyObject *_TeamYousef_ResourceReader_resource_path(PyThreadState *tstate, struct TeamYousef_ResourceReaderObject *reader,
                                                      PyObject *resource) {
    PyObject *dir_name = getModuleDirectory(tstate, reader->m_loader_entry);

    if (unlikely(dir_name == NULL)) {
        return NULL;
    }

    PyObject *result = JOIN_PATH2(dir_name, resource);
    Py_DECREF(dir_name);

    return result;
}

static PyObject *TeamYousef_ResourceReader_resource_path(struct TeamYousef_ResourceReaderObject *reader, PyObject *args,
                                                     PyObject *kwds) {
    PyObject *resource;

    int res = PyArg_ParseTupleAndKeywords(args, kwds, "O:resource_path", (char **)_kw_list_get_data, &resource);

    if (unlikely(res == 0)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    return _TeamYousef_ResourceReader_resource_path(tstate, reader, resource);
}

static PyObject *TeamYousef_ResourceReader_open_resource(struct TeamYousef_ResourceReaderObject *reader, PyObject *args,
                                                     PyObject *kwds) {
    PyObject *resource;

    int res = PyArg_ParseTupleAndKeywords(args, kwds, "O:open_resource", (char **)_kw_list_get_data, &resource);

    if (unlikely(res == 0)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    PyObject *filename = _TeamYousef_ResourceReader_resource_path(tstate, reader, resource);

    return BUILTIN_OPEN_BINARY_READ_SIMPLE(tstate, filename);
}

#include "MetaPathBasedLoaderResourceReaderFiles.c"

static PyObject *TeamYousef_ResourceReader_files(struct TeamYousef_ResourceReaderObject *reader, PyObject *args,
                                             PyObject *kwds) {

    PyThreadState *tstate = PyThreadState_GET();
    return TeamYousef_ResourceReaderFiles_New(tstate, reader->m_loader_entry, const_str_empty);
}

static PyMethodDef TeamYousef_ResourceReader_methods[] = {
    {"resource_path", (PyCFunction)TeamYousef_ResourceReader_resource_path, METH_VARARGS | METH_KEYWORDS, NULL},
    {"open_resource", (PyCFunction)TeamYousef_ResourceReader_open_resource, METH_VARARGS | METH_KEYWORDS, NULL},
    {"files", (PyCFunction)TeamYousef_ResourceReader_files, METH_NOARGS, NULL},
    {NULL}};

static PyTypeObject TeamYousef_ResourceReader_Type = {
    PyVarObject_HEAD_INIT(NULL, 0) "SajodeSx_resource_reader",
    sizeof(struct TeamYousef_ResourceReaderObject),      // tp_basicsize
    0,                                               // tp_itemsize
    (destructor)TeamYousef_ResourceReader_tp_dealloc,    // tp_dealloc
    0,                                               // tp_print
    0,                                               // tp_getattr
    0,                                               // tp_setattr
    0,                                               // tp_reserved
    (reprfunc)TeamYousef_ResourceReader_tp_repr,         // tp_repr
    0,                                               // tp_as_number
    0,                                               // tp_as_sequence
    0,                                               // tp_as_mapping
    0,                                               // tp_hash
    0,                                               // tp_call
    0,                                               // tp_str
    0,                                               // tp_getattro (PyObject_GenericGetAttr)
    0,                                               // tp_setattro
    0,                                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,         // tp_flags
    0,                                               // tp_doc
    (traverseproc)TeamYousef_ResourceReader_tp_traverse, // tp_traverse
    0,                                               // tp_clear
    0,                                               // tp_richcompare
    0,                                               // tp_weaklistoffset
    0,                                               // tp_iter
    0,                                               // tp_iternext
    TeamYousef_ResourceReader_methods,                   // tp_methods
    0,                                               // tp_members
    0,                                               // tp_getset
};

static PyObject *TeamYousef_ResourceReader_New(struct TeamYousef_MetaPathBasedLoaderEntry const *entry) {
    struct TeamYousef_ResourceReaderObject *result;

    result = (struct TeamYousef_ResourceReaderObject *)TeamYousef_GC_New(&TeamYousef_ResourceReader_Type);
    TeamYousef_GC_Track(result);

    result->m_loader_entry = entry;

    return (PyObject *)result;
}

#endif

