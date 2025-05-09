import paddle

"""
   isort:skip_file
"""


class MyNet(paddle.nn.Layer):
    test = "str"

    def __init__(self):
        self._fc1 = paddle.nn.Linear(in_features=10, out_features=10)
        self._fc2 = paddle.nn.Linear(in_features=10, out_features=10)
        self._fc3 = paddle.nn.Linear(in_features=10, out_features=10)

    @paddle.no_grad()
    def forward(self, x):
        x = self._fc1(x)
        x = self._fc2(x)
        x = self._fc3(x)
        y = paddle.add(x=x, y=paddle.to_tensor(x))
        return paddle.nn.functional.relu(x=y)


class MyNet1(paddle.nn.Layer):
    def forward(self, x):
        x = paddle.rand(shape=[10, 10])
        return paddle.transpose(x=x, perm=dim2perm(x.ndim, 1, 0))


class MyNet2(paddle.nn.Layer):
    pass


@paddle.no_grad()
def func1(x):
    return paddle.abs(x=x)


def func2(x) -> paddle.Tensor:
    return paddle.abs(x=x)


def func3(x: paddle.Tensor) -> paddle.Tensor:
    def func5(x):
        return paddle.transpose(x=x, perm=dim2perm(x.ndim, 1, 0))

    return paddle.abs(x=x)


if x > 1:
    y = x.transpose(perm=dim2perm(x.ndim, 0, 1))
else:
    z = x.transpose(perm=dim2perm(x.ndim, 0, 1))


def func4(x: paddle.Tensor = None) -> paddle.Tensor:
    if isinstance(x, paddle.Tensor):
        out_0 = paddle.rand(shape=[1, 2])
        out_0.stop_gradient = not True
        out_1 = paddle.rand(shape=[1, 2])
        out_1.stop_gradient = not True
        paddle.add(x=out_0, y=paddle.to_tensor(out_1))
        return paddle.transpose(x=x, perm=dim2perm(x.ndim, 1, 0))


