$(function () {
  var reg_status = '';
  var progress = 0;
  $(".js-upload-photos").click(function () {
    let files = $(this)[0].files;
    let files_count = $("#files_count").val();
    let files_count_limit = $("#files_count_limit").val();
    reg_status = parseInt($("#reg_status").val());
    
    if (files_count < 10) {
      $("#fileupload").click();
    } else {
      let str = `Превышен лимит на количество загружаемых файлов!`
      str += `\n\nОграничение на количество файлов - ${files_count_limit}`
      str += `\n\nУже загружено ${files_count} файлов.`
      str += ` Файлы можно заменить друними в личном кабинете`
      alert(str);
      if (reg_status == 100) {
        window.location.href = "diploma_actions";
       } ;
      return 0
    }
    
  });


  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,
    
    start: function (e) {
      $("#modal-progress").modal("show");
    },


    stop: function (e) {
      $('#modal-progress').modal("hide");
      // $("#modal-progress").on("shown.bs.modal", function () {
      //   $('#modal-progress').modal("hide");
      // })
    },

    progressall: function (e, data) {
      // alert(reg_status);
      progress = parseInt(data.loaded / data.total * 100, 10);
      let strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").tprogress1 = progress
    },
    
    done: function (e, data) {
      if (data.result.is_valid) {
      	if (progress === 100 && data.result.reg_status == 100) {
      	 window.location.href = "diploma_actions";
      	};
        $("#gallery tbody").prepend(
            "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        )
      } else {
        alert(data.result.error_message);
      }
    }

  });

});
