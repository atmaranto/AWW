defmodule IndexWeb.PageController do
  use IndexWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