linear = MyNet()
x = paddle.rand(shape=[10, 10])
y = paddle.transpose(x=x, perm=dim2perm(x.ndim, 1, 0))
y = x.transpose(perm=dim2perm(x.ndim, 1, 0))
y_shape = tuple(x.transpose(perm=dim2perm(x.ndim, 1, 0)).shape)
z = linear(y)
out = paddle.rand(shape=[1, 2, 3], dtype="float32")
out_2 = paddle.rand(shape=[1, 2, 3], dtype="float32")
out_2.stop_gradient = not True
out_2
paddle.assign(paddle.abs(x=x), output=y)
return paddle.assign(paddle.abs(x=x), output=y)
z = paddle.assign(paddle.abs(x=x), output=y)
paddle.reshape(x=paddle.add(x=paddle.abs(x=x), y=paddle.to_tensor(y)), shape=[3])
paddle.reshape(x=paddle.add(x=x.abs(), y=paddle.to_tensor(y)), shape=[3])
paddle.reshape(x=paddle.abs(x=x).add(y), shape=[3])
paddle.add(x=paddle.abs(x=x), y=paddle.to_tensor(y)).reshape(3)
paddle.abs(x=x).add(y).reshape(3)
paddle.add(x=x.abs(), y=paddle.to_tensor(y)).reshape(3)
paddle.reshape(x=x.abs().add(y), shape=[3])
x.abs().add(y).reshape([3])
paddle.nn.CrossEntropyLoss().cuda(device_id=device2int(args.gpu))
model = paddle.nn.Sequential(
    paddle.nn.Conv2D(in_channels=1, out_channels=20, kernel_size=5),
    paddle.nn.ReLU(),
    paddle.nn.Conv2D(in_channels=20, out_channels=64, kernel_size=5),
    paddle.nn.ReLU(),
)
model = paddle.nn.Sequential(
    *[
        ("conv1", paddle.nn.Conv2D(in_channels=1, out_channels=20, kernel_size=5)),
        ("relu1", paddle.nn.ReLU()),
        ("conv2", paddle.nn.Conv2D(in_channels=20, out_channels=64, kernel_size=5)),
        ("relu2", paddle.nn.ReLU()),
    ]
)
blocks = []
blocks.append(("block1", paddle.nn.Linear(in_features=10, out_features=10)))
blocks.append(("block2", paddle.nn.Linear(in_features=10, out_features=10)))
paddle.nn.Sequential(*blocks)
blocks = []
blocks.append(paddle.nn.Linear(in_features=10, out_features=10))
blocks.append(paddle.nn.Linear(in_features=10, out_features=10))
paddle.nn.Sequential(*blocks)
paddle.nn.Sequential(
    paddle.nn.Conv2D(
        in_channels=in_dim,
        out_channels=in_dim,
        kernel_size=3,
        stride=2,
        padding=1,
        groups=in_dim,
    )
)
linears = paddle.nn.LayerList(
    sublayers=[paddle.nn.Linear(in_features=10, out_features=10) for i in range(10)]
)
layers = paddle.nn.LayerDict(
    sublayers={
        "conv": paddle.nn.Conv2D(in_channels=10, out_channels=10, kernel_size=3),
        "pool": paddle.nn.Conv2D(in_channels=10, out_channels=10, kernel_size=3),
    }
)
gelu = paddle.nn.GELU(approximate=True)
paddle.nn.GELU()
paddle.nn.GELU(approximate=False)
paddle.nn.functional.gelu(x=x, approximate=False)
y = paddle.nn.functional.gelu(x=x, approximate=False)
size = tuple(x.shape)
size = tuple(paddle.assign(paddle.abs(x=x), output=y).shape)
tuple(x.abs().shape)
image.size
image.size[2]
tuple(x.shape)[2]
shape = tuple(x.shape)
device = x.place
dtype = x.dtype
y = paddle.abs(x=x).T
shape = tuple(paddle.abs(x=x).shape)
tuple(paddle.abs(x=x).shape)
z = (paddle.triu(x=paddle.ones(shape=[sz, sz])) == 1).abs()
(x + y).abs()
(x == y).abs()
(-x).abs()
x.reshape(2, 3)
x.reshape([2, 2])
x.reshape(shape=[2, 3])
paddle.max(x=image)
paddle.max(x=image, axis=1), paddle.argmax(x=image, axis=1)
paddle.maximum(x=image, y=label)
paddle.min(x=image)
paddle.min(x=image, axis=1), paddle.argmin(x=image, axis=1)
paddle_min(image, label)
paddle_max(max_exp_avg_sq, exp_avg_sq, out=max_exp_avg_sq)
m = 2
n = 3
paddle.rand(shape=[m, n])
paddle.assign(paddle.randn(shape=[2 + 3, 3]), output=y)
paddle.assign(paddle.zeros(shape=[m + n, n], dtype="float32"), output=y)
y.stop_gradient = not True
y
out_3 = paddle.ones(shape=[2, 3])
out_3.stop_gradient = not False
out_3
paddle.empty(shape=[m, n]).pin_memory()
out_4 = paddle.full(shape=[2, 3], fill_value=1.0)
out_4.stop_gradient = not False
out_4
paddle.rand(shape=[2, 3])
paddle.rand(shape=(2, 3))
paddle.rand(shape=[2, 3])
paddle.rand(shape=(2, 3))
paddle.rand(shape=[2, 3])
paddle.rand(shape=())
paddle.rand(shape=[])
paddle.rand(shape=[2])
paddle.rand(shape=[2, 3])
paddle.rand(shape=[2, 3])
paddle.rand(shape=(2, 3))
shape = 2
paddle.rand(shape=shape)
shape = 2, 3
paddle.rand(shape=shape)
shape = [2, 3]
paddle.rand(shape=shape)
shape = 2, 3
paddle.rand(shape=shape)
paddle.randint(low=0, high=10, shape=[2, 2])
paddle.randint(low=2, high=10, shape=[2, 2])
tuple(paddle.abs(x=x).shape)
paddle.abs(x=x).shape[2]
tuple(x.shape)
x.shape[0]
paddle.abs(x=x).item()
x.item()
assert not not label.stop_gradient
out_5 = label
out_5.stop_gradient = not True
label_requires_grad = out_5
out_6 = label
out_6.stop_gradient = not False
label = out_6
requires_grad = [True, False]
out_7 = label
out_7.stop_gradient = not requires_grad[1]
out_7
assert not label.stop_gradient
assert not label_requires_grad.stop_gradient
paddle.einsum("...ijk, ...xijk -> ...xjk", mask, a4)
if pic.mode == "1":
    img = 255 * img
if pic.mode == "1":
    img = 255 * img
return paddle.to_tensor(data=nppic).to(dtype=default_float_dtype)
x.transpose(perm=[2, 3])
x.transpose(perm=[2, 3])
x.transpose(perm=[2, 3])
import numpy as np

np.array([2.0, 3.0]).repeat(2, axis=0)
x.tile(repeat_times=[2, 3])
x.tile(repeat_times=[2, 3])
x.tile(repeat_times=[2, 3])
import numpy
import numpy as np

