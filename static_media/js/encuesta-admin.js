(function($){
	$(document).ready( function()
	{
		$('#id_productor').select2();
		$('#id_encuestador').select2();
    valor = $('.field-certificacion select').val();
    if (valor == 'Si') {
      $('#tipocertificacion_set-group').show();
      $('#certificadoempresa_set-group').show();
    } else if (valor == 'No') {
      $('#tipocertificacion_set-group').hide();
      $('#certificadoempresa_set-group').hide();
    } else {
      $('#tipocertificacion_set-group').hide();
      $('#certificadoempresa_set-group').hide();
    }

    $('.field-certificacion select').change(function(){
      valor = $('.field-certificacion select').val();
      if (valor == 'Si') {
        $('#tipocertificacion_set-group').show();
        $('#certificadoempresa_set-group').show();
      } else if (valor == 'No') {
        $('#tipocertificacion_set-group').hide();
        $('#certificadoempresa_set-group').hide();
      } else {
        $('#tipocertificacion_set-group').hide();
        $('#certificadoempresa_set-group').hide();
      }
    });

		valor = $('#id_ingresosfamilia_set-0-respuesta').val();
    if (valor == 'Si') {
      $('#fuenteingresos_set-group').show();
    } else if (valor == 'No') {
      $('#fuenteingresos_set-group').hide();
    } else {
      $('#fuenteingresos_set-group').hide();
    }

		$('#id_ingresosfamilia_set-0-respuesta').change(function(){
			valor = $('#id_ingresosfamilia_set-0-respuesta').val();
			if (valor == 'Si') {
	      $('#fuenteingresos_set-group').show();
	    } else if (valor == 'No') {
	      $('#fuenteingresos_set-group').hide();
	    } else {
	      $('#fuenteingresos_set-group').hide();
	    }
		});

		valor = $('#id_condicionesriegos_set-0-sistema_riego').val();
    if (valor == 'Si') {
      $('.field-tipo_sistema_riego').show();
			$('.171-tipo-de-sistema-de-riego-posee').show();
			$('.field-estado_sistema_riego').show();
			$('.172-cual-es-el-estado-del-sistema-de-riego').show();
			$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').show();
			$('.field-area_sistema_riego').show();
    } else if (valor == 'No') {
			$('.field-tipo_sistema_riego').hide();
			$('.171-tipo-de-sistema-de-riego-posee').hide();
			$('.field-estado_sistema_riego').hide();
			$('.172-cual-es-el-estado-del-sistema-de-riego').hide();
			$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').hide();
			$('.field-area_sistema_riego').hide();
    } else {
			$('.field-tipo_sistema_riego').hide();
			$('.171-tipo-de-sistema-de-riego-posee').hide();
			$('.field-estado_sistema_riego').hide();
			$('.172-cual-es-el-estado-del-sistema-de-riego').hide();
			$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').hide();
			$('.field-area_sistema_riego').hide();
    }

		$('#id_condicionesriegos_set-0-sistema_riego').change(function(){
			valor = $('#id_condicionesriegos_set-0-sistema_riego').val();
			if (valor == 'Si') {
	      $('.field-tipo_sistema_riego').show();
				$('.171-tipo-de-sistema-de-riego-posee').show();
				$('.field-estado_sistema_riego').show();
				$('.172-cual-es-el-estado-del-sistema-de-riego').show();
				$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').show();
				$('.field-area_sistema_riego').show();
	    } else if (valor == 'No') {
				$('.field-tipo_sistema_riego').hide();
				$('.171-tipo-de-sistema-de-riego-posee').hide();
				$('.field-estado_sistema_riego').hide();
				$('.172-cual-es-el-estado-del-sistema-de-riego').hide();
				$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').hide();
				$('.field-area_sistema_riego').hide();
	    } else {
				$('.field-tipo_sistema_riego').hide();
				$('.171-tipo-de-sistema-de-riego-posee').hide();
				$('.field-estado_sistema_riego').hide();
				$('.172-cual-es-el-estado-del-sistema-de-riego').hide();
				$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').hide();
				$('.field-area_sistema_riego').hide();
	    }

		});

  });
})(jQuery || django.jQuery);
