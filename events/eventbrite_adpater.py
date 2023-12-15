import json
import urllib3
from django.conf import settings
from urllib3.exceptions import HTTPError


class EventbriteAdapter:
    BASE_URL = 'https://www.eventbriteapi.com/v3/'
    ORGANIZATION_ENDPOINT = f'{BASE_URL}organizations/{settings.ORGANIZATION_ID}/'
    DIRECT_EVENTS_ENDPOINT = f'{BASE_URL}events/'
    EVENTS_ENDPOINT = f'{ORGANIZATION_ENDPOINT}events/'
    VENUES_ENDPOINT = f'{ORGANIZATION_ENDPOINT}venues/'

    def __init__(self):
        self.api_key = settings.EVENTBRITE_0AUTH_TOKEN
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        self.http = urllib3.PoolManager()

    def _send_request(self, method, endpoint, data=None):
        encoded_data = json.dumps(data).encode('utf-8') if data else None

        try:
            response = self.http.request(method, endpoint, headers=self.headers, body=encoded_data, retries=False,
                                         timeout=urllib3.Timeout(connect=2.0, read=7.0))
            return json.loads(response.data.decode('utf-8'))

        except HTTPError as e:
            print(f"Failed request to {endpoint}. Error: {str(e)}")
            return None

        except Exception as e:
            print(f"An error occurred while making the request to {endpoint}: {str(e)}")
            return None

    def get_events(self):
        return self._send_request('GET', self.EVENTS_ENDPOINT).get('events', [])


    def get_event_detail(self, event_id):
        return self._send_request('GET', f'{self.DIRECT_EVENTS_ENDPOINT}{event_id}/?expand=ticket_classes,venue')

    def create_event(self, event_data):
        return self._send_request('POST', self.EVENTS_ENDPOINT, data=event_data)

    def create_venue(self, venue_data):
        res = self._send_request('POST', self.VENUES_ENDPOINT, data=venue_data)
        return res['id'] if res else None

    def create_inventory_tier(self, event_id, inventory_data):
        url = f'{self.DIRECT_EVENTS_ENDPOINT}{event_id}/inventory_tiers/'
        res = self._send_request('POST', url, data=inventory_data)
        return res['inventory_tier']['id'] if res else None

    def create_ticket_class(self, event_id, ticket_data):
        url = f'{self.DIRECT_EVENTS_ENDPOINT}{event_id}/ticket_classes/'
        res = self._send_request('POST', url, data=ticket_data)
        return res['id'] if res else None



    def get_organization_id(self):
        res = self._send_request('GET', f'{self.BASE_URL}users/me/organizations/')
        organizations = res.get('organizations', None)
        if organizations:
            return organizations[0]['id']
        return


    def create_organization(self):
        organization_data = {
            "event": {
                "name": {"html": "<p>Some text</p>"},
                "description": {"html": "<p>Some text</p>"},
                "start": {"timezone": "UTC", "utc": "2018-05-12T02:00:00Z"},
                "end": {"timezone": "UTC", "utc": "2018-05-12T02:00:00Z"},
                "currency": "USD",
            }
        }

        response_data = self._send_request('POST', self.ORGANIZATION_ENDPOINT, data=organization_data)

        if response_data:
            organization_id = response_data.get('id')
            print(f"Organization created successfully with ID: {organization_id}")
            return organization_id
        else:
            return None


