# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .base import AttributesProvider
import os
import opentelemetry.util.types as api_types
from typing import Mapping


class EnvironmentVariablesAttributesProvider(AttributesProvider):
    """
    Provides :py:type:``api_types.Attributes`` from environment variables.
    """

    #: Attribute key to environment variable key map.
    _attributes: Mapping[str, str]

    def __init__(self, attributes: Mapping[str, str]):
        self._attributes = attributes

    def attributes(self) -> api_types.Attributes:
        return {
            attribute_key: os.environ[environment_variable_key]
            for attribute_key, environment_variable_key in self._attributes.items()
            if environment_variable_key in os.environ
        }
