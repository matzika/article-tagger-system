
var tags = [];
var people = [];
var orgs = [];
var locations = [];
var concepts = [];
var added_tags = [];
var selected_tags = [];
var start = 0; 
var STEP_COEFF = 15;

tag_flag = "people";

$(function() {
	$("#article").click(function(){
		$("#article").html("");
	});

	$("#loader-button").click(function(){
	    load_more();
	});

	$('textarea').bind('input propertychange', function() {
		console.log("Load new tags");
		$("#suggested-tags").empty();
		$("#selected-tags").empty();
		tags = [];
		selected_tags = [];
		start=0;
		step = STEP_COEFF;
		data = this.value;
		var urlToSearch = "search/";

		$.ajax({
	      url: urlToSearch,
	      cache: true,
	      data: data,
	      type: "POST",
	      crossDomain:true,
	      error: function() {
	         $('#info').html('<p>An error has occurred</p>');
	      },
	      success: function(data) {
	      	var json = JSON.parse(data);
	      	tags = json["tags"];

	      	people = tags["people"];
	      	orgs = tags["organizations"];
	      	locations = tags["locations"];
	      	concepts = tags["concepts"];

	      	console.log(concepts.length);

	      	document.getElementById("people").checked = true;
	      	show_tags("people");
	      },
	   	});
	});

	$('#people').change(function() {
		start = 0;
		step = STEP_COEFF;
		$('#suggested-tags').empty();
		if ($(this).prop('checked')) {
			document.getElementById("orgs").checked = false;
			document.getElementById("locations").checked = false;
			document.getElementById("categories").checked = false;
			show_tags("people");
		}
	});

	$('#orgs').change(function() {
		start = 0;
		step = STEP_COEFF;
		$('#suggested-tags').empty();
		if ($(this).prop('checked')) {
			document.getElementById("people").checked = false;
			document.getElementById("locations").checked = false;
			document.getElementById("categories").checked = false;
			show_tags("orgs");
		}
	});

	$('#locations').change(function() {
		start = 0;
		step = STEP_COEFF;
		$('#suggested-tags').empty();
		if ($(this).prop('checked')) {
			document.getElementById("people").checked = false;
			document.getElementById("orgs").checked = false;
			document.getElementById("categories").checked = false;
			show_tags("locations");
		}
	});

	$('#categories').change(function() {
		start = 0;
		step = STEP_COEFF;
		$('#suggested-tags').empty();
		if ($(this).prop('checked')) {
			document.getElementById("people").checked = false;
			document.getElementById("orgs").checked = false;
			document.getElementById("locations").checked = false;
			show_tags("categories");
		}
	});
});

function show_tags(category) {

	if(category === "people") {
		tag_flag = "people";
		
		for(i = start; i < people.length; i++) {
			var parts = people[i].split("_");
			var show_tag = parts.join(" ");
	  		show_tag = show_tag.replace("._",". ");
	  		show_tag = capitalize(show_tag);
	  		var real_tag = people[i].replace(".","");
	  		$("#suggested-tags").append("<div class=\"tag\" id=\""+real_tag+"\" class=\"ui-widget-content\" onclick=\"select_tag()\" style=\"background: #a5d7a7;border-color:#1f9b23;\">" + show_tag + "</div>");
	  		if(selected_tags.indexOf(real_tag) >= 0)
	  			$( "#"+real_tag ).css("background-color", '#29cb8c');
	  		adjust_tag_width(String(real_tag));
	  		if(i == (step))
	  			break;
	    }
	}

	else if(category === "orgs") {
		tag_flag = "orgs";
		
		for(i = start; i < orgs.length; i++) {
			var parts = orgs[i].split("_");
			var show_tag = parts.join(" ");
	  		show_tag = show_tag.replace("._",". ");
	  		show_tag = capitalize(show_tag);
	  		var real_tag = orgs[i].replace(".","");
	  		$("#suggested-tags").append("<div class=\"tag\" id=\""+real_tag+"\" class=\"ui-widget-content\" onclick=\"select_tag()\" style=\"background: #63B8FF;border-color:#00C5CD;\">" + show_tag + "</div>");
	  		if(selected_tags.indexOf(real_tag) >= 0)
	  			$( "#"+real_tag ).css("background-color", '#33A1C9');
	  		adjust_tag_width(String(real_tag));
	  		if(i == (step))
	  			break;
	    }
	}

	else if(category === "locations") {
		tag_flag = "locations";
		
		for(i = start; i < locations.length; i++) {
	  		var parts = locations[i].split("_");
			var show_tag = parts.join(" ");
	  		show_tag = show_tag.replace("._",". ");
	  		show_tag = capitalize(show_tag);
	  		var real_tag = locations[i].replace(".","");
	  		$("#suggested-tags").append("<div class=\"tag\" id=\""+real_tag+"\" class=\"ui-widget-content\" onclick=\"select_tag()\" style=\"background: #FFD700; border-color:#EE9A00;\">" + show_tag + "</div>");
	  		if(selected_tags.indexOf(real_tag) >= 0)
	  			$( "#"+real_tag ).css("background-color", '#CD8500');
	  		adjust_tag_width(String(real_tag));
	  		if(i == (step))
	  			break;
	    }
	}

	else if(category === "categories") {
		tag_flag = "categories";
		
		for(i = start; i < concepts.length; i++) {
	  		var parts = concepts[i].split("_");
			var show_tag = parts.join(" ");
	  		show_tag = show_tag.replace("._",". ");
	  		show_tag = capitalize(show_tag);
	  		var real_tag = concepts[i].replace(".","");
	  		$("#suggested-tags").append("<div class=\"tag\" id=\""+real_tag+"\" class=\"ui-widget-content\" onclick=\"select_tag()\" style=\"background: #FFC1C1; border-color:#A52A2A;\">" + show_tag + "</div>");
	  		if(selected_tags.indexOf(real_tag) >= 0)
	  			$( "#"+real_tag ).css("background-color", '#EE5C42');
	  		
	  		adjust_tag_width(String(real_tag));
	  		if(i == (step))
	  			break;
	    }
	}
}

