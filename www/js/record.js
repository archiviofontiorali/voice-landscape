const config = { type: "audio", mimeType: "audio/wav" };
const constrains = { audio: true, video: false };
let recorder;

const recordButton = $('#record-button');
const stopButton = $('#stop-button');

function animateControls() {
  recordButton.toggleClass('dn');
  stopButton.toggleClass('dn');
}

function onDataAvailable(blob) {
  let formData = new FormData();
  formData.append("audio", blob, "audio.wav")
  
  axios.post("/api/stt", formData, {headers: {'Content-Type': 'multipart/form-data'}})
      .then(response => $('input#text').val(response.data))
      .catch(error => showErrorAlert(error));
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
  recorder.stopRecording(() => onDataAvailable(recorder.getBlob()));
  animateControls();
}

recordButton.click(startRecording)
stopButton.click(stopRecording)