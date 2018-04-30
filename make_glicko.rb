require 'date'
require 'json'
require 'glicko2'

tourneys = JSON.load File.open "all_tournaments.json"

def tourney_time(t)
    Time.at t['printouts']['Has start date'][0]['timestamp'].to_i
end

def fix(tag)
    changes = {'chu dat' => 'chudat',
               'sephirothken' => 'ken',
               'the moon' => 'la luna',
               'azen zagenite' => 'azen',
               'chillin' => 'chillindude',
               'king' => 'the king',
               'dr. peepee' => 'ppmd',
               'unknown522' => 'ryan ford',
               'el fuego' => 'santiago',
               'smashg0d' => 'rishi',
               'takuto' => 's-royal',
               'luninspectra' => 'lunin',
               'tori' => 'dj combo'
    }
    if changes[tag]
        return changes[tag]
    else
        return tag
    end
end

games = []

tourneys.sort_by { |name, t| tourney_time(t) }.each do |name, t|
    date = Date.new(2003, 1, 1).step(Date.parse(tourney_time(t).to_s), 7).count
    begin
        dir = "./brackets/#{t['fulltext']}"
        Dir["#{dir}/*.json"].each do |bracket_loc|
            unless bracket_loc["Doubles"] or bracket_loc["Pools"] or bracket_loc["Crews"]
                puts bracket_loc
                bracket = JSON.load File.open bracket_loc
                bracket.each do |n, brak|
                    brak.each do |round, game|
                        if game['p1'] and game['p2'] and game['p1'] != 'Bye' and game['p2'] != 'Bye' and game['p1'] != game['p2']
                            p1 = p2 = 0
                            if game['p1score'] and game['p1score'].is_a? Integer
                                p1 = game['p1score']
                            elsif game['p1score'] and (['W', 'advance', 'win'].include? game['p1score']) and game['p2score'] != 'DQ'
                                p1 = 2
                            elsif game['win'] == '1'
                                p1 = 2
                            end

                            if game['p2score'] and game['p2score'].is_a? Integer
                                p2 = game['p2score']
                            elsif game['p2score'] and (['W', 'advance', 'win'].include? game['p2score']) and game['p1score'] != 'DQ'
                                p2 = 2
                            elsif game['win'] == '2'
                                p2 = 2
                            end

                            p1.times do |i|
                                games << [date, [fix(game['p1'].downcase), fix(game['p2'].downcase)], [1, 2]]
                            end

                            p2.times do |i|
                                games << [date, [fix(game['p1'].downcase), fix(game['p2'].downcase)], [2, 1]]
                            end
                        end
                    end
                end
            end
        end
    end
end

puts "Parsed #{games.length} games"

Rating = Struct.new(:id, :rating, :rating_deviation, :volatility)
current_ratings = Hash.new
ratings = Hash.new

num_players = 0

games.group_by {|game| game[0]}.each do |date, games_at_date|
    players = games_at_date.map {|game| game[1]}.flatten.uniq
    puts players.inspect
    players.each do |p|
        if not current_ratings[p]
            current_ratings[p] = Glicko2::Player.from_obj Rating.new(num_players, 1500, 100, 0.06)
            num_players += 1
        end
    end
    puts players.map{ |p| current_ratings[p] }
    period = Glicko2::RatingPeriod.new players.map { |p| current_ratings[p] }
    games_at_date.each do |game|
        puts game.inspect
        game_players = game[1].map { |p| current_ratings[p] }
        puts game_players.inspect
        period.game(game_players, game[2])
    end

    next_period = period.generate_next(0.5)
    next_period.players.each { |p| p.update_obj }
    puts current_ratings
end
