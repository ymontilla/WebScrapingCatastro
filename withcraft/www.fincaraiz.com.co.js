var getNextImage = function(){
    b = document.getElementById("bigPhoto")
    c = document.getElementById("ctl00_phMasterPage_cAdvert_ucMultimedias_photoArrowRight")
    c.click()
    return b.src;
}

var hasImages = function(){
    var a = document.getElementById("dynamicContent")
    return a.style.display == "none"
}

var iterateImages = function(){
    self = this
    while(hasImages()){
        self.push(getNextImage())
        setTimeout(function(){
            return iterateImages.call(self)
        }, 500)
    }
    return self.join(";")
}

var getPaginationLinks = function(){
    var a = document.getElementById("divPaginator")

    if(a){
        var i;
        for(i = 0; i < a.childElementCount; i++){
            if(a.children[i].text.match(".*Siguiente") != null){
                var nextPageId = 2
                if(a.children[i].id != "") nextPageId = a.children[i].id.replace("lnkPage", "")
                return {
                    "nextPageElement": a.children[i],
                    "nextPageId": nextPageId - 1
                }
          }
        }
    }

    return null;
}

var getAdvertsLinks = function(){
    var divAdverts = document.getElementById("divAdverts")
    var entries = divAdverts.getElementsByTagName("ul")
    var links = [], i = 0;
    for(; i < entries.length; i++){
        var rawLinks = entries[i].getElementsByTagName("li"), j = 0
        for(; j < rawLinks.length; j++){
            if(rawLinks[j].getAttribute("class") == "title-grid"){
                var linkElement = rawLinks[j].getElementsByTagName("a")
                console.assert(linkElement.length == 1, "There should be only an 'a' element")
                links.push(linkElement[0])
            } 
        }
    }
    return links
}



var downloadAllPublicationsInCurrentPage = function(success){
    document.getElementById("divPaginator").scrollIntoView()
    var endPosition = window.scrollY
    window.scroll(0,0)
     
    var scrollToNext = function(links, elementPosition){
        if(!links[elementPosition]) return -1
        links[elementPosition].scrollIntoView()
        return ++elementPosition
    }
     
    var delayedScroll = function(elementPosition){
        var links = getAdvertsLinks() 
        if(window.scrollY + window.innerHeight < endPosition){
            var nextPosition = scrollToNext(links, elementPosition)
            setTimeout(function(){
               delayedScroll(nextPosition)
            }, 1000)
        }else{
            success(links)
        }
    }
     
    return delayedScroll(0)
}

var filterItems = function(list, condition){
    var i = 0, filtered = []
    for(; i< list.length; i++){
        if(condition(list[i])) filtered.push(list[i])
    }
    return filtered
}

var getPublicationLatLon = function(){
    var scripts = document.getElementsByTagName("body")[0].getElementsByTagName("script")
     
    var leafLetInit = filterItems(scripts, function(e){
        if(e.text){
           if(e.text.match(/var extrasId =/) != null){
               return true
           }else{
               return false
           }
       } else {
          return false
       }
    });

    console.assert(leafLetInit.length == 1, "There should be jist one intiatlization script")
    
    var definitions = leafLetInit[0].text.match(/MapFR\..+ = parseFloat.+/g)
    var lat = definitions[0].match(/MapFR\.(.+) = parseFloat\('(.+)'\)/)
    var lon = definitions[1].match(/MapFR\.(.+) = parseFloat\('(.+)'\)/)

    return "lat:" + lat[2] + "," + "lon:" + lon[2]
}


var getPublicationValue = function(key, executor){
    if(key === "function") {
        return executor.call()
    } else if(key === "text") {
        return executor
    }

    console.assert(true, "This value is not being handled")
}


var getTagNameWithClass = function(tagName, className){
    var tags = document.getElementsByTagName(tagName), i = 0
    for(; i < tags.length; i++){
        if(tags[i].className === className) return tags[i].innerText.replace("\n", "")
    }
    return null
}

var getByIdAndTagName = function(id, tagName){
    var tags = document.getElementById(id).getElementsByTagName(tagName)
//    console.assert(tags.length != 1, "There should be only an element")
    return tags[0].innerText.replace("\n", "")
}


