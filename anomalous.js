//TODO: Convert this from a global variable to a "plotting function"
var opts = {
    scales: {
	"x" : {
	    time: false
	}
    },
    axes: [
	{
	    space: 60
	},
	{
       	    show: true,
       	    label: "Healthy Rat",
       	    labelSize: 30,
       	    labelFont: "bold 12px Arial",
       	    font: "12px Arial",
       	    gap: 5,
       	    size: 100,
       	    stroke: "black",
       	    grid: {
       		show: true,
       		stroke: "#eee",
       		width: 2,
       		dash: [],
       	    },
       	    ticks: {
       		show: true,
       		stroke: "#eee",
       		width: 2,
       		dash: [],
       		size: 20,
       	    }
 	}
    ],
    title: "Anomalous Points Finder",
    id: "chart1",
    class: "my-chart",
    width: 1200 + 100,
    height: 600,
    series: [
       	{},
       	{
       	    show: true,
	    spanGaps: false,
       	    stroke: "red",
	    width: 4,
       	    fill: "rgba(255, 0, 0, 0)",
       	},
	{
       	    show: true,
       	    spanGaps: false,
	    label: "Data",
       	    stroke: "black",
       	    width: 1,
       	    fill: "rgba(0, 0, 0, 0)",
       	    dash: [10, 5],
       	},
    ],
};


function renderAnomalousPoints() {
    // 1. Graph the anomalous points on level 4 data with the red dots.
    // 2. Create text boxes on the side that zoom to a certain anomalous point
    // 3. On zoom -> move to a level 0 data
    fetch('http://localhost:8000/getAllData', {
	method: "POST",
	body: JSON.stringify({
	    plot_type: 'rat_healthy',
	    max_x_values: 21000000,
	    level: 5,
	})
    }).then(res => res.json())
	.then(json => {
	    let apoints = new Array(json.data[0].length).fill(0);
	    for(let i = 0; i < json.apoints[1].length; i++) {
		let rawValue = json.apoints[1][i];
		let idxOfValue = (json.data[1].indexOf(json.apoints[1][i]));
		console.log(idxOfValue);
		apoints[idxOfValue] = rawValue;

	    }
	    let uplot = new uPlot(opts,[json.data[0], apoints, json.data[1]],document.getElementById('graph'));
	})

}
renderAnomalousPoints();
