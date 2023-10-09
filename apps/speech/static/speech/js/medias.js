const MEDIA_TYPES = [
  'video/webm',
  'audio/webm',
  'video/webm;codecs=vp8',
  'video/webm;codecs=daala',
  'video/webm;codecs=h264',
  'audio/webm;codecs=opus',
  'video/mpeg',
  'audio/ogg',
  'audio/wav',
  'audio/mp4',
  'audio/mp3'
]

function checkSupportedTypes () {
  for (const type of MEDIA_TYPES) {
    if (MediaRecorder.isTypeSupported(type)) {
      showInfoAlert(`${type} is supported`)
    } else {
      showErrorAlert(`${type} is not supported`)
    }
  }
}
