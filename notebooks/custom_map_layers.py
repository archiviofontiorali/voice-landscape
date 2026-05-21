import marimo

__generated_with = "0.23.6"
app = marimo.App(width="full", sql_output="polars")

with app.setup:
    import marimo as mo
    import pydantic
    import anywidget
    import traitlets


@app.class_definition
class LeafletAnyWidget(anywidget.AnyWidget):
    """Custom AnyWidget that renders a Leaflet map."""

    lat = traitlets.Float(0.0).tag(sync=True)
    lon = traitlets.Float(0.0).tag(sync=True)
    zoom = traitlets.Int(4).tag(sync=True)

    _css = """     
        :host {
            display: block;          /* needed for height to take effect */
            height: 500px;           /* <-- adjust to whatever you want */
            width: 100%;
        }
        
        @import url('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css');
    """

    _esm = """
        import L from "https://esm.sh/leaflet@1.9.4";

        export default {
            render({ model, el }) {
                const container = document.createElement("div");
                container.style.width = "100%";
                container.style.height = "100%";
                el.appendChild(container);

                const map = L.map(container).setView([model.get("lat), model.get("lon")],
                    model.get("zoom")
                });
                
                //L.tileLayer().addTo(map);
                    // "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", 
                    //{
                    //    referrerPolicy: "origin",
                    //    maxZoom: 16,
                    //    tileSize: 256,
                    //}
                    

                const marker = L.marker([model.get("lat"), model.get("lon")]).addTo(map);

                // Update map when Python changes lat/lon
                model.on("change:lat change:lon change:zoom", () => {
                    const lat = model.get("lat");
                    const lon = model.get("lon");
                    const zoom = model.get("zoom");
                    
                    marker.setLatLng([lat, lon]);
                    map.setView([lat, lon], zoom);
                });

                const invalidate = () => { map.invalidateSize(); };
                
                map.whenReady(invalidate);
                const ro = new ResizeObserver(invalidate);
                ro.observe(el);
            }
        };
        """


@app.cell(hide_code=True)
def _():
    _center_options = {
        "New York": (40.7128, -74.0060),
        "London": (51.5074, -0.1278),
        "Tokyo": (35.6895, 139.6917),
        "Sydney": (-33.8688, 151.2093),
    }
    center_selector = mo.ui.dropdown(
        label="Map center",
        options=_center_options,
        value="New York",
    )
    center_selector
    return (center_selector,)


@app.cell
def _(center_selector):
    map_widget = LeafletAnyWidget(
        lat=center_selector.value[0],
        lon=center_selector.value[1],
    )
    map_widget
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
