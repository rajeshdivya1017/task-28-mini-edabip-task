import {
  LogOut
} from "lucide-react";

import {
  useNavigate
} from "react-router-dom";


export default function Navbar() {

  const navigate =
    useNavigate();

  const user =
    JSON.parse(
      localStorage.getItem(
        "user"
      ) || "null"
    );


  const logout = () => {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );

    navigate(
      "/login"
    );
  };


  return (

    <header className="navbar">

      <div>

        <h2>
          Analytics Dashboard
        </h2>

        <span>
          Welcome,{" "}
          {user?.name || "User"}
        </span>

      </div>


      <button
        className="logout-button"
        onClick={logout}
      >

        <LogOut size={18} />

        Logout

      </button>

    </header>
  );
}