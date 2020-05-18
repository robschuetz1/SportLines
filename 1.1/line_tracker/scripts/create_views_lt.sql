create view v_money_line as 

select l.game_id,
g.kickoff,
l.home_team_id,
l.away_team_id,
l.favorite_id,
avg(l.spread) spread_avg,
avg(l.money_line) money_line_avg,
l.pulled_time
from lines l
left join games g on g.game_id = l.game_id
where fail_flag = 0
group by l.game_id, g.kickoff, l.home_team_id, l.away_team_id, l.favorite_id, l.pulled_time
order by g.kickoff desc, g.game_id, pulled_time

;

create view v_sharp_moves as 

with previous_row as (
select l.*,
row_number() over (partition by game_id order by pulled_time) + 1 row_num
from v_money_line l
),

current_row  as (
select l.*,
row_number() over (partition by game_id order by pulled_time) row_num
from v_money_line l
),

doubles as (
select game_id,
pulled_time,
count(*) count
from v_money_line
group by game_id, pulled_time
)

select *
from (
select c.game_id,
c.favorite_id,
c.pulled_time,
p.spread_avg spread,
c.money_line_avg - p.money_line_avg dif
from current_row c
left join previous_row p on p.game_id = c.game_id and c.row_num = p.row_num
left join doubles d on d.game_id = c.game_id and d.pulled_time = d.pulled_time
where d.count = 1
)
where abs(dif) > 8
group by game_id, favorite_id, spread, pulled_time, dif
order by game_id, pulled_time
;