// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function (n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

// Bar Chart
export function barchart(volatility, volatility_average, volatility_date) {
    var ctx = document.getElementById("myBarChart");
    var myBarChart = new Chart(ctx, {
        data: {

            datasets: [
                {
                    type: 'bar',
                    label: "異常後波動率",
                    backgroundColor: "#4e73df",
                    hoverBackgroundColor: "#2e59d9",
                    borderColor: "#4e73df",
                    data: volatility
                },


                {
                    type: 'line',
                    label: "平均波動率",
                    data: volatility_average
                }


            ],
            labels: volatility_date,
        },

        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    time: {
                        unit: 'month'
                    },
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    },
                    maxBarThickness: 25,
                }],
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: (Math.max(...volatility) + 1).toFixed(0) ,
                        maxTicksLimit: 5 ,
                        padding: 10,
                        // Include a dollar sign in the ticks
                        callback: function (value, index, values) {
                            return number_format(value) + "%";
                        }
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
            },
            legend: {
                display: true,
                align: "end",
            },
            tooltips: {
                titleMarginBottom: 10,
                titleFontColor: '#6e707e',
                titleFontSize: 14,
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
                callbacks: {
                    label: function (tooltipItem, chart) {
                        var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                        return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                    }
                }
            },
        }

    });
}

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
barchart(volatility, volatility_average, volatility_date)




