const DEFAULT_WORDCLOUD_OPTIONS = {
  backgroundColor: "rgba(255, 255, 255, 0)",
  gridSize: 5,
  shrinkToFit: true,
  drawOutOfBound: true,
  minSize: "2rem",
  // weightFactor: (w) => 6 + 20 * Math.tanh(w),
  // weightFactor: (size) => Math.floor(5 + size * (30 - 5)),
  weightFactor: (size) => 12 + Math.pow(size, 2.3),
  fontWeight: "700",
  fontFamily: "Open Sans, Consolas, monaco, monospace",
  color: "inherit",
  shape: "circle",
};

const DEFAULT_LEAFLET_MAP_OPTIONS = {
  zoom: { initial: 15, min: 13, max: 20 },
  map: {
    provider: {
      // url: "https://tiles.stadiamaps.com/tiles/stamen_toner_background/{z}/{x}/{y}{r}.png",
    },
  },
  markers: { minWidth: 100, maxWidth: 200, minHeight: 50, maxHeight: 200 },
  useDOM: false,
};

class WordCloudMarker {
  constructor(index = 0, coordinates = [0, 0], options) {
    this.index = index;
    this.coordinates = coordinates;
    this.options = { ...DEFAULT_WORDCLOUD_OPTIONS, ...options };
  }

  addMarker(map, place) {
    const icon = L.divIcon({
      html: '<div class="canvas relative"></div>',
      className: `word-cloud word-cloud-${this.index}`,
      iconSize: null,
    });
    this.marker = L.marker(this.coordinates, { icon: icon, url: place.url })
      .addTo(map)
      .on("click", function (e) {
        // e.target is the marker; you can store the URL on the marker options
        var url = e.target.options.url; // e.g. set when you create it
        window.location.href = url; // navigate like a normal link
      });
    this.canvas = $(`#map .word-cloud.word-cloud-${this.index} .canvas`);
    return this;
  }

  /** Remove previously generate words */
  emptyCanvas() {
    this.canvas.empty();
    return this;
  }

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
    WordCloud(this.canvas[0], { list: frequencies, ...this.options });
    return this;
  }
}

