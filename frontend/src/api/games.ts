export async function getLatestGames(): Promise<GameResponse[]> {
  const response = await fetch("http://localhost:5000/api/games/latest");

  if (!response.ok) {
    throw new Error("Failed to fetch games");
  }

  return await response.json();
}
