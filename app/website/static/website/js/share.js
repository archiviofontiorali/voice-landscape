class Coordinates {
  constructor(latitude, longitude) {
    this.latitude = latitude;
    this.longitude = longitude;
  }
  
  get as_array() { return [this.latitude, this.longitude] }
  get as_string() { return `(${this.latitude}, ${this.longitude})` }
}

function ensureNumberRange(value, a, b) {
    value = Math.max(Number(value), a);
    return Math.min(value, b);
}

class TabWidget {
    constructor(prevButton, nextButton, tabs = 2) {
        this.prevButton = $(prevButton);
        this.nextButton = $(nextButton);
        
        this.first = 0;
        this.last = tabs - 1;
        this.current = this.first;
        
        this.showTab();
        
        this.prevButton.click(() => this.showPrevTab());
        this.nextButton.click(() => this.showNextTab());        
    }
    
    showTab(index = this.current) {        
        this.current = ensureNumberRange(index, this.first, this.last);      
        
        this.nextButton
            .toggleClass("dn", this.current >= this.last)
            .toggleClass("flex", this.current < this.last);
        this.prevButton
            .toggleClass("dn", this.current <= this.first)
            .toggleClass("flex", this.current > this.first);
    
        $("form").children('section.widget-tab').each((index, tab) => {
            $(tab)
              .addClass((this.current === index) ? "flex" : "dn")
              .removeClass((this.current === index) ? "dn" : "flex");
        });
    }
    
    showNextTab() {
        this.showTab(Math.min(this.current + 1, this.last));       
    }
    showPrevTab() { 
        this.showTab(Math.max(this.current - 1, 0));
    }
}

class ShareWidget {
    constructor(latitudeElement, longitudeElement, messageElement, previewElement) {
        this.inputLatitude = $(latitudeElement);
        this.inputLongitude = $(longitudeElement);
        this.inputMessage = $(messageElement);
        this.previewMessage = $(previewElement);
        
        this.buttonSubmit = $("input#submit-button");
        
        this.autoLocationIcon = $("#location-auto-icon svg");
        this.selectPlaceLocation = $(`#location-place select#place`);
        
        this.inputMessage.on("change", () => this.updatePreview());
        this.autoLocationIcon.click(() => this.getAutoPosition());
        this.selectPlaceLocation.on("change", o => this.getPlacePosition(o.value));
    }
    
    resetMessage() {
        this.inputMessage.val('');
        this.updatePreview();
    }
    
    updatePreview() { 
        let text = this.inputMessage.val().trim()
        this.previewMessage.text(text);
        text ? this.enableSubmit() : this.disableSubmit();
    }
    
    enableSubmit() {
        if ($(this.inputMessage).val() && 
            $(this.inputLatitude).val() && 
            $(this.inputLongitude).val())
            this.buttonSubmit.prop("disabled", false);
    }
    disableSubmit() { this.buttonSubmit.prop("disabled", true); }
    
    /** Set coordinates inside respective input tags and display value for user */
    setCoordinates(coords, title='') {
        console.info(`Select coordinates ${coords.as_string}`, coords.as_array);
        this.inputLatitude.val(coords.latitude);
        this.inputLongitude.val(coords.longitude);
        
        $('#location-display-coordinates').text(title ? '' : coords.as_string);
        $('#location-display-title').text(title);
        
        this.enableSubmit();
    }
    
    /** Unset coordinates from input tags and display */
    unsetCoordinates() {
        this.inputLatitude.removeAttr("value");
        this.inputLongitude.removeAttr("value");
        $('#location-display-coordinates').html('&nbsp;');
        $('#location-display-title').text('');
        this.disableSubmit();
    }
    
    getPlacePosition() {        
        const option = this.selectPlaceLocation.find(`option:selected`); 
        if (option.text() === "") { this.unsetCoordinates(); return }
        let coords = new Coordinates(option.data("latitude"), option.data("longitude"));
      
        this.setCoordinates(coords, option.text());
        this.autoLocationIcon.attr("data-state", "waiting")
    }
    
    getAutoPosition() { 
        if (this.autoLocationIcon.attr("data-state") === "processing") 
            return;
        
        this.autoLocationIcon.attr("data-state", "processing")
      
        if (!navigator.geolocation) { 
            showErrorAlert("Geolocation is not supported by this browser.");
            this.autoLocationIcon
                .attr("data-state", "disabled")
                .removeAttr("onclick").removeClass("grow");
            return;
        }
      
        navigator.geolocation.getCurrentPosition(
            position => {
              let coords = new Coordinates(position.coords.latitude, position.coords.longitude);
              this.setCoordinates(coords);
              this.autoLocationIcon.attr("data-state", "success");
            },
            error => { 
              showErrorAlert(error); 
              this.autoLocationIcon.attr("data-state", "error"); 
            }
        );
    }
}