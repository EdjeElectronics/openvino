// Copyright (C) 2018-2022 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include "permute_inst.h"
#include "primitive_base.hpp"
#include "impls/implementation_map.hpp"
#include "intel_gpu/runtime/error_handler.hpp"
#include "kernel_selector_helper.h"
#include "permute/permute_kernel_selector.h"
#include "permute/permute_kernel_ref.h"

using namespace cldnn;

namespace cldnn {
namespace ocl {

namespace {
// This helper function is needed to convert permute order from IE format (bfyx) into cldnn format (bfxy)
inline std::vector<uint16_t> convert_permute_order(const std::vector<uint16_t>& ie_order, size_t rank = 0) {
    std::vector<uint16_t> ie_order_aligned = ie_order;
    // if order size is less than 4 - fill the rest with just copy
    rank = std::max(rank, (size_t)4);
    for (auto o = ie_order_aligned.size(); o < rank; o++)
        ie_order_aligned.push_back((uint16_t)o);

    std::vector<uint16_t> cldnn_order;
    // 1. Switch permute order values for spatial dims
    for (auto const& o : ie_order_aligned) {
        if (o >= 2)
            cldnn_order.push_back(1 + ie_order_aligned.size() - o);
        else
            cldnn_order.push_back(o);
    }

    // 2. Swap spatial positions
    for (int i = 0; i < (static_cast<int>(cldnn_order.size()) - 2) / 2; i++) {
        std::swap(cldnn_order[2 + i], cldnn_order[1 + cldnn_order.size() - (2 + i)]);
    }

    return cldnn_order;
}
}  // namespace

struct permute_impl : typed_primitive_impl_ocl<permute> {
    using parent = typed_primitive_impl_ocl<permute>;
    using parent::parent;
    using kernel_selector_t = kernel_selector::permute_kernel_selector;
    using kernel_params_t = std::pair<kernel_selector::permute_params, kernel_selector::permute_optional_params>;

    DECLARE_OBJECT_TYPE_SERIALIZATION

    std::unique_ptr<primitive_impl> clone() const override {
        return make_unique<permute_impl>(*this);
    }

    static kernel_params_t get_kernel_params(const kernel_impl_params& impl_param) {
        const auto& primitive = impl_param.typed_desc<permute>();
        auto params = get_default_params<kernel_selector::permute_params>(impl_param);
        auto optional_params = get_default_optional_params<kernel_selector::permute_optional_params>(impl_param.get_program());

        auto in_rank = impl_param.get_input_layout(0).get_rank();
        auto permute_order = convert_permute_order(primitive->permute_order, in_rank);
        params.order = permute_order;

        return {params, optional_params};
    }
};

namespace detail {

attach_permute_impl::attach_permute_impl() {
    implementation_map<permute>::add(impl_types::ocl, typed_primitive_impl_ocl<permute>::create<permute_impl>, {});
}

}  // namespace detail
}  // namespace ocl
}  // namespace cldnn

BIND_BINARY_BUFFER_WITH_TYPE(cldnn::ocl::permute_impl, cldnn::object_type::PERMUTE_IMPL)
