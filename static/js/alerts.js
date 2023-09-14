class AlertLevel {
  static SUCCESS = new AlertLevel("success");
  static ERROR =   new AlertLevel("error");
  static WARNING = new AlertLevel("warning")
  static DEBUG =   new AlertLevel("debug");
  static INFO =    new AlertLevel("info");
  
  constructor(name) { this.name = name; }
}


function log(message, level=AlertLevel.INFO) {
  switch (level) {
      case AlertLevel.ERROR:
      case AlertLevel.DEBUG:
          console[level.name](message);
          break;
      case AlertLevel.WARNING:
          console.warn(message);
          break;
      default:
          console.log(message);
  }
}

function showAlert(message, level=AlertLevel.INFO) {
    log(message, level);
    
    $("#alert-box > #alert-list").append(
        `
          <div class="alert alert-${level.name} mv1 pa1 flex">
            <div class="w-100 tc pl-2">${message}</div>
            <a class="alert-close-button w2 tc _ml-auto pointer dark-gray" 
               aria-label="Close ${level.name} alert box" onclick="closeAlert(this)">×</a>
          </div>
        `
    );
}

function showErrorAlert(message) { showAlert(message, AlertLevel.ERROR) }
function showWarningAlert(message) { showAlert(message, AlertLevel.WARNING) }
function showInfoAlert(message) { showAlert(message, AlertLevel.INFO) }
function showDebugAlert(message) { showAlert(message, AlertLevel.DEBUG) }

function closeAlert(element) { element.parentNode.remove() }
