# Copyright (C) 2020-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

from copy import deepcopy
from pathlib import Path

from scipy.stats import mode

from .range_estimator import get_range_estimator_config
from ...api.engine import Engine
from ...configs.hardware_config import HardwareConfig
from ...engines.ac_engine import ACEngine
from ...statistics.function_selector import ACTIVATIONS, WEIGHTS, get_stats_function, AGGREGATION_FN
from ...statistics.statistics import TensorStatistic

__HARDWARE_CONFIG_DIR = Path(__file__).parent.parent.parent.absolute() / 'configs' / 'hardware'

__HARDWARE_CONFIGS_MAP = {'ANY': 'cpu.json',
                          'CPU': 'cpu.json',
                          'GNA': 'gna.json',
                          'GNA3': 'gna3.json',
                          'GNA3.5': 'gna3.json',
                          'GPU': 'gpu.json',  # Same as cpu.json but without LSTM/GRUSequence quantization
                          'VPU': 'vpu.json',
                          'CPU_SPR': 'cpu.json'}


def load_hardware_config(config):
    """ Loads hardware config based on tool config
    :return hardware config dict
    """
    if config['target_device'] is not None and __HARDWARE_CONFIGS_MAP.get(config['target_device']) is None:
        raise ValueError('Unsupported target_device : {}'.format(config['target_device']))

    hardware_config_path = __HARDWARE_CONFIG_DIR / __HARDWARE_CONFIGS_MAP.get(config['target_device'], "cpu.json")
    return HardwareConfig.from_json(hardware_config_path.as_posix())


