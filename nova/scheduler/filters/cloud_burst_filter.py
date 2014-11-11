# Copyright (c) 2014 ThoughtWorks
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo.config import cfg

from nova.openstack.common import log as logging
from nova.scheduler import filters

opts = [
    cfg.BoolOpt('cloud_burst',
                help='Switch to enable could bursting'),
    cfg.StrOpt('cloud_burst_availablity_zone',
                help='The availability zone of only compute hosts with the public cloud driver'),
]
CONF = cfg.CONF
CONF.register_opts(opts)

LOG = logging.getLogger(__name__)


class CloudBurstFilter(filters.BaseHostFilter):
    """CloudBurstFilter returns the hosts with """

    # Aggregate data and instance type does not change within a request
    run_filter_once_per_request = True


    def host_passes(self, host_state, filter_properties):
        spec = filter_properties.get('request_spec', {})
        props = spec.get('instance_properties', {})
        availability_zone = props.get('availability_zone')

        LOG.info("cloud burst options = %s, %s" % (CONF.cloud_burst, CONF.cloud_burst_availablity_zone))
        LOG.info("avaiablity zone = %s" % availability_zone)

        if CONF.cloud_burst:
            if availability_zone == CONF.cloud_burst_availablity_zone or availability_zone == None:
                return True
            else:
                return False
        return True