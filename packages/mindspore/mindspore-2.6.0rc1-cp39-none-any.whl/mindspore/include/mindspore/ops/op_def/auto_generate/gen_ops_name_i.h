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
#ifndef MINDSPORE_CORE_OP_NAME_I_H_
#define MINDSPORE_CORE_OP_NAME_I_H_

namespace mindspore::ops {
constexpr auto kNameIHFFT = "IHFFT";
constexpr auto kNameInplaceScatterSrc = "InplaceScatterSrc";
constexpr auto kNameInplaceAddsExt = "InplaceAddsExt";
constexpr auto kNameInplaceScatterAdd = "InplaceScatterAdd";
constexpr auto kNameInplaceDivMods = "InplaceDivMods";
constexpr auto kNameInplaceMaskedFillScalar = "InplaceMaskedFillScalar";
constexpr auto kNameInplaceLog = "InplaceLog";
constexpr auto kNameInnerNonZero = "InnerNonZero";
constexpr auto kNameIFFTShift = "IFFTShift";
constexpr auto kNameInplaceScatterValueReduce = "InplaceScatterValueReduce";
constexpr auto kNameIsNegInf = "IsNegInf";
constexpr auto kNameIsInf = "IsInf";
constexpr auto kNameInplaceFloorDivides = "InplaceFloorDivides";
constexpr auto kNameIDCTN = "IDCTN";
constexpr auto kNameIncreFlashAttention = "IncreFlashAttention";
constexpr auto kNameInplaceReLU = "InplaceReLU";
constexpr auto kNameIndexFillScalar = "IndexFillScalar";
constexpr auto kNameInnerCommAllReduce = "InnerCommAllReduce";
constexpr auto kNameIndexFillTensor = "IndexFillTensor";
constexpr auto kNameInplaceMaskedFillTensor = "InplaceMaskedFillTensor";
constexpr auto kNameInplaceGroupedMatmulAdd = "InplaceGroupedMatmulAdd";
constexpr auto kNameInplaceTanh = "InplaceTanh";
constexpr auto kNameInplaceStopGradient = "InplaceStopGradient";
constexpr auto kNameInplaceHardtanh = "InplaceHardtanh";
constexpr auto kNameIm2ColExt = "Im2ColExt";
constexpr auto kNameInplaceZero = "InplaceZero";
constexpr auto kNameInplaceRandom = "InplaceRandom";
constexpr auto kNameInplaceFillScalar = "InplaceFillScalar";
constexpr auto kNameInplaceMul = "InplaceMul";
constexpr auto kNameInplaceElu = "InplaceElu";
constexpr auto kNameInnerCommIsend = "InnerCommIsend";
constexpr auto kNameIDCT = "IDCT";
constexpr auto kNameInplaceAddmm = "InplaceAddmm";
constexpr auto kNameInnerCommReduceScatter = "InnerCommReduceScatter";
constexpr auto kNameInplaceUniform = "InplaceUniform";
constexpr auto kNameInplaceDivMod = "InplaceDivMod";
constexpr auto kNameIFFT2 = "IFFT2";
constexpr auto kNameInplaceFillTensor = "InplaceFillTensor";
constexpr auto kNameIdentity = "Identity";
constexpr auto kNameInnerIndex = "InnerIndex";
constexpr auto kNameInnerInplaceIndexPut = "InnerInplaceIndexPut";
constexpr auto kNameInplaceFloorDivide = "InplaceFloorDivide";
constexpr auto kNameIndex = "Index";
constexpr auto kNameIRFFT2 = "IRFFT2";
constexpr auto kNameInplaceIndexAddExt = "InplaceIndexAddExt";
constexpr auto kNameIRFFTDouble = "IRFFTDouble";
constexpr auto kNameInplaceScatterSrcReduce = "InplaceScatterSrcReduce";
constexpr auto kNameInplaceIndexPut = "InplaceIndexPut";
constexpr auto kNameIRFFTN = "IRFFTN";
constexpr auto kNameIFFTN = "IFFTN";
constexpr auto kNameInplaceFillDiagonal = "InplaceFillDiagonal";
constexpr auto kNameInplaceSubExt = "InplaceSubExt";
constexpr auto kNameIndexAddExt = "IndexAddExt";
constexpr auto kNameInplaceNormal = "InplaceNormal";
constexpr auto kNameInplaceSubScalar = "InplaceSubScalar";
constexpr auto kNameInnerCommAllGather = "InnerCommAllGather";
constexpr auto kNameInplaceCopy = "InplaceCopy";
constexpr auto kNameInplaceDivs = "InplaceDivs";
constexpr auto kNameIsClose = "IsClose";
constexpr auto kNameInplaceClampScalar = "InplaceClampScalar";
constexpr auto kNameInplaceMuls = "InplaceMuls";
constexpr auto kNameIHFFTN = "IHFFTN";
constexpr auto kNameInplaceAddExt = "InplaceAddExt";
constexpr auto kNameIRFFT = "IRFFT";
constexpr auto kNameInsertGemV2InBackward = "InsertGemV2InBackward";
constexpr auto kNameInplaceScatterValue = "InplaceScatterValue";
constexpr auto kNameIndexSelect = "IndexSelect";
constexpr auto kNameInplaceFloor = "InplaceFloor";
constexpr auto kNameInplacePut = "InplacePut";
constexpr auto kNameInplaceDiv = "InplaceDiv";
constexpr auto kNameInplaceThreshold = "InplaceThreshold";
constexpr auto kNameInplaceClampTensor = "InplaceClampTensor";
constexpr auto kNameIFFT = "IFFT";
constexpr auto kNameIsFinite = "IsFinite";
constexpr auto kNameInplaceErfinv = "InplaceErfinv";
constexpr auto kNameInnerCommAllToAllV = "InnerCommAllToAllV";
constexpr auto kNameIHFFT2 = "IHFFT2";
constexpr auto kNameInnerCommIrecv = "InnerCommIrecv";
constexpr auto kNameInplaceExp = "InplaceExp";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_I_H_
