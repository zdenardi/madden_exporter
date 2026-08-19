/**
 * PlayerResponse models the core details of a player.
 * Equivalent to Python's PlayerResponse (MaddenDataFromDB).
 */
export interface PlayerResponse {
    age: number;
    college: string;
    firstName: string;
    lastName: string;
    position: string;
    isActive: boolean;
    jerseyNum: number;
    yearsPro: number;
    ratings: Record<string, number>; // Assuming ratings is a dictionary mapping string to number
}

/**
 * PlayerStatBase is the base structure for all player performance statistics.
 * It requires an associated PlayerResponse to identify the athlete.
 * Equivalent to Python's PlayerStat.
 */
export interface PlayerStatBase {
    player: PlayerResponse;
    // Common stats fields that were on PlayerStat in Python (e.g., implicit fields, or future additions)
    // If there are no universal fields, this can remain minimal.
}