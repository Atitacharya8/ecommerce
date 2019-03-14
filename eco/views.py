from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from eco.forms import ReviewForm, SigninForm, SignupForm
from eco.models import Product, Category

from eco.serializer import ProductSerializer


def about(req):
    return render(req,"eco/about.html")


def home(req):
    products = Product.objects.filter(active=True)
    categories = Category.objects.filter(active=True)
    context = {"products": products, "categories": categories}
    return render(req, "eco/home.html", context)


def search(req):
    q = req.GET["q"]
    products = Product.objects.filter(active=True, name__icontains=q)
    categories = Category.objects.filter(active=True)
    context = {'products': products,
               'categories': categories,
               'title': q + " - search"}
    return render(req, "eco/list.html", context)


def categories(req, slug):
    cat = Category.objects.get(slug=slug)
    products = Product.objects.filter(active=True, category=cat)
    categories = Category.objects.filter(active=True)
    context = {"products": products, "categories": categories, "title": cat.name + " - Categories"}
    return render(req, "eco/list.html", context)


def detail(req, slug):
    product = Product.objects.get(active=True, slug=slug)
    if req.method == "POST":
        form = ReviewForm(req.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = req.user
            review.save()
            messages.success(req, "Review saved")
        else:
            messages.error(req, "Invalid form")
    else:
        form = ReviewForm()

    categories = Category.objects.filter(active=True)
    context = {"product": product,
               "categories": categories,
               "form": form}
    return render(req, "eco/detail.html", context)


def profile(req):
    return render(req,"eco/profile.html")


def signup(req):
    if req.method == "POST":
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(req, "User saved")
            return redirect("eco:signin")
        else:
            messages.error(req, "Error in form")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(req, "eco/signup.html", context)


def signin(req):
    if req.method == "POST":
        form = SigninForm(req.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, "Successfully logged in")
            return redirect("eco:home")
        else:
            messages.error(req, "Invalid Username or Password")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(req, "eco/signin.html", context)


def signout(req):
    logout(req)
    return redirect("eco:signin")


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
    sess1 = req.session.get("data", {"items": []})
    products = Product.objects.filter(active=True, slug__in=sess1["items"])
    categories = Category.objects.filter(active=True)
    context = {"products": products,
               "categories": categories,
               "title": "My Cart"}
    return render(req, "eco/list.html", context)


def checkout(req):
    req.session.pop('data', None)
    return redirect("/")


@api_view(['GET'])
def api_products(req):
    query = req.GET.get("q", "")
    products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
