$(document).ready(function(){
    // style for changing status
    const status = parseInt($("input#id_status").val()); 

    // Start with last comments
    let counterComments = 0;

    // Load comments 10 at a time
    const quantityComments = 10; 

    $("button#status-prev").addClass("btn");
    $("button#status-next").addClass("btn");

    // load base style table and timeline for current inventory status
    updateStyleDisplayStatus(status);

    // next status inventory
    $("button#status-next").click( e => {
        e.preventDefault();
        const status = parseInt($("input#id_status").val());
        updateInventoryStatus($("#inventory_pk").text(), status + 1);
    });

    // prev status inventory
    $("button#status-prev").click( e => {
        e.preventDefault();
        const status = parseInt($("input#id_status").val());
        updateInventoryStatus($("#inventory_pk").text(), status - 1);
    });

    // show offcanvas with form for add tree photos
    $("button.cameraButton").click((el) => {
        const parents = $(el.currentTarget).parentsUntil("tbody")
        const thWithID = $($(parents)[$(parents).length-1]).children("th:first")
        $("form#cameraForm > span#photo-tree-lp").text($(thWithID).text())
        $("form#cameraForm > input#id_tree").val(parseInt($(thWithID).data("tree-pk")));
    });

    // action for form submit adding tree photo
    $("form#cameraForm").submit((e) => {
        e.preventDefault();
        var formData = new FormData($("form#cameraForm")[0]);
        $.ajax({
            method:"POST",
            url: $("form#cameraForm").attr("action"),
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: formData,
            dataType: 'json',
            mimeType: "multipart/form-data",
            processData: false,
            contentType: false,
            cache:false,
            success:function(data){
                console.log(data);
                $("#offcanvasPhotoLabel").next().click()
                $("div#trees").first("div").prepend($("<p/>")
                    .text(`Successful! Added new photos to the tree with number ${$("form#cameraForm > span#photo-tree-lp").text()}.`)
                    .addClass("alert alert-success text-center")
                    .attr("role", "alert")
                    .fadeOut(7000, () => {
                        $("p.alert-success").slideUp(500, () => {
                             $("p.alert").remove();
                        })
                    })
                )
                $("#offcanvasPhoto").on('hidden.bs.offcanvas', () => {
                        $("form#cameraForm > span#photo-tree-lp").text("")
                        $("form#cameraForm > input#id_image").val("");
                        $("div#offcanvasPhoto > p.alert").remove();
                    }
                );
            },
            error: function(data){
                console.log(data);
                $("form#cameraForm").after($("<p/>")
                    .text("Something went wrong!  Make sure you select the correct file format.")
                    .addClass("alert alert-danger mx-3 mb-5 text-center")
                    .attr("role", "alert")
                )
                $("#offcanvasPhoto").on('hidden.bs.offcanvas', () => {
                        $("form#cameraForm > input#id_image").val("");
                        $("div#offcanvasPhoto > p.alert").remove();
                    }
                );
            }
        });
    });
    
    // show offcanvas with form for add tree comments and display ones
    $("button.commentButton").click((el) => {
        const parents = $(el.currentTarget).parentsUntil("tbody")
        const thWithID = $($(parents)[$(parents).length-1]).children("th:first")
        $("form#commentForm > span#comment-tree-lp").text($(thWithID).text())
        $("form#commentForm > input#id_tree").val(parseInt($(thWithID).data("tree-pk")));
        load_comments($("form#commentForm > input#id_tree").val());
        // $("div#comments-list").scroll(() => {
        //     if ($("div#comments-list").scrollTop() == 0) {
        //         load_comments($("form#commentForm > input#id_tree").val());
        //     }
        // });
    });

    // event for hide offcanvas with tree comments
    $("#offcanvasComments").on('hidden.bs.offcanvas', () => {
            $("form#commentForm > textarea#id_description").val("");
            $("div#offcanvasComments > p.alert").remove();
            $("div#comments-list").empty();
            // counterComments = 0;
        }
    );

    // action for form submit adding tree comments
    $("form#commentForm").submit((e) => {
        e.preventDefault();
        var formData = new FormData($("form#commentForm")[0]);
        $.ajax({
            method:"POST",
            url: $("form#commentForm").attr("action"),
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            data: formData,
            dataType: 'json',
            processData: false,
            contentType: false,
            cache:false,
            success:function(data){
                counterComments = 0
                $("form#commentForm > textarea#id_description").val("");
                $("div#offcanvasComments > p.alert").remove();
                $("div#comments-list").empty();
                load_comments(pkTree=$("form#commentForm > input#id_tree").val());
                $("form#commentForm > button").blur();
            },
            error: function(data){
                $("form#commentForm").after($("<p/>")
                    .text("Something went wrong!  See details in console.")
                    .addClass("alert alert-danger mx-3 mb-5 text-center")
                    .attr("role", "alert")
                )
                $("#offcanvasComments").on('hidden.bs.offcanvas', () => {
                        $("form#commentForm > textarea#id_description").val("");
                        $("div#offcanvasComments > p.alert").remove();
                    }
                );
            }
        });
    });    


    // definitions functions

    function updateStyleDisplayStatus(status) {
        $("button#status-prev").show();
        $("button#status-next").show();    
        if (status < 1) {
            $("button#status-prev").hide();
            $("div.step-2").removeClass("active");
            $("div.step-3").removeClass("active");
            hideCellsOfTableWithTrees(6, 8);
            showCellsOfTableWithTrees(2, 4);
            $("button#valorization-submit").addClass("d-none");
            $("button#management-submit").addClass("d-none");
            $("a#add-tree-link").removeClass("pe-none");
            $("tr#status-labels > td").eq(2).addClass("d-none");
            $("tr#status-labels > td").eq(3).addClass("d-none");
            $("tr#status-labels > td").eq(1).attr("colspan", 5);
            $("td.tree-valorization > select").attr("disabled", false);
        } else if (status < 2) {
            $("div.step-2").addClass("active");
            $("div.step-3").removeClass("active");
            showCellsOfTableWithTrees(6, 7);
            hideCellsOfTableWithTrees(2, 4);
            hideCellsOfTableWithTrees(8, 8);
            $("table.table tr").css("background-color", "transparent");
            $("button#valorization-submit").removeClass("d-none");
            $("button#management-submit").addClass("d-none");
            $("tr#status-labels > td").eq(2).removeClass("d-none");
            $("tr#status-labels > td").eq(3).addClass("d-none");            
            $("tr#status-labels > td").eq(1).attr("colspan", 2);
            $("td.tree-valorization > select").attr("disabled", false);
        } else {
            $("button#status-next").hide();
            $("div.step-3").addClass("active");
            $("div.step-2").addClass("active");
            $("div.step-1").addClass("active");
            showCellsOfTableWithTrees(8, 8);
            hideCellsOfTableWithTrees(2, 4);
            $("td.tree-management > select").change((el) => {
                if ($(el.currentTarget).val() == 2) {
                   $(el.currentTarget).parent().parent().css("background-color", "#FB424D");
                } else if ($(el.currentTarget).val() == 1) {
                    $(el.currentTarget).parent().parent().css("background-color", "#FBF042");
                } else {
                    $(el.currentTarget).parent().parent().css("background-color", "#B5FCC0");
                }
                
            });
            $("button#valorization-submit").addClass("d-none");
            $("button#management-submit").removeClass("d-none");
            $("tr#status-labels > td").eq(3).removeClass("d-none");
            $("tr#status-labels > td").eq(1).attr("colspan", 2);
            $("td.tree-valorization > select").attr("disabled", true);
        }
    }

    function updateInventoryStatus(pk, status) {
        return fetch(`/api/inventory/${pk}/details/`, {
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({status: status}),
            method: 'PATCH',
        }).then(
            (resp) => {
                if (!resp.ok) {
                    alert('An error has occurred! Open devtools and the Network tab, and look for the cause')
                } else {
                    $("input#id_status").val(status);
                    updateStyleDisplayStatus(status);
                    return resp.json();
                }
                
        })
    }

    function load_comments(pkTree) {
        // Set start and end comments number
        const start = counterComments
        const end = start + quantityComments
        // counterComments = end

        $.ajax({
            method:"GET",
            url: $("form#commentForm").attr("action"),
            dataType: 'json',
            data: {
                pk: pkTree,
                start: start,
                end: end,
            },
            contentType: "application/json",
            cache:false,
            success:function(data){
                display_comments(data);
                if (start == 0) {
                    $("div#comments-list").scrollTop($("div#comments-list").prop("scrollHeight"));
                }
            },
            error: function(data){
                console.log(data);
            }
        })
    }

    function display_comments(data) {
        $(data).each((index, el) => {
            let spanCreatedDate = el.created.replace("T", " ").slice(0, 19)
            $("div#comments-list").prepend(
                $("<div/>").addClass("mt-2").append(
                    $("<span/>").text(spanCreatedDate).addClass("text-muted ms-2 fs-italic").attr("style", "font-size: 75%;")
                ).append(
                    $("<div/>").text(el.description).addClass("form-control text-break")
                )
            );
        });
    }

    function hideCellsOfTableWithTrees(startIndex, endIndex) {
        for (let i=startIndex; i <= endIndex; i++) {
            $("tr#row-with-headers-of-table-trees > th").eq(i).addClass("d-none");
            $("tr.one-position-tree").each((index, el) => {
                $(el).find("td").eq(i-1).addClass("d-none");
            });
        }
    }

    function showCellsOfTableWithTrees(startIndex, endIndex) {
        for (let i=startIndex; i <= endIndex; i++) {
            $("tr#row-with-headers-of-table-trees > th").eq(i).removeClass("d-none");
            $("tr.one-position-tree").each((index, el) => {
                $(el).find("td").eq(i-1).removeClass("d-none");
            });
        }
    }


    // for csrf token and others cookies

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

})