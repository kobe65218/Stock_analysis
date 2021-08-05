## 三大法人異常偵測

* 透過爬蟲抓取證交所三大法人資訊並以isolation forest進行異常偵測
* 主要將爬取資料及模型預測結果存入Mysql並將訓練好的模型存入Mongodb，以每日自動化產出結果
* 透過airflow將爬取資料及丟入模型預測，自動化排程成例行pipline
* 以flask為框架呈現dashboard
* 開發過程以jenkins及Ansible實現專案自動化整合以及部署至gcp
* 目前架設於gcp : <http://34.81.62.62:5000/>
