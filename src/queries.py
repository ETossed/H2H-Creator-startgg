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
                
              }
            }
          }
        }
      }
    }
  }
}
'''