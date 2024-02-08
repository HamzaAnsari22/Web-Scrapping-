import json
import urllib

import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup


from .forms import updateForm
from .models import sku_modal as sku_modal_db
from .models import sku_setting as sku_setting_db


def login(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            messages.success(request, f'Login Successfully {username}')
            return redirect('view_setting')
        else:
            form = UserCreationForm()
        return render(request, "login/login.html", {"form": form})


@login_required
def sku_modal(request):
    return render(request, "login/sku_modal.html")


@csrf_exempt
def sku_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        country = request.POST['country']
        dali_ref = request.POST['dali_ref']
        sku_id = request.POST.get('sku_id')
        sku_url = request.POST.get('sku_url')
        catalog = request.POST.get('catalog')
        title = request.POST.get('title')
        platform = request.POST.get('platform')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        unit_cost = request.POST.get('unit_cost')
        note = request.POST.get('note')

        try:
            print("enter")
            sku = sku_modal_db(country=country, dali_ref=dali_ref, sku_id=sku_id, sku_url=sku_url,
                               catalog=catalog, title=title, percent=platform, min_price=min_price,
                               max_price=max_price, unit_cost=unit_cost, note=note)
            print(sku)
            sku.save()
            # messages.success(request, "Successfully Added Session")
            print("save")
            return HttpResponseRedirect(reverse("sku_modal"))

        except:
            messages.error(request, "Failed to Add Session")
            print("no")
            return HttpResponseRedirect(reverse("sku_modal"))



@login_required
def sku_setting(request):
    return render(request, "login/sku_setting.html")


@csrf_exempt
def sku_setting_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        timer = request.POST.get('timer')
        uae_box = request.POST.get('uae_box')
        uae_box_price = request.POST.get('uae_box_price')
        ksa_box = request.POST.get('ksa_box')
        ksa_box_price = request.POST.get('ksa_box_price')

        try:
            print("enter")
            sku_set = sku_setting_db(timer=timer, uae_box=uae_box, uae_box_price=uae_box_price, ksa_box=ksa_box,
                               ksa_box_price=ksa_box_price)

            print(sku_set)
            sku_set.save()
            # messages.success(request, "Successfully Added Session")
            print("save")
            return HttpResponseRedirect(reverse("sku_modal"))

        except:
            messages.error(request, "Failed to Add Session")
            print("no")
            return HttpResponseRedirect(reverse("sku_modal"))

@login_required
def logout(request):
    return render(request, "login/login.html")


def view_sku(request):
    queryset = sku_modal_db.objects.all()
    return render(request, "login/view_sku.html", {"Sku_View": list(queryset.values())})


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        queryset = sku_modal_db.objects.filter(country=keyword)
        print(queryset, "keyword")
    else:
        queryset = sku_modal_db.objects.all()
    return render(request, "login/view_sku.html", {"Sku_View": list(queryset.values())})

@csrf_exempt
def view_sku_country(request):
    country = request.POST.get('country')
    print(country)
    queryset = sku_modal_db.objects.filter(country=country)
    print(queryset)
    return JsonResponse({"Sku_Country": list(queryset.values())})


def delete_data(request, id):
    if request.method == 'POST':
        pi = sku_modal_db.objects.get(id=id)
        pi.delete()
        queryset = sku_modal_db.objects.all()
        return render(request, "login/view_sku.html", {"Sku_View": list(queryset.values())})


@csrf_exempt
def update_data(request, id):
    if request.method == 'POST':
        pi = sku_modal_db.objects.get(pk=id)
        print(pi)
        fm = updateForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
        else:
            pi = sku_modal_db.objects.get(pk=id)
            print(pi)
            fm = updateForm(instance=pi)

    return render(request, 'login/update_data.html', {'form': fm})


def view_sku_ajax(request):
    queryset = sku_modal_db.objects.all()
    return JsonResponse({"Sku_View": list(queryset.values())})


def view_setting(request):
    return render(request, "login/view_setting.html")


def view_setting_ajax(request):
    list1 = []
    sku_list = []

    data = []
    percent = []
    unit_cost = []
    qs1 = sku_modal_db.objects.all()
    qs = sku_setting_db.objects.all()
    for q in qs:
        uae_buybox_seller = q.uae_box
        uae_buybox_price = q.uae_box_price
        ksa_buybox_seller = q.ksa_box
        ksa_buybox_price = q.ksa_box_price
        list1.append([uae_buybox_seller, uae_buybox_price])

    for q1 in qs1:
        sku_list.append([q1.sku_url,q1.country])
        percent.append(q1.percent)
        unit_cost.append(q1.unit_cost)
        data.append([q1.sku_id, q1.sku_url, q1.title, q1.catalog, q1.percent])

    c_list = []
    seller = []

    for i in range(len(sku_list)):
        c = i+1
        c_list.append([c, data[i], list1[i]])

    # print(c_list,)

    # print( uae_buybox_seller, uae_buybox_price)
    # links = queryset.values('uae_box')
    # print(sku_list[3])
    ##################################################

    #
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

    # buy_box_price_string = "priceNow"
    # buy_box_seller_string = "storeLink"
    price = []

    for p,u in sku_list:
        field = ''
        seller=''
        req = requests.get(u, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find(id="__next")
        if sku_list[p][1]=='uae':
            field = uae_buybox_price
        else:
            field = ksa_buybox_price
        r = results.find_all("div", class_=field)

        for r1 in r:
            a = r1.text.replace("AED", "")
            a = a.replace("(Inclusive of VAT)", "")
            a = a.replace("Inclusive of VAT", "")
            a = a.replace(" ", "")

            print(type(a))
            b = float(a)
            price.append(b)
            # print(b)
        if sku_list[p][1]=='uae':
            seller = uae_buybox_seller
        else:
            seller = ksa_buybox_seller
        r2 = results.find_all("button", class_=uae_buybox_seller)
        for r1 in r2:
            print(r1.text)
            seller.append(r1.text)
    roi = []
    roi_per = []
    price_list = []
    for i in range(len(percent)):
        print(price[i], float(percent[i]), float(unit_cost[i]))
        a = price[i] - (price[i] * float(percent[i])) - float(unit_cost[i])
        roi_p = a / float(unit_cost[i])
        # print(roi_p, "roi percentage", a, "roi")
        # print("percent", float(percent[i]))
        price_list.append(price[i])
        roi_per.append(roi_p)
        roi.append(a)
    for i in range(len(c_list)):
        c_list[i].append([seller[i], price_list[i], roi[i], roi_per[i]])

    # print(c_list)
# ################################################################
#     print(queryset.only('uae_box'))
    return JsonResponse({"Sku_Setting": c_list})
