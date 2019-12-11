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
	var minMonth = monthDim.bottom(1)[0]["month"];
	var maxMonth = monthDim.top(1)[0]["month"];

    //Charts
	var timeChart = dc.lineChart("#time-chart");
	var msgCountChart = dc.barChart("#msg-count-row-chart");
	var msgPctChart = dc.pieChart('#poverty-level-row-chart')
	var totalMsgND = dc.numberDisplay("#total-msg-nd");
	var toukaCreation = timeFormat(minDate);

	timeChart
		.width(600)
		.height(160)
		.x(d3.scale.linear().domain())
		.y()


	msgCountChart
		.width(300)
		.height(280)
		.x(d3.scale.ordinal().domain(toukaData["n_msg"].map(function(d) {return d.key })))
		.y(d3.scale.linear().domain([0, max(toukaData["n_msg"])+5000]))
		.xUnits(dc.units.ordinal)
		.brushOn(false)
		.yAxisLabel("Messages envoyés")
		
	totalMsgND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all)
		.formatNumber(d3.format(".3s"));
	
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
