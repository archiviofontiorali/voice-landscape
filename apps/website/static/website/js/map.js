const defaultOptions = {
  zoom: { initial: 15, min: 13, max: 20 },
  map: { provider: "Stamen.TonerBackground" },
  markers: {minWidth: 100, maxWidth: 200, minHeight: 50, maxHeight: 200},
  useDOM: false,
}

const wordCloudOptions = { 
  backgroundColor: "rgba(255, 255, 255, 0)", 
  shrinkToFit: true,
  minSize: '2rem',
  weightFactor: size => Math.floor(6 + size * (30-6)),
  fontWeight: '700',
  fontFamily: "Open Sans, Consolas, monaco, monospace",
  color: 'black',
  shape: "circle",
};


function createCanvasMarker(coordinates, index) {
  let icon = L.divIcon({ 
    html: '<div class="canvas relative"></div>',
    className: `word-cloud word-cloud-${index}`, 
    iconSize: null 
  });
  return L.marker(coordinates, { icon: icon })
}


function addWordCloudCanvas(index, markerWidth, markerHeight) {
  let canvas = $(`#map .word-cloud.word-cloud-${index} .canvas`);

  // Remove previously generate words
  canvas.empty();

  // Set width, height
  canvas.css({
    width: `${markerWidth}px`,
    height: `${markerHeight}px`,
    "margin-left": `-${markerWidth / 2}px`, 
    "margin-top": `-${markerHeight / 2}px`,
  });

  return canvas[0]
}


function createMap(centroid = [0., 0.], o) {
  // Generate Map
  const map = L.map('map').setView(centroid, o.zoom.initial);
  
  // Generate Background
  const bgOptions = {minZoom: o.zoom.min, maxZoom: o.zoom.max}
  L.tileLayer.provider(o.map.provider, bgOptions).addTo(map);
  
  return map;  
}


function addWordClouds(map, places, o) {
  // Get marker width
  const widthRatio = (o.markers.maxWidth - o.markers.minWidth) / (o.zoom.max - o.zoom.min);
  function getMarkerWidth() { 
    return Math.floor(o.markers.minWidth + widthRatio * (map.getZoom() - o.zoom.min)); 
  }
  
  // Get marker height
  const heightRatio = (o.markers.maxHeight - o.markers.minHeight) / (o.zoom.max - o.zoom.min);
  function getMarkerHeight() {  
    return Math.floor(o.markers.minHeight + heightRatio * (map.getZoom() - o.zoom.min));
  } 
  
  
  for(const [index, {coordinates, frequencies}] of places.entries()) {
    if ($.isEmptyObject(frequencies))
      continue
    
    createCanvasMarker(coordinates, index).addTo(map);
    let canvas = addWordCloudCanvas(index, getMarkerWidth(), getMarkerHeight());
    
    WordCloud(canvas, {list: frequencies, ...wordCloudOptions});
  }
  
  function updateWordCloudMarkers() {
    for(const [index, {_coordinates, frequencies}] of places.entries()) {
      if ($.isEmptyObject(frequencies))
        continue
      
      let canvas = addWordCloudCanvas(index, getMarkerWidth(), getMarkerHeight());
      WordCloud(canvas, {list: frequencies, ...wordCloudOptions});
    }
  }
  
  map.on('zoomend', () => updateWordCloudMarkers());
}



function initMap(places, centroid = [0., 0.], o) {
  o = {
    zoom: {...defaultOptions.zoom, ...o.zoom },
    map: {...defaultOptions.map, ...o.map },
    markers: {...defaultOptions.markers, ...o.markers },
    useDOM: (o.useDOM) ? o.useDOM : defaultOptions.useDOM,
  }
  
  const map = createMap(centroid, o);
  addWordClouds(map, places, o);
}





