let currentChunk = 0;
let maxLevel = 4;
let G_MAX_VALUE = 1_000_000;
function handleLevelChangeEvent(val) {
    console.log('Handling Level Change Event');
//TODO: Fix bug that messes up level for lower levels (just run it and test and you'll see it)

    console.log(`Current chunk = ${currentChunk}`);
    let obj = document.getElementById('chart1');
    obj.remove()
    obj = document.getElementById('radio-fragment');
    obj.remove()
    let center = document.getElementById("myUL").innerText
    
    center = center.substr(1, center.length - 1)
    center = parseInt(center.split(',')[0])
    let computed_chunk = parseInt(center / G_MAX_VALUE)
    console.log("CENTERING POINT = ", computed_chunk);

    console.log(center);
    if (center) {
	document.getElementById('level').innerText = val;
	if (val != maxLevel) {
	    document.getElementById('chunk').innerText = Math.floor(computed_chunk/(parseInt(val)+1));
	}
	else {
	    document.getElementById('chunk').innerText=0;
	}
	renderChunk()
	for(let i = 0; i <= 4; i++) {
	    if(i == val) createRadioElement('levelRadio', true, i, i);
	    else createRadioElement('levelRadio',false , i, i);
	}
    } else {
	getData(val);
    }

}
function renderChunk() {
    let inputLevel = parseInt(document.getElementById("level").innerText);
    let val = document.getElementById("chunk").innerText;
    let obj = document.getElementById('chart1');
    console.time('fetch');
    if (obj != null) obj.remove()
    fetch('http://localhost:8000/getAllDataForChunk', {
	method: "POST",
	body: JSON.stringify({plot_type: 'rats_all_levels', max_x_values: 10_000_000, chunk_number: parseInt(val), level: inputLevel})
    }).then(res => res.json()).then(json => {
	console.timeEnd('fetch')
	 console.log(json);
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
		}
	    ],
	};
	let uplot = new uPlot(opts,json.data, document.getElementById('graph'));
    })
}
function renderNextChunk(direction) {
    let inputLevel = parseInt(document.getElementById("level").innerText);
    if(direction == 'forward' && document.getElementById("chunk").innerText != document.getElementById("num-chunks").innerText) {
	document.getElementById('chunk').innerText = parseInt(document.getElementById('chunk').innerText) + 1
	currentChunk = document.getElementById('chunk').innerText;
	
	renderChunk();
    }
    if(direction == 'backward' && document.getElementById('chunk').innerText != "0") {
	document.getElementById('chunk').innerText = parseInt(document.getElementById('chunk').innerText) - 1
	currentChunk = document.getElementById('chunk').innerText;
	
	renderChunk();
	
    }


}
function createRadioElement(name, checked, id, lbl, lbl_prefix = 'level', onclick_value = true, root_div = 'levels', child_div = 'radio-fragment') {
    if(document.getElementById(child_div) == null) {
	// console.log(root_div);
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
	body: JSON.stringify({plot_type: 'test_all_levels', max_x_values: 10_000_000, level: inputLevel})
    })
	.then(res => res.json())
	.then(json => {
	    // console.log(json);
	    document.getElementById('num-levels').innerText = json.num_levels;
	    document.getElementById('chunk').innerText = 0;
	    // console.log("JSON NUM_CHUNKS");
	    // console.log(json.num_chunks);
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
			label: "Rat healthy",
			stroke: "black",
			width: 1,
			fill: "rgba(0, 0, 0, 0)",
		    },

		],
	    };
	    let vals = json.data;

	    let dat = []
	    let uplot = new uPlot(opts,vals,document.getElementById('graph'));
	    let pts = Array.from(uplot.root.querySelectorAll(".u-cursor-pt"));
	    for(let i = 0; i <= 4; i++) {
		if(i == json.level) createRadioElement('levelRadio', true, i, i);
		else createRadioElement('levelRadio',false , i, i);
	    }
	    pts.forEach((pt, i) => {
		pt.onclick = e => {
		    
  		  const seriesIdx = i+1;
		  const dataIdx = uplot.cursor.idx;
		  const xVal = uplot.data[        0][dataIdx];
		  const yVal = uplot.data[seriesIdx][dataIdx];
		    dat.push([xVal, yVal]);
		    document.getElementById("myUL").innerHTML = `(${xVal}, ${yVal}) `
		    var span = document.getElementById('foo');
		    var txt = document.createTextNode("\u00D7");
		    span.className = "close";
		    span.appendChild(txt);
		    
		    span.onclick = function() {
			document.getElementById('myUL').innerText = null;
			document.getElementById('foo').innerText = null;
		    }
		  
		}
	    })
	})
}


getData(maxLevel);
