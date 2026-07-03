import { useEffect, useState } from "react";
import {
  getTickets,
  deleteTicket,
  changeStatus,
  createTicket,
} from "../api/ticket.ts";
import {
  loginAdmin
} from "../api/auth.ts";
import "../MainPage.css"

const BASE_URL = "http://localhost:8000/api/v1";

function MainPage() {

    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(false);
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    const [isCreateOpen, setIsCreateOpen] = useState(false);

    const [loginForm, setLoginForm] = useState({
      username: "",
      password: "",
    });

    const [createTicketForm, setCreateTicketForm] = useState({
      title: "",
      description: "",
      priority: "",
    });

    const [filters, setFilters] = useState({
      search: "",
      status: "",
      priority: "",
      sortBy: "",
      order: "asc",
      page: 1,
      limit: 10,
    });

    useEffect(() => {
      loadTickets();
    }, [filters]);

    async function loadTickets() {
      setLoading(true);
      const data = await getTickets(filters);
      console.log(data);

      console.log(Array.isArray(data));
      setTickets(data);
      setLoading(false);
    }
    async function handleDelete(id: number) {
        await deleteTicket(id);
        await loadTickets();
    }


    return (
        <>
        <header className="header">
          <div id="menu">
            <ul>
              <button className="button_log_in" onClick={() => setIsLoginOpen(true)}>
                Вход администратора
              </button>
            </ul>
          </div>
        </header>
        <div className="layout">

            <aside className="filters">

            <input
                type="text"
                placeholder="Поиск..."
                value={filters.search}
                onChange={(e) =>
                    setFilters({
                    ...filters,
                    search: e.target.value,
                })
            }
            />
                <p>Фильтр</p>
                <select
                    value={filters.status}
                    onChange={(e) =>
                        setFilters({
                            ...filters,
                            status: e.target.value,
                        })
                    }
                >
                    <option value="">Все статусы</option>
                    <option value="new">New</option>
                    <option value="in_progress">In Progress</option>
                    <option value="done">Done</option>
                </select>
                <select
                    value={filters.priority}
                    onChange={(e) =>
                        setFilters({
                        ...filters,
                        priority: e.target.value,
                    })
                    }
                >
                    <option value="">Все приоритеты</option>
                    <option value="low">Low</option>
                    <option value="normal">Normal</option>
                    <option value="high">High</option>
                </select>
                <p>Сортировка</p>
                <select
                    value={filters.sortBy}
                    onChange={(e) =>
                        setFilters({
                        ...filters,
                        sortBy: e.target.value,
                        })
                    }
                >
                    <option value="">Без сортировки</option>
                    <option value="created_at">Дата создания</option>
                    <option value="priority">Приоритет</option>
                </select>
                <select
                    value={filters.order}
                    onChange={(e) =>
                        setFilters({
                        ...filters,
                        order: e.target.value,
                        })
                    }
                >
                    <option value="asc">По возрастанию</option>
                    <option value="desc">По убыванию</option>
                </select>
                <div>
                    <button
                        disabled={filters.page === 1}
                        onClick={() =>
                        setFilters({ ...filters, page: filters.page - 1 })
                        }
                    >
                    Prev
                    </button>

                    <span>Page {filters.page}</span>

                    <button
                        onClick={() =>
                            setFilters({ ...filters, page: filters.page + 1 })
                        }
                    >
                    Next
                    </button>
                </div>
                <div><button className="button_create_ticket" onClick={() => setIsCreateOpen(true)}>
                    Создать заявку
                    </button >
                </div>
            </aside>
                <main className="tickets">
                    <div>Список заявок</div>
                    {loading && <p>Loading...</p>}

                    {!loading && tickets.length === 0 && <p>No tickets</p>}
                    {tickets.map((t) => (
                      <div key={t.id}>
                        <h3>{t.title}</h3>
                        <p>{t.description}</p>
                        <p>{t.status} | {t.priority}</p>

                        <p><select
                            value={t.status}
                            onChange={async (e) => {
                                await changeStatus(t.id, e.target.value);
                                await loadTickets();
                            }}
                        >
                            <option value="">Выбрать статус заявки</option>
                            <option value="in_progress">In Progress</option>
                            <option value="done">Done</option>
                        </select></p>

                        <button onClick={() => handleDelete(t.id)}>delete</button>
                      </div>
                    ))}
                </main>
        </div>

        {isLoginOpen && (
            <div
                style={{
                position: "fixed",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: "rgba(0,0,0,0.5)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                }}
            >
            <div
                style={{
                background: "white",
                padding: 20,
                borderRadius: 8,
                width: 300,
                }}
            >
        <h3>Вход администратора</h3>

            <p><input
                placeholder="username"
                value={loginForm.username}
                onChange={(e) =>
                  setLoginForm({ ...loginForm, username: e.target.value })
                }
            /></p>

            <p><input
                placeholder="password"
                type="password"
                value={loginForm.password}
                onChange={(e) =>
                  setLoginForm({ ...loginForm, password: e.target.value })
                }
            /></p>

            <p><button
                onClick={async () => {
                  await loginAdmin(loginForm);

                  setLoginForm ({
                      username: "",
                      password: "",
                  });

                  setIsLoginOpen(false);
                }}
                >
                Войти
            </button></p>

            <p><button onClick={() => setIsLoginOpen(false)}>
                Закрыть
            </button></p>
            </div>
        </div>
        )}

        {isCreateOpen && (
            <div
                style={{
                position: "fixed",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: "rgba(0,0,0,0.5)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                }}
            >
            <div
                style={{
                background: "white",
                padding: 20,
                borderRadius: 8,
                width: 300,
                }}
            >
        <h3>Создание заявки</h3>

            <p><input
                placeholder="title"
                value={createTicketForm.title}
                onChange={(e) =>
                  setCreateTicketForm({ ...createTicketForm, title: e.target.value })
                }
            /></p>

            <p><input
                placeholder="description"
                value={createTicketForm.description}
                onChange={(e) =>
                  setCreateTicketForm({ ...createTicketForm, description: e.target.value })
                }
            /></p>
            <p><select
                placeholder="priority"
                value={createTicketForm.priority}
                onChange={(e) =>
                  setCreateTicketForm({ ...createTicketForm, priority: e.target.value })
                }
            >
                <option value="">Выберите приоритет</option>
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
            </select>
            </p>

            <p><button
                onClick={async () => {
                  await createTicket(createTicketForm);
                  await loadTickets();

                  setCreateTicketForm({
                    title: "",
                    description: "",
                    priority: "",
                  });
                  setIsCreateOpen(false);
                }}
                >
                Создать
            </button></p>

            <p><button onClick={() => setIsCreateOpen(false)}>
                Закрыть
            </button></p>
        </div>
        </div>
        )}
      </>
    );
}

export default MainPage;