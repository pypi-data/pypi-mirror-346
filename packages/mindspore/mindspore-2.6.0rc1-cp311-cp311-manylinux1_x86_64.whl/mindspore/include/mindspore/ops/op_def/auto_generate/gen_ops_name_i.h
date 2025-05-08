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
constexpr auto kNameInsertGemV2InBackward = "InsertGemV2InBackward";
constexpr auto kNameInnerCommReduceScatter = "InnerCommReduceScatter";
constexpr auto kNameIDCT = "IDCT";
constexpr auto kNameIFFT2 = "IFFT2";
constexpr auto kNameInplaceAddsExt = "InplaceAddsExt";
constexpr auto kNameIFFTShift = "IFFTShift";
constexpr auto kNameInplaceZero = "InplaceZero";
constexpr auto kNameInplaceScatterValue = "InplaceScatterValue";
constexpr auto kNameIndexAddExt = "IndexAddExt";
constexpr auto kNameInplaceElu = "InplaceElu";
constexpr auto kNameIsNegInf = "IsNegInf";
constexpr auto kNameInplaceErfinv = "InplaceErfinv";
constexpr auto kNameIFFTN = "IFFTN";
constexpr auto kNameInplaceHardtanh = "InplaceHardtanh";
constexpr auto kNameInplaceFloor = "InplaceFloor";
constexpr auto kNameIFFT = "IFFT";
constexpr auto kNameInplaceAddmm = "InplaceAddmm";
constexpr auto kNameInplaceIndexAddExt = "InplaceIndexAddExt";
constexpr auto kNameIsInf = "IsInf";
constexpr auto kNameInplaceExp = "InplaceExp";
constexpr auto kNameInplaceUniform = "InplaceUniform";
constexpr auto kNameInplacePut = "InplacePut";
constexpr auto kNameInplaceClampTensor = "InplaceClampTensor";
constexpr auto kNameInplaceMaskedFillTensor = "InplaceMaskedFillTensor";
constexpr auto kNameInplaceSubScalar = "InplaceSubScalar";
constexpr auto kNameInplaceFloorDivides = "InplaceFloorDivides";
constexpr auto kNameInnerCommAllToAllV = "InnerCommAllToAllV";
constexpr auto kNameInnerIndex = "InnerIndex";
constexpr auto kNameInplaceFloorDivide = "InplaceFloorDivide";
constexpr auto kNameInplaceGroupedMatmulAdd = "InplaceGroupedMatmulAdd";
constexpr auto kNameIm2ColExt = "Im2ColExt";
constexpr auto kNameIRFFT2 = "IRFFT2";
constexpr auto kNameIDCTN = "IDCTN";
constexpr auto kNameIHFFT2 = "IHFFT2";
constexpr auto kNameIsFinite = "IsFinite";
constexpr auto kNameInplaceThreshold = "InplaceThreshold";
constexpr auto kNameInnerCommAllReduce = "InnerCommAllReduce";
constexpr auto kNameInplaceFillDiagonal = "InplaceFillDiagonal";
constexpr auto kNameInplaceMaskedFillScalar = "InplaceMaskedFillScalar";
constexpr auto kNameInnerCommIsend = "InnerCommIsend";
constexpr auto kNameInplaceIndexPut = "InplaceIndexPut";
constexpr auto kNameInplaceFillTensor = "InplaceFillTensor";
constexpr auto kNameInnerInplaceIndexPut = "InnerInplaceIndexPut";
constexpr auto kNameIncreFlashAttention = "IncreFlashAttention";
constexpr auto kNameIRFFTDouble = "IRFFTDouble";
constexpr auto kNameInplaceMul = "InplaceMul";
constexpr auto kNameInnerCommIrecv = "InnerCommIrecv";
constexpr auto kNameInplaceDivs = "InplaceDivs";
constexpr auto kNameInplaceScatterValueReduce = "InplaceScatterValueReduce";
constexpr auto kNameInplaceScatterSrc = "InplaceScatterSrc";
constexpr auto kNameInplaceDivMod = "InplaceDivMod";
constexpr auto kNameIndexFillTensor = "IndexFillTensor";
constexpr auto kNameInplaceClampScalar = "InplaceClampScalar";
constexpr auto kNameIndexFillScalar = "IndexFillScalar";
constexpr auto kNameInplaceCopy = "InplaceCopy";
constexpr auto kNameIndex = "Index";
constexpr auto kNameInplaceFillScalar = "InplaceFillScalar";
constexpr auto kNameInplaceSubExt = "InplaceSubExt";
constexpr auto kNameInplaceLog = "InplaceLog";
constexpr auto kNameIHFFTN = "IHFFTN";
constexpr auto kNameIsClose = "IsClose";
constexpr auto kNameInplaceDivMods = "InplaceDivMods";
constexpr auto kNameIRFFTN = "IRFFTN";
constexpr auto kNameInplaceScatterSrcReduce = "InplaceScatterSrcReduce";
constexpr auto kNameInplaceTanh = "InplaceTanh";
constexpr auto kNameIndexSelect = "IndexSelect";
constexpr auto kNameInplaceScatterAdd = "InplaceScatterAdd";
constexpr auto kNameInplaceDiv = "InplaceDiv";
constexpr auto kNameIRFFT = "IRFFT";
constexpr auto kNameInnerCommAllGather = "InnerCommAllGather";
constexpr auto kNameInplaceReLU = "InplaceReLU";
constexpr auto kNameIHFFT = "IHFFT";
constexpr auto kNameInnerNonZero = "InnerNonZero";
constexpr auto kNameIdentity = "Identity";
constexpr auto kNameInplaceRandom = "InplaceRandom";
constexpr auto kNameInplaceStopGradient = "InplaceStopGradient";
constexpr auto kNameInplaceAddExt = "InplaceAddExt";
constexpr auto kNameInplaceNormal = "InplaceNormal";
constexpr auto kNameInplaceMuls = "InplaceMuls";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_I_H_
