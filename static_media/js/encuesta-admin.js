(function($){
	$(document).ready( function()
	{
    valor = $('.field-certificacion select').val();
    if (valor == 1) {
      $('#tipocertificacion_set-group').show();
      $('#certificadoempresa_set-group').show();
    } else if (valor == 2) {
      $('#tipocertificacion_set-group').hide();
      $('#certificadoempresa_set-group').hide();
    } else {
      $('#tipocertificacion_set-group').hide();
      $('#certificadoempresa_set-group').hide();
    }

    $('.field-certificacion select').change(function(){
      valor = $('.field-certificacion select').val();
      if (valor == 1) {
        $('#tipocertificacion_set-group').show();
        $('#certificadoempresa_set-group').show();
      } else if (valor == 2) {
        $('#tipocertificacion_set-group').hide();
        $('#certificadoempresa_set-group').hide();
      } else {
        $('#tipocertificacion_set-group').hide();
        $('#certificadoempresa_set-group').hide();
      }
    });

  });
})(jQuery || django.jQuery);
