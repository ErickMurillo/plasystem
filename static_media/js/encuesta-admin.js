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

		valor1 = $('#id_bpapregunta_set-0-respuesta').val();
    if (valor1 == 'Si') {
      $('#bpa_set-group').show();
    } else if (valor1 == 'No') {
      $('#bpa_set-group').hide();
    } else {
      $('#bpa_set-group').hide();
    }

    $('#id_bpapregunta_set-0-respuesta').change(function(){
      valor1 = $('#id_bpapregunta_set-0-respuesta').val();
			if (valor1 == 'Si') {
	      $('#bpa_set-group').show();
	    } else if (valor1 == 'No') {
	      $('#bpa_set-group').hide();
	    } else {
	      $('#bpa_set-group').hide();
	    }
    });

		valor2 = $('#id_ingresosfamilia_set-0-respuesta').val();
    if (valor2 == 'Si') {
      $('#fuenteingresos_set-group').show();
    } else if (valor2 == 'No') {
      $('#fuenteingresos_set-group').hide();
    } else {
      $('#fuenteingresos_set-group').hide();
    }

		$('#id_ingresosfamilia_set-0-respuesta').change(function(){
			valor2 = $('#id_ingresosfamilia_set-0-respuesta').val();
			if (valor2 == 'Si') {
	      $('#fuenteingresos_set-group').show();
	    } else if (valor2 == 'No') {
	      $('#fuenteingresos_set-group').hide();
	    } else {
	      $('#fuenteingresos_set-group').hide();
	    }
		});

		valor3 = $('#id_condicionesriegos_set-0-sistema_riego').val();
    if (valor3 == 'Si') {
      $('.field-tipo_sistema_riego').show();
			$('.171-tipo-de-sistema-de-riego-posee').show();
			$('.field-estado_sistema_riego').show();
			$('.172-cual-es-el-estado-del-sistema-de-riego').show();
			$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').show();
			$('.field-area_sistema_riego').show();
    } else if (valor3 == 'No') {
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
			valor4 = $('#id_condicionesriegos_set-0-sistema_riego').val();
			if (valor4 == 'Si') {
	      $('.field-tipo_sistema_riego').show();
				$('.171-tipo-de-sistema-de-riego-posee').show();
				$('.field-estado_sistema_riego').show();
				$('.172-cual-es-el-estado-del-sistema-de-riego').show();
				$('.173-cantidad-de-area-en-mz-bajo-sistema-de-riego').show();
				$('.field-area_sistema_riego').show();
	    } else if (valor4 == 'No') {
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
