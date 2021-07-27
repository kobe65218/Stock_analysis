import { barchart } from './bar_chart.js'


$("button#dateButton").click(() => {
    var stock_id = $("input#search").val()
    location.href = "http:/?stock_id=" + stock_id

})

$("button#searchbutton").click(() => {
    var stock_id = $("input#search").val()
    location.href = "http:/?stock_id=" + stock_id

})

$("button#dateButton").click(() => {
    var stock_id = $("input#search").val()
    var start = $("input#start").val()
    var end = $("input#end").val()
    location.href = "http:/?stock_id=" + stock_id + "&start=" + start + "&end=" + end


})



// 異常發生後幾日下拉式選單bar_chart
$("a.dropdown-item").click(
    function () {
        var date_after = this.getAttribute('value')
        console.log(date_after)


        // 股價假報酬率
        var close_log_ = data["Close_log"]



        // 取出股價報酬率
        var close_log = []
        time.forEach(t => {
            if (!isNaN(close_log_[t])) {
                close_log.push(close_log_[t])
            }
        })

        // 計算標準差
        function getStandardDeviation(array) {
            const n = array.length
            const mean = array.reduce((a, b) => a + b) / n
            return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n)
        }


        // 計算全部報酬率波動率
        var average_volatility = getStandardDeviation(close_log) * 100

        // 記錄發生異常後幾日波動
        var volatility = []

        //// 記錄發生異常日
        var volatility_date = []


        accurentTime.forEach((date, number) => {
                var near = []
                for (var i = 0; i <= date_after; i++) {
                    var close_log_re = close_log[indexs[number] + i]
                    near.push(close_log_re)
                }
                if (!isNaN(getStandardDeviation(near) * 100)) {
                    volatility.push(getStandardDeviation(near) * 100)
                    volatility_date.push(date)
                }

            }
        )

        // 畫平均異常的線
        var volatility_average = []
        for (var i = 0; i <= volatility.length; i++) {
            volatility_average.push(average_volatility)
        }
        barchart(volatility , volatility_average,volatility_date)
        $('a#dropdownMenuLink').text('異常發生後'+date_after+'日')
        $('h6#barchart_title').text('異常發生'+ date_after + ' 日後報酬波動率')
    }
)
