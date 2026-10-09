import {
  useState
} from "react";

import {
  Link,
  useNavigate
} from "react-router-dom";

import api from "../services/api";


export default function Signup() {

  const navigate =
    useNavigate();


  const [form, setForm] =
    useState({
      name: "",
      email: "",
      password: "",
      confirmPassword: ""
    });


  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  const handleChange =
    (event) => {

      setForm({
        ...form,
        [event.target.name]:
          event.target.value
      });

    };


  const handleSubmit =
    async (event) => {

      event.preventDefault();

      setError("");


      if (
        !form.name ||
        !form.email ||
        !form.password ||
        !form.confirmPassword
      ) {

        setError(
          "Please fill in all fields."
        );

        return;
      }


      if (
        form.password.length < 6
      ) {

        setError(
          "Password must contain at least 6 characters."
        );

        return;
      }


      if (
        form.password !==
        form.confirmPassword
      ) {

        setError(
          "Passwords do not match."
        );

        return;
      }


      try {

        setLoading(true);


        await api.post(
          "/api/auth/signup",
          {
            name: form.name,
            email: form.email,
            password: form.password
          }
        );


        navigate(
          "/login"
        );

      } catch (error) {

        setError(
          error.response?.data?.detail ||
          "Signup failed."
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
            Create account
          </h1>

          <p>
            Create your dashboard account
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
            Full Name
          </label>

          <input
            name="name"
            placeholder="Your name"
            value={form.name}
            onChange={handleChange}
          />


          <label>
            Email
          </label>

          <input
            name="email"
            type="email"
            placeholder="you@example.com"
            value={form.email}
            onChange={handleChange}
          />


          <label>
            Password
          </label>

          <input
            name="password"
            type="password"
            placeholder="Minimum 6 characters"
            value={form.password}
            onChange={handleChange}
          />


          <label>
            Confirm Password
          </label>

          <input
            name="confirmPassword"
            type="password"
            placeholder="Confirm password"
            value={
              form.confirmPassword
            }
            onChange={handleChange}
          />


          <button
            className="primary-button"
            disabled={loading}
          >

            {loading
              ? "Creating..."
              : "Create Account"}

          </button>

        </form>


        <p className="auth-footer">

          Already have an account?{" "}

          <Link to="/login">
            Sign in
          </Link>

        </p>

      </div>

    </div>
  );
}