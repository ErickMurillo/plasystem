(function($){
	$(document).ready( function()
	{
    valor = $('.field-respuesta select').val();
    if (valor == 1) {
      $('#duenosi_set-group').show();
      $('#duenono_set-group').hide();
    } else if (valor == 2) {
      $('#duenosi_set-group').hide();
      $('#duenono_set-group').show();
    } else {
      $('#duenosi_set-group').hide();
      $('#duenono_set-group').hide();
    }

    $('.field-respuesta select').change(function(){
      valor = $('.field-respuesta select').val();
      if (valor == 1) {
        $('#duenosi_set-group').show();
        $('#duenono_set-group').hide();
      } else {
        $('#duenosi_set-group').hide();
        $('#duenono_set-group').show();
      }
    });

  });
})(jQuery || django.jQuery);
