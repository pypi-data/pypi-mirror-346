# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Add tensor cpp methods for stub tensor"""

tensor_cpp_methods = ['tan', 'nansum', 'scatter_add', 'flatten', 'baddbmm', 'tile', 'greater_equal', 'ge', 'floor_divide', 'transpose', 'var', 'rsqrt', 'mul', 'prod', 'argmin', 'eq', 'narrow', 'select', 'count_nonzero', 'argsort', 'allclose', 'scatter_', 'bitwise_not', 'greater', 'gt', 'diag', 'log_', 'exp', 'split', 'index_add', 'sqrt', 'div_', '__itruediv__', 'atan', 'arctan', 'add_', '__iadd__', 'triu', 'view_as', 'new_zeros', 'sub_', '__isub__', 'copy_', 'repeat_interleave', 'addbmm', 'maximum', 'pow', '__pow__', 'isclose', 'ceil', 'trunc', 'bitwise_xor', '__xor__', 'min', 'fill_diagonal_', 'bitwise_or', '__or__', 'where', 'tanh', 'all', 'lerp', 'scatter', 'index_select', 'remainder', 'xlogy', 'expm1', 'take', 'cos', 'unbind', 'sort', 'atan2', 'arctan2', 'topk', 'hardshrink', 'addmm', 'logsumexp', 'masked_fill_', 'subtract', 'sin', 'repeat', 'sigmoid', 'sinh', 'minimum', 'logical_and', 'square', 't', 'tril', 'log', 'new_ones', 'asinh', 'arcsinh', 'type_as', 'histc', 'gather', 'logaddexp', 'bincount', 'sum', 'clone', 'less_equal', 'le', 'mean', 'erf', 'inverse', 'log2', 'kthvalue', 'less', 'lt', 'not_equal', 'ne', 'matmul', 'round', 'logical_not', '_to', 'argmax', 'logical_xor', 'masked_fill', 'log1p', 'asin', 'arcsin', 'put_', 'gcd', 'unsqueeze', 'add', '__add__', 'cosh', 'addmv', 'fmod', 'mul_', '__imul__', 'cumsum', 'isneginf', 'isfinite', 'expand_as', 'chunk', 'log10', 'unique', 'div', 'divide', 'outer', 'erfc', 'neg', 'negative', 'logical_or', 'clamp', 'clip', 'reshape', 'sub', '__sub__', 'nan_to_num', 'any', 'fill_', 'floor_divide_', '__ifloordiv__', 'acos', 'arccos', 'logaddexp2', 'bitwise_and', '__and__', 'acosh', 'arccosh', 'sinc', 'exp_', 'dot', 'reciprocal', 'atanh', 'arctanh', 'mm', 'roll', 'std', 'addcdiv', 'isinf', 'masked_select', 'max', 'true_divide', 'abs', 'absolute', '__abs__', 'median', 'floor', 'frac']
