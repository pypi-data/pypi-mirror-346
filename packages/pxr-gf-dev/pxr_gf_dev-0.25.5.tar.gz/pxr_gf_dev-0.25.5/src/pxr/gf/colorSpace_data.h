// Copyright 2024 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
// Modified by Jeremy Retailleau.

namespace pxr {

struct GfColorSpace::_Data
{
    ~_Data() {
        NcFreeColorSpace(colorSpace);
    }

    const NcColorSpace* colorSpace = nullptr;
};

}  // namespace pxr
