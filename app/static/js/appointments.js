
let appointment = {};
appointment.data = [];

$(document).ready(() => {
  console.log(":>",appointment.data)
  
  $("#saveAppt").click((e) => {
    $("#apptForm").submit();
  });
  
  $("#addAppointment").click((e) => {
    (async () => {
      const formContent = await $.ajax({
        url: "/admin/appointments/view/upsert",
        type: "POST"
      });
      $("#appointmentUpsertModalLabel").text("New Appointment");
      $("#appointmentUpsertModal").find(".modal-body").html(formContent);
      $("#appointmentUpsertModal").modal('show');
    })();
  });
  
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    timeZone: 'UTC',
    events: appointment.data,
    eventClick: function(info) {
      (async () => {
        const formContent = await $.ajax({
          url: "/admin/appointments/view/upsert",
          type: "POST",
          data: {id: info.event.id}
        });
        $("#appointmentUpsertModalLabel").text("Edit Appointment");
        $("#appointmentUpsertModal").find(".modal-body").html(formContent);
        $("#appointmentUpsertDelForm").attr('action', `/admin/appointments/${info.event.id}/delete`)
        $("#appointmentUpsertModal").modal('show');
      })();
      // change the border color just for fun
      // info.el.style.borderColor = 'red';
    },
    dateClick: function() {
      alert('a day has been clicked!');
    }
  });
  calendar.render();
});
