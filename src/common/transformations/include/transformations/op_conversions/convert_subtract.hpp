// Copyright (C) 2018-2022 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#pragma once

#include <memory>
#include <openvino/pass/graph_rewrite.hpp>
#include <transformations_visibility.hpp>
#include <vector>

namespace ov {
namespace pass {

class TRANSFORMATIONS_API ConvertSubtract;

}  // namespace pass
}  // namespace ov

class ov::pass::ConvertSubtract : public ov::pass::MatcherPass {
public:
    OPENVINO_RTTI("ConvertSubtract", "0");
    ConvertSubtract();
};

namespace ngraph {
namespace pass {
using ov::pass::ConvertSubtract;
}  // namespace pass
}  // namespace ngraph
