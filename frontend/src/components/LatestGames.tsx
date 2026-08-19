import { useQuery } from "@tanstack/react-query";
import { getLatestGames } from "../api/games";
import { Game } from "./Game";

export const LatestGames = () => {
  const { isLoading, error, data } = useQuery({
    queryKey: ["latest-games"],
    queryFn: getLatestGames,
  });

  if (isLoading) return "Loading...";
  if (error) return "An error has occurred: " + error.message;
  if (!data) return "No data";
  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 shadow-lg rounded-xl">
      <h1 className="text-2xl font-bold mb-6 text-center">Latest Games</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
        {data.map((game) => (
          <Game game={game} />
        ))}
      </div>
    </div>
  );
};
