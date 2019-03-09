from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from eco.forms import ReviewForm
from eco.models import Product, Category


def home(req):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    context = {"products": products, "categories": categories}
    return render(req, "eco/home.html", context)


def search(req):
    q = req.get["q"]
    products = Product.objects.filter(active=True, name__icontains=q)
    categories = Category.objects.filter(active=True)
    context = {'products': products,
               'categories': categories,
               'title': q + "-search"}
    return render(req, "eco/list.html", context)


def categories(req, slug):
    cat = Category.objects.get(slug=slug)
    products = Product.objects.filter(active=True, category=cat)
    categories = Category.objects.filter(active=True)
    context = {"products": products, "categories": categories, "title": cat.name + " - Categories"}
    return render(req, "eco/list.html", context)


def detail(req, slug):
    product = Product.objects.get(active=True, slug=slug)
    if req.method=="post":
        form=ReviewForm(req.post)
        if form.is_valid():
            review=form.save(commit=False)
            review.product=product
            review.user=req.user
            review.save()
            messages.success(req,"Review saved")
        else:
            messages.error(req,"Invalid form")
    else:
        form=ReviewForm()
    categories = Category.objects.filter(active=True)
    context = {"product": product,
               "categories": categories,
               "form":form}
    return render(req, "eco/detail.html", context)


def cart(req, slug):
    product = Product.objects.get(slug=slug)
    initial = {"items": [], "price": 0.0, "count": 0}
    session = req.session.get("data", initial)
    if slug in session["items"]:
        messages.error(req, "Already added to cart")
    else:
        session["items"].append(slug)
        session["price"] += float(product.price)
        session["count"] += 1
        req.session["data"] = session
        messages.success(req, "Added Successfully")
    return redirect("eco:detail", slug)


def mycart(req):
    sess = req.session.get("data", {"items": []})
    products = Product.objects.filter(active=True, slug__in=["items"])
    categories = Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": "My Cart"}
    return render(req, "eco/list.html", context)


def checkout(req):
    req.session.pop('data', None)
    return redirect("/")