var getByIdAndTagNameWithoutClass = function(id, tagName, className){
    var tags = document.getElementById(id).getElementsByTagName(tagName), i = 0
//    console.assert(tags.length != 1, "There should be only an 'a' element")
    for(; i < tags.length; i++){
        if(tags[i].className !== className) return tags[i].innerText.replace("\n", "")
    }
    return null
}

var getByIdAndTagNameWithoutAnyClass = function(id, tagName){
    var tags = document.getElementById(id).getElementsByTagName(tagName), i = 0
//    console.assert(tags.length != 1, "There should be only an 'a' element")
    for(; i < tags.length; i++){
        if(tags[i].className === "") return tags[i].innerText.split("\n").join(" ")
    }
    return null
}

var getByIdAndTagNameAndTagName = function(id, outer, inner, className){
    var outerTag = document.getElementById(id).getElementsByTagName(outer)
    var innerTag = outerTag[0].getElementsByTagName(inner), i = 0
    return innerTag[0].innerText.replace("\n", "")
}  

// #AdvertDetail > div.centerPage > div.row.features_2 > ul
var newMappings = {
    "surface": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertSurface")}},
    "rooms": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertRooms")}},
    "baths": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertBaths")}},
    "garages": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertGarages")}},
    "price": {"type": "function", "value": function(){return getByIdAndTagNameWithoutAnyClass("aspnetForm", "h2")}},
    "location": {"type": "function", "value":function(){return document.getElementById("divAdressBuilder").innerText.replace("\n", "")}},
    "description": {"type": "function", "value":function(){return getByIdAndTagNameWithoutClass("AdvertDetail", "p", "title")}},
    "coordinates": {"type": "function", "value":getPublicationLatLon},
    "used": {
        "type": "function",
        "value":function(){
            var element = document.getElementById("ctl00_phMasterPage_cAdvert_ucMultimedias_icoNewBuilding");
            return element ? element.innerText.replace("\n", "") : null
        }
    },
    "url": {"type": "text", "value": window.location.href},
    "additional_info": {"type": "function", "value": function(){return getByIdAndTagName("AdvertDetail", "ul")}},
    "nature": {"type": "text", "value": "selling-house"},
    "images": {"type": "function", "value": iterateImages.bind([])}
}

var usedMappings = {
    "surface": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertSurface")}},
    "rooms": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertRooms")}},
    "baths": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertBaths")}},
    "garages": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertGarages")}},
    "price": {"type": "function", "value": function(){return getByIdAndTagName("aspnetForm", "h2")}},
    "location": {"type": "function", "value":function(){return getByIdAndTagNameAndTagName("aspnetForm", "h1", "span")}},
    "description": {"type": "function", "value":function(){return getByIdAndTagNameWithoutClass("AdvertDetail", "p", "title")}},
    "coordinates": {"type": "function", "value":getPublicationLatLon},
    "used": {
        "type": "function",
        "value":function(){
            var element = document.getElementById("ctl00_phMasterPage_cAdvert_ucMultimedias_icoUsed");
            return element ? element.innerText.replace("\n", "") : null
        }
    },
    "url": {"type": "text", "value": window.location.href},
    "additional_info": {"type": "function", "value": function(){return getByIdAndTagName("AdvertDetail", "ul")}},
    "nature": {"type": "text", "value": "selling-house"},
    "images": {"type": "function", "value": iterateImages.bind([])}
}

var rentMappings = {
    "surface": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertSurface")}},
    "rooms": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertRooms")}},
    "baths": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertBaths")}},
    "garages": {"type": "function", "value": function(){return getTagNameWithClass("span", "advertGarages")}},
    "price": {"type": "function", "value": function(){return getByIdAndTagName("aspnetForm", "h2")}},
    "location": {"type": "function", "value":function(){return getByIdAndTagNameAndTagName("aspnetForm", "h1", "span")}},
    "description": {"type": "function", "value":function(){return getByIdAndTagNameWithoutClass("AdvertDetail", "p", "title")}},
    "coordinates": {"type": "function", "value":getPublicationLatLon},
    "url": {"type": "text", "value": window.location.href},
    "additional_info": {"type": "function", "value": function(){return getByIdAndTagName("AdvertDetail", "ul")}},
    "nature": {"type": "text", "value": "renting-house"},
    "images": {"type": "function", "value": iterateImages.bind([])}
}

