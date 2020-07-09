//Set global variable for mobile
if (window.innerWidth < 500){
  var mobile = true;
}
else{
  var mobile = false;
}

/* Use to log page events by sending a POST request to server. Can't
log page unload due to asynchronous running - page finishes closing
before the request can receive a response. Use "navigator.sendbeacon"
for unload events instead.
        
:param event_type: (str) - Type of event to log, currently used values are 
"page_load", "page_unload", "page_show", "page_hide", and "click."
:param element_id: (str) Optional element_id, currently used for "click" 
events to identify what was clicked on.  Defaults to "none."  */
function logEvent(event_type, element_id="na") {
  // Send POST request to backend
  fetch(`${window.location}`, {
    method: "POST",
    credentials: "include",
    body: makeData(event_type, element_id),
    cache: 'no-cache',
    headers: new Headers({
      'content-type': 'application/json'})
    });
}
    
/* Use if calling "navigator.sendbeacon" to log an event.  Makes a 
string with the timestamp, event type, and element id which the
server can receive through a POST request and process.

:param event_type: (str) - Type of event to log, currently used values are 
"page_load", "page_unload", "page_show", "page_hide", and "click."
:param element_id: (str) Optional element_id, currently used for "click" 
events to identify what was clicked on.  Defaults to "none." */
function makeData(event_type, element_id="na") 
{
  // Set banner style to "none" value if undefined
  if(typeof banner_style == 'undefined')
  {
    banner_style = 'nobanner';
  }

  // Get time in ms, round to 1/10th second due to browser imprecision
  timestamp = Math.floor(Date.now() / 100 );
  timestamp = timestamp / 10;
  timestamp = String(timestamp);
    
  // Compile parameters into JSON object
  var data = timestamp + ";;;" + event_type + ";;;" + element_id + ";;;" + banner_style + ";;;" + navigator.userAgent + ";;;" + String(mobile);
  return data;
}

// listener for page load
window.addEventListener("load", function(){
  logEvent("page_load")});



// Script to log focus changes

var browserPrefixes = ['moz', 'ms', 'o', 'webkit'],
isVisible = true; // internal flag, defaults to true

// get the correct attribute name
function getHiddenPropertyName(prefix) {
  return (prefix ? prefix + 'Hidden' : 'hidden');
}

// get the correct event name
function getVisibilityEvent(prefix) {
  return (prefix ? prefix : '') + 'visibilitychange';
}

// get current browser vendor prefix
function getBrowserPrefix() {
  for (var i = 0; i < browserPrefixes.length; i++) {
    if(getHiddenPropertyName(browserPrefixes[i]) in document) {
      // return vendor prefix
      return browserPrefixes[i];
    }
  }

  // no vendor prefix needed
  return null;
}

// bind and handle events
var browserPrefix = getBrowserPrefix(),
    hiddenPropertyName = getHiddenPropertyName(browserPrefix),
    visibilityEventName = getVisibilityEvent(browserPrefix);

function onVisible() {
  // prevent double execution
  if(isVisible) {
    return;
  }

  // send page focus event to server
    navigator.sendBeacon(`${window.location}`, 
    makeData("page_focus"));

  // change flag value
  isVisible = true;
}

function onHidden() {
  // prevent double execution
  if(!isVisible) {
    return;
  }
    navigator.sendBeacon(`${window.location}`, 
    makeData("page_blur"));

  // change flag value
  isVisible = false;
}

function handleVisibilityChange(forcedFlag) {
  // forcedFlag is a boolean when this event handler is triggered by a
  // focus or blur eventotherwise it's an Event object
  if(typeof forcedFlag === "boolean") {
    if(forcedFlag) {
      return onVisible();
    }

    return onHidden();
  }

  if(document[hiddenPropertyName]) {
    return onHidden();
  }

  return onVisible();
}

document.addEventListener(visibilityEventName, handleVisibilityChange, false);

// extra event listeners for better behaviour
document.addEventListener('focus', function() {
  handleVisibilityChange(true);
}, false);

document.addEventListener('blur', function() {
  handleVisibilityChange(false);
}, false);

window.addEventListener('focus', function() {
    handleVisibilityChange(true);
}, false);

window.addEventListener('blur', function() {
  handleVisibilityChange(false);
}, false);