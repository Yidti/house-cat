# House Cat

House Cat is a Python Crawler which collect house information from House for Sale Website in Taiwan.

## Run the script

```sh
git clone https://github.com/Yidti/house-cat.git
cd house-cat
python3.10 main.py
```

## Examples

![sample-1](https://github.com/Yidti/house-cat/blob/master/sample/sample-1.png)
![sample-2](https://github.com/Yidti/houses-cat/blob/master/sample/sample-2.png)

## Introduction - [Web Crawler](https://en.wikipedia.org/wiki/Web_crawler)

網路爬蟲，一種用來自動瀏覽全球資訊網的機器人，其目的一般為編纂網路索引使用。

## Version History

### V.1.0 - 2022.06.25

1. crawler target for real estate (`https://buy.housefun.com.tw/region`)
2. select city and district in Taiwan
3. save url for district into txt file (`district_url.txt`)
4. save house information into csv file (`house_properties.csv`)