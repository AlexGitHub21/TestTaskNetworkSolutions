const BASE_URL = "http://localhost:8000/api/v1";

export async function getTickets(filters: any) {
    const params = {
        search: filters.search,
        status: filters.status,
        priority: filters.priority,
        sort_by: filters.sortBy,
        order: filters.order,
        limit: filters.limit,
        page: filters.page,
        offset: (filters.page - 1) * filters.limit,
    };
  const query = new URLSearchParams(params).toString();

  const res = await fetch(`${BASE_URL}/tickets?${query}`);
  return res.json();
}

export async function deleteTicket(id: number) {
  await fetch(`${BASE_URL}/tickets/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });

}

export async function changeStatus(id: number, status: string) {
  await fetch(`${BASE_URL}/tickets/${id}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify( status ),
  });

}

export async function createTicket(dataTicket: {
    title: string;
    description: string;
    priority: string;
    }) {

    const res = await fetch(`${BASE_URL}/tickets/create_ticket`, {
        method: "POST",
        headers: {
      "Content-Type": "application/json",
        },

        body: JSON.stringify(dataTicket),
    });

    return await res.json();
}