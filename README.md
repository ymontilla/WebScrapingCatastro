# WebScrapingCatastro

## Descargar fuentes

> git clone https://github.com/ymontilla/WebScrapingCatastro.git

> cd web-scrapping && checkout sebastian

Es necesario crear el archivo .env en la raiz de proyecto, el archivo debe contener el token para poder consumir las APIs de google maps.

> echo "GOOGLE_MAPS_KEY=AIzaSyD3ezHPMru97j8AR33OQEn5jsOqGR3SvKI" >> web-scrapping/.env


## Configurar python

> sudo apt-get install python3 python3-pip

> sudo pip3 install dvc


## Configurar nodejs

> sudo apt-get update && sudo apt-get install -y curl procps 

> curl -sL https://deb.nodesource.com/setup_13.x |  sudo bash -

> sudo apt-get update && sudo apt-get install -y nodejs

Instalar chrome remote interface

> sudo  npm -g install chrome-remote-interface




## Install Chromium

> sudo apt-get install chromium

## Iniciar chromium

> chromium --remote-debugging-port=9222


## Configurar extensiones de chrome

- https://luciopaiva.com/witchcraft/how-to-install.html
 - https://github.com/luciopaiva/witchcraft
 - https://github.com/kzahel/web-server-chrome


## Scrapping

### Recorrer páginas

Unir los resultados de todas la páginas

> rm -f links.csv

> find -not -name "links.csv" -type f -exec cat {} \; >> links.csv

> find -not -name "links.csv" -type f -exec rm {} \; >> links.csv


### Descarga publicaciones

<!-- #region -->
> export NODE_PATH=/usr/lib/node_modules:$NODE_PATH

> sudo apt-get install parallel

> cat ~/sources/web-scraping/links/casas/manizales-venta/links.csv  | parallel --gnu -j 10 --workdir "$PWD" '
> nodejs ~/sources/web-scraping/chromium/screenshot.js "{}"
> '

> echo "surface|rooms|baths|garages|price|location|description|coordinates|used|url|additional_info|nature|pictures" > apartments.csv
> find . -type f -not -name "apartments.csv" -exec perl ~/sources/web-scraping/withcraft/format_result.pl {} \; >> apartments.csv


Verifica los resultados:

> cat apartments.csv | perl -F\\\| -lane 'print $#F' | sort | uniq
<!-- #endregion -->

### Versionar datos

> find . -type f -not -name "*.dvc" -not -name "https___www.fincaraiz.com.co*" -not -name "*.ipynb" -not -name "*.pyc" -not -name "*.py" -not -name "*.Rmd" -not -name "*.js" -not -name "*.pl" -not -name "*.md" -not -name "*.sh" -not -name "*.conf" -not -name "Dockerfile" -not -name "LICENSE" -not -name "README" -not -path '*/\.*' -not -path '*mintic*'  | xargs dvc add

> git add -A .

```python

```
