Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById('pingLineChart')
var pingChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: []
    },
    options: {
        plugins: {
            colorschemes: {
                scheme: 'office.BlueII6'
            }
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'day'
                },
                scaleLabel: {
                    display: true,
                },
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    suggestedMin: 0,
                    suggestedMax: 100,
                    stepSize: 25
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Loss Rate (%)'
                },
            }]
        }
    }
})

for(let host in hosts) {
    var hostData = []
    for(let i=0; i < hosts[host].length; i++){
        var lossRate = hosts[host][i]['ping-ext']['loss'] === "" ? 100 : hosts[host][i]['ping-ext']['loss'].replace(/%/g, "")
        hostData.push({
            x: hosts[host][i]['observed-time'],
            y: lossRate
        })
    }
    pingChart.data.datasets.push({
        label: host,
        data: hostData,
        fill: false,
        lineTension: 0
    })
    pingChart.update()
}
console.log(pingChart.data.datasets)
/* 

httpChart.data.datasets.data.push({
        label: host,
        data: data
    })

[
    {x: "2020-11:11T00:00:00", y: "200"},
    {x: "2021-07:11T00:00:00", y: "404"}
]
*/