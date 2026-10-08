import React, {useState} from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

const API="http://localhost:5000";
const sample=`def calculate_total(items):\n    total = 0\n    for item in items:\n        if item["active"]:\n            total += item["price"]\n    return total`;

function Metric({title,value}){return <div className="metric"><span>{title}</span><strong>{value}</strong></div>}
function App(){
 const [code,setCode]=useState(sample),[result,setResult]=useState(null),[loading,setLoading]=useState(false),[error,setError]=useState("");
 async function analyze(){setLoading(true);setError("");setResult(null);try{const r=await fetch(`${API}/api/analyze`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code})});const d=await r.json();if(!r.ok)throw new Error(d.error||"Analysis failed.");setResult(d)}catch(e){setError(`${e.message} Make sure the Flask backend is running on port 5000.`)}finally{setLoading(false)}}
 return <main className="page">
  <nav className="nav"><div><span className="eyebrow">Developer Tool</span><h1>Code Quality Review</h1></div><span className="status">Local analysis</span></nav>
  <section className="hero"><h2>Find problems before they become bugs.</h2><p>Paste Python code and get a quick report on syntax, complexity, error handling and maintainability.</p></section>
  <section className="workspace">
   <div className="panel"><div className="panel-head"><div><span className="label">Source code</span><span className="muted">Python</span></div><button className="secondary" onClick={()=>setCode("")}>Clear</button></div><textarea value={code} onChange={e=>setCode(e.target.value)} spellCheck="false"/><button className="primary" onClick={analyze} disabled={loading}>{loading?"Analyzing...":"Run analysis"}</button>{error&&<div className="error">{error}</div>}</div>
   <div className="panel report"><div className="panel-head"><span className="label">Review report</span>{result&&<span className="muted">{result.lines} lines</span>}</div>
    {!result?<div className="empty"><div className="empty-icon">⌁</div><h3>Your report will appear here</h3><p>Run an analysis to see quality score, complexity, issues and suggestions.</p></div>:<>
     <div className="metrics"><Metric title="Quality score" value={`${result.score}/100`}/><Metric title="Complexity" value={result.complexity}/><Metric title="Functions" value={result.functions}/></div>
     <div className="section"><h3>Issues</h3>{result.issues.length===0?<p className="good">No major issues detected.</p>:result.issues.map((i,n)=><div className="issue" key={n}><div><strong>{i.title}</strong><p>{i.detail}</p></div><span className={`severity ${i.severity}`}>{i.severity}</span></div>)}</div>
     <div className="section"><h3>Suggestions</h3><ul className="suggestions">{result.suggestions.map((s,n)=><li key={n}>{s}</li>)}</ul></div>
    </>}
   </div>
  </section><footer>Flask REST API · React · Python AST · SQL database</footer>
 </main>
}
ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
