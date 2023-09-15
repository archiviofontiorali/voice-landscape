class SpeechToText {    
    constructor(
        button, output, 
        url = "/api/speech/stt", mimeType = "audio/webm", timeout = 5000
    ) {
        this.button = $(button);
        this.output = $(output);
        this.url = url;
        
        this.chunks = []
        this.timeout = timeout;
        
        this.mimeType = mimeType;
        
        this.setIdle();
    }
    
    async _openStream() {
        if(!window.navigator || !window.navigator.mediaDevices)
            throw "mediaDevices not available on your device"
        
        console.info("Starting MediaStream with getUserMedia")
        return await window.navigator.mediaDevices.getUserMedia(
            {audio: true, video: false}
        );
    }
    
    setIdle() {
        this.button.attr("data-speech", "idle");
        this.button.off("click"); this.button.click(() => this.record());
    }
    
    setRecording() {
        console.log("Start recording")
        this.button.attr("data-speech", "recording")
        
        const timeout = setTimeout(() => this.stop(), this.timeout);
        this.button.off(); 
        this.button.click(async () => { clearTimeout(timeout); await this.stop(); });
    }
    
    async record() {
        if (this.recorder instanceof MediaRecorder) {
            console.warn(`Recorder is not ready to take other audio`)
            return
        }            
        
        try {
            // Open stream and create recorder
            const stream = await this._openStream();
            this.recorder = new MediaRecorder(stream, { mimeType: this.mimeType });
            this.recorder.ondataavailable = (e) => this.chunks.push(e.data)
            
            this.recorder.onstop = async () => {
                this.closeStreams();
                
                console.log("Hanfling audio data with `ondataready`");
                let blob = new Blob(this.chunks, { type: this.mimeType });
                await this.transcribe(blob);
                
                this.clean();
            }
                        
            // Start recording
            this.recorder.start();
            this.setRecording();
        } 
        catch (error) { 
            console.error(error);
            this.closeStreams();
            this.clean();
        }
    }
    
    async stop() {
        if (!(this.recorder instanceof MediaRecorder)) {
            console.error(`this.recorder is not a valid MediaRecorder`);
            return
        }
            
        this.recorder.stop(); 
        this.setIdle(); 
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
            
            if (response.status === 200 && response.data)             
                this.output.val(response.data.text);
        } 
        catch (error) { console.error(error) }    
        finally { this.setIdle() }
    }
        
    closeStreams() {
        if (!(this.recorder instanceof MediaRecorder)) return;
        
        console.info("Closing MediaStream");
        this.recorder.stream.getTracks().forEach(track => track.stop());    
    }
    
    clean() { this.recorder = undefined; this.chunks = []; }
}


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";



