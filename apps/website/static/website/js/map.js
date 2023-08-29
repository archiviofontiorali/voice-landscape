const DEFAULT_WORDCLOUD_OPTIONS = { 
  backgroundColor: "rgba(255, 255, 255, 0)", 
  shrinkToFit: true,
  minSize: '2rem',
  weightFactor: size => Math.floor(6 + size * (30-6)),
  fontWeight: '700',
  fontFamily: "Open Sans, Consolas, monaco, monospace",
  color: 'black',
  shape: "circle",
};


const DEFAULT_LEAFLET_MAP_OPTIONS = {
  zoom: { initial: 15, min: 13, max: 20 },
  map: { provider: { url: 'https://tiles.stadiamaps.com/tiles/stamen_toner_background/{z}/{x}/{y}{r}.png' }},
  markers: {minWidth: 100, maxWidth: 200, minHeight: 50, maxHeight: 200},
  useDOM: false,
}


class WordCloudMarker {  
  constructor(index = 0, coordinates = [0., 0.], options) {
    this.index = index;
    this.coordinates = coordinates;
    this.options = { ...DEFAULT_WORDCLOUD_OPTIONS, ...options };
  }
  
  addMarker(map) {
    const icon = L.divIcon({
      html: '<div class="canvas relative"></div>',
      className: `word-cloud word-cloud-${this.index}`,
      iconSize: null
    });
    this.marker = L.marker(this.coordinates, {icon: icon}).addTo(map)
    this.canvas = $(`#map .word-cloud.word-cloud-${this.index} .canvas`);
    return this;
  }
  
  /** Remove previously generate words */
  emptyCanvas() { this.canvas.empty(); return this; }
  
  /** Update sizes of canvas marker */
  updateCanvas(width, height) {
    this.canvas.css({
      width: `${width}px`,
      height: `${height}px`,
      "margin-left": `-${width / 2}px`, 
      "margin-top": `-${height / 2}px`,
    });
    return this;
  }
  
  updateWords(frequencies) {
    this.emptyCanvas();
    WordCloud(this.canvas[0], {list: frequencies, ...this.options});
    return this;
  }
  
}

class LeafletMap {
  constructor(id = "map", center = [0., 0.], options) {
    this.center = center;
    
    this.options = {
      zoom: {...DEFAULT_LEAFLET_MAP_OPTIONS.zoom, ...options.zoom },
      map: {...DEFAULT_LEAFLET_MAP_OPTIONS.map, ...options.map },
      markers: {...DEFAULT_LEAFLET_MAP_OPTIONS.markers, ...options.markers },
      useDOM: (options.useDOM) ? options.useDOM : DEFAULT_LEAFLET_MAP_OPTIONS.useDOM,
    };
    
    this.map = L.map(id).setView(this.center, this.options.zoom.initial);
    this._addBackground();
    
    this.markers = {};
    
    const { markers, zoom } = this.options;
    this.widthRatio = (markers.maxWidth - markers.minWidth) / (zoom.max - zoom.min);
    this.heightRatio = (markers.maxHeight - markers.minHeight) / (zoom.max - zoom.min);
  }
    
  _addBackground() {
    const {zoom} = this.options;
    const {name, url} = this.options.map.provider;
    const opts = {minZoom: zoom.min, maxZoom: zoom.max}

    if (name)
      return L.tileLayer.provider(name, opts).addTo(this.map);
    else
      return L.tileLayer(url, opts).addTo(this.map);
  }
  
  _addWordCloud(index, coordinates, frequencies, width, height) {
    if ($.isEmptyObject(frequencies)) return
    if (!width) width = this.markerWidth;
    if (!height) height = this.markerHeight;
    
    this.markers[index] = (new WordCloudMarker(index, coordinates))
        .addMarker(this.map)
        .updateCanvas(width, height)
        .updateWords(frequencies);
  }
  
  _updateWordCloud(index, frequencies, width, height) {
    if ($.isEmptyObject(frequencies)) return
    if (!width) width = this.markerWidth;
    if (!height) height = this.markerHeight;
    this.markers[index].updateCanvas(width, height).updateWords(frequencies);
  }
  
  addWordClouds(places) {
    this.places = places;
    const width = this.markerWidth, height = this.markerHeight;
    for(const [index, {coordinates, frequencies}] of this.places.entries()) {
      this._addWordCloud(index, coordinates, frequencies, width, height);
    }
    
    this.map.on('zoomend', () => this.updateWordClouds());
    return this;
  }
  
  updateWordClouds(places) {
    if (places) this.places = places;
    const width = this.markerWidth, height = this.markerHeight;
    for(const [index, {frequencies}] of this.places.entries()) {
      this._updateWordCloud(index, frequencies, width, height);
    }
  }
  
  get markerWidth() {
    const {zoom, markers} = this.options;
    return Math.floor(markers.minWidth + this.widthRatio * (this.map.getZoom() - zoom.min));
  }
  
  get markerHeight() {
    const {zoom, markers} = this.options;
    return Math.floor(markers.minHeight + this.heightRatio * (this.map.getZoom() - zoom.min));
  }
}