x = paddle.rand(shape=[2, 3])
x.view(np.int32)
x.view(numpy.int32)
x.view(3, 2)
x.view([3, 2])
x.view("int32")
x.to("float64")
cuda0 = device2str("cuda:0")
x.to(gpu0)
other = paddle.randn(shape=(), dtype="float64")
x.to(other, blocking=not True)
x = paddle.rand(shape=[2, 3])
x.astype(dtype="float32")
x.astype(dtype="float64")
x.astype(dtype="int32")
x.astype(dtype="int64")
x = paddle.rand(shape=[2, 3])
y = paddle.rand(shape=[2, 3])
x.astype("float32")
x.astype("float32")
x.astype(dtype=y.dtype)
x.type_as(tensor=y)
paddle.nn.functional.interpolate(x=input_data, scale_factor=[2, 1])
paddle.nn.functional.interpolate(
    x=input_data, scale_factor=[2, 1], recompute_scale_factor=True
)
paddle.nn.functional.interpolate(
    x=input_data, scale_factor=[2, 1], recompute_scale_factor=False
)
>>>>>>torch.nn.functional.interpolate(input_data, scale_factor=[2, 1], antialias=False)
device = device2str("cuda")
paddle.to_tensor(data=1.0, place=device)
paddle.to_tensor(data=1.0, place=device2str("gpu:1"))
paddle.to_tensor(data=1.0, place="gpu")
paddle.to_tensor(data=1.0, place="gpu:1")
paddle.to_tensor(data=1.0)
paddle.to_tensor(data=1.0, stop_gradient=not True)
paddle.to_tensor(data=1.0, dtype="float32", place=device2str("cuda:0"))
import numpy as np
from np import array

np.add(x, y)
array(1.0).abs().add(y)
paddle.abs(x=x)
(array(1.0) + array(2.0)).abs()
(array(1.0) - array(2.0)).abs()
(array(1.0) * array(2.0).numpy()).abs()
"""_torch.npy"""
str1 = "_torch.npy"
str2 = "_torch.npy"
hellotorch.test
paddle.save(obj=obj, path="torch.parma")
np.save("torch.parma")
paddle.to_tensor(data=features_A).T.cuda()
all_dists = dists.transpose()
all_dists = dists.transpose(perm=dim2perm(dists.ndim, 0, 1))
paddle.nn.CrossEntropyLoss().to(device2str("gpu"))
missing_keys, unexpected_keys = model_without_ddp.set_state_dict(
    state_dict=checkpoint["model"]
)
linear = paddle.nn.Linear(in_features=10, out_features=10)
state_dict = linear.state_dict()
linear.set_state_dict(state_dict=state_dict)
linear.parameters()
linear.named_parameters()
linear.buffers()
linear.named_buffers()
linear.children()
linear.named_children()
linear.sublayers()
linear.named_sublayers(include_self=True)
linear.train()
linear.eval()
out_8 = linear
out_8.stop_gradient = not True
out_8
linear.clear_gradients(set_to_zero=False)
>>>>>>sgd = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
state_dict = sgd.state_dict()
sgd.set_state_dict(state_dict=state_dict)
sgd.clear_gradients(set_to_zero=False)
sgd.step()
x.place
args.device
self.args.device
x = x + self.pos_embed.expand(shape=[B, -1, -1]).detach()
(attn @ v).transpose(perm=dim2perm((attn @ v).ndim, -2, -1))
x = (
    self.proj(x)
    .flatten(start_axis=2)
    .transpose(perm=dim2perm(self.proj(x).flatten(start_axis=2).ndim, 1, 2))
)
lt = paddle.max(x=boxes1[:, None, :2])
lt = paddle_max(boxes1[:, None, :2], boxes2[:, :2])
lt = paddle.min(x=boxes1[:, None, :2])
lt = paddle_min(boxes1[:, None, :2], boxes2[:, :2])
paddle.sum(x=input, axis=1)
paddle.sum(x=input, axis=1, dtype="float32")
paddle.mean(x=input, axis=1).astype("float32")
src_logits.take_along_axis(axis=2, indices=activated_class_ids, broadcast=False)
paddle.vision.models.resnet50
import numpy
############################## 相关utils函数，如下 ##############################

def dim2perm(ndim, dim0, dim1):
    perm = list(range(ndim))
    perm[dim0], perm[dim1] = perm[dim1], perm[dim0]
    return perm

