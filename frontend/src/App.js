import LoginPage from "./Components/LoginPage";
import { useState } from "react";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  return (
    <>
      {loggedIn ? "welcome user :/" : <LoginPage setLoggedIn={setLoggedIn} />}
    </>
  );
}

export default App;
