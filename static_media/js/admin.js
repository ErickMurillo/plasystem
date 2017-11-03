(function($){
	$(document).ready( function()
	{
    valor = $('.field-respuesta select').val();
    if (valor == 'Si') {
      $('#duenosi_set-group').show();
      $('#duenono_set-group').hide();
    } else if (valor == 'No') {
      $('#duenosi_set-group').hide();
      $('#duenono_set-group').show();
    } else {
      $('#duenosi_set-group').hide();
      $('#duenono_set-group').hide();
    }

    $('.field-respuesta select').change(function(){
      valor = $('.field-respuesta select').val();
      if (valor == 'Si') {
        $('#duenosi_set-group').show();
        $('#duenono_set-group').hide();
      } else {
        $('#duenosi_set-group').hide();
        $('#duenono_set-group').show();
      }
    });

  });
})(jQuery || django.jQuery);