def append_estimator_configs(quantization_configs, is_weights, config, opt_conf=None):
    """ Appends estimator configs to quantization configs of given operation
    :param quantization_configs: quantization configs of given operation read from hardware config
    :param is_weights: true if configuration is done for weights node
    :param config: the algorithm config
    :param opt_conf: optimal configuration from previous optimization runs
    :return: list of quantization configs with range estimator configs for given operation
             (based on hardware config and tuning scope)
    """

    def _generate_configs(base_estimator_config, param_name, values):
        """
        Generator function that derives new estimator configs from base one
        with specified values of a specific param
        :param base_estimator_config: base estimator config
        :param param_name: name of the parameter with new values
        :param values: new values for parameter
        :return: derived estimator configs one by one
        """
        for value in values:
            derived_estimator_config = deepcopy(base_estimator_config)
            derived_estimator_config[param_name] = value
            yield derived_estimator_config

    def _generate_type_values(key, _base_estimator_config):
        """
        Values generator function for type parameter
        :param key: estimated value name
        :param _base_estimator_config: base estimator config
        :return: list of values for type parameter
        """
        stats_functions = {
            'min': ['min', 'quantile'],
            'max': ['max', 'abs_max', 'quantile', 'abs_quantile']
        }
        return stats_functions[key]

    def _generate_outlier_prob_values(_key, base_estimator_config):
        """
        Values generator function for outlier_prob parameter
        :param _key: estimated value name
        :param base_estimator_config: base estimator config
        :return: list of values for outlier_prob parameter
        """
        if base_estimator_config['type'] in ['quantile', 'abs_quantile']:
            outlier_prob_values = config.outlier_prob_choices
        else:
            outlier_prob_values = [base_estimator_config['outlier_prob']]
        return outlier_prob_values

    def _extend_options(available_config_options, param_name, values, values_generator=None):
        """
        Extends available_config_options with new config options derived from existing ones, but with new values
        (optionally generated by values_generator function) of specified param_name.
        :param available_config_options: dict with estimated value name as key and list of available estimator
        config options as values
        :param param_name: name of config parameter to be extended with new values
        :param values: list of values for config parameter
        :param values_generator: optional function that generates new values depending on already available options
        :return: available_config_options extended with new options
        """
        new_available_config_options = {}
        for key, options in available_config_options.items():
            new_options = []
            for option in options:
                if values_generator:
                    values = values_generator(key, option)
                new_options.extend(list(_generate_configs(option, param_name, values)))
            new_available_config_options[key] = new_options
        return new_available_config_options

    def _merge_configs(available_config_options):
        """
        Merges available config options for min and max into complete estimator configs
        :param available_config_options: available config options for min and max estimators
        :return: list of complete estimator configs as a combination of all min options with all max options
        """
        merged_configs = []
        if len(available_config_options.keys()) == 1:
            key, values = list(available_config_options.items())[0]
            for value in values:
                merged_configs.append({key: value})
        else:
            for min_config in available_config_options['min']:
                for max_config in available_config_options['max']:
                    merged_configs.append({'min': min_config, 'max': max_config})
        return merged_configs

    def _create_estimator_configs(qconfig):
        tensor_type = 'weights' if is_weights else 'activations'
        default_config = get_range_estimator_config(config, tensor_type, qconfig['granularity'],
                                                    qconfig['mode'])
        if opt_conf is not None and tensor_type in opt_conf \
                and len(opt_conf[tensor_type]['range_estimator']) >= len(default_config):
            # Some configurations (e.g. weights symmetric quantization) do not have min and max estimator configs,
            # so we need to check opt_conf compatibility and either use default or limit the scope
            base_configs = [{key: value for key, value in opt_conf[tensor_type]['range_estimator'].items() if
                             key in default_config.keys()}]
        else:
            base_configs = [default_config]

        if 'estimator_preset' in config.tuning_scope:
            base_configs.extend([get_range_estimator_config(config, tensor_type, qconfig['granularity'],
                                                            qconfig['mode'], preset)
                                 for preset in ['default', 'quantile']])

        estimator_configs = []
        for base_config in base_configs:
            for value in base_config.values():
                if 'outlier_prob' not in value:
                    # Add default outlier_prob value to be used later if type is changed to quantile,
                    # but outlier_prob is not in tuning_scope
                    value['outlier_prob'] = 1e-4
            if base_config in estimator_configs:
                # If base_config is already in estimator_configs then below code will generate subset of options
                # already in estimator_configs
                continue
            available_config_options = {key: [value] for key, value in base_config.items()}
            if 'estimator_type' in config.tuning_scope:
                available_config_options = _extend_options(available_config_options, 'type', [None],
                                                           _generate_type_values)
            # outlier_prob config extension requires new types to be already added to config options
            if 'estimator_outlier_prob' in config.tuning_scope:
                available_config_options = _extend_options(available_config_options, 'outlier_prob', [None],
                                                           _generate_outlier_prob_values)
            if 'estimator_aggregator' in config.tuning_scope and not is_weights:
                available_config_options = _extend_options(available_config_options, 'aggregator',
                                                           list(AGGREGATION_FN.registry_dict.keys()))
            estimator_configs.extend(_merge_configs(available_config_options))

        return estimator_configs

    final_configs = []
    for quantization_config in quantization_configs:
        for estimator_config in _create_estimator_configs(quantization_config):
            final_configs.append({**quantization_config, 'range_estimator': estimator_config})
    return final_configs


