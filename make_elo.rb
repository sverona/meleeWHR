require 'whole_history_rating'
require 'date'
require 'json'

@whr = WholeHistoryRating::Base.new(:w2 => 100)

tourneys = JSON.load File.open "all_tournaments.json"

end_date = DateTime.new(2015,1,1,0,0,0)

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

tourneys.sort_by { |name, t| tourney_time(t) }.select{ |name, t| tourney_time(t).to_datetime < end_date }.each do |name, t|
    # puts Date.parse(tourney_time(t).to_s).step(Date.new(2003, 1, 1), 7).to_a
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
                                @whr.create_game(fix(game['p1'].downcase), fix(game['p2'].downcase), 'B', date, 0)
                            end

                            p2.times do |i|
                                @whr.create_game(fix(game['p1'].downcase), fix(game['p2'].downcase), 'W', date, 0)
                            end
                            puts "#{game['p1']}\t#{game['p2']}\t#{game['win']}"
                        end
                    end
                end
            end
        end
    end
end

@whr.iterate(1000)
ratings = Hash.new([])

@whr.players.each do |tag, rates|
    ratings[tag] = @whr.ratings_for_player(tag)
end

puts ratings
rate_list = File.new("ratings_whr_5.json", "w")
rate_list.write JSON.pretty_generate(ratings)
