// Copyright 2016 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
// Modified by Jeremy Retailleau.

#include "./size3.h"

#include <pxr/tf/type.h>

#include <ostream>

namespace pxr {

TF_REGISTRY_FUNCTION(pxr::TfType) {
    TfType::Define<GfSize3>();
}


//  This should probably be moved to ostreamMethods.cpp
//! Output operator
std::ostream &operator<<(std::ostream &o, GfSize3 const &v) {
    return o << "( " << v._vec[0] << " " << v._vec[1] << " " <<
        v._vec[2] << " )";
}

}  // namespace pxr
