
let appointment = {};
appointment.data = [];

$(document).ready(() => {
  console.log(":>",appointment.data)

  $("#addAppointment").click((e) => {
    (async () => {
      const resp = await fetch("/admin/appointments/view/upsert");
      const formContent = await resp.text();
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
      $("#appointmentDetailModelLabel").text(info.event.title);
      $("#appointmentDetailModel").modal('show');
      $("#appointmentDetailDel").attr('action', `/admin/appointments/${info.event.id}/delete`);
  
      // change the border color just for fun
      // info.el.style.borderColor = 'red';
    },
    dateClick: function() {
      alert('a day has been clicked!');
    }
  });
  calendar.render();
});
