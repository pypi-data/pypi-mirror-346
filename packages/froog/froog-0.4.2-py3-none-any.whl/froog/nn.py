#  _______  ______    _______  _______  _______ 
# |       ||    _ |  |       ||       ||       |
# |    ___||   | ||  |   _   ||   _   ||    ___|
# |   |___ |   |_||_ |  | |  ||  | |  ||   | __ 
# |    ___||    __  ||  |_|  ||  |_|  ||   ||  |
# |   |    |   |  | ||       ||       ||   |_| |
# |___|    |___|  |_||_______||_______||_______|

from froog.tensor import Tensor
import numpy as np

def Linear(*x):
  # random Glorot initialization
  ret = np.random.uniform(-1., 1., size=x)/np.sqrt(np.prod(x))
  return ret.astype(np.float32)

def swish(x):
  return x.mul(x.sigmoid())

# *************************************
#     _   ___   __   ____  ____  _____
#    / | / / | / /  / __ \/ __ \/ ___/
#   /  |/ /  |/ /  / / / / /_/ /\__ \ 
#  / /|  / /|  /  / /_/ / ____/___/ / 
# /_/ |_/_/ |_/   \____/_/    /____/  
#
# ************* nn ops ************   

class BatchNorm2D:
  """
  __call__ follows the formula from the link below
  pytorch version: https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html

  self.weight       = γ
  self.bias         = β
  self.running_mean = E[x] 
  self.running_var  = Var[x]

  the reshaping step ensures that each channel of the input has its 
  own separate set of parameters (mean, variance, weight, and bias)

  self.running_mean has shape [num_channels].
  self.running_mean.reshape(shape=[1, -1, 1, 1]) reshapes it to [1, num_channels, 1, 1]
  """
  def __init__(self, sz, eps=0.001):
    self.eps = eps
    self.weight = Tensor.zeros(sz)
    self.bias = Tensor.zeros(sz)

    # TODO: need running_mean and running_var
    self.running_mean = Tensor.zeros(sz)
    self.running_var = Tensor.zeros(sz)
    self.num_batches_tracked = Tensor.zeros(1)

  def __call__(self, x):
    x = x.sub(self.running_mean.reshape(shape=[1, -1, 1, 1]))
    x = x.mul(self.weight.reshape(shape=[1, -1, 1, 1]))
    x = x.div(self.running_var.add(Tensor([self.eps], gpu=x.gpu)).reshape(shape=[1, -1, 1, 1]).sqrt())
    x = x.add(self.bias.reshape(shape=[1, -1, 1, 1]))
    return x