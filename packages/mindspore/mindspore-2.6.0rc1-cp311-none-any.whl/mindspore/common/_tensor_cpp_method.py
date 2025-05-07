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

tensor_cpp_methods = ['baddbmm', 'unique', 'acosh', 'arccosh', 'fill_diagonal_', 'type_as', 'flatten', 'less_equal', 'le', 'logical_or', 'atanh', 'arctanh', 'not_equal', 'ne', 'logsumexp', 'frac', 'log_', 'floor_divide', 'argmin', 'ceil', 'remainder', 'take', 'gather', 'pow', '__pow__', 'kthvalue', 'expm1', 'fmod', 'transpose', 'eq', 'minimum', 'atan2', 'arctan2', 'addmm', 'addcdiv', 'add_', '__iadd__', 'clone', 'exp_', 'any', 'outer', 'div_', '__itruediv__', 'neg', 'negative', 'exp', 'logical_xor', 'log', 'argmax', 'tile', 'asin', 'arcsin', 'allclose', 'logical_and', 'bitwise_xor', '__xor__', 'bitwise_or', '__or__', 'reciprocal', 'less', 'lt', 'atan', 'arctan', 'mul_', '__imul__', 'xlogy', 'gcd', 'subtract', 'scatter', 'repeat', 'cumsum', 'hardshrink', 'rsqrt', 'topk', 'reshape', 'isinf', 'scatter_', 'erf', 'sum', 'trunc', 'nan_to_num', 'bitwise_and', '__and__', 'bincount', 'log10', 'asinh', 'arcsinh', 'matmul', 'div', 'divide', 'min', 'floor_divide_', '__ifloordiv__', 'index_add', 'put_', 'isneginf', 'isfinite', 'floor', 'add', '__add__', 'lerp', 'masked_fill', 'inverse', 'new_zeros', 'new_ones', 'addbmm', 'square', 'std', 'cosh', 'erfc', 'nansum', 'split', 'scatter_add', 'mul', 'sub', '__sub__', 'cos', 'copy_', 'median', 'maximum', 'sqrt', 'masked_select', 'unsqueeze', 'triu', 'sort', 'var', 'clamp', 'clip', 'logaddexp2', 'isclose', 'mm', 'view_as', 'sigmoid', 'narrow', 'sinh', 'log1p', 'sub_', '__isub__', 'true_divide', 'fill_', 'greater', 'gt', 'prod', 'chunk', 'index_select', 'round', 'addmv', 'acos', 'arccos', 'bitwise_not', 'unbind', 'expand_as', 'tanh', 'roll', 'sin', 'greater_equal', 'ge', 'count_nonzero', 'sinc', 'argsort', 'max', 'where', 'tan', 'logaddexp', 't', 'log2', 'all', 'mean', 'logical_not', 'select', 'masked_fill_', 'diag', 'repeat_interleave', 'abs', 'absolute', '__abs__', 'histc', 'dot', '_to', 'tril']
