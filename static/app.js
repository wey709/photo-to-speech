
var map;
var marker;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: {lat:latitude, lng:longitude},
    // center: {lat:value[0][0], lng:value[0][1]},
    zoom: 10
  })

  marker = new google.maps.Marker({
  position: {lat:latitude, lng:longitude},
  // position: {lat:value[0][0], lng:value[0][1]},
  map: map
})
}



document.onload = initMap()