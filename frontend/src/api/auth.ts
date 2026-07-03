const BASE_URL = "http://localhost:8000/api/v1";

export async function loginAdmin(dataUser: {
  username: string;
  password: string;
}) {
  const formData = new URLSearchParams();

  formData.append("username", dataUser.username);
  formData.append("password", dataUser.password);

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  const data = await res.json();
  localStorage.setItem("token", data.access_token);

  return data;
}