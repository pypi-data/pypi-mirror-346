/**
 * Copyright 2023-2025 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef MINDSPORE_CORE_OP_NAME_M_H_
#define MINDSPORE_CORE_OP_NAME_M_H_

namespace mindspore::ops {
constexpr auto kNameMaxPoolGradWithMask = "MaxPoolGradWithMask";
constexpr auto kNameMaxPoolWithIndices = "MaxPoolWithIndices";
constexpr auto kNameMedianExt = "MedianExt";
constexpr auto kNameMatrixInverseExt = "MatrixInverseExt";
constexpr auto kNameMoeTokenUnpermute = "MoeTokenUnpermute";
constexpr auto kNameMSELossExt = "MSELossExt";
constexpr auto kNameMv = "Mv";
constexpr auto kNameMatMul = "MatMul";
constexpr auto kNameMinimumGrad = "MinimumGrad";
constexpr auto kNameMinimum = "Minimum";
constexpr auto kNameMinDim = "MinDim";
constexpr auto kNameMaximumGrad = "MaximumGrad";
constexpr auto kNameMedianDim = "MedianDim";
constexpr auto kNameMaximumGradGrad = "MaximumGradGrad";
constexpr auto kNameMultiScaleDeformableAttnGrad = "MultiScaleDeformableAttnGrad";
constexpr auto kNameMoeTokenUnpermuteGrad = "MoeTokenUnpermuteGrad";
constexpr auto kNameMSELossGradExt = "MSELossGradExt";
constexpr auto kNameMaskedSelect = "MaskedSelect";
constexpr auto kNameMin = "Min";
constexpr auto kNameMaxPoolGradWithIndices = "MaxPoolGradWithIndices";
constexpr auto kNameMaxDim = "MaxDim";
constexpr auto kNameMax = "Max";
constexpr auto kNameMaxUnpool2DExt = "MaxUnpool2DExt";
constexpr auto kNameMishGradExt = "MishGradExt";
constexpr auto kNameMaskedSelectGrad = "MaskedSelectGrad";
constexpr auto kNameMaxPoolWithMask = "MaxPoolWithMask";
constexpr auto kNameMishExt = "MishExt";
constexpr auto kNameMul = "Mul";
constexpr auto kNameMaskedFill = "MaskedFill";
constexpr auto kNameMoeTokenPermute = "MoeTokenPermute";
constexpr auto kNameMatMulExt = "MatMulExt";
constexpr auto kNameMaximum = "Maximum";
constexpr auto kNameMultiScaleDeformableAttn = "MultiScaleDeformableAttn";
constexpr auto kNameMatmulReduceScatter = "MatmulReduceScatter";
constexpr auto kNameMm = "Mm";
constexpr auto kNameMeanExt = "MeanExt";
constexpr auto kNameMuls = "Muls";
constexpr auto kNameMoeTokenPermuteGrad = "MoeTokenPermuteGrad";
constexpr auto kNameMatrixDeterminant = "MatrixDeterminant";
constexpr auto kNameMultinomialExt = "MultinomialExt";
constexpr auto kNameMeshgrid = "Meshgrid";
constexpr auto kNameMatrixExp = "MatrixExp";
constexpr auto kNameMatmulBiasSplitSiluOut2 = "MatmulBiasSplitSiluOut2";
constexpr auto kNameMatmulBiasSplitOut2 = "MatmulBiasSplitOut2";
constexpr auto kNameMatmulSplitOut3 = "MatmulSplitOut3";
constexpr auto kNameMoeComputeExpertTokens = "MoeComputeExpertTokens";
constexpr auto kNameMoeGatingTopKSoftmax = "MoeGatingTopKSoftmax";
constexpr auto kNameMoeInitRoutingV2 = "MoeInitRoutingV2";
constexpr auto kNameMatmulSplitOut2 = "MatmulSplitOut2";
constexpr auto kNameMatmulBiasSplitOut3 = "MatmulBiasSplitOut3";
constexpr auto kNameMoeInitRouting = "MoeInitRouting";
constexpr auto kNameMatmulSplitSiluOut2 = "MatmulSplitSiluOut2";
constexpr auto kNameMatmulAllReduceAddRmsNorm = "MatmulAllReduceAddRmsNorm";
constexpr auto kNameMoeFinalizeRouting = "MoeFinalizeRouting";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_M_H_
