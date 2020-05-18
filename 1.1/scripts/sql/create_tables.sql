drop table weeks;
drop table games;
drop table drives;
drop table plays;
drop table weather;
drop table locations;
drop table teams;
drop table people;
drop table boxscore_game_summary;
drop table odds;


create table weeks (

week_id varchar(12),
group_id varchar(5),
season_start varchar(10),
season_end varchar(10),
week varchar(10),
week_start varchar(10),
week_end varchar(10)

);


create table games (

group_id varchar (5),
season_start varchar(4),
week_id varchar(12),
game_id varchar(10),
ht_id varchar(5),
ht_coach_id varchar(5),
ht_rank varchar (5),
ht_score int,
at_id varchar(5),
at_coach_id varchar(5),
at_rank varchar(5),
at_score int,
location_id varchar(5),
date varchar(10),
time varchar(5),
attendance int,
tv_rating real,
ticket_price real,
is_neutral int default 0,
is_gameday int,
is_delay int

);


create table drives (

group_id varchar (5),
game_id varchar(10),
drive_id varchar(15),
o_team_id varchar(5),
d_team_id varchar(5),
start_o_score int,
start_d_score int,
end_o_score int,
end_d_score int,
points_scored int,
start_quarter varchar(2),
start_time varchar(5),
end_quarter varchar(2),
end_time varchar(5),
play_count int,
yards_to_go int,
yards int,
result varchar(30),
is_score int,
is_turnover int

);


create table plays (

group_id varchar(5),
game_id varchar(10),
drive_id varchar(15),
play_id varchar(25),
o_team_id varchar(5),
d_team_id varchar(5),
start_poss_team_id varchar(5),
end_poss_team_id varchar(5),
quarter varchar(2),
start_time varchar(5),
end_time varchar(5),
play_clock varchar(5),
start_yl int,
end_yl int,
down int,
distance int,
yardage int,
adj_yardage int,
category varchar(20),
description varchar(300),
runner varchar(75),
passer varchar(75),
receiver varchar(75),
fumbler varchar(75),
tackler varchar(75),
fumble_forcer varchar(75),
fumble_recov varchar(75),
interceptor varchar(75),
pen_decision varchar(20),
pen_yardage int,
is_pen int,
is_turnover int,
is_score int,
is_rz int,
is_blitz int,
is_zone int

);

create table weather (

game_id varchar(10),
date varchar(10),
time varchar(5),
lat_coordinate real,
lng_coordinate real,
high int,
low int,
precip_chance int,
precip_actual int,
wind_speed int,
wind_dir int,
sunrise varchar(5),
sunset varchar(5)

);


create table locations (

location_id varchar(5),
lat_coordinate real,
lng_coordinate real,
address varchar(50),
city varchar(50),
region varchar(2),
zip varchar(5),
stadium_name varchar(50),
ht_id varchar(5),
capacity int,
year_built varchar(4)

);


create table teams (

group_id varchar(5),
team_id varchar(5),
team_name varchar(40),
team_abbr varchar(10),
team_mascot varchar(40),
location_id varchar(5),
is_superpower int,
bis_flag int

);


create table people (

individual_id varchar(10),
first_name varchar(50),
last_name varchar(50),
team_id varchar(5),
season_start varchar(4),
salary int,
is_coach int

);


create table boxscore_game_summary (

game_id varchar(10),
team_id varchar(5),
is_home int,
score int,
rush_yards int,
rush_plays int,
rush_tds int,
pass_yards int,
pass_plays int,
pass_completions int,
pass_tds int,
fumbles int,
fumbles_lost int,
interceptions int,
penalties int,
pen_yardage int,
time_of_possession varchar(5)

);


create table odds (

odds_id varchar(10),
game_id varchar(50),
source varchar(15),
unit int,
value varchar(5),
ht_id real,
ht_spread real,
ht_spread_odds real,
ht_ml varchar(5),
at_id real,
at_spread real,
at_spread_odds real,
at_ml int

);