def _Tensor_add(self, *args, **kwargs):
    if "other" in kwargs:
        y = kwargs["other"]
    elif "y" in kwargs:
        y = kwargs["y"]
    else:
        y = args[0]
    if "alpha" in kwargs:
        alpha = kwargs["alpha"]
        if alpha != 1:
            if not isinstance(y, paddle.Tensor):
                y = paddle.to_tensor(alpha * y)
            else:
                y = alpha * y
    else:
        if not isinstance(y, paddle.Tensor):
            y = paddle.to_tensor(y)
    return paddle.add(self, y)

setattr(paddle.Tensor, "add", _Tensor_add)

def _Tensor_reshape(self, *args, **kwargs):
    if args:
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            return paddle.reshape(self, args[0])
        else:
            return paddle.reshape(self, list(args))
    elif kwargs:
        assert "shape" in kwargs
        return paddle.reshape(self, shape=kwargs["shape"])

setattr(paddle.Tensor, "reshape", _Tensor_reshape)

def device2int(device):
    if isinstance(device, str):
        device = device.replace('cuda', 'gpu')
        device = device.replace('gpu:', '')
    return int(device)

def paddle_min(*args, **kwargs):
    if "input" in kwargs:
        kwargs["x"] = kwargs.pop("input")

    out_v = None
    if "out" in kwargs:
        out_v = kwargs.pop("out")

    if "other" in kwargs:
        kwargs["y"] = kwargs.pop("other")
        ret = paddle.minimum(*args, **kwargs)
    elif len(args)==2 and isinstance(args[1], paddle.Tensor):
        ret = paddle.minimum(*args, **kwargs)
    else:
        if "dim" in kwargs:
            kwargs["axis"] = kwargs.pop("dim")

        if "axis" in kwargs or len(args) >= 2:
            if out_v:
                ret = paddle.min(*args, **kwargs), paddle.argmin(*args, **kwargs)
                paddle.assign(ret[0], out_v[0])
                paddle.assign(ret[1], out_v[1])
                return out_v
            else:
                ret = paddle.min(*args, **kwargs), paddle.argmin(*args, **kwargs)
                return ret
        else:
            ret = paddle.min(*args, **kwargs)
            return ret

    if out_v:
        paddle.assign(ret, out_v)
        return out_v
    else:
        return ret

def paddle_max(*args, **kwargs):
    if "input" in kwargs:
        kwargs["x"] = kwargs.pop("input")

    out_v = None
    if "out" in kwargs:
        out_v = kwargs.pop("out")

    if "other" in kwargs:
        kwargs["y"] = kwargs.pop("other")
        ret = paddle.maximum(*args, **kwargs)
    elif len(args)==2 and isinstance(args[1], paddle.Tensor):
        ret = paddle.maximum(*args, **kwargs)
    else:
        if "dim" in kwargs:
            kwargs["axis"] = kwargs.pop("dim")

        if "axis" in kwargs or len(args) >= 2:
            if out_v:
                ret = paddle.max(*args, **kwargs), paddle.argmax(*args, **kwargs)
                paddle.assign(ret[0], out_v[0])
                paddle.assign(ret[1], out_v[1])
                return out_v
            else:
                ret = paddle.max(*args, **kwargs), paddle.argmax(*args, **kwargs)
                return ret
        else:
            ret = paddle.max(*args, **kwargs)
            return ret

    if out_v:
        paddle.assign(ret, out_v)
        return out_v
    else:
        return ret

def device2str(type=None, index=None, *, device=None):
    type = device if device else type
    if isinstance(type, int):
        type = f'gpu:{type}'
    elif isinstance(type, str):
        if 'cuda' in type:
            type = type.replace('cuda', 'gpu')
        if 'cpu' in type:
            type = 'cpu'
        elif index is not None:
            type = f'{type}:{index}'
    elif isinstance(type, paddle.CPUPlace) or (type is None):
        type = 'cpu'
    elif isinstance(type, paddle.CUDAPlace):
        type = f'gpu:{type.get_device_id()}'

    return type

def _Tensor_view(self, *args, **kwargs):
    if args:
        if len(args)==1 and isinstance(args[0], (tuple, list, str)):
            return paddle.view(self, args[0])
        else:
            return paddle.view(self, list(args))
    elif kwargs:
        return paddle.view(self, shape_or_dtype = list(kwargs.values())[0])

setattr(paddle.Tensor, 'view', _Tensor_view)

def _Tensor_min(self, *args, **kwargs):
    if "other" in kwargs:
        kwargs["y"] = kwargs.pop("other")
        ret = paddle.minimum(self, *args, **kwargs)
    elif len(args) == 1 and isinstance(args[0], paddle.Tensor):
        ret = paddle.minimum(self, *args, **kwargs)
    else:
        if "dim" in kwargs:
            kwargs["axis"] = kwargs.pop("dim")

        if "axis" in kwargs or len(args) >= 1:
            ret = paddle.min(self, *args, **kwargs), paddle.argmin(self, *args, **kwargs)
        else:
            ret = paddle.min(self, *args, **kwargs)

    return ret

