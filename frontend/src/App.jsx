import { useState } from "react";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

 const handleSubmit = async () => {
  if (!question) return;

  setLoading(true);

  const res = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const data = await res.json();
  setResult(data);
  setLoading(false);
};
  return (
  <div style={{ padding: "40px", textAlign: "center" }}>
    <h1>NavX Decision Engine 🚀</h1>

    <input
      type="text"
      placeholder="Enter your question"
      value={question}
      onChange={(e) => setQuestion(e.target.value)}
      style={{ padding: "10px", width: "300px", marginRight: "10px" }}
    />

    <button onClick={handleSubmit} disabled={loading}>
      {loading ? "Analyzing..." : "Analyze"}
    </button>

    {result && (
      <div style={{ marginTop: "20px" }}>
        <h2>✅ {result.final_decision}</h2>

        {result.options.map((opt, i) => (
          <div key={i}>
            <b>{opt.name} ({opt.status})</b>
            <p>Pros: {opt.pros.join(", ")}</p>
            <p>Cons: {opt.cons.join(", ")}</p>
          </div>
        ))}

        <p>{result.reasoning}</p>
      </div>
    )}
  </div>
);
}

export default App;