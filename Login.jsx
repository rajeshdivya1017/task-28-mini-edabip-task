import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import api from "../services/api";


export default function Login() {

  const navigate =
    useNavigate();


  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  const handleSubmit =
    async (event) => {

      event.preventDefault();

      setError("");


      if (!email || !password) {

        setError(
          "Please enter email and password."
        );

        return;
      }


      try {

        setLoading(true);


        const response =
          await api.post(
            "/api/auth/login",
            {
              email,
              password
            }
          );


        localStorage.setItem(
          "access_token",
          response.data.access_token
        );


        localStorage.setItem(
          "user",
          JSON.stringify(
            response.data.user
          )
        );


        navigate(
          "/dashboard"
        );

      } catch (error) {

        setError(
          error.response?.data?.detail ||
          "Invalid email or password."
        );

      } finally {

        setLoading(false);
      }
    };


  return (

    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-header">

          <span className="logo-text">
            EDABIP
          </span>

          <h1>
            Welcome back
          </h1>

          <p>
            Sign in to your analytics dashboard
          </p>

        </div>


        {error && (

          <div className="error-message">
            {error}
          </div>

        )}


        <form
          onSubmit={handleSubmit}
        >

          <label>
            Email
          </label>

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
          />


          <label>
            Password
          </label>

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />


          <button
            className="primary-button"
            disabled={loading}
          >

            {loading
              ? "Signing in..."
              : "Sign In"}

          </button>

        </form>


        <p className="auth-footer">

          Don't have an account?{" "}

          <Link to="/signup">
            Create account
          </Link>

        </p>

      </div>

    </div>
  );
}