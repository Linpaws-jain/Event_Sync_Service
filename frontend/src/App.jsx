import { useEffect, useState } from "react";
import { fetchMeetings, fetchMeeting } from "./api";
import MeetingList from "./MeetingList";
import MeetingDetail from "./MeetingDetail";

function App() {
  const [meetings, setMeetings] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetchMeetings().then(setMeetings);
  }, []);

  if (selected !== null) {
    return (
      <MeetingDetail
        meeting={selected}
        onBack={() => setSelected(null)}
      />
    );
  }

  return (
    <MeetingList
      meetings={meetings}
      onSelect={(id) => fetchMeeting(id).then(setSelected)}
    />
  );
}

export default App