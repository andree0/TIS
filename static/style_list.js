$(document).ready(function(){
    // style nav items
    if ($(location).attr('pathname') === "/inventory/create/") {
        $("a#new-inventory-link").addClass("active");
    } else if ($(location).attr('pathname') === "/inventory/all/") {
        $("a#all-inventory-link").addClass("active");
    } else {
        $("a#new-inventory-link").removeClass("active");
        $("a#all-inventory-link").removeClass("active");
    }

    // style other list


    // style for alert message
    $("div.error").addClass("alert alert-danger my-1").attr("role", "alert");
    $("div.success").addClass("alert alert-success my-1 text-center").attr("role", "alert");
})