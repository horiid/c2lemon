// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById('httpPieChart')

var ratioData = {}
for(let host in hosts) {
    for(let i=0; i<hosts[host].length; i++) {
        statusCode = hosts[host][i]['http-response-ext']['status_code'] === "" ? 0 : hosts[host][i]['http-response-ext']['status_code']
        if(!(statusCode in ratioData)){
            ratioData[statusCode.toString()] = 1
        }
        ratioData[statusCode.toString()] += 1
    }
}

var httpPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        datasets: [{
            data: Object.values(ratioData)
        }],
        labels: Object.keys(ratioData)
    },
    options: {
        plugins: {
            colorschemes: {
                scheme: 'office.BlueII6'
            }
        },
    }
})

console.log(httpPieChart)