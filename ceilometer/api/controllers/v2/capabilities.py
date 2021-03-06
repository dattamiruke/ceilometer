#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright 2013 IBM Corp.
# Copyright 2013 eNovance <licensing@enovance.com>
# Copyright Ericsson AB 2013. All rights reserved
# Copyright 2014 Hewlett-Packard Company
# Copyright 2015 Huawei Technologies Co., Ltd.
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

import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from ceilometer.api.controllers.v2 import base
from ceilometer import utils


def _flatten_capabilities(capabilities):
    return dict((k, v) for k, v in utils.recursive_keypairs(capabilities))


class Capabilities(base.Base):
    """A representation of the API and storage capabilities.

    Usually constrained by restrictions imposed by the storage driver.
    """

    api = {wtypes.text: bool}
    "A flattened dictionary of API capabilities"
    storage = {wtypes.text: bool}
    "A flattened dictionary of storage capabilities"
    alarm_storage = {wtypes.text: bool}
    "A flattened dictionary of alarm storage capabilities"
    event_storage = {wtypes.text: bool}
    "A flattened dictionary of event storage capabilities"

    @classmethod
    def sample(cls):
        return cls(
            api=_flatten_capabilities({
                'meters': {'pagination': True,
                           'query': {'simple': True,
                                     'metadata': True,
                                     'complex': False}},
                'resources': {'pagination': False,
                              'query': {'simple': True,
                                        'metadata': True,
                                        'complex': False}},
                'samples': {'pagination': True,
                            'groupby': True,
                            'query': {'simple': True,
                                      'metadata': True,
                                      'complex': True}},
                'statistics': {'pagination': True,
                               'groupby': True,
                               'query': {'simple': True,
                                         'metadata': True,
                                         'complex': False},
                               'aggregation': {'standard': True,
                                               'selectable': {
                                                   'max': True,
                                                   'min': True,
                                                   'sum': True,
                                                   'avg': True,
                                                   'count': True,
                                                   'stddev': True,
                                                   'cardinality': True,
                                                   'quartile': False}}},
                'alarms': {'query': {'simple': True,
                                     'complex': True},
                           'history': {'query': {'simple': True,
                                                 'complex': True}}},
                'events': {'query': {'simple': True}},
            }),
            storage=_flatten_capabilities(
                {'storage': {'production_ready': True}}),
            alarm_storage=_flatten_capabilities(
                {'storage': {'production_ready': True}}),
            event_storage=_flatten_capabilities(
                {'storage': {'production_ready': True}}),
        )


class CapabilitiesController(rest.RestController):
    """Manages capabilities queries."""

    @wsme_pecan.wsexpose(Capabilities)
    def get(self):
        """Returns a flattened dictionary of API capabilities.

        Capabilities supported by the currently configured storage driver.
        """
        # variation in API capabilities is effectively determined by
        # the lack of strict feature parity across storage drivers
        conn = pecan.request.storage_conn
        alarm_conn = pecan.request.alarm_storage_conn
        event_conn = pecan.request.event_storage_conn
        driver_capabilities = conn.get_capabilities().copy()
        driver_capabilities['alarms'] = alarm_conn.get_capabilities()['alarms']
        driver_capabilities['events'] = event_conn.get_capabilities()['events']
        driver_perf = conn.get_storage_capabilities()
        alarm_driver_perf = alarm_conn.get_storage_capabilities()
        event_driver_perf = event_conn.get_storage_capabilities()
        return Capabilities(api=_flatten_capabilities(driver_capabilities),
                            storage=_flatten_capabilities(driver_perf),
                            alarm_storage=_flatten_capabilities(
                                alarm_driver_perf),
                            event_storage=_flatten_capabilities(
                                event_driver_perf))
