from pathlib import Path
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from tracker.models import Product, Snapshot
from tracker.scraper import parse_html
class Command(BaseCommand):
    help="Import a local HTML snapshot. Repeat imports are idempotent."
    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument("--at", required=True, help="Timezone-aware ISO timestamp")
    def handle(self,*args,**options):
        try:
            at=datetime.fromisoformat(options["at"])
            if at.tzinfo is None: raise ValueError("Timestamp must include timezone")
            rows=parse_html(Path(options["file"]).read_text())
            with transaction.atomic():
                for row in rows:
                    p,_=Product.objects.update_or_create(sku=row.pop("sku"),defaults={"name":row.pop("name"),"category":row.pop("category")})
                    source=row.pop("source")
                    Snapshot.objects.update_or_create(product=p,source=source,checked_at=at,defaults=row)
            self.stdout.write(self.style.SUCCESS(f"Imported {len(rows)} offers"))
        except (ValueError,OSError) as exc:
            raise CommandError(str(exc))