setattr(paddle.Tensor, "_min", _Tensor_min)

def _Tensor_max(self, *args, **kwargs):
    if "other" in kwargs:
        kwargs["y"] = kwargs.pop("other")
        ret = paddle.maximum(self, *args, **kwargs)
    elif len(args) == 1 and isinstance(args[0], paddle.Tensor):
        ret = paddle.maximum(self, *args, **kwargs)
    else:
        if "dim" in kwargs:
            kwargs["axis"] = kwargs.pop("dim")

        if "axis" in kwargs or len(args) >= 1:
            ret = paddle.max(self, *args, **kwargs), paddle.argmax(self, *args, **kwargs)
        else:
            ret = paddle.max(self, *args, **kwargs)

    return ret

setattr(paddle.Tensor, "_max", _Tensor_max)

import numpy as np
def _Tensor_index_copy_(self, dim, index, source):
    if dim == 0:
        return self.scatter_(index, source)

    shape = self.shape

    new_index = []
    for i in range(0, np.prod(shape[:dim])):
        new_index.append(index + i * len(index))
    new_index = paddle.concat(new_index)
    new_self = self.reshape_([-1] + shape[dim+1:])
    new_source = source.reshape([-1] + shape[dim+1:])

    return new_self.scatter_(new_index, new_source).reshape_(shape)

setattr(paddle.Tensor, "index_copy_", _Tensor_index_copy_)
############################## 相关utils函数，如上 ##############################


>>>>>>mmcv.load
>>>>>>mmcv.dump
>>>>>>mmdet.models.build_backbone
>>>>>>mmdet3d.core.bbox.structures.lidar_box3d.LiDARInstance3DBoxes
>>>>>>mmdet3d.core.draw_heatmap_gaussian
x.cuda()
a == True
>>>>>>torch.backends.cudnn.deterministic()
x.astype(dtype="bfloat16")
x.astype(dtype="bool")
x.astype(dtype="uint8")
x.astype(dtype="int8")
x.astype(dtype="float64")
x.astype(dtype="float32")
x.astype(dtype="float16")
x.astype(dtype="int32")
x.astype(dtype="int64")
x.astype(dtype="int16")
"""Not Support auto convert *.chalf, please judge whether it is Pytorch API and convert by yourself"""
>>>>>>x.chalf()
x.astype(dtype="complex64")
x.astype(dtype="complex128")
x.expand(shape=[2])
x.expand(shape=[2, 3])
x.expand(shape=[2])
x.expand(shape=(2, 3))
x.expand(shape=[2, 3])
x.expand(shape=[2, 3])
x.expand(shape=(2, 3))
list1 = [2, 3]
x.expand(shape=list1)
list1 = 2, 3
x.expand(shape=list1)
mask = mask.astype(dtype="float32").masked_fill(mask=mask == 1, value=float("-inf"))
paddle.nn.CrossEntropyLoss(reduction="none")
a = paddle.to_tensor(
    data=paddle.to_tensor(data=[2, 3, 4]),
    dtype="float32",
    place=device2str("gpu"),
    stop_gradient=not True,
)
print("[torch.tensor case-1]: ", tuple(a.shape), a.dtype)
flag = True
a = paddle.to_tensor(
    data=paddle.to_tensor(data=[2, 3, 4]),
    dtype="float32",
    place=device2str("gpu"),
    stop_gradient=not flag,
)
print("[torch.tensor case-2]: ", tuple(a.shape), a.dtype)
print("[torch.cuda.is_available case-1]: ", paddle.device.cuda.device_count() >= 1)


def a(x: paddle.Tensor):
    pass


a = paddle.empty(shape=[2, 3])
print("[torch.Tensor case-2]: ", tuple(a.shape), a.dtype)


def a(x: paddle.Tensor):
    pass


a = paddle.empty(shape=[2, 3], dtype="int64")
print("[LongTensor case-2]: ", tuple(a.shape), a.dtype)


def a(x: paddle.Tensor):
    pass


a = paddle.empty(shape=[2, 3, 6], dtype="int32")
print("[IntTensor case-2]: ", tuple(a.shape), a.dtype)


def a(x: paddle.Tensor):
    pass


