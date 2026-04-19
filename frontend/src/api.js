const API = "http://localhost:8000/api";

export const fetchMeetings = async () =>
  fetch(`${API}/meetings`).then(r => r.json());

export const fetchMeeting = async (id) =>
  fetch(`${API}/meetings/${id}`).then(r => r.json());