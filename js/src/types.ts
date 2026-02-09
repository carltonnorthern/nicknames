/**
 * Supported relationship types between names.
 */
export const RELATIONSHIPS = [
    "has_nickname",
] as const;

/**
 * Union type of valid relationship types.
 */
export type Relationship = typeof RELATIONSHIPS[number];

/**
 * A single triple of (canonical name, relationship, nickname).
 *
 * For example: ("robert", "has_nickname", "bob") or ("bob", "is_nickname_of", "robert").
 */
export type NameTriple = [string, Relationship, string];