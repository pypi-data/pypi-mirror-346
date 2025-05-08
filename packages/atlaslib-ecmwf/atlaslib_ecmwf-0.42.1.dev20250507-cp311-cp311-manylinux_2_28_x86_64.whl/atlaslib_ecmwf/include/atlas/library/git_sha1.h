/*
 * (C) Copyright 2013 ECMWF.
 *
 * This software is licensed under the terms of the Apache Licence Version 2.0
 * which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
 * In applying this licence, ECMWF does not waive the privileges and immunities
 * granted to it by virtue of its status as an intergovernmental organisation
 * nor does it submit to any jurisdiction.
 */

#pragma once

#define ATLAS_GIT_SHA1 "7a3b05744ce76b619bc1b6437be029675cd57187"

#include <algorithm>
#include <string>

namespace atlas {
namespace library {
inline const char* git_sha1( unsigned int chars = 7 ) {
    static std::string sha1( ATLAS_GIT_SHA1 );
    if ( sha1.empty() ) { return "not available"; }
    sha1 = sha1.substr( 0, std::min( chars, 40u ) );
    return sha1.c_str();
}
}  // namespace library
}  // namespace atlas
