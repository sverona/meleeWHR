require 'whole_history_rating'
require 'date'
require 'json'

@whr = WholeHistoryRating::Base.new

tourneys = JSON.load File.open "all_tournaments.json"

def tourney_time(t)
    Time.at t['printouts']['Has start date'][0]['timestamp'].to_i
end

tourneys.sort_by { |name, t| tourney_time(t) }.each do |name, t|
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
                            @whr.create_game(game['p1'].downcase, game['p2'].downcase,
                                             'BW'[game['win'].to_i - 1], date, 0)
                            puts "#{game['p1']}\t#{game['p2']}\t#{game['win']}"
                        end
                    end
                end
            end
        end
    rescue Errno::ENOENT
        puts "No bracket found for #{name}"
    end
end

@whr.iterate(1000)
ratings = Hash.new([])

@whr.players.each do |tag, rates|
    ratings[tag] = @whr.ratings_for_player(tag)
end

puts ratings
rate_list = File.new("ratings_whr.json", "w")
rate_list.write JSON.pretty_generate(ratings)
