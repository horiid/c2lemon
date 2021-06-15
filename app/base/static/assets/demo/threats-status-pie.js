// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

let statusDict = {};
for(let key of statusCodes){
  statusDict[key] = statusCodes.filter(function(x){return x==key}).length
}
console.log(statusDict)
console.log(Object.keys(statusDict))
// Pie Chart Example
var ctx = document.getElementById("httpPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: Object.keys(statusDict),
    datasets: [{
      data: Object.values(statusDict),
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
