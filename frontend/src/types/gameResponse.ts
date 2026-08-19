import { TeamInfoResponse } from "./team";
import type {
  PassingStats,
  RushingStats,
  ReceivingStats,
  DefenseStats,
  KickingStats,
  PuntingStats,
} from "./gameStats";

/**
 * TeamGameResponse aggregates all the statistical records for one team in a single game.
 * Equivalent to Python's TeamGameResponse.
 */
export interface TeamGameResponse {
  team: TeamInfoResponse;
  passingStats: PassingStats[];
  rushingStats: RushingStats[];
  receivingStats: ReceivingStats[];
  defensiveStats: DefenseStats[];
  kickingStats: KickingStats[];
  puntingStats: PuntingStats[];
}

/**
 * GameResponse is the root data structure containing all game details.
 * Equivalent to Python's GameResponse.
 */
export interface GameResponse {
  id: number;
  awayScore: number;
  homeScore: number;
  awayTeam: TeamGameResponse;
  homeTeam: TeamGameResponse;
  status: string;
}
