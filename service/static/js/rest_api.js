$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // ****************************************
    //  WISHLISTS
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_name").val(res.wishlist_name);
        $("#wishlist_id").val(res.wishlist_id);
        $("#account_id").val(res.account_id);
        $("#items").val(res.items);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#wishlist_name").val("");
        $("#wishlist_id").val("");
        $("#account_id").val("");
        $("#items").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#wishlist-create-btn").click(function () {
        let id = $("#wishlist_id").val();
        let name = $("#wishlist_name").val();
        let account_id = $("#account_id").val();
        let items = $("#items").val();

        let data = {
            "id": parseInt(id),
            "account_id": parseInt(account_id),
            "name": name,
            "items": items,
        };
        console.log(data);

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(){
            update_form_data()
            flash_message("Success")
        });

        ajax.fail(function(){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a wishlist
    // ****************************************

    $("#wishlist-update-btn").click(function () {
        let name = $("#wishlist_name").val();
        let id = $("#wishlist_id").val();
        let account_id = $("#account_id").val();
        let items = $("#items").val();

        let data = {
            "id": parseInt(id),
            "account_id": parseInt(account_id),
            "name": name,
            "items": items,
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/wishlists/${wishlist_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#wishlist-delete-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************

    $("#wishlist-search-btn").click(function () {

        let wishlist_name = $("#wishlist_name").val();

        let queryStrings = []

        if (wishlist_name) {
            queryStrings.push('name=' + wishlist_name)
        }
        if (wishlist_id) {
            queryStrings.push('id=' + wishlist_id)
        }


        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists?${queryStrings.join('&')}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Account ID</th>'
            table += '<th class="col-md-2">Items</th>'


            table += '</tr></thead><tbody>'
            let firstWishlist = "";
            for(let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table +=  `<tr id="row_${i}"><td>${wishlist.name}</td><td>${wishlist.id}</td><td>${wishlist.account_id}</td><td>${wishlist.items}</td></tr>`;
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstWishlist != "") {
                update_form_data(firstWishlist)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    //  ITEMS
    // ****************************************

    // ****************************************
    // Add Item to a Wishlist
    // ****************************************

    $("#create-item-btn").click(function () {

        let item_id = $("#item_id").val();
        let wishlist_id = $("#wishlist_id_2").val();
        let sku = $("#sku").val();
        let item_available = $("#item_available").val();
        let item_count;
        if( ($("#item_count").val()) == ""){
            item_count = 1;
        } else{
            item_count = $("#item_count").val();
        }
        if( ($("#item_available").val()) == ""){
            item_count = 1;
        } else{
            item_count = $("#item_count").val();
        }
        
        let data = {
            "id": item_id,
            "wishlist_id": wishlist_id,
            "sku": parseInt(sku),
            "item_available": item_available,
            "count": parseInt(item_count),
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/api/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data_item(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        let item_id = $("#item_id").val();
        // doesn't matter
        let wishlist_id = 1;

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/wishlists/${item_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data_item(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-item-btn").click(function () {

        let item_id = $("#item_id").val();
        // doesn't matter
        let wishlist_id = 1;

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/wishlists/${item_id}/items/${item_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Update a Wishlist Item
    // ****************************************

    $("#update-item-btn").click(function () {

        let id = $("#item_id").val();
        let wishlist_id = $("#wishlist_id_2").val();
        let sku = $("#sku").val();
        let item_available = $("#item_available").val();
        let count = $("#item_count").val();
   
        let data = {
            "id": item_id,
            "wishlist_id": wishlist_id,
            "sku": parseInt(sku),
            "item_available": item_available,
            "count": parseInt(count),
        };


        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/wishlists/${wishlist_id}/items/${item_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data_item(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Search for a Wishlist Item
    // ****************************************

    $("#search-item-btn").click(function () {

        let item_id = $("#item_id").val();
        let wishlist_id = $("#wishlist_id_2").val();

        let queryString = ""

        if(item_id){
            get_url = `/api/wishlists/${item_id}/items/${item_id}`
        } else if (item_id){
            queryString += 'name=' + item_name
            get_url = `/api/wishlists/${wishlist_id}/items?${queryString}`
        } else{
            get_url = `/api/wishlists/${wishlist_id}/items`
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: get_url,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_item_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">Item ID</th>'
            table += '<th class="col-md-3">Wishlist ID</th>'
            table += '<th class="col-md-4">SKU</th>'
            table += '<th class="col-md-2">Item Available</th>'
            table += '<th class="col-md-2">Count</th>'
            table += '</tr></thead><tbody>'
            let firstIList = "";
            if(item_id){
                let item = res;
                table +=  `<tr id="row_0"><td>${item.id}</td><td>${item.wishlist_id}</td><td>${item.sku}</td><td>${item.item_available}</td>
                <td>${item.count}</td></tr>`;
                firstIList = item;
            } else{
                for(let i = 0; i < res.length; i++) {
                    let item = res[i];
                    table +=  `<tr id="row_${i}"><td>${item.id}</td><td>${item.wishlist_id}</td><td>${item.sku}</td><td>${item.item_available}</td>
                    <td>${item.count}</td></tr>`;
                    if (i == 0) {
                        firstIList = item;
                    }
                }
            }
            

            table += '</tbody></table>';
            $("#search_item_results").append(table);

            // copy the first result to the form
            if (firstIList != "") {
                update_form_data_item(firstIList)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
})