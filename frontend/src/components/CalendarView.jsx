import FullCalendar from "@fullcalendar/react";
import timeGridPlugin from "@fullcalendar/timegrid";
import dayGridPlugin from "@fullcalendar/daygrid";

export default function CalendarView({ events }) {
  return (
    <div style={{ background: "#fff", borderRadius: 12, padding: 12 }}>
      <FullCalendar
        plugins={[timeGridPlugin, dayGridPlugin]}
        initialView="timeGridDay"
        height={650}
        slotMinTime="06:00:00"
        slotMaxTime="23:00:00"
        headerToolbar={{
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        }}
        events={events}
        eventTimeFormat={{
    hour: 'numeric',
    minute: '2-digit',
    meridiem: 'short'
  }}
      />
    </div>
  );
}
