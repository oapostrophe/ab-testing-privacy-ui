/* Use to log page events by sending a POST request to server. Can't
log page unload due to asynchronous running - page finishes closing
before the request can receive a response. Use "logBeacon" for these events
instead.
        
:param eventType: (str) - Type of event to log, currently used values are 
"page_load", "page_unload", "page_blur", "page_focus", "survey_id" and "click."
:param elementId: (str) Optional element_id, currently used for "click" 
events to identify what was clicked on. Default value "na"  */
function logEvent(eventType, elementId="na") {
  // Send POST request to backend
  fetch(`${window.location}`, {
    method: "POST",
    credentials: "include",
    body: makeData(eventType, elementId),
    cache: 'no-cache',
    headers: new Headers({
      'content-type': 'application/json'})
    });
}

/* Use if logging an event that will trigger the page unloading, such as
clicking on a link or closing the page.  Logs event using navigator.sendBeacon,
which will send without waiting for a response and thus complete even if the
page unloads.  Avoid using when not necessary due to possible unreliability
of the beacon API.

:param eventType: (str) - See documentation for logEvent above
:param elementId: (str) See documentation for logEvent above  */
function logBeacon(eventType, elementId="na") {
  navigator.sendBeacon(`${window.location}`, makeData(eventType, elementId));
}
    
/*   Makes a string with all logged data which server can receive through POST
request.  Values are separated by triple semicolons (;;;).  The following is
included:
  **timestamp - Epoch time of event in seconds.  Rounded to 1/10th of a second.
  **event type - Type of event.  Currently used values are "page_load", 
  "page_unload", "page_blur", "page_focus", "survey_id" and "click."
  **element id - description of what was clicked on for click events
  **bannerStyle - Number describing style of CCPA banner displayed, if any.
  **navigator.userAgent - User Agent string from browser
  **mobile - true or false denoting whether user has a mobile device.

:param eventType: (str) - See documentation for logEvent above
:param elementId: (str) See documentation for logEvent above */
function makeData(eventType, elementId="na") 
{
  // Set banner style to "nobanner" value if undefined
  if(typeof bannerStyle == 'undefined')
  {
    bannerStyle = 'nobanner';
  }

  // Get time in ms, round to 1/10th second due to browser imprecision
  timeStamp = Math.floor(Date.now() / 100 );
  timeStamp = timeStamp / 10;
  timeStamp = String(timeStamp);
    
  // Compile parameters into string
  var data = timeStamp + ";;;" + eventType + ";;;" + elementId + ";;;" + bannerStyle + ";;;" + navigator.userAgent + ";;;" + String(mobile);
  return data;
}

/* Script setting event listeners to log various page events.  The following
 DOM events are recorded with the corresponding event types:

 window.load - "window_load"
 document.visibilitychange / document.focus / document.blur /
 window.focus / window.blur - "page_blur" or "page_focus" (each time the page
  comes into or out of visibility, the corresponding value is only logged once)

 Additionally, a timer attempts to log a "page_active" event 
 every 1 second.  This catches issues where page closing is not always recorded,
 mostly on iOS.

 */

// Listener for page load
window.addEventListener("load", function(){
  logBeacon("window_load")});

// Log every 1 second while page is active
window.setInterval(function(){logEvent("page_active");}, 1000);

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
    logBeacon("page_focus");

  // change flag value
  isVisible = true;
}

function onHidden() {
  // prevent double execution
  if(!isVisible) {
    return;
  }
    logBeacon("page_blur");

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