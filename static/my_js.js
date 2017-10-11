var markers = [];
var map = null;


$('#search_form').submit(function( event ) {
    event.preventDefault();
    var select_date = $('#date-picker').val();
    var select_kw = $('#keyword option:selected').text();
    var select_sz = $('#size').val();
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function()
    {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200){
            var return_obj = JSON.parse(xmlHttp.responseText);
            if (return_obj.status === true) {
                mark_search(return_obj.msg)
            }else {
                alert(return_obj.msg)
            }
        }

    };
    xmlHttp.open("GET", "/search?keyword="+select_kw+'&datetime='+select_date+'&size='+select_sz, true);
    xmlHttp.send();
});



function mark_search(tweet_array) {
    remove_markers();
    console.log(tweet_array);

    for(var _i=0;_i<tweet_array.length;_i++){
        var loc = {lat:tweet_array[_i].location[1] , lng: tweet_array[_i].location[0]};
        var marker = new google.maps.Marker({
          position: loc,
          map: map
        });

        var contentString = "<div  style='overflow: hidden;line-height: 1.35;width: 300px;'><div class=\"row\" >\n" +
            "        <div class=\"col-md-3\"><img src=\""+tweet_array[_i].headicon_url+"\"></div>\n" +
            "        <div class=\"col-md-9\"><h5>"+tweet_array[_i].author+"</h5><p>" +tweet_array[_i].created_at +
            "</p></div>\n" +
            "    </div>\n" +
            "    <div class=\"row\" style='width: 300px;word-break: break-all'>\n" +
            "        <div class=\"col-md-12\"><p>"+tweet_array[_i].text+"</p></div>\n" +
            "    </div></div>";


        marker.myinfowindow = new google.maps.InfoWindow({
            content: contentString
        });

        marker.addListener('click', function () {
            this.myinfowindow.open(map, this)
        });

        markers.push(marker);
    }
}


function remove_markers() {
    var prev_len = markers.length;
    for (var _i=0; _i<prev_len; _i++){
        var marker = markers.pop();
        marker.setMap(null)
    }
}


function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: 0, lng: 0},
		zoom: 3,
		disableDoubleClickZoom: true
	});

	map.addListener('click', function(e) {
		var select_lng = e.latLng.lng();
        var select_lat = e.latLng.lat();
        var select_sz = $('#size').val();
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function()
        {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200){
                var return_obj = JSON.parse(xmlHttp.responseText);
                if (return_obj.status === true) {
                    mark_search(return_obj.msg)
                }else {
                    alert(return_obj.msg)
                }
            }
        };
        xmlHttp.open("GET", "/geospatial?select_lng="+select_lng+'&select_lat='+select_lat+'&size='+select_sz, true);
        xmlHttp.send();
  	});
}
