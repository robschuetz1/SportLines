with rushing_total as (
select d.drive_id,
sum(p.adj_yardage) as yardage,
count(*) as play_count
from cfb_drives d
left join plays p on p.drive_id = d.drive_id
where (p.category = 'Rush'
or (p.category = 'Turnover' and p.description like '%fumble%'))
and p.description not like '%punt%'
group by d.drive_id
),

passing_total as (
select d.drive_id,
sum(case when p.category = 'Turnover' then 0 else p.adj_yardage end) as yardage,
count(*) as play_count
from cfb_drives d
left join plays p on p.drive_id = d.drive_id
where p.category = 'Pass'
or (p.category = 'Turnover' and p.description like '%intercept%')
group by d.drive_id
)

select g.season_start,
g.week,
g.game_id,
d.team_abbr,
sum(r.yardage) as rushing_yards,
sum(r.play_count) as rush_count,
sum(p.yardage) as passing_yards,
sum(p.play_count) as pass_count
from games g
left join cfb_drives d on d.game_id = g.game_id
left join rushing_total r on r.drive_id = d.drive_id
left join passing_total p on p.drive_id = d.drive_id
where g.week = 1
and g.game_id != '401121950'
group by g.season_start, g.week, g.game_id, d.team_abbr
order by g.season_start, g.week, g.game_id, d.team_abbr
;