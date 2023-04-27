const config = { type: "audio", mimeType: "audio/wav" };
const constrains = { audio: true, video: false };
let recorder;

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const recordButton = $('#record-button');
const stopButton = $('#stop-button');

function animateControls() {
  recordButton.toggleClass('dn flex');
  stopButton.toggleClass('dn flex');
}

function onDataAvailable(blob) {
  let formData = new FormData();
  formData.append("audio", blob, "audio.wav")
  
  axios.post("/api/speech/stt", formData, {headers: {'Content-Type': 'multipart/form-data'}})
      .then(response => $('#text-container > textarea').val(response.data.text))
      .catch(error => showErrorAlert(error.response.data.message));
}

function startRecording() {
  if(!navigator.mediaDevices)
    showErrorAlert("Audio recording is not supported by this browser.");
  else 
    navigator.mediaDevices.getUserMedia(constrains)
      .then(function(stream) {
        recorder = RecordRTC(stream, config);
        recorder.startRecording();
        animateControls();
      })
      .catch(error => showErrorAlert(error));
}

function stopRecording() {
  if (recorder.state !== "recording") return
  setTimeout(() => {
    recorder.stopRecording(() => onDataAvailable(recorder.getBlob()));
    animateControls();  
  }, 300)
}

recordButton.click(startRecording)
stopButton.click(stopRecording)