const provider = "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-background/{z}/{x}/{y}{r}.png";
const tileLayerOptions = { 
  attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  minZoom: 15, maxZoom: 19
};

const initialZoom = 17;
const minWidth = 240, maxWidth = 480;
const zoomRatio = (maxWidth - minWidth) / (tileLayerOptions.maxZoom - tileLayerOptions.minZoom);

const options = { 
  backgroundColor: "rgba(255, 255, 255, 0)", 
  shrinkToFit: true,
  fontFamily: "Consolas, monaco, monospace",
  color: "rgba(0, 0, 0, .8)",
};



function initMap(places) {
  const map = L.map('map').setView([44.6543412, 10.9011459], initialZoom);
  L.tileLayer(provider, tileLayerOptions).addTo(map);  
    
  let canvas, icon;
  
  for(const [index, {coordinates, frequencies}] of places.entries()) {
    icon = L.divIcon({ 
      html: '<canvas></canvas>', 
      className: `word-cloud word-cloud-${index}`, 
      iconSize: null 
    });
    L.marker(coordinates, { icon: icon }).addTo(map);
    let _frequencies = Object.entries(frequencies).map(([w, f]) => [w, f * 64]);
    canvas = $(`#map .word-cloud.word-cloud-${index} canvas`);
    WordCloud(canvas[0], { list: _frequencies, ...options });
  }
  
  function setMarkersWidth() {
    let width = minWidth + zoomRatio * (map.getZoom() - tileLayerOptions.minZoom);
    let height = width / 2;
    $("#map .word-cloud canvas").css({
      width: `${width}px`, height: `${height}px`,
      "margin-left": `-${width / 2}px`, "margin-top": `-${height / 2}px`
    });
  }

  setMarkersWidth()
  map.on('zoomend', () => setMarkersWidth());
  
}





