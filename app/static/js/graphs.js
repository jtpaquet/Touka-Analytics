queue()
	.defer(d3.json, "/ToukaAnalytics")
    .await(makeGraphs);

function makeGraphs(error, dataJson) {

	//Clean dataJson data
	var toukaData = dataJson;
	var dateFormat = d3.time.format("%m-%Y");
	var timeFormat = d3.time.format("%a %d %b %Y à %Hh%Mm%ss");
	console.log(toukaData);
	//Define values (to be used in charts)
	var minDate = toukaData['date_min'];
	var maxDate = toukaData['date_max'];
	var minMonth = dateFormat(new Date(minDate))
	var maxMonth = dateFormat(new Date(maxDate))

    //Charts
	// var timeChart = dc.lineChart("#time-chart");
	var msgCountBarChart = dc.barChart("#msg-count-row-chart");
	// var msgCountPieChart = dc.pieChart('#msg-count-pie-chart')
	// var totalMsgND = dc.numberDisplay("#total-msg-nd");
	var toukaCreation = timeFormat(new Date(minDate));

	// timeChart
	// 	.width(600)
	// 	.height(160)
	// 	.x(d3.scale.linear().domain())
	// 	.y()

	var data_n_msg = [];
	for(var key in toukaData["n_msg"]) {
		if ((key != "Kaven") && (key != "Marcel Leboeuf") && (key != "Charles Pilon")) {
			data_n_msg.push({"author":key, "count":toukaData["n_msg"][key]});
		}
	};
	
	var ndx = crossfilter(data_n_msg);
	authorDimension = ndx.dimension(function(d) {return d.author;});
	authorGroup = authorDimension.group().reduceSum(function(d) {return d.count;});
	
	var names = [];
	authorGroup.top(Infinity).forEach(function(d) {names.push(d.author)});

	msgCountBarChart
		.width(300)
		.height(250)
		.x(d3.scale.ordinal())
		.xUnits(dc.units.ordinal)
		// .y(d3.scale.linear().domain([0, Math.ceil(Math.max(...Object.values(authorGroup.top(1)[0].value)) / 10000) * 10000]))
		.renderlet(function (chart) {
			chart.selectAll("g.x text")
			.attr('dx', '-30')
			.attr('transform', "rotate(-45)");
		})
		.brushOn(false)
		.yAxisLabel("Messages envoyés")
		.dimension(authorDimension)
		.group(authorGroup)

	msgCountBarChart.ordering(function(d) { return -d.value; })


	// msgCountPieChart
	// 	.width(300)
	// 	.height(250)
	// 	.x(d3.scale.ordinal())
	// 	.xUnits(dc.units.ordinal)
	// 	// .y(d3.scale.linear().domain([0, Math.ceil(Math.max(...Object.values(authorGroup.top(1)[0].value)) / 10000) * 10000]))
	// 	.renderlet(function (chart) {
	// 		chart.selectAll("g.x text")
	// 		.attr('dx', '-30')
	// 		.attr('transform', "rotate(-45)");
	// 	})
	// 	.brushOn(false)
	// 	.yAxisLabel("Messages envoyés")
	// 	.dimension(authorDimension)
	// 	.group(authorGroup);
		
	// totalMsgND
	// 	.formatNumber(d3.format("d"))
	// 	.valueAccessor(function(d){return d; })
	// 	.formatNumber(d3.format(".3s"));
	
	// timeChart
	// 	.width(600)
	// 	.height(160)
	// 	.margins({top: 10, right: 50, bottom: 30, left: 50})
	// 	.dimension(dateDim)
	// 	.group(msgByDate)
	// 	.transitionDuration(500)
	// 	.x(d3.time.scale().domain([minDate, maxDate]))
	// 	.elasticY(true)
	// 	.xAxisLabel("Year")
	// 	.yAxis().ticks(4);

	// Msg par année

    dc.renderAll();
	console.log("--Graphics rendered--")
};
