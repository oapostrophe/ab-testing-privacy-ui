function disableScroll() { 
  // Get the current page scroll position 
  scrollTop = window.pageYOffset || document.documentElement.scrollTop; 
  scrollLeft = window.pageXOffset || document.documentElement.scrollLeft, 

  // if any scroll is attempted, set this to the previous value 
  window.onscroll = function() { 
    window.scrollTo(scrollLeft, scrollTop); 
    }; 
} 

function enableScroll() { 
  window.onscroll = function() {}; 
} 

function determine_layout() {
  var x = document.getElementById("notification");
  var overlay=document.getElementById("myNav");
  var button2 = document.getElementById("button2");
  var screenWidthString=String(window.innerWidth+100)+"px";
  var screenHeight=String(window.innerHeight -340)+"px";
  var bannerScreenHeight=String(window.innerHeight-200)+"px";
  var middleScreenHeight=String((window.innerHeight)/3)+"px";
  var acceptCookies = getCookie("acceptCookies")
  x.style.display="block";
  if (String(acceptCookies)=="1"){
    x.style.display="none";
  }
  if (mobile == false){
    if (String(desktopLayout) == "0"){
      x.style.bottom="10px";
      x.style.left = "10px";
      x.style.right="";
    }
    if (String(desktopLayout) == "1"){
      x.style.bottom="10px";
      x.style.left = "24px";
      x.style.right="24px";
      x.style.maxWidth=screenWidthString;
    }
    if (String(desktopLayout) == "2"){
      x.style.bottom="10px";
      x.style.left = "";
      x.style.right="10px"
    }
    if (String(desktopLayout) == "3"){
      x.style.bottom=screenHeight;
      x.style.left = "10px";
      x.style.right="";
    }
    if (String(desktopLayout) == "4"){
      x.style.bottom=bannerScreenHeight;
      x.style.left = "24px";
      x.style.right="24px";
      x.style.maxWidth=screenWidthString;
    }
    if (String(desktopLayout) == "5"){
      x.style.bottom=screenHeight;
      x.style.left = "";
      x.style.right="10px"
    }
    if (String(desktopLayout) == "6"){
      x.style.bottom=middleScreenHeight;
      x.style.left = "24px";
      x.style.right="24px";
    }
    if (String(desktopLayout)=="7"){
      x.style.display="none";
    }
  }
  else{
    x.style.left = "24px";
    x.style.right="24px";
    if (String(mobileLayout)=="0"){
      x.style.bottom="10px"
    }
    if (String(mobileLayout)=="1"){
      x.style.bottom=middleScreenHeight;
    }
    if (String(mobileLayout)=="2"){
      x.style.bottom=screenHeight;
    }
    if (String(mobileLayout)=="3"){
      x.style.display="none";
    }
  }
}
function linkClicked(){
  var x = document.getElementById("notification");
  var middleScreenHeight=String((window.innerHeight)/3)+"px"
  x.style.display="block";
  x.style.bottom=middleScreenHeight;
  x.style.left = "24px";
  x.style.right="24px";
  x.style.maxWidth="400px";
}

function endOverlay(){
  var overlay=document.getElementById("myNav");
  overlay.style.display="none"
}
function readMore(){
  var button2 = document.getElementById("button2");
  var text = document.getElementById("text");
  text.innerHTML="Under the California Consumer Privacy Act, you have the right to opt-out of the sale of your personal information to third parties. You may exercise your right to opt out of the sale of personal information by clicking the 'Deny Cookies' button.";
  button2.innerHTML="Don't allow";
  button2.setAttribute( "onClick", "javascript: myFunction(), enableScroll(), endOverlay();" )
}
function myFunction() {
  document.cookie="acceptCookies=1; path=/; ";
  var x = document.getElementById("notification");
  if (x.style.display === "none") {
    x.style.display = "block";
  } 
  else {
    x.style.display = "none";
  }
}
    
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}