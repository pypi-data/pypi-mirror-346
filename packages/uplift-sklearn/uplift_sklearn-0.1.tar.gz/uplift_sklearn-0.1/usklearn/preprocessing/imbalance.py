"""Handle class imbalance."""

import numpy as np

from sklearn.utils import check_random_state

from ..base import UpliftRegressorMixin

def class_flip(y, trt, n_trt=None, kc0=1, kc1=1, kt0=1, kt1=1, k=None,
               random_state=None):
    rng = check_random_state(random_state)
    if k is not None:
        raise RuntimeError("multiclass/treatment flipping not implemented.")
    assert 0 <= kc0 <= 1
    assert 0 <= kc1 <= 1
    assert 0 <= kt0 <= 1
    assert 0 <= kt1 <= 1
    mask_c0 = ((trt==0) & (y==0))
    mask_c1 = ((trt==0) & (y==1))
    mask_t0 = ((trt==1) & (y==0))
    mask_t1 = ((trt==1) & (y==1))
    for mask, k in [(mask_c0, kc0), (mask_c1, kc1), (mask_t0, kt0), (mask_t1, kt1)]:
        if k == 1:
            continue
        n = mask.sum()
        n_flip = int(n * k)
        mask_flip = rng.choice(np.flatnonzero(mask), n_flip)
        y[mask_flip] = 1-y[mask_flip]
    return y

