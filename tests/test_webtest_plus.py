#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from nose.tools import *  # PEP8 asserts

from .testapp import app
from webtest_plus import TestApp


class TestTestApp(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.auth = ("admin", "secret")

    def test_auth_get(self):
        res = self.app.get("/foo/bar/", auth=self.auth)
        assert_equal(res.status_code, 200)

    def test_bad_auth_get(self):
        # /foo/bar/ requires HTTP basic auth
        res = self.app.get("/foo/bar/", expect_errors=True)
        assert_equal(res.status_code, 401)
        bad_auth = ("no", "go")
        res = self.app.get("/foo/bar/", auth=bad_auth, expect_errors=True)
        assert_equal(res.status_code, 401)

    def test_auth_post(self):
        res = self.app.post("/foo/bar/baz/", auth=self.auth)
        assert_equal(res.status_code, 200)

    def test_auto_follow(self):
        res = self.app.get("/redirect/", auto_follow=True)
        assert_equal(res.status_code, 200)

    def test_authorize(self):
        self.app.authenticate(username='admin', password='secret')
        res = self.app.get("/foo/bar/")
        assert_equal(res.status_code, 200)
        self.app.deauthenticate()
        res = self.app.get("/foo/bar/", expect_errors=True)
        assert_equal(res.status_code, 401)

    def test_auth_put(self):
        assert_equal(self.app.put("/foo/bar/baz/", expect_errors=True).status_code,
                    401)
        assert_equal(self.app.put("/foo/bar/baz/", auth=self.auth).status_code, 200)

    def test_auth_patch(self):
        assert_equal(self.app.patch("/foo/bar/baz/", expect_errors=True).status_code,
                    401)
        assert_equal(self.app.patch("/foo/bar/baz/", auth=self.auth).status_code, 200)

    def test_auth_options(self):
        assert_equal(self.app.options("/foo/bar/baz/", expect_errors=True).status_code,
                    401)
        assert_equal(self.app.options("/foo/bar/baz/", auth=self.auth).status_code, 200)

    def test_auth_delete(self):
        assert_equal(self.app.delete("/foo/bar/baz/", expect_errors=True).status_code,
                    401)
        assert_equal(self.app.delete("/foo/bar/baz/", auth=self.auth).status_code, 200)

    def test_auth_post_json(self):
        assert_equal(self.app.post_json("/secretjson/", {"name": "Steve"},
                    expect_errors=True).status_code, 401)
        res = self.app.post_json("/secretjson/", {"name": "Steve"}, auth=self.auth)
        assert_equal(res.request.content_type, "application/json")
        assert_equal(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