var isUsed = function(){
    var used = usedMappings["used"].value()
    if(used)
        return true
    used = newMappings["used"].value()
    if(used)
        return false
    return null
}

// from https://stackoverflow.com/questions/7717851/save-file-javascript-with-file-name
function saveAs(filename, uri) {
    var link = document.createElement("a")
    document.body.appendChild(link)
    link.href = uri
    link.download = filename
    link.click()
    document.body.removeChild(link)
}

var saveStringToFile = function(name, text){
    var uri = "data:text/csv;charset=utf-8," + escape(text);
    saveAs(name, uri)
}

var savePublicationHeaders = function(name, csvMappings){
    var keys = Object.keys(csvMappings)
    saveStringToFile(name, keys.join("|"))
}

var publicationToCSV = function(csvMappings){
    var keys = Object.keys(csvMappings)
    var values = keys.map(function(k){
        return getPublicationValue(csvMappings[k]["type"], csvMappings[k]["value"])
    })

    var i = 0, name = "download" + Math.random()
    for(; i < keys.length; i++)
        if(keys[i] === "url")
            name = values[i]

    //savePublicationHeaders(name + "___keys", usedMappings)
    saveStringToFile(name, values.join("|"))
}

var saveCurrentPagePublicationToFile = function(csvMappings){
    publicationToCSV(csvMappings)
    console.log("Indibvidual publication")
}

var delayedNewPage = function(link){
    return function(){
        window.open(link);
    }
}

var traverseCurrenPageLinks = function(links){
    var i = 0, linksText = links.map(function(e){return e.href});
    for(; i < linksText.length; i++){
        setTimeout(delayedNewPage(linksText[i]), 4000*i)
    }
}

var dowloandLinksPage = function(contador){
    //Obtener las urls de los tags 'a'
    var getLinksTags = getAdvertsLinks().map(paginas =>paginas.href);

    //En un Array se guarda un string separado por un salto de linea
    var linksSeparados = getLinksTags.join('\n');

    //conversion a CSV
    saveStringToFile(contador + ".csv",linksSeparados);
}

var traverseResultPages = function(pagination){
    if(pagination == null){
        dowloandLinksPage("last")
        return null;
    }
        
    dowloandLinksPage(pagination.nextPageId)
    pagination.nextPageElement.click()
    
    setTimeout(() => {
        traverseResultPages(getPaginationLinks())
    }, 5000);
}

window.addEventListener('load', function () {
    var pathElements = window.location.pathname.split("/")
    var searchCity = pathElements[pathElements.length - 2] 
    if(window.location.pathname.match(/\/apartamentos\/venta\/.+/) ||
       window.location.pathname.match(/\/apartamentos\/arriendo\/.+/) ||
       window.location.pathname.match(/\/casas\/venta\/.+/) || 
       window.location.pathname.match(/\/casas\/arriendo\/.+/)){
        traverseResultPages(getPaginationLinks())
        console.log("Traversing")
    } else if(window.location.pathname.match(/\/.+en-venta/)) {
        var used = isUsed()
        if(used == null || !used)
            return
        saveCurrentPagePublicationToFile(usedMappings)
        setTimeout(function(){
           window.close()
        }, 2000)
    } else if(window.location.pathname.match(/\/.+\/proyecto-nuevo/)) {
        /*
        var used = isUsed()
        if(used == null || used)
            return
        saveCurrentPagePublicationToFile(newMappings)
        */
        setTimeout(function(){
           window.close()
        }, 2000)
    } else if(window.location.pathname.match(/\/.+en-arriendo/)) {
        saveCurrentPagePublicationToFile(rentMappings)
        setTimeout(function(){
           window.close()
        }, 2000)
    } else {
        setTimeout(function(){
           window.close()
        }, 2000)
    }
});
