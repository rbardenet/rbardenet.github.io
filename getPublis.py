import urllib.request

page = urllib.request.urlopen("http://haltools.archives-ouvertes.fr/Public/afficheRequetePubli.php?auteur_exp=rbardenet&CB_auteur=oui&CB_titre=oui&CB_article=non&CB_Resume_court=non&CB_typdoc=oui&CB_vignette=non&langue=Anglais&tri_exp=annee_publi&tri_exp2=typdoc&tri_exp3=date_publi&&ordre_aff=TA&Fen=Aff&css=../css/VisuCondenseSsCadre.css")
page = page.readlines()

with open("publis.html",'wb') as fout:
    for line in page:
        strLine = line.decode()

        # give the right address to css files
        if "../css" in strLine:
            strLine = strLine.replace("../css", "css")

        # Erase abstract
        queryStart = "<dt class=\"ChampRes\">Resume_court</dt>"
        queryStop = "</dd>"
        tic = strLine.find(queryStart)
        toc = strLine.find(queryStop)
        abstract = strLine[tic:toc+len(queryStop)]
        strLine = strLine.replace(abstract, '')

        # make my name bold
        for query in ["R. Bardenet", "Rémi Bardenet"]:
            tic = strLine.find(query)
            toc = tic + len(query)
            name = strLine[tic:toc]
            if not tic == -1:
                strLine = strLine.replace(name, "<b>"+name+"</b>")

        # Erase document type
        queryStart = "<dt class=\"ChampRes\">typdoc</dt>"
        queryStop = "</dd>"
        tic = strLine.find(queryStart)
        toc = strLine.find(queryStop)
        abstract = strLine[tic:toc+len(queryStop)]
        strLine = strLine.replace(abstract, '')

        # find Auger author lists and shorten them
        queryStart = "class=\"ValeurRes Auteurs\">"
        queryStop = "</dd>\n<dt class=\"ChampRes\">article"
        tic = strLine.find(queryStart)
        queryLength = len(queryStart)
        if not tic == -1:
            # We've found a list of authors
            toc = strLine[tic:].find(queryStop)
            authorList = strLine[tic+queryLength:toc]
            length = len(authorList)
            checkStr = "P. Abreu"
            if length > 200 and checkStr in authorList:
                strLine = strLine.replace(authorList, "The Full Pierre Auger collaboration</dd>")
                
        fout.write(strLine.encode())
