export default {
  async fetch(request, env) {
    const allowedOrigin = "https://ansh44233.github.io";
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": allowedOrigin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin"
    };
    if (request.method === "OPTIONS") {
      if (origin !== allowedOrigin) return new Response(null, { status: 403 });
      return new Response(null, { headers: cors });
    }
    if (origin !== allowedOrigin) return json({ error: "Origin not allowed." }, 403, cors);
    if (request.method !== "POST") return json({ error: "Use POST." }, 405, cors);
    try {
      const body = await request.json();
      const message = typeof body.message === "string" ? body.message.trim() : "";
      if (!message || message.length > 1200) return json({ error: "Message must contain 1–1200 characters." }, 400, cors);
      const history = Array.isArray(body.history) ? body.history.slice(-8) : [];
      const messages = [
        { role: "system", content: "You are JARVIS, a polished, friendly, intelligent personal assistant. Respond naturally and conversationally to greetings, casual chat, questions, and Hinglish or English. Be concise by default, but explain clearly when needed. Never pretend to access the visitor's device, private files, accounts, or perform actions. This is a public demo: you cannot persist or execute real tasks, notes, reminders, or control hardware. Explain that demo workspace commands are simulated in the browser when relevant. Do not provide unsafe instructions." },
        ...history.filter(x => x && ["user", "assistant"].includes(x.role) && typeof x.content === "string").map(x => ({ role: x.role, content: x.content.slice(0, 1200) })),
        { role: "user", content: message }
      ];
      const result = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", { messages, max_tokens: 450 });
      const reply = result?.response?.trim();
      if (!reply) return json({ error: "The AI model returned an empty response." }, 502, cors);
      return json({ reply }, 200, cors);
    } catch (error) {
      return json({ error: "JARVIS AI is temporarily unavailable. Please try again." }, 502, cors);
    }
  }
};
function json(data, status, headers = {}) {
  return new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json; charset=utf-8", ...headers } });
}
