from client import MCSRRankedAPYClient
import asyncio


async def main():
  client = MCSRRankedAPYClient()
  query = await client.users.get_data("lowk3y_")
  print(query.connections.youtube.id)
  await client.close()

if __name__ == "__main__":
  asyncio.run(main())