function buildCircleMarker(size = 24, color = "red") {
  return L.divIcon({
    className: "circle-marker",
    html: `<div style="background:${color};width:20px;height:20px;border-radius:50%;border:2px solid #fff;"></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}

class LeafletMap {
  constructor(
    id = "map",
    center = [0, 0],
    useSimpleCRS = false,
    scale = 1,
    showcase = false,
    overlay = {},
    options = {},
  ) {
    this.center = center;
    this.overlay = overlay;
    this.scale = scale;
    this.showcase = showcase;

    this.options = {
      zoom: { ...DEFAULT_LEAFLET_MAP_OPTIONS.zoom, ...options.zoom },
      map: { ...DEFAULT_LEAFLET_MAP_OPTIONS.map, ...options.map },
      markers: { ...DEFAULT_LEAFLET_MAP_OPTIONS.markers, ...options.markers },
      useDOM: options.useDOM ? options.useDOM : DEFAULT_LEAFLET_MAP_OPTIONS.useDOM,
    };

    const opts = {
      minZoom: this.options.zoom.min,
      maxZoom: this.options.zoom.max,
      zoomControl: !showcase,
      attributionControl: !showcase,
      referrerPolicy: "strict-origin-when-cross-origin",
    };
    if (useSimpleCRS) opts["crs"] = L.CRS.Simple;

    if (overlay.url) {
      opts.maxBounds = [
        [0, 0],
        [overlay.height / this.scale, overlay.width / this.scale],
      ];
    }

    this.map = L.map(id, opts).setView(this.center, this.options.zoom.initial);
    this._addBackground();

    // Enable to see axis and border
    // L.marker([0, 0], { icon: buildCircleMarker() }).addTo(this.map);
    // L.marker([30, 0], { icon: buildCircleMarker() }).addTo(this.map);
    // L.marker([0, 30], { icon: buildCircleMarker() }).addTo(this.map);
    // L.marker([0, overlay.width], { icon: buildCircleMarker() }).addTo(this.map);
    // L.marker([overlay.height, 0], { icon: buildCircleMarker() }).addTo(this.map);

    if (overlay.url) this._addOverlay(overlay, this.scale);

    this.markers = {};

    const { markers, zoom } = this.options;
    this.widthRatio = (markers.maxWidth - markers.minWidth) / (zoom.max - zoom.min);
    this.heightRatio = (markers.maxHeight - markers.minHeight) / (zoom.max - zoom.min);
  }

  _addBackground() {
    const { zoom } = this.options;
    const { name, url } = this.options.map.provider;
    const opts = {
      minZoom: zoom.min,
      maxZoom: zoom.max,
      referrerPolicy: "strict-origin-when-cross-origin",
    };

    if (name) return L.tileLayer.provider(name, opts).addTo(this.map);
    else if (url) return L.tileLayer(url, opts).addTo(this.map);
  }

  _addOverlay(overlay, scale) {
    const bounds = [
      [0, 0],
      [Math.floor(overlay.height / scale), Math.floor(overlay.width / scale)],
    ];
    L.imageOverlay(overlay.url, bounds, { opacity: overlay.opacity }).addTo(this.map);
    // if (this.showcase) this.map.fitBounds(bounds); // WORKAROUND: and it's not working
  }

  _addWordCloud(index, coordinates, frequencies, width, height, place) {
    if ($.isEmptyObject(frequencies)) return;
    if (!width) width = this.markerWidth;
    if (!height) height = this.markerHeight;

    this.markers[index] = new WordCloudMarker(index, coordinates)
      .addMarker(this.map, place)
      .updateCanvas(width, height)
      .updateWords(frequencies);
  }

  _updateWordCloud(index, frequencies, width, height) {
    if ($.isEmptyObject(frequencies)) return;
    if (!width) width = this.markerWidth;
    if (!height) height = this.markerHeight;
    this.markers[index].updateCanvas(width, height).updateWords(frequencies);
  }

  addWordClouds(places) {
    this.places = places;
    const width = this.markerWidth,
      height = this.markerHeight;
    for (const [index, place] of this.places.entries()) {
      const { coordinates, frequencies, url, title } = place;
      const scaledCoordinates = [
        (this.overlay.height - coordinates[0]) / this.scale,
        coordinates[1] / this.scale,
      ];
      L.marker(scaledCoordinates, { icon: buildCircleMarker("blue"), url: url })
        .addTo(this.map)
        .on("click", function (e) {
          // e.target is the marker; you can store the URL on the marker options
          var url = e.target.options.url; // e.g. set when you create it
          window.location.href = url; // navigate like a normal link
        });
      // .bindPopup(title)
      // .on("mouseover", function (e) {
      //   this.openPopup();
      // })
      // .on("mouseout", function (e) {
      //   this.closePopup();
      // });

      this._addWordCloud(index, scaledCoordinates, frequencies, width, height, place);
    }

    this.map.on("zoomend", () => this.updateWordClouds());
    return this;
  }

  updateWordClouds(places) {
    if (places) this.places = places;
    const width = this.markerWidth,
      height = this.markerHeight;
    for (const [index, { frequencies }] of this.places.entries()) {
      this._updateWordCloud(index, frequencies, width, height);
    }
  }

  get markerWidth() {
    const { zoom, markers } = this.options;
    return Math.floor(
      markers.minWidth + this.widthRatio * (this.map.getZoom() - zoom.min),
    );
  }

  get markerHeight() {
    const { zoom, markers } = this.options;
    return Math.floor(
      markers.minHeight + this.heightRatio * (this.map.getZoom() - zoom.min),
    );
  }
}
