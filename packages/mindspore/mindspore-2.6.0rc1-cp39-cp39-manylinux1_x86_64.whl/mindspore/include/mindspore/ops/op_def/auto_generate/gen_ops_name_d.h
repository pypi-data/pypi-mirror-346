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
#ifndef MINDSPORE_CORE_OP_NAME_D_H_
#define MINDSPORE_CORE_OP_NAME_D_H_

namespace mindspore::ops {
constexpr auto kNameDivMod = "DivMod";
constexpr auto kNameDense = "Dense";
constexpr auto kNameDropoutGenMaskExt = "DropoutGenMaskExt";
constexpr auto kNameDropoutDoMaskExt = "DropoutDoMaskExt";
constexpr auto kNameDistCommAllGather = "DistCommAllGather";
constexpr auto kNameDistCommReduceScatter = "DistCommReduceScatter";
constexpr auto kNameDistCommReduce = "DistCommReduce";
constexpr auto kNameDistCommGatherIntoTensor = "DistCommGatherIntoTensor";
constexpr auto kNameDistCommAllReduce = "DistCommAllReduce";
constexpr auto kNameDiag = "Diag";
constexpr auto kNameDistCommIrecv = "DistCommIrecv";
constexpr auto kNameDCTN = "DCTN";
constexpr auto kNameDistCommIsend = "DistCommIsend";
constexpr auto kNameDivMods = "DivMods";
constexpr auto kNameDistCommBatchIsendIrecv = "DistCommBatchIsendIrecv";
constexpr auto kNameDistCommBroadcast = "DistCommBroadcast";
constexpr auto kNameDistCommBarrier = "DistCommBarrier";
constexpr auto kNameDivs = "Divs";
constexpr auto kNameDiv = "Div";
constexpr auto kNameDistCommScatter = "DistCommScatter";
constexpr auto kNameDot = "Dot";
constexpr auto kNameDistCommReduceScatterTensor = "DistCommReduceScatterTensor";
constexpr auto kNameDiagonal = "Diagonal";
constexpr auto kNameDistCommAllToAllV = "DistCommAllToAllV";
constexpr auto kNameDCT = "DCT";
constexpr auto kNameDistCommAllToAllVSingle = "DistCommAllToAllVSingle";
constexpr auto kNameDecoderKVCache = "DecoderKVCache";
constexpr auto kNameDropout = "Dropout";
constexpr auto kNameDropoutGradExt = "DropoutGradExt";
constexpr auto kNameDistCommScatterTensor = "DistCommScatterTensor";
constexpr auto kNameDropoutExt = "DropoutExt";
constexpr auto kNameDistCommGather = "DistCommGather";
constexpr auto kNameDiagExt = "DiagExt";
constexpr auto kNameDistCommAllGatherIntoTensor = "DistCommAllGatherIntoTensor";
constexpr auto kNameDynamicQuantExt = "DynamicQuantExt";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_D_H_
