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

tensor_cpp_methods = ['tanh', 'prod', 't', 'all', 'mean', 'isinf', 'put_', 'tile', 'add', '__add__', 'sigmoid', 'lerp', 'argmax', 'floor_divide', 'index_select', 'log2', 'bitwise_xor', '__xor__', 'take', 'sub_', '__isub__', 'trunc', 'logical_or', '_to', 'kthvalue', 'less_equal', 'le', 'dot', 'inverse', 'unique', 'mm', 'new_ones', 'reciprocal', 'roll', 'log_', 'repeat', 'acos', 'arccos', 'sqrt', 'split', 'narrow', 'remainder', 'expand_as', 'greater', 'gt', 'baddbmm', 'log', 'isfinite', 'minimum', 'sinc', 'logaddexp2', 'addmv', 'true_divide', 'div_', '__itruediv__', 'new_zeros', 'nansum', 'acosh', 'arccosh', 'add_', '__iadd__', 'floor_divide_', '__ifloordiv__', 'select', 'unbind', 'isneginf', 'abs', 'absolute', '__abs__', 'asinh', 'arcsinh', 'any', 'nan_to_num', 'hardshrink', 'logical_xor', 'clone', 'frac', 'rsqrt', 'flatten', 'bitwise_not', 'log10', 'median', 'fill_', 'topk', 'type_as', 'logaddexp', 'bitwise_and', '__and__', 'pow', '__pow__', 'clamp', 'clip', 'exp_', 'sinh', 'masked_fill', 'transpose', 'count_nonzero', 'addbmm', 'round', 'gcd', 'logical_not', 'diag', 'addcdiv', 'chunk', 'scatter_add', 'xlogy', 'argmin', 'repeat_interleave', 'div', 'divide', 'atan2', 'arctan2', 'fill_diagonal_', 'allclose', 'exp', 'log1p', 'logical_and', 'sum', 'erfc', 'fmod', 'tan', 'scatter_', 'cosh', 'mul', 'expm1', 'triu', 'index_add', 'matmul', 'floor', 'tril', 'square', 'masked_select', 'isclose', 'atan', 'arctan', 'less', 'lt', 'bitwise_or', '__or__', 'sort', 'subtract', 'max', 'reshape', 'outer', 'eq', 'not_equal', 'ne', 'asin', 'arcsin', 'masked_fill_', 'neg', 'negative', 'scatter', 'bincount', 'atanh', 'arctanh', 'histc', 'erf', 'unsqueeze', 'var', 'addmm', 'view_as', 'cumsum', 'sin', 'copy_', 'min', 'ceil', 'argsort', 'greater_equal', 'ge', 'gather', 'mul_', '__imul__', 'sub', '__sub__', 'logsumexp', 'maximum', 'std', 'where', 'cos']