def get_quantize_op_config(op, config, opt_conf=None):
    """
    Return the list of quantization params for given op
    :param op: the quantizable operation read from hardware config
    :param config: the algorithm config
    :param opt_conf: optimal configuration from previous optimization runs
    :return:
    """

    tuning_scope = config.tuning_scope

    def _select_options(confs_by_op, default_conf=None):
        options = []
        # if optimal conf is not provided choose default conf based on preset
        # all configurations are sorted per corresponded layer
        # the fastest is the first one and the most accurate it the last one
        if not default_conf:
            if 'preset' not in config or config['preset'] == 'performance':
                default_conf = confs_by_op[0]
            elif config['preset'] == 'accuracy':
                default_conf = confs_by_op[-1]
            else:
                raise Exception(
                    'Unsupported preset option: {}'.format(config['preset']))
        options.append(default_conf)

        # then add the other config based on tuning_scope
        def _get_conf(conf):
            new_in_scope = False
            new_out_scope = False
            for key in default_conf.keys():
                if key in ['level_low', 'level_high']:
                    continue
                l, r = (default_conf[key], conf[key])
                if key in tuning_scope and l != r:
                    new_in_scope = True
                elif key not in tuning_scope and l != r:
                    new_out_scope = True
            return conf if new_in_scope and not new_out_scope else default_conf

        for op_conf in confs_by_op:
            new_conf = _get_conf(op_conf)
            if new_conf and new_conf not in options:
                options.append(new_conf)
        return options

    def _merge_configs(qconfig, op_options, op_type):
        new_qconfig = []
        for qconf in qconfig:
            for option in op_options:
                new_qconfig.append({**qconf, op_type: option})
        return new_qconfig

    qconfig = []
    if opt_conf and opt_conf['quantize'] == 0:
        qconfig.append(opt_conf)
    else:
        act_options = _select_options(op['activations'], opt_conf['activations'] if opt_conf else None) if \
            len(op['activations']) > 0 else None
        wgt_options = _select_options(op['weights'], opt_conf['weights'] if opt_conf else None) if \
            len(op['weights']) > 0 else None
        qconfig.append({'quantize': 1})
        if act_options:
            qconfig = _merge_configs(qconfig, act_options, 'activations')
        if wgt_options:
            qconfig = _merge_configs(qconfig, wgt_options, 'weights')
        if 'layer' in tuning_scope:
            default_config = deepcopy(qconfig[0])
            default_config['quantize'] = 0
            qconfig.append(default_config)
    return qconfig


def get_tensor_statistics(range_estimator_config, for_weights, **kwargs):
    stats = {}
    for stats_name in ['min', 'max']:
        if stats_name not in range_estimator_config:
            continue

        fn_type = range_estimator_config[stats_name]['type']
        granularity = range_estimator_config[stats_name]['granularity']

        inplace_statistics = 'compute_statistic'
        if fn_type not in ['quantile', 'abs_quantile'] and not for_weights\
                and kwargs.get('inplace_statistics', False):
            kwargs['granularity'] = granularity
            kwargs['type'] = fn_type
            inplace_statistics = 'statistic_in_graph'

        fn = get_stats_function(WEIGHTS if for_weights else ACTIVATIONS, fn_type, granularity, inplace_statistics)
        ts_args = deepcopy(kwargs)
        stat_mod_name = get_stat_name_by_config(range_estimator_config, stats_name)
        if fn_type in ['quantile', 'abs_quantile']:
            q_value = range_estimator_config[stats_name]['outlier_prob']
            if not for_weights:
                ts_args['inplace_statistics'] = False
            if stats_name == 'max':
                q_value = 1 - q_value
            ts_args.update({'q': q_value})
        stats[stat_mod_name] = TensorStatistic(fn, **ts_args)
    return stats


def merge_nested_dicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_nested_dicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def select_evaluation_dataset(engine: Engine):
    if isinstance(engine, ACEngine):
        engine.set_dataset_tag(engine.evaluation_dataset_tag)


def select_optimization_dataset(engine: Engine):
    if isinstance(engine, ACEngine):
        engine.set_dataset_tag(engine.optimization_dataset_tag)


def reset_dataset_to_default(engine: Engine):
    if isinstance(engine, ACEngine):
        engine.set_dataset_tag(None)


def get_stat_name_by_config(config, stat_type):
    agg_type = config[stat_type]['type']
    name_list = [stat_type, agg_type, ]
    if agg_type in ['quantile', 'abs_quantile']:
        name_list.append(str(config[stat_type]['outlier_prob']))
    return '_'.join(name_list)


def get_input_shape_for_bias(activations_statistics, input_node_name):
    input_shape = mode(activations_statistics[input_node_name]['shape'])[0][0]
    if len(input_shape) > 1:
        input_shape[0] = 1
    return input_shape


def get_ignored_operations(model):
    operation = {"transformer": [{"type": "Add"}, {"type": "Power"},
                                 {"type": "Squeeze"}, {"type": "Multiply"},
                                 {"type": "Subtract"}, {"type": "ReduceMean"},
                                 {"type": "SquaredDifference"}, {"type": "MVN"}]}
    return operation[model]
