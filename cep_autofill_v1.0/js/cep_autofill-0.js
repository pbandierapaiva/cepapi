const cepField = 'cep';           
const logradouroField = 'logradouro';
const bairroField = 'bairro';
const cidadeField = 'cidade';

const API_URL = 'http://localhost:8000';  // FastAPI endpoint

$(function () {
    //const cepInput = $('input[name="__field__' + cepField + '"]');
    const cepInput = $('input[name=' + cepField + ']');

	alert("Alo 1 !!");
    cepInput.on('blur', function () {
        const cep = $(this).val().replace(/\D/g, '');
	alert("Alo!!");
        if (cep.length === 8) {
            $.get(`${API_URL}/${cep}`, function (data) {
                if (data.logradouro) {
                    $('input[name="__field__' + logradouroField + '"]').val(data.logradouro);
                }
                if (data.bairro) {
                    $('input[name="__field__' + bairroField + '"]').val(data.bairro);
                }
                if (data.cidade) {
                    $('input[name="__field__' + cidadeField + '"]').val(data.cidade);
                }
            }).fail(function () {
                alert("CEP não encontrado no servidor externo.");
            });
        }
    });
});

