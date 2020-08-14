"use strict";

document.addEventListener("keydown", enterForm);

function enterForm(e){
    if(e.shiftKey && e.keyCode == 13){
        e.preventDefault();
        document.querySelector(".main__chat-textarea").value += '\n';
    }
    else if (e.keyCode == 13){
        e.preventDefault();
        let form = document.querySelector(".form-send-message");
        form.submit();
    }
}

