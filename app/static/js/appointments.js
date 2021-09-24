
let appointment = {};
appointment.data = [];

const handleLoadUpsertModal = async (mode, apptId, selectedDate) => {
  let payload = {};
  if (apptId)
    payload["id"] = apptId
  if (selectedDate)
    payload['selected_date'] = selectedDate
  
  return await $.ajax({
    url: "/admin/appointments/view/upsert",
    type: "POST",
    data: payload
  });
};

$(document).ready(() => {
  $("#saveAppt").click((e) => {
    $("#apptForm").submit();
  });
  
  $("#addAppointment").click((e) => {
    (async () => {
      const formContent = await handleLoadUpsertModal("add");
      $("#appointmentUpsertModalLabel").text("New Appointment");
      $("#appointmentUpsertModal").find(".modal-body").html(formContent);
      $("#appointmentUpsertDelForm").hide();
      $("#appointmentUpsertModal").modal('show');
    })();
  });
  
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: appointment.data,
    eventClick: function(info) {
      (async () => {
        const formContent = await handleLoadUpsertModal("edit", info.event.id);
        $("#appointmentUpsertModalLabel").text("Edit Appointment");
        $("#appointmentUpsertModal").find(".modal-body").html(formContent);
        $("#appointmentUpsertDelForm").show();
        $("#appointmentUpsertModal").modal('show');
        // set the action path for deleting form
        $("#appointmentUpsertDelForm").attr('action', `/admin/appointments/${info.event.id}/delete`);
      })();
    },
    dateClick: function(info) {
      (async () => {
        const formContent = await handleLoadUpsertModal("add", null, info.dateStr);
        $("#appointmentUpsertModalLabel").text("New Appointment");
        $("#appointmentUpsertModal").find(".modal-body").html(formContent);
        $("#appointmentUpsertDelForm").hide();
        $("#appointmentUpsertModal").modal('show');
      })();
    }
  });
  calendar.render();
});
