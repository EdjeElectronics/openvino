// Copyright (C) 2023 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include <gtest/gtest.h>

#include "any_copy.hpp"
#include <ie_system_conf.h>
#include "ngraph_functions/builders.hpp"

#include "gna_executable_network.hpp"
#include "gna_plugin.hpp"
#include "memory/gna_memory.hpp"

using namespace ov::intel_gna;
using namespace InferenceEngine;


class GNAPluginForNetworkMetricsTest : public GNAPlugin {
public:
    GNAPluginForNetworkMetricsTest(const std::map<std::string, std::string>& configMap) : GNAPlugin(configMap) {
        gnamem.reset(new gna_memory_float(memory::GNAFloatAllocator{}));
        graphCompiler.setGNAMemoryPtr(gnamem);
        gnadevice.reset();
    }
};

class GnaExecutableNetworkMetricsTest : public ::testing::Test {
public:
    void Run(const std::string& metricName, const std::string& expectedResult) {
        ov::AnyMap gnaConfig = {
            ov::intel_gna::execution_mode(ov::intel_gna::ExecutionMode::SW_EXACT),
        };
        auto plugin = std::make_shared<GNAPluginForNetworkMetricsTest>(ov::any_copy(gnaConfig));
        auto function = getFunction();
        CNNNetwork cnnNetwork(function);
        GNAExecutableNetwork gnaNetwork = GNAExecutableNetwork(cnnNetwork, plugin);
        std::string result = gnaNetwork.GetMetric(metricName);
        ASSERT_EQ(result, expectedResult);
    }

protected:
    std::shared_ptr<ov::Model> getFunction() {
        auto firstInput = std::make_shared<ngraph::opset8::Parameter>(net_precision, shape);
        auto secondInput = std::make_shared<ngraph::opset8::Constant>(net_precision, shape);
        auto matmul = std::make_shared<ngraph::opset8::MatMul>(firstInput, secondInput, false, true);
        auto result = std::make_shared<ngraph::opset8::Result>(matmul);
        auto function =
            std::make_shared<ov::Model>(ov::ResultVector({result}), ov::ParameterVector({firstInput}), "MatMul");
        return function;
    }
    const ngraph::element::Type net_precision = ngraph::element::f32;
    const ngraph::Shape shape = {1, 10};
};


TEST_F(GnaExecutableNetworkMetricsTest, TestNetworkName) {
    Run(ov::model_name.name(), "MatMul");
}

TEST_F(GnaExecutableNetworkMetricsTest, TestSupportedProperties) {
    std::string supportedProperties =
        "SUPPORTED_PROPERTIES AVAILABLE_DEVICES OPTIMAL_NUMBER_OF_INFER_REQUESTS RANGE_FOR_ASYNC_INFER_REQUESTS "
        "OPTIMIZATION_CAPABILITIES FULL_DEVICE_NAME GNA_LIBRARY_FULL_VERSION CACHING_PROPERTIES "
        "GNA_DEVICE_MODE PERFORMANCE_HINT LOG_LEVEL EXECUTION_DEVICES CACHE_DIR "
        "GNA_SCALE_FACTOR_PER_INPUT GNA_FIRMWARE_MODEL_IMAGE GNA_HW_EXECUTION_TARGET GNA_HW_COMPILE_TARGET "
        "GNA_PWL_DESIGN_ALGORITHM GNA_PWL_MAX_ERROR_PERCENT INFERENCE_PRECISION_HINT PERFORMANCE_HINT_NUM_REQUESTS";
    Run(ov::supported_properties.name(), supportedProperties);
}
