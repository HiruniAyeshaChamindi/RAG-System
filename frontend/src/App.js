import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Header from './components/header/Header.js';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer('');
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:5000/ask', {
        question,
      });

      setAnswer(response.data.answer);
    } catch (err) {
      setError('Error fetching answer. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      <textarea
        placeholder="Ask a registration question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        rows={3}
        cols={60}
      />
      <br />
      <button onClick={handleAsk} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>
      <div className="output">
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {answer && (
          <>
            <h3>🤖 Answer:</h3>
            <p>{answer}</p>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
