# Copyright 2025 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# -*- coding: utf-8 -*-

from typing import Optional, Sequence

import brainunit as u
import jax
import numpy as np
from jax import numpy as jnp
from jax.interpreters import ad

from ._jitc_float_normal_impl import float_jitc_mv_normal_p_call, float_jitc_mm_normal_p_call
from ._jitc_util import _initialize_seed, _initialize_conn_length
from ._typing import Data, MatrixShape
from ._xla_custom_op import XLACustomKernel
from ._xla_custom_op_numba import NumbaKernelGenerator, numba_kernel
from ._xla_custom_op_util import general_batching_rule
from ._xla_custom_op_warp import dtype_to_warp_type, WarpKernelGenerator, warp_kernel

__all__ = [
    "event_jitc_normal_matvec",
    "event_jitc_normal_matmat",
]


def event_jitc_normal_matvec(
    w_loc: Data,
    w_scale: Data,
    prob: float,
    vector: Data,
    seed: Optional[int] = None,
    *,
    shape: MatrixShape,
    transpose: bool = False,
    corder: bool = True,
) -> Data:
    u.fail_for_dimension_mismatch(w_loc, w_scale, "w_loc and w_scale must have the same dimension.")
    seed = _initialize_seed(seed)
    w_loc, unitd = u.split_mantissa_unit(w_loc)
    w_scale = u.Quantity(w_scale).to(unitd).mantissa
    vector, unitv = u.split_mantissa_unit(vector)
    clen = _initialize_conn_length(prob)
    res = event_jitc_mv_normal_p_call(
        w_loc,
        w_scale,
        clen,
        vector,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder
    )[0]
    return u.maybe_decimal(res * unitd * unitv)


def event_jitc_normal_matmat(
    w_loc: Data,
    w_scale: Data,
    prob: float,
    B: Data,
    seed: Optional[int] = None,
    *,
    shape: MatrixShape,
    transpose: bool = False,
    corder: bool = True,
) -> Data:
    u.fail_for_dimension_mismatch(w_loc, w_scale, "w_loc and w_scale must have the same dimension.")
    seed = _initialize_seed(seed)
    w_loc, unitd = u.split_mantissa_unit(w_loc)
    w_scale = u.Quantity(w_scale).to(unitd).mantissa
    B, unitB = u.split_mantissa_unit(B)
    clen = _initialize_conn_length(prob)
    res = event_jitc_mm_normal_p_call(
        w_loc,
        w_scale,
        clen,
        B,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder
    )[0]
    return u.maybe_decimal(res * unitd * unitB)


