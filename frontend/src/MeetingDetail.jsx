export default function MeetingDetail({ meeting, onBack }) {
  const { location } = meeting;

  return (
    <div>
      <button onClick={onBack}>← Back</button>
      <h2>{meeting.title}</h2>

      <p><b>Start:</b> {meeting.start_time}</p>
      <p><b>Client:</b> {meeting.client_company}</p>

      <h3>Location</h3>
      <p><b>Final:</b> {location.value} ({location.source})</p>

      {location.conflict && (
        <>
          <p>Calendar: {location.calendar}</p>
          <p>CRM: {location.crm}</p>
        </>
      )}

      <h4>Sources</h4>
      <pre>{JSON.stringify(meeting.sources, null, 2)}</pre>
    </div>
  );
}