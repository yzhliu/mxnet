/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/*!
 * Copyright (c) 2017 by Contributors
 * \file random_generator.h
 * \brief Native random number generator.
 */
#ifndef MXNET_COMMON_RANDOM_GENERATOR_H_
#define MXNET_COMMON_RANDOM_GENERATOR_H_

#include <mxnet/base.h>
#include <random>

#if MXNET_USE_CUDA
#include <curand_kernel.h>
#endif  // MXNET_USE_CUDA

using namespace mshadow;

namespace mxnet {
namespace common {
namespace random {

// Elementary random number generation for int/uniform/gaussian in CPU and GPU.
// Will use float data type whenever instantiated for half_t or any other non
// standard real type.
template<typename Device, typename DType MSHADOW_DEFAULT_DTYPE>
class RandGenerator;

template<typename Device, typename DType MSHADOW_DEFAULT_DTYPE>
class RandGeneratorGlobal;

template<typename xpu, typename DType MSHADOW_DEFAULT_DTYPE>
void RandGeneratorSeed(Stream<xpu> *, RandGenerator<xpu, DType> *, uint32_t seed);

template<typename xpu, typename DType MSHADOW_DEFAULT_DTYPE>
RandGenerator<xpu, DType> *NewRandGenerator();

template<typename xpu, typename DType MSHADOW_DEFAULT_DTYPE>
void DeleteRandGenerator(RandGenerator<xpu, DType> *);

template<typename DType>
class RandGenerator<cpu, DType> {
public:
  typedef typename std::conditional<std::is_floating_point<DType>::value,
                                    DType, float>::type FType;

  explicit RandGenerator() {}

  MSHADOW_XINLINE void Seed(uint32_t seed, uint32_t idx) { engine.seed(seed); }

  MSHADOW_XINLINE int rand() { return engine(); }

  MSHADOW_XINLINE FType uniform() { return uniformNum(engine); }

  MSHADOW_XINLINE FType normal() { return normalNum(engine); }

private:
  std::mt19937 engine;
  std::uniform_real_distribution<FType> uniformNum;
  std::normal_distribution<FType> normalNum;
};

#if MXNET_USE_CUDA
// at least how many random numbers should be generated by one GPU thread.
const int kGPUMinRndNumberPerThread = 64;
// store how many global random states.
const int kGPURndStateNum = 32768;

#endif  // MXNET_USE_CUDA

}  // nanespace random
}  // namespace common
}  // namespace mxnet
#endif  // MXNET_COMMON_RANDOM_GENERATOR_H_
