import {
  useEffect,
  useState
} from "react";

import {
  Search,
  ChevronLeft,
  ChevronRight
} from "lucide-react";

import api from "../services/api";

import Layout from "../components/Layout";


export default function Reports() {

  const [
    transactions,
    setTransactions
  ] = useState([]);


  const [search, setSearch] =
    useState("");

  const [category, setCategory] =
    useState("All");

  const [startDate, setStartDate] =
    useState("");

  const [endDate, setEndDate] =
    useState("");


  const [page, setPage] =
    useState(1);

  const [pagination, setPagination] =
    useState(null);

  const [loading, setLoading] =
    useState(false);


  const loadTransactions =
    async () => {

      try {

        setLoading(true);


        const response =
          await api.get(
            "/api/transactions",
            {
              params: {

                search:
                  search || undefined,

                category:
                  category === "All"
                    ? undefined
                    : category,

                start_date:
                  startDate || undefined,

                end_date:
                  endDate || undefined,

                page,

                page_size: 10
              }
            }
          );


        setTransactions(
          response.data.items
        );

        setPagination(
          response.data
        );

      } finally {

        setLoading(false);
      }
    };


  useEffect(() => {

    loadTransactions();

  }, [
    search,
    category,
    startDate,
    endDate,
    page
  ]);


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
        Number(value)
      );
    };


  return (

    <Layout>

      <div className="page-heading">

        <h1>
          Reports
        </h1>

        <p>
          Search, filter and analyze transactions
        </p>

      </div>


      <section className="table-card">


        <div className="filters">


          <div className="search-box">

            <Search size={18} />

            <input
              placeholder="Search order, customer or category..."
              value={search}
              onChange={(e) => {

                setSearch(
                  e.target.value
                );

                setPage(1);

              }}
            />

          </div>


          <select
            className="filter-select"
            value={category}
            onChange={(e) => {

              setCategory(
                e.target.value
              );

              setPage(1);

            }}
          >

            <option value="All">
              All Categories
            </option>

            <option value="Electronics">
              Electronics
            </option>

            <option value="Furniture">
              Furniture
            </option>

            <option value="Clothing">
              Clothing
            </option>

          </select>


          <input
            className="date-input"
            type="date"
            value={startDate}
            onChange={(e) => {

              setStartDate(
                e.target.value
              );

              setPage(1);

            }}
          />


          <input
            className="date-input"
            type="date"
            value={endDate}
            onChange={(e) => {

              setEndDate(
                e.target.value
              );

              setPage(1);

            }}
          />

        </div>


        <div className="table-wrapper">

          <table>

            <thead>

              <tr>

                <th>
                  Order
                </th>

                <th>
                  Customer
                </th>

                <th>
                  Category
                </th>

                <th>
                  Amount
                </th>

                <th>
                  Status
                </th>

                <th>
                  Date
                </th>

              </tr>

            </thead>


            <tbody>

              {loading ? (

                <tr>

                  <td
                    colSpan="6"
                    className="table-message"
                  >
                    Loading...
                  </td>

                </tr>

              ) : transactions.length === 0 ? (

                <tr>

                  <td
                    colSpan="6"
                    className="table-message"
                  >
                    No transactions found.
                  </td>

                </tr>

              ) : (

                transactions.map(
                  (item) => (

                    <tr key={item.id}>

                      <td>
                        <strong>
                          {item.order_number}
                        </strong>
                      </td>

                      <td>
                        {item.customer_name}
                      </td>

                      <td>
                        <span className="category-badge">
                          {item.category}
                        </span>
                      </td>

                      <td>
                        {currency(
                          item.amount
                        )}
                      </td>

                      <td>

                        <span
                          className={
                            `status-badge ${item.status.toLowerCase()}`
                          }
                        >
                          {item.status}
                        </span>

                      </td>

                      <td>
                        {item.transaction_date}
                      </td>

                    </tr>

                  )
                )

              )}

            </tbody>

          </table>

        </div>


        {pagination && (

          <div className="pagination">

            <span>

              Showing{" "}
              {transactions.length}{" "}
              of{" "}
              {pagination.total}

            </span>


            <div className="pagination-buttons">

              <button
                disabled={
                  page <= 1
                }
                onClick={() =>
                  setPage(
                    page - 1
                  )
                }
              >

                <ChevronLeft
                  size={18}
                />

              </button>


              <span>
                Page {page} of{" "}
                {pagination.total_pages}
              </span>


              <button
                disabled={
                  page >=
                  pagination.total_pages
                }
                onClick={() =>
                  setPage(
                    page + 1
                  )
                }
              >

                <ChevronRight
                  size={18}
                />

              </button>

            </div>

          </div>

        )}

      </section>

    </Layout>
  );
}