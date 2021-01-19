from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    
    quantity_from_form = int(request.POST["quantity"])
    price_from_form = float(request.POST["price"])
    total_charge = quantity_from_form * price_from_form

    print(f"Total Charge: {total_charge}")
    print("Charging credit card...")
    myOrder = Order.objects.create(
        quantity_ordered=quantity_from_form,
        total_price=total_charge
        )
    print(myOrder.id)
    return redirect(f'receipt/{myOrder.id}')

def receipt(request, myOrder):
    details = Order.objects.get(id=myOrder)
    allOrders = Order.objects.count()
    sumOrders = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    context = {
        "d": details,
        "orders": allOrders,
        "spend": sumOrders
    }
    return render(request, "store/checkout.html", context)

