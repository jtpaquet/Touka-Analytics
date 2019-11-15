queue()
	.defer(d3.json, "/ToukaAnalytics")
	.defer(d3.json, "/members")
    .await(makeGraphs);

function makeGraphs(error, projectsJson, membersJson) {
	
	//Clean projectsJson data
	var toukaData = projectsJson;
	var membersData = {};
	membersJson.forEach(function(d) {
		membersData[d['name']] = d['pseudo'];
	});
	var dateFormat = d3.time.format("%Y-%m-%d");
	toukaData.forEach(function(d) {
		d["timestamp"] = new Date(d['timestamp']);
		d['author'] = membersData[d['author']];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(toukaData);

	//Define Dimensions
	var authorDim = ndx.dimension(function(d) { return d["author"] });
	// Si je veux avoir tous les messages écrits par un auteur, je fais authorDim.filter('author')
	var dateDim = ndx.dimension(function(d) { return d["timestamp"] });
	var typeDim = ndx.dimension(function(d) { return d["type"] });
	var contentDim = ndx.dimension(function(d) { return d["content"] });

	//Calculate metrics
	var msgByAuthor = authorDim.group();
	var msgByDate = dateDim.group(); 
	var msgByType = typeDim.group();
	var msgByContent = contentDim.group();

	var all = ndx.groupAll();
	var totalMsg = all.reduceCount().value();

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["timestamp"];
	var maxDate = dateDim.top(1)[0]["timestamp"];

    //Charts
	var timeChart = dc.lineChart("#time-chart");
	var msgCountChart = dc.barChart("#msg-count-bar-chart");
	var totalMsgND = dc.numberDisplay("#total-msg-nd");

	totalMsgND
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalMsg)
		.formatNumber(d3.format(".3s"));

	timeChart
		.width(600)
		.height(160)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(msgByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.elasticY(true)
		.xAxisLabel("Year")
		.yAxis().ticks(4);

	msgCountChart
        .width(300)
        .height(250)
        .dimension(authorDim)
        .group(msgByAuthor)
        .xAxis().ticks(4);

    dc.renderAll();

};