$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-service_account').modal('show');
			},
			success: function(data){
				$('#modal-service_account .modal-content').html(data.html_form);
			}
		});
	};
	var SaveForm =  function(){
		var form = $(this);

		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('#service_account-table tbody').html(data.service_account_list);
					$('#modal-service_account').modal('hide');
					jQuery("body").load(window.location.href);
				} else {
					$('#modal-service_account .modal-content').html(data.html_form)
					
				}
			}
		})
		return false;
	}
// create 
$(".show-form").click(ShowForm);
$("#modal-service_account").on("submit",".create-form",SaveForm);

//update
$('#service_account-table').on("click",".show-form-update",ShowForm);
$('#modal-service_account').on("submit",".update-form",SaveForm)

//delete
$('#service_account-table').on("click",".show-form-delete",ShowForm);
$("#modal-service_account").on("submit",".delete-form",SaveForm);

});