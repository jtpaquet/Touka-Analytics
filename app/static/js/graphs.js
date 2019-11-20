queue()
	.defer(d3.json, "/ToukaAnalytics")
    .await(makeGraphs);

function makeGraphs(error, projectsJson) {
};
