$(document).ready(function(){
    setBasicStyleForm();

    // creating new div
    const divPassword = $("<div></div>");
    divPassword.addClass("input-group mt-2");

    // cloning created div
    const divConfirmPassword = divPassword.clone();
    const divLoginPassword = divPassword.clone();

    // createing new span element
    const spanForEyePassword = $("<span></span>");
    spanForEyePassword.addClass("input-group-text show_password");
    spanForEyePassword.attr("role", "button");

    // eye icon from bootsrap icons
    const showEyePassword = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
            <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
            <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
        </svg>
    `
    // adding input element for password to created and cloned div elements
    $(divPassword).append($("form#register_form > #id_password").removeClass("mt-2"));
    $(divConfirmPassword).append($("form#register_form > #id_confirmation_password").removeClass("mt-2"));
    $(divLoginPassword).append($("form#login_form > #id_password").removeClass("mt-2"));

    // adding icon eye to span element
    $(spanForEyePassword).append(showEyePassword);

    // adding span element to created div elements
    $(divPassword).append(spanForEyePassword);
    $(divConfirmPassword).append(spanForEyePassword.clone());
    $(divLoginPassword).append(spanForEyePassword.clone());

    // adding div elements to forms
    $("form#register_form > [for=id_password]").after(divPassword);  
    $("form#register_form > [for=id_confirmation_password]").after(divConfirmPassword);
    $("form#login_form > #id_username").after(divLoginPassword);

    // crossed out eye icon from bootsrap
    const hideEyePassword = `
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-eye-slash" viewBox="0 0 16 16">
            <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"/>
            <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"/>
            <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"/>
        </svg>
    `       

    // events for eye icons
    $("span.show_password").click( e => {
        showPassword($(e.currentTarget));
    })

    $("span.hide_password").click( e => {
        hidePassword($(e.currentTarget));
    })

    // defined functions

    function setBasicStyleForm () {
        $("input").addClass("form-control");
        $("*[type='submit']").addClass("btn btn-primary position-absolute bottom-0 end-0 me-4 mb-3");
        $("textarea").addClass("form-control");
        $("select").addClass("form-select");
        $("form").addClass("w-50 m-auto px-4 pt-4 pb-5 border rounded mt-5 position-relative");
        $(".helptext").addClass("form-text");
        addCircuit($(".plus-circuit"));
        $("form#register_form > label").hide();
        $("form#register_form > br").remove();
        $("form#register_form > input").addClass("mt-2");
        $("form#login_form > input").addClass("mt-2");
        $("form#register_form > [type=submit]").removeClass("position-absolute bottom-0 end-0 me-4 mb-3");
        $("form#login_form > [type=submit]").removeClass("position-absolute bottom-0 end-0 me-4 mb-3");
        $("form#register_form > [type=submit]").addClass("mt-4");
        $("form#login_form > [type=submit]").addClass("mt-4");
    } 

    function showPassword (el) {
        $(el).children(":first").replaceWith(hideEyePassword);
        $(el).prev().attr("type", "text");
        $(el).removeClass("show_password");
        $(el).addClass("hide_password");

        $(el).click( e => {
            hidePassword($(e.currentTarget));
        })
    }

    function hidePassword (el) {
        $(el).children(":first").replaceWith(showEyePassword);
        $(el).prev().attr("type", "password");
        $(el).removeClass("hide_password");
        $(el).addClass("show_password");

        $(el).click( e => {
            showPassword($(e.currentTarget));
        })
    }

    function addCircuit (el) {
        el.click((e) => {
            e.preventDefault();
            const newCircuit = $(e.currentTarget).parent().clone();
            newCircuit.appendTo(
                $(e.currentTarget).parent().parent()
            );
            addCircuit(newCircuit.find($("button.plus-circuit")));
            cancelCircuit($(".cancel-circuit"));
        })
    }

    function cancelCircuit (el) {
        el.click((e) => {
            e.preventDefault();
            if ($(".cancel-circuit").length > 1) {
                $(e.currentTarget).parent().css("animationPlayState", "running");
                e.currentTarget.parentElement.addEventListener("animationend", () => {
                    $(e.currentTarget).parent().remove();
                })
            } else {
                $(e.currentTarget).parent().find($("input#id_circuit")).val(null)
            }
        });            
    }
});