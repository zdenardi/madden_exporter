import type { GameResponse } from "../types/gameResponse";

export const Game = ({ game }: { game: GameResponse }) => {
  return (
    <div className="game-card bg-white p-5 rounded-xl shadow-md flex flex-col justify-center items-center">
      <div className="w-full scoreboard py-2 border-y border-gray-200 flex flex-col items-center">
        <p className="text-lg font-semibold text-center">
          <span className="text-blue-600">{game.awayTeam.team.cityName}</span>{" "}
          {game.awayScore} <span className="text-gray-400">@</span>{" "}
          {game.homeTeam.team.cityName} : {game.homeScore}
        </p>
      </div>
    </div>
  );
};
