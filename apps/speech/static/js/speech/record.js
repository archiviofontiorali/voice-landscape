class AudioRecorderError extends Error {
  constructor(message) {
    super(message);
    this.name = "RecordError";
  }
}

class AlreadyRecordingError extends AudioRecorderError {
  constructor(message) {
    super(message);
    this.name = "AlreadyRecordingError";
  }
}

class UnavailableUserMediaError extends AudioRecorderError {
  constructor(message) {
    super(message);
    this.name = "UnavailableUserMediaError";
  }
}

class ServerResponseError extends Error {
  constructor(message) {
    super(message);
    this.name = "ServerResponseError";
  }
}


async function getLegacyUserMedia(constraints) {
    let api = 
        navigator.getUserMedia || 
        navigator.webkitGetUserMedia || 
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia;
    
    if (!api) 
        throw new UnavailableUserMediaError();
    
    return new Promise(
        function (resolve, reject) {
            api.bind(window.navigator)(constraints, resolve, reject);
        });
}


class AudioRecorder {
    constructor() {
        this.constraints = {audio: true, video: false};
        this.options = {type: "audio", mimeType: 'audio/ogg;codecs=opus'};
        this.recorder = null;
        this.chunks = [];
    }
    
    async getMediaStream() {
        // if (!window.navigator.mediaDevices)          
        //     return getLegacyUserMedia(constraints);
        return window.navigator.mediaDevices.getUserMedia(this.constraints);
    }
    
    async getMediaRecorder(onBlobReady) {
        const stream = await  this.getMediaStream();
        const recorder = new MediaRecorder(stream, this.options);
        recorder.ondataavailable = (event) => this.chunks.push(event.data)
        recorder.onstop = async () => {
            let blob = new Blob(this.chunks, {type: 'audio/ogg;codecs=opus'});
            this.closeMediaRecorder();
            await onBlobReady(blob);
        }
        return recorder
    }
    
    closeMediaStream() {
        if (this.recorder)
            this.recorder.stream.getTracks().forEach(track => track.stop())
    }
    
    closeMediaRecorder() {
        this.closeMediaStream();
        this.chunks = [];
        this.recorder = null;
    }
    
    async start(onBlobReady) {
        if (this.recorder && this.recorder.state === "recording")
            throw new AlreadyRecordingError()
        
        this.recorder = await this.getMediaRecorder(onBlobReady);
        this.recorder.start();
    }
    
    async stop() {
        if (this.recorder && this.recorder.state !== "inactive")
            this.recorder.stop();
    }
    
    get state() { return (this.recorder) ? this.recorder.state : "inactive" }

}


class RecordWidget {    
    constructor(recordButton, stopButton, waitButton, textElement, recorder, url) { 
        this.recordButton = $(recordButton);
        this.stopButton = $(stopButton);
        this.waitButton = $(waitButton);
        this.textElement = $(textElement);
        
        this.recorder = recorder;
        this.timeout = null;
        
        this.recordButton.click(() => this.start());
        this.stopButton.click(() => this.stop());
        
        this.url = url
    }
    
    setText(text) { this.textElement.val(text); }
    
    setDefault() {
        this.recordButton.addClass('flex').removeClass('dn');
        this.stopButton.addClass('dn').removeClass('flex');
        this.waitButton.addClass('dn').removeClass('flex');
    }
    
    setRecording() {
        this.recordButton.addClass('dn').removeClass('flex');
        this.stopButton.addClass('flex').removeClass('dn');
        this.waitButton.addClass('dn').removeClass('flex');
    }
    
    setWaiting() {
        this.recordButton.addClass('dn').removeClass('flex');
        this.stopButton.addClass('dn').removeClass('flex');
        this.waitButton.addClass('flex').removeClass('dn');
    }
    
    async sendAudio(blob, url, filename = "audio.ogg") {
        let formData = new FormData();
        formData.append("audio", blob, filename);
        try {
            let response = await axios.post(
                url, 
                formData, 
                {
                    headers: {'Content-Type': 'multipart/form-data'},
                    signal: AbortSignal.timeout(3000),
                    timeout: 10000,
                }
            );
            this.setText(response.data.text);
            this.setDefault();
        }
        catch (error) { 
            throw new ServerResponseError(error.response.data.message) 
        }    
    }
    
    async start() {
        this.setRecording();
        this.timeout = setTimeout(() => this.stop(), 30000);
        await this.recorder.start(blob => this.sendAudio(blob, this.url, "audio.ogg"));
    }
    
    async stop() {
        await this.recorder.stop();
        clearTimeout(this.timeout);
        this.setWaiting();
    }
}

