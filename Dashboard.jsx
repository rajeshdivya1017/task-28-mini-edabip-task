import {
  useEffect,
  useState
} from "react";

import {
  DollarSign,
  Users,
  ShoppingCart,
  Activity
} from "lucide-react";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import api from "../services/api";

import Layout from "../components/Layout";

import StatCard from "../components/StatCard";


export default function Dashboard() {

  const [kpis, setKpis] =
    useState(null);

  const [trend, setTrend] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  useEffect(() => {

    const loadDashboard =
      async () => {

        try {

          const [
            kpiResponse,
            trendResponse
          ] =
            await Promise.all([

              api.get(
                "/api/dashboard/kpis"
              ),

              api.get(
                "/api/dashboard/trend"
              )

            ]);


          setKpis(
            kpiResponse.data
          );

          setTrend(
            trendResponse.data
          );

        } catch {

          setError(
            "Unable to load dashboard data."
          );

        } finally {

          setLoading(false);
        }
      };


    loadDashboard();

  }, []);


  const currency =
    (value) => {

      return new Intl.NumberFormat(
        "en-IN",
        {
          style: "currency",
          currency: "INR",
          maximumFractionDigits: 0
        }
      ).format(
        Number(value || 0)
      );
    };


  return (

    <Layout>

      <div className="page-heading">

        <h1>
          Dashboard
        </h1>

        <p>
          Overview of your business performance
        </p>

      </div>


      {error && (

        <div className="error-message">
          {error}
        </div>

      )}


      {loading ? (

        <div className="loading-box">
          Loading dashboard...
        </div>

      ) : (

        <>

          <section className="stats-grid">

            <StatCard
              title="Total Revenue"
              value={
                currency(
                  kpis.total_revenue
                )
              }
              icon={
                <DollarSign
                  size={22}
                />
              }
              description="Completed transaction revenue"
            />


            <StatCard
              title="Active Users"
              value={
                kpis.active_users
              }
              icon={
                <Users
                  size={22}
                />
              }
              description="Currently active users"
            />


            <StatCard
              title="Total Orders"
              value={
                kpis.total_orders
              }
              icon={
                <ShoppingCart
                  size={22}
                />
              }
              description="Non-cancelled orders"
            />

          </section>


          <section className="dashboard-grid">

            <div className="chart-card">

              <div className="card-header">

                <div>

                  <h2>
                    Revenue Trend
                  </h2>

                  <p>
                    Monthly completed revenue
                  </p>

                </div>

                <Activity size={22} />

              </div>


              <div className="chart-container">

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <LineChart
                    data={trend}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                    />

                    <XAxis
                      dataKey="month"
                    />

                    <YAxis />

                    <Tooltip
                      formatter={(value) =>
                        currency(value)
                      }
                    />

                    <Line
                      type="monotone"
                      dataKey="revenue"
                      stroke="#5965db"
                      strokeWidth={3}
                    />

                  </LineChart>

                </ResponsiveContainer>

              </div>

            </div>


            <div className="info-card">

              <h2>
                Performance Summary
              </h2>


              <div className="summary-item">

                <span>
                  Revenue status
                </span>

                <strong>
                  Healthy
                </strong>

              </div>


              <div className="summary-item">

                <span>
                  Active users
                </span>

                <strong>
                  {kpis.active_users}
                </strong>

              </div>


              <div className="summary-item">

                <span>
                  Orders
                </span>

                <strong>
                  {kpis.total_orders}
                </strong>

              </div>

            </div>

          </section>

        </>

      )}

    </Layout>
  );
}