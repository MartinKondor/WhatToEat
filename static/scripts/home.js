(function ($) {

// int for keeping track of new added ingredient "name" attributes
let ingredientNumber = 1;


$("#add-ingredient-button").on("click", function (e) {
    e.preventDefault();
    ingredientNumber++;

    $("#ingredients-list").append(`<li><input name="ingredient-${ingredientNumber}" type="text" class="form-control" placeholder="Type in an other ingredient ..."></li>`);
});

$('#search-button').on('click', function (e) {
    $('#loading-modal').modal('toggle');
});

})(jQuery);
