// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById('pingPieChart')

var ratioData = {}
for(let host in hosts) {
    for(let i=0; i<hosts[host].length; i++) {
        lossRate = hosts[host][i]['ping-ext']['loss'] === "" ? 0 : hosts[host][i]['ping-ext']['loss']
        if(!(lossRate in ratioData)){
            ratioData[lossRate.toString()] = 1
        }
        ratioData[lossRate.toString()] += 1
    }
}

var pingPieChart = new Chart(ctx, {
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

console.log(pingPieChart)