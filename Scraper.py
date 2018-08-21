from bs4 import BeautifulSoup
import requests
import re
import csv

# selecione o dia
page = requests.get("https://www.theguardian.com/theguardian/2018/aug/18")
c = page.content

# fazer uma sopa pa nois
soup = BeautifulSoup(c, features="html.parser")

# inicializando lista de urls
urls = []

# populandi
for url in soup.find_all(href=re.compile("https(.*)aug")):
    urls.append(url.get('href'))

# dedupe
newUrls = list(set(urls))

# inicializando tabela
study = [['Link', 'Data', 'Título', 'Autor', 'Seção', 'Enquadramento', 'Recursos', 'Patrocínio']]

# lacim de fita
for url in newUrls:

    # url
    iteratorURL = url

    # data
    iteratorDate = "18/08/2018"  # mude a data, filho da puta sem costume

    # bora
    iteratorPage = requests.get(url)
    iteratorContent = iteratorPage.content
    iteratorSoup = BeautifulSoup(iteratorContent, features='html.parser')

    # título
    if len(iteratorSoup.find_all(itemprop="headline")) != 0:
        iteratorTitle = iteratorSoup.find_all(itemprop="headline")[0].text
        iteratorTitle = iteratorTitle.replace("\n", "")
    else:
        iteratorTitle = iteratorSoup.find_all(articleprop="headline")[0].text
        iteratorTitle = iteratorTitle.replace("\n", "")

    # autor(es)
    if len(iteratorSoup.find_all(itemprop="name")) == 3:
        iteratorAuthor = iteratorSoup.find_all(itemprop="name")[1].contents[0] + " and " + \
                         iteratorSoup.find_all(itemprop="name")[2].contents[0]
        iteratorAuthor = iteratorAuthor.replace("\n", "")
    elif len(iteratorSoup.find_all(itemprop="name")) == 4:
        iteratorAuthor = iteratorSoup.find_all(itemprop="name")[1].contents[0] + ", " + \
                         iteratorSoup.find_all(itemprop="name")[2].contents[0] + " and " + \
                         iteratorSoup.find_all(itemprop="name")[3].contents[0]
        iteratorAuthor = iteratorAuthor.replace("\n", "")
    elif len(iteratorSoup.find_all(itemprop="name")) == 5:
        iteratorAuthor = iteratorSoup.find_all(itemprop="name")[1].contents[0] + ", " + \
                         iteratorSoup.find_all(itemprop="name")[2].contents[0] + ", " + \
                         iteratorSoup.find_all(itemprop="name")[3].contents[0] + " and " + \
                         iteratorSoup.find_all(itemprop="name")[4].contents[0]
        iteratorAuthor = iteratorAuthor.replace("\n", "")
    elif len(iteratorSoup.find_all(itemprop="name")) == 2:
        iteratorAuthor = iteratorSoup.find_all(itemprop="name")[1].contents[0]
        iteratorAuthor = iteratorAuthor.replace("\n", "")
    else:
        iteratorAuthor = iteratorSoup.find_all("p", class_="byline")[0].text

    # seção
    if len(iteratorSoup.find_all("a", class_="subnav-link")) != 0:
        iteratorSection = iteratorSoup.find_all("a", class_="subnav-link")[0].contents[0]
        iteratorSection = iteratorSection.replace("\n", "")
        if iteratorSection == "Money" or iteratorSection == "Business":
            iteratorSection = "Economia"
        elif iteratorSection == "Books" or iteratorSection == "Fashion" or iteratorSection == "Film" or iteratorSection == "Art & Design":
            iteratorSection = "Cultura"
        elif iteratorSection == "Education":
            iteratorSection = "Educação"
        elif iteratorSection == "Politics" or iteratorSection == "US politics":
            iteratorSection = "Política"
        elif iteratorSection == "Health":
            iteratorSection = "Saúde"
        elif iteratorSection == "Environment":
            iteratorSection = "Meio Ambiente"
        elif iteratorSection == "World":
            iteratorSection = "Mundo"
        else:
            iteratorSection = "CHECAR"
    else:
        iteratorSection = url.split('/')[3]
        if iteratorSection == "money" or "business":
            iteratorSection = "Economia"
        elif iteratorSection == "books" or iteratorSection == "fashion" or iteratorSection == "film" or iteratorSection == "artanddesign":
            iteratorSection = "Cultura"
        elif iteratorSection == "education":
            iteratorSection = "Educação"
        elif iteratorSection == "health":
            iteratorSection = "Saúde"
        elif iteratorSection == "environment":
            iteratorSection = "Meio Ambiente"
        elif iteratorSection == "world":
            iteratorSection = "Mundo"
        elif iteratorSection == "politics":
            iteratorSection = "Política"
        else:
            iteratorSection = "CHECAR"

    # enquadramento
    if not iteratorSoup.find_all("div", class_="content__label-interview"):
        if len(iteratorSoup.find_all("a", class_="content__label__link")) > 0:
            enquadra = str(iteratorSoup.find_all("a", class_="content__label__link")[0].contents)
            if 'Opinion' in enquadra:
                iteratorEnquadramento = "Opinião"
            elif 'Observer' in enquadra:
                iteratorEnquadramento = "Reportagem"
            elif 'Nils Pratley' in enquadra:
                iteratorEnquadramento = "Opinião"
            else:
                iteratorEnquadramento = "Notícia"
        else:
            iteratorEnquadramento = "Notícia"
    else:
        iteratorEnquadramento = "Entrevista"

    # recurso
    iteratorRecurso = "Imagem"
    if 'href' in str(iteratorSoup.find("div", class_="content__article-body")):
        iteratorRecurso += " / Hiperlink"
    if (0 != len(iteratorSoup.find_all("div", class_="html5-video-player"))) or (len(iteratorSoup.find_all("figure", class_="element-video")) != 0):
        iteratorRecurso += " / Vídeo"
    if len(iteratorSoup.find_all("div", class_="graph")) != 0:
        iteratorRecurso += " / Gráfico"
    if len(iteratorSoup.find_all("div", class_="atom--snippet__body")) != 0:
        iteratorRecurso += " / Guide"

    # patrocinio
    x = iteratorSoup.find_all("a", class_="badge__link")
    iteratorPatrocinio = ''
    for elem in x:
        iteratorPatrocinio = elem('img')[0]['alt']

    # build the wall
    study.append(
        [url, iteratorDate, iteratorTitle, iteratorAuthor, iteratorSection, iteratorEnquadramento, iteratorRecurso,
         iteratorPatrocinio])

# log the wall
with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(study)
