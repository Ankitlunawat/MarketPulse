import csv
from decimal import Decimal
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
def records():
    result=[]
    for p in Product.objects.prefetch_related("snapshots").order_by("id"):
        grouped={}
        for s in p.snapshots.all():
            grouped.setdefault(s.source,[]).append(s)
        offers=[]
        for source, observations in grouped.items():
            latest=observations[-1]
            prev=observations[-2] if len(observations)>1 else None
            offers.append({"source":source,"price":str(latest.price),"currency":latest.currency,"available":latest.available,"url":latest.url,"checked_at":latest.checked_at.isoformat(),"change":str(latest.price-prev.price) if prev else None})
        available=[Decimal(o["price"]) for o in offers if o["available"]]
        result.append({"id":p.id,"sku":p.sku,"name":p.name,"category":p.category,"best_price":str(min(available)) if available else None,"offers":offers})
    return result
@api_view(["GET"])
def products(request):
    rows=records()
    query=request.GET.get("q","").lower()
    category=request.GET.get("category","")
    return Response([p for p in rows if query in p["name"].lower() and (not category or p["category"]==category)])
@api_view(["GET"])
def history(request,pk):
    p=get_object_or_404(Product,pk=pk)
    return Response([{"source":s.source,"price":str(s.price),"currency":s.currency,"checked_at":s.checked_at.isoformat()} for s in p.snapshots.all()])
@api_view(["GET"])
def summary(request):
    rows=records()
    return Response({"mode":"Synthetic portfolio demo","products":len(rows),"sources":len({o["source"] for p in rows for o in p["offers"]}),"available_offers":sum(o["available"] for p in rows for o in p["offers"]),"price_drops":sum(o["change"] is not None and Decimal(o["change"])<0 for p in rows for o in p["offers"])})
@api_view(["GET"])
def export(request):
    response=HttpResponse(content_type="text/csv")
    response["Content-Disposition"]='attachment; filename="marketpulse.csv"'
    writer=csv.writer(response)
    writer.writerow(["sku","name","category","source","price","currency","available","change","checked_at"])
    for p in records():
        for o in p["offers"]:
            writer.writerow([p["sku"],p["name"],p["category"],o["source"],o["price"],o["currency"],o["available"],o["change"],o["checked_at"]])
    return response
