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
constexpr auto kNameDropoutExt = "DropoutExt";
constexpr auto kNameDCT = "DCT";
constexpr auto kNameDistCommIsend = "DistCommIsend";
constexpr auto kNameDistCommScatter = "DistCommScatter";
constexpr auto kNameDivMod = "DivMod";
constexpr auto kNameDiag = "Diag";
constexpr auto kNameDense = "Dense";
constexpr auto kNameDiagonal = "Diagonal";
constexpr auto kNameDistCommAllGather = "DistCommAllGather";
constexpr auto kNameDistCommReduceScatterTensor = "DistCommReduceScatterTensor";
constexpr auto kNameDistCommBatchIsendIrecv = "DistCommBatchIsendIrecv";
constexpr auto kNameDistCommReduceScatter = "DistCommReduceScatter";
constexpr auto kNameDivs = "Divs";
constexpr auto kNameDiagExt = "DiagExt";
constexpr auto kNameDistCommAllToAllV = "DistCommAllToAllV";
constexpr auto kNameDivMods = "DivMods";
constexpr auto kNameDCTN = "DCTN";
constexpr auto kNameDistCommReduce = "DistCommReduce";
constexpr auto kNameDistCommScatterTensor = "DistCommScatterTensor";
constexpr auto kNameDistCommAllToAllVSingle = "DistCommAllToAllVSingle";
constexpr auto kNameDot = "Dot";
constexpr auto kNameDropoutDoMaskExt = "DropoutDoMaskExt";
constexpr auto kNameDistCommBroadcast = "DistCommBroadcast";
constexpr auto kNameDropout = "Dropout";
constexpr auto kNameDistCommBarrier = "DistCommBarrier";
constexpr auto kNameDiv = "Div";
constexpr auto kNameDistCommIrecv = "DistCommIrecv";
constexpr auto kNameDecoderKVCache = "DecoderKVCache";
constexpr auto kNameDistCommGatherIntoTensor = "DistCommGatherIntoTensor";
constexpr auto kNameDropoutGradExt = "DropoutGradExt";
constexpr auto kNameDistCommAllReduce = "DistCommAllReduce";
constexpr auto kNameDistCommAllGatherIntoTensor = "DistCommAllGatherIntoTensor";
constexpr auto kNameDropoutGenMaskExt = "DropoutGenMaskExt";
constexpr auto kNameDistCommGather = "DistCommGather";
constexpr auto kNameDynamicQuantExt = "DynamicQuantExt";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_D_H_
