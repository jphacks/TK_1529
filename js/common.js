
$('#searchform').keypress( function (e){$("#search").trigger("click");});
$("#search").click( function(){
	$("#panel").empty();
	$.ajax({
		type: 'POST',
		    url: 'cgi-bin/main_cgi.py',
		    async: true,
		    data: {query:$("#searchform").val()},
		    dataType: "json",
		    error: function (e){$("#panel").empty().append("<p id='catchphrase'>残念。<br>つながりが、<br>見つからない！</p>");},
		    success:  function(graph) {
		    var w = 800;
		    var h = 650;
		    var nodes = graph.nodes;
		    var links = graph.links;
		    var force = d3.layout.force()
			.nodes(nodes)
			.links(links)
			.size([w, h])
			.linkDistance(30)
			.linkStrength(0.7)
			.charge(-400)
			.gravity(0.1)
			.alpha(0.1)
			.start();

		    var svg = d3.select("#panel").append("svg").attr({width:w, height:h});
		    var link = svg.selectAll("line")
			.data(links)
			.enter()
			.append("line")
			.style({"stroke": "#0cc",
				"length":1,
				"stroke-width": 3});
		    var node = svg.selectAll("circle")
			.data(nodes)
			.enter()
			.append("circle")
			.attr("r",function(d){ if(d.name == "info"){return 5;}
				else{ return 30;}})
			.attr("opacity",function(d){ if(d.name == "info"){return 1;}
				else{ return 0.6;}})
			.attr("fill",function(d){ if(d.name == "info"){return "blue";}
				else{ return "red"}})
			.call(force.drag);

                        node
                            .on("mouseover", function(d){
				    if(d.name == "info" ){
					$("#tooltip1").css("visibility","visible")
					    .css("top","20%")
					    .css("left","10%")
					    .empty()
					    .append(
						    "<h3><a style='color: black' href ='" + d.url + "'>" + d.title + "</a></h3>"+"<hr>"+d.sentence);}
				    else{
					$("#tooltip2").css("visibility","visible")
					    .css("top","20%")
					    .css("left","70%")
					    .empty()
					    .append(
						    "<h3><a style='color: black' href ='" + d.url + "'>" + d.title + "</a></h3>"+"<hr>"+d.sentence);}
                                })
			    .on("dblclick",function(d){
				    if (d.name != "info"){
					$("#searchform").val(d.name);
					$("#search").trigger("click");
				    }
				});
                        var label = svg.selectAll('text')
                            .data(nodes)
                            .enter()
                            .append('text')
                            .attr({"text-anchor":"middle",
				   "fill":"white"})
                            .style({"font-size":10,
                                    "font-weight":"bold"})
                            .text(function(d){ if(d.name != "info"){return d.name;}});

                        force.on("tick", function() {
				link.attr({x1: function(d) { return d.source.x; },
					    y1: function(d) { return d.source.y; },
					    x2: function(d) { return d.target.x; },
					    y2: function(d) { return d.target.y; }});
				node.attr({cx: function(d) { return d.x; },
					    cy: function(d) { return d.y; }});
				label.attr({x: function(d) { return d.x; },
					    y: function(d) { return d.y; }})});
		}});
    });
$("body").click(function(){$("#tooltip1").css("visibility","hidden");});
$("body").click(function(){$("#tooltip2").css("visibility","hidden");});
