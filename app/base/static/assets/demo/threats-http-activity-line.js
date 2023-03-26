Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// input: ip address, domain or url
// sort data by input and monitor location
console.log("HOSTS",hosts)
for (let host in hosts) {
    console.log("LOCATIONS:", hosts[host])
    var ctx_http = document.getElementById('http_' + host)
    var httpChart = new Chart(ctx_http, {
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
                        suggestedMax: 599,
                        stepSize: 100
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Status Code'
                    },
                }]
            }
        }
    })
    var ctx_ping = document.getElementById('ping_' + host)
    var pingChart = new Chart(ctx_ping, {
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

    for(let location in hosts[host]) {
        // initialization
        console.log('LOCATION:', location)
        httpData = []
        pingData = []
        for(let data in hosts[host][location]) {
            if ("loss" in hosts[host][location][data]['ping-ext']){
                var lossRate = hosts[host][location][data]['ping-ext']['loss'] === "" ? 100 : hosts[host][location][data]['ping-ext']['loss'].replace(/%/g, "")
            }
            else if('lost' in hosts[host][location][data]['ping-ext']){
                var lossRate = hosts[host][location][data]['ping-ext']['lost'] === "" ? 100 : hosts[host][location][data]['ping-ext']['lost'].replace(/%/g, "")
            }
            pingData.push({
                x: hosts[host][location][data]['observed-time'],
                y: lossRate
            })
            httpData.push({
                x: hosts[host][location][data]['observed-time'],
                y: hosts[host][location][data]['http-response-ext']['status_code'] === "" ? 0 : hosts[host][location][data]['http-response-ext']['status_code']
            })
        }
        httpChart.data.datasets.push({
            label: location,
            data: httpData,
            fill: false,
            lineTension: 0,
        })
        pingChart.data.datasets.push({
            label: location,
            data: pingData,
            fill: false,
            lineTension: 0,
        })
        httpChart.update()
        pingChart.update()
    }
}

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