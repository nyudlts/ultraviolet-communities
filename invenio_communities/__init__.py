# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Invenio digital library framework."""

from __future__ import absolute_import, print_function

from .ext import Communities
from .proxies import current_communities

__all__ = ('Communities', 'current_communities')
