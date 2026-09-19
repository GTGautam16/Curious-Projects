import { useEffect, useState } from "react";
import { getTickets, createTicket, deleteTicket, } from "./services/api";
import "./App.css";

function App() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({
    customer_name: "",
    title: "",
    description: "",
    priority: "medium",
  });

  const loadTickets = async () => {
    try {
      const data = await getTickets();
      setTickets(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load tickets");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTickets();
  }, []);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await createTicket(form);

      setForm({
        customer_name: "",
        title: "",
        description: "",
        priority: "medium",
      });

      await loadTickets();
    } catch (error) {
      console.error(error);
      alert("Failed to create ticket");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this ticket?")) {
      return;
    }

    try {
      await deleteTicket(id);
      await loadTickets();
    } catch (error) {
      console.error(error);
      alert("Failed to delete ticket");
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Support Ticket Dashboard</h1>
          <p>Customer support management system</p>
        </div>

        <div className="ticket-count">
          <strong>{tickets.length}</strong>
          <span>Total Tickets</span>
        </div>
      </header>

      <main className="container">
        <section className="card form-card">
          <h2>Create Ticket</h2>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label>Customer Name</label>
                <input
                  type="text"
                  name="customer_name"
                  value={form.customer_name}
                  onChange={handleChange}
                  placeholder="Enter customer name"
                  required
                />
              </div>

              <div className="form-group">
                <label>Priority</label>

                <select
                  name="priority"
                  value={form.priority}
                  onChange={handleChange}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Title</label>

              <input
                type="text"
                name="title"
                value={form.title}
                onChange={handleChange}
                placeholder="Enter ticket title"
                required
              />
            </div>

            <div className="form-group">
              <label>Description</label>

              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                placeholder="Describe the customer's problem"
                rows="4"
                required
              />
            </div>

            <button type="submit">
              Create Ticket
            </button>
          </form>
        </section>

        <section className="card">
          <div className="section-header">
            <h2>Tickets</h2>

            <button
              className="refresh-button"
              onClick={loadTickets}
            >
              Refresh
            </button>
          </div>

          {loading ? (
            <p>Loading tickets...</p>
          ) : tickets.length === 0 ? (
            <div className="empty-state">
              <h3>No tickets yet</h3>
              <p>Create your first support ticket above.</p>
            </div>
          ) : (
            <div className="tickets">
              {tickets.map((ticket) => (
                <div className="ticket" key={ticket.id}>
                  <div className="ticket-main">
                    <div className="ticket-title">
                      <h3>{ticket.title}</h3>

                      <span
                        className={`priority ${ticket.priority}`}
                      >
                        {ticket.priority}
                      </span>
                    </div>

                    <p className="customer">
                      Customer: {ticket.customer_name}
                    </p>

                    <p>{ticket.description}</p>

                    <span className="status">
                      {ticket.status}
                    </span>
                  </div>

                  <button
                    className="delete-button"
                    onClick={() => handleDelete(ticket.id)}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;