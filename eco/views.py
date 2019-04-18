from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from eco.forms import ReviewForm, SigninForm, SignupForm, FeedbackForm, ProductForm, CategoryForm
from eco.models import Product, Category

from eco.serializer import ProductSerializer


def AtitAdmin(req):
    if req.method == "POST":
        form = SigninForm(req.POST)
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, "Successfully logged in")
            return render(req, "eco/AtitAdmin.html")
        else:
            messages.error(req, "Invalid Username or Password")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(req, "eco/signinAdmin.html", context)


def category(req):
    return render(req, "eco/category.html")


def product(req):
    return render(req, "eco/product.html")


def about(req):
    return render(req, "eco/about.html")


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


def googlemap(req):
    return render(req, "eco/map.html", {})


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
    return render(req, "eco/profile.html")


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


def feedback(req):
    if req.method == "POST":
        form = FeedbackForm(req.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = req.user
            feedback.save()
            messages.success(req, "Feedback saved")
        else:
            messages.error(req, "Invalid form")
    else:
        form = FeedbackForm()
    context = {'form': form}
    return render(req, "eco/feedback.html", context)


def category_create_view(req):
    form = CategoryForm(req.POST or None)
    if form.is_valid():
        form.save()
        return redirect('eco:home')
    context = {'form': form}
    return render(req, "eco/category_create.html", context)


def category_update_view(req,slug):
    category = Category.objects.get(slug=slug)
    form = CategoryForm(req.POST or None,instance=category)
    if form.is_valid():
        form.save()
    context = {'category': category, 'form': form}
    return render(req, "eco/category_update.html", context)


def category_delete_view(req,slug):
    category = Category.objects.get(slug=slug)
    if req.method == 'POST':
        category.delete()
        return redirect('eco:category_list_delete')

    return render(req, "eco/product_delete.html", {'category': category})

def category_list_update(req):
    category=Category.objects.all()
    return render(req,"eco/category_list_update.html",{'category':category})

def category_list_delete(req):
    category = Category.objects.all()
    return render(req,"eco/category_list_delete.html",{'category':category})


def product_create_view(req):
    form = ProductForm(req.POST or None)
    if form.is_valid():
        form.save()
        return redirect("eco:home")
    context = {'form': form}
    return render(req, "eco/product_create.html", context)


def product_delete_view(req,slug):
    products = Product.objects.get(slug=slug)
    if req.method=='POST':
        products.delete()
        return redirect('eco:product_list_delete')

    return render(req, "eco/product_delete.html",{'products':products})


def product_update_view(req,slug):
    products = Product.objects.get(slug=slug)
    form = ProductForm(req.POST or None,instance=products)
    if form.is_valid():
        form.save()
    context = {'products': products, 'form': form}
    return render(req, "eco/product_update.html", context)


def product_list_update(req):
    products=Product.objects.all()
    return render(req,"eco/product_list_update.html",{'products':products})

def product_list_delete(req):
    products = Product.objects.all()
    return render(req,"eco/product_list_delete.html",{'products':products})

@api_view(['GET'])
def api_products(req):
    query = req.GET.get("q", "")
    products = Product.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
