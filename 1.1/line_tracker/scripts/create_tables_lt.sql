create table games (

game_id varchar(10)

);

create table lines (

game_id varchar(10),
home_team_id varchar(5),
away_team_id varchar(5),
odd_maker varchar(50),
favorite_id varchar(5),
spread real,
spread_odds real,
money_line real,
fail_flag int

);