function delete_tag() {
	var target_id = event.target.id;
	var selected_tag = target_id.replace("-sel","");
	if($.inArray(selected_tag, selected_tags) >= 0){
		index = -1;
		for(i = 0; i < selected_tags.length; i++){
			if(selected_tags[i] == selected_tag)
				index = i;
		}
		
		selected_tags.splice(index, 1);
	}
	if(tag_flag === "people")
		$( "#"+selected_tag).css("background-color", '#a5d7a7');
	else if(tag_flag === "orgs")
		$( "#"+selected_tag).css("background-color", '#63B8FF');
	else if(tag_flag === "locations")
		$( "#"+selected_tag).css("background-color", '#EE9A00');
	else if(tag_flag === "categories")
		$( "#"+selected_tag).css("background-color", '#A52A2A');
	return (elem=document.getElementById("selected-tags")).removeChild(document.getElementById(target_id));
}

function select_tag() {
	var target_id = event.target.id;
	if($.inArray(target_id, selected_tags) >= 0) //if already a selected tag
		return;
	selected_tags.push(target_id);
	var selected_tag = event.target.id+"-sel";

	var show_tag = target_id.replace("_"," ");
	show_tag = show_tag.replace("._",". ");
	show_tag = capitalize(show_tag);

	if(tag_flag === "people"){
		$( "#selected-tags" ).append("<div class=\"tag\" id=\""+selected_tag+"\" class=\"ui-widget-content\" onclick=\"delete_tag()\">" + show_tag + "</div>");
	
		$( "#"+target_id ).css("background-color", '#29cb8c');
		$( "#"+selected_tag).css("background-color", '#29cb8c');
	}
	else if (tag_flag === "orgs") {
		$( "#selected-tags" ).append("<div class=\"tag\" id=\""+selected_tag+"\" class=\"ui-widget-content\" onclick=\"delete_tag()\">" + show_tag + "</div>");
	
		$( "#"+target_id ).css("background-color", '#33A1C9');
		$( "#"+selected_tag).css("background-color", '#33A1C9');
	}
	else if (tag_flag === "locations") {
		$( "#selected-tags" ).append("<div class=\"tag\" id=\""+selected_tag+"\" class=\"ui-widget-content\" onclick=\"delete_tag()\">" + show_tag + "</div>");
	
		$( "#"+target_id ).css("background-color", '#CD8500');
		$( "#"+selected_tag).css("background-color", '#CD8500');
	}
	else if (tag_flag === "categories") {
		$( "#selected-tags" ).append("<div class=\"tag\" id=\""+selected_tag+"\" class=\"ui-widget-content\" onclick=\"delete_tag()\">" + show_tag + "</div>");
	
		$( "#"+target_id ).css("background-color", '#EE5C42');
		$( "#"+selected_tag).css("background-color", '#EE5C42');
	}
		

	adjust_tag_width(String(selected_tag));
}

function add_tag() {
	var added_tag = jQuery("#add-tag-area").val();
	$( "#selected-tags" ).append("<div class=\"tag\" id=\""+added_tag+"\" class=\"ui-widget-content\">" + added_tag + "</div>");
	adjust_tag_width(String(added_tag));
	$( "#"+added_tag).css("background-color", '#EEE685');
}

function remove_tag(id) {
	var elem=document.getElementById(id);
	var parent = elem.parentNode;
	parent.removeChild(elem);
    //return (elem=document.getElementById(id)).parentNode.removeChild(elem);
}

function load_more() {

	start = step + 1;
	step += start;

    if(tag_flag === "people")
    	show_tags("people")
    if(tag_flag === "orgs")
    	show_tags("orgs")
    if(tag_flag === "locations")
    	show_tags("locations")
    if(tag_flag === "categories")
    	show_tags("categories")
    
}

function adjust_tag_width(ID) {
	width = measure_width("#"+ID);
	$("#"+ID).css("width",(width+30));
}

function capitalize(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function measure_width(obj){
	var html_org = $(obj).html();
	var html_calc = '<span>' + html_org + '</span>';
	$(obj).html(html_calc);
	var width = $(obj).find('span:first').width();
	$(obj).html(html_org);
	return width;
}