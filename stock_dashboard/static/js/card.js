//異常發生日期
var accurentTime = []

// array index位置
var indexs = []

annomyTime.forEach(function (value, index) {
    if (annomy[value] == 1) {
        accurentTime.push(value)
        indexs.push(index)
    } else {
    }
})

// 最近異常發生日
var accurentdate = accurentTime[accurentTime.length - 1]

// 異常佔比
var percent = accurentTime.length / time.length * 100

//最近異常當日股價
var price_annony_now = closePrice[indexs[accurentTime.length - 1]]

//最近異常前一日股價
var price_past_day = closePrice[indexs[accurentTime.length - 1] - 1]

//最近異常股價報酬率
var accurentreturn = ((price_annony_now - price_past_day) / price_past_day) * 100


$("div#accurentdate").text(accurentdate)

$("div#accurenttime").text(accurentTime.length)

$("div#accurentpercent").text(Math.round(percent) + "%")

$("div#displayPrecent").attr("style", "width:" + Math.round(percent) + "%")

$("div#accurentreturn").text(accurentreturn.toFixed(2) + "%")



