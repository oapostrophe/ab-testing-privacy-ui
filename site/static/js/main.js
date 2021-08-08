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
  var button1 = document.getElementById("button1");
  var button2 = document.getElementById("button2");
  var screenWidthString=String(window.innerWidth+100)+"px";
  var screenHeight=String(window.innerHeight -340)+"px";
  var bannerScreenHeight=String(window.innerHeight-200)+"px";
  var middleScreenHeight=String((window.innerHeight)/3)+"px";
  var acceptCookies = getCookie("acceptCookies")
  var form= document.getElementById("form");
  var toggle=document.getElementById("toggle");
  var one_button=document.getElementById("one_button");
  var form_input=document.getElementById("form_input")
  var button_and_link=document.getElementById("button_and_link");
  var link_choice=document.getElementById("link_choice");
  var link_text=document.getElementById("link_text");
  var mobile_button_and_link=document.getElementById("mobile_button_and_link");
  var link_in_text=document.getElementById("link_in_text");
  var toggle_table=document.getElementById("toggle_table");
  var toggle_table_b=document.getElementById("toggle_table_b");
  ///form.style.display="none";
  x.style.display="block";
  if (String(acceptCookies)=="1"){
    return;
  }
  if (mobile == false){
    x.style.left = "24px";
    x.style.right="24px";
    x.style.maxWidth=screenWidthString;
    x.style.bottom=bannerScreenHeight;
    if (String(desktopLayout) == "0"){
    }
    else if (String(desktopLayout) == "1"){
      button2.style.fontWeight="normal";
      button2.style.background="skyblue";
      button2.style.border="1px solid black"
      button1.style.background="darkblue";
      button1.style.border="1px solid white"
      button1.style.color="white";
    }
    else if (String(desktopLayout) == "2"){
      button2.setAttribute("onClick", "javascript: myForm(), logEvent('click', 'button_do_not_sell');");
    }
    else if (String(desktopLayout) == "3"){
      toggle_table_b.style.display="none";
      button2.setAttribute("onClick", "javascript: myToggle(), logEvent('click', 'button_do_not_sell');");
    }
    else if (String(desktopLayout) == "4"){
      x.style.display="none";
      bannerScreenHeight=String(window.innerHeight-280)+"px";
      toggle.style.bottom=bannerScreenHeight;
      toggle.style.maxWidth=screenWidthString;
      toggle_table.style.display="none";
      toggle.style.left = "24";
      toggle.style.right="24px";
    }
    else if (String(desktopLayout) == "5"){
      x.style.display="none";
      one_button.style.bottom=bannerScreenHeight;
      one_button.style.maxWidth=screenWidthString;
      one_button.style.left="10px";
      one_button.style.right="10px";
    }
    else if (String(desktopLayout)=="6"){
      x.style.display="none";
      bannerScreenHeight=String(window.innerHeight-130)+"px";
      button_and_link.style.bottom=bannerScreenHeight;
      button_and_link.style.maxWidth=screenWidthString;
      button_and_link.style.left="10px";
      button_and_link.style.right="10px";
    }
    else if (String(desktopLayout)=="7"){
      x.style.display="none";
      link_text.style.bottom=bannerScreenHeight;
      link_text.style.maxWidth=screenWidthString;
      link_text.style.left="10px";
      link_text.style.right="10px";
    }
  }
  else{
    x.style.bottom=screenHeight
    x.style.left = "24px";
    x.style.right="24px";
    if (String(mobileLayout)=="0"){
      
    }
    else if (String(mobileLayout)=="1"){
      button2.style.fontWeight="normal";
      button2.style.background="skyblue";
      button2.style.border="1px solid black"
      button1.style.background="darkblue";
      button1.style.border="1px solid white";
      button1.style.color="white";
    }
    else if (String(mobileLayout)=="2"){
      form.style.maxWidth="310px";
      button2.setAttribute("onClick", "javascript: myForm(), logEvent('click', 'button_do_not_sell')");
      form_input.setAttribute("onClick", "javascript: myFixForm()");
      one_button.style.display="none";
    }
    else if (String(mobileLayout)=="3"){
      toggle_table_b.style.display="none";
      button2.setAttribute("onClick", "javascript: myMobileToggle(), logEvent('click', 'button_do_not_sell');");
    }
    else if (String(mobileLayout)=="4"){
      x.style.display="none";
      var screenHeight=String(window.innerHeight -600)+"px";
      toggle_table_b.style.display="none";
      toggle.style.bottom=screenHeight;
      toggle.style.left = "";
      toggle.style.right="24px";
    }
    else if (String(mobileLayout)=="5"){
      x.style.display="none";
      one_button.style.bottom=screenHeight;
      one_button.style.maxWidth="300px";
      one_button.style.left="10px";
      one_button.style.right="10px";
    }
    else if (String(mobileLayout)=="6"){
      x.style.display="none";
      mobile_button_and_link.style.bottom=screenHeight;
      mobile_button_and_link.style.maxWidth="275px";
      link_choice.setAttribute("onClick", "javascript: myMobileToggle(), logEvent('click', 'button_do_not_sell');");
      mobile_button_and_link.style.left="24px";
      mobile_button_and_link.style.right="24px";
    }
    else if (String(mobileLayout)=="7"){
      x.style.display="none";
      link_in_text.setAttribute("onClick", "javascript: myMobileToggle(), logEvent('click', 'button_do_not_sell');");
      link_text.style.bottom=screenHeight;
      link_text.style.maxWidth="310px";
      link_text.style.left="10px";
      link_text.style.right="10px";
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
  var link_accept=document.getElementById("link_accept")
  var button0=document.getElementById("button0");
  var button1=document.getElementById("button1");
  var button2 = document.getElementById("button2");
  var options= document.getElementById("options");
  var text = document.getElementById("text");
  text.innerHTML="Under the California Consumer Privacy Act, you have the right to opt-out of the sale of your personal information to third parties. You may exercise your right to opt out of the sale of personal information by clicking the 'Deny Cookies' button.";
  button1.style.display="none";
  button2.style.display="none";
  options.style.display="block";
  button0.style.display="block";
  link_accept.style.display="none";
  ///button2.innerHTML="Don't allow";
  ///button2.setAttribute( "onClick", "javascript: myFunction(), enableScroll(), endOverlay();" )
}
function myClose() {
  document.cookie="acceptCookies=1; path=/; ";
  var x=document.getElementById("notification");
  var overlay=document.getElementById("myNav");
  var form=document.getElementById("form");
  var toggle=document.getElementById("toggle");
  var one_button=document.getElementById("one_button");
  var button_and_link=document.getElementById("button_and_link");
  var link_text=document.getElementById("link_text");
  var mobile_button_and_link=document.getElementById("mobile_button_and_link");
  x.style.display="none";
  form.style.display="none";
  toggle.style.display="none";
  one_button.style.display="none";
  overlay.style.display="none";
  button_and_link.style.display="none";
  link_text.style.display="none";
  mobile_button_and_link.style.display="none";
}
function myFunction() {
  document.cookie="acceptCookies=1; path=/; ";
  var toggle=document.getElementById("toggle");
  var form=document.getElementById("form");
  var x = document.getElementById("notification");
  toggle.style.display="none";
  form.style.display="none";
  if (x.style.display === "none") {
    x.style.display = "block";
  } 
  else {
    x.style.display = "none";
  }
}
function myFixForm(){
  var toggle=document.getElementById("toggle");
  toggle.style.display="none";
  var middleScreenHeight=String((window.innerHeight)/3-150)+"px";
  var form=document.getElementById("form");
  form.style.bottom=middleScreenHeight;
}
function myForm(){
  var x= document.getElementById("notification");
  var overlay=document.getElementById("myNav")
  overlay.style.display="block";
  x.style.display="none";
  var middleScreenHeight=String((window.innerHeight)/3-50)+"px";
  var screenHeight=String(window.innerHeight -530)+"px";
  var form=document.getElementById("form");
  form.style.bottom=middleScreenHeight;
  form.style.left = "10px";
  form.style.right="10px";
}
function myToggle(){
  var x = document.getElementById("notification");
  var overlay=document.getElementById("myNav")
  overlay.style.display="block";
  x.style.display="none";
  var screenHeight=String(window.innerHeight -600)+"px";
  var middleScreenHeight=String((window.innerHeight)/3-100)+"px";
  var toggle=document.getElementById("toggle");
  toggle.style.bottom=middleScreenHeight;
  toggle.style.left = "24px";
  toggle.style.right="24px";
}
function myMobileToggle(){
  var x = document.getElementById("notification");
  var overlay=document.getElementById("myNav")
  overlay.style.display="block";
  x.style.display="none";
  var screenHeight=String(window.innerHeight -750)+"px";
  var middleScreenHeight=String(((window.innerHeight)/3)-100)+"px";
  var toggle=document.getElementById("toggle");
  toggle.style.bottom=middleScreenHeight;
  toggle.style.left = "24px";
  toggle.style.right="24px";
}
function myDirectToggle(){
  var x = document.getElementById("notification");
  x.style.display="none";
  var screenHeight=String(window.innerHeight -530)+"px";
  var middleScreenHeight=String((window.innerHeight)/3)+"px";
  var toggle=document.getElementById("toggle");
  toggle.style.bottom=screenHeight;
  toggle.style.left = "";
  toggle.style.right="24px";
}
 
 
function one_button(){
  var x=document.getElementById("notification")
  var screenHeight=String(window.innerHeight -350)+"px";
  var middleScreenHeight=String((window.innerHeight)/3)+"px";
  var one_button=document.getElementById("one_button");
  x.style.display="none";
  one_button.style.bottom=screenHeight;
  one_button.style.left="";
  one_button.style.right="10px";
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
 
 

