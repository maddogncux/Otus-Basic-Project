from http import HTTPStatus


from django.test import TestCase
from django.urls import reverse, reverse_lazy
from .models import Event

class TestEventTestCase(TestCase):

    fixtures = [
        "event.fixture.json",
        "event_Posts.fixture.json",
        "event_Tags.fixture.json",
    ]

    url = reverse_lazy("event:events")


    def test_event_list(self):
        url = reverse("event:events")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        event = (Event
                    .objects
                    # .select_related("tags")
                    .prefetch_related("post", "tags")
                    .all()
                    )
        event_in_context = response.context["events"]
        self.assertEqual(len(event), len(event_in_context))
        for a1, a2 in zip(event, event_in_context):
            self.assertEqual(a1.pk, a2.pk)


    def test_anon_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["user"].is_anonymous)