queue()
	.defer(d3.json, "/ToukaAnalytics")
    .await(makeGraphs);

function makeGraphs(error, projectsJson) {
	
	//Clean projectsJson data
	var toukaProjects = projectsJson;
	var dateFormat = d3.time.format("%m-%y");
	console.log(toukaProjects);

	//Create a Crossfilter instance
	var ndx = crossfilter(toukaProjects);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d3.time(d["msg_timstamps"]*1000); });
	console.log(dateDim);
	var msgCountDim = ndx.dimension(function(d) { return d["msg_count"]; });
	var charCountDim = ndx.dimension(function(d) { return d["char_count"]; });
	var ratioDim = ndx.dimension(function(d) { return d["ratio_char_msg"]; });
	// var totalMsgDim  = ndx.dimension();


	//Calculate metrics
	var numProjectsByDate = dateDim.group(); 
	var numProjectsByMsgCount = msgCountDim.group();
	var numProjectsByCharCount = charCountDim.group();
	var numProjectsByRatio = ratioDim.group();

	var all = ndx.groupAll();
	// var totalDonations = ndx.groupAll().reduceSum(function(d) {return d[""];});

	var max_msg = numProjectsByMsgCount.top(1)[0].value;
	var max_msg_author = numProjectsByMsgCount.top(1)[0].key;

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["msg_timstamps"];
	var maxDate = dateDim.top(1)[0]["msg_timstamps"];

    //Charts
	var timeChart = dc.barChart("#time-chart");
	var msgCountChart = dc.rowChart("#msg-count-row-chart");
	var charCountChart = dc.rowChart("#char-count-row-chart");
	var ratioChart = dc.rowChart("#ratio-row-chart");
	var numberProjectsND = dc.numberDisplay("#number-projects-nd");
	// var totalDonationsND = dc.numberDisplay("#total-donations-nd");

	numberProjectsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(all);

	totalDonationsND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalDonations)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numProjectsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);

	msgCountChart
        .width(300)
        .height(250)
        .dimension(msgCountDim)
        .group(numProjectsByMsgCount)
        .xAxis().ticks(4);

	charCountChart
		.width(300)
		.height(250)
        .dimension(charCountDim)
        .group(numProjectsByCharCount)
        .xAxis().ticks(4);

    dc.renderAll();

};