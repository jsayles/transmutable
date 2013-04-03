var transmutable = transmutable || {};

transmutable.initSearch = function(){
	var searchTerms = $("#search-terms");
	
	$( "#search-overlay" ).dialog({
		autoOpen: false,
		height: 95,
		width: 350,
		title: 'Search',
	});

	var searchTrigger = $('<a style="position: absolute; display: none; width: 0px; height: 0px;" href="." accesskey="f">search</a>');
	searchTrigger.click(function(){
		console.log("Searching");
		$("#search-overlay").dialog( "open" );
		return false;
	});
	$('body').append(searchTrigger);
};