import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [latestMessage, setLatestMessage] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch latest message from backend via reverse proxy (/api/message)
  const fetchLatestMessage = async () => {
    try {
      const response = await fetch('/api/message');
      if (response.ok) {
        const data = await response.json();
        setLatestMessage(data.message);
      } else {
        setStatus('Failed to load latest message from backend.');
      }
    } catch (err) {
      console.error(err);
      setStatus('Backend unreachable. Check reverse proxy and backend containers.');
    }
  };

  useEffect(() => {
    fetchLatestMessage();
  }, []);

  // Save new message via POST /api/message
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setLoading(true);
    setStatus('');

    try {
      const response = await fetch('/api/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (response.ok) {
        setInputText('');
        setStatus('Message successfully saved!');
        await fetchLatestMessage();
      } else {
        const errorData = await response.json().catch(() => ({}));
        setStatus(errorData.error || 'Failed to save message.');
      }
    } catch (err) {
      console.error(err);
      setStatus('Network error when attempting to reach backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Docker Flask + React Lab</h1>
        <p className="subtitle">Production Architecture (Nginx Reverse Proxy + Dual Networks)</p>
      </header>

      <main className="card">
        <form onSubmit={handleSubmit} className="form-group">
          <label htmlFor="message-input" className="input-label">
            Enter a Message:
          </label>
          <div className="input-row">
            <input
              id="message-input"
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your message here..."
              disabled={loading}
              className="text-input"
            />
            <button
              id="save-button"
              type="submit"
              disabled={loading || !inputText.trim()}
              className="save-button"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>

        {status && <div className="status-banner">{status}</div>}

        <div className="message-display">
          <span className="display-label">Latest Saved Message:</span>
          <p id="latest-message" className="message-content">
            {latestMessage ? `"${latestMessage}"` : 'No messages stored yet.'}
          </p>
        </div>
      </main>

      <footer className="footer">
        <p>Entry: Nginx Proxy (8080) | Frontend & Backend on frontend-net | Backend & DB on database-net (internal)</p>
      </footer>
    </div>
  );
}

export default App;
