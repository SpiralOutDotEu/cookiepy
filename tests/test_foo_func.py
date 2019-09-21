#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cookiepy` package."""

import pytest
import cookiepy as p


class TestFooBar:
    def test_p_foo_returns_foo(self):
        assert p.foo() == 'foo'

    def test_p_bar_returns_bar(self):
        assert p.bar() == "bar"
