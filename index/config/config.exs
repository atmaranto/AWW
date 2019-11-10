# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

# Configures the endpoint
config :index, IndexWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "ai6r69nxy05JgL+QLt1IkQAQJnUkLD8QBBk8lkVX+cWYXXW095KAQyz0CWd8TrAZ",
  render_errors: [view: IndexWeb.ErrorView, accepts: ~w(html json)],
  pubsub: [name: Index.PubSub, adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
