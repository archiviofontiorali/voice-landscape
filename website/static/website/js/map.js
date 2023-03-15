const defaultOptions = {
  zoom: { initial: 15, min: 14, max: 20 },
  map: { provider: "Stamen.TonerBackground" }
}

const wordCloudOptions = { 
  backgroundColor: "rgba(255, 255, 255, 0)", 
  shrinkToFit: true,
  minSize: '1rem',
  weightFactor: 15,
  fontWeight: 'bold',
  fontFamily: "Consolas, monaco, monospace",
  color: "black",
};


function initMap(places, centerCoordinates = [0., 0.], options) {
  options = {
    zoom: {...defaultOptions.zoom, ...options.zoom },
    map: {...defaultOptions.map, ...options.map }
  }
  console.log(options)
  
  const minWidth = 100, maxWidth = 400;
  const zoomRatio = (maxWidth - minWidth) / (options.zoom.max - options.zoom.min);
  
  const map = L.map('map').setView(centerCoordinates, options.zoom.initial);
  
  const bgOptions = {minZoom: options.zoom.min, maxZoom: options.zoom.max}
  L.tileLayer.provider(options.map.provider, bgOptions).addTo(map);
    
  let canvas, icon;
  
  for(const [index, {coordinates, frequencies}] of places.entries()) {
    if ($.isEmptyObject(frequencies)) continue
    // L.marker(coordinates).addTo(map);
    icon = L.divIcon({ 
      html: '<canvas></canvas>', 
      className: `word-cloud word-cloud-${index}`, 
      iconSize: null 
    });
    L.marker(coordinates, { icon: icon }).addTo(map);
    canvas = $(`#map .word-cloud.word-cloud-${index} canvas`);
    WordCloud(canvas[0], { list: Object.entries(frequencies), ...wordCloudOptions });
  }
  
  function setMarkersWidth() {
    let width = minWidth + zoomRatio * (map.getZoom() - options.zoom.min);
    let height = width / 2;
    $("#map .word-cloud canvas").css({
      width: `${width}px`, height: `${height}px`,
      "margin-left": `-${width / 2}px`, "margin-top": `-${height / 2}px`
    });
  }

  setMarkersWidth()
  map.on('zoomend', () => setMarkersWidth());
  
}





