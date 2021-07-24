Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
var canvas = document.getElementById("myAreaChart");
var ctx = canvas.getContext("2d");


// 收盤價
var close = data["Close"]

console.log(close)
// 選取收盤價index時間
var time = Object.keys(close)

// 遍例收盤價
var closePrice = []
time.forEach(t => closePrice.push(close[t]))




// 選取異常點
var annomy = data["annomy"]
var annomyTime = Object.keys(annomy)

// var color = []

// 正常點的顏色
var normalColor = "rgba(78, 115, 223, 1)"

// 異常點的顏色
var annomyColor = "rgb(238,11,11)"

// 作圖時異常與正常點的顏色
var annomyPoint = []

// 作圖時異常與正常點的大小
var pointRadius = []


annomyTime.forEach(t => {
    if (annomy[t] == 1) {
        annomyPoint.push(annomyColor)
        pointRadius.push(2)

    } else {
        annomyPoint.push(normalColor)
        pointRadius.push(0)
    }

})


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





// 畫股價圖與異常點
var myLineChart = new Chart(ctx, {
    data: {
        labels: time,
        datasets: [{
            type: 'line',
            label: "收盤價",
            lineTension: 0.3,
            backgroundColor: "rgba(78, 115, 223, 0.05)",
            borderColor: "rgba(78, 115, 223, 1)",
            pointRadius: pointRadius,
            pointBackgroundColor: annomyPoint,
            pointBorderColor: annomyPoint,
            pointHoverRadius: 3,
            pointHoverBackgroundColor: annomyPoint,
            pointHoverBorderColor: annomyPoint,
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: closePrice,
        },
            {
                type: 'scatter',
                label: "異常點",
                pointBorderColor: 'rgb(255, 99, 132)',
                pointBackgroundColor: 'rgb(255, 99, 132)'

            }
        ],
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
                    unit: 'date'
                },
                gridLines: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    maxTicksLimit: 7
                }
            }],
            yAxes: [{
                ticks: {
                    maxTicksLimit: 5,
                    padding: 10,
                    // Include a dollar sign in the ticks
                    callback: function (value, index, values) {
                        return '$' + number_format(value);
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
            labels: {
                boxWidth: 80,
                usePointStyle: true,
                pointStyle: "circle",
                color: 'rgb(255, 99, 132)'
            },
            title: {
                display: true,
                text: "teste"


            }


        },
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: 'index',
            caretPadding: 10,
            callbacks: {
                label: function (tooltipItem, chart) {
                    var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                    point = chart.datasets[tooltipItem.datasetIndex].pointRadius[tooltipItem.index]
                    if (point == 3) {

                        return datasetLabel + ': $' + number_format(tooltipItem.yLabel) + " annnomy: True";

                    } else {

                        return datasetLabel + ': $' + number_format(tooltipItem.yLabel) + " annnomy:False ";
                    }
                    // var annomy = chart.dataIndex.pointRadius || '';


                }
            }
        }
    }
});