a = paddle.empty(shape=[2, 3, 6], dtype="float32")
print("[FloatTensor case-2]: ", tuple(a.shape), a.dtype)
a = paddle.nn.functional.interpolate(
    x=paddle.randn(shape=[1, 2, 20, 20]), size=[24, 24]
)
print("[nn.functional.interpolate case-1]: ", tuple(a.shape))
a = paddle.nn.functional.interpolate(
    x=paddle.rand(shape=[1, 2, 20, 20]), scale_factor=0.6
)
print("[nn.functional.interpolate case-2]: ", tuple(a.shape))
r = paddle.equal_all(
    x=paddle.to_tensor(data=[1, 2]), y=paddle.to_tensor(data=[1, 2])
).item()
print("[equal]: ", r)
a = paddle.randint(low=2, high=5, shape=[3, 4])
print("[randint]: ", tuple(a.shape), a._min(), a._max())
paddle.randint(low=0, high=10, shape=[2, 2])
print("[randint]: ", tuple(a.shape), a._min(), a._max())
a, b = 2, 25
a = paddle.randint(low=a, high=b, shape=[3, 4])
print("[randint]: ", tuple(a.shape), a._min(), a._max())
print(paddle.__version__)
a = paddle.to_tensor(data=[1, 2, 3])
b = paddle.to_tensor(data=[4, 5, 6], dtype="float64", stop_gradient=not True)
print("[Tensor.new_tensor case-1]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
b = paddle.to_tensor(data=[4, 5, 6], dtype=a.dtype)
print("[Tensor.new_tensor case-2]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
out_9 = paddle.zeros(shape=[3, 4], dtype="float64")
out_9.stop_gradient = not True
b = out_9
print("[Tensor.new_zeros case-1]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
b = paddle.zeros(shape=[3, 4], dtype=a.dtype)
print("[Tensor.new_zeros case-2]: ", b)
b = paddle.zeros(shape=[3, 4], dtype=a.dtype)
print("[Tensor.new_zeros case-3]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
out_10 = paddle.ones(shape=[3, 4], dtype="float64")
out_10.stop_gradient = not True
b = out_10.pin_memory()
print("[Tensor.new_ones case-1]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="float64")
out_11 = paddle.ones(shape=[3, 4], dtype=a.dtype)
out_11.stop_gradient = not True
b = out_11
print("[Tensor.new_ones case-2]: ", b)
b = paddle.ones(shape=[3, 4], dtype=a.dtype)
print("[Tensor.new_ones case-3]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
out_12 = paddle.full(shape=[3, 4], fill_value=2.43, dtype="float64")
out_12.stop_gradient = not True
b = out_12.pin_memory()
print("[Tensor.new_full case-1]: ", b)
flag = False
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
out_13 = paddle.full(shape=(2, 3), fill_value=4, dtype=a.dtype)
out_13.stop_gradient = not flag
b = out_13
print("[Tensor.new_full case-2]: ", b)
a = paddle.to_tensor(data=[1, 2, 3], dtype="int64")
out_14 = paddle.empty(shape=(3, 4), dtype="float64")
out_14.stop_gradient = not True
b = out_14.pin_memory()
print("[Tensor.new_empty case-1]: ", b)
a = paddle.to_tensor(data=[1, 3, 4, 9, 0.5, 1.5])
a = a.normal_(mean=0.2, std=0.3)
print("[Tensor.normal_ case-1]: ", a)
c = paddle.to_tensor(data=a.uniform_(min=2, max=6))
print("[Tensor.uniform_ case-1]: ", c)
x = paddle.to_tensor(data=[[1], [2], [3]])
y = x.expand(shape=[3, 4])
print("[Tensor.expand case-1]: ", tuple(y.shape))
x = paddle.to_tensor(data=[[1], [2], [3]])
y = x.expand(shape=(3, 4))
print("[Tensor.expand case-2]: ", tuple(y.shape))
paddle.seed(seed=23)
paddle.zeros(shape=[2], dtype=x.dtype)
paddle.zeros(shape=[2, 3], dtype=x.dtype)
paddle.zeros(shape=[2, 3], dtype=x.dtype)
paddle.zeros(shape=(2, 3), dtype=x.dtype)
shape = 2
paddle.zeros(shape=shape, dtype=x.dtype)
shape = 2, 3
out_15 = paddle.zeros(shape=shape, dtype=x.dtype)
out_15.stop_gradient = not True
out_15
shape = 2, 3
out_16 = paddle.zeros(shape=shape, dtype="float32")
out_16.stop_gradient = not True
out_16
out_17 = paddle.zeros(shape=shape, dtype="float32")
out_17.stop_gradient = not True
out_17.pin_memory()
out_18 = paddle.zeros(shape=shape, dtype="float32")
out_18.stop_gradient = not True
out_18
paddle.zeros(shape=tuple(x.shape), dtype=x.dtype)
paddle.zeros(shape=tuple(x.shape), dtype=x.dtype)
paddle.full(shape=[2, 3], fill_value=2.0, dtype=x.dtype)
out_19 = paddle.full(shape=[2, 3], fill_value=2.0, dtype=x.dtype)
out_19.stop_gradient = not True
out_19
out_20 = paddle.full(shape=[2, 3], fill_value=2.0, dtype=x.dtype)
out_20.stop_gradient = not True
out_20
out_21 = paddle.full(shape=[2, 3], fill_value=2.0, dtype="float32")
out_21.stop_gradient = not True
out_21.pin_memory()
g_cpu = paddle.framework.core.default_cpu_generator()
print("[torch.Generator() case-1]: ", g_cpu)
g_cpu = paddle.framework.core.default_cpu_generator()
print("[torch.Generator() case-2]: ", g_cpu)
g_cpu = paddle.framework.core.default_cpu_generator()
print("[torch.Generator() case-3]: ", g_cpu)
print(tuple([2, 8, 64, 64]))
assert tuple(paddle.randn(shape=[6, 5, 7]).shape) == tuple([6, 5, 7])
out = tuple([6, 5, 7])
shape_nchw = tuple([6, 5, 7])
assert out == tuple(shape_nchw)
print(tuple([1]))
shape = tuple([1])
x = paddle.zeros(shape=[5, 3])
t = paddle.to_tensor(data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype="float32")
index = paddle.to_tensor(data=[0, 4, 2])
x.index_copy_(0, index, t)
print("[torch.Tensor.index_copy_ case-1]: ", x)
x = paddle.zeros(shape=[2, 1, 3, 3])
t = paddle.to_tensor(
    data=[[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]],
    dtype="float32",
)
index = paddle.to_tensor(data=[0, 1, 2])
x.index_copy_(2, index, t)
print("[torch.Tensor.index_copy_ case-2]: ", x)
x = paddle.zeros(shape=[5, 3])
t = paddle.to_tensor(data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype="float32")
index = paddle.to_tensor(data=[0, 4, 2])
y = x.index_copy_(0, index, t)
print("[torch.Tensor.index_copy_ case-3]: ", y)
x = paddle.zeros(shape=[2, 1, 3, 3])
t = paddle.to_tensor(
    data=[[[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]],
    dtype="float32",
)
index = paddle.to_tensor(data=[0, 1, 2])
y = x.index_copy_(2, index, t)
print("[torch.Tensor.index_copy_ case-4]: ", y)
x = paddle.zeros(shape=[20])
t = paddle.to_tensor(data=[1, 3, 4, 5], dtype="float32")
index = paddle.to_tensor(data=[0, 12, 2, 1])
y = x.index_copy_(0, index, t)
print("[torch.Tensor.index_copy_ case-5]: ", y)
data = paddle.to_tensor(data=[23.0, 32.0, 43.0])
if not not data.stop_gradient:
    print(1)
print(not data.stop_gradient)
data.stop_gradient = not False
requires_grad = not data.stop_gradient
data = paddle.to_tensor(
    data=[23.0, 32.0, 43.0], stop_gradient=not not data.stop_gradient
)
print((not data.stop_gradient) == False)
print(not not data.stop_gradient)
print("{} , {}".format("1", str(not data.stop_gradient)))


def test():
    return True


data.stop_gradient = not test()
z = True, False, True
a, temp, c = z
data.stop_gradient = not temp
print(not data.stop_gradient)
m = paddle.nn.InstanceNorm3D(num_features=100)
input = paddle.randn(shape=[20, 100, 35, 45, 10])
output = m(input)
print("[torch.nn.InstanceNorm3d case-1]: ", output)
m = paddle.nn.InstanceNorm3D(num_features=100, weight_attr=True, bias_attr=True)
input = paddle.randn(shape=[20, 100, 35, 45, 10])
output = m(input)
print("[torch.nn.InstanceNorm3d case-2]: ", output)
m = paddle.nn.InstanceNorm3D(num_features=100, weight_attr=False, bias_attr=False)
input = paddle.randn(shape=[20, 100, 35, 45, 10])
output = m(input)
print("[torch.nn.InstanceNorm3d case-3]: ", output)
m = paddle.nn.InstanceNorm3D(
    num_features=100, weight_attr=True, bias_attr=True, momentum=1 - 0.1
)
input = paddle.randn(shape=[20, 100, 35, 45, 10])
output = m(input)
print("[torch.nn.InstanceNorm3d case-4]: ", output)
m = paddle.nn.InstanceNorm3D(
    num_features=100, weight_attr=False, bias_attr=False, momentum=1 - 0.1
)
input = paddle.randn(shape=[20, 100, 35, 45, 10])
output = m(input)
print("[torch.nn.InstanceNorm3d case-5]: ", output)
loss = paddle.nn.BCEWithLogitsLoss(reduction="none")
input = paddle.to_tensor(data=[1.0, 0.7, 0.2], stop_gradient=not True)
target = paddle.to_tensor(data=[1.0, 0.0, 0.0])
output = loss(input, target)
print("[torch.nn.BCEWithLogitsLoss case-1]: ", output)
loss = paddle.nn.BCEWithLogitsLoss(
    weight=paddle.to_tensor(data=[1.0, 0.2, 0.2]), reduction="none"
)
input = paddle.to_tensor(data=[1.0, 0.7, 0.2], stop_gradient=not True)
target = paddle.to_tensor(data=[1.0, 0.0, 0.0])
output = loss(input, target)
print("[torch.nn.BCEWithLogitsLoss case-2]: ", output)
loss = paddle.nn.BCEWithLogitsLoss(pos_weight=paddle.ones(shape=[3]))
input = paddle.to_tensor(data=[1.0, 0.7, 0.2], stop_gradient=not True)
target = paddle.to_tensor(data=[1.0, 0.0, 0.0])
output = loss(input, target)
print("[torch.nn.BCEWithLogitsLoss case-3]: ", output)
loss = paddle.nn.BCEWithLogitsLoss(reduction="mean")
input = paddle.to_tensor(data=[1.0, 0.7, 0.2], stop_gradient=not True)
target = paddle.to_tensor(data=[1.0, 0.0, 0.0])
output = loss(input, target)
print("[torch.nn.BCEWithLogitsLoss case-4]: ", output)
loss = paddle.nn.BCEWithLogitsLoss()
input = paddle.to_tensor(data=[1.0, 0.7, 0.2], stop_gradient=not True)
target = paddle.to_tensor(data=[1.0, 0.0, 0.0])
output = loss(input, target)
print("[torch.nn.BCEWithLogitsLoss case-5]: ", output)
o = list(paddle.io.BatchSampler(sampler=range(10), batch_size=3, drop_last=True))
print("[torch.utils.data.BatchSampler case-1]: ", o)
o = list(paddle.io.BatchSampler(sampler=range(10), batch_size=3, drop_last=False))
print("[torch.utils.data.BatchSampler case-2]: ", o)
batch_sampler_train = paddle.io.BatchSampler(
    sampler=range(10), batch_size=2, drop_last=True
)
print("[torch.utils.data.BatchSampler case-3]: ", list(batch_sampler_train))
batch_size = 4
batch_sampler_train = paddle.io.BatchSampler(
    sampler=range(10), batch_size=batch_size, drop_last=False
)
print("[torch.utils.data.BatchSampler case-4]: ", list(batch_sampler_train))
batch_size = 4
batch_sampler_train = paddle.io.BatchSampler(
    sampler=range(10), batch_size=batch_size, drop_last=False
)
print("[torch.utils.data.BatchSampler case-5]: ", list(batch_sampler_train))
cpu = device2str("cpu")
a = paddle.randn(shape=[2, 3])
c = paddle.randn(shape=[2, 3], dtype="float64")
b = a.to(cpu, blocking=not False)
print("[torch.Tensor.to case-1]: ", b)
b = a.to("cpu")
print("[torch.Tensor.to case-2]: ", b)
b = a.to(device=cpu, dtype="float64")
print("[torch.Tensor.to case-3]: ", b)
b = a.to("float64")
print("[torch.Tensor.to case-4]: ", b)
b = a.to(dtype="float64")
print("[torch.Tensor.to case-5]: ", b)
b = a.to(c)
print("[torch.Tensor.to case-6]: ", b)
a = a.to("float16")
print("[torch.Tensor.to case-8]: ", b)
table = a
b = a.to(table.place)
print("[torch.Tensor.to case-9]: ", b)
b = a.to("float32")
print("[torch.Tensor.to case-10]: ", b)
device = device2str("cpu")
b = paddle.to_tensor(data=[-1]).to("bool")
print("[torch.Tensor.to case-11]: ", b)
dtype = "float32"
b = a.to(dtype=dtype)
print("[torch.Tensor.to case-12]: ", b)
b = a.to(device2str("cpu"))
print("[torch.Tensor.to case-13: ", b)