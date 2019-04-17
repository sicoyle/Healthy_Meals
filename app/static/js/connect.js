console.log("IM HERE!!!")

function toggleModal(index) {
    $('#exampleModal').modal('toggle')
    console.log("Inside function")
    console.log(index)
}

$('.input-number-increment').click(function() {
    var $input = $(this).parents('.input-number-group').find('.input-number');
    var val = parseInt($input.val(), 10);
    $input.val(val + 1);
  });
  
  $('.input-number-decrement').click(function() {
    var $input = $(this).parents('.input-number-group').find('.input-number');
    var val = parseInt($input.val(), 10);
    $input.val(val - 1);
  })