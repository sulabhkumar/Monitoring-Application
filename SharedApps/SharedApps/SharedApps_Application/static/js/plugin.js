$(document).ready(function(){
	var ShowForm = function(){
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType:'json',
			beforeSend: function(){
				$('#modal-certificate').modal('show');
			},
			success: function(data){
				$('#modal-certificate .modal-content').html(data.html_form);
			}
		});
	};
	var SaveForm =  function(e){
		e.preventDefault();
		var form = $(this);
        $form = $(this);
        var formData = new FormData(this);

		// var form = $(this);
		// console.log('form',form);
		// console.log('sulabh');
		// data=form.serialize();
		// console.log('data',data);
		// var formData = new FormData(form);
		 console.log('formData',formData);
		
		$.ajax({

			url: form.attr('data-url'),
			type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
			// data: form.serialize(),
			// type: form.attr('method'),
			dataType: 'json',
			success: function(data){
				if(data.form_is_valid){
					$('#Certificate-table tbody').html(data.list);
					$('#modal-certificate').modal('hide');
					jQuery("body").load(window.location.href);
				} else {
					$('#modal-certificate .modal-content').html(data.html_form)
					
				}
			}
		})
		return false;
	}
// create 
$(".show-form").click(ShowForm);
$("#modal-certificate").on("submit",".create-form",SaveForm);

//update
$('#Certificate-table').on("click",".show-form-update",ShowForm);
$('#modal-certificate').on("submit",".update-form",SaveForm)

//delete
$('#Certificate-table').on("click",".show-form-delete",ShowForm);
$("#modal-certificate").on("submit",".delete-form",SaveForm);

});