def _jitc_mv_normal_cpu_kernel_generator(
    transpose: bool,
    corder: bool,
    vector_info: jax.ShapeDtypeStruct,
    **kwargs
):
    r"""Generate the CPU kernel for the :func:`_jitc_matvec_normal` operation.
    """

    if corder:
        # This means that the for loop is parallelized along the dimension of the output vector: ``post.shape[0]``.

        if transpose:
            if vector_info.dtype == jnp.bool_:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    # Output vector dimension = number of columns in the matrix
                    n_col = posts.shape[0]

                    # Input vector dimension = number of rows in the matrix
                    n_row = vector.shape[0]

                    # Extract scalar values from input arrays
                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    clen0 = clen[0]  # Connection length (inverse of connection probability)
                    seed0 = seed[0]  # Random seed

                    # Initialize the random number generator with the provided seed
                    # This ensures reproducibility for the same seed value
                    np.random.seed(seed0)

                    # Process each output element (column in the matrix)
                    for i_col in range(n_col):
                        # Generate first row index randomly - this determines where to start sampling
                        i_row = np.random.randint(0, clen0)

                        # Initialize accumulator for this output element with proper dtype
                        out = np.asarray(0., dtype=posts.dtype)

                        # Process all connected entries for this column
                        while i_row < n_row:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if vector[i_row]:
                                out += w

                            # Skip ahead to next connected row (sparse sampling)
                            # The random skip ensures proper connection probability
                            # Each skip distance is randomly determined to maintain the sparse pattern
                            i_row += np.random.randint(1, clen0)

                        posts[i_col] = out
            else:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    # Output vector dimension = number of columns in the matrix
                    n_col = posts.shape[0]

                    # Input vector dimension = number of rows in the matrix
                    n_row = vector.shape[0]

                    # Extract scalar values from input arrays
                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    clen0 = clen[0]  # Connection length (inverse of connection probability)
                    seed0 = seed[0]  # Random seed

                    # Initialize the random number generator with the provided seed
                    # This ensures reproducibility for the same seed value
                    np.random.seed(seed0)

                    # Process each output element (column in the matrix)
                    for i_col in range(n_col):
                        # Generate first row index randomly - this determines where to start sampling
                        i_row = np.random.randint(0, clen0)

                        # Initialize accumulator for this output element with proper dtype
                        out = np.asarray(0., dtype=posts.dtype)

                        # Process all connected entries for this column
                        while i_row < n_row:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if vector[i_row] != 0.:
                                out += w

                            # Skip ahead to next connected row (sparse sampling)
                            # The random skip ensures proper connection probability
                            # Each skip distance is randomly determined to maintain the sparse pattern
                            i_row += np.random.randint(1, clen0)

                        posts[i_col] = out

        else:
            if vector_info.dtype == jnp.bool_:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    # Output vector dimension = number of rows in the matrix
                    # Each row in the matrix will produce one element in the output vector
                    num_row = posts.shape[0]
                    num_col = vector.shape[0]
                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)
                    for i_row in range(num_row):
                        i_col = np.random.randint(0, clen0)
                        out = np.asarray(0., dtype=posts.dtype)
                        while i_col < num_col:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if vector[i_col]:
                                out += w
                            i_col += np.random.randint(1, clen0)
                        posts[i_row] = out
            else:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    # Output vector dimension = number of rows in the matrix
                    # Each row in the matrix will produce one element in the output vector
                    num_row = posts.shape[0]
                    num_col = vector.shape[0]
                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)
                    for i_row in range(num_row):
                        i_col = np.random.randint(0, clen0)
                        out = np.asarray(0., dtype=posts.dtype)
                        while i_col < num_col:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if vector[i_col] != 0.:
                                out += w
                            i_col += np.random.randint(1, clen0)
                        posts[i_row] = out

    else:
        if transpose:
            if vector_info.dtype == jnp.bool_:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    num_col = posts.shape[0]
                    num_row = vector.shape[0]
                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    clen0 = clen[0]  # Controls sparsity - higher values mean fewer connections
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    np.random.seed(seed0)
                    for i_row in range(num_row):
                        v = vector[i_row]
                        i_col = np.random.randint(0, clen0)
                        while i_col < num_col:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if v:
                                posts[i_col] += w
                            i_col += np.random.randint(1, clen0)
            else:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    num_col = posts.shape[0]
                    num_row = vector.shape[0]
                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    clen0 = clen[0]  # Controls sparsity - higher values mean fewer connections
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    np.random.seed(seed0)
                    for i_row in range(num_row):
                        v = vector[i_row] != 0.
                        i_col = np.random.randint(0, clen0)
                        while i_col < num_col:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if v:
                                posts[i_col] += w
                            i_col += np.random.randint(1, clen0)

        else:
            if vector_info.dtype == jnp.bool_:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    num_row = posts.shape[0]
                    num_col = vector.shape[0]

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    clen0 = clen[0]  # Controls sparsity - higher values mean fewer connections
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    np.random.seed(seed0)
                    for i_col in range(num_col):
                        v = vector[i_col]
                        i_row = np.random.randint(0, clen0)
                        while i_row < num_row:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if v:
                                posts[i_row] += w
                            i_row += np.random.randint(1, clen0)
            else:
                @numba_kernel(parallel=False, input_output_aliases={5: 0})
                def kernel(w_loc, w_scale, clen, vector, seed, _, posts):
                    num_row = posts.shape[0]
                    num_col = vector.shape[0]

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    clen0 = clen[0]  # Controls sparsity - higher values mean fewer connections
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    np.random.seed(seed0)
                    for i_col in range(num_col):
                        v = vector[i_col] != 0.
                        i_row = np.random.randint(0, clen0)
                        while i_row < num_row:
                            w = np.random.normal(loc=w_loc0, scale=w_scale0)
                            if v:
                                posts[i_row] += w
                            i_row += np.random.randint(1, clen0)
    return kernel


