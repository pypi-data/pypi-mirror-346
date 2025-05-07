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
constexpr auto kNameIRFFT2 = "IRFFT2";
constexpr auto kNameInplacePut = "InplacePut";
constexpr auto kNameInplaceScatterValue = "InplaceScatterValue";
constexpr auto kNameIsNegInf = "IsNegInf";
constexpr auto kNameInplaceClampTensor = "InplaceClampTensor";
constexpr auto kNameInplaceZero = "InplaceZero";
constexpr auto kNameInplaceFloor = "InplaceFloor";
constexpr auto kNameIFFT = "IFFT";
constexpr auto kNameInplaceHardtanh = "InplaceHardtanh";
constexpr auto kNameInplaceAddExt = "InplaceAddExt";
constexpr auto kNameIRFFTDouble = "IRFFTDouble";
constexpr auto kNameInplaceScatterSrcReduce = "InplaceScatterSrcReduce";
constexpr auto kNameInplaceAddmm = "InplaceAddmm";
constexpr auto kNameInnerCommIsend = "InnerCommIsend";
constexpr auto kNameInplaceCopy = "InplaceCopy";
constexpr auto kNameIFFTShift = "IFFTShift";
constexpr auto kNameInplaceFloorDivide = "InplaceFloorDivide";
constexpr auto kNameInnerCommAllToAllV = "InnerCommAllToAllV";
constexpr auto kNameIHFFT2 = "IHFFT2";
constexpr auto kNameIRFFTN = "IRFFTN";
constexpr auto kNameInplaceGroupedMatmulAdd = "InplaceGroupedMatmulAdd";
constexpr auto kNameInplaceExp = "InplaceExp";
constexpr auto kNameIDCTN = "IDCTN";
constexpr auto kNameInplaceScatterValueReduce = "InplaceScatterValueReduce";
constexpr auto kNameInplaceTanh = "InplaceTanh";
constexpr auto kNameInplaceStopGradient = "InplaceStopGradient";
constexpr auto kNameIHFFT = "IHFFT";
constexpr auto kNameInplaceMaskedFillTensor = "InplaceMaskedFillTensor";
constexpr auto kNameIsClose = "IsClose";
constexpr auto kNameInplaceFillScalar = "InplaceFillScalar";
constexpr auto kNameInplaceDivMod = "InplaceDivMod";
constexpr auto kNameInplaceIndexPut = "InplaceIndexPut";
constexpr auto kNameInplaceMuls = "InplaceMuls";
constexpr auto kNameInnerInplaceIndexPut = "InnerInplaceIndexPut";
constexpr auto kNameInplaceScatterAdd = "InplaceScatterAdd";
constexpr auto kNameInplaceUniform = "InplaceUniform";
constexpr auto kNameInnerCommReduceScatter = "InnerCommReduceScatter";
constexpr auto kNameIdentity = "Identity";
constexpr auto kNameInplaceSubExt = "InplaceSubExt";
constexpr auto kNameInplaceScatterSrc = "InplaceScatterSrc";
constexpr auto kNameInplaceDivs = "InplaceDivs";
constexpr auto kNameInplaceNormal = "InplaceNormal";
constexpr auto kNameInplaceElu = "InplaceElu";
constexpr auto kNameInnerCommAllReduce = "InnerCommAllReduce";
constexpr auto kNameIFFT2 = "IFFT2";
constexpr auto kNameInplaceLog = "InplaceLog";
constexpr auto kNameInplaceFloorDivides = "InplaceFloorDivides";
constexpr auto kNameInplaceFillDiagonal = "InplaceFillDiagonal";
constexpr auto kNameIRFFT = "IRFFT";
constexpr auto kNameInplaceIndexAddExt = "InplaceIndexAddExt";
constexpr auto kNameInplaceFillTensor = "InplaceFillTensor";
constexpr auto kNameIndex = "Index";
constexpr auto kNameIncreFlashAttention = "IncreFlashAttention";
constexpr auto kNameInplaceAddsExt = "InplaceAddsExt";
constexpr auto kNameInplaceClampScalar = "InplaceClampScalar";
constexpr auto kNameInplaceErfinv = "InplaceErfinv";
constexpr auto kNameInnerIndex = "InnerIndex";
constexpr auto kNameIndexSelect = "IndexSelect";
constexpr auto kNameIndexAddExt = "IndexAddExt";
constexpr auto kNameIsInf = "IsInf";
constexpr auto kNameInnerNonZero = "InnerNonZero";
constexpr auto kNameIDCT = "IDCT";
constexpr auto kNameInplaceMaskedFillScalar = "InplaceMaskedFillScalar";
constexpr auto kNameInnerCommAllGather = "InnerCommAllGather";
constexpr auto kNameInsertGemV2InBackward = "InsertGemV2InBackward";
constexpr auto kNameIsFinite = "IsFinite";
constexpr auto kNameInplaceMul = "InplaceMul";
constexpr auto kNameInplaceReLU = "InplaceReLU";
constexpr auto kNameInplaceDiv = "InplaceDiv";
constexpr auto kNameIHFFTN = "IHFFTN";
constexpr auto kNameIndexFillScalar = "IndexFillScalar";
constexpr auto kNameInplaceRandom = "InplaceRandom";
constexpr auto kNameIFFTN = "IFFTN";
constexpr auto kNameInplaceThreshold = "InplaceThreshold";
constexpr auto kNameIndexFillTensor = "IndexFillTensor";
constexpr auto kNameIm2ColExt = "Im2ColExt";
constexpr auto kNameInnerCommIrecv = "InnerCommIrecv";
constexpr auto kNameInplaceSubScalar = "InplaceSubScalar";
constexpr auto kNameInplaceDivMods = "InplaceDivMods";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_I_H_
