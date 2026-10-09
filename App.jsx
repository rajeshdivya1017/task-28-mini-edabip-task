import {
  Navigate,
  Route,
  Routes
} from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Reports from "./pages/Reports";


function ProtectedRoute({
  children
}) {

  const token =
    localStorage.getItem(
      "access_token"
    );

  if (!token) {

    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  return children;
}


export default function App() {

  return (

    <Routes>

      <Route
        path="/"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />


      <Route
        path="/login"
        element={
          <Login />
        }
      />


      <Route
        path="/signup"
        element={
          <Signup />
        }
      />


      <Route
        path="/dashboard"
        element={

          <ProtectedRoute>

            <Dashboard />

          </ProtectedRoute>

        }
      />


      <Route
        path="/reports"
        element={

          <ProtectedRoute>

            <Reports />

          </ProtectedRoute>

        }
      />


      <Route
        path="*"
        element={
          <Navigate
            to="/login"
            replace
          />
        }
      />

    </Routes>
  );
}