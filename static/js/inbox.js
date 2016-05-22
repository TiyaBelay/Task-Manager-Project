"use strict";

function showMessage(msg) {
    alert("test")
}

$("#click-message").on("click", showMessage)


function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
}

function openMessage() {





}