EVENT_QUERY = '''
query TournamentEvents($slug: String!) {
  tournament(slug: $slug) {
    events {
      id
      slug
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
query EventSets($slug: String!, $page: Int!) {
  event(slug: $slug) {
    slug
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
        state
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

TOURNAMENTS_BY_TIME_QUERY = '''
query TournamentsByVideogame($page: Int!, $videogameId: [ID!], $after: Timestamp!, $before: Timestamp!) {
  tournaments(query: {
    perPage: 32
    page: $page
    sortBy: "startAt asc"
    filter: {
      past: false
      videogameIds: $videogameId
      afterDate: $after
      beforeDate: $before
    }
  }) {
    nodes {
      name
      id
      slug
      isOnline
      startAt
      endAt
      events {
        name
        id
        slug
        numEntrants
        videogame {
          id
        }
      }
    }
  }
}
'''