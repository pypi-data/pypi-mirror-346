// Copyright 2016 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
// Modified by Jeremy Retailleau.

#ifndef PXR_GF_PY_BUFFER_UTILS_H
#define PXR_GF_PY_BUFFER_UTILS_H

#include "./api.h"

namespace pxr {

////////////////////////////////////////////////////////////////////////
// Format strings matching Python buffer proto / struct module scheme.

// This function template is explicitly instantiated for T =
//    bool, [unsigned] (char, short, int, long), half, float, and double.
template <class T>
char *Gf_GetPyBufferFmtFor();

}  // namespace pxr

#endif // PXR_GF_PY_BUFFER_UTILS_H
