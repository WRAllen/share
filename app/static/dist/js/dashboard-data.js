/*Dashboard Init*/
 
"use strict"; 

/*****Ready function start*****/
$(document).ready(function(){
	$('#statement').DataTable({
		"bFilter": false,
		"bLengthChange": false,
		"bPaginate": false,
		"bInfo": false,
	});
	if( $('#chart_2').length > 0 ){
		var ctx2 = document.getElementById("chart_2").getContext("2d");
		var data2 = order_data
		
		var hBar = new Chart(ctx2, {
			type:"horizontalBar",
			data:data2,
			
			options: {
				tooltips: {
					mode:"label"
				},
				scales: {
					yAxes: [{
						stacked: true,
						gridLines: {
							color: "#878787",
						},
						ticks: {
							fontFamily: "Roboto",
							fontColor:"#878787"
						}
					}],
					xAxes: [{
						stacked: true,
						gridLines: {
							color: "#878787",
						},
						ticks: {
							fontFamily: "Roboto",
							fontColor:"#878787"
						}
					}],
					
				},
				elements:{
					point: {
						hitRadius:40
					}
				},
				animation: {
					duration:	3000
				},
				responsive: true,
				maintainAspectRatio:false,
				legend: {
					display: false,
				},
				
				tooltip: {
					backgroundColor:'rgba(33,33,33,1)',
					cornerRadius:0,
					footerFontFamily:"'Roboto'"
				}
				
			}
		});
	}
	if( $('#chart_6').length > 0 ){
		var ctx6 = document.getElementById("chart_6").getContext("2d");
		var data6 = category1
		
		var pieChart  = new Chart(ctx6,{
			type: 'pie',
			data: data6,
			options: {
				animation: {
					duration:	3000
				},
				responsive: true,
				maintainAspectRatio:false,
				legend: {
					display:false
				},
				tooltip: {
					backgroundColor:'rgba(33,33,33,1)',
					cornerRadius:0,
					footerFontFamily:"'Roboto'"
				},
				elements: {
					arc: {
						borderWidth: 0
					}
				}
			}
		});
	}
	// 30天鞋子服饰折线图
	if($('#morris_extra_line_chart').length > 0) {
		var data= sale_num
		var dataNew = sale_pro

		var lineChart = Morris.Line({
	        element: 'morris_extra_line_chart',
	        data: data ,
	        xkey: '天',
	        ykeys: ['鞋类', '服饰', '其它'],
	        labels: ['鞋类', '服饰', '其它'],
	        pointSize: 2,
	        fillOpacity: 0,
			lineWidth:2,
			pointStrokeColors:['#fec107', '#e91e63', '#2879ff'],
			behaveLikeLine: true,
			gridLineColor: '#878787',
			hideHover: 'auto',
			lineColors: ['#fec107', '#e91e63', '#2879ff'],
			resize: true,
			redraw: true,
			gridTextColor:'#878787',
			gridTextFamily:"Roboto",
	        parseTime: false
   		});

	}
 	// 4大平台销售数量和金额
	if($('#4platform').length > 0) {
		var platformdata= platform_num
		var platformdataNew = platform_pro
		// 这里不把linechart改了就会用上面那个函数的横坐标
		var platform_line = Morris.Line({
	        element: '4platform',
	        data: platformdata ,
	        xkey: '天',
	        ykeys: ['TOTAL','AMAZON','ALIEXPRESS','EBAY','WISH'],
	        // 纯粹显示用的标签
	        labels: ['总和','亚马逊','速卖通','EBAY','WISH',],
	        pointSize: 2,
	        fillOpacity: 0,
			lineWidth:2,
			pointStrokeColors:['#fec107', '#e91e63', '#2879ff','#f80617','#f711ff'],
			behaveLikeLine: true,
			gridLineColor: '#878787',
			hideHover: 'auto',
			lineColors: ['#fec107', '#e91e63', '#2879ff','#f80617','#f711ff'],
			resize: true,
			redraw: true,
			gridTextColor:'#878787',
			gridTextFamily:"Roboto",
	        parseTime: false
   		});

	}



	/* Switchery Init*/
	var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
	$('#morris_switch').each(function() {
		new Switchery($(this)[0], $(this).data());
	});
	var swichMorris = function() {
		if($("#morris_switch").is(":checked")) {
			lineChart.setData(data);
			lineChart.redraw();
		} else {
			lineChart.setData(dataNew);
			lineChart.redraw();
		}
	}
	swichMorris();	
	$(document).on('change', '#morris_switch', function () {
		swichMorris();
	});

	// 4platform按钮
	$('#platform_switch').each(function() {
		new Switchery($(this)[0], $(this).data());
	});
	var swichplatform = function() {
		if($("#platform_switch").is(":checked")) {
			platform_line.setData(platform_num);
			platform_line.redraw();
		} else {
			platform_line.setData(platform_pro);
			platform_line.redraw();
		}
	}
	swichplatform();	
	$(document).on('change', '#platform_switch', function () {
		swichplatform();
	});
	
});
/*****Ready function end*****/

/*****Load function start*****/
$(window).load(function(){
	window.setTimeout(function(){
		$.toast({
			heading: 'Welcome to Hound',
			text: 'Use the predefined ones, or specify a custom position object.',
			position: 'top-right',
			loaderBg:'#fec107',
			icon: 'success',
			hideAfter: 3500, 
			stack: 6
		});
	}, 3000);
});
/*****Load function* end*****/

var sparklineLogin = function() { 
	if( $('#sparkline_1').length > 0 ){
		$("#sparkline_1").sparkline(xz_week, {
			type: 'line',
			width: '100%',
			height: '35',
			lineColor: '#2879ff',
			fillColor: 'rgba(40,121,255,.2)',
			maxSpotColor: '#2879ff',
			highlightLineColor: 'rgba(0, 0, 0, 0.2)',
			highlightSpotColor: '#2879ff'
		});
	}	
	if( $('#sparkline_2').length > 0 ){
		$("#sparkline_2").sparkline(fs_week, {
			type: 'line',
			width: '100%',
			height: '35',
			lineColor: '#2879ff',
			fillColor: 'rgba(40,121,255,.2)',
			maxSpotColor: '#2879ff',
			highlightLineColor: 'rgba(0, 0, 0, 0.2)',
			highlightSpotColor: '#2879ff'
		});
	}	
	if( $('#sparkline_3').length > 0 ){
		$("#sparkline_3").sparkline(qt_week, {
			type: 'line',
			width: '100%',
			height: '35',
			lineColor: '#2879ff',
			fillColor: 'rgba(40,121,255,.2)',
			maxSpotColor: '#2879ff',
			highlightLineColor: 'rgba(0, 0, 0, 0.2)',
			highlightSpotColor: '#2879ff'
		});
	}
	if( $('#sparkline_4').length > 0 ){
		$("#sparkline_4").sparkline([0,2,8,6,8,5,6,4,8,6,6,2 ], {
			type: 'bar',
			width: '100%',
			height: '50',
			barWidth: '5',
			resize: true,
			barSpacing: '5',
			barColor: '#fec107',
			highlightSpotColor: '#fec107'
		});
	}	
}
var sparkResize;
	$(window).resize(function(e) {
		clearTimeout(sparkResize);
		sparkResize = setTimeout(sparklineLogin, 200);
	});
sparklineLogin();
