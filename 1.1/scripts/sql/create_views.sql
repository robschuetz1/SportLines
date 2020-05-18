drop view v_team_game_summ;
drop view v_game_total_discrepancies;
drop view v_first_downs;


create view v_team_game_summ as 
	select *
	from
	(select group_id,
	game_id,
	season_start,
	week,
	home_team_id as team_id,
	1 as is_home,
	home_team_score,
	home_teak_rank,
	home_team_spread,
	home_team_spread_odds,
	home_team_ml
	from games
	
	union all
	
	select group_id,
	game_id,
	season_start,
	week,
	away_team_id as team_id,
	0 as is_home,
	away_team_score,
	away_team_rank,
	away_team_spread,
	away_team_spread_odds,
	away_team_ml
	from games)
	
	order by season_start desc, week, game_id, team_id
	
;

--declare 

create view v_game_total_discrepancies as 

	with rushing_total as (
		select d.drive_id,
		p.team_id,
		sum(p.adj_yardage) as yardage,
		count(*) as play_count
		from drives d
		left join plays p on p.drive_id = d.drive_id and p.team_id = d.team_id
		where (p.category = 'Rush'
		or (p.category = 'Turnover' and p.description like '%fumble%'))
		and p.description not like '%punt%'
		and p.description not like '%pass%'
		group by d.drive_id, p.team_id
		),

	passing_total as (
		select d.drive_id,
		p.team_id,
		sum(case when p.category = 'Turnover' then 0 else p.adj_yardage end) as yardage,
		count(*) as play_count
		from drives d
		left join plays p on p.drive_id = d.drive_id and d.team_id = p.team_id
		where p.category = 'Pass'
		or (p.category = 'Turnover' and p.description like '%intercept%')
		group by d.drive_id, p.team_id
		)
	
	
	
	select g.season_start,
	g.week,
	g.game_id,
	gt.team_id,
	t.team_abbr,
	b.rush_count as pd_rush_count,
	gt.rush_attempts as gd_rush_count,
	b.rushing_yards as pd_rush_yards,
	gt.rush_yards as gd_rush_yards,
	b.pass_count as pd_pass_count,
	gt.pass_attempts as gd_pass_count,
	b.passing_yards as pd_pass_yards,
	gt.pass_yards as gd_pass_yards
	from games g 
	left join game_yard_totals gt on gt.game_id = g.game_id
	left join 
	(
	select g.game_id,
		d.team_id,
		sum(r.yardage) as rushing_yards,
		sum(r.play_count) as rush_count,
		sum(p.yardage) as passing_yards,
		sum(p.play_count) as pass_count
	from games g
	left join drives d on d.game_id = g.game_id
	left join rushing_total r on r.drive_id = d.drive_id and r.team_id = d.team_id
	left join passing_total p on p.drive_id = d.drive_id and p.team_id = d.team_id
	where /*g.week = 1
	and */ g.game_id != '401121950'
	group by g.season_start, g.week, g.game_id, d.team_id
	order by g.season_start, g.week, g.game_id, d.team_id
	) b on gt.game_id = b.game_id and gt.team_id = b.team_id
	left join teams t on t.team_id = gt.team_id
	
	where b.rush_count is null
	or gt.game_id is null
	or 
	(
--	b.rush_count not between cast(gt.rush_attempts as integer) - run_play_tolerance and cast(gt.rush_attempts as integer) + run_play_tolerance
--	or b.rushing_yards not between cast(gt.rush_yards as integer) -  run_yard_tolerance and cast(gt.rush_yards as integer) + run_yard_tolerance
--	or b.pass_count not between cast(gt.pass_attempts as integer) - pass_play_tolerance and cast(gt.pass_attempts as integer) + pass_play_tolerance
--	or b.passing_yards not between cast(gt.pass_yards as integer) - pass_yard_tolerance and cast(gt.pass_yards as integer) + pass_yard_tolerance
	
	b.rush_count not between cast(gt.rush_attempts as integer) - 3 and cast(gt.rush_attempts as integer) + 3
	or b.rushing_yards not between cast(gt.rush_yards as integer) -  15 and cast(gt.rush_yards as integer) + 15
	or b.pass_count not between cast(gt.pass_attempts as integer) - 3 and cast(gt.pass_attempts as integer) + 3
	or b.passing_yards not between cast(gt.pass_yards as integer) - 30	and cast(gt.pass_yards as integer) + 30
	
	
	--or cast(b.pass_count as text) != gt.pass_attempts
	--or cast(b.passing_yards as text) != gt.pass_yards
	)
	
	group by g.season_start, g.week,  g.game_id, gt.team_id, t.team_abbr, b.rush_count, gt.rush_attempts, b.rushing_yards, gt.rush_yards, b.pass_count, gt.pass_attempts, b.passing_yards, gt.pass_yards
;


create view v_first_downs as 

	select play_id
	category,
	down,
	distance,
	yardage
	from plays
	where yardage > distance

;

create view v_drive_summary as

with rush as (

select game_id,
team_id,
avg(play_count) avg_play_count,
avg(yardage) avg_yardage
from (
select d.game_id,
d.drive_id,
p.team_id,
count(*) play_count,
sum(p.adj_yardage) yardage
from drives d
left join plays p on p.drive_id = d.drive_id
where p.category = "Rush"
group by d.game_id, d.drive_id, p.team_id
) drives
group by game_id, team_id

),

pass as (

select game_id,
team_id,
avg(play_count) avg_play_count,
avg(yardage) avg_yardage
from (
select d.game_id,
d.drive_id,
p.team_id,
count(*) play_count,
sum(p.adj_yardage) yardage
from drives d
left join plays p on p.drive_id = d.drive_id
where p.category = "Pass"
group by d.game_id, d.drive_id, p.team_id
) drives
group by game_id, team_id

),

teams as (

select game_id,
home_team_id team_id,
0 home_flag
from games

union all

select game_id,
away_team_id,
1
from games

order by game_id
)


select g.season_start,
w.week,
d.game_id,
t.team_id,
t.home_flag,
d.start_quarter quarter,
d.start_time time,
case when d.team_id = g.home_team_id then g.away_team_id else g.home_team_id end as other_team,
round(rush.avg_play_count, 3) rush_plays,
round(rush.avg_yardage, 3) rush_yards,
round(pass.avg_play_count, 3) pass_plays,
round(pass.avg_yardage, 3) pass_yards,
d.yards_to_go,
case when d.result = 'TD' then 7
	 when d.result = 'FG' then 3
	 else 0 end as score,
row_number() over (partition by g.game_id, t.team_id order by d.start_quarter, cast (substr(d.start_time,0,instr(d.start_time,':')) as integer) desc) row_num
from weeks w
left join games g on w.week = g.week and substr(w.season_start, 0, 5) = g.season_start
--left join weeks w on w.week_id = g.week_id, d.start_time
left join teams t on g.game_id = t.game_id
left join drives d on d.game_id = g.game_id and d.team_id = t.team_id
left join rush on rush.game_id = d.game_id and rush.team_id = t.team_id
left join pass on pass.game_id = d.game_id and pass.team_id = t.team_id

order by g.season_start desc, w.week, t.game_id, t.team_id, d.start_quarter, cast (substr(d.start_time,0,instr(d.start_time,':')) as integer) desc