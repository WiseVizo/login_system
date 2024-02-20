import { useState } from "react";
function LoginPage({ setLoggedIn }) {
  async function handleLogin() {
    const res = await fetch(`http://127.0.0.1:5000/react/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: userName,
        password: password,
        email: email,
      }),
    });
    const data = await res.json();
    if (data.task === "success") {
      setLoggedIn(true);
    }
  }
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  return (
    <>
      <label>Username:</label>
      <input
        key="username"
        type="text"
        required
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      <br />
      <label>Password:</label>
      <input
        key="password"
        type="text"
        required
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />

      <label>Email:</label>
      <input
        key="email"
        type="text"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <button onClick={handleLogin}>Login</button>
    </>
  );
}

export default LoginPage;
