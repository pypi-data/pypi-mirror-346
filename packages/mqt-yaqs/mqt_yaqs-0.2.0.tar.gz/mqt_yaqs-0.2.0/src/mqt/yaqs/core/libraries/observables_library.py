# Copyright (c) 2025 Chair for Design Automation, TUM
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""Library of observables matrices.

This module provides a collection of matrices representing quantum observables,
such as the Pauli X, Y, and Z matrices. These matrices are useful in quantum
computing and simulation tasks.
"""

from __future__ import annotations

import numpy as np

ObservablesLibrary = {
    "x": np.array([[0, 1], [1, 0]]),
    "y": np.array([[0, -1j], [1j, 0]]),
    "z": np.array([[1, 0], [0, -1]]),
    "h": np.array([[1, 1], [1, -1]]) / np.sqrt(2),
    "id": np.eye(2),
    "sx": 0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]),
    "cx": np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]),
    "cz": np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]),
}
