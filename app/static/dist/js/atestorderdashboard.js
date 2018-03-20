// 用于显示订单页面趋势的图表
function showdata(divid,number){
     $('#'+divid).sparkline(number,{
        type: 'line',
        width: '250',
        height: '90',
		lineColor: '#1f1fec',
		fillColor: 'rgba(97,246,225)',
		maxSpotColor: '#2879ff',
		highlightLineColor: 'rgba(0, 0, 0, 0)',
		highlightSpotColor: '#f80617'
    }); 
}
