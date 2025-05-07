# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #
#
# This file provides wrappers for torch API that changed between versions,
# so that our other code didn't have to deal with those discrepancies.
#

from functools import wraps
from typing import Optional

import torch
from packaging import version
from torch._dynamo.utils import dynamo_timed

_IS_TORCH_2_6_OR_LATER = (
    version.Version(torch.__version__).release
    >= version.Version("2.6.0").release
)


# This API has been renamed and moved to a different location in 2.5. To make
# things simple in our code, import it under the previous name.
# This API has been renamed and moved to a different location in 2.5. To make
# things simple in our code, import it under the previous name.
from torch._subclasses.fake_tensor import (
    unset_fake_temporarily as maybe_disable_fake_tensor_mode,  # noqa: F401
)


def dynamo_timed_wrapper(phase_name: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return dynamo_timed(phase_name, phase_name=phase_name)(func)(
                *args, **kwargs
            )

        return wrapped

    return decorator
