# Copyright (C) 2014 Jason Trost <jason.trost@threatstream.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import json

from normalizer.modules.basenormalizer import BaseNormalizer


class P0fEvents(BaseNormalizer):
    channels = ('p0f.events',)

    def normalize(self, data, channel, submission_timestamp, ignore_rfc1918=True):
        o_data = json.loads(data)

        if ignore_rfc1918 and self.is_RFC1918_addr(o_data['client_ip']):
            return []

        session = {
            'timestamp': submission_timestamp,
            'source_ip': o_data['client_ip'],
            'source_port': int(o_data['client_port']),
            'destination_ip': o_data['server_ip'],
            'destination_port': int(o_data['server_port']),
            'honeypot': 'p0f',
            'protocol': 'pcap'
        }
        relations = {'session': session}
        return [relations]
