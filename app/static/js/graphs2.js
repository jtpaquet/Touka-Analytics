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
	var dateFormat = d3.time.format("%Y-%m");
	var timeFormat = d3.time.format("%a %d %b %Y à %Hh%Mm%ss");
	toukaData.forEach(function(d) {
		d["timestamp"] = new Date(d['timestamp']);
		d["month"] = dateFormat(new Date(d['timestamp']));
		d['author'] = membersData[d['author']];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(toukaData);

	//Define Dimensions
	var authorDim = ndx.dimension(function(d) { return d.author });
	// Si je veux avoir tous les messages écrits par un auteur, je fais authorDim.filter('author')
	var dateDim = ndx.dimension(function(d) { return d.timestamp });
	var monthDim = ndx.dimension(function(d) { return d.month });
	var typeDim = ndx.dimension(function(d) { return d.type });
	// var contentDim = ndx.dimension(function(d) { return d.content }); // On en a pas vrm besoin

	//Calculate metrics
	var msgByAuthor = authorDim.group();
	var n_msgByAuthor = msgByAuthor.top(msgByAuthor.size());
	// msgByAuthor.reduceCount().all()
	// var msgByDate = dateDim.group(); // pas besoin
	var msgByMonth = monthDim.group();
	var msgByType = typeDim.group();
	// msgByType.reduceCount().all()
	// var msgByContent = contentDim.group(); // pas besoin

	var all = ndx.groupAll();
	var totalMsg = all.reduceCount().value();

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["timestamp"];
	var maxDate = dateDim.top(1)[0]["timestamp"];
	var minMonth = monthDim.bottom(1)[0]["month"];
	var maxMonth = monthDim.top(1)[0]["month"];

    //Charts
	// var timeChart = dc.lineChart("#time-chart");
	var msgCountChart = dc.barChart("#msg-count-row-chart");
	var totalMsgND = dc.numberDisplay("#total-msg-nd");
	var toukaCreation = timeFormat(minDate);

	msgCountChart
		.width(300)
		.height(280)
		.x(d3.scale.ordinal().domain(n_msgByAuthor.map(function(d) {return d.key })))
		.y(d3.scale.linear().domain([0, 55000]))
		.xUnits(dc.units.ordinal)
		.brushOn(false)
		.yAxisLabel("Messages envoyés")
		.dimension(authorDim)
		.group(msgByAuthor)
		
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

    dc.renderAll();
	console.log("--Graphics rendered--")
};
