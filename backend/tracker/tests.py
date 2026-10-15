from django.test import TestCase
from django.core.management import call_command
from pathlib import Path
from .models import Snapshot
from .scraper import parse_html
class WorkflowTests(TestCase):
    def setUp(self):
        fixtures=Path(__file__).resolve().parents[2]/"fixtures"
        for day in (1,2,3):
            call_command("import_snapshot",str(fixtures/f"day{day}.html"),at=f"2026-10-0{day}T10:00:00+00:00")
    def test_import_idempotency(self):
        before=Snapshot.objects.count()
        call_command("import_snapshot",str(Path(__file__).resolve().parents[2]/"fixtures/day3.html"),at="2026-10-03T10:00:00+00:00")
        self.assertEqual(Snapshot.objects.count(),before)
    def test_api_filter_history_export(self):
        products=self.client.get("/api/products/?q=headphones").json()
        self.assertEqual(len(products),1)
        self.assertEqual(len(self.client.get(f'/api/products/{products[0]["id"]}/history/').json()),6)
        self.assertContains(self.client.get("/api/export/"),"currency")
        self.assertEqual(self.client.get("/api/products/999/history/").status_code,404)
    def test_bad_source_fails(self):
        with self.assertRaises(ValueError): parse_html("<html></html>")
