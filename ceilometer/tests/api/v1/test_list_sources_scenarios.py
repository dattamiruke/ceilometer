# -*- encoding: utf-8 -*-
#
# Copyright © 2012 Julien Danjou
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Test listing users.
"""
from ceilometer.tests import api as tests_api
from ceilometer.tests import db as tests_db


class TestListSource(tests_api.TestBase,
                     tests_db.MixinTestsWithBackendScenarios):

    def test_source(self):
        ydata = self.get('/sources/test_source')
        self.assertIn("somekey", ydata)
        self.assertEqual(666, ydata["somekey"])

    def test_unknownsource(self):
        ydata = self.get('/sources/test_source_that_does_not_exist')
        self.assertEqual({}, ydata)
