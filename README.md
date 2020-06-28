# Joble
This Platform  Search Thousands Of Job Boards In Different Technologies From Over The World .


## Installation

step 1 : Create clone of Joble.
```
git clone https://github.com/chavarera/Joble.git
```
step 2 : Change working directory to Joble
```
cd Joble
```
step 3 : Create Virtual environment
```
virtualenv -p python3 vnev
```

setp 4 : Activate Virtual environment
```
source vnev/bin/activate
```

step 5 : Install required packages
```
pip install -r requirements.txt
```

step 6 : Now Exceute Spiders



## List of Spiders Available
1. Naukri
2. MonsterIndia


### 1. Naukri
Get 20 Jobs per catgory
```
scrapy crawl Naukri
```

Available Option
1. city
2. count
3. keyword

For Example
```
scrapy crawl Naukri -a  keyword=python -a count=20 -a city=pune

```

Export Output in csv,json
```
scrapy crawl Naukri -a  keyword=python -o python.csv

```

### 2. MonsterIndia
Available Option
1. city
2. count
3. keyword

For Example
```
scrapy crawl MonsterIndia -a  keyword=python -a
```