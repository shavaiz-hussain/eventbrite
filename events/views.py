from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .eventbrite_adpater import EventbriteAdapter
from .forms import EventForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EventListView(LoginRequiredMixin, View):
    template_name = "events/list.html"
    detail_template_name = "events/detail.html"

    def get(self, request, *args, **kwargs):
        eventbrite_adapter = EventbriteAdapter()
        event_id = self.kwargs.get("event_id")
        eventbrite_adapter.get_organization_id()
        if event_id:
            event = eventbrite_adapter.get_event_detail(event_id)
            ticket_class = (
                event["ticket_classes"][0] if event["ticket_classes"] else None
            )
            return render(
                request,
                self.detail_template_name,
                {"event": event, "ticket_class": ticket_class},
            )

        events = eventbrite_adapter.get_events()

        return render(request, self.template_name, {"events": events})


class CreateEventView(LoginRequiredMixin, View):
    template_name = "events/create.html"

    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        adapter = EventbriteAdapter()
        try:
            if form.is_valid():
                # Process the form data, including latitude and longitude
                name = form.cleaned_data["name"]
                description = form.cleaned_data["description"]
                venue_name = form.cleaned_data["venue_name"]
                start_datetime = form.cleaned_data["start_datetime"]
                end_datetime = form.cleaned_data["end_datetime"]
                latitude = form.cleaned_data["latitude"]
                longitude = form.cleaned_data["longitude"]
                inventory_tier = form.cleaned_data["inventory_tier"]
                ticket_price = form.cleaned_data["ticket_price"]
                capacity = form.cleaned_data["ticket_price"]
                # first create the venue and then the event
                venue_payload = self.generate_venue_payload(
                    venue_name, latitude, longitude
                )
                venue = adapter.create_venue(venue_payload)
                if venue:
                    event_payload = self.generate_event_payload(
                        name, description, start_datetime, end_datetime, venue
                    )
                    event = adapter.create_event(event_payload)
                    if event:
                        inventory_tier_payload = self.generate_inventory_tier_data(
                            inventory_tier, capacity
                        )
                        inventory_tier = adapter.create_inventory_tier(
                            event["id"], inventory_tier_payload
                        )
                        if inventory_tier:
                            ticket_payload = self.generate_ticket_payload(
                                ticket_price * capacity, inventory_tier
                            )
                            adapter.create_ticket_class(event["id"], ticket_payload)

                    # Perform actions with the data, such as saving to the database
                    return redirect(
                        "event_list"
                    )  # Redirect to a success page or another view
        except Exception as e:
            return HttpResponse("Something went wrong while trying to submit the form")

        return render(request, self.template_name, {"form": form})

    @staticmethod
    def generate_venue_payload(name, lat, long):
        return {
            "venue": {
                "name": name,
                "capacity": 100,
                "address": {"latitude": lat, "longitude": long},
            }
        }

    @staticmethod
    def generate_event_payload(name, desc, start_datetime, end_datetime, venue_id):
        return {
            "event": {
                "name": {"html": f"<p>{name}</p>"},
                "description": {"html": f"<p>{desc}</p>"},
                "start": {
                    "timezone": "UTC",
                    "utc": start_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                "end": {
                    "timezone": "UTC",
                    "utc": end_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
                "venue_id": venue_id,
                "currency": "USD",
                "online_event": False,
                "organizer_id": "",
                "listed": False,
                "shareable": False,
                "invite_only": False,
                "show_remaining": True,
                "capacity": 100,
                "is_reserved_seating": True,
                "is_series": False,
                "show_pick_a_seat": True,
                "show_seatmap_thumbnail": True,
                "show_colors_in_seatmap_thumbnail": True,
            }
        }

    @staticmethod
    def generate_inventory_tier_data(name, capacity="1000"):
        return {
            "inventory_tier": {
                "name": name,
                "count_against_event_capacity": True,
                "quantity_total": capacity,
            }
        }

    @staticmethod
    def generate_ticket_payload(price, inv_id):
        return {
            "ticket_class": {
                "name": "Ticket Class",
                "free": False,
                "donation": False,
                "quantity_total": "",
                "minimum_quantity": "1",
                "maximum_quantity": "10",
                "cost": f"USD,{price}",
                "hidden": False,
                "auto_hide": False,
                "auto_hide_before": "",
                "auto_hide_after": "",
                "sales_channels": ["online", "atd"],
                "hide_sale_dates": False,
                "delivery_methods": ["electronic"],
                "inventory_tier_id": inv_id,
                "include_fee": False,
            }
        }
