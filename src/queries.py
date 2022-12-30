EVENT_QUERY = '''
query TournamentEvents($slug: String!) {
  tournament(slug: $slug) {
    events {
      id
      name
      numEntrants
      videogame {
        id
      }
      teamRosterSize {
        maxPlayers
        minPlayers
      }
      tournament {
        name
        id
      }
    }
  }
}
'''

RESULTS_QUERY = '''
query EventSets($eventId: ID!, $page: Int!) {
  event(id: $eventId) {
    tournament {
      id
      name
    }
    id
    name
    sets(page: $page, perPage: 18, sortType: STANDARD) {
      nodes {
        fullRoundText
        id
        slots {
          standing {
            placement
            stats {
              score {
                value
              }
            }
          }
          entrant {
            id
            name
            participants {
              entrants {
                id
              }
              player {
                id
                gamerTag
                user {
                  slug
                }
              }
            }
          }
        }
      }
    }
  }
}
'''

PLAYERS_QUERY = '''
query ($slug: String!) {
  user(slug: $slug) {
    player {
      id
      gamerTag
    }
    name
    location {
      country
      state
      city
    }
  }
}
'''