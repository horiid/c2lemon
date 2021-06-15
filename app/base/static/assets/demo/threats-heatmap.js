Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

heatmapData_epoch = {}
for(let key of Object.keys(heatmapData)) {
    epochTime = new Date(...(
        /(\d{4})-(\d{1,2})-(\d{1,2})/
        .exec(key)
        .slice(1)
        .map((v,i)=> v - (i===1?1:0))
      ))
    let activityLevel = (val)=>{
        if(val <= 0.2) return 0
        else if(val <= 0.4) return 10
        else if(val <= 0.6) return 20
        else if(val <= 0.8) return 30
        else if(val <= 1.0) return 40
    }
    heatmapData_epoch[epochTime.getTime()/1000] = activityLevel(heatmapData[key])
}
console.log(heatmapData_epoch)

var cal = new CalHeatMap();
var now = new Date();
cal.init({
    itemSelector: '#heatmap',
    domain: 'month',
    data: heatmapData_epoch,
    domainLabelFormat: '%Y-%m',
    start: new Date(now.getFullYear(), now.getMonth() - 11),
    cellSize: 10,
    range: 12,
    legendColors: {
        min: "#efefef",
        max: "red",
        empty: "#efefef"
    },
})
