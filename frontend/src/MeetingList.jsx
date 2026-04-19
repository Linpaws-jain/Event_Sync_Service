export default function MeetingList({ meetings, onSelect }) {
  return (
    <div>
      <h2>Meetings</h2>
      <ul>
        {meetings.map(m => (
          <li key={m.id} onClick={() => onSelect(m.id)}>
            <b>{m.title}</b> – {m.start_time}
            {m.conflicts.length > 0 && <span> ⚠️</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}