def _jitc_mv_normal_gpu_kernel_generator(
    w_loc_info: jax.ShapeDtypeStruct,
    w_scale_info: jax.ShapeDtypeStruct,
    clen_info: jax.ShapeDtypeStruct,
    vector_info: jax.ShapeDtypeStruct,
    out_info: jax.ShapeDtypeStruct,
    seed_info: jax.ShapeDtypeStruct,
    transpose: bool = False,
    corder: bool = True,
    **kwargs
):
    r"""
    Generate the GPU kernel for the :func:`_jitc_matvec_normal` operation.
    """
    import warp

    w_loc_dtype = dtype_to_warp_type(w_loc_info.dtype)
    w_scale_dtype = dtype_to_warp_type(w_scale_info.dtype)
    clen_dtype = dtype_to_warp_type(clen_info.dtype)
    v_dtype = dtype_to_warp_type(vector_info.dtype)
    seed_dtype = dtype_to_warp_type(seed_info.dtype)

    if corder:

        if transpose:
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                vector: warp.array1d(dtype=v_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array1d(dtype=w_loc_dtype),
                posts: warp.array1d(dtype=w_loc_dtype),
            ):
                # Input vector dimension (number of rows in the matrix)
                num_row = vector.shape[0]

                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]  # Connection length parameter (controls sparsity)
                seed0 = seed[0]  # Base random seed value

                # Get thread ID - each thread processes one output element
                i_col = warp.tid()

                # Initialize accumulator for dot product calculation
                r = float(0.0)

                # Initialize random state with base seed plus thread ID to ensure
                # different but reproducible random sequences across threads
                state = warp.rand_init(seed0 + i_col)

                # Sample the first connected row using random skipping
                # Start at a random position in [0, clen0) for variability in connection patterns
                i_row = warp.randi(state, 0, clen0)

                # Process all connected entries for this output element
                while i_row < num_row:
                    # Add contribution from the current connected element
                    r += vector[i_row] * (warp.randn(state) * w_scale0 + w_loc0)

                    # Skip ahead to next connected row using geometric-like distribution
                    # This creates sparse connectivity with ~1/clen0 connection probability
                    i_row += warp.randi(state, 1, clen0)

                # Scale accumulated sum by weight and store in output array
                posts[i_col] = r

        else:
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                vector: warp.array1d(dtype=v_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array1d(dtype=w_loc_dtype),
                posts: warp.array1d(dtype=w_loc_dtype),
            ):
                # Input vector dimension (number of columns in the matrix)
                num_col = vector.shape[0]

                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]  # Connection length parameter (controls sparsity)
                seed0 = seed[0]  # Base random seed value

                # Get thread ID - each thread processes one output element (one row of the matrix)
                i_row = warp.tid()

                # Initialize accumulator for dot product calculation
                r = float(0.0)

                # Initialize random state with base seed plus thread ID to ensure
                # different but reproducible random sequences across threads
                state = warp.rand_init(seed0 + i_row)

                # Sample the first connected column using random skipping
                # Start at a random position in [0, clen0) for variability in connection patterns
                i_col = warp.randi(state, 0, clen0)

                # Process all connected entries for this output element (row)
                while i_col < num_col:
                    # Add contribution from the current connected element
                    r += vector[i_col] * (warp.randn(state) * w_scale0 + w_loc0)

                    # Skip ahead to next connected column using geometric-like distribution
                    # This creates sparse connectivity with ~1/clen0 connection probability
                    i_col += warp.randi(state, 1, clen0)

                # Scale accumulated sum by weight and store in output array
                posts[i_row] = r
    else:

        if transpose:
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                vector: warp.array1d(dtype=v_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array1d(dtype=w_loc_dtype),
                posts: warp.array1d(dtype=w_loc_dtype),
            ):
                # Output dimension (number of columns in the matrix)
                num_col = posts.shape[0]

                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]  # Connection length parameter (controls sparsity)
                seed0 = seed[0]  # Base random seed value

                # Get thread ID - each thread processes one input element (row)
                i_row = warp.tid()

                # Pre-multiply the input value by weight for efficiency
                # This avoids multiplying inside the inner loop for each connection
                v = vector[i_row]

                # Initialize random state with base seed plus thread ID to ensure
                # different but reproducible random sequences across threads
                state = warp.rand_init(seed0 + i_row)

                # Sample the first connected column using random skipping
                # Start at a random position in [0, clen0) for variability in connection patterns
                i_col = warp.randi(state, 0, clen0)

                # Process all connected output positions for this input element
                while i_col < num_col:
                    # Atomically add contribution to the appropriate output element
                    # Using atomic operation because multiple threads may update the same output element
                    posts[i_col] += v * (warp.randn(state) * w_scale0 + w_loc0)

                    # Skip ahead to next connected column using geometric-like distribution
                    # This creates sparse connectivity with ~1/clen0 connection probability
                    i_col += warp.randi(state, 1, clen0)


        else:

            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                vector: warp.array1d(dtype=v_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array1d(dtype=w_loc_dtype),
                posts: warp.array1d(dtype=w_loc_dtype),
            ):
                # Output dimension (number of rows in the matrix)
                num_row = posts.shape[0]

                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]  # Connection length parameter (controls sparsity)
                seed0 = seed[0]  # Base random seed value

                # Get thread ID - each thread processes one input element (column)
                i_col = warp.tid()

                # Pre-multiply the input value by weight for efficiency
                # This avoids multiplying inside the inner loop for each connection
                v = vector[i_col]

                # Initialize random state with base seed plus thread ID to ensure
                # different but reproducible random sequences across threads
                state = warp.rand_init(seed0 + i_col)

                # Sample the first connected row using random skipping
                # Start at a random position in [0, clen0) for variability in connection patterns
                i_row = warp.randi(state, 0, clen0)

                # Process all connected output positions for this input element
                while i_row < num_row:
                    # Atomically add contribution to the appropriate output element
                    # Using atomic operation because multiple threads may update the same output element
                    posts[i_row] += v * (warp.randn(state) * w_scale0 + w_loc0)

                    # Skip ahead to next connected row using geometric-like distribution
                    # This creates sparse connectivity with ~1/clen0 connection probability
                    i_row += warp.randi(state, 1, clen0)

    dim = (out_info.shape[0] if corder else vector_info.shape[0])
    return warp_kernel(kernel, dim=dim, input_output_aliases={5: 0})


def _jitc_mv_normal_jvp_v(
    v_dot,
    w_loc,
    w_scale,
    clen,
    vector,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    return float_jitc_mv_normal_p_call(
        w_loc,
        w_scale,
        clen,
        v_dot,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder
    )


def _jitc_mv_normal_jvp_wloc(
    w_dot,
    w_loc,
    w_scale,
    clen,
    vector,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    return event_jitc_mv_normal_p_call(
        w_dot,
        w_scale,
        clen,
        vector,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder
    )


def _jitc_mv_normal_jvp_wscale(
    w_dot,
    w_loc,
    w_scale,
    clen,
    vector,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    return event_jitc_mv_normal_p_call(
        w_loc,
        w_dot,
        clen,
        vector,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder
    )


def _jitc_mv_normal_transpose_rules(
    ct,
    w_loc,
    w_scale,
    clen,
    vector,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    assert not ad.is_undefined_primal(clen)
    assert not ad.is_undefined_primal(seed)
    assert not ad.is_undefined_primal(w_loc)
    assert not ad.is_undefined_primal(w_scale)

    ct = ct[0]
    if ad.is_undefined_primal(vector):
        r = float_jitc_mv_normal_p_call(
            w_loc,
            w_scale,
            clen,
            ct,
            seed,
            shape=shape,
            transpose=not transpose,
            corder=not corder
        )[0]
        return w_loc, w_scale, clen, r, seed, _
    else:
        raise NotImplementedError(
            f"Transpose rule for {ct} not implemented "
            f"for event-driven COO matrix-vector product."
        )


def _jitc_mv_normal_batching(
    args,
    axes,
    **kwargs
):
    if tuple(axes) == (None, None, None, 0, None, None):
        assert args[3].ndim == 2, 'Batching axis 0 requires 2D input.'
        r = event_jitc_mm_normal_p_call(
            args[0],
            args[1],
            args[2],
            args[3].T,
            args[4],
            shape=kwargs['shape'],
            transpose=kwargs['transpose'],
            corder=kwargs['corder'],
        )
        return r, [1]
    elif tuple(axes) == (None, None, None, 1, None, None):
        assert args[3].ndim == 2, 'Batching axis 0 requires 2D input.'
        r = event_jitc_mm_normal_p_call(
            args[0],
            args[1],
            args[2],
            args[3],
            args[4],
            shape=kwargs['shape'],
            transpose=kwargs['transpose'],
            corder=kwargs['corder'],
        )
        return r, [1]
    else:
        return general_batching_rule(
            event_jitc_mv_normal_p,
            args,
            axes,
            **kwargs,
        )


def event_jitc_mv_normal_p_call(
    w_loc,
    w_scale,
    clen,
    vector,
    seed,
    *,
    shape: Sequence[int],
    transpose: bool,
    corder: bool,
):
    w_loc = jnp.atleast_1d(w_loc)
    w_scale = jnp.atleast_1d(w_scale)
    clen = jnp.atleast_1d(clen)

    assert len(shape) == 2, "The matrix shape should be a tuple of two integers."
    assert w_loc.shape == (1,), f"The weight shape should be (1,), but got {w_loc.shape}."
    assert w_scale.shape == (1,), f"The weight shape should be (1,), but got {w_scale.shape}."
    assert clen.shape == (1,), f"The clen shape should be (1,), but got {clen.shape}."
    assert vector.ndim == 1, f"The vector should be a 1D array, but got {vector.ndim}D."
    assert seed.shape == (1,), f"The seed shape should be (1,), but got {seed.shape}."

    if transpose:
        assert shape[0] == len(vector), f"The matrix shape and vector length do not match. {vector.shape} @ {shape}"
    else:
        assert shape[1] == len(vector), f"The matrix shape and vector length do not match. {shape} @ {vector.shape}"

    out_info = (
        jax.ShapeDtypeStruct([shape[1]], w_loc.dtype)
        if transpose else
        jax.ShapeDtypeStruct([shape[0]], w_loc.dtype)
    )

    return event_jitc_mv_normal_p(
        w_loc,
        w_scale,
        clen,
        vector,
        seed,
        jnp.zeros(out_info.shape, out_info.dtype),
        outs=[out_info],
        w_loc_info=jax.ShapeDtypeStruct(w_loc.shape, w_loc.dtype),
        w_scale_info=jax.ShapeDtypeStruct(w_scale.shape, w_scale.dtype),
        clen_info=jax.ShapeDtypeStruct(clen.shape, clen.dtype),
        vector_info=jax.ShapeDtypeStruct(vector.shape, vector.dtype),
        seed_info=jax.ShapeDtypeStruct(seed.shape, seed.dtype),
        out_info=out_info,
        shape=shape,
        transpose=transpose,
        corder=corder,
    )


event_jitc_mv_normal_p = XLACustomKernel('event_jitc_mv_normal')
event_jitc_mv_normal_p.def_cpu_kernel(NumbaKernelGenerator(_jitc_mv_normal_cpu_kernel_generator))
event_jitc_mv_normal_p.def_gpu_kernel(WarpKernelGenerator(_jitc_mv_normal_gpu_kernel_generator))
event_jitc_mv_normal_p.def_jvp_rule2(
    _jitc_mv_normal_jvp_wloc,
    _jitc_mv_normal_jvp_wscale,
    None,
    _jitc_mv_normal_jvp_v,
    None,
    None
)
event_jitc_mv_normal_p.def_transpose_rule(_jitc_mv_normal_transpose_rules)
event_jitc_mv_normal_p.def_batching_rule(_jitc_mv_normal_batching)


def _jitc_mm_normal_cpu_kernel_generator(
    transpose: bool,
    corder: bool,
    B_info: jax.ShapeDtypeStruct,
    **kwargs
):
    r"""
    Generate the CPU kernel for the :func:`_jitc_matmat_normal` operation.
    """

    if corder:
        if transpose:
            # JIT Matrix.T @ B
            #
            # - JIT matrix: [k, m]
            # - B: [k, n]

            if B_info.dtype == jnp.bool_:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (columns in M)
                    n = posts.shape[1]  # Number of columns in output matrix (columns in B)
                    k = B.shape[0]  # Number of rows in B (rows in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)

                    for i_m in range(m):
                        i_k = np.random.randint(0, clen0)
                        out = np.zeros(n, dtype=posts.dtype)
                        while i_k < k:
                            w = np.random.normal(w_loc0, w_scale0)
                            for j in range(B.shape[1]):
                                if B[i_k, j]:
                                    out[j] += w
                            i_k += np.random.randint(1, clen0)
                        posts[i_m] = out
            else:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (columns in M)
                    n = posts.shape[1]  # Number of columns in output matrix (columns in B)
                    k = B.shape[0]  # Number of rows in B (rows in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)

                    for i_m in range(m):
                        i_k = np.random.randint(0, clen0)
                        out = np.zeros(n, dtype=posts.dtype)
                        while i_k < k:
                            w = np.random.normal(w_loc0, w_scale0)
                            for j in range(B.shape[1]):
                                if B[i_k, j] != 0.:
                                    out[j] += w
                            i_k += np.random.randint(1, clen0)
                        posts[i_m] = out

        else:
            # JIT Matrix @ B
            #
            # - JIT matrix: [m, k]
            # - B: [k, n]

            if B_info.dtype == jnp.bool_:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (rows in M)
                    n = posts.shape[1]  # Number of columns in output matrix (columns in B)
                    k = B.shape[0]  # Number of rows in B (columns in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)  # Initialize random number generator with seed for reproducibility

                    for i_m in range(m):
                        i_k = np.random.randint(0, clen0)
                        out = np.zeros(n, dtype=posts.dtype)
                        while i_k < k:
                            w = np.random.normal(w_loc0, w_scale0)
                            for j in range(B.shape[1]):
                                if B[i_k, j]:
                                    out[j] += w
                            i_k += np.random.randint(1, clen0)
                        posts[i_m] = out

            else:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (rows in M)
                    n = posts.shape[1]  # Number of columns in output matrix (columns in B)
                    k = B.shape[0]  # Number of rows in B (columns in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)  # Initialize random number generator with seed for reproducibility

                    for i_m in range(m):
                        i_k = np.random.randint(0, clen0)
                        out = np.zeros(n, dtype=posts.dtype)
                        while i_k < k:
                            w = np.random.normal(w_loc0, w_scale0)
                            for j in range(B.shape[1]):
                                if B[i_k, j] != 0.:
                                    out[j] += w
                            i_k += np.random.randint(1, clen0)
                        posts[i_m] = out

    else:
        if transpose:
            # JIT Matrix.T @ B
            #
            # - JIT matrix: [k, m]
            # - B: [k, n]

            if B_info.dtype == jnp.bool_:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (columns in M)
                    k = B.shape[0]  # Number of rows in B (rows in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)  # Initialize random number generator with seed

                    for i_k in range(k):
                        indices = np.where(B[i_k])[0]
                        i_m = np.random.randint(0, clen0)
                        while i_m < m:
                            w = np.random.normal(w_loc0, w_scale0)
                            posts[i_m, indices] += w
                            i_m += np.random.randint(1, clen0)
            else:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (columns in M)
                    k = B.shape[0]  # Number of rows in B (rows in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)  # Initialize random number generator with seed

                    for i_k in range(k):
                        indices = np.where(B[i_k] != 0.)[0]
                        i_m = np.random.randint(0, clen0)
                        while i_m < m:
                            w = np.random.normal(w_loc0, w_scale0)
                            posts[i_m, indices] += w
                            i_m += np.random.randint(1, clen0)

        else:
            # JIT Matrix @ B
            #
            # - JIT matrix: [m, k]
            # - B: [k, n]

            if B_info.dtype == jnp.bool_:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (rows in M)
                    k = B.shape[0]  # Number of rows in B (columns in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)  # Initialize random number generator with seed
                    for i_k in range(k):
                        indices = np.where(B[i_k])[0]
                        i_m = np.random.randint(0, clen0)
                        while i_m < m:
                            w = np.random.normal(w_loc0, w_scale0)
                            posts[i_m, indices] += w
                            i_m += np.random.randint(1, clen0)

            else:
                def kernel(w_loc, w_scale, clen, B, seed, _, posts):
                    m = posts.shape[0]  # Number of rows in output matrix (rows in M)
                    k = B.shape[0]  # Number of rows in B (columns in M)

                    w_loc0 = w_loc[0]
                    w_scale0 = w_scale[0]
                    seed0 = seed[0]  # Random seed for reproducible matrix generation
                    clen0 = clen[0]  # Connection length parameter (controls sparsity)
                    np.random.seed(seed0)  # Initialize random number generator with seed
                    for i_k in range(k):
                        indices = np.where(B[i_k] != 0.)[0]
                        i_m = np.random.randint(0, clen0)
                        while i_m < m:
                            w = np.random.normal(w_loc0, w_scale0)
                            posts[i_m, indices] += w
                            i_m += np.random.randint(1, clen0)

    return numba_kernel(kernel, parallel=False, input_output_aliases={5: 0})


def _jitc_mm_normal_gpu_kernel_generator(
    w_loc_info: jax.ShapeDtypeStruct,
    w_scale_info: jax.ShapeDtypeStruct,
    clen_info: jax.ShapeDtypeStruct,
    B_info: jax.ShapeDtypeStruct,
    seed_info: jax.ShapeDtypeStruct,
    out_info: jax.ShapeDtypeStruct,
    TITLE_SIZE: int,
    transpose: bool = False,
    corder: bool = True,
    **kwargs
):
    import warp

    w_loc_dtype = dtype_to_warp_type(w_loc_info.dtype)
    w_scale_dtype = dtype_to_warp_type(w_scale_info.dtype)
    clen_dtype = dtype_to_warp_type(clen_info.dtype)
    B_dtype = dtype_to_warp_type(B_info.dtype)
    seed_dtype = dtype_to_warp_type(seed_info.dtype)

    if corder:
        if transpose:
            # JIT Matrix.T @ B
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                B: warp.array2d(dtype=B_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array2d(dtype=w_loc_dtype),
                posts: warp.array2d(dtype=w_loc_dtype),
            ):
                k = B.shape[0]
                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]
                seed0 = seed[0]

                i_m = warp.tid()
                state = warp.rand_init(seed0 + i_m)

                out = warp.tile_zeros(TITLE_SIZE, dtype=w_loc_dtype)
                i_k = warp.randi(state, 0, clen0)
                while i_k < k:
                    w = warp.randn(state) * w_scale0 + w_loc0
                    out += warp.tile_load(B[i_k], TITLE_SIZE) * w
                    i_k += warp.randi(state, 1, clen0)
                warp.tile_store(posts[i_m], out)

        else:
            # JIT Matrix @ B
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                B: warp.array2d(dtype=B_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array2d(dtype=w_loc_dtype),
                posts: warp.array2d(dtype=w_loc_dtype),
            ):
                k = B.shape[0]
                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]
                seed0 = seed[0]

                i_m = warp.tid()
                state = warp.rand_init(seed0 + i_m)

                out = warp.tile_zeros(TITLE_SIZE, dtype=w_loc_dtype)
                i_k = warp.randi(state, 0, clen0)
                while i_k < k:
                    w = warp.randn(state) * w_scale0 + w_loc0
                    out += warp.tile_load(B[i_k], TITLE_SIZE) * w
                    i_k += warp.randi(state, 1, clen0)
                warp.tile_store(posts[i_m], out)

    else:
        if transpose:
            # JIT Matrix.T @ B
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                B: warp.array2d(dtype=B_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array2d(dtype=w_loc_dtype),
                posts: warp.array2d(dtype=w_loc_dtype),
            ):
                m = posts.shape[0]
                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]
                seed0 = seed[0]

                i_k = warp.tid()
                state = warp.rand_init(seed0 + i_k)

                out = warp.tile_load(B[i_k], TITLE_SIZE)
                i_m = warp.randi(state, 0, clen0)
                while i_m < m:
                    w = warp.randn(state) * w_scale0 + w_loc0
                    warp.tile_atomic_add(posts[i_m], out * w)
                    i_m += warp.randi(state, 1, clen0)


        else:
            # JIT Matrix @ B
            def kernel(
                w_loc: warp.array1d(dtype=w_loc_dtype),
                w_scale: warp.array1d(dtype=w_scale_dtype),
                clen: warp.array1d(dtype=clen_dtype),
                B: warp.array2d(dtype=B_dtype),
                seed: warp.array1d(dtype=seed_dtype),
                _: warp.array2d(dtype=w_loc_dtype),
                posts: warp.array2d(dtype=w_loc_dtype),
            ):
                m = posts.shape[0]
                w_loc0 = w_loc[0]
                w_scale0 = w_scale[0]
                clen0 = clen[0]
                seed0 = seed[0]

                i_k = warp.tid()
                state = warp.rand_init(seed0 + i_k)

                out = warp.tile_load(B[i_k], TITLE_SIZE)
                i_m = warp.randi(state, 0, clen0)
                while i_m < m:
                    w = warp.randn(state) * w_scale0 + w_loc0
                    warp.tile_atomic_add(posts[i_m], out * w)
                    i_m += warp.randi(state, 1, clen0)

    tile = (out_info.shape[0] if corder else B_info.shape[0])
    kernel = warp_kernel(kernel, tile=tile, block_dim=256, input_output_aliases={5: 0})
    return kernel


def _jitc_mm_normal_jvp_wloc(
    w_dot,
    w_loc,
    w_scale,
    clen,
    B,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    return event_jitc_mm_normal_p_call(
        w_dot,
        w_scale,
        clen,
        B,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder,
    )


def _jitc_mm_normal_jvp_wscale(
    w_dot,
    w_loc,
    w_scale,
    clen,
    B,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    return event_jitc_mm_normal_p_call(
        w_loc,
        w_dot,
        clen,
        B,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder,
    )


def _jitc_mm_normal_jvp_B(
    B_dot,
    w_loc,
    w_scale,
    clen,
    B,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    return float_jitc_mm_normal_p_call(
        w_loc,
        w_scale,
        clen,
        B_dot,
        seed,
        shape=shape,
        transpose=transpose,
        corder=corder,
    )


def _jitc_mm_normal_transpose_rules(
    ct,
    w_loc,
    w_scale,
    clen,
    B,
    seed,
    _,
    *,
    shape,
    transpose,
    corder,
    **kwargs
):
    assert not ad.is_undefined_primal(clen)
    assert not ad.is_undefined_primal(seed)
    assert not ad.is_undefined_primal(w_loc)
    assert not ad.is_undefined_primal(w_scale)

    ct = ct[0]
    if ad.is_undefined_primal(B):
        r = float_jitc_mm_normal_p_call(
            w_loc,
            w_scale,
            clen,
            ct,
            seed,
            shape=shape,
            transpose=not transpose,
            corder=not corder,
        )[0]

        return w_loc, w_scale, clen, r, seed, _

    else:
        raise NotImplementedError(
            'Transpose rules for jitc_matmat_normal not implemented for '
            'non-undefined primals.'
        )


def _batching_axis0(args, axes, **kwargs):
    assert args[3].ndim == 3, 'Batching axis 0 requires 3D input.'
    batch_size, m, n = args[3].shape
    B = jnp.transpose(args[3], (1, 0, 2)).reshape(m, batch_size * n)
    r = event_jitc_mm_normal_p_call(
        args[0],
        args[1],
        args[2],
        B,
        args[4],
        shape=kwargs['shape'],
        transpose=kwargs['transpose'],
        corder=kwargs['corder'],
    )
    r = jnp.reshape(r[0], [r[0].shape[0], batch_size, n])
    return [r], [1]


def _jitc_mm_normal_batching(
    args,
    axes,
    **kwargs
):
    if tuple(axes) == (None, None, None, 0, None, None):
        return _batching_axis0(args, axes, **kwargs)

    elif tuple(axes) == (None, None, None, 1, None, None):
        assert args[3].ndim == 3, 'Batching axis 0 requires 3D input.'
        args = list(args)
        args[3] = jnp.transpose(args[3], (1, 0, 2))
        return _batching_axis0(args, axes, **kwargs)

    elif tuple(axes) == (None, None, None, 1, None, None):
        assert args[3].ndim == 3, 'Batching axis 0 requires 3D input.'
        args = list(args)
        args[3] = jnp.transpose(args[3], (2, 0, 1))
        return _batching_axis0(args, axes, **kwargs)

    else:
        return general_batching_rule(
            event_jitc_mm_normal_p,
            args,
            axes,
            **kwargs,
        )


def event_jitc_mm_normal_p_call(
    w_loc,
    w_scale,
    clen,
    B,
    seed,
    *,
    shape: MatrixShape,
    transpose: bool,
    corder: bool,
):
    w_loc = jnp.atleast_1d(w_loc)
    w_scale = jnp.atleast_1d(w_scale)
    clen = jnp.atleast_1d(clen)

    assert len(shape) == 2, "The matrix shape should be a tuple of two integers."
    assert B.ndim == 2, "The input matrix B should be a 2D array."
    assert seed.ndim == 1, "The seed should be a 1D array."
    assert w_loc.ndim == 1, "The weight should be a 1D array."
    assert w_scale.ndim == 1, "The weight should be a 1D array."
    assert clen.ndim == 1, "The clen should be a 1D array."
    assert w_loc.shape == (1,), "The weight should be a scalar."
    assert w_scale.shape == (1,), "The weight should be a scalar."
    assert clen.shape == (1,), "The clen should be a scalar."
    assert seed.shape == (1,), "The seed should be a scalar."
    if transpose:
        assert shape[0] == B.shape[0], f"The matrix shape and B shape do not match. {B.shape} @ {shape}"
    else:
        assert shape[1] == B.shape[0], f"The matrix shape and B shape do not match. {shape} @ {B.shape}"

    out_info = (
        jax.ShapeDtypeStruct([shape[1], B.shape[1]], w_loc.dtype)
        if transpose else
        jax.ShapeDtypeStruct([shape[0], B.shape[1]], w_loc.dtype)
    )

    return event_jitc_mm_normal_p(
        w_loc,
        w_scale,
        clen,
        B,
        seed,
        jnp.zeros(out_info.shape, out_info.dtype),
        outs=[out_info],
        w_loc_info=jax.ShapeDtypeStruct(w_loc.shape, w_loc.dtype),
        w_scale_info=jax.ShapeDtypeStruct(w_scale.shape, w_scale.dtype),
        clen_info=jax.ShapeDtypeStruct(clen.shape, clen.dtype),
        B_info=jax.ShapeDtypeStruct(B.shape, B.dtype),
        seed_info=jax.ShapeDtypeStruct(seed.shape, seed.dtype),
        out_info=out_info,
        shape=shape,
        transpose=transpose,
        corder=corder,
        TITLE_SIZE=B.shape[1],  # Assuming B is [k, n], we want to process n columns at once
    )


event_jitc_mm_normal_p = XLACustomKernel('event_jitc_mm_normal')
event_jitc_mm_normal_p.def_cpu_kernel(NumbaKernelGenerator(_jitc_mm_normal_cpu_kernel_generator))
event_jitc_mm_normal_p.def_gpu_kernel(WarpKernelGenerator(_jitc_mm_normal_gpu_kernel_generator))
event_jitc_mm_normal_p.def_jvp_rule2(
    _jitc_mm_normal_jvp_wloc,
    _jitc_mm_normal_jvp_wscale,
    None,
    _jitc_mm_normal_jvp_B,
    None,
    None
)
event_jitc_mm_normal_p.def_transpose_rule(_jitc_mm_normal_transpose_rules)
event_jitc_mm_normal_p.def_batching_rule(_jitc_mm_normal_batching)
