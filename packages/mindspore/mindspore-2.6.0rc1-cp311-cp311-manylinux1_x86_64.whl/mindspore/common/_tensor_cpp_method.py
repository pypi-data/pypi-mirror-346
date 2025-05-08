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

tensor_cpp_methods = ['tan', 'put_', 'nansum', 'add_', '__iadd__', 'isinf', 'bitwise_or', '__or__', 'reshape', 'isneginf', 'floor', 'fill_', 'isclose', 'lerp', 'erfc', 'bitwise_not', 'argmin', 'gcd', 'gather', 'cumsum', 'mean', 'roll', 'dot', 'exp', 'prod', 'index_select', 'erf', 'sub_', '__isub__', 'cos', 'logical_and', '_to', 'select', 'asinh', 'arcsinh', 'histc', 'split', 'kthvalue', 'median', 'unique', 'sum', 'scatter', 'asin', 'arcsin', 'atan2', 'arctan2', 'where', 'sinc', 'triu', 'expand_as', 'masked_select', 'logaddexp2', 'mul_', '__imul__', 'all', 'min', 'addmm', 'bitwise_xor', '__xor__', 'tanh', 'reciprocal', 'pow', '__pow__', 'fill_diagonal_', 'xlogy', 'clamp', 'clip', 'outer', 'div_', '__itruediv__', 'mul', 'addmv', 'neg', 'negative', 'scatter_add', 'less', 'lt', 'bitwise_and', '__and__', 'logical_xor', 'div', 'divide', 'trunc', 'view_as', 'logaddexp', 'repeat', 'max', 'sub', '__sub__', 'abs', 'absolute', '__abs__', 't', 'flatten', 'atan', 'arctan', 'isfinite', 'mm', 'logsumexp', 'addcdiv', 'frac', 'tile', 'addbmm', 'subtract', 'narrow', 'log_', 'sin', 'masked_fill_', 'argsort', 'count_nonzero', 'fmod', 'acosh', 'arccosh', 'less_equal', 'le', 'any', 'log', 'round', 'atanh', 'arctanh', 'rsqrt', 'nan_to_num', 'not_equal', 'ne', 'floor_divide_', '__ifloordiv__', 'type_as', 'log10', 'hardshrink', 'eq', 'inverse', 'greater', 'gt', 'chunk', 'diag', 'sinh', 'square', 'sqrt', 'acos', 'arccos', 'take', 'logical_not', 'allclose', 'index_add', 'tril', 'logical_or', 'masked_fill', 'remainder', 'log2', 'baddbmm', 'cosh', 'matmul', 'var', 'copy_', 'exp_', 'floor_divide', 'scatter_', 'add', '__add__', 'true_divide', 'expm1', 'unbind', 'minimum', 'repeat_interleave', 'ceil', 'argmax', 'log1p', 'new_zeros', 'topk', 'sigmoid', 'bincount', 'greater_equal', 'ge', 'transpose', 'clone', 'maximum', 'std', 'sort', 'unsqueeze', 'new_ones']
