document.addEventListener('DOMContentLoaded', function() {

 document.querySelector('#createjob').addEventListener('click', function() {
        if (document.querySelector('#createjobview').style.display === 'none') {
        document.querySelector('#createjobview').style.display = 'block';
        } else {
            document.querySelector('#createjobview').style.display = 'none';
        }
    });
    document.querySelector('#createjobview').style.display = 'none';



 document.querySelector('#timeslotcreation').addEventListener('click', function() {
        if (document.querySelector('#overallview').style.display === 'none') {
        document.querySelector('#overallview').style.display = 'block';
        } else {
            document.querySelector('#overallview').style.display = 'none';
        }
    });




   $(function() {
  $("#addMore").click(function(e) {
    e.preventDefault();
    $("#timeslotview").append("&nbsp;");
    $("#timeslotview").append("<input name='day' type='date' class='form-control' placeholder='Day of the week with Date'>");
    $("#timeslotview").append("<input name='time' type='time' class='form-control' placeholder='Time'>");
  });
});


 document.querySelector('#createjobview').style.display = 'none';

 document.querySelector('#reloadmaster').onclick = function() {
  window.location.reload()
 };







  $('#datetimepicker1').datetimepicker({
   // dateFormat: 'dd-mm-yy',
   format:'dddd DD MMMM YYYY hh:mm A',
    //minDate: getFormattedDate(new Date())
});

});
