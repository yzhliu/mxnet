# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import print_function
import mxnet as mx
import mxnet.ndarray as nd
import numpy as np
from PIL import Image
from mxnet import gluon
from mxnet.gluon.data.vision import transforms
from mxnet.test_utils import assert_almost_equal
from mxnet.test_utils import almost_equal

def test_to_tensor():
    data_in = np.random.uniform(0, 255, (300, 300, 3)).astype(dtype=np.uint8)
    out_nd = transforms.ToTensor()(nd.array(data_in, dtype='uint8'))
    assert_almost_equal(out_nd.asnumpy(), np.transpose(
        data_in.astype(dtype=np.float32) / 255.0, (2, 0, 1)))

def test_normalize():
    data_in = np.random.uniform(0, 255, (300, 300, 3)).astype(dtype=np.uint8)
    data_in = transforms.ToTensor()(nd.array(data_in, dtype='uint8'))
    out_nd = transforms.Normalize(mean=(0, 1, 2), std=(3, 2, 1))(data_in)
    data_expected = data_in.asnumpy()
    data_expected[:][:][0] = data_expected[:][:][0] / 3.0
    data_expected[:][:][1] = (data_expected[:][:][1] - 1.0) / 2.0
    data_expected[:][:][2] = data_expected[:][:][2] - 2.0
    assert_almost_equal(data_expected, out_nd.asnumpy())

def run_random(func, func_expect, data_in, n=100, ratio_same=0.5, ratio_delta=0.1):
    num_same = 0
    for i in range(n):
        data_trans = func(nd.array(data_in, dtype='uint8')).asnumpy()
        if almost_equal(data_trans, data_in):
            num_same += 1
        else:
            assert_almost_equal(func_expect(data_in), data_trans)
    ratio = num_same * 1.0 / n
    assert ratio >= ratio_same - ratio_delta and ratio <= ratio_same + ratio_delta

def test_random_horizontal_flip():
    f = transforms.RandomHorizontalFlip()
    def f_expect(img):
        pil_img = Image.fromarray(img).transpose(Image.FLIP_LEFT_RIGHT)
        return np.array(pil_img)
    run_random(transforms.RandomHorizontalFlip(),
        f_expect,
        np.random.uniform(0, 255, (300, 300, 3)).astype(dtype=np.uint8))

def test_random_vertical_flip():
    def f_expect(img):
        pil_img = Image.fromarray(img).transpose(Image.FLIP_TOP_BOTTOM)
        return np.array(pil_img)
    run_random(transforms.RandomVerticalFlip(),
        f_expect,
        np.random.uniform(0, 255, (300, 300, 3)).astype(dtype=np.uint8))

if __name__ == '__main__':
    import nose
    nose.runmodule()
