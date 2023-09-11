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
            await onBlobReady(blob);            
            this.closeMediaRecorder();
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
    constructor(recordElement, stopElement, textElement) { 
        this.recordElement = $(recordElement);
        this.stopElement = $(stopElement);
        this.textElement = $(textElement);        
    }
    
    setText(text) { this.textElement.val(text); }
    
    setDefault() {
        this.stopElement.addClass('dn').removeClass('flex');
        this.recordElement.addClass('flex').removeClass('dn animated');
    }
    
    setRecording() {
        this.recordElement.addClass('dn').removeClass('flex');
        this.stopElement.addClass('flex').removeClass('dn');
    }
    
    setWaiting() {
        this.stopElement.addClass('dn').removeClass('flex');
        this.recordElement.addClass('flex animated').removeClass('dn');
    }
}


axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const button = new RecordWidget('#record-button', '#stop-button', '#text-container > textarea');
const recorder = new AudioRecorder('audio/ogg');


async function sendAudio(blob, url, filename = "audio.ogg") {
    let formData = new FormData();
    formData.append("audio", blob, filename);
    try {
        let response =  await axios.post(url, formData, {headers: {'Content-Type': 'multipart/form-data'}})
        button.setText(response.data.text);
        button.setDefault();
    } 
    catch (error) { 
        throw new ServerResponseError(error.response.data.message) 
    }    
}


button.recordElement.click(
    async () => {
        await recorder.start(
            blob => sendAudio(blob, "/api/speech/stt", "audio.ogg")
        );
        button.setRecording();
    })

button.stopElement.click(
    async () => {
        await recorder.stop();
        button.setWaiting();
    })

