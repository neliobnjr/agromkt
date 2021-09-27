import os
from time import sleep
import json

def update():
    os.system('git add --all')
    sleep(1)
    os.system('git commit -m "test"')
    sleep(1)
    os.system('git push')
    sleep(1)
    os.system('git fetch')
    sleep(1)

##readlines html to cut from line 52 to n(should read which line is equal/contains "'<!--END CUT HERE-->\n'" to find the index then cut everything else).
def createElement():
    with open('../products/config/config2.json', 'r') as f:
            data = json.load(f)
            data = data['features']

            elements = []
            try:
                for i in data:
                    productName = i['product']
                    prodZap = productName.replace(' ', '%20')
                    
                    photo = i['photo_location1']
                    photo2= i['photo_location2']
                    photo3= i['photo_location3']
                    vendPhone = i['vendedor_phone']
                    zapLink = f"https://api.whatsapp.com/send?phone={vendPhone}&text=Ol%C3%A1!%20Gostaria%20de%20saber%20mais%20informa%C3%A7%C3%B5es%20sobre%20o%20produto%20{prodZap}%20que%20vi%20no%20oferta%20agr%C3%ADcola"
                    productDesc = i['vendedor_nome']
                    prodId= i['ID']
                    elementProd =+ 1
                    prodElement = f"""<div class="content">
                            <!--<img src="products/vagaoipacol.08.08.jpeg">-->
                            <!--Carousel Starts here -->
                            <div id="{prodId}" class="carousel slide" data-ride="carousel">
                                        <div class="carousel-inner" role="listbox">
                                            <div class="carousel-item active">
                                                <img class="d-block img-fluid" src="{photo}">
                                            </div>
                                                <div class="carousel-item">
                                                    <img class="d-block img-fluid" src="{photo2}">
                                                </div>
                                                <div class="carousel-item">
                                                    <img class="d-block img-fluid" src="{photo3}">
                                                    </div>
                                                </div>
                                    <a class="carousel-control-prev" href="#{prodId}" role="button" data-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="false"></span>
                                        <span class="sr-only" style='background-color: black' >Previous</span>
                                    </a>
                                        <a class="carousel-control-next" href="#{prodId}" role="button" data-slide="next">
                                        <span class="carousel-control-next-icon"  aria-hidden="true"></span>
                                        <span class="sr-only" style='background-color: black' >Next</span>
                                    </a>
                                    </div>
                            <!---Carousel Ends here-->
                            <h3>{productName}</h3>
                            <p>{productDesc}</p>
                            <h6>Condições Especiais</h6>
                            <ul>
                            <li><i class="fa fa-star" aria-hidden="true"></i></li>
                            <li><i class="fa fa-star" aria-hidden="true"></i></li>
                            <li><i class="fa fa-star" aria-hidden="true"></i></li>
                            <li><i class="fa fa-star" aria-hidden="true"></i></li>
                            <li><i class="fa fa-star" aria-hidden="true"></i></li>
                            </ul>
                            <button class="buy-1" onclick="location.href='{zapLink}';">COMPRE JÁ! <i class="fa fa-whatsapp" aria-hidden='true'></i></button>
                        </div>"""

                    elements.append(prodElement)
                return elements
            except:
                pass
                return elements

def addElement(elements):
    with open('../pages/baseline.html', 'r', encoding='utf-8') as g:
        htmlines = g.readlines()

        for i in elements:
            pos =+ 1
            htmlines.insert((52+pos), i)

        with open('../index.html','w', encoding='utf-8') as c:
            for i in htmlines:
                line = str(i)
                c.write(line)
def run():
    el = createElement()
    addElement(el)
    sleep(1)
    update()

run()