const CENTER_COORDINATES = [44.64686795312118, 10.925334855944921]

const wordCloudOptions = { 
  backgroundColor: "rgba(255, 255, 255, 0)", 
  shrinkToFit: true,
  minSize: '1rem',
  weightFactor: 15,
  fontWeight: 'bold',
  fontFamily: "Consolas, monaco, monospace",
  color: "black",
};


function initMap(
    places, 
    centerCoordinates = CENTER_COORDINATES, 
    initialZoom = 16,
    minZoom = 15,
    maxZoom = 19
) {
  const minWidth = 100, maxWidth = 400;
  const zoomRatio = (maxWidth - minWidth) / (maxZoom - minZoom);
  
  const map = L.map('map').setView(centerCoordinates, initialZoom);
  
  const bgOptions = {minZoom: minZoom, maxZoom: maxZoom}
  L.tileLayer.provider('Stamen.TonerBackground', bgOptions).addTo(map);
    
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
    let width = minWidth + zoomRatio * (map.getZoom() - minZoom);
    let height = width / 2;
    $("#map .word-cloud canvas").css({
      width: `${width}px`, height: `${height}px`,
      "margin-left": `-${width / 2}px`, "margin-top": `-${height / 2}px`
    });
  }

  setMarkersWidth()
  map.on('zoomend', () => setMarkersWidth());
  
}





