class MediaDeviceNotAvailableError extends Error {
    constructor(message) {
        super(message)
        this.name = "MediaDeviceNotAvailableError"
    }
}


class SpeechToText {    
    constructor(
        button, output, 
        url = "/api/speech/stt", mimeType = "audio/webm", timeout = 30000
    ) {
        this.button = $(button);
        this.output = $(output);
        this.url = url;
        
        this.chunks = []
        this.timeout = timeout;
        
        this.mimeType = mimeType;
        
        this.setIdle();
    }
    
    async record() {
        if (this.recorder instanceof MediaRecorder) {
            console.warn(`Recorder is not ready to take other audio`)
            return
        }            
        
        try {
            // Open stream and create recorder
            const stream = await this.openStream();

            this.recorder = new MediaRecorder(stream, { mimeType: this.mimeType });
            this.recorder.ondataavailable = (e) => this.chunks.push(e.data)
            
            this.recorder.onstop = async () => {
                this.closeStreams();
                this.setWaiting();
                
                console.log("Transcribe audio data from server");
                let blob = new Blob(this.chunks, { type: this.mimeType });
                await this.transcribe(blob);
                
                this.clean();
                this.setIdle();
            }
                        
            // Start recording
            this.recorder.start();
            this.setRecording();
        } 
        catch (error) {            
            this.closeStreams();
            this.clean();
            
            if(error.name === "NotAllowedError"|| error.name === "NotFoundError" ||
               error.name === "MediaDeviceNotAvailableError") {
                this.setIdle();  
                showErrorAlert("Il tuo dispositivo non è supportato o devi abilitare " +
                               "i permessi per la geolocalizzazione")
                return;
            }
            
            this.setIdle(); 
            showErrorAlert(error);
        }
    }
    
    async openStream() {
        if(!window.navigator || !window.navigator.mediaDevices) {
            showErrorAlert("Il tuo dispositivo non è compatibile con la funzione di " +
                           "trascrizione automatica")
            throw MediaDeviceNotAvailableError("navigator.mediaDevice not available")
        }   
        
        console.info("Starting MediaStream with getUserMedia")
        return await window.navigator.mediaDevices.getUserMedia(
            {audio: true, video: false}
        );
    }
    
    closeStreams() {
        if (!(this.recorder instanceof MediaRecorder)) return;
        
        console.info("Closing MediaStream");
        this.recorder.stream.getTracks().forEach(track => track.stop());    
    }
    
    setRecording() {
        console.log("Start recording")
        this.button.attr("data-speech", "recording")
        
        const timeout = setTimeout(() => this.stop(), this.timeout);
        this.button.off("click"); 
        this.button.click(async () => { clearTimeout(timeout); await this.stop(); });
    }
    
    setWaiting() {
        this.button.attr("data-speech", "waiting")
        this.button.removeClass("grow").off("click")
    }
    
    setIdle() {
        this.button.attr("data-speech", "idle");
        this.button.off("click").click(() => this.record());
    }
    
    setDisabled() {
        this.button.attr("data-speech", "disabled")
        this.button.removeClass("grow").off("click")
    }
    
    handleResponse(text) {
        if (!text) {
            alert(`Non siamo riusciti a trascrivere la tua voce, riprova!`);
            return;
        }
        
        if(!this.output.val() ||
           confirm(`Trascrizione:\n\n${text}\n\nVuoi sostituirlo al messaggio attuale?`)) 
            this.output.val(text);
            
    }

    async transcribe(blob) {
        const request = new FormData();
        
        request.append("audio", blob);
        request.append("media_type", this.mimeType);
        
        const options = {
            headers: {'Content-Type': 'multipart/form-data'},
            signal: AbortSignal.timeout(5000),
            timeout: 30000,
        };
        
        try {
            const response = await axios.post(this.url, request, options);
            this.handleResponse(response.data.text);
        } 
        catch (error) { 
            alert("Trascrizione fallita");
            console.error(error);
        }
        finally { 
            this.clean(); 
            this.setIdle(); 
        }        
    }
    
    async stop() {
        if (!(this.recorder instanceof MediaRecorder)) {
            console.error(`this.recorder is not a valid MediaRecorder`);
            return;
        }
            
        this.recorder.stop();
        this.setIdle();
    }
    
    clean() { this.recorder = undefined; this.chunks = []; }
}


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";



