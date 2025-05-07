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

tensor_cpp_methods = ['exp_', 'expand_as', 'baddbmm', 'unique', 'mean', 'minimum', 'xlogy', 'div', 'divide', 'view_as', 'scatter_', 'atan', 'arctan', 'rsqrt', 'neg', 'negative', 'fill_', 'tile', 'asinh', 'arcsinh', 't', 'sinh', 'masked_fill_', 'prod', 'narrow', 'repeat_interleave', 'kthvalue', 'allclose', 'isneginf', 'min', 'nan_to_num', 'logaddexp2', 'tan', 'select', 'ceil', 'diag', 'clamp', 'clip', 'sinc', 'logical_and', 'put_', 'erf', 'add', '__add__', 'all', 'floor', 'log_', 'acos', 'arccos', 'div_', '__itruediv__', 'mm', 'logical_not', 'exp', 'maximum', 'clone', 'expm1', 'copy_', 'sigmoid', 'floor_divide_', '__ifloordiv__', 'split', 'subtract', 'argmin', 'erfc', 'reshape', 'type_as', 'pow', '__pow__', 'atan2', 'arctan2', 'cosh', 'new_ones', 'any', 'log', 'greater', 'gt', 'mul', 'lerp', 'repeat', 'where', 'index_select', 'median', 'flatten', 'std', 'dot', 'sum', 'sub', '__sub__', 'acosh', 'arccosh', 'isclose', 'new_zeros', 'bitwise_not', 'max', 'triu', 'add_', '__iadd__', 'abs', 'absolute', '__abs__', 'trunc', 'take', 'round', 'scatter_add', 'hardshrink', 'count_nonzero', 'tril', 'floor_divide', 'logsumexp', 'argmax', 'log1p', 'sort', 'fmod', 'addbmm', 'histc', 'cumsum', 'asin', 'arcsin', 'scatter', 'remainder', 'unsqueeze', 'reciprocal', 'not_equal', 'ne', 'unbind', 'frac', 'masked_select', 'square', 'log10', 'addmm', 'masked_fill', 'less', 'lt', 'matmul', 'chunk', 'inverse', 'logical_or', 'isfinite', 'bitwise_or', '__or__', 'bitwise_and', '__and__', '_to', 'transpose', 'less_equal', 'le', 'addcdiv', 'index_add', 'log2', 'fill_diagonal_', 'logaddexp', 'isinf', 'topk', 'tanh', 'gather', 'addmv', 'mul_', '__imul__', 'atanh', 'arctanh', 'eq', 'bincount', 'sqrt', 'bitwise_xor', '__xor__', 'argsort', 'roll', 'outer', 'cos', 'greater_equal', 'ge', 'true_divide', 'nansum', 'gcd', 'logical_xor', 'var', 'sub_', '__isub__', 'sin']
