$(document).ready(function(){
    // style form
    $("button#btn-save-inventory").hide();
    $("form#update-inventory input").prop("readonly", true);
    $("form#update-inventory input#id_status").prop("readonly", false);
    $("form#update-inventory input").addClass("ps-2 bg-white border ronuded text-muted");
    $("form#update-inventory").addClass("m-0 border-0 w-100 position-relative");
    $("form#update-inventory").removeClass("m-auto mt-5 w-50 border rounded px-4 pt-4 pb-5");

    // activate form
    $("button#btn-edit-inventory").click( e => {
        e.preventDefault();
        $("div.container-sm h2").after($("<textarea></textarea>").attr("name", "description")
        .attr("cols", "40").attr("rows", "5").attr("id", "id_description")
        .text($("div.container-sm h2 + p").text()).addClass("form-control text-center"));

        $("div.container-sm h2 + textarea + p").remove();
        $("button#btn-edit-inventory").hide();
        $("form#update-inventory input").prop("readonly", false);
        $("form#update-inventory input").removeClass("text-muted");
        $("button#btn-save-inventory").show();

        $("div.container-sm > div:first").prepend(
            $("<input>").attr("type", "text").attr("name", "name")
            .attr("id", "id_name").attr("maxlenght", "64")
            .attr("required", true)
            .addClass("form-control fs-2 text-center w-50 m-2").val($("div.container-sm h2:first").text())
        )
        $("div.container-sm h2:first").remove();
    });

    // trigger inventory-update form if errors
    if ($("div.error").length > 0) {
        $("button#btn-edit-inventory").trigger("click");
    }

})