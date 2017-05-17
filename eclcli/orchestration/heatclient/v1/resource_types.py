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
from eclcli.orchestration.heatclient.common import utils

from oslo_utils import encodeutils
from six.moves.urllib import parse

from eclcli.orchestration.heatclient.openstack.common.apiclient import base


class ResourceType(base.Resource):
    def __repr__(self):
        return "<ResourceType %s>" % self._info

    def data(self, **kwargs):
        return self.manager.data(self, **kwargs)

    def _add_details(self, info):
        self.resource_type = info


class ResourceTypeManager(base.BaseManager):
    resource_class = ResourceType
    KEY = 'resource_types'

    def list(self, **kwargs):
        """Get a list of resource types.

        :rtype: list of :class:`ResourceType`
        """

        url = '/%s' % self.KEY
        params = {}
        if 'filters' in kwargs:
            filters = kwargs.pop('filters')
            params.update(filters)
            url += '?%s' % parse.urlencode(params, True)

        return self._list(url, self.KEY)

    def get(self, resource_type):
        """Get the details for a specific resource_type.

        :param resource_type: name of the resource type to get the details for
        """
        url_str = '/%s/%s' % (
                  self.KEY,
                  parse.quote(encodeutils.safe_encode(resource_type), ''))
        resp = self.client.get(url_str)
        body = utils.get_response_body(resp)
        return body

    def generate_template(self, resource_type, template_type='cfn'):
        url_str = '/%s/%s/template' % (
                  self.KEY,
                  parse.quote(encodeutils.safe_encode(resource_type), ''))
        if template_type:
            url_str += '?%s' % parse.urlencode(
                {'template_type': template_type}, True)
        resp = self.client.get(url_str)
        body = utils.get_response_body(resp)
        return body
