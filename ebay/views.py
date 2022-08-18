from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import *



def index(request):

    Product.objects.all().delete()

    url = ''
    if request.method == 'POST':
        search = request.POST['search']

        if 'http' in search:
            url = search
        else:
            search = search.replace(' ','+')
            url='https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw='+search+'&_sacat=0'
        
        webpage = requests.get(url)        
        soup = BeautifulSoup(webpage.text,'lxml')
        
        title = soup.find_all('h3', {'class':'s-item__title'})
        pricebox = soup.findAll('span',{'class':'s-item__price'})
        ship = soup.find_all('span',class_='s-item__shipping s-item__logisticsCost')
        link = soup.find_all('div',class_='s-item__image')
    
        # pl = [p.text for p in pricebox]

        tloop = [p.text for p in title]
        sloop = [s.text for s in ship]
        lloop = [l.a['href'] for l in link]
        ploop = []
        
        for p in pricebox:
            if '$' in p.text:
                ploop.append(p.text)
             
        lloop.pop(0)
        tloop.pop(0)
        ploop.pop(0)
        
        for t in range(20):
            Product.objects.create(id=(t+1),title=tloop[t], price=ploop[t], shipfee = sloop[t],link=lloop[t])

    product = Product.objects.all()
    
    return render(request,'ebay/index.html',{'product':product})


def detail(request, id):
    detail = Detail.objects.all().delete()

    product = Product.objects.get(id=id)
    
    webpage = requests.get(product.link)
    soup = BeautifulSoup(webpage.text,'lxml')

    check = soup.find('span',class_='msgTextAlign').text

    if not check:
        seller = soup.find('div',class_='ux-seller-section__item--seller')
        itemlocation = soup.find('span',class_='ux-textspans ux-textspans--BOLD ux-textspans--SECONDARY').text
        feedback = soup.find_all('span',{'class':'ux-textspans'})
        floop = ''
        for f in feedback:
            if 'feedback' in f.text:
                floop = f.text

        Detail.objects.create(product=product,sellerlink=seller.a.get('href'),sellername=seller.span.text,itemlocation=itemlocation,
        feedback=floop)
    detail = Detail.objects.all()
    return render(request,'ebay/detail.html',{'detail':detail})