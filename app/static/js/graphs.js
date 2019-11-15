queue()
	.defer(d3.json, "/ToukaAnalytics")
    .await(makeGraphs);

function makeGraphs(error, projectsJson) {
	
	//Clean projectsJson data
	var toukaProjects = JSON.parse(projectsJson);
	// var dateFormat = d3.time.format("%m-%y");
	for (var member in toukaProjects['timestamp']) {
		toukaProjects['timestamp'][member].forEach(function(elem, idx, arr) {arr[idx] = new Date(elem); });
	}
	var total_msg = 0;
	for (var member in toukaProjects['n_msg']) {
		total_msg += toukaProjects['n_msg'][member];
	}

	// var ndx = crossfilter(toukaProjects);

	// set the dimensions and margins of the graph
	var margin = {top: 10, right: 30, bottom: 30, left: 60},
		width = 460 - margin.left - margin.right,
		height = 400 - margin.top - margin.bottom;

	// append the svg object to the body of the page
	var svg = d3.select("#time-chart")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform",
			"translate(" + margin.left + "," + margin.top + ")");
	

	for (var member in toukaProjects['timestamp']) {
		if (member == 'Djézeune') {

			// Add X axis --> it is a date format
			var x = d3.scaleTime()
			.domain(toukaProjects['timestamp'][member])
			.range([ 0, width ]);
			svg.append("g")
			.attr("transform", "translate(0," + height + ")")
			.call(d3.axisBottom(x));
			
			// Add Y axis
			var y = d3.scaleLinear()
			.domain(range(1, toukaProjects['timestamp'][member].length))
			.range([ height, 0 ]);
			svg.append("g")
			.call(d3.axisLeft(y));
			
			// Add the area
			svg.append("path")
			.datum(toukaProjects['timestamp'][member])
			.attr("fill", "#cce5df")
			.attr("stroke", "#69b3a2")
			.attr("stroke-width", 1.5)
			.attr("d", d3.area()
			.x(function(d) { return x(d.date) })
			.y0(y(0))
			.y1(function(d) { return y(d.value) })
			)
		}
	}

};
