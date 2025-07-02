<?php
namespace Unifesp\cep_autofill;

use ExternalModules\AbstractExternalModule;
//use RCView;

class cep_autofill extends AbstractExternalModule
{
/*    function redcap_every_page_top($project_id) {
	    ?><script>console.log("alo");</script><?php
        if (PAGE == 'DataEntry/index.php' || PAGE == 'surveys/index.php') {
            $this->includeJs("js/cep_autofill.js");
        }
    }
 */

    function redcap_data_entry_form($project_id, $record, $instrument, $event_id, $group_id, $repeat_instance)
    {
 //           $this->includeJs("js/cep_autofill.js");
	?><script>
	const API_URL = 'https://redcap.unifesp.br:8000';
	const cepInput = $('input[name="cep"]');    
	cepInput.on('blur', function(){   
		cep = cepInput.val().replace(/\D/g, '');	
	        if (cep.length === 8) {
			fetch(`${API_URL}/${cep}`, {
		            method: 'GET',
		            mode: 'cors',
		            credentials: 'include'
		           })
			   .then(response => response.json())
		           .then(data => {
			   	if (data.detail) {
					alert(data.detail);
					$('input[name=logradouro]').val('');
					$('input[name=bairro]').val('');
					$('input[name=cidade]').val('');
				}
          		      	if (data.logradouro) {
	                	    $('input[name=logradouro]').val(data.logradouro);
		                }
		                if (data.bairro) {
		                    $('input[name=bairro]').val(data.bairro);
		                }
		                if (data.cidade) {
		                    $('input[name=cidade]').val(data.cidade);
		                }
				})
				//.fail(function () {
        	       		// alert("CEP não encontrado no servidor externo.");
				//});
				.catch(error => console.error('Error:', error));
			}
		else {
			alert("Entre CEP com 8 dígitos.");
			$('input[name=logradouro]').val('');
			$('input[name=bairro]').val('');
			$('input[name=cidade]').val('');

		}
		
		} );
	    
	    </script><?php
	        print '<div class="yellow">Special announcement text to display at the very bottom
			            of every data entry form.</div>';
	$this->log("Entrou no form versão 2");
     }

/*    function redcap_project_home_page($project_id) {

        // Define attributes for html elements
        $button_attributes = [
            'class' => 'btn btn-primary',
            'id' => 'incrementButton'
        ];
        $button_text = "Click to increment";

        // call a prebuilt button maker
        echo RCView::button($button_attributes, $button_text);

        echo RCView::p(['id' => 'incrementValue'], '0');

        // FIXME
        // include a JavaScript file that increments the contents of incrementValue
        // upon clicking the incrementButton
        /* write your code below */
//    }

}
