function handleLevelChangeEvent(val) {
    let obj = document.getElementById('chart1');
    obj.remove()
    obj = document.getElementById('radio-fragment');
    obj.remove()
    getData(val);
}
function renderChunk() {
    let inputLevel = parseInt(document.getElementById("level").innerText);
    let val = document.getElementById("chunk").innerText;
    let obj = document.getElementById('chart1');
    obj.remove()
    fetch('http://localhost:8000/getAllDataForChunk', {
	method: "POST",
	body: JSON.stringify({plot_type: 'rat_healthy', max_x_values: 21000000, chunk_number: parseInt(val), level: inputLevel})
    }).then(res => res.json()).then(json => {
	let opts = {
	    scales: {
		"x" : {
       		    time: false,
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
	    title: "Healthy Rat Brain Scan",
	    id: "chart1",
	    class: "my-chart",
	    width: 1200 + 100,
	    height: 600,
	    series: [
       		{
		},
       		{
       		    show: true,
       		    spanGaps: false,
       		    stroke: "black",
       		    width: 1,
       		    fill: "rgba(0, 0, 0, 0)",
       		    dash: [10, 5],
       		}
	    ],
	};
	console.log(json.data);
	let uplot = new uPlot(opts,json.data, document.getElementById('graph'));
    })
}
function renderNextChunk(direction) {
    let inputLevel = parseInt(document.getElementById("level").innerText);
    if(direction == 'forward' && document.getElementById("chunk").innerText != document.getElementById("num-chunks").innerText) {
	document.getElementById('chunk').innerText = parseInt(document.getElementById('chunk').innerText) + 1
	renderChunk();
    }
    if(direction == 'backward' && document.getElementById('chunk').innerText != "0") {
	document.getElementById('chunk').innerText = parseInt(document.getElementById('chunk').innerText) - 1
	renderChunk();
    }


}
function createRadioElement(name, checked, id, lbl, lbl_prefix = 'level', onclick_value = true, root_div = 'levels', child_div = 'radio-fragment') {
    if(document.getElementById(child_div) == null) {
	console.log(root_div);
	document.getElementById(root_div).innerHTML += `<div id="radio-fragment" style='text-align:right;display:block;float:right;margin:10px;'> </div>`
    }
    var radioHtml = '<input type="radio" value=03 name="' + name + '"';
    if (checked) {
	radioHtml += ' checked="checked"';
    }
    radioHtml += 'id=' + id;
    radioHtml += ' onclick=handleLevelChangeEvent(this.id)';

    radioHtml += `>${lbl_prefix}=${lbl}`;

    document.getElementById('radio-fragment').innerHTML += radioHtml;
    // document.getElementById('radio-fragment').innerHTML += `<label style='float=right;' for=${id}> ${lbl}</label>`
    document.getElementById('radio-fragment').innerHTML += '<br /><br />'
}



function getData(inputLevel) {
    document.getElementById('level').innerText = inputLevel;
    fetch('http://localhost:8000/getAllData', {
	method: "POST",
	body: JSON.stringify({plot_type: 'rat_healthy', max_x_values: 21000000, level: inputLevel})
    })
	.then(res => res.json())
	.then(json => {
	    document.getElementById('num-levels').innerText = json.num_levels;
	    document.getElementById('chunk').innerText = 0;
	    document.getElementById('num-chunks').innerText = json.num_chunks;
	    let opts = {
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
		title: "Healthy Rat Brain Scan",
		id: "chart1",
		class: "my-chart",
		width: 1200 + 100,
		height: 600,
		series: [
       		    {},
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
	    
	    apoints[json.apoints[0][0]] = json.apoints[1][0];
	    apoints[json.apoints[0][1]] = json.apoints[1][1];
	    console.log(apoints);
	    let vals = json.data;
	    console.log("VALS -> ", vals);
	    let uplot = new uPlot(opts,vals,document.getElementById('graph'));
	    console.log(json.level);
	    for(let i = 0; i < parseInt(json.num_levels) + 2; i++) {
		if(i == json.level) createRadioElement('levelRadio', true, '0' + i, i);
		else createRadioElement('levelRadio',false , i, i);
	    }
	});


}

getData(2)
