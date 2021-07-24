
var accurentTime = []
var indexs = []
annomyTime.forEach( function(value, index) {
    if (annomy[value] == 1 ){
      accurentTime.push(value)
      indexs.push(index)
    }else {
    }
    })

var  accurentdate =  accurentTime[accurentTime.length - 1]

var percent = accurentTime.length/time.length*100

var price_annony_now = closePrice[indexs[accurentTime.length - 1]]

var price_past_day = closePrice[indexs[accurentTime.length - 1] -1]

var accurentreturn = ((price_annony_now - price_past_day) / price_past_day)*100

console.log(closePrice[indexs[accurentTime.length - 1]])
console.log(closePrice[indexs[accurentTime.length - 1] -1])

$("div#accurentdate").text( accurentdate)

$("div#accurenttime").text(accurentTime.length)

$("div#accurentpercent").text(Math.round(percent)+ "%")

$("div#displayPrecent").attr("style","width:" +Math.round(percent)+ "%")

$("div#accurentreturn").text(accurentreturn.toFixed(2) + "